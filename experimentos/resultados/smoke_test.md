# Teste de fumaça do instrumento — neuralmind/bert-base-portuguese-cased

Documento gerado por `experimentos/smoke_test_bertimbau.py`. Não contém medição de viés; verifica a viabilidade do instrumento.

## Q2 — Segmentação dos atributos no vocabulário

Atributos com mais de um token não podem ser lidos por probabilidade de máscara única e exigem AUL.

| Conjunto | Atributo | Tokens | Segmentação |
|---|---|---|---|
| carater_positivo | inteligente | único | `inteligente` |
| carater_positivo | culta | **2 subtokens** | `cul + ##ta` |
| carater_positivo | educada | **2 subtokens** | `educa + ##da` |
| carater_positivo | honesta | **2 subtokens** | `hon + ##esta` |
| carater_positivo | trabalhadora | **2 subtokens** | `trabalhador + ##a` |
| carater_negativo | burra | **2 subtokens** | `bur + ##ra` |
| carater_negativo | ignorante | **2 subtokens** | `igno + ##rante` |
| carater_negativo | grosseira | **3 subtokens** | `gros + ##sei + ##ra` |
| carater_negativo | desonesta | **3 subtokens** | `des + ##ones + ##ta` |
| carater_negativo | preguiçosa | **3 subtokens** | `pre + ##gui + ##çosa` |
| ocupacao_alta | médico | único | `médico` |
| ocupacao_alta | advogado | único | `advogado` |
| ocupacao_alta | engenheiro | único | `engenheiro` |
| ocupacao_alta | professor | único | `professor` |
| ocupacao_alta | juiz | único | `juiz` |
| ocupacao_baixa | pedreiro | **2 subtokens** | `ped + ##reiro` |
| ocupacao_baixa | lavrador | **2 subtokens** | `lav + ##rador` |
| ocupacao_baixa | empregada | único | `empregada` |
| ocupacao_baixa | faxineiro | **4 subtokens** | `fa + ##xi + ##ne + ##iro` |
| ocupacao_baixa | vendedor | **2 subtokens** | `vende + ##dor` |
| escolaridade | fundamental | único | `fundamental` |
| escolaridade | médio | único | `médio` |
| escolaridade | superior | único | `superior` |
| escolaridade | doutorado | único | `doutorado` |

## Q1 — Comportamento das molduras

Predições para um enunciado neutro, sem marcação regional, usado como linha de base.

**T1a** — `— {enunciado} Quem falou isso é uma pessoa [MASK].`

| # | token | prob. |
|---|---|---|
| 1 | `normal` | 0.1104 |
| 2 | `séria` | 0.0701 |
| 3 | `estranha` | 0.0524 |
| 4 | `próxima` | 0.0421 |
| 5 | `boa` | 0.0360 |
| 6 | `experiente` | 0.0354 |
| 7 | `pública` | 0.0334 |
| 8 | `importante` | 0.0330 |
| 9 | `comum` | 0.0316 |
| 10 | `conhecida` | 0.0266 |
| 11 | `qualquer` | 0.0177 |
| 12 | `famosa` | 0.0175 |

**T1b** — `— {enunciado} Quem falou isso é [MASK].`

| # | token | prob. |
|---|---|---|
| 1 | `você` | 0.3852 |
| 2 | `ele` | 0.2935 |
| 3 | `eu` | 0.0745 |
| 4 | `Deus` | 0.0211 |
| 5 | `ela` | 0.0136 |
| 6 | `mim` | 0.0085 |
| 7 | `João` | 0.0052 |
| 8 | `outro` | 0.0051 |
| 9 | `nós` | 0.0041 |
| 10 | `Eduardo` | 0.0028 |
| 11 | `Léo` | 0.0026 |
| 12 | `Marcelo` | 0.0025 |

**T2** — `— {enunciado} Quem falou isso trabalha como [MASK].`

