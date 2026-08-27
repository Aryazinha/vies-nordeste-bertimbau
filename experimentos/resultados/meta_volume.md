# Meta de volume do corpus de áudio — passo 4.2

Derivada do requisito estatístico do Filtro 2. Gerado por `experimentos/meta_volume_corpus.py`.

## Suposições declaradas

| Parâmetro | Valor | Origem |
|---|---|---|
| Palavras por minuto | 130 | suposição, a recalibrar com o piloto |
| Palavras por oração | 9 | suposição, a recalibrar com o piloto |
| Proporção de orações negadas | 5% | suposição, a recalibrar com o piloto |
| Produtividade da negação pós-verbal | 5.6% | Santos e Vitório (2025), máximo observado |

Disso resulta **43 contextos de negação por hora** de fala do locutor-alvo, e portanto 2.4 ocorrência(s) esperada(s) da variante por hora.

## Volume necessário por estado, segundo o critério adotado

| Critério de decisão do Filtro 2 | Contextos | Horas de fala-alvo |
|---|---|---|
| Detectar ao menos 1 ocorrência com 90% de confiança | 40 | **0.9 h** |
| Detectar ao menos 1 ocorrência com 95% de confiança | 52 | **1.2 h** |
| Detectar ao menos 1 ocorrência com 99% de confiança | 80 | **1.8 h** |
| Esperar 5 ocorrências (estimativa de taxa, não só presença) | 90 | **2.1 h** |
| Esperar 10 ocorrências (comparação entre estados) | 179 | **4.1 h** |

**Critério recomendado:** esperar 10 ocorrências, isto é, **4.1 h de fala do locutor-alvo por estado**. Justificativa: presença ou ausência é suficiente para promover um marcador, mas a comparação entre Nordeste e grupo de controle exige estimar a taxa em cada grupo, não apenas constatar ocorrência. Com esse volume, a probabilidade de zero ocorrências, se a variante de fato tiver a produtividade suposta, é de 0.0033% — a ausência passa a ser evidência, que é a condição para o Filtro 2 significar alguma coisa.

## Conversão para áudio bruto a coletar

Fala do locutor-alvo é menos que áudio gravado: descontam-se vinheta, música, silêncio e turnos de locutores de outra variedade. Os rendimentos abaixo são conservadores e devem ser medidos na verificação manual do piloto.

| Camada | Composição | Rendimento | Fala-alvo por estado | Áudio bruto por estado |
|---|---|---|---|---|
| `entrevista_vox_pop` | 35% | 35% | 1.4 h | 4.1 h |
| `podcast_radio_tv_regional` | 30% | 60% | 1.2 h | 2.1 h |
| `vlog_amador` | 35% | 70% | 1.4 h | 2.1 h |
| **Total** | 100% | — | **4.1 h** | **8.3 h** |

Para os 6 estados (PB, PE, CE, BA, SP, RJ): **50 h de áudio bruto**, 25 h de fala-alvo.

## Consequência para o processamento

Transcrever 50 h com `large-v3` é inviável em CPU. Em GPU, o `faster-whisper` opera bem acima do tempo real, o que põe a transcrição na ordem de poucas horas de máquina. A coleta deve, portanto, ser planejada para ambiente com GPU desde o início, e não migrada para lá depois.

## Amostra de verificação manual

Independente do volume total, o cálculo de WER e DER exige transcrição manual de referência. Recomenda-se 20 minutos por estado, estratificados entre as camadas — 2 h de transcrição manual ao todo. É o suficiente para estimar WER por variedade, que é a ameaça à validade registrada na Parte 3 do `CLAUDE.md` e um resultado publicável por si só.
