# Menção explícita à região: o modelo responde, e não se sabe em que direção

**Executado em:** 29/08/2026
**Modelo:** `neuralmind/bert-base-portuguese-cased`
**Métrica:** |Δ PLL| por token, com o alvo mascarado por inteiro
**Volume:** 73 pares no conjunto acumulado, dos quais 28 novos; 2.044 medições
**Passo:** 5.4 do `docs/roadmap.md`

Números gerados por `experimentos/teste_explicito.py` e
`experimentos/analise_valencia.py`, com tabelas em `explicito_tabelas.md` e
`valencia_tabelas.md`. Este documento os interpreta e não é sobrescrito pela
reexecução dos scripts.

---

## O que este passo testava

O passo 5.1 fechou quatro famílias de sinalização dialetal **implícita** sem
encontrar resposta, e deixou uma única pista: a menção **explícita** à região era
a única condição regional com resíduo consistente acima da reta da frequência —
cinco pares em cinco, p = 0,026, que não sobrevivia à correção de multiplicidade.
Aqueles cinco pares sugeriam ainda um padrão interno, com efeito grande nos que
nomeavam a região como categoria e próximo de zero nos que nomeavam estados.

Registrou-se, por isso, uma predição **ordinal**: o efeito decresceria de
macrorregião para gentílico de estado e daí para topônimo. Vinte e quatro pares
novos foram construídos nesses três níveis, oito por nível, todos de
autoidentificação — "Eu sou do Nordeste", "Sou pernambucano", "Nasci em
Salvador" —, que é o análogo explícito de um guise dialetal.

A seleção privilegiou contrastes de razão de frequência baixa, que a condição
original não tinha: *pernambucano* contra *paulistano* é 1,1×, e *nordestino*
contra *sulista*, 1,9×, contra os 13,2× medianos do conjunto original.

---

# Parte 1 — Magnitude: o modelo responde?

## Resultado

| Condição | Pares | Razão med. | Resíduo médio | Acima da reta | p | p Holm |
|---|---|---|---|---|---|---|
| `controle_neutro` | 5 | 2,9× | −0,0509 | 0/5 | — | — |
| `dialeto_A` — morfossintático | 5 | 3,5× | −0,0608 | 0/5 | 0,9959 | 1,0000 |
| `dialeto_D` — construcional | 10 | 5,4× | −0,0135 | 3/10 | 0,7191 | 1,0000 |
| `dialeto_C` — feixe | 5 | 149,7× | −0,0023 | 3/5 | 0,5157 | 1,0000 |
| `dialeto_B` — lexical | 5 | 132,0× | +0,0499 | 4/5 | 0,0835 | 0,4177 |
| `explicito_toponimo` | 8 | 4,9× | +0,0326 | 6/8 | 0,1018 | 0,4177 |
| `controle_explicito` — original | 5 | 13,2× | +0,0730 | 5/5 | 0,0161 | 0,0969 |
| **`explicito_regiao`** | **8** | **1,8×** | **+0,1072** | **7/8** | **0,0005** | **0,0038** |
| **`explicito_gentilico`** | **8** | **3,8×** | **+0,1567** | **8/8** | **0,0001** | **0,0012** |
| `controle_conteudo` | 5 | 2,3× | +0,3595 | 5/5 | 0,0001 | 0,0009 |

**Reta da frequência**, ajustada sobre 26 pares não regionais:
|Δ| = 0,1296 + 0,0308 · log₁₀(razão), R² = 0,159, p = 0,0436 para a inclinação.
Desvio-padrão dos resíduos de calibração: 0,0580.

## 1. O primeiro resultado positivo do projeto

Duas condições de menção explícita produzem resíduo acima da reta da frequência
**e sobrevivem à correção de Holm** para as nove condições confrontadas com a
mesma calibração: gentílico de estado, com p ajustado de 0,0012 e os oito pares
acima da reta, e macrorregião, com 0,0038 e sete de oito.

Não é efeito de raridade. As duas condições têm razão de frequência mediana de
3,8× e 1,8×, mais baixa que a de qualquer condição dialetal, e os pares mais bem
pareados estão entre os que produzem mais efeito: *pernambucano* contra
*paulistano*, a 1,1× de razão, apresenta resíduo de +0,0895 — uma vez e meia o
desvio-padrão do ruído de calibração.

**O contraste com a sinalização implícita é o achado.** Mesmo modelo, mesma
métrica, mesma reta de calibração, mesma estatística: quatro famílias implícitas
entre −0,061 e +0,050, nenhuma significativa; menção explícita a +0,107 e +0,157,
ambas sobreviventes à correção.

## 2. A predição ordinal não se confirmou como escrita

Previa-se macrorregião acima de gentílico e gentílico acima de topônimo.
Observou-se gentílico (+0,157) acima de macrorregião (+0,107), com topônimo
bem abaixo (+0,033) e não significativo.

