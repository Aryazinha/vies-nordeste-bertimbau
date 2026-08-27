# Pipeline piloto de coleta de áudio

Implementação executável do protocolo definido na seção 1.4 do `CLAUDE.md`. Encadeia `yt-dlp`, `faster-whisper` e `pyannote.audio`; a justificativa de cada parâmetro está em `docs/stack_tecnica.md`.

## Estado de validação

| Etapa | Módulo | Situação |
|---|---|---|
| Configuração e validação de escopo | `config.py`, `collect.py` | **Validada.** A verificação de escopo geográfico e de tipo de fonte rejeita estados fora de PB, PE, CE, BA, SP e RJ |
| Coleta de metadados e áudio | `collect.py` | **Validada em execução real.** Um vídeo coletado, com extração para WAV 16 kHz mono conforme especificado |
| Transcrição | `transcribe.py` | **Não executada.** Sintaticamente correta; requer o modelo `faster-whisper` |
| Diarização | `diarize.py` | **Não executada.** Requer `torch`, `pyannote.audio` e token do Hugging Face |
| Orquestração e registro final | `pipeline.py` | **Não executada** |

## Execução

Requisitos de ambiente: GPU e conexão à internet para a configuração de referência; `faster-whisper` opera também em CPU, com `compute_type="int8"`, ao custo de tempo de processamento.

1. `pip install -r requirements.txt`
2. Instalar o `ffmpeg`, dependência de `yt-dlp` e de `pyannote.audio`.
3. Criar token em https://hf.co/settings/tokens e aceitar os termos do modelo `pyannote/speaker-diarization-community-1`.
4. Definir a variável de ambiente `HF_TOKEN` com esse token. O token nunca deve ser escrito no código.
5. Preencher a lista `video_specs` em `pipeline.py` com as URLs do piloto, combinando os três tipos de fonte conforme as camadas da seção 1.4.3 do `CLAUDE.md`.
6. Executar `python pipeline.py`.

## Saída

Cada vídeo processado gera um arquivo JSON em `dataset_raw/registros_finais/{id}.json`, no esquema da seção 1.4.1 do `CLAUDE.md`: `id`, `canal`, `data_upload`, `duracao_s`, `transcricao` (com timestamps e locutor por palavra), `diarizacao`, `estado_alvo` e `tipo_fonte`.

O diretório `dataset_raw/` não é versionado.

## Verificação obrigatória após o piloto

Antes de qualquer uso dos registros para extração ou confirmação de marcadores dialetais, deve-se realizar verificação manual amostral com cálculo de WER e de DER. A Parte 3 do `CLAUDE.md` registra ambas como ameaças à validade previstas, e o WER estratificado por variedade regional é resultado publicável por si só, além de pré-requisito para o Filtro 2 do protocolo de validação descrito em `docs/pares_minimos_v1.md`.
