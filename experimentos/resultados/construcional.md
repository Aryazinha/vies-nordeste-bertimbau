# Marcadores construcionais, e a frequência que não explica tanto quanto se supunha

**Executado em:** 28/08/2026
**Modelo:** `neuralmind/bert-base-portuguese-cased`
**Métrica:** |Δ PLL| por token, com o alvo mascarado por inteiro
**Volume:** 45 pares, 1.260 medições, das quais 616 novas
**Passo:** 5.1 do `docs/roadmap.md`

Números gerados por `experimentos/teste_construcional.py`, com tabelas em
`construcional_tabelas.md`. Este documento os interpreta e não é sobrescrito
pela reexecução do script.

---

## O que este teste responde

O teste anterior (`sensibilidade_guise.md`) deixou uma pista única: o par
*menino* / *cara* produzia efeito maior que seu correspondente de controle,
apesar de razão de frequência menor — o inverso do previsto pela explicação por
raridade. A pista apontava para uma classe de marcador que o levantamento de
frequência havia identificado independentemente: itens **de frequência atestada
cuja marcação regional está na construção**, e não na raridade da palavra.

A hipótese sob teste é, portanto: *existe sinal dialetal em marcadores
construcionais, invisível para os marcadores lexicais raros e para os
morfossintáticos?*

## Por que o desenho mudou

Comparar medianas entre condições, como no teste anterior, não decidiria a
questão. Uma condição dialetal e um controle de raridade com o mesmo perfil de
frequência produzem o mesmo número por construção, e o pareamento perfeito de
frequência — que resolveria o problema — é inalcançável para marcadores
construcionais: os melhores candidatos apresentam razão de 5 a 11 vezes, faixa
em que o próprio controle de menção explícita já produzia efeito apreciável.

Adotou-se, em lugar do pareamento, a **calibração da lei de frequência**:

1. Ajusta-se |Δ| mediano contra log₁₀ da razão de frequência **apenas sobre
   pares não regionais** — 22 deles, com razões espalhadas de 1,0× a 2.883×. A
   reta resultante é a resposta do modelo à raridade, e nada mais.
2. Para cada par dialetal, mede-se o **resíduo** contra essa reta. Resíduo em
   torno de zero significa que o par não faz nada que a frequência já não
   explique. Resíduo positivo é sinal a investigar.

A razão de frequência é calculada por código a partir dos próprios enunciados —
diferença de multiconjunto entre os dois lados, média geométrica de cada lado —,
e não digitada a partir de consulta avulsa. Pares que diferem apenas na **ordem**
das palavras, como *fui não* contra *não fui*, recebem razão 1,0: são o
pareamento de frequência perfeito, e não casos indefinidos como a primeira versão
do código os tratava.

Toda estatística opera no nível do **par**, e não da medição: as 28 medições de
um par compartilham o enunciado e não são independentes.

---

## Resultado

| Condição | Pares | Mediana \|Δ\| | Sobre o piso | Razão med. | Resíduo médio | Acima da reta | p | p Holm |
|---|---|---|---|---|---|---|---|---|
| `controle_neutro` | 5 | 0,1026 | 1,00× | 2,9× | −0,0506 | 0/5 | — | — |
| `controle_frequencia` | 12 | 0,1360 | 1,33× | 3,0× | +0,0014 | 7/12 | — | — |
| `controle_raridade` | 5 | 0,2399 | 2,34× | 43,7× | +0,0474 | 3/5 | — | — |
| `dialeto_A` — morfossintático | 5 | 0,0901 | 0,88× | 3,5× | −0,0608 | 0/5 | 0,9900 | 1,0000 |
| `dialeto_B` — lexical | 5 | 0,2786 | 2,72× | 132,0× | +0,0447 | 4/5 | 0,1266 | 0,5064 |
| `dialeto_C` — feixe | 5 | 0,1639 | 1,60× | 149,7× | −0,0063 | 3/5 | 0,5671 | 1,0000 |
| **`dialeto_D` — construcional** | **10** | **0,1186** | **1,16×** | **5,4×** | **−0,0141** | **3/10** | **0,7129** | **1,0000** |
| `controle_explicito` | 5 | 0,2094 | 2,04× | 13,2× | +0,0711 | **5/5** | **0,0260** | 0,1300 |
| `controle_conteudo` | 5 | 0,5209 | 5,08× | 2,3× | +0,3597 | **5/5** | **0,0000** | **0,0003** |

**Reta da frequência:** |Δ| = 0,1281 + 0,0340 · log₁₀(razão), com R² = 0,180 e
p = 0,0493 para a inclinação. Desvio-padrão dos resíduos de calibração: 0,0618.

> **Comparação com o relatório anterior.** A coluna "sobre o piso" não é
> diretamente comparável à tabela de `sensibilidade_guise.md`. Lá o piso e as
> medianas eram calculados sobre medições individuais; aqui ambos são calculados
> sobre medianas de par, que é a unidade de replicação correta. A ordenação das
> condições não se altera; as magnitudes, sim.

