"""
pipeline.py
Orquestrador: roda coleta -> transcrição -> diarização -> mescla no schema
final da seção 1.4.1 do documento de referência do projeto.

Uso (Colab ou máquina com GPU, após configurar HF_TOKEN):

    from pipeline import rodar_pipeline_piloto

    video_specs = [
        {"url": "https://youtube.com/watch?v=XXXX", "estado_alvo": "PB",
         "tipo_fonte": "entrevista_vox_pop"},
        ...
    ]
    registros = rodar_pipeline_piloto(video_specs)

Cada registro final é salvo em FINAL_DIR/{id}.json e segue exatamente os
campos definidos na seção 1.4.1: id, canal, data_upload, duracao_s,
transcricao, diarizacao, estado_alvo, tipo_fonte.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path

from config import AUDIO_DIR, FINAL_DIR
from collect import coletar_lote, duracao_coletada_s, VideoMetadata
from transcribe import transcrever_audio
from diarize import diarizar_audio, atribuir_locutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def _montar_registro_final(meta: VideoMetadata, transcricao: dict, turnos: list[dict]) -> dict:
    """
    Monta o registro final no schema da seção 1.4.1, já com o locutor
    atribuído por palavra (integração transcrição + diarização, seção 2.3.5).
    """
    for segmento in transcricao["segmentos"]:
        for word in segmento["words"]:
            word["speaker"] = atribuir_locutor(word["start"], word["end"], turnos)

    registro = asdict(meta)
    registro.pop("title", None)  # campo auxiliar de triagem, não faz parte do schema publicado
    # `duracao_s` é a duração do vídeo de origem; quando há recorte, o áudio
    # analisado é menor. Ver `duracao_coletada_s` em collect.py.
    registro["duracao_coletada_s"] = duracao_coletada_s(meta)
    registro["transcricao"] = transcricao
    registro["diarizacao"] = turnos
    return registro


def rodar_pipeline_piloto(video_specs: list[dict], num_speakers: int | None = None) -> list[dict]:
    """
    Roda o pipeline completo para uma lista de vídeos.

    ATENÇÃO — QA obrigatório antes de qualquer curadoria automática:
    esta função NÃO valida WER/DER. Conforme a Parte 3 do documento
    (ameaças à validade), uma subamostra deve ser checada manualmente
    antes de confiar nos registros para extração de marcadores dialetais.
    """
    metas = coletar_lote(video_specs)
    registros = []

    for meta in metas:
        audio_path = AUDIO_DIR / f"{meta.id}.wav"
        if not audio_path.exists():
            logger.warning("Áudio não encontrado para %s, pulando.", meta.id)
            continue

        transcricao = transcrever_audio(audio_path)
        turnos = diarizar_audio(audio_path, num_speakers=num_speakers)
        registro = _montar_registro_final(meta, transcricao, turnos)

        out_path = FINAL_DIR / f"{meta.id}.json"
        out_path.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Registro final salvo: %s", out_path)
        registros.append(registro)

    return registros


if __name__ == "__main__":
    exemplo = [
        {"url": "URL_DO_VIDEO_1", "estado_alvo": "PB", "tipo_fonte": "entrevista_vox_pop"},
    ]
    resultado = rodar_pipeline_piloto(exemplo)
    print(f"{len(resultado)} registro(s) finalizado(s) em {FINAL_DIR}/")
