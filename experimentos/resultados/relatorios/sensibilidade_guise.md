# Teste de sensibilidade ao guise

**Executado em:** 28/08/2026
**Modelo:** `neuralmind/bert-base-portuguese-cased`
**Métrica:** |Δ PLL| por token, com o alvo mascarado por inteiro
**Volume:** 7 condições × 5 pares × 3 molduras × 8 a 12 atributos = 980 medições

Responde a uma pergunta anterior à de viés: **o BERTimbau responde a guise dialetal?** Sem ela, um resultado nulo seria ininterpretável — "o modelo não trata pior quem fala como nordestino" e "o modelo não percebe a diferença" produzem o mesmo número.

---

## Resultado

| Condição | n | Mediana \|Δ\| | Média \|Δ\| | Sobre o piso |
|---|---|---|---|---|
| `controle_neutro` | 140 | 0,0824 | 0,1316 | 1,00× |
| `dialeto_A` — morfossintático | 140 | 0,0821 | 0,0964 | **1,00×** |
| `dialeto_C` — feixe | 140 | 0,1659 | 0,2211 | 2,01× |
| `dialeto_B` — lexical | 140 | 0,2236 | 0,2852 | 2,71× |
| `controle_explicito` | 140 | 0,2263 | 0,3148 | 2,75× |
| `controle_raridade` | 140 | 0,2306 | 0,2987 | **2,80×** |
| `controle_conteudo` | 140 | 0,5209 | 0,7043 | 6,32× |

---

## 1. A medição funciona

O controle de conteúdo — "fui preso ontem à noite" contra "defendi minha tese ontem à noite" — produz 6,32 vezes o piso, e nenhum de seus cinco pares fica abaixo de 4,06×. O instrumento distingue diferenças reais.

Isso é condição de interpretabilidade, e não detalhe: sem ele, qualquer nulo sobre dialeto seria indistinguível de aparelho quebrado.

## 2. O bloco morfossintático não produz efeito algum

`dialeto_A` fica em 1,00× o piso, e a inspeção por par não deixa margem:

| Par | Sobre o piso |
|---|---|
| *feche* / *fecha* | 1,09× |
| *me diga* / *me diz* | 1,27× |
| *traga* / *traz* | 1,11× |
| *fui não* / *não fui* | 0,70× |
| *sei não* / *não sei* | 0,90× |

Os cinco valores caem dentro da faixa da própria condição neutra, que vai de 0,41× a 1,55×. **Trocar o imperativo ou deslocar a negação move o modelo tanto quanto trocar "porta" por "janela".**

Este é o achado central, e é um resultado positivo sobre ausência de efeito, não uma falha de medição: a condição é frequencialmente pareada — *feche* e *fecha* são ambas comuns — e o instrumento demonstrou capacidade de detectar diferença quando ela existe.

## 3. O bloco lexical mede raridade, não dialeto

`controle_raridade` emprega palavras raras **não regionais**, pareadas por frequência com os itens do instrumento: *chinfrim* (0,081 por milhão) para *arretado* (0,100), *combalido* (0,071) para *aperreado* (0,000), *afoito* (0,120) para *avexado* (0,000).

A correspondência entre as duas condições é quase item a item:

| Par | `dialeto_B` | `controle_raridade` |
|---|---|---|
| 1 | 3,92× | 4,06× |
| 2 | 2,85× | 2,91× |
| 3 | 1,23× | 2,00× |
| 4 | 3,55× | 3,38× |
| 5 | 3,38× | 2,23× |
| **mediana** | **2,71×** | **2,80×** |

Uma condição sem qualquer marcação regional reproduz o efeito do bloco dialetal. **O que `dialeto_B` mede é a perturbação que uma palavra rara causa na probabilidade da sentença**, e não associação regional.

O bloco C, intermediário em 2,01×, é consistente com a mistura de um bloco sem efeito e outro cujo efeito é de raridade.

## 4. A menção explícita também não se separa da frequência

`controle_explicito` produz 2,75×, indistinguível de `controle_raridade`. E os termos que diferem nessa condição carregam assimetria de frequência substancial: *paulista* é 13 vezes mais frequente que *nordestino*, *São Paulo* é 22 vezes mais frequente que *Paraíba*, *Rio* é 13 vezes mais frequente que *Ceará* — razão mediana de 13×.

Não se pode, portanto, ler os 2,75× como associação regional do modelo. É a mesma faixa que qualquer par frequencialmente desbalanceado produz.

**Consequência mais geral:** nesta métrica, a diferença de escore entre dois contextos é dominada pela frequência das palavras que os distinguem. Comparação entre guises só é interpretável se os guises forem **pareados em frequência** — condição que apenas `dialeto_A` satisfazia, e que é justamente onde não há efeito.

## 5. A única pista que sobra

O par *menino* / *cara* apresenta 3,38× com razão de frequência de apenas 7,1× — enquanto seu correspondente no controle, *moço* / *cara*, apresenta 2,23× com razão de 97,8×, já que *moço* (4,90 por milhão) é bem mais raro que *menino* (67,60).

> **Correção, 28/08/2026.** A redação original desta seção atribuía a *moço* a frequência de 0,158 por milhão, e a razão do par não era declarada. O valor fora obtido sobre a forma sem cedilha, *moco*, que a fonte trata como palavra distinta. O valor correto é 4,90, e a razão do par é 97,8×. A direção do argumento não se altera — o par de controle continua tendo razão de frequência muito maior e efeito menor —, mas o número anterior não deve ser citado.

O padrão é o inverso do esperado sob explicação por raridade, e é o único caso em que isso ocorre. Trata-se de um par isolado, e a diferença pode dever-se a semântica — *menino* e *cara* implicam idades distintas do interlocutor —, mas é a única pista de efeito lexical não redutível a frequência, e coincide com a classe de itens que o levantamento de frequência havia apontado como viável: marcadores de alta frequência cuja marcação regional é construcional.

---

## Limitações

**Cinco pares por condição.** As 140 medições por condição não são independentes: derivam de cinco enunciados, três molduras e um conjunto de atributos. A unidade de replicação é o par, e cinco é pouco. Os valores são consistentes entre pares dentro de cada condição, o que ampara a leitura, mas não substitui um conjunto maior.

**Um modelo, uma métrica.** BERTimbau Base, com PLL sobre alvo mascarado. Não foi testado o Large, nem métricas baseadas em representação em vez de probabilidade.

**Sem teste de significância.** Os valores são medianas e razões, não estimativas com intervalo.

---

## O que isso decide

**Elimina a conduta (c)** da seção 8 de `docs/pares_minimos_v1.md`, de reposicionar o instrumento sobre a morfossintaxe: não há sinal ali para medir.

**Esvazia a conduta (a)**, de manter o bloco lexical: seu efeito é de raridade.

**Restringe a conduta (b)** a uma forma específica: marcadores lexicais **pareados em frequência** com seus correspondentes de controle, o que exclui todo o repertório atual e aponta para marcadores construcionais de alta frequência.

**E impõe uma pergunta nova:** se nenhum guise frequencialmente pareado produzir efeito, o desenho *matched-guise* não é aplicável ao BERTimbau Base com esta métrica, e a decisão passa a ser entre trocar de modelo, trocar de métrica, ou reposicionar o artigo.