---

## 1. O método funciona, e isso precisa ser verificado antes de tudo

O controle de conteúdo proposicional apresenta resíduo de +0,3597, com os cinco
pares acima da reta e p = 0,0003 depois da correção de Holm. É efeito grande
onde a frequência prevê efeito pequeno — a razão mediana da condição é de apenas
2,3×, porque trocar "fui preso" por "defendi minha tese" substitui palavras
comuns por outras palavras comuns.

A verificação não é cerimônia. Se a análise do resíduo não acusasse esta
condição, seria a análise que estaria quebrada, e nenhum nulo nas demais
condições poderia ser interpretado.

## 2. Os marcadores construcionais não produzem sinal

`dialeto_D` apresenta resíduo médio de −0,0141 e três de dez pares acima da
reta, com p = 0,71. A hipótese do passo 5.1 não se confirma.

**A pista original não replica.** O par que motivou o teste era o vocativo
*menino* contra *cara*. Ele reaparece aqui com resíduo positivo, de +0,0443 —
mas seu irmão, o vocativo *rapaz* contra o mesmo *cara*, apresenta −0,0846, o
maior resíduo negativo da condição. Mesma construção, mesmo termo de comparação,
sinais opostos. O que no teste anterior parecia efeito de uma classe de
marcadores é, à luz de dez pares, variação entre itens.

| Construção | Razão | Resíduo |
|---|---|---|
| avaliativo *massa* | 1,9× | +0,0927 |
| *toda vida* com valor de sempre | 1,2× | +0,0832 |
| vocativo *menino* dirigido a adulto | 7,1× | +0,0443 |
| *lhe* acusativo de 2ª pessoa | 5,4× | −0,0203 |
| durativo *tá com* | 1,5× | −0,0412 |
| comitativo com *mais* | 19,7× | −0,0436 |
| *lhe* dativo de 2ª pessoa | 5,4× | −0,0442 |
| clivagem interrogativa *que foi que* | 2,9× | −0,0566 |
| *tu* com verbo não flexionado | 8,3× | −0,0702 |
| vocativo *rapaz* | 11,0× | −0,0846 |

Nenhum dos dez resíduos alcança 1,5 desvio-padrão do ruído de calibração
(0,0618). Os três positivos merecem uma ressalva que os enfraquece ainda mais:
os dois maiores são justamente os pares em que o lado nordestino é
**semanticamente anômalo** sob leitura padrão — *massa* lido como substantivo,
*toda vida* não disponível com valor adverbial fora da variedade. É mais
econômico atribuí-los a estranheza semântica que a reconhecimento de dialeto.

Os marcadores gramaticais melhor documentados da condição — *lhe* de segunda
pessoa, *tu* sem flexão, comitativo com *mais* — estão todos abaixo da reta.

## 3. A negação pós-verbal é o caso mais limpo, e é nulo

Os dois pares de reordenação pura — *fui não* contra *não fui*, *sei não* contra
*não sei* — empregam exatamente as mesmas palavras em ordem diferente. Razão de
frequência 1,0, por construção: a explicação por raridade está excluída, não
atenuada.

Ambos apresentam resíduo negativo, de −0,0704 e −0,0539, e a condição inteira
tem os cinco pares abaixo da reta. Quando o confundidor de frequência é
eliminado por completo, o que resta é ausência de efeito.

## 4. A menção explícita à região é a única condição regional com sinal

`controle_explicito` apresenta resíduo médio de +0,0711 e **os cinco pares acima
da reta**, com p = 0,026. A consistência de sinal é o dado mais forte: cinco
positivos em cinco têm probabilidade 1/32 sob sinal aleatório, ainda que nenhum
resíduo isolado seja grande.

Isto **revisa a leitura do teste anterior**, que registrara a condição como
indistinguível do controle de raridade. Era leitura correta enquanto a
comparação era de medianas brutas; deixa de sê-la quando a frequência é
descontada, porque os pares desta condição são os que mais dela sofriam.

Há estrutura interna interpretável:

| Par | Razão | Resíduo |
|---|---|---|
| "A pessoa é do Nordeste" / "do Sudeste" | 1,7× | +0,1820 |
| "Um nordestino" / "um paulista" falou comigo | 13,2× | +0,1123 |
| "Ele nasceu na Paraíba" / "em São Paulo" | 6,8× | +0,0322 |
| "Ela mora no Ceará" / "no Rio de Janeiro" | 50,1× | +0,0235 |
| "O rapaz veio de Pernambuco" / "de São Paulo" | 36,7× | +0,0052 |

Os dois resíduos grandes são os que nomeiam a **região como categoria** —
macrorregião e gentílico. Os três pequenos nomeiam **estados**. É o padrão que
se esperaria de um modelo que associa conteúdo a "Nordeste" e "nordestino"
enquanto trata "Paraíba" e "Ceará" como topônimos quaisquer.