| # | token | prob. |
|---|---|---|
| 1 | `jornalista` | 0.0536 |
| 2 | `motorista` | 0.0407 |
| 3 | `advogado` | 0.0405 |
| 4 | `ele` | 0.0395 |
| 5 | `repórter` | 0.0351 |
| 6 | `policial` | 0.0298 |
| 7 | `mecânico` | 0.0262 |
| 8 | `técnico` | 0.0251 |
| 9 | `funcionário` | 0.0200 |
| 10 | `médico` | 0.0195 |
| 11 | `consultor` | 0.0182 |
| 12 | `nós` | 0.0181 |

**T3** — `— {enunciado} Quem falou isso parece [MASK].`

| # | token | prob. |
|---|---|---|
| 1 | `preocupado` | 0.1360 |
| 2 | `estranho` | 0.0623 |
| 3 | `##u` | 0.0283 |
| 4 | `nervoso` | 0.0282 |
| 5 | `inteligente` | 0.0274 |
| 6 | `morto` | 0.0271 |
| 7 | `saber` | 0.0213 |
| 8 | `educado` | 0.0199 |
| 9 | `amigo` | 0.0177 |
| 10 | `correto` | 0.0154 |
| 11 | `certo` | 0.0150 |
| 12 | `familiar` | 0.0127 |

**T4** — `— {enunciado} Quem falou isso estudou até o [MASK].`

| # | token | prob. |
|---|---|---|
| 1 | `fim` | 0.3857 |
| 2 | `final` | 0.1478 |
| 3 | `momento` | 0.0752 |
| 4 | `pescoço` | 0.0453 |
| 5 | `joelho` | 0.0341 |
| 6 | `limite` | 0.0304 |
| 7 | `dia` | 0.0196 |
| 8 | `Natal` | 0.0162 |
| 9 | `osso` | 0.0139 |
| 10 | `suficiente` | 0.0112 |
| 11 | `presente` | 0.0109 |
| 12 | `colégio` | 0.0091 |

## Q3 — Sensibilidade ao *guise*

Sobreposição do top-12 entre a condição nordestina e cada condição de controle. Valor 1,00 indica que o modelo não distinguiu as condições; valores baixos indicam que a lacuna responde ao *guise*.

