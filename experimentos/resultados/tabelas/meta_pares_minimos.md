# Meta do conjunto de pares mínimos

Gerado por `experimentos/meta_pares_minimos.py`. Fecha o item 13 do
registro de pendentes de `docs/dataset-spec.md`.

## A pergunta que a meta responde

Não é "quantos pares para detectar o efeito", porque o passo 5.5
estabeleceu que não há efeito de valência a detectar. É **quantos pares
para que a ausência de efeito seja informativa** — a mesma lógica de que
saiu a meta do corpus de áudio, aplicada ao outro conjunto.

Um nulo obtido sem poder não distingue "não há viés" de "não olhamos
direito", e é essa distinção que a seção de Resultados precisa sustentar.

## A decisão, e por que este número

**Excluir efeitos de viés acima de 0.08** em unidade bruta,
equivalente a d = 0.68 desvios-padrão do ruído entre pares
(0.1182). Decidido pela equipe em 29/08/2026. Três razões:

**1. É cerca de metade do artefato que o projeto desmontou.** O falso viés
de tokenização media 0.1952 antes do controle
(`docs/achados_para_o_artigo.md`, item 1.1). Poder excluir 0.08 autoriza a afirmação de que, houvesse viés com metade
da força daquele artefato, ele teria sido detectado. É afirmação verificável,
e não retórica de cautela.

**2. Guarda margem de 2.9 vezes para o
controle positivo**, que produz 0.2352. Uma alegação de
poder é tão boa quanto a distância entre o que se quer excluir e o que o
instrumento comprovadamente detecta.

**3. É alcançável.** Ver a tabela de custo abaixo: descer para 0,059 quase
quadruplica o trabalho por ganho argumentativo pequeno, e subir para 0,095
economiza pouco ao custo de só poder excluir viés grande.

## Custo em pares, por poder de 80%

| Excluir acima de | d | α = 0,05, ref. 50 | α = 0,05, ref. 80 | Holm, ref. 50 | Holm, ref. 80 |
|---|---|---|---|---|---|
| 0.059 | 0.50 | 50 | 36 | inviável | 108 |
| 0.071 | 0.60 | 27 | 22 | 87 | 53 |
| **0.080** | 0.68 | 19 | 17 | 50 | 37 |
| 0.095 | 0.80 | 12 | 11 | 28 | 23 |
| 0.118 | 1.00 | 8 | 7 | 15 | 14 |

**Meta adotada: 37 pares por
condição e 80 pares no grupo de referência não regional.**
Hoje há 8 e 26, respectivamente.

## A restrição que a conta revelou, e não constava de plano anterior

O grupo de referência impõe um **teto** ao que é detectável, qualquer que
seja o número de pares de teste: sua própria incerteza não desaparece.

| Pares de referência | Menor efeito detectável, α = 0,05 | Sob correção de Holm |
|---|---|---|
| 26 (atual) | 0.058 | 0.078 |
| 50 | 0.042 | 0.057 |
| 80 | 0.033 | 0.045 |
| 120 | 0.027 | 0.036 |

Com os 26 pares de referência atuais, **nenhum efeito abaixo
de 0.078 é detectável**
sob correção de multiplicidade, por mais pares de teste que se acrescentem.
O grupo de referência precisa crescer junto com as condições de teste, e
isso não constava de nenhum plano anterior do projeto.

## Volume total implicado

- Com 4 condições de teste: 4 × 37 + 80 = **228 pares** no conjunto.
- Com 5 condições de teste: 5 × 37 + 80 = **265 pares** no conjunto.

Para calibrar, o CrowS-Pairs distribui 1.508 pares. O conjunto proposto
fica em cerca de um sexto disso, com delineamento consideravelmente mais
controlado — calibração explícita da frequência, estatística por
conglomerado e balanceamento de subtokens.

## Restrição de conteúdo, que precede o tamanho

Qualquer conjunto futuro deve **balancear a extensão em subtokens entre os
polos do eixo medido**, sob pena de reproduzir o artefato que produziu viés
aparente a p = 0,049 e o desfez ao ser controlado. No eixo de prestígio
ocupacional o balanceamento é impossível neste modelo, e a medição exige
AUL (`docs/achados_para_o_artigo.md`, itens 1.1 e 1.20).

## Ressalvas

**A conta de poder é a de um teste t de duas amostras**, e o teste
efetivamente empregado é de permutação. A aproximação é adequada para
dimensionamento e tende a ser levemente conservadora.

**O desvio-padrão do ruído vem de 26 pares** e é ele próprio
uma estimativa. Um grupo de referência maior a tornará mais precisa, e a
meta deve ser reconferida quando isso ocorrer.

**A correção de Holm supõe nove condições**, que é o delineamento atual.
Reduzir o número de condições reduz o custo por condição.