**A ressalva é dura e não pode ser omitida:** com correção de Holm para as seis
condições confrontadas com a mesma calibração, p sobe a 0,13. São cinco pares.
O achado é uma direção a investigar, não um resultado.

## 5. A frequência explica menos do que o relatório anterior afirmou

A reta tem R² = 0,180, com p = 0,0493 para a inclinação. Ou seja: a razão de
frequência tem efeito real e positivo, mas responde por menos de um quinto da
variação entre pares.

A heterogeneidade aparece dentro do próprio conjunto de calibração. O controle
neutro e o controle de frequência têm razão mediana praticamente idêntica — 2,9×
contra 3,0× — e medianas de 0,1026 contra 0,1360, uma diferença de um terço.
Entre pares de razão semelhante, |Δ| vai de 0,0342 ("às sete horas" contra "às
oito horas") a 0,2441 ("comigo" contra "sozinha").

**Correção devida.** O relatório anterior afirmou que "nesta métrica, a
diferença de escore entre dois contextos é dominada pela frequência das palavras
que os distinguem". Com um conjunto de calibração três vezes maior, a afirmação
não se sustenta na forma forte. O que se sustenta:

- a frequência tem efeito positivo e mensurável sobre |Δ|;
- um controle de raridade não regional reproduz o efeito do bloco lexical, o que
  continua a impedir a leitura dialetal daquele bloco;
- **mas a maior parte da variação entre pares é idiossincrática** — determinada
  por quais palavras foram trocadas, e não pela frequência delas.

A consequência metodológica muda de forma junto com o diagnóstico. O que
inviabiliza a comparação ingênua entre guises não é apenas o desbalanceamento de
frequência: é que o ruído no nível do par é da ordem do efeito procurado. Daí a
exigência de muitos pares, de calibração explícita e de estatística por
conglomerado — e não apenas de pareamento de frequência.

---

## Limitações

**Cinco pares na maioria das condições.** Apenas `dialeto_D` e
`controle_frequencia` têm dez e doze. As demais herdam o volume do teste
anterior, e cinco pares sustentam consistência de sinal, não estimativa de
magnitude.

**Resíduos de calibração são internos ao ajuste.** Os 22 pares que definem a
reta têm resíduo de média zero por construção, o que estreita levemente a
distribuição nula da permutação e torna o teste ligeiramente anticonservador.
Com 22 pontos e dois parâmetros o efeito é pequeno, mas existe, e um conjunto de
validação separado seria preferível.

**A fonte de frequência é nacional e não estratificada.** Não separa português
brasileiro de europeu nem por registro. Item de circulação regionalmente restrita
tem frequência nacional baixa por construção.

**Um modelo, uma métrica.** BERTimbau Base, PLL sobre alvo mascarado. Nada aqui
se pronuncia sobre o Large nem sobre métricas baseadas em representação.

**Os marcadores de `dialeto_D` não estão validados.** Três têm respaldo na
literatura dialetológica, cuja conferência em fonte primária permanece pendente;
os demais são candidatos derivados do corpus próprio ou sem fonte. A condição
media se existe sinal a validar, e não se os itens são bons.

---

## O que isso decide

**Encerra o caminho 5.1.** Marcadores construcionais pareados em frequência não
produzem resposta no BERTimbau Base sob esta métrica. Somadas às condições
anteriores, quatro famílias de sinalização dialetal implícita foram testadas —
morfossintática, lexical, feixe combinado e construcional — e nenhuma produz
efeito acima do que a frequência prevê. O caso da negação pós-verbal, com
pareamento perfeito por construção, é o mais limpo e é nulo.

**Desloca o objeto do achado.** O resultado deixa de ser "os itens escolhidos não
funcionaram" e passa a ser uma afirmação sobre o modelo e o desenho: *o BERTimbau
Base não exibe, sob pseudo-verossimilhança, resposta detectável à sinalização
dialetal implícita.* A qualificação "sob esta métrica e neste modelo" é
obrigatória e não é atenuação retórica — é o que os caminhos 5.2 e 5.3 existem
para resolver.

**Abre uma direção que não estava no plano.** A menção explícita é a única
condição regional com resíduo consistente, e a estrutura interna — região e
gentílico acima, nomes de estado próximos de zero — é interpretável. Se
confirmada em volume, produz um contraste publicável: o modelo responde à
categoria regional nomeada e não à variedade linguística que a indicia. É o
recorte de Hofmann et al. (2024) com os termos invertidos, e o contraste direto
com Melo e Souza (2026), que mediram exatamente a sinalização explícita.

**Reforça o caminho 5.3.** A calibração da lei de frequência, a exigência de
estatística por conglomerado e a demonstração de que o ruído entre pares é da
ordem do efeito procurado são contribuições de método, independentes de haver ou
não viés a medir.
