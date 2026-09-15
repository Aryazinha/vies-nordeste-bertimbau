# Retomada — fechamento do dataset v1

**Para quem é este documento:** a próxima sessão de trabalho, que começa sem o histórico da conversa em que o fechamento foi planejado. Escrito em 15/09/2026. Lido este arquivo, a sessão deve ser capaz de conduzir o restante do fechamento sem perguntar ao usuário o que já foi decidido.

**Para o AUL do eixo ocupacional**, que é trabalho distinto e posterior, o documento é `docs/plano_aul_eixo_ocupacional.md`.

---

## 1. Onde o projeto está

O projeto investiga viés regional no BERTimbau e produz **dois conjuntos de dados**, objeto de um **primeiro artigo, de recurso e método**. Um segundo artigo, de análise de sentimento, virá depois e não é tratado aqui.

| Conjunto | Situação em 15/09/2026 |
|---|---|
| **Pares mínimos** | **Concluídos para a v1.** 306 pares medidos no BERTimbau, esquema 1.3, validação registrada em cada par. Nada a criar, medir ou validar. |
| **Corpus de fala** | **Coleta concluída; validação por fazer.** 83 arquivos, 7,96 h, 216 falantes distintos, transcrições anonimizadas. Faltam três validações de trabalho humano. |

O escopo da v1 está **congelado** pelo critério de conclusão aprovado em 15/09/2026: `docs/criterio_conclusao_v1.md`. Nada entra além do que ali está, salvo decisão expressa do usuário.

---

## 2. Leitura obrigatória, nesta ordem

1. `docs/criterio_conclusao_v1.md` — as condições que faltam (C4, C5, C6, D1, D2, D4, D5), as limitações declaradas e o que fica de fora.
2. `docs/roadmap.md`, seção **"Plano de fechamento do dataset v1"** — os 18 itens, de **numeração estável**, com responsável, situação e dependências. É a fonte do plano; não criar numeração paralela.
3. `docs/plano_corpus/03-validar.md` — as três frentes de validação do corpus, com seus scripts.
4. `docs/pendencias.md`, itens 2.14 e 2.15 — a validação dos pares sem juízes e a dispersão da documentação.

`CLAUDE.md` é carregado automaticamente e resume o estado; `docs/achados_para_o_artigo.md` só precisa ser lido se alguma tarefa tocar resultados.

---

## 3. Estado do repositório

- Branch principal: `main`. O usuário exige **branch por conjunto de alterações** e **merge só com pedido explícito**, a cada vez.
- Esta retomada e o plano do AUL foram criados na branch `retomada-e-plano-aul`, enviada ao GitHub **sem merge**. **Primeira ação da sessão:** perguntar ao usuário se integra essa branch à `main`.
- `CLAUDE.md` está fora do versionamento (`.gitignore`); decidir se passa a ser versionado é parte do item 17.
- Áudio e transcrições ficam em `pipeline_coleta_piloto/dataset_raw/`, fora do versionamento. **Nunca versionar trecho de transcrição**; arquivos versionados levam só contagens, identificadores de vídeo e instantes.

---

## 4. O que falta, com os números do plano

| # | Item | Quem | Depende de |
|---|---|---|---|
| **5** | Regerar a amostra do WER sobre os 83 arquivos — **concluído em 15/09/2026** | sessão | — |
| **6** | Gerar a amostra de coerência dialetal, 10 locutores por estado — **concluído em 15/09/2026** | sessão | — |
| **9** | Ouvir 2 arquivos: participação de ouvinte (cerca de 15 min) | usuário | — |
| **10** | Ouvir os 60 locutores da amostra de coerência (cerca de 1 h) | usuário | 6 |
| **11** | Transcrever à mão os trechos da amostra do WER (8 a 16 h) | usuário | 5 |
| **12** | Consultar a orientação sobre comitê de ética | usuário | — |
| **7** | Fechar a ficha do conjunto | sessão | 9, 10, 11 |
| **17** | Consolidar a documentação | sessão | — |
| **18** | AUL do eixo ocupacional — **só depois da v1, se houver tempo** | outra sessão | v1 concluída |

**Ordem sugerida:** 5 e 6 primeiro, porque destravam o trabalho humano; em seguida, o usuário faz 9 (curto) e 10, e começa 11 (longo, divisível por estado); 12 corre em paralelo; 7 e 17 por último; então o ato de conclusão (seção 7 deste documento).

