# Densidade de contextos de palatalização na fala coletada

Gerado por `experimentos/densidade_palatalizacao.py` sobre os registros
finais do piloto, lidos em memória a partir do arquivo compactado. Apenas
contagens agregadas: nenhum trecho de transcrição é gravado.

## Densidade agregada

| Medida | Valor |
|---|---|
| Palavras transcritas | 45.132 |
| Tempo de fala atribuído | 4.30 h |
| Contextos explícitos (*ti*. *di*) | 1.686 |
| Contextos por redução (*-te*. *-de* final) | 1.817 |
| **Total de contextos** | **3.503** |

**13.6 contextos por minuto de fala**, dos quais 6.5 explícitos e 7.0 por redução.
Equivale a um contexto a cada 4.4 segundos de fala.

## Por camada

| Camada | Falantes | Palavras | Contextos por minuto |
|---|---|---|---|
| `entrevista_vox_pop` | 95 | 15742 | 14.7 |
| `podcast_radio_tv_regional` | 82 | 16072 | 14.6 |
| `vlog_amador` | 34 | 13318 | 10.7 |

## O piso de fala por falante, agora derivável

Estimar a taxa de palatalização de um falante exige ao menos
10 contextos, pelo mesmo critério que
`meta_volume_corpus.py` aplicou à negação pós-verbal: constatar presença
basta com um, comparar grupos exige estimar a taxa.

Com 13.6 contextos por minuto, isso significa **44 segundos, ou 0.7 minutos de fala por falante**.

| Ocorrências desejadas | Fala por falante |
|---|---|
| 10 | 0.7 min |
| 20 | 1.5 min |
| 30 | 2.2 min |
| 50 | 3.7 min |

## Quantos falantes do corpus atual já satisfazem o piso

| Contextos do falante | Falantes |
|---|---|
| 50 ou mais | 18 |
| 30 a 49 | 20 |
| 10 a 29 | 52 |
| menos de 10 | 121 |

**90 de 211 falantes** têm hoje material suficiente para que sua taxa seja estimável com 10 ocorrências.

## Por estado

| UF | Arquivos | Falantes | Falantes com 10+ contextos |
|---|---|---|---|
| BA | 7 | 31 | 14 |
| CE | 10 | 35 | 13 |
| PB | 10 | 40 | 20 |
| PE | 9 | 38 | 17 |
| RJ | 9 | 39 | 13 |
| SP | 7 | 28 | 13 |

## Ressalvas

**A contagem é ortográfica, não fonética.** Mede contextos em que a
palatalização *pode* ocorrer, e não ocorrências dela — a realização exige
análise do áudio. É exatamente o que a meta precisa: quantas oportunidades
de observação o corpus oferece.

**O contexto por redução é aproximado.** A regra adotada — `-te`/`-de`
final em palavra de mais de três letras — inclui casos que não reduzem e
exclui outros que reduzem. O erro é de segunda ordem para dimensionamento.

**Falantes não são pessoas distintas entre arquivos.** A diarização rotula
locutores dentro de cada arquivo; o mesmo indivíduo em dois arquivos conta
duas vezes. Ver `docs/pendencias.md`, seção 6.4.