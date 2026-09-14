# Meta de frases por condição no desenho pareado

Gerado por `experimentos/meta_pareada.py`. Estatística: D = |Δ| teste − |Δ| gêmeo,
pareada por frase. Poder de 80%, teste unilateral. Decisão do efeito-alvo pendente
da equipe (`docs/pendencias.md` 2.11, parte b).

## Dispersão de D nos gêmeos de moldura

| condição | frases | D médio | desvio-padrão |
|---|---|---|---|
| `explicito_regiao` | 8 | +0.0279 | 0.0641 |
| `explicito_gentilico` | 8 | +0.0158 | 0.1705 |
| `explicito_toponimo` | 8 | -0.0010 | 0.0772 |
| `controle_explicito` | 5 | +0.0398 | 0.0436 |
| **combinado** | 29 | — | **0.1061** |

A dispersão é heterogênea: o gentílico tem desvio-padrão várias vezes maior que o
topônimo. Dimensionar pelo combinado subestima o necessário no gentílico; a última
coluna da tabela seguinte dimensiona pelo maior desvio-padrão observado.

## Frases necessárias por condição

| efeito específico a excluir (δ) | α = 0,05, σ combinado | Holm (α/4), σ combinado | Holm, σ máximo (0.170) |
|---|---|---|---|
| 0.03 | 79 | 122 | 310 |
| 0.05 | 30 | 46 | 113 |
| 0.08 | 13 | 20 | 46 |
| 0.10 | 9 | 14 | 31 |

## Menor efeito específico detectável, por número de frases

| frases por condição | Holm, σ combinado | Holm, σ máximo |
|---|---|---|
| 8 (atual) | 0.140 | 0.224 |
| 16 | 0.089 | 0.143 |
| 24 | 0.071 | 0.113 |
| 40 | 0.053 | 0.086 |

## Custo implicado

Cada frase de teste nasce com um gêmeo inter-regional e, se o controle intrarregional
se mostrar informativo, também com um intrarregional: duas ou três medições de par por
frase, a 28 medições cada.
