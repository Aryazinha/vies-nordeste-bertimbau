"""
selecionar_videos.py

Converte a lista de canais de `fontes.json` em um plano de coleta concreto —
a etapa que faltava entre a lista de fontes (passo 4.1 do roadmap) e o
`collect.py`, que opera sobre vídeos individuais.

Três decisões de desenho estão implementadas aqui, e não são acessórias:

1. **Distribuição em rodízio entre canais.** A cota de cada camada é
   preenchida tomando um vídeo de cada canal por vez, e não esgotando um
   canal antes de passar ao seguinte. Como um canal de vlog corresponde na
   prática a um falante, o rodízio é o que converte volume em diversidade.

2. **Coleta por trecho, não por vídeo inteiro.** Vídeos longos entram como
   recorte de duração fixa, começando depois da abertura. Um programa de
   rádio de quatro horas contribui dez minutos, e a mesma cota de horas
   passa a cobrir muito mais falantes. Sem isso, dois programas longos
   consumiriam a cota inteira de uma camada.

3. **Teto por canal.** Nenhum canal responde por mais que uma fração
   definida da cota de sua camada, o que impede que um único falante
   domine a camada espontânea de um estado.

As metas de volume vêm de `experimentos/meta_volume_corpus.py` (passo 4.2).

Uso:
    python selecionar_videos.py --piloto
    python selecionar_videos.py --estados PB SP --saida plano.json
    python selecionar_videos.py --max-canais 4        # aplica teto de simetria
"""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
from collections import defaultdict
from pathlib import Path

from config import ESTADOS_VALIDOS, TIPOS_FONTE_VALIDOS

RAIZ = Path(__file__).resolve().parent
FONTES = RAIZ / "fontes.json"

# --------------------------------------------------------------------------
# Metas de áudio bruto por estado, em horas (passo 4.2 do roadmap)
# --------------------------------------------------------------------------
META_HORAS = {
    "entrevista_vox_pop": 4.1,
    "podcast_radio_tv_regional": 2.1,
    "vlog_amador": 2.1,
}
META_HORAS_PILOTO = {k: 0.25 for k in META_HORAS}   # 15 min por camada, por estado

# --------------------------------------------------------------------------
# Filtros de duração
# --------------------------------------------------------------------------
DURACAO_MIN_S = 90          # abaixo disso há pouca fala aproveitável
DURACAO_MAX_S = 6 * 3600    # acima disso é quase sempre transmissão contínua
LIMITE_TRECHO_S = 900       # vídeos mais longos que isso entram como recorte
TRECHO_S = 600              # duração do recorte
ABERTURA_S = 120            # descarta o início, onde ficam vinheta e escalada

TETO_POR_CANAL = 0.35       # fração máxima da cota de uma camada por canal

# --------------------------------------------------------------------------
# Alvo em pessoas (etapa 2 de `docs/plano_corpus/`)
# --------------------------------------------------------------------------
# Desde 12/09/2026 o critério de conclusão do corpus não é volume, e sim
# pessoas que conservem 0,7 min de fala depois do recorte pelo teto de 5%
# (`docs/plano_corpus/01-verificar-falantes.md`, seção 7.1). As metas em horas
# acima continuam servindo à coleta por volume; o que segue converte um déficit
# de pessoas em cota de arquivos.
#
# Rendimento medido sobre os 52 arquivos já coletados, em pessoas com pelo
# menos 0,7 min de fala por arquivo — medianas, não suposições:
RENDIMENTO_PESSOAS = {
    "entrevista_vox_pop": 2.0,
    "podcast_radio_tv_regional": 1.5,
    "vlog_amador": 1.0,          # um canal de vlog é, na prática, uma pessoa
}

# Duração mediana efetivamente coletada por arquivo, em segundos, no mesmo
# corpus. Serve só para converter arquivos em cota de horas, que é a unidade
# em que `planejar_camada` opera.
DURACAO_TIPICA_S = 4 * 60

# Repartição do déficit entre as duas camadas que rendem pessoas novas. Vlog
# fica fora: acrescenta uma pessoa por canal, não por arquivo, e a etapa 2
# precisa de pessoas por arquivo coletado.
REPARTICAO = {"entrevista_vox_pop": 2 / 3, "podcast_radio_tv_regional": 1 / 3}

# Margem sobre o déficit. O piso de 20 é mínimo, e não alvo: coletar o exato
# deixa o corpus no limite, sem folga para arquivo perdido no download, para
# falante abaixo do segundo piso ou para exclusão por qualidade.
MARGEM_PADRAO = 1.5
N_VIDEOS_LISTADOS = 40      # profundidade da listagem por canal


