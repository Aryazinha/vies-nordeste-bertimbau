# Pipeline piloto de coleta — Fase 4 do roadmap

Implementa `yt-dlp` → `faster-whisper` → `pyannote.audio`, conforme a Parte 2
e seção 1.4 de `contexto_projeto_vies_nordeste_bertimbau.md` (v1.3).

## O que já foi validado (neste ambiente, sem GPU/internet aberta)
- `config.py` e `collect.py` importam e rodam sem erro.
- Validação de escopo geográfico/tipo de fonte funciona (barra estados fora de PB/PE/CE/BA/SP/RJ).
- `transcribe.py`, `diarize.py`, `pipeline.py` são sintaticamente corretos.

## O que só roda no Colab / máquina com GPU + internet
1. `pip install -r requirements.txt`
2. `sudo apt-get install -y ffmpeg` (dependência do yt-dlp e do pyannote)
3. Criar token em https://hf.co/settings/tokens e aceitar os termos do modelo
   `pyannote/speaker-diarization-community-1`
4. Definir a variável de ambiente `HF_TOKEN` com esse token (nunca hardcode)
5. Editar a lista `video_specs` em `pipeline.py` com 5–10 URLs reais para o piloto
   (misturando `entrevista_vox_pop`, `podcast_radio_tv_regional`, `vlog_amador`,
   conforme as camadas da seção 1.4.3)
6. Rodar: `python pipeline.py`

## Saída
Cada vídeo processado gera um JSON em `dataset_raw/registros_finais/{id}.json`
no schema exato da seção 1.4.1: `id`, `canal`, `data_upload`, `duracao_s`,
`transcricao` (com timestamps + locutor por palavra), `diarizacao`,
`estado_alvo`, `tipo_fonte`.

## Próximo passo depois do piloto rodar
QA manual amostral: checar WER e DER numa subamostra antes de confiar nos
registros para extrair/confirmar os marcadores dialetais (Parte 3 do
documento — "Qualidade/ruído da transcrição automática" e "Erros de
diarização" são ameaças à validade já previstas).
