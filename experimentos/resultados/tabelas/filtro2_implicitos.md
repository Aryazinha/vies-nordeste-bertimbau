# Validação dos pares de sinalização implícita — fonte e corpus

Gerado por `experimentos/validar_implicitos.py`. Substitui o Filtro 1 (juízes),
inviável, conforme `docs/pendencias.md` 2.14. **Contagens de candidatos por busca
automática, antes da conferência humana** — não são ocorrências confirmadas.

Corpus: 83 arquivos; 39.851 palavras do Nordeste e 23.218 do Sudeste. Taxas por 100 mil palavras.

A coluna de arquivos importa tanto quanto a de candidatos: vários candidatos
num único arquivo podem ser um único falante.

| traço | pares | fonte | candidatos NE (arquivos) | por 100 mil | candidatos SE (arquivos) | por 100 mil | situação provisória |
|---|---|---|---|---|---|---|---|
| imperativo com morfologia de subjuntivo (olhe, veja, diga, traga, deixe…) | 7 | verificada — Figuereido (2025): 47% de indicativo em Feira de Santana-BA contra 81% em Campinas-SP | 13 (7) | 32.6 | 1 (1) | 4.3 | a conferir |
| referência: imperativo com morfologia de indicativo (olha, diz, traz, deixa…) | 0 | referência para a proporção do traço anterior | 70 (28) | 175.7 | 37 (14) | 159.4 | referência |
| negação pós-verbal: verbo + não, sem não anterior (fui não, sei não) | 4 | verificada — Santos e Vitório (2025): produtividade máxima de 5,6% | 4 (4) | 10.0 | 1 (1) | 4.3 | a conferir |
| arretado, aperreado, avexado, oxe, oxente | 7 | sem fonte | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |
| marcador discursivo visse? (Recife) | 1 | sem fonte | 1 (1) | 2.5 | 0 (0) | 0.0 | a conferir; um único arquivo no NE |
| menino como vocativo dirigido a adulto | 2 | sem fonte (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B) | 2 (2) | 5.0 | 0 (0) | 0.0 | a conferir |
| rapaz como vocativo ou interjeição | 2 | sem fonte (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B) | 6 (6) | 15.1 | 0 (0) | 0.0 | a conferir |
| lhe com referência à segunda pessoa (eu lhe vi, lhe ligo) | 2 | descrita na literatura; referência não localizada no projeto | 2 (1) | 5.0 | 0 (0) | 0.0 | a conferir; um único arquivo no NE |
| comitativo com mais (foi mais eu = foi comigo) | 1 | descrita na literatura; referência não localizada no projeto | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |
| massa como avaliativo (a festa foi massa) | 1 | sem fonte (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B) | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |
| tu com verbo em terceira pessoa (tu vai, tu foi) | 1 | descrita na literatura; referência não localizada no projeto; registrado também no Rio de Janeiro (docs/pares_minimos_v1.md, M4) | 12 (3) | 30.1 | 4 (1) | 17.2 | a conferir |
| clivagem interrogativa que foi que | 1 | sem fonte | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |
| durativo tá com + tempo (tá com dois dias que) | 1 | sem fonte | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |
| toda vida com valor de sempre | 1 | sem fonte | 0 (0) | 0.0 | 0 (0) | 0.0 | não confirmado no corpus |

**Imperativo, proporção de forma de subjuntivo entre os candidatos:** NE 16% (13 de 83), SE 3% (1 de 38). Pela fonte, espera-se proporção maior no Nordeste. Valor antes da conferência.

## Pares e traços

Um par de feixe (`dialeto_C`) só é confirmado se todos os seus traços o forem.

| par | traços |
|---|---|
| `dialeto_A-00` | imperativo |
| `dialeto_A-01` | imperativo |
| `dialeto_A-02` | imperativo |
| `dialeto_A-03` | negacao_posverbal |
| `dialeto_A-04` | negacao_posverbal |
| `dialeto_B-00` | lexico_regional |
| `dialeto_B-01` | lexico_regional |
| `dialeto_B-02` | lexico_regional |
| `dialeto_B-03` | lexico_regional |
| `dialeto_B-04` | vocativo_menino |
| `dialeto_C-00` | imperativo, lexico_regional |
| `dialeto_C-01` | negacao_posverbal, lexico_regional |
| `dialeto_C-02` | imperativo, lexico_regional |
| `dialeto_C-03` | imperativo, negacao_posverbal, visse |
| `dialeto_C-04` | imperativo, vocativo_rapaz |
| `dialeto_D-00` | lhe_segunda_pessoa |
| `dialeto_D-01` | lhe_segunda_pessoa |
| `dialeto_D-02` | comitativo_mais |
| `dialeto_D-03` | vocativo_menino |
| `dialeto_D-04` | vocativo_rapaz |
| `dialeto_D-05` | massa_avaliativo |
| `dialeto_D-06` | tu_sem_flexao |
| `dialeto_D-07` | que_foi_que |
| `dialeto_D-08` | ta_com_tempo |
| `dialeto_D-09` | toda_vida |
