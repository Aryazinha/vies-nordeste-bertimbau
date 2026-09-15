# Meta de frases por condição no desenho pareado

Gerado por `experimentos/meta_pareada.py`. Estatística: D = |Δ| teste − |Δ| gêmeo,
pareada por frase. Poder de 80%, teste unilateral. Decisão do efeito-alvo pendente
da equipe (`docs/pendencias.md` 2.11, parte b).

## Dispersão de D nos gêmeos de moldura

| condição | frases | D médio | desvio-padrão |
|---|---|---|---|
| `explicito_regiao` | 20 | -0.0210 | 0.1027 |
| `explicito_gentilico` | 20 | +0.0147 | 0.1612 |
| `explicito_toponimo` | 20 | +0.0108 | 0.0637 |
| `controle_explicito` | 20 | +0.0262 | 0.0465 |
| **combinado** | 80 | — | **0.1034** |

A dispersão é heterogênea: o gentílico tem desvio-padrão várias vezes maior que o
topônimo. Dimensionar pelo combinado subestima o necessário no gentílico; a última
coluna da tabela seguinte dimensiona pelo maior desvio-padrão observado.

## Frases necessárias por condição

| efeito específico a excluir (δ) | α = 0,05, σ combinado | Holm (α/4), σ combinado | Holm, σ máximo (0.161) |
|---|---|---|---|
| 0.03 | 75 | 116 | 277 |
| 0.05 | 28 | 44 | 102 |
| 0.08 | 12 | 19 | 42 |
| 0.10 | 8 | 13 | 28 |

## Menor efeito específico detectável, por número de frases

| frases por condição | Holm, σ combinado | Holm, σ máximo |
|---|---|---|
| 8 (atual) | 0.136 | 0.212 |
| 16 | 0.087 | 0.135 |
| 24 | 0.069 | 0.107 |
| 40 | 0.052 | 0.081 |

## Custo implicado

Cada frase de teste nasce com um gêmeo inter-regional e, se o controle intrarregional
se mostrar informativo, também com um intrarregional: duas ou três medições de par por
frase, a 28 medições cada.
