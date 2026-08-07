"""
collect.py
Coleta de metadados (triagem) e download de áudio via yt-dlp.

Referência: seção 2.1 do documento de referência do projeto.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from typing import Optional

import yt_dlp

from config import YDL_OPTS, ESTADOS_VALIDOS, TIPOS_FONTE_VALIDOS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class VideoMetadata:
    """Espelha exatamente o schema da seção 1.4.1 do documento (campos por vídeo)."""
    id: str
    canal: str
    data_upload: Optional[str]
    duracao_s: Optional[int]
    estado_alvo: str
    tipo_fonte: str
    title: str = ""          # auxiliar de triagem, não faz parte do schema final publicado


def triagem_metadados(url: str, estado_alvo: str, tipo_fonte: str) -> VideoMetadata:
    """
    Extrai apenas metadados (sem baixar mídia) — útil para decidir, em lote,
    quais vídeos entram na coleta antes de gastar banda/tempo com download.

    Levanta ValueError se `estado_alvo` ou `tipo_fonte` não pertencerem ao
    escopo já fechado na seção 1.4.3 do documento — isso é intencional:
    evita que um vídeo fora do escopo entre silenciosamente no dataset.
    """
    if estado_alvo not in ESTADOS_VALIDOS:
        raise ValueError(f"estado_alvo inválido: {estado_alvo}. Use um de {ESTADOS_VALIDOS}")
    if tipo_fonte not in TIPOS_FONTE_VALIDOS:
        raise ValueError(f"tipo_fonte inválido: {tipo_fonte}. Use um de {TIPOS_FONTE_VALIDOS}")

    ydl_opts = {"skip_download": True, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    meta = VideoMetadata(
        id=info.get("id"),
        canal=info.get("uploader"),
        data_upload=info.get("upload_date"),
        duracao_s=info.get("duration"),
        estado_alvo=estado_alvo,
        tipo_fonte=tipo_fonte,
        title=info.get("title", ""),
    )
    logger.info("Triagem OK: %s | canal=%s | %ss | %s/%s",
                meta.id, meta.canal, meta.duracao_s, meta.estado_alvo, meta.tipo_fonte)
    return meta


def baixar_audio(url: str) -> None:
    """
    Baixa e extrai áudio (WAV, 16kHz, mono) usando os parâmetros já validados
    na seção 2.1.4 do documento. Respeita download_archive — não reprocessa
    vídeos já baixados em execuções anteriores.
    """
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([url])


def coletar_lote(video_specs: list[dict]) -> list[VideoMetadata]:
    """
    Roda triagem + download para uma lista de specs no formato:
        {"url": ..., "estado_alvo": "PB", "tipo_fonte": "entrevista_vox_pop"}

    Retorna a lista de metadados triados com sucesso. Vídeos que falharem na
    triagem (URL quebrada, estado/tipo inválido) são pulados e logados —
    não interrompem o lote inteiro (mesma filosofia de `ignoreerrors` do yt-dlp).
    """
    resultados = []
    for spec in video_specs:
        try:
            meta = triagem_metadados(spec["url"], spec["estado_alvo"], spec["tipo_fonte"])
            baixar_audio(spec["url"])
            resultados.append(meta)
        except Exception as exc:  # noqa: BLE001 — lote não pode parar por 1 vídeo
            logger.warning("Falha ao processar %s: %s", spec.get("url"), exc)
    return resultados


if __name__ == "__main__":
    # Exemplo mínimo de uso — substitua pelos vídeos reais do piloto (5-10 vídeos,
    # conforme a fase 4 do roadmap: validar o pipeline antes de escalar).
    exemplo = [
        {"url": "URL_DO_VIDEO_1", "estado_alvo": "PB", "tipo_fonte": "entrevista_vox_pop"},
        {"url": "URL_DO_VIDEO_2", "estado_alvo": "SP", "tipo_fonte": "podcast_radio_tv_regional"},
    ]
    metas = coletar_lote(exemplo)
    print(f"{len(metas)}/{len(exemplo)} vídeos coletados com sucesso.")
