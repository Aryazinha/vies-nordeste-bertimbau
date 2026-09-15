# Plano — AUL para o eixo de prestígio ocupacional

**Item 18 do plano de fechamento** (`docs/roadmap.md`). Escrito em 15/09/2026 para uma sessão futura dedicada exclusivamente a este trabalho, que começa sem o histórico da conversa em que foi planejado.

**Condição de início:** o dataset v1 está concluído, com a marca `dataset-v1.0` aplicada (`docs/criterio_conclusao_v1.md`), **e há tempo antes da submissão do primeiro artigo**. Decisão da equipe de 15/09/2026: retomar ao final, caso haja tempo, para entregar o dataset mais completo. Se a v1 não estiver concluída, este trabalho não começa.

---

## 1. Objetivo, em uma frase

Medir se o BERTimbau associa o falante nordestino a ocupações de prestígio mais baixo, empregando a métrica AUL, única viável neste eixo, e com isso **retirar a limitação** "eixo ocupacional sem medição válida" do artigo — ou, se a métrica não se validar, **registrar a tentativa** como resultado de método.

---

## 2. Por que o eixo não foi medido

A análise de direção (`experimentos/analise_valencia.py`) compara a probabilidade de atributos desfavoráveis e favoráveis sob o enunciado nordestino e sob o de controle. Nos pares, cada enunciado é seguido da moldura **T2** — *"Quem falou isso trabalha como ___."* — e o modelo pontua dez ocupações:

| Grupo | Ocupações | Subtokens no BERTimbau |
|---|---|---|
| alto prestígio | *médico*, *advogado*, *professor*, *juiz* | 1, 1, 1, 1 |
| baixo prestígio | *empregada*, *pedreiro*, *lavrador*, *faxineiro* | 1, 2, 2, 4 |
| excluídas (prestígio intermediário) | *vendedor*, *motorista* | — |

A métrica empregada em todo o projeto é o **PLL com o atributo mascarado por inteiro** (`experimentos/metricas.py`, `Medidor._pll`): esconde-se a ocupação e mede-se a probabilidade de o modelo recuperá-la. A probabilidade de uma palavra fragmentada não é comparável à de uma palavra inteira, e a fragmentação **acompanha o eixo medido**: no vocabulário do modelo, das 16 ocupações de alto prestígio testadas, 15 são palavra inteira; das 20 de baixo prestígio, apenas 3 (`docs/achados_para_o_artigo.md` 1.1).

O controle usado no eixo de caráter — restringir a análise a atributos de token único — **não é executável aqui**: sobraria *empregada* sozinha no grupo de baixo prestígio, e ela é também a única do feminino, trocando um confundidor por outro (achados 1.20).

Os valores já calculados neste eixo por PLL — inclusive −0,2706 na condição de gentílico — **não podem ser citados em direção alguma**.

---

## 3. O que é o AUL

*All Unmasked Likelihood*, de Kaneko e Bollegala (2022), `docs/referencias.bib`, chave `kaneko2022unmasking`. O modelo recebe a frase **sem máscara alguma** e atribui log-probabilidade a cada token numa única passagem; o escore é a média. A variante **AULA** pondera cada posição pela atenção que recebe. Os autores a propõem justamente para atributos de mais de um token e para atenuar o viés de frequência do PLL.

---

## 4. O que já existe no código

`experimentos/metricas.py`, classe `Medidor`, método `escore(texto, alvo, apenas_pll=False)`, devolve quatro valores:

| Campo | O que é | Situação conhecida |
|---|---|---|
| `pll` | atributo mascarado por inteiro | métrica de todas as medições do projeto |
| `aul` | AUL restrito às posições do atributo | **satura**: com o token à mostra, o modelo o copia; diferenças da ordem de 10⁻⁴, indistinguíveis de ruído |
| `aula` | AUL restrito, ponderado por atenção | mesma saturação |
| `aul_sentenca` | AUL sobre a sentença inteira | recupera sensibilidade, mas mistura o efeito do guise com o comprimento da sentença |

**Nenhuma medição AUL foi guardada.** As medições do projeto chamam `escore(..., apenas_pll=True)` (`experimentos/teste_construcional.py`, função `medir`), e `explicito_bruto.json` só contém PLL. O modelo já é carregado com `attn_implementation="eager"`, exigido pela AULA.

---

## 5. O problema de método a resolver primeiro

O AUL restrito ao atributo não serve (satura). O AUL sobre a sentença serve, mas precisa ser validado quanto a dois confundidores:

1. **O enunciado entra na conta.** A sentença inclui o rótulo — *cearense* num lado, *paulista* no outro —, e a diferença de probabilidade desses tokens aparece em todos os atributos. No escore de direção (média sobre baixo prestígio menos média sobre alto), esse termo **tende a se cancelar**, por ser comum aos dois grupos; mas a média por token dilui o termo de forma diferente conforme o comprimento do atributo, e o cancelamento deixa de ser exato.
2. **O comprimento do atributo.** *faxineiro* acrescenta quatro tokens à sentença; *juiz*, um. Se a diferença entre os lados do par variar com o número de tokens do atributo, o AUL reproduz, por outra via, o artefato que se quer evitar.

**Variantes candidatas**, a comparar antes de qualquer leitura de resultado:

