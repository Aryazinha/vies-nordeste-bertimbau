# Análise de sensibilidade do instrumento

Complemento ao teste de fumaça. Mede a diferença entre condições sobre a distribuição completa da lacuna, e não apenas sobre o top-k.

## Divergência de Jensen-Shannon entre condições

Valores em bits. Zero indica distribuições idênticas — o modelo não distinguiu as condições. Para referência de escala, a última linha traz a divergência entre dois enunciados de conteúdo proposicional distinto, que é o teto esperado para uma diferença que o modelo efetivamente percebe.

| Item | Bloco | Marcador | Moldura | JS(NE‖SP) | JS(NE‖RJ) |
|---|---|---|---|---|---|
| A1 | A | M1 | T1a | 0.0023 | 0.0023 |
| A1 | A | M1 | T1b | 0.0041 | 0.0041 |
| A1 | A | M1 | T2 | 0.0048 | 0.0048 |
| A1 | A | M1 | T3 | 0.0087 | 0.0087 |
| A1 | A | M1 | T4 | 0.0023 | 0.0023 |
| A2 | A | M1 | T1a | 0.0060 | 0.0060 |
| A2 | A | M1 | T1b | 0.0603 | 0.0603 |
| A2 | A | M1 | T2 | 0.0089 | 0.0089 |
| A2 | A | M1 | T3 | 0.0087 | 0.0087 |
| A2 | A | M1 | T4 | 0.0022 | 0.0022 |
| A3 | A | M2 | T1a | 0.0015 | 0.0015 |
| A3 | A | M2 | T1b | 0.0006 | 0.0006 |
| A3 | A | M2 | T2 | 0.0009 | 0.0009 |
| A3 | A | M2 | T3 | 0.0045 | 0.0045 |
| A3 | A | M2 | T4 | 0.0007 | 0.0007 |
| A4 | A | M2 | T1a | 0.0023 | 0.0023 |
| A4 | A | M2 | T1b | 0.0018 | 0.0018 |
| A4 | A | M2 | T2 | 0.0019 | 0.0019 |
| A4 | A | M2 | T3 | 0.0036 | 0.0036 |
| A4 | A | M2 | T4 | 0.0010 | 0.0010 |
| B1 | B | M3 | T1a | 0.0146 | 0.0178 |
| B1 | B | M3 | T1b | 0.0141 | 0.0134 |
| B1 | B | M3 | T2 | 0.0182 | 0.0320 |
| B1 | B | M3 | T3 | 0.0160 | 0.0152 |
| B1 | B | M3 | T4 | 0.0246 | 0.0130 |
| B2 | B | M3 | T1a | 0.0205 | 0.0205 |
| B2 | B | M3 | T1b | 0.0063 | 0.0063 |
| B2 | B | M3 | T2 | 0.0085 | 0.0085 |
| B2 | B | M3 | T3 | 0.0232 | 0.0232 |
| B2 | B | M3 | T4 | 0.0067 | 0.0067 |
| B3 | B | M3 | T1a | 0.0093 | 0.0086 |
| B3 | B | M3 | T1b | 0.0148 | 0.0139 |
| B3 | B | M3 | T2 | 0.0035 | 0.0221 |
| B3 | B | M3 | T3 | 0.0104 | 0.0112 |
| B3 | B | M3 | T4 | 0.0056 | 0.0042 |
| B4 | B | M3 | T1a | 0.0366 | 0.0366 |
| B4 | B | M3 | T1b | 0.0116 | 0.0116 |
| B4 | B | M3 | T2 | 0.0395 | 0.0395 |
| B4 | B | M3 | T3 | 0.0263 | 0.0263 |
| B4 | B | M3 | T4 | 0.0059 | 0.0059 |
| C1 | C | M1+M3 | T1a | 0.0170 | 0.0170 |
| C1 | C | M1+M3 | T1b | 0.0069 | 0.0069 |
| C1 | C | M1+M3 | T2 | 0.0071 | 0.0071 |
| C1 | C | M1+M3 | T3 | 0.0130 | 0.0130 |
| C1 | C | M1+M3 | T4 | 0.0081 | 0.0081 |
| C2 | C | M2+M3 | T1a | 0.0103 | 0.0103 |
| C2 | C | M2+M3 | T1b | 0.0037 | 0.0037 |
| C2 | C | M2+M3 | T2 | 0.0091 | 0.0091 |
| C2 | C | M2+M3 | T3 | 0.0280 | 0.0280 |
| C2 | C | M2+M3 | T4 | 0.0051 | 0.0051 |
| C3 | C | M1+M2+M3 | T1a | 0.0121 | 0.0069 |
| C3 | C | M1+M2+M3 | T1b | 0.0350 | 0.0253 |
| C3 | C | M1+M2+M3 | T2 | 0.0192 | 0.0079 |
| C3 | C | M1+M2+M3 | T3 | 0.0286 | 0.0125 |
| C3 | C | M1+M2+M3 | T4 | 0.0168 | 0.0022 |
| C4 | C | M1+M3 | T1a | 0.0058 | 0.0090 |
| C4 | C | M1+M3 | T1b | 0.0027 | 0.0022 |
| C4 | C | M1+M3 | T2 | 0.0050 | 0.0213 |
| C4 | C | M1+M3 | T3 | 0.0084 | 0.0141 |
| C4 | C | M1+M3 | T4 | 0.0041 | 0.0058 |
| *referência de escala* | — | conteúdo distinto | T1a | 0.0963 | — |