---

## 5. Itens da sessão: como fazer

### Itens 5 e 6 — executados em 15/09/2026

A branch `retomada-e-plano-aul` foi integrada à `main` no início da sessão. As duas amostras foram geradas localmente, e o registro completo está em `docs/plano_corpus/03-validar.md`, "Amostras geradas em 15/09/2026". Decisões e ajustes: **trechos com nome mascarado excluídos da amostra do WER**, por decisão da equipe; `preparar_amostra_wer.py` criado para reproduzir a seção 6.4 sem Colab; `preparar_amostra_coerencia.py` revisto para ler os registros anonimizados e sortear pessoas, e não rótulos. Arquivos: `dataset_raw/amostra_wer.json` (trechos `PB-001`…) e `dataset_raw/diarizacao/coerencia_{UF}.json` (pessoas `COE-PB-01`…). A composição por camada da amostra do WER difere entre estados, e a leitura do item 11 deve considerá-lo (`docs/pendencias.md` 4.11). O texto abaixo, das duas subseções, fica como histórico do planejamento.

### Item 5 — amostra do WER

**Situação.** `amostra_wer.json` foi sorteado quando o corpus tinha 52 arquivos; precisa ser regerado sobre os 83.

**Onde está a lógica.** Seção "6.4 Amostra para transcrição manual" de `notebooks/piloto_colab.ipynb`: trechos de pelo menos 5 s, sorteio com semente `20260827`, até 20 minutos por estado, com `hipotese_asr` preenchida e `referencia_manual` em branco. O cálculo é de `pipeline_coleta_piloto/medir_wer.py --entrada amostra_wer.json`.

**Recomendação.** Os registros estão na máquina local (`dataset_raw/registros_anonimizados/`), e a amostra não exige GPU. Escrever um script local que reproduza exatamente a lógica da seção 6.4, em vez de pedir ao usuário que abra o Colab.

**Duas decisões a tomar antes de gerar, e a levar ao usuário:**

1. **Registros anonimizados ou originais.** Nos anonimizados, nomes de terceiros viram `[NOME_1]`. Se a amostra sair deles, a transcrição manual precisa usar a mesma marcação onde houver nome, ou o WER contará a máscara como erro. Alternativa: excluir da amostra os trechos com máscara. Verificar se os registros originais (`registros_finais`) existem localmente ou só no Drive.
2. **Onde gravar.** A amostra contém transcrição e fica em `dataset_raw/`, fora do versionamento.

**Convenção da transcrição manual (item 11), já fixada em `03-validar.md` §3.1:** digitar exatamente o que foi dito, sem corrigir gramática e sem expandir números por extenso, na mesma convenção ortográfica da transcrição automática.

### Item 6 — amostra de coerência dialetal

```bash
cd pipeline_coleta_piloto
python preparar_amostra_coerencia.py --estado PB --n 10
python preparar_amostra_coerencia.py --estado PE --n 10
python preparar_amostra_coerencia.py --estado CE --n 10
python preparar_amostra_coerencia.py --estado BA --n 10
python preparar_amostra_coerencia.py --estado SP --n 10
python preparar_amostra_coerencia.py --estado RJ --n 10
```

O script recorta o segmento mais longo de cada locutor e gera planilha com veredito em aberto: `coerente`, `suspeito` ou `inconclusivo`. **Ler o cabeçalho do script antes de rodar:** ele foi escrito para o ambiente de processamento, e o áudio hoje está na máquina local (`03-validar.md` §3.2 afirma que roda localmente); confirmar caminhos de entrada e de saída.

### Item 7 — ficha do conjunto

`docs/ficha_conjunto.md` está preliminar. Incorporar: WER por estado (C6), resultado da coerência dialetal (C5), participação de ouvinte (C4), validação dos pares e as limitações da seção 3 do critério de conclusão.

### Item 17 — consolidação da documentação

Conteúdo em `docs/pendencias.md` 2.15: um único documento de resultados, com os demais remetendo a ele; histórico de pendências resolvidas movido para arquivo próprio; aviso de "histórico" nos documentos superados (entre eles `docs/pares_minimos_v1.md` e `AUDITORIA.md`); decisão do usuário sobre versionar `CLAUDE.md`. **Não** unificar as listas de pares no código — isso é fase posterior, por risco de deslocar medições.

