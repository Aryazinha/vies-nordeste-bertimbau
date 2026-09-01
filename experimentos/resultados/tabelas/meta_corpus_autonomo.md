# Meta do corpus como entregável autônomo

Gerado por `experimentos/meta_corpus_autonomo.py`. Substitui a meta de
`meta_volume.md`, derivada de uma função que o corpus deixou de ter.

## O piso de falantes, derivado do teto já vigente

O teto de 5% por falante, fixado em `docs/fontes_coleta.md`
seção 2.4.5, exige por aritmética **20 falantes distintos por estado**.
Não é escolha: é o que satisfazer o teto significa.

## Plano por estado, priorizando vox-pop e podcast

Vox-pop e podcast entram primeiro, cada canal explorado por vários
arquivos até o teto por canal (7 falantes, 
35% do piso — mesma proporção de `TETO_POR_CANAL` em
`selecionar_videos.py`). Vlog só entra se essas duas camadas, mesmo
exploradas ao máximo, não atingirem o piso.

| UF | Canais vox-pop usados | Arquivos vox-pop | Canais podcast usados | Arquivos podcast | Canais vlog | Falantes cobertos | Falta |
|---|---|---|---|---|---|---|---|
| PB | 3/3 | 3 | 2/4 | 6 | 0/7 | 26.6 | — |
| PE | 4/4 | 4 | 1/5 | 3 | 0/10 | 23.8 | — |
| CE | 4/4 | 4 | 1/4 | 3 | 0/8 | 23.8 | — |
| BA | 3/3 | 3 | 2/4 | 6 | 0/12 | 26.6 | — |
| SP | 2/2 | 2 | 2/4 | 6 | 0/11 | 22.4 | — |
| RJ | 5/5 | 5 | 0/2 | 0 | 0/13 | 21.0 | — |

## O segundo piso: quanta fala por falante

O teto de 5% restringe **quantos** falantes, e nada diz sobre **quanta**
fala cada um precisa produzir. Sem esse segundo piso a conta permitiria um
corpus de vinte pessoas com quatro minutos cada, inútil para o marcador de
áudio do projeto.

A densidade de contextos de palatalização foi medida em **13.6 por minuto** de fala (`densidade_palatalizacao.md`),
de modo que 10 contextos exigem apenas 
**0.7 minuto de fala por falante** — e trinta contextos,
2.2 minutos.

**O piso de fala por falante é, portanto, folgado, e não é o gargalo.**
Dos 211 rótulos de locutor do corpus atual, 90 já superam dez contextos.

## Horas implicadas, que agora são consequência e não meta

Com duração média de 6.4 min por arquivo coletado:

| UF | Arquivos estimados | Horas brutas |
|---|---|---|
| PB | 9 | 1.0 h |
| PE | 7 | 0.7 h |
| CE | 7 | 0.7 h |
| BA | 9 | 1.0 h |
| SP | 8 | 0.8 h |
| RJ | 5 | 0.5 h |
| **Total** | — | **4.8 h** |

Compare-se com as 50 h da meta anterior e com as 38 h de seu recálculo.
A diferença não é de precisão, e sim de critério: aquelas mediam volume de
fala para detectar uma variante; esta mede cobertura de falantes.

## Ressalvas

**Os rendimentos de locutor por arquivo são medianas de 52 arquivos**, e a
variação entre arquivos é grande — um debate rendeu oito locutores.

**A contagem de falantes distintos não está implementada.** Nada garante,
hoje, que dois arquivos não contenham a mesma pessoa; a verificação exigiria
comparação de vozes na diarização (`docs/pendencias.md`, seção 6.4). Até que
exista, os números abaixo são estimativa e não medição.

**O piso de 20 é mínimo, não alvo.** Satisfazê-lo por pouco deixa o corpus
no limite exato do teto, sem margem para exclusão de trecho por qualidade.

## O gargalo mudou de lugar, e é este o achado do recálculo

Sob o critério antigo, o que faltava eram **horas**: 5,52 h de 50 h, 11%.
Sob o critério de entregável autônomo, as horas deixam de ser escassas — a
densidade medida mostra que um minuto de fala por pessoa basta para o
marcador, e o corpus atual já tem 90 locutores acima do piso.

**O que falta passa a ser a verificação de que os falantes são pessoas
distintas.** A diarização rotula locutores dentro de cada arquivo; nada
garante que o rótulo `SPEAKER_00` de dois arquivos do mesmo canal não seja
a mesma pessoa — e no caso do repórter ou do apresentador, quase certamente
é. Os 211 rótulos são, portanto, **limite superior** do número de pessoas,
e possivelmente muito acima dele.

Segue-se que a pendência 6.4 de `docs/pendencias.md` — comparação de vozes
entre arquivos, hoje não implementada — deixa de ser melhoria desejável e
passa a ser **condição para declarar o corpus completo**. Sem ela não é
possível afirmar que o teto de 5% é respeitado, e o teto é a única regra
de que a meta inteira deriva.
