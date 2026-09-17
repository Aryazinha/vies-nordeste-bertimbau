"""
preparar_amostra_wer.py

Gera `amostra_wer.json`, insumo da medição do WER por estado (`medir_wer.py`;
condição C6 de `docs/criterio_conclusao_v1.md`, item 5 do plano de fechamento).

## Duas gerações desta amostra, e por que a segunda existe

A primeira versão, de 15/09/2026, reproduzia a seção 6.4 do notebook: um
trecho por segmento do ASR, com pelo menos 5 s, até 20 minutos por estado. O
teste de transcrição de 17/09/2026, com dez trechos, mostrou um artefato que
inviabilizava a medida: **as marcas de tempo de palavra do `faster-whisper` são
aproximadas, e o recorte entra no meio da palavra das pontas.** Quem transcreve
ouve "crian", "soci", "priva"; a hipótese do ASR traz a palavra inteira, e a
diferença conta como erro que não houve. Em trechos de 17 palavras medianas, os
dois extremos respondem por cerca de 12% de erro espúrio.

Duas saídas foram consideradas e uma foi descartada com dado: restringir a
amostra a segmentos cercados de silêncio deixaria de fora 94% do material, pois
apenas 6% dos segmentos elegíveis têm pausa de 0,4 s dos dois lados.

A saída adotada é **agrupar segmentos consecutivos do mesmo arquivo em blocos
de cerca de 30 segundos**. O artefato de borda continua existindo — duas
palavras por bloco, no máximo —, mas passa a pesar sobre 80 palavras em vez de
17, e incide igualmente em todos os estados. O volume por estado não muda, e o
número de arquivos a abrir cai de 900 para cerca de 240.

## Regras do sorteio

- Blocos de segmentos **consecutivos** do mesmo arquivo, com no máximo 2 s de
  intervalo entre segmentos vizinhos, somando de 20 s a 35 s.
- Blocos que contenham nome mascarado (`[NOME_n]`) ficam fora, por decisão da
  equipe de 15/09/2026: a transcrição manual registraria o nome pronunciado, e
  a máscara contaria como erro do reconhecedor.
- Sorteio por estado com semente fixa, acumulando até 20 minutos.
- `recorte_inicio_s` e `recorte_fim_s` trazem 0,4 s de folga de cada lado, para
  que as palavras das pontas sejam audíveis por inteiro; quem transcreve é
  instruído a ignorar fragmento solto nas bordas.

A saída contém transcrição e fica em `dataset_raw/`, fora do versionamento.

Uso:
    python preparar_amostra_wer.py
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from config import BASE_DIR, ESTADOS_VALIDOS

SEMENTE = 20260917           # sorteio de blocos; a semente 20260827 era a dos trechos avulsos
BLOCO_ALVO_S = 30.0
BLOCO_MIN_S = 20.0
BLOCO_MAX_S = 35.0
INTERVALO_MAX_S = 2.0
MINUTOS_POR_ESTADO = 20
MARGEM_S = 0.4
MASCARA = re.compile(r"\[NOME_\d+\]")


def blocos_do_registro(reg: dict) -> list[dict]:
    """Blocos de segmentos consecutivos, sem máscara, entre BLOCO_MIN_S e BLOCO_MAX_S."""
    segs = sorted(reg["transcricao"]["segmentos"], key=lambda s: s["start"])
    blocos, i = [], 0
    while i < len(segs):
        corrente = [segs[i]]
        j = i + 1
        while j < len(segs):
            if segs[j]["start"] - corrente[-1]["end"] > INTERVALO_MAX_S:
                break
            if segs[j]["end"] - corrente[0]["start"] > BLOCO_MAX_S:
                break
            corrente.append(segs[j])
            if corrente[-1]["end"] - corrente[0]["start"] >= BLOCO_ALVO_S:
                j += 1
                break
            j += 1
        duracao = corrente[-1]["end"] - corrente[0]["start"]
        texto = " ".join(s["text"].strip() for s in corrente)
        if duracao >= BLOCO_MIN_S and not MASCARA.search(texto):
            blocos.append({
                "id": reg["id"], "arquivo": reg["arquivo"], "canal": reg["canal"],
                "estado": reg["estado_alvo"], "camada": reg["tipo_fonte"],
                "inicio_s": round(corrente[0]["start"], 2),
                "fim_s": round(corrente[-1]["end"], 2),
                "recorte_inicio_s": round(max(0.0, corrente[0]["start"] - MARGEM_S), 2),
                "recorte_fim_s": round(corrente[-1]["end"] + MARGEM_S, 2),
                "n_segmentos": len(corrente),
                "hipotese_asr": texto,
                "referencia_manual": "",
            })
        i = max(j, i + 1)
    return blocos


def main() -> None:
    ap = argparse.ArgumentParser(description="Sorteia a amostra do WER em blocos.")
    ap.add_argument("--registros", default=str(BASE_DIR / "registros_anonimizados"))
    ap.add_argument("--saida", default=str(BASE_DIR / "amostra_wer.json"))
    args = ap.parse_args()

    por_estado: dict[str, list[dict]] = defaultdict(list)
    for caminho in sorted(Path(args.registros).glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("transcricao") and reg.get("diarizacao"):
            for bloco in blocos_do_registro(reg):
                por_estado[bloco["estado"]].append(bloco)

    rng = random.Random(SEMENTE)
    selecao = []
    print(f"{'UF':4} {'blocos':>6} {'min':>5} {'arquivos':>8} {'palavras':>8} {'candidatos':>10}")
    for uf in ESTADOS_VALIDOS:
        candidatos = por_estado.get(uf, [])
        rng.shuffle(candidatos)
        acumulado, escolhidos = 0.0, []
        for bloco in candidatos:
            if acumulado >= MINUTOS_POR_ESTADO * 60:
                break
            escolhidos.append(bloco)
            acumulado += bloco["fim_s"] - bloco["inicio_s"]
        for posicao, bloco in enumerate(escolhidos, 1):
            bloco["codigo"] = f"{uf}-B{posicao:02d}"
        selecao.extend(escolhidos)
        palavras = sum(len(b["hipotese_asr"].split()) for b in escolhidos)
        print(f"{uf:4} {len(escolhidos):>6} {acumulado/60:>5.1f} "
              f"{len({b['id'] for b in escolhidos}):>8} {palavras:>8} {len(candidatos):>10}")

    selecao.sort(key=lambda b: (ESTADOS_VALIDOS.index(b["estado"]), b["codigo"]))
    selecao = [{"codigo": b.pop("codigo"), **b} for b in selecao]
    Path(args.saida).write_text(json.dumps(selecao, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(b["fim_s"] - b["inicio_s"] for b in selecao) / 60
    print(f"\n{len(selecao)} blocos, {total:.1f} min, em {args.saida}")


if __name__ == "__main__":
    main()
