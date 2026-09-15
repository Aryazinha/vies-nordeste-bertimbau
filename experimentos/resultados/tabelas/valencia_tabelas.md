# Direção do efeito: o modelo responde com preconceito?

Gerado por `experimentos/analise_valencia.py` sobre as medições já
existentes, sem nova passagem pelo modelo. Escore de viés por par:
média de Δ PLL nos atributos desfavoráveis menos média nos favoráveis.
**Positivo** significa que o guise nordestino torna os atributos
desfavoráveis relativamente mais prováveis.

Valor-p unilateral, por permutação de rótulos de par contra o grupo de
referência de pares não regionais; `p Holm` corrige para a família de
condições testadas em cada eixo. As condições que compõem o próprio grupo
de referência não são testadas, com a exceção deliberada do controle
neutro, que serve de verificação de sanidade e deve resultar não
significativo.

## Eixo de caráter

Grupo de referência: 86 pares não regionais, viés médio +0.0072, desvio-padrão 0.1217. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0325 | -0.0082–+0.1413 | 3/5 | 0.3171 | — |
| controle de frequência | 12 | -0.0151 | -0.0210–+0.0444 | 7/12 | — | — |
| calibração extra | 4 | +0.0873 | -0.0195–+0.1549 | 3/4 | — | — |
| calibração ampliada | 61 | -0.0027 | -0.0391–+0.0343 | 28/61 | — | — |
| controle de raridade | 5 | +0.0900 | -0.0747–+0.3803 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | +0.0633 | -0.0090–+0.1333 | 4/5 | 0.1536 | 0.5292 |
| dialetal implícito — lexical | 5 | +0.0382 | -0.1310–+0.2923 | 2/5 | 0.2928 | 0.5292 |
| dialetal implícito — feixe | 5 | +0.0720 | +0.0151–+0.1476 | 5/5 | 0.1208 | 0.5292 |
| dialetal implícito — construcional | 10 | +0.0579 | -0.0293–+0.1308 | 6/10 | 0.1058 | 0.5292 |
| menção explícita — topônimo | 20 | +0.0591 | +0.0180–+0.1211 | 15/20 | 0.0598 | 0.3591 |
| menção explícita — conjunto original | 20 | +0.1571 | +0.0396–+0.2565 | 16/20 | 0.0002 | 0.0020 |
| menção explícita — macrorregião | 20 | +0.2119 | +0.0374–+0.3799 | 18/20 | 0.0000 | 0.0004 |
| menção explícita — gentílico de estado | 20 | +0.0562 | -0.0542–+0.2562 | 13/20 | 0.1203 | 0.5292 |
| controle de conteúdo | 5 | +0.2352 | +0.0759–+0.5942 | 5/5 | 0.0006 | 0.0045 |

**Reagrupamento pessoa/lugar, eixo de caráter** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 30 | +0.1698 | 23/30 | 0.0000 |
| rótulo de lugar | 30 | +0.0484 | 23/30 | 0.0677 |

## Eixo de caráter, restrito a token único

Grupo de referência: 86 pares não regionais, viés médio +0.0183, desvio-padrão 0.1841. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0217 | -0.0485–+0.0758 | 4/5 | 0.5010 | — |
| controle de frequência | 12 | -0.0125 | -0.0832–+0.0993 | 8/12 | — | — |
| calibração extra | 4 | +0.1147 | +0.0715–+0.1677 | 4/4 | — | — |
| calibração ampliada | 61 | +0.0090 | -0.0274–+0.0561 | 29/61 | — | — |
| controle de raridade | 5 | +0.1308 | -0.2254–+0.4401 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | +0.0173 | -0.1106–+0.1127 | 3/5 | 0.5219 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.2045 | -0.1445–+0.5639 | 3/5 | 0.0171 | 0.1372 |
| dialetal implícito — feixe | 5 | +0.1184 | +0.0253–+0.3166 | 5/5 | 0.1130 | 0.6780 |
| dialetal implícito — construcional | 10 | +0.0724 | -0.0328–+0.1807 | 7/10 | 0.1860 | 0.7977 |
| menção explícita — topônimo | 20 | +0.0187 | -0.0352–+0.1027 | 12/20 | 0.5018 | 1.0000 |
| menção explícita — conjunto original | 20 | +0.0684 | -0.0573–+0.1877 | 12/20 | 0.1595 | 0.7977 |
| menção explícita — macrorregião | 20 | +0.0945 | -0.0700–+0.2113 | 10/20 | 0.0578 | 0.4049 |
| menção explícita — gentílico de estado | 20 | +0.0600 | -0.0383–+0.1342 | 13/20 | 0.1760 | 0.7977 |
| controle de conteúdo | 5 | +0.4758 | +0.3174–+0.6326 | 5/5 | 0.0000 | 0.0004 |

**Reagrupamento pessoa/lugar, eixo de caráter, restrito a token único** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 30 | +0.1226 | 21/30 | 0.0057 |
| rótulo de lugar | 30 | -0.0071 | 14/30 | 0.7589 |

## Eixo de ocupação

Grupo de referência: 86 pares não regionais, viés médio +0.0062, desvio-padrão 0.3933. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0833 | -0.1575–+0.2252 | 4/5 | 0.3169 | — |
| controle de frequência | 12 | +0.0368 | -0.1419–+0.2683 | 7/12 | — | — |
| calibração extra | 4 | -0.0049 | -0.2924–+0.2958 | 2/4 | — | — |
| calibração ampliada | 61 | -0.0099 | -0.1136–+0.0200 | 25/61 | — | — |
| controle de raridade | 5 | +0.0915 | -0.1775–+0.2637 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | -0.0305 | -0.1213–+0.1810 | 1/5 | 0.5744 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.0967 | -0.2694–+0.4516 | 3/5 | 0.2913 | 1.0000 |
| dialetal implícito — feixe | 5 | +0.0492 | -0.1820–+0.1647 | 4/5 | 0.3870 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.1594 | +0.0827–+0.2894 | 9/10 | 0.1139 | 0.9116 |
| menção explícita — topônimo | 20 | -0.0080 | -0.1133–+0.1538 | 8/20 | 0.5589 | 1.0000 |
| menção explícita — conjunto original | 20 | -0.0160 | -0.1823–+0.0125 | 6/20 | 0.5899 | 1.0000 |
| menção explícita — macrorregião | 20 | -0.0452 | -0.2159–+0.1381 | 8/20 | 0.7021 | 1.0000 |
| menção explícita — gentílico de estado | 20 | -0.0194 | -0.3463–+0.1196 | 6/20 | 0.5899 | 1.0000 |
| controle de conteúdo | 5 | +1.1606 | -0.2811–+2.3287 | 4/5 | 0.0000 | 0.0004 |

**Reagrupamento pessoa/lugar, eixo de ocupação** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 30 | +0.0282 | 14/30 | 0.4048 |
| rótulo de lugar | 30 | -0.0766 | 8/30 | 0.8638 |