| Variante | Definição | Motivação |
|---|---|---|
| V1 | `aul_sentenca`, média por token, como implementada | ponto de partida disponível |
| V2 | soma, e não média, das log-probabilidades da sentença | torna exato o cancelamento do termo do enunciado no escore de direção |
| V3 | AUL sobre as posições **fora** do enunciado — moldura e atributo | exclui o rótulo da conta por construção |
| V4 | AULA sobre a sentença | referência de Kaneko e Bollegala |

---

## 6. Passos

### A0 — Preparação

Branch própria. Confirmar a marca `dataset-v1.0`. Ler `experimentos/metricas.py`, `experimentos/teste_construcional.py` (função `medir`), `experimentos/analise_valencia.py` e os itens 1.1, 1.19 e 1.20 de `docs/achados_para_o_artigo.md`.

### A1 — Medir

Estender a medição para gravar, **apenas na moldura T2** e nos seus dez atributos, os escores das variantes da seção 5, para os **306 pares**. São 3.060 medições de atributo. **Gravar em arquivo novo** — por exemplo `experimentos/resultados/dados/aul_ocupacional_bruto.json` —, **sem tocar** `explicito_bruto.json`, que sustenta os resultados publicados. Manter a associação da medição ao par pela mesma chave `(condicao, par)`.

**Custo estimado.** A conferência de 14/09/2026 mediu 140 medições de PLL em 44 s em processador. As variantes de AUL exigem de uma a duas passagens adicionais por medição; a estimativa é de 30 a 60 minutos locais, ou menos no Colab (`notebooks/medir_calibracao_colab.ipynb` serve de modelo, inclusive a conferência de reprodutibilidade).

### A2 — Escolher a variante, sem olhar as condições de teste

A escolha usa **apenas** o grupo de referência (86 pares não regionais), o controle neutro e o controle de conteúdo. Três critérios, nesta ordem:

1. **Controle positivo.** O controle de conteúdo (*Fui preso* / *Defendi minha tese*) deve produzir escore de direção sobrevivente à correção contra o grupo de referência.
2. **Sanidade.** O controle neutro, testado contra o grupo de que faz parte, não deve ser significativo.
3. **Independência do comprimento.** No grupo de referência, a diferença entre os lados do par, por atributo, **não deve variar com o número de subtokens do atributo** — regressão de |d| sobre o número de subtokens, com inclinação compatível com zero.

A variante aprovada é a que satisfaz os três. Se mais de uma satisfizer, prefere-se a de menor dependência do comprimento; se nenhuma, ver A6.

### A3 — Registro prévio

Antes de rodar a análise sobre as condições de teste, registrar em `docs/pendencias.md` e versionar num commit: a variante escolhida e o resultado dos três critérios; a análise, idêntica à de `analise_valencia.py` (escore de direção por par, permutação contra o grupo de referência, correção de Holm sobre as condições, verificação de sanidade); e as regras de leitura, no molde das de `docs/pendencias.md` 2.12 — viés detectado, viés acima de um limiar excluído, ou inconclusivo. O limiar a excluir é decisão da equipe.

### A4 — Analisar

Rodar a análise de direção no eixo ocupacional com a variante aprovada, sobre todas as condições de teste.

### A5 — Registrar e atualizar

Tabela em `experimentos/resultados/tabelas/`. Reescrever o item 1.20 de `docs/achados_para_o_artigo.md` com o resultado, proposto ao usuário antes de aplicar. Atualizar `docs/criterio_conclusao_v1.md` (seção 3, retirando ou requalificando a limitação), a ficha do conjunto e `CLAUDE.md`. As medições entram como **versão 1.1 das medições**, sem alterar o conteúdo nem a marca da v1.

### A6 — Critério de abandono

Se nenhuma variante satisfizer A2, **parar**. A limitação permanece, e registra-se como resultado de método: *o AUL, nas variantes testadas, não permitiu medir o eixo ocupacional neste modelo*, com os critérios que falharam. É contribuição legítima, na mesma linha do item 1.1. Não afrouxar os critérios para obter uma variante aprovada.

---

## 7. Riscos e cuidados

- **Não misturar métricas.** Resultados por AUL não se combinam com os de PLL na mesma tabela nem na mesma afirmação.
- **A classificação de prestígio é do projeto** e não foi validada por juízes; declarar, como no eixo de caráter.
- **Gênero gramatical:** *empregada* é o único atributo feminino; examinar o resultado com e sem ela.
- **Poder:** com 20 frases por condição de menção explícita, a análise de direção no eixo de caráter só exclui vieses a partir de cerca de 0,10; o eixo ocupacional tem dispersão maior (desvio-padrão do grupo de referência de 0,39 por PLL), e o limiar alcançável deve ser calculado antes do registro prévio.
- **Escopo:** este trabalho não reabre nenhuma decisão da v1. Ideias surgidas durante ele vão a `docs/pendencias.md`.

---

## 8. Como conduzir com o usuário

As preferências listadas em `docs/retomada_fechamento_v1.md`, seção 8, valem aqui: linguagem simples na conversa, documentos formais, plano com numeração estável — os passos deste documento são A0 a A6 —, branch por conjunto de alterações e merge só com pedido explícito. Explicar o propósito antes do procedimento: o usuário decidiu por este trabalho para **entregar o dataset mais completo**, e deve entender, antes de cada passo, o que ele acrescenta.