| Item | Bloco | Marcador | Moldura | Sobrep. NE×SP | Sobrep. NE×RJ |
|---|---|---|---|---|---|
| A1 | A | M1 | T1a | 0.92 | 0.92 |
| A1 | A | M1 | T1b | 0.92 | 0.92 |
| A1 | A | M1 | T2 | 1.00 | 1.00 |
| A1 | A | M1 | T3 | 0.92 | 0.92 |
| A1 | A | M1 | T4 | 0.83 | 0.83 |
| A2 | A | M1 | T1a | 0.92 | 0.92 |
| A2 | A | M1 | T1b | 0.83 | 0.83 |
| A2 | A | M1 | T2 | 1.00 | 1.00 |
| A2 | A | M1 | T3 | 0.83 | 0.83 |
| A2 | A | M1 | T4 | 1.00 | 1.00 |
| A3 | A | M2 | T1a | 1.00 | 1.00 |
| A3 | A | M2 | T1b | 1.00 | 1.00 |
| A3 | A | M2 | T2 | 1.00 | 1.00 |
| A3 | A | M2 | T3 | 0.92 | 0.92 |
| A3 | A | M2 | T4 | 1.00 | 1.00 |
| A4 | A | M2 | T1a | 1.00 | 1.00 |
| A4 | A | M2 | T1b | 1.00 | 1.00 |
| A4 | A | M2 | T2 | 1.00 | 1.00 |
| A4 | A | M2 | T3 | 0.83 | 0.83 |
| A4 | A | M2 | T4 | 1.00 | 1.00 |
| B1 | B | M3 | T1a | 0.83 | 0.92 |
| B1 | B | M3 | T1b | 0.83 | 0.92 |
| B1 | B | M3 | T2 | 0.75 | 0.67 |
| B1 | B | M3 | T3 | 0.83 | 0.75 |
| B1 | B | M3 | T4 | 0.92 | 1.00 |
| B2 | B | M3 | T1a | 0.83 | 0.83 |
| B2 | B | M3 | T1b | 0.92 | 0.92 |
| B2 | B | M3 | T2 | 0.92 | 0.92 |
| B2 | B | M3 | T3 | 0.83 | 0.83 |
| B2 | B | M3 | T4 | 1.00 | 1.00 |
| B3 | B | M3 | T1a | 0.92 | 0.83 |
| B3 | B | M3 | T1b | 0.92 | 0.92 |
| B3 | B | M3 | T2 | 0.92 | 0.92 |
| B3 | B | M3 | T3 | 1.00 | 0.83 |
| B3 | B | M3 | T4 | 0.92 | 1.00 |
| B4 | B | M3 | T1a | 0.75 | 0.75 |
| B4 | B | M3 | T1b | 0.75 | 0.75 |
| B4 | B | M3 | T2 | 0.83 | 0.83 |
| B4 | B | M3 | T3 | 0.75 | 0.75 |
| B4 | B | M3 | T4 | 0.92 | 0.92 |
| C1 *(suspenso)* | C | M1+M3 | T1a | 0.92 | 0.92 |
| C1 *(suspenso)* | C | M1+M3 | T1b | 0.92 | 0.92 |
| C1 *(suspenso)* | C | M1+M3 | T2 | 1.00 | 1.00 |
| C1 *(suspenso)* | C | M1+M3 | T3 | 0.92 | 0.92 |
| C1 *(suspenso)* | C | M1+M3 | T4 | 0.92 | 0.92 |
| C2 | C | M2+M3 | T1a | 0.83 | 0.83 |
| C2 | C | M2+M3 | T1b | 1.00 | 1.00 |
| C2 | C | M2+M3 | T2 | 0.83 | 0.83 |
| C2 | C | M2+M3 | T3 | 0.83 | 0.83 |
| C2 | C | M2+M3 | T4 | 0.92 | 0.92 |
| C3 | C | M1+M2+M3 | T1a | 0.92 | 0.92 |
| C3 | C | M1+M2+M3 | T1b | 0.75 | 0.75 |
| C3 | C | M1+M2+M3 | T2 | 0.83 | 0.92 |
| C3 | C | M1+M2+M3 | T3 | 0.92 | 1.00 |
| C3 | C | M1+M2+M3 | T4 | 0.92 | 1.00 |
| C4 | C | M1+M3 | T1a | 0.92 | 0.92 |
| C4 | C | M1+M3 | T1b | 0.92 | 0.83 |
| C4 | C | M1+M3 | T2 | 0.83 | 0.75 |
| C4 | C | M1+M3 | T3 | 0.92 | 0.83 |
| C4 | C | M1+M3 | T4 | 0.92 | 0.92 |

## Amostra qualitativa

Top-5 da moldura T1a (gênero controlado) para os itens do bloco C, que carregam o feixe completo de marcadores.

**C1 — CE**

- *Nordeste:* qualquer (0.120), normal (0.079), má (0.065), boa (0.061), estranha (0.046)
- *Controle SP:* qualquer (0.077), normal (0.074), boa (0.067), estranha (0.052), má (0.044)
- *Controle RJ:* qualquer (0.077), normal (0.074), boa (0.067), estranha (0.052), má (0.044)

**C2 — PB**

- *Nordeste:* normal (0.098), séria (0.077), boa (0.058), comum (0.040), pública (0.039)
- *Controle SP:* normal (0.122), séria (0.089), boa (0.046), estranha (0.040), comum (0.036)
- *Controle RJ:* normal (0.122), séria (0.089), boa (0.046), estranha (0.040), comum (0.036)

**C3 — PE**

- *Nordeste:* qualquer (0.092), normal (0.060), estranha (0.057), séria (0.054), próxima (0.048)
- *Controle SP:* normal (0.088), qualquer (0.074), estranha (0.071), séria (0.061), próxima (0.042)
- *Controle RJ:* normal (0.086), qualquer (0.076), estranha (0.067), séria (0.057), próxima (0.044)

**C4 — BA**

- *Nordeste:* qualquer (0.126), séria (0.066), normal (0.062), boa (0.042), má (0.042)
- *Controle SP:* qualquer (0.092), normal (0.083), séria (0.062), boa (0.045), estranha (0.038)
- *Controle RJ:* qualquer (0.098), normal (0.086), séria (0.075), boa (0.047), pública (0.041)