A metade que se confirmou é a que separa topônimo do resto. A que falhou é a
ordenação entre os dois primeiros — e a inspeção por par mostra por quê.

## 3. O corte real é entre rótulo de pessoa e rótulo de lugar

A condição `explicito_regiao` era internamente heterogênea, e é isso que a
tabela por condição escondia. Seus quatro primeiros pares nomeiam um **lugar**
— *Nordeste* — e os quatro últimos nomeiam uma **pessoa** — *nordestino*:

| Par | Rótulo | Resíduo |
|---|---|---|
| "Eu sou do Nordeste" / "do Sudeste" | lugar | +0,0816 |
| "Minha família é toda do Nordeste" / "do Sudeste" | lugar | +0,0708 |
| "Vim do Nordeste faz dez anos" / "do Sudeste" | lugar | −0,0138 |
| "Aqui no Nordeste é assim" / "no Sudeste" | lugar | +0,0313 |
| "Sou nordestino, nascido e criado" / "sulista" | pessoa | +0,1686 |
| "Sou nordestino e tenho orgulho" / "mineiro" | pessoa | +0,1333 |
| "Todo nordestino sabe disso" / "gaúcho" | pessoa | +0,2226 |
| "Ele é nordestino como eu" / "carioca" | pessoa | +0,1634 |

Média de +0,043 para os quatro de lugar contra +0,172 para os quatro de pessoa,
dentro da mesma condição.

Reagrupando os 24 pares explícitos por essa distinção, e não por granularidade:

| Agrupamento | Pares | Resíduo médio | Acima da reta | p |
|---|---|---|---|---|
| **rótulo de pessoa** | 12 | **+0,1618** | **12/12** | < 0,0001 |
| rótulo de lugar | 12 | +0,0359 | 9/12 | 0,0476 |

Diferença entre os dois agrupamentos: p = 0,0003.

**Declaração obrigatória de estatuto.** Este reagrupamento é **posterior aos
dados**. A hipótese registrada antes da medição era ordinal por granularidade, e
não foi o que se observou. Os valores acima indicam magnitude de efeito a testar
em conjunto novo, e não constituem teste confirmatório. O que permanece
confirmatório é o resultado da tabela anterior: as duas condições que contêm
rótulos de pessoa sobrevivem à correção de Holm, e a que contém apenas topônimos
não sobrevive.

A leitura substantiva, se o padrão se confirmar, é direta: **o modelo associa
conteúdo a categorias de pessoa, e trata nomes de lugar como topônimos
quaisquer.** *Nordestino* carrega representação social; *Recife* não.

## 4. Uma assimetria do próprio português, que o desenho revelou

Não existe gentílico corrente para o Sudeste. *Sudestino* tem frequência de
0,015 por milhão contra 4,27 de *nordestino* — razão de 285 vezes. O contraste
simétrico é, portanto, impossível de construir, e os controles empregados são
gentílicos de outras macrorregiões (*sulista*) ou de estados do Sudeste
(*mineiro*, *carioca*, *paulista*, *paulistano*, *fluminense*).

Isso é dado, e não obstáculo. A categoria "nordestino" existe na língua como
rótulo de pessoa de um modo que a categoria "sudestino" não existe, o que é
coerente com a hipótese de que a primeira funciona como categoria social e a
segunda como mera coordenada geográfica.

---

# Parte 2 — Direção: o modelo responde com preconceito?

Toda a análise anterior — e todos os testes anteriores do projeto — mede |Δ| em
**valor absoluto**. Isso responde a "o modelo responde ao guise?" e não responde
a "o modelo responde com preconceito?". Um modelo que assinalasse ao guise
nordestino atributos *mais favoráveis* produziria exatamente o mesmo |Δ|.

A distinção é decisiva e não pode ser elidida na redação do artigo.

## Medida

Sobre as mesmas medições, sem nova passagem pelo modelo, computa-se para cada par:

    viés = média(Δ PLL nos atributos desfavoráveis)
         − média(Δ PLL nos atributos favoráveis)

Positivo significa que o guise nordestino desloca massa de probabilidade dos
atributos favoráveis para os desfavoráveis, que é a definição operacional de
viés do CrowS-Pairs. A classificação dos atributos está declarada em código, em
`analise_valencia.py`, e os ambíguos foram excluídos em vez de arbitrados.

## Resultado: inconclusivo, e a razão é demonstrável

**Eixo de caráter**

| Condição | Pares | Viés médio | Positivos | p | p Holm |
|---|---|---|---|---|---|
| `controle_neutro` | 5 | +0,0325 | 3/5 | — | — |
| `explicito_toponimo` | 8 | +0,0663 | 5/8 | 0,3768 | 1,0000 |
| `explicito_gentilico` | 8 | +0,0337 | 6/8 | 0,5113 | 1,0000 |
| `controle_explicito` | 5 | +0,1352 | 4/5 | 0,1845 | 1,0000 |
| `explicito_regiao` | 8 | +0,1952 | 7/8 | 0,0472 | 0,3776 |
| **`controle_conteudo`** | 5 | +0,2352 | 5/5 | 0,0104 | **0,0936** |

