"""
diarize.py
Diarização de locutores via pyannote.audio + atribuição de locutor por palavra.

Referência: seção 2.3 do documento de referência do projeto.
Requer variável de ambiente HF_TOKEN com um token do Hugging Face que já
tenha aceitado os termos de uso do modelo em:
https://huggingface.co/pyannote/speaker-diarization-community-1
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import torch
from pyannote.audio import Pipeline

from config import PYANNOTE_PIPELINE_NAME, HUGGINGFACE_TOKEN_ENV_VAR, DIARIZATION_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

_pipeline: Pipeline | None = None


def get_pipeline() -> Pipeline:
    """Carrega o pipeline de diarização uma única vez (lazy singleton)."""
    global _pipeline
    if _pipeline is None:
        token = os.environ.get(HUGGINGFACE_TOKEN_ENV_VAR)
        if not token:
            raise EnvironmentError(
                f"Defina a variável de ambiente {HUGGINGFACE_TOKEN_ENV_VAR} com um token do "
                "Hugging Face válido (com os termos do modelo já aceitos)."
            )
        logger.info("Carregando pipeline de diarização (%s)...", PYANNOTE_PIPELINE_NAME)
        _pipeline = Pipeline.from_pretrained(PYANNOTE_PIPELINE_NAME, token=token)
        _pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    return _pipeline


def diarizar_audio(audio_path: Path, num_speakers: int | None = None) -> list[dict]:
    """
    Roda a diarização e retorna uma lista de turnos:
        [{"start": float, "end": float, "speaker": str}, ...]

    Se `num_speakers` for conhecido (ex. entrevista 1-para-1), passe explicitamente
    para melhorar a precisão — conforme seção 2.3.3 do documento.
    """
    pipeline = get_pipeline()
    kwargs = {"num_speakers": num_speakers} if num_speakers else {}
    output = pipeline(str(audio_path), **kwargs)

    turnos = [
        {"start": turn.start, "end": turn.end, "speaker": speaker}
        for turn, _, speaker in output.itertracks(yield_label=True)
    ]
    logger.info("Diarizado %s: %d turnos, %d locutores distintos",
                audio_path.name, len(turnos), len({t["speaker"] for t in turnos}))
    return turnos


def atribuir_locutor(word_start: float, word_end: float, turnos: list[dict]) -> str | None:
    """
    Atribui o locutor dominante a uma palavra transcrita, por sobreposição temporal.
    Mesma lógica descrita na seção 2.3.5 do documento.
    """
    melhor_speaker, melhor_overlap = None, 0.0
    for turno in turnos:
        overlap = max(0.0, min(word_end, turno["end"]) - max(word_start, turno["start"]))
        if overlap > melhor_overlap:
            melhor_overlap, melhor_speaker = overlap, turno["speaker"]
    return melhor_speaker


def diarizar_e_salvar(audio_path: Path, num_speakers: int | None = None) -> Path:
    """Diariza e persiste o resultado como JSON em DIARIZATION_DIR. Retorna o path salvo."""
    turnos = diarizar_audio(audio_path, num_speakers=num_speakers)
    out_path = DIARIZATION_DIR / f"{audio_path.stem}.json"
    out_path.write_text(json.dumps(turnos, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import sys
    from config import AUDIO_DIR

    audios = list(AUDIO_DIR.glob("*.wav"))
    if not audios:
        print(f"Nenhum .wav encontrado em {AUDIO_DIR}. Rode collect.py primeiro.")
        sys.exit(1)

    for audio_path in audios:
        out = diarizar_e_salvar(audio_path)
        print(f"OK: {audio_path.name} -> {out}")
