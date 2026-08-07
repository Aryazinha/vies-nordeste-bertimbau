"""
transcribe.py
Transcrição com timestamps a nível de palavra via faster-whisper.

Referência: seção 2.2 do documento de referência do projeto.
Os parâmetros de `WHISPER_TRANSCRIBE_KWARGS` (config.py) já refletem as
recomendações críticas para reprodutibilidade científica (temperature=0.0)
e mitigação de alucinação (condition_on_previous_text=False, vad_filter=True).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from faster_whisper import WhisperModel

from config import (
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_TRANSCRIBE_KWARGS,
    TRANSCRIPT_DIR,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

_model: WhisperModel | None = None


def get_model() -> WhisperModel:
    """Carrega o modelo uma única vez (lazy singleton) — evitar recarregar por vídeo."""
    global _model
    if _model is None:
        logger.info("Carregando faster-whisper (%s, %s, %s)...",
                     WHISPER_MODEL_SIZE, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE)
        _model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE)
    return _model


def transcrever_audio(audio_path: Path) -> dict:
    """
    Transcreve um arquivo .wav e retorna um dicionário estruturado:
        {"idioma": str, "confianca_idioma": float, "segmentos": [...]}

    Cada segmento contém start/end/text e a lista de palavras com
    start/end/probability — a granularidade exigida pelo schema da seção 1.4.1
    (campo `transcricao`, com timestamps a nível de palavra).
    """
    model = get_model()
    segments, info = model.transcribe(str(audio_path), **WHISPER_TRANSCRIBE_KWARGS)

    resultado = {
        "idioma": info.language,
        "confianca_idioma": info.language_probability,
        "segmentos": [],
    }

    for segment in segments:
        seg_dict = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "words": [],
        }
        if segment.words:
            for word in segment.words:
                seg_dict["words"].append({
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                    "probability": word.probability,  # útil para QA/filtragem de baixa confiança
                })
        resultado["segmentos"].append(seg_dict)

    logger.info("Transcrito %s: idioma=%s (conf=%.2f), %d segmentos",
                audio_path.name, resultado["idioma"], resultado["confianca_idioma"],
                len(resultado["segmentos"]))
    return resultado


def transcrever_e_salvar(audio_path: Path) -> Path:
    """Transcreve e persiste o resultado como JSON em TRANSCRIPT_DIR. Retorna o path salvo."""
    resultado = transcrever_audio(audio_path)
    out_path = TRANSCRIPT_DIR / f"{audio_path.stem}.json"
    out_path.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import sys
    from config import AUDIO_DIR

    audios = list(AUDIO_DIR.glob("*.wav"))
    if not audios:
        print(f"Nenhum .wav encontrado em {AUDIO_DIR}. Rode collect.py primeiro.")
        sys.exit(1)

    for audio_path in audios:
        out = transcrever_e_salvar(audio_path)
        print(f"OK: {audio_path.name} -> {out}")
