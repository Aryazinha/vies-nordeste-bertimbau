"""
collect.py
Coleta de metadados (triagem) e download de áudio via yt-dlp.

Referência: seção 2.1 do documento de referência do projeto.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import yt_dlp

from config import YDL_OPTS, AUDIO_DIR, ESTADOS_VALIDOS, TIPOS_FONTE_VALIDOS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Formas de URL do YouTube que designam coleções, e não um vídeo isolado.
_PADRAO_NAO_VIDEO = re.compile(
    r"/(channel|c|user|playlist|@[^/]+)(/|$)|[?&]list=", re.IGNORECASE)


@dataclass
class VideoMetadata:
    """
    Espelha o schema da seção 1.4.1 do `CLAUDE.md`, com uma extensão.

    `trecho` registra o recorte temporal efetivamente coletado, quando o vídeo
    de origem é longo demais para entrar inteiro (ver `selecionar_videos.py`).
    O campo é parte do schema publicado, e não auxiliar: o compromisso de
    reprodutibilidade da seção 1.4.2 é publicar identificadores em vez de
    áudio, e um identificador de vídeo sem o recorte usado não permite
    reconstruir o material analisado.
    """
    id: str
    canal: str
    data_upload: Optional[str]
    duracao_s: Optional[int]
    estado_alvo: str
    tipo_fonte: str
    trecho: Optional[dict] = None
    # Herdado do canal em fontes.json, como estado_alvo e tipo_fonte. Diz se o
    # canal tem quadro de participação de ouvinte — não se ESTE trecho contém
    # fala de ouvinte, que é o campo seguinte.
    canal_tem_participacao_ouvinte: str = "nao_verificado"
    # Fato do arquivo, e só se estabelece ouvindo. Nasce 'nao_verificado' de
    # propósito: é o volume de fala de ouvinte por estado que precisa ser
    # equilibrado ou descontado, e contagem de canal não mede volume
    # (docs/pendencias.md, seção 1.1).
    participacao_ouvinte: str = "nao_verificado"
    title: str = ""          # auxiliar de triagem, não faz parte do schema final publicado


def duracao_coletada_s(registro) -> Optional[int]:
    """
    Segundos de áudio efetivamente coletados, que **não** são `duracao_s`.

    `duracao_s` guarda a duração do vídeo de origem. Quando o vídeo excede
    `LIMITE_TRECHO_S`, apenas um recorte é baixado, e a duração do material em
    disco é a do recorte. Somar `duracao_s` sobre o conjunto devolve, por isso,
    um valor maior que o corpus real — apurado em 28/08/2026 sobre os 52
    registros então existentes: 11,43 h contra 5,52 h de áudio coletado.

    O defeito é da classe catalogada em `docs/pendencias.md`, seção 5-A: não
    produz erro, produz número plausível. Daí a existência deste campo em vez
    da redefinição de `duracao_s` — os produtos de processamento já gerados
    foram escritos sob a semântica antiga, e alterá-la em silêncio tornaria os
    lotes incoerentes entre si.

    Aceita `VideoMetadata` ou dicionário já serializado.
    """
    obter = (registro.get if isinstance(registro, dict)
             else lambda campo: getattr(registro, campo, None))
    trecho = obter("trecho")
    if trecho:
        return int(trecho["fim_s"]) - int(trecho["inicio_s"])
    return obter("duracao_s")


def triagem_metadados(url: str, estado_alvo: str, tipo_fonte: str,
                      trecho: Optional[dict] = None,
                      canal_participacao: str = "nao_verificado") -> VideoMetadata:
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

    # Verificação de forma da URL, feita ANTES de qualquer chamada de rede.
    # Resolver um endereço de canal é caro: o yt-dlp percorreria o acervo
    # inteiro antes de devolver o controle, de modo que uma checagem posterior
    # ao extract_info não protegeria contra o engano — só o tornaria lento.
    if _PADRAO_NAO_VIDEO.search(url):
        raise ValueError(
            f"URL não corresponde a um vídeo único: {url}. "
            "Para expandir um canal em vídeos, use selecionar_videos.py."
        )

    ydl_opts = {"skip_download": True, "quiet": True, "extract_flat": False,
                "js_runtimes": YDL_OPTS.get("js_runtimes", {})}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Rede de segurança, para formas de URL não previstas pelo padrão acima.
    if info.get("_type") in {"playlist", "multi_video"} or "entries" in info:
        raise ValueError(
            f"URL não corresponde a um vídeo único: {url}. "
            "Para expandir um canal em vídeos, use selecionar_videos.py."
        )
    if not info.get("duration"):
        raise ValueError(f"Vídeo sem duração (transmissão ao vivo?): {url}")

    meta = VideoMetadata(
        id=info.get("id"),
        canal=info.get("uploader"),
        data_upload=info.get("upload_date"),
        duracao_s=info.get("duration"),
        estado_alvo=estado_alvo,
        tipo_fonte=tipo_fonte,
        trecho=trecho,
        canal_tem_participacao_ouvinte=canal_participacao,
        title=info.get("title", ""),
    )
    logger.info("Triagem OK: %s | canal=%s | %ss | %s/%s",
                meta.id, meta.canal, meta.duracao_s, meta.estado_alvo, meta.tipo_fonte)
    return meta


def baixar_audio(url: str, video_id: str, trecho: Optional[dict] = None) -> Path:
    """
    Baixa e extrai áudio (WAV, 16kHz, mono) com os parâmetros de `config.py`.
    Respeita download_archive — não reprocessa vídeos de execuções anteriores.

    Quando `trecho` é informado, baixa apenas o recorte {inicio_s, fim_s}, o
    que permite que um programa longo contribua com poucos minutos em vez de
    consumir a cota inteira de uma camada (ver `selecionar_videos.py`).

    Atenção: o arquivo de saída é nomeado pelo id do vídeo, e o
    download_archive opera por vídeo. Coletar dois recortes distintos de um
    mesmo vídeo exigiria alterar ambos — o planejador seleciona no máximo um
    recorte por vídeo justamente para não esbarrar nisso.
    """
    opts = dict(YDL_OPTS)
    if trecho:
        from yt_dlp.utils import download_range_func
        opts["download_ranges"] = download_range_func(
            None, [(trecho["inicio_s"], trecho["fim_s"])])
        opts["force_keyframes_at_cuts"] = True

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    # Confirmação de que o arquivo existe. `ignoreerrors` faz o yt-dlp registrar
    # a falha e prosseguir sem levantar exceção, de modo que uma falha de rede,
    # de formato ou de autenticação passaria por sucesso e produziria um
    # registro apontando para áudio inexistente. Foi o que ocorreu no teste de
    # 27/08/2026: três vídeos reportados como coletados, nenhum no disco.
    destino = AUDIO_DIR / f"{video_id}.wav"
    if not destino.exists():
        raise RuntimeError(
            f"download não produziu áudio para {video_id}: {destino} não existe. "
            "Causas frequentes: HTTP 403 por ausência de runtime de JavaScript, "
            "versão desatualizada do yt-dlp, ou vídeo com restrição etária."
        )
    if destino.stat().st_size < 32000:          # menos de 1 segundo a 16 kHz mono
        raise RuntimeError(f"áudio truncado para {video_id}: {destino.stat().st_size} bytes")
    return destino


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
            trecho = spec.get("trecho")
            meta = triagem_metadados(
                spec["url"], spec["estado_alvo"], spec["tipo_fonte"], trecho=trecho,
                canal_participacao=spec.get("canal_tem_participacao_ouvinte",
                                            "nao_verificado"))
            baixar_audio(spec["url"], meta.id, trecho=trecho)
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
