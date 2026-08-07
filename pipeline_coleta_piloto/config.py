"""
config.py
Configuração central do pipeline de coleta piloto (Fase 4 do roadmap do projeto).

Todos os parâmetros aqui refletem exatamente o que já está documentado e decidido
na Parte 2 e seção 1.4 de `contexto_projeto_vies_nordeste_bertimbau.md` (v1.3).
Não redefina parâmetros soltos em outros módulos — centralize aqui.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Diretórios
# --------------------------------------------------------------------------
BASE_DIR = Path("dataset_raw")
AUDIO_DIR = BASE_DIR / "audio"
TRANSCRIPT_DIR = BASE_DIR / "transcricoes"
DIARIZATION_DIR = BASE_DIR / "diarizacao"
FINAL_DIR = BASE_DIR / "registros_finais"      # JSON final, schema seção 1.4.1
ARCHIVE_FILE = BASE_DIR / "archive.txt"          # evita redownload (yt-dlp download_archive)

for d in (AUDIO_DIR, TRANSCRIPT_DIR, DIARIZATION_DIR, FINAL_DIR):
    d.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# Escopo geográfico do projeto (seção 1.4.3)
# --------------------------------------------------------------------------
ESTADOS_NORDESTE = ["PB", "PE", "CE", "BA"]
ESTADOS_CONTROLE = ["SP", "RJ"]
ESTADOS_VALIDOS = ESTADOS_NORDESTE + ESTADOS_CONTROLE

TIPOS_FONTE_VALIDOS = [
    "entrevista_vox_pop",
    "podcast_radio_tv_regional",
    "vlog_amador",
]

# --------------------------------------------------------------------------
# yt-dlp (seção 2.1) — áudio WAV, 16kHz, mono (padrão exigido por
# faster-whisper e pyannote.audio)
# --------------------------------------------------------------------------
YDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": str(AUDIO_DIR / "%(id)s.%(ext)s"),
    "writeinfojson": True,
    "postprocessors": [
        {"key": "FFmpegExtractAudio", "preferredcodec": "wav"},
    ],
    "postprocessor_args": {"ffmpeg": ["-ar", "16000", "-ac", "1"]},
    "ignoreerrors": True,
    "download_archive": str(ARCHIVE_FILE),
    "quiet": False,
}

# --------------------------------------------------------------------------
# faster-whisper (seção 2.2.3) — parâmetros exatos já validados no documento
# --------------------------------------------------------------------------
WHISPER_MODEL_SIZE = "large-v3"
WHISPER_DEVICE = "cuda"              # trocar para "cpu" se não houver GPU
WHISPER_COMPUTE_TYPE = "float16"     # "int8" se rodar em CPU

WHISPER_TRANSCRIBE_KWARGS = {
    "language": "pt",
    "beam_size": 5,
    "word_timestamps": True,
    "vad_filter": True,
    "vad_parameters": {"min_silence_duration_ms": 500},
    "condition_on_previous_text": False,
    "temperature": 0.0,               # decodificação determinística (reprodutibilidade)
}

# --------------------------------------------------------------------------
# pyannote.audio (seção 2.3) — requer token do Hugging Face com termos aceitos
# em https://hf.co/settings/tokens para o modelo:
# https://huggingface.co/pyannote/speaker-diarization-community-1
# --------------------------------------------------------------------------
PYANNOTE_PIPELINE_NAME = "pyannote/speaker-diarization-community-1"
HUGGINGFACE_TOKEN_ENV_VAR = "HF_TOKEN"   # defina como variável de ambiente, nunca hardcoded
