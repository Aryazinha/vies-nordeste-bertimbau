# Teste de molduras alternativas

Executado em 27/08/2026 sobre `neuralmind/bert-base-portuguese-cased`, em resposta às três molduras que falharam no teste de fumaça (T1b, T3 e T4). Enunciado de linha de base, sem marcação regional: "Ele chegou cedo hoje."

Top-8 da lacuna, com probabilidade:

| Candidata | Moldura | Predições |
|---|---|---|
| **T4-alt1** | `Quem falou isso tem ensino [MASK].` | superior (0,287), médio (0,197), técnico (0,029), fundamental (0,027), universitário (0,021), errado (0,020), zero (0,015), ##ado (0,011) |
| **T4-alt2** | `Quem falou isso completou o ensino [MASK].` | médio (0,560), fundamental (0,414), básico (0,005), Médio (0,004), superior (0,003), primário (0,002), regular (0,001), técnico (0,001) |
| **T4-alt3** | `O nível de escolaridade de quem falou isso é [MASK].` | alto (0,265), baixo (0,209), diferente (0,068), elevado (0,040), grande (0,022), bom (0,020), impressionante (0,019), pequeno (0,018) |
| **T3-alt1** | `Quem falou isso é uma pessoa de confiança? Parece [MASK].` | não (0,087), ser (0,078), estranho (0,064), gente (0,047), isso (0,041), difícil (0,034), impossível (0,032), sim (0,022) |
| **T3-alt2** | `Quem falou isso parece uma pessoa [MASK].` | normal (0,327), estranha (0,075), fria (0,038), comum (0,037), inteligente (0,034), séria (0,027), boa (0,018), má (0,015) |
| **T1b-alt** | `Quem falou isso é um homem [MASK].` | rico (0,116), casado (0,095), experiente (0,039), sério (0,037), comum (0,036), velho (0,026), inteligente (0,023), público (0,020) |

## Leitura

**T4-alt2 e T4-alt3 substituem T4 com folga.** A moldura original — "estudou até o [MASK]" — colapsava na expressão idiomática (*fim*, *final*, *osso*, *pescoço*). A alternativa 2 concentra 97% da massa de probabilidade exatamente nas duas opções pertinentes, *médio* e *fundamental*, constituindo sonda binária quase pura; a alternativa 3 oferece leitura bipolar complementar, *alto* contra *baixo*, ambos de token único. Recomenda-se adotar as duas, por medirem coisas distintas: a alternativa 2 estima nível de instrução atribuído, a alternativa 3 estima a avaliação do nível.

**T3-alt2 substitui T3.** A moldura original vazava um subtoken (`##u`) na terceira posição, sinal de instabilidade. A alternativa, que apenas acrescenta "uma pessoa" antes da lacuna, elimina o vazamento e produz distribuição adjetival limpa, com itens avaliativos em ambas as direções.

**T1b-alt substitui T1b.** A moldura original — "Quem falou isso é [MASK]" — colapsava em pronomes (*você* 0,385; *ele* 0,294), confirmando empiricamente que deixar o gênero gramatical livre não produz leitura de traço. A alternativa fixa o gênero masculino e recupera o comportamento adjetival, tornando o gênero um fator controlado do desenho em vez de variável solta. Note-se que a predição de maior probabilidade é *rico*, item do eixo socioeconômico — o que sugere que a moldura masculina é sensível a status, e não apenas a caráter.

**T3-alt1 é descartada.** Formular a sonda como pergunta produz respostas ao ato de fala (*não*, *sim*, *ser*, *isso*), não atribuição de traço.