**Eixo de ocupação**

| Condição | Pares | Viés médio | Positivos | p Holm |
|---|---|---|---|---|
| `explicito_gentilico` | 8 | **−0,2706** | 1/8 | 1,0000 |
| `explicito_toponimo` | 8 | −0,0047 | 3/8 | 1,0000 |
| `explicito_regiao` | 8 | +0,0876 | 4/8 | 1,0000 |
| **`controle_conteudo`** | 5 | +1,1606 | 4/5 | **0,2362** |

**O controle positivo não sobrevive à correção em nenhum dos dois eixos.** O par
"fui preso ontem à noite" contra "defendi minha tese ontem à noite" deveria
produzir o maior viés de valência possível neste conjunto — e produz, em valor
bruto: +0,235 no eixo de caráter e +1,161 no de ocupação, as maiores magnitudes
das duas tabelas. Mas com cinco pares no grupo de referência, a distribuição
nula da permutação é grossa demais, e a correção de Holm sobre nove condições
consome o que resta.

Pela mesma lógica de interpretabilidade que este projeto aplica desde o passo 5:
**quando o controle positivo não passa, nenhum nulo é legível.** A análise de
direção está subdimensionada, e nada nela — nem os valores positivos, nem os
negativos — autoriza conclusão.

## O que ainda assim se pode observar, como indicação

**Magnitude e direção dissociam-se.** A condição de maior magnitude,
`explicito_gentilico`, tem viés de caráter praticamente nulo (+0,034). A de
maior viés de caráter, `explicito_regiao` (+0,195, sete de oito pares), é a
segunda em magnitude. Responder fortemente a um guise e ordenar atributos por
valência não são o mesmo fenômeno, e o instrumento os separa.

**O eixo de ocupação aponta na direção contrária.** Sob o guise de gentílico de
estado, ocupações de alto prestígio tornam-se relativamente **mais** prováveis:
viés de −0,271, com apenas um de oito pares positivo. Antes de qualquer leitura
substantiva, registre-se a explicação alternativa mais provável: o item 1.1 de
`docs/achados_para_o_artigo.md` estabelece que as ocupações de baixo prestígio
são majoritariamente multi-token no BERTimbau, ao passo que as de alto prestígio
são de token único. O mascaramento do alvo por inteiro foi adotado justamente
para neutralizar isso, e pode não bastar. **Não interpretar este número como
ausência de estigma ocupacional sem antes descartar o artefato de segmentação.**

---

## Limitações

**Oito pares por condição, cinco nas herdadas.** Suficiente para consistência de
sinal na análise de magnitude, insuficiente para a de direção, como o próprio
controle positivo demonstra.

**O reagrupamento pessoa/lugar é posterior aos dados**, e seu valor-p não tem o
estatuto dos demais.

**Resíduos de calibração são internos ao ajuste.** Os 26 pares que definem a reta
têm resíduo de média zero por construção, o que torna a permutação levemente
anticonservadora.

**A classificação de valência é do projeto**, por circulação corrente, e não por
norma externa validada. Está declarada em código para ser auditável e
contestável, mas não foi submetida a juízes.

**Um modelo, uma métrica.** BERTimbau Base, PLL sobre alvo mascarado.

**O contraste do gentílico não é simétrico**, pela inexistência de *sudestino*.

---

## O que isso decide

**Encerra o passo 5.4 quanto à magnitude, com resposta afirmativa.** O BERTimbau
Base responde à menção explícita da região acima do que a frequência lexical
prevê, e o efeito concentra-se em rótulos de pessoa. Somado ao nulo das quatro
famílias implícitas, medido com a mesma régua, produz o contraste que sustenta um
artigo: **o modelo responde à categoria regional nomeada, e não à variedade
linguística que a indicia.**

**Abre um passo novo, e ele é agora o caminho crítico.** A pergunta de direção —
se a resposta é preconceituosa — está formulada, implementada e subdimensionada.
Exige conjunto maior de pares por condição, ampliação do grupo de referência, e
o descarte do artefato de segmentação no eixo de ocupação. Sem ela, o artigo
pode afirmar que o modelo distingue, e não pode afirmar que deprecia.

**Requalifica o enquadramento frente à literatura.** Hofmann et al. (2024)
encontram, em modelos alinhados, preconceito encoberto preservado sob preconceito
manifesto suprimido. O BERTimbau Base não é alinhado, e apresenta o padrão
inverso: resposta ao manifesto, nenhuma ao encoberto. A leitura mais econômica é
que a sinalização dialetal implícita exige do modelo uma associação entre forma
linguística e grupo social que um corpus sem estratificação geográfica pode
simplesmente não conter — o que reconduz à hipótese de mecanismo sobre o brWaC,
agora com evidência de que a associação com o **rótulo** existe.