def canais_ja_usados(registros_dir: Path) -> set[str]:
    """
    Nomes de canal que já figuram no corpus coletado.

    Existe porque recoletar de um canal já usado acrescenta horas e não
    acrescenta pessoas: o déficit vem justamente da recorrência do apresentador
    entre episódios do mesmo canal (`docs/plano_corpus/02-completar-coleta.md`,
    seção 1). Excluí-los é o que faz a etapa 2 atacar o déficit que tem.
    """
    if not registros_dir.is_dir():
        return set()
    usados = set()
    for caminho in registros_dir.glob("*.json"):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("canal"):
            usados.add(reg["canal"])
    return usados


def metas_por_deficit(deficit: dict[str, int], margem: float = MARGEM_PADRAO) -> dict[str, dict]:
    """
    Converte um déficit de pessoas, por estado, em cota de horas por camada.

    A conversão passa por arquivos, e não direto por horas, porque o que rende
    pessoa é o arquivo novo de canal novo — a hora a mais no mesmo arquivo
    rende fala da mesma pessoa. Estados sem déficit recebem cota zero.
    """
    metas = {}
    for estado, pessoas in deficit.items():
        alvo = pessoas * margem
        metas[estado] = {camada: 0.0 for camada in TIPOS_FONTE_VALIDOS}
        for camada, fracao in REPARTICAO.items():
            arquivos = math.ceil(alvo * fracao / RENDIMENTO_PESSOAS[camada]) if alvo else 0
            metas[estado][camada] = arquivos * DURACAO_TIPICA_S / 3600
    return metas