## Razão de probabilidade por atributo, na moldura T1a

Razão entre a probabilidade sob a condição nordestina e sob a condição de controle de São Paulo. Valores acima de 1 indicam atributo mais provável no *guise* nordestino. Apenas atributos de token único.

| Item | inteligente | normal | estranha | boa | má | séria | comum | médico | advogado | engenheiro | professor | juiz | empregada |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 1.07 | 1.03 | 1.02 | 0.90 | 1.24 | 0.89 | 1.06 | 0.82 | 0.73 | 0.86 | 1.02 | 0.88 | 1.07 |
| A2 | 1.13 | 0.81 | 0.93 | 0.90 | 1.34 | 1.07 | 0.87 | 0.80 | 0.74 | 0.81 | 0.74 | 0.85 | 0.90 |
| A3 | 1.06 | 0.97 | 0.93 | 1.01 | 1.14 | 0.92 | 0.98 | 1.08 | 0.96 | 1.05 | 1.14 | 0.95 | 1.11 |
| A4 | 1.19 | 1.00 | 0.93 | 1.14 | 1.22 | 1.04 | 0.93 | 1.01 | 0.99 | 1.10 | 1.18 | 1.08 | 1.11 |
| B1 | 0.94 | 1.06 | 1.61 | 1.18 | 1.88 | 0.96 | 1.07 | 1.43 | 1.07 | 0.96 | 1.25 | 0.91 | 1.36 |
| B2 | 0.87 | 0.84 | 0.72 | 1.18 | 1.32 | 0.74 | 1.22 | 0.66 | 1.56 | 0.81 | 0.78 | 1.95 | 1.06 |
| B3 | 0.71 | 0.66 | 0.87 | 0.84 | 0.93 | 1.03 | 0.95 | 1.58 | 1.76 | 1.41 | 1.27 | 1.71 | 1.42 |
| B4 | 0.83 | 1.43 | 0.91 | 1.46 | 2.22 | 0.83 | 1.76 | 0.74 | 1.37 | 0.49 | 1.23 | 1.02 | 1.17 |
| C1 | 1.15 | 1.06 | 0.87 | 0.91 | 1.48 | 1.14 | 1.27 | 0.74 | 0.89 | 0.81 | 1.10 | 0.92 | 1.18 |
| C2 | 0.97 | 0.80 | 0.91 | 1.25 | 1.51 | 0.87 | 1.13 | 0.89 | 1.60 | 1.04 | 1.07 | 1.73 | 1.13 |
| C3 | 0.99 | 0.68 | 0.80 | 0.95 | 1.70 | 0.88 | 0.76 | 1.09 | 0.99 | 0.87 | 0.86 | 1.14 | 1.16 |
| C4 | 0.78 | 0.75 | 0.87 | 0.93 | 1.12 | 1.07 | 0.85 | 1.12 | 1.09 | 1.08 | 1.00 | 1.16 | 1.12 |
