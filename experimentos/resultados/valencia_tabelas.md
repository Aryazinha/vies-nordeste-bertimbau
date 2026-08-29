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

Grupo de referência: 26 pares não regionais, viés médio +0.0300, desvio-padrão 0.1182. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0325 | -0.0082–+0.1413 | 3/5 | 0.4728 | — |
| controle de frequência | 12 | -0.0151 | -0.0210–+0.0444 | 7/12 | — | — |
| calibração extra | 4 | +0.0873 | -0.0195–+0.1549 | 3/4 | — | — |
| controle de raridade | 5 | +0.0900 | -0.0747–+0.3803 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | +0.0633 | -0.0090–+0.1333 | 4/5 | 0.2579 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.0382 | -0.1310–+0.2923 | 2/5 | 0.4382 | 1.0000 |
| dialetal implícito — feixe | 5 | +0.0720 | +0.0151–+0.1476 | 5/5 | 0.2123 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.0579 | -0.0293–+0.1308 | 6/10 | 0.2630 | 1.0000 |
| menção explícita — topônimo | 8 | +0.0663 | -0.0738–+0.2611 | 5/8 | 0.2587 | 1.0000 |
| menção explícita — conjunto original | 5 | +0.1352 | -0.1754–+0.4000 | 4/5 | 0.0741 | 0.5187 |
| menção explícita — macrorregião | 8 | +0.1952 | +0.0582–+0.3829 | 7/8 | 0.0054 | 0.0486 |
| menção explícita — gentílico de estado | 8 | +0.0337 | -0.4957–+0.2969 | 6/8 | 0.5069 | 1.0000 |
| controle de conteúdo | 5 | +0.2352 | +0.0759–+0.5942 | 5/5 | 0.0069 | 0.0556 |

**Reagrupamento pessoa/lugar, eixo de caráter** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 12 | +0.1390 | 10/12 | 0.0664 |
| rótulo de lugar | 12 | +0.0577 | 8/12 | 0.2775 |

## Eixo de caráter, restrito a token único

Grupo de referência: 26 pares não regionais, viés médio +0.0412, desvio-padrão 0.1676. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0217 | -0.0485–+0.0758 | 4/5 | 0.6165 | — |
| controle de frequência | 12 | -0.0125 | -0.0832–+0.0993 | 8/12 | — | — |
| calibração extra | 4 | +0.1147 | +0.0715–+0.1677 | 4/4 | — | — |
| controle de raridade | 5 | +0.1308 | -0.2254–+0.4401 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | +0.0173 | -0.1106–+0.1127 | 3/5 | 0.6317 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.2045 | -0.1445–+0.5639 | 3/5 | 0.0507 | 0.4060 |
| dialetal implícito — feixe | 5 | +0.1184 | +0.0253–+0.3166 | 5/5 | 0.1715 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.0724 | -0.0328–+0.1807 | 7/10 | 0.3115 | 1.0000 |
| menção explícita — topônimo | 8 | -0.0089 | -0.1338–+0.1658 | 3/8 | 0.7761 | 1.0000 |
| menção explícita — conjunto original | 5 | -0.0318 | -0.4950–+0.2462 | 3/5 | 0.7843 | 1.0000 |
| menção explícita — macrorregião | 8 | +0.0309 | -0.1235–+0.2054 | 3/8 | 0.5576 | 1.0000 |
| menção explícita — gentílico de estado | 8 | +0.0368 | -0.0073–+0.0877 | 6/8 | 0.5390 | 1.0000 |
| controle de conteúdo | 5 | +0.4758 | +0.3174–+0.6326 | 5/5 | 0.0001 | 0.0013 |

**Reagrupamento pessoa/lugar, eixo de caráter, restrito a token único** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 12 | +0.0645 | 8/12 | 0.3490 |
| rótulo de lugar | 12 | -0.0254 | 4/12 | 0.8814 |

## Eixo de ocupação

Grupo de referência: 26 pares não regionais, viés médio +0.0498, desvio-padrão 0.2371. A proximidade da média a zero é o que autoriza usá-lo como nulo.

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0833 | -0.1575–+0.2252 | 4/5 | 0.3999 | — |
| controle de frequência | 12 | +0.0368 | -0.1419–+0.2683 | 7/12 | — | — |
| calibração extra | 4 | -0.0049 | -0.2924–+0.2958 | 2/4 | — | — |
| controle de raridade | 5 | +0.0915 | -0.1775–+0.2637 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | -0.0305 | -0.1213–+0.1810 | 1/5 | 0.7687 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.0967 | -0.2694–+0.4516 | 3/5 | 0.3628 | 1.0000 |
| dialetal implícito — feixe | 5 | +0.0492 | -0.1820–+0.1647 | 4/5 | 0.5200 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.1594 | +0.0827–+0.2894 | 9/10 | 0.0960 | 0.7680 |
| menção explícita — topônimo | 8 | -0.0047 | -0.2404–+0.2031 | 3/8 | 0.7175 | 1.0000 |
| menção explícita — conjunto original | 5 | +0.0326 | -0.3685–+0.6589 | 1/5 | 0.5574 | 1.0000 |
| menção explícita — macrorregião | 8 | +0.0876 | -0.2742–+0.4769 | 4/8 | 0.3655 | 1.0000 |
| menção explícita — gentílico de estado | 8 | -0.2706 | -0.5973–-0.0310 | 1/8 | 0.9897 | 1.0000 |
| controle de conteúdo | 5 | +1.1606 | -0.2811–+2.3287 | 4/5 | 0.0002 | 0.0022 |

**Reagrupamento pessoa/lugar, eixo de ocupação** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 12 | -0.0550 | 5/12 | 0.8063 |
| rótulo de lugar | 12 | -0.0701 | 3/12 | 0.9287 |