---

## 6. Itens do usuário: como conduzir

O usuário **não tem formação técnica em aprendizado de máquina** e pede explicações simples. A sessão deve montar o passo a passo **concreto**, e não descrever a tarefa em abstrato.

### Método que funcionou em 15/09/2026, e deve ser repetido

Na conferência dos trechos da validação dos pares, a instrução em forma de arquivo com colunas a preencher **confundiu o usuário**. O que funcionou:

1. trazer os itens **para a conversa**, cada um com **código estável** (`VIS-1`, `NEG-3`…);
2. agrupar por pergunta, com **uma pergunta simples por grupo** e **um exemplo resolvido**;
3. pedir que o usuário mande **só os códigos que não valem**, contando o resto como válido;
4. comparar com a leitura da própria sessão, dizer onde concorda e onde discorda, e **deixar a decisão com o usuário**;
5. registrar as decisões em arquivo versionado **sem reproduzir transcrição**.

### Item 9 — participação de ouvinte

Rodar `python balanco_participacao.py` para listar os arquivos de canal com o formato (em 14/09/2026 eram dois: um em PE, um na BA). Para cada um, dizer ao usuário **qual arquivo abrir e em que trecho**, e fazer uma pergunta: *há ouvinte participando por telefone ou mensagem de voz? quanto tempo, aproximadamente?* Verificar no script onde o campo `participacao_ouvinte` é gravado, e gravá-lo com a resposta.

### Item 10 — coerência dialetal

Para cada um dos 60 locutores, informar arquivo e instante do segmento recortado, e perguntar: *essa pessoa soa como alguém daquele estado?* Respostas: `coerente`, `suspeito`, `inconclusivo`. Pode ser feito por estado, em seis blocos. Lembrar ao usuário a direção da ameaça: um falante nordestino migrado, gravado como paulista, esconde diferença entre as regiões.

### Item 11 — transcrição para o WER

É o item mais longo e o de maior valor: o WER por estado é resultado publicável. Dividir por estado, e dizer ao usuário que pode ser feito em sessões curtas e por mais de uma pessoa. Dar a convenção da seção 5 com exemplos. Ao final, rodar `medir_wer.py`, reportar **por estado** e comparar Nordeste com Sudeste, **qualquer que seja o resultado**.

### Item 12 — orientação

Pergunta a levar: consulta a pessoas, se vier a ocorrer (juízes como reforço), exige comitê de ética? Se não houver consulta, registrar "não se aplica". Registrar a resposta em `docs/questoes_para_orientacao.md` — é a condição D4.

---

## 7. Ato de conclusão da v1

Satisfeitas todas as condições de `docs/criterio_conclusao_v1.md`:

1. atualizar `CLAUDE.md`, `README.md` e `docs/roadmap.md` para "v1 concluída";
2. pedir ao usuário autorização para o merge final;
3. aplicar a marca `dataset-v1.0` ao commit de conclusão, com autorização expressa.

Só então o item 18 (AUL) pode começar, em sessão própria, e só se houver tempo antes da submissão.

---

## 8. Preferências do usuário, a respeitar em toda a sessão

- **Conversa em linguagem simples**, sem jargão, com exemplo concreto; **documentos do repositório em registro acadêmico formal**.
- **Um plano único, com numeração estável.** Referir-se aos itens pelos números do plano; item novo recebe o número seguinte. Instruções de execução usam **rótulo estável** — nome de seção, de arquivo, de função —, nunca posição de célula ou de linha.
- **Branch por conjunto de alterações; merge só com pedido explícito**, a cada vez; apagar a branch depois do merge.
- **Toda pendência nova vai a `docs/pendencias.md`** no momento em que surge.
- **O dataset é a prioridade**; não desviar para refinamento de instrumento. **Escopo congelado:** ideia nova vai a pendências com destino "fase posterior".
- **Antes de escrever trecho de artigo, consultar `docs/achados_para_o_artigo.md`** — há formulações vedadas.
- O usuário pede, com frequência, **"o que isso significa?" e "para que serve?"**. Responder com o propósito antes do procedimento.
- Visualização do plano, fora do repositório: https://claude.ai/artifact/7fHCS2WfMGEBYUnu76VrrR — a fonte continua sendo `docs/roadmap.md`.