def listar_videos(channel_id: str, n: int = N_VIDEOS_LISTADOS) -> list[dict]:
    """Lista os vídeos mais recentes de um canal, com id e duração."""
    cmd = [
        "yt-dlp", f"https://www.youtube.com/channel/{channel_id}/videos",
        "--flat-playlist", "-I", f"1:{n}",
        "--extractor-args", "youtube:lang=pt",
        "--print", "%(id)s\t%(duration)s\t%(title)s",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=240,
                           encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return []

    videos = []
    for linha in r.stdout.splitlines():
        partes = linha.split("\t")
        if len(partes) < 3:
            continue
        vid, dur, titulo = partes[0], partes[1], partes[2]
        try:
            dur = float(dur)
        except ValueError:
            continue                      # transmissão ao vivo, sem duração
        if DURACAO_MIN_S <= dur <= DURACAO_MAX_S:
            videos.append({"id": vid, "duracao_s": dur, "titulo": titulo})
    return videos


def montar_spec(video: dict, canal: dict, estado: str) -> dict:
    """
    Monta a especificação de coleta de um vídeo, recortando-o quando longo.

    `estado_alvo` e `tipo_fonte` vêm do canal, jamais digitados à mão — é o
    que faz a regra de atribuição de `docs/fontes_coleta.md` valer também em
    tempo de execução. Desde 01/09/2026 o mesmo vale para
    `canal_tem_participacao_ouvinte`, herdado de `fontes.json`.

    **Dois campos, e a distinção é o ponto.** `canal_tem_participacao_ouvinte`
    é fato do canal e vem de graça; `participacao_ouvinte` é fato do arquivo e
    só se estabelece ouvindo, de modo que nasce `nao_verificado`. Confundi-los
    daria a ilusão de medida: um canal ter quadro de ouvinte não significa que
    este trecho específico contenha fala de ouvinte, e é o volume por estado —
    não a contagem de canais — que precisa ser equilibrado ou descontado
    (`docs/pendencias.md`, seção 1.1).
    """
    spec = {
        "url": f"https://www.youtube.com/watch?v={video['id']}",
        "video_id": video["id"],
        "estado_alvo": estado,
        "tipo_fonte": canal["tipo_fonte"],
        "canal": canal["canal"],
        "channel_id": canal["channel_id"],
        "canal_tem_participacao_ouvinte": canal.get("participacao_ouvinte", "nao_verificado"),
        "participacao_ouvinte": "nao_verificado",
        "titulo": video["titulo"],
        "duracao_total_s": video["duracao_s"],
    }
    if video["duracao_s"] > LIMITE_TRECHO_S:
        inicio = max(ABERTURA_S, video["duracao_s"] * 0.05)
        fim = min(inicio + TRECHO_S, video["duracao_s"])
        spec["trecho"] = {"inicio_s": round(inicio), "fim_s": round(fim)}
        spec["duracao_coletada_s"] = round(fim - inicio)
    else:
        spec["duracao_coletada_s"] = round(video["duracao_s"])
    return spec


def planejar_camada(canais: list[dict], estado: str, camada: str,
                    meta_h: float, semente: int, min_por_canal: int = 1,
                    verbose: bool = True) -> list[dict]:
    """
    Preenche a cota de uma camada distribuindo os vídeos em rodízio entre os
    canais disponíveis. Devolve a lista de especificações selecionadas.
    """
    meta_s = meta_h * 3600
    teto_s = meta_s * TETO_POR_CANAL

    disponiveis = {}
    for canal in canais:
        vids = listar_videos(canal["channel_id"])
        if not vids:
            if verbose:
                print(f"    [aviso] sem vídeos utilizáveis: {canal['canal']}")
            continue
        # Ordem determinística, porém não cronológica: evita coletar apenas a
        # semana mais recente, que tende a ser tematicamente homogênea.
        random.Random(f"{semente}:{canal['channel_id']}").shuffle(vids)
        disponiveis[canal["channel_id"]] = {"canal": canal, "videos": vids, "usado_s": 0.0}
        if verbose:
            print(f"    {canal['canal'][:34]:34s} {len(vids):3d} vídeos utilizáveis")

    selecionados: list[dict] = []
    total_s = 0.0

    def tomar(dados: dict) -> None:
        nonlocal total_s
        spec = montar_spec(dados["videos"].pop(), dados["canal"], estado)
        selecionados.append(spec)
        dados["usado_s"] += spec["duracao_coletada_s"]
        total_s += spec["duracao_coletada_s"]

    # Fase 1 — cobertura mínima. Todo canal contribui, ainda que isso exceda a
    # cota de horas. A cota mede volume; a finalidade da camada é diversidade
    # de falantes, e um canal de vlog corresponde na prática a um falante.
    # Sem esta fase, uma cota pequena é preenchida pelos primeiros canais do
    # rodízio e os demais não entram — o que anula o propósito do rodízio.
    for dados in disponiveis.values():
        for _ in range(min(min_por_canal, len(dados["videos"]))):
            tomar(dados)

    if total_s > meta_s and verbose:
        print(f"    [nota] cobertura mínima excede a cota: {total_s/3600:.2f} h "
              f"contra {meta_h} h. Diversidade preservada; volume acima da meta.")

    # Fase 2 — completar a cota, mantendo o rodízio e o teto por canal.
    esgotados: set[str] = set()
    while total_s < meta_s and len(esgotados) < len(disponiveis):
        for cid, dados in disponiveis.items():
            if cid in esgotados or total_s >= meta_s:
                continue
            if not dados["videos"] or dados["usado_s"] >= teto_s:
                esgotados.add(cid)
                continue
            tomar(dados)

    if verbose:
        n_canais = len({s["channel_id"] for s in selecionados})
        print(f"    -> {len(selecionados)} trechos, {total_s/3600:.2f} h, "
              f"{n_canais} de {len(disponiveis)} canais; meta {meta_h} h")
    return selecionados


def planejar(estados: list[str], metas: dict, max_canais: int | None,
             semente: int, min_por_canal: int = 1, verbose: bool = True,
             metas_por_estado: dict[str, dict] | None = None,
             excluir_canais: set[str] | None = None) -> dict:
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))
    excluir_canais = excluir_canais or set()
    plano: dict = {
        "_meta": {
            "gerado_por": "selecionar_videos.py",
            "semente": semente,
            "metas_horas": metas,
            "max_canais_por_camada": max_canais,
            "min_videos_por_canal": min_por_canal,
            "metas_horas_por_estado": metas_por_estado,
            "canais_excluidos_por_ja_usados": sorted(excluir_canais),
            "regra": "estado_alvo e tipo_fonte derivam do canal em fontes.json, "
                     "nunca de digitação manual",
        },
        "specs": [],
    }

    for estado in estados:
        if verbose:
            print(f"\n=== {estado} ===")
        por_camada = defaultdict(list)
        metas_estado = (metas_por_estado or {}).get(estado, metas)
        for canal in fontes.get(estado, []):
            if canal["situacao"] in ("a_confirmar", "rejeitado"):
                continue                   # não entra em coleta antes de inspeção
            if canal["canal"] in excluir_canais:
                continue                   # já no corpus: renderia horas, não pessoas
            por_camada[canal["tipo_fonte"]].append(canal)

        for camada in TIPOS_FONTE_VALIDOS:
            canais = por_camada.get(camada, [])
            if max_canais:
                canais = canais[:max_canais]
            if not metas_estado.get(camada):
                continue                   # camada sem cota neste estado
            if not canais:
                if verbose:
                    print(f"  {camada}: nenhum canal disponível")
                continue
            if verbose:
                print(f"  {camada} (meta {metas_estado[camada]:.2f} h)")
            plano["specs"].extend(
                planejar_camada(canais, estado, camada, metas_estado[camada], semente,
                                min_por_canal, verbose))

    return plano


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--estados", nargs="+", default=ESTADOS_VALIDOS,
                    help="estados a planejar (padrão: todos do escopo)")
    ap.add_argument("--piloto", action="store_true",
                    help="metas reduzidas, para validar a esteira antes de escalar")
    ap.add_argument("--max-canais", type=int, default=None,
                    help="teto de canais por camada; usar para impor simetria entre grupos")
    ap.add_argument("--min-por-canal", type=int, default=1,
                    help="vídeos garantidos por canal, mesmo que a cota seja excedida")
    ap.add_argument("--semente", type=int, default=20260827,
                    help="semente de sorteio, para tornar a seleção reprodutível")
    ap.add_argument("--deficit", nargs="+", metavar="UF=N", default=None,
                    help="déficit de pessoas por estado, ex.: PE=3 CE=5 BA=5 SP=8 RJ=6. "
                         "Converte-se em cota de arquivos pelo rendimento medido de cada camada.")
    ap.add_argument("--margem", type=float, default=MARGEM_PADRAO,
                    help=f"margem sobre o déficit (padrão: {MARGEM_PADRAO})")
    ap.add_argument("--excluir-usados", action="store_true",
                    help="exclui canais que já estão no corpus; recoletá-los renderia horas, não pessoas")
    ap.add_argument("--registros", default=None,
                    help="pasta dos registros já coletados, para --excluir-usados "
                         "(padrão: dataset_raw/registros_anonimizados)")
    ap.add_argument("--saida", default="plano_coleta.json")
    args = ap.parse_args()

    for e in args.estados:
        if e not in ESTADOS_VALIDOS:
            raise SystemExit(f"estado fora do escopo: {e}")

    metas = META_HORAS_PILOTO if args.piloto else META_HORAS

    metas_por_estado = None
    if args.deficit:
        deficit = {}
        for item in args.deficit:
            uf, _, n = item.partition("=")
            if uf.upper() not in ESTADOS_VALIDOS or not n.isdigit():
                raise SystemExit(f"déficit malformado: {item!r}; use UF=N, ex.: SP=8")
            deficit[uf.upper()] = int(n)
        metas_por_estado = metas_por_deficit(deficit, args.margem)
        estados = [e for e in args.estados if deficit.get(e)]
        if not estados:
            raise SystemExit("nenhum dos estados pedidos tem déficit")
        args.estados = estados
        print(f"Alvo em pessoas, com margem de {args.margem}x: "
              + ", ".join(f"{uf}={n}" for uf, n in sorted(deficit.items())))

    excluir = set()
    if args.excluir_usados:
        registros = Path(args.registros) if args.registros else RAIZ / "dataset_raw" / "registros_anonimizados"
        excluir = canais_ja_usados(registros)
        print(f"{len(excluir)} canal(is) já no corpus serão excluídos do plano.")

    plano = planejar(args.estados, metas, args.max_canais, args.semente,
                     args.min_por_canal, metas_por_estado=metas_por_estado,
                     excluir_canais=excluir)

    Path(args.saida).write_text(json.dumps(plano, ensure_ascii=False, indent=2),
                                encoding="utf-8")

    specs = plano["specs"]
    horas = sum(s["duracao_coletada_s"] for s in specs) / 3600
    recortes = sum(1 for s in specs if "trecho" in s)
    print(f"\n{len(specs)} trechos ({recortes} recortados de vídeos longos), "
          f"{horas:.2f} h, {len({s['channel_id'] for s in specs})} canais distintos")
    print(f"Plano gravado em {args.saida}")
    print("\nPara coletar:")
    print("    from pipeline import rodar_pipeline_piloto")
    print(f"    specs = json.load(open('{args.saida}', encoding='utf-8'))['specs']")
    print("    rodar_pipeline_piloto(specs)")


if __name__ == "__main__":
    main()
