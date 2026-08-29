# Direção do efeito: o modelo responde com preconceito?

Gerado por `experimentos/analise_valencia.py` sobre as medições já
existentes, sem nova passagem pelo modelo. Escore de viés por par:
média de Δ PLL nos atributos desfavoráveis menos média nos favoráveis.
**Positivo** significa que o guise nordestino torna os atributos
desfavoráveis relativamente mais prováveis.

Valor-p unilateral, por permutação de rótulos de par contra o controle
neutro; `p Holm` corrige para a família de condições testadas em cada eixo.

## Eixo de caráter

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0325 | -0.0082–+0.1413 | 3/5 | — | — |
| dialetal implícito — morfossintático | 5 | +0.0633 | -0.0090–+0.1333 | 4/5 | 0.2269 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.0382 | -0.1310–+0.2923 | 2/5 | 0.4833 | 1.0000 |
| dialetal implícito — feixe | 5 | +0.0720 | +0.0151–+0.1476 | 5/5 | 0.1477 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.0579 | -0.0293–+0.1308 | 6/10 | 0.3295 | 1.0000 |
| menção explícita — topônimo | 8 | +0.0663 | -0.0738–+0.2611 | 5/8 | 0.3768 | 1.0000 |
| menção explícita — conjunto original | 5 | +0.1352 | -0.1754–+0.4000 | 4/5 | 0.1845 | 1.0000 |
| menção explícita — macrorregião | 8 | +0.1952 | +0.0582–+0.3829 | 7/8 | 0.0472 | 0.3776 |
| menção explícita — gentílico de estado | 8 | +0.0337 | -0.4957–+0.2969 | 6/8 | 0.5113 | 1.0000 |
| controle de conteúdo | 5 | +0.2352 | +0.0759–+0.5942 | 5/5 | 0.0104 | 0.0936 |

**Reagrupamento pessoa/lugar, eixo de caráter** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 12 | +0.1390 | 10/12 | 0.2453 |
| rótulo de lugar | 12 | +0.0577 | 8/12 | 0.4055 |

## Eixo de ocupação

| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |
|---|---|---|---|---|---|---|
| controle neutro | 5 | +0.0833 | -0.1575–+0.2252 | 4/5 | — | — |
| dialetal implícito — morfossintático | 5 | -0.0305 | -0.1213–+0.1810 | 1/5 | 0.8909 | 1.0000 |
| dialetal implícito — lexical | 5 | +0.0967 | -0.2694–+0.4516 | 3/5 | 0.4721 | 1.0000 |
| dialetal implícito — feixe | 5 | +0.0492 | -0.1820–+0.1647 | 4/5 | 0.6860 | 1.0000 |
| dialetal implícito — construcional | 10 | +0.1594 | +0.0827–+0.2894 | 9/10 | 0.1837 | 1.0000 |
| menção explícita — topônimo | 8 | -0.0047 | -0.2404–+0.2031 | 3/8 | 0.7780 | 1.0000 |
| menção explícita — conjunto original | 5 | +0.0326 | -0.3685–+0.6589 | 1/5 | 0.6084 | 1.0000 |
| menção explícita — macrorregião | 8 | +0.0876 | -0.2742–+0.4769 | 4/8 | 0.4931 | 1.0000 |
| menção explícita — gentílico de estado | 8 | -0.2706 | -0.5973–-0.0310 | 1/8 | 0.9253 | 1.0000 |
| controle de conteúdo | 5 | +1.1606 | -0.2811–+2.3287 | 4/5 | 0.0262 | 0.2362 |

**Reagrupamento pessoa/lugar, eixo de ocupação** (exploratório, pelas razões declaradas em `teste_explicito.py`):

| agrupamento | pares | viés médio | positivos | p |
|---|---|---|---|---|
| rótulo de pessoa | 12 | -0.0550 | 5/12 | 0.7119 |
| rótulo de lugar | 12 | -0.0701 | 3/12 | 0.9247 |
