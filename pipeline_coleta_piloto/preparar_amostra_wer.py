"""
preparar_amostra_wer.py

Gera `amostra_wer.json`, insumo da medição do WER por estado
(`medir_wer.py`; condição C6 de `docs/criterio_conclusao_v1.md`, item 5 do
plano de fechamento em `docs/roadmap.md`).

## Por que existe, se o notebook já gerava a amostra

A amostra era produzida pela seção "6.4 Amostra para transcrição manual" de
`notebooks/piloto_colab.ipynb`, e foi sorteada quando o corpus tinha 52
arquivos. Com o corpus final de 83 arquivos na máquina local, e sem exigência
de GPU, a regeração dispensa o Colab. Este script reproduz a lógica daquela
seção — trechos de transcrição de pelo menos 5 s, embaralhados por estado com a
semente 20260827, acumulados até atingir 20 minutos por estado, com
`hipotese_asr` preenchida e `referencia_manual` em branco —, com uma única
diferença deliberada, descrita a seguir.

## A diferença: trechos com nome mascarado ficam fora do sorteio

Os registros disponíveis localmente são os anonimizados, nos quais nomes de
terceiros aparecem como `[NOME_1]`. A transcrição manual registra o nome
efetivamente pronunciado, e o cálculo contaria a máscara como erro de
transcrição que o `faster-whisper` não cometeu. A equipe decidiu, em
15/09/2026, excluir do sorteio os trechos com máscara, em vez de impor ao
transcritor uma convenção adicional. O custo, de 2 a 5 minutos elegíveis por
estado, é declarado como limitação da medida: os trechos com nome próprio,
possivelmente mais difíceis para o reconhecedor, ficam sub-representados, e de
forma aproximadamente igual nos seis estados.

Fora dos trechos mascarados, o texto anonimizado coincide com o original, e os
tempos e a diarização são idênticos — verificado nos 31 registros cujo
original está na máquina local.

## Instantes

`inicio_s` e `fim_s` referem-se ao arquivo de áudio local indicado em
`arquivo`. Nos arquivos coletados como recorte de um vídeo mais longo (campo
`trecho` do registro), o instante no YouTube é o do áudio somado a
`trecho.inicio_s`; a escuta deve ser feita no arquivo local.

A saída contém transcrição e por isso é gravada em `dataset_raw/`, fora do
versionamento.

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

SEMENTE = 20260827          # a mesma da seção 6.4 do notebook
DURACAO_MINIMA_S = 5
MINUTOS_POR_ESTADO = 20
MASCARA = re.compile(r"\[NOME_\d+\]")


def carregar_registros(pasta: Path) -> list[dict]:
    """Registros com transcrição e diarização, na ordem do nome do arquivo, como no notebook."""
    registros = []
    for caminho in sorted(pasta.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("transcricao") and reg.get("diarizacao"):
            registros.append(reg)
    return registros


def main() -> None:
    ap = argparse.ArgumentParser(description="Regera a amostra do WER sobre o corpus local.")
    ap.add_argument("--registros", default=str(BASE_DIR / "registros_anonimizados"))
    ap.add_argument("--saida", default=str(BASE_DIR / "amostra_wer.json"))
    args = ap.parse_args()

    registros = carregar_registros(Path(args.registros))
    if not registros:
        raise SystemExit(f"nenhum registro em {args.registros}")

    random.seed(SEMENTE)
    por_estado: dict[str, list[dict]] = defaultdict(list)
    excluidos: dict[str, list[float]] = defaultdict(list)
    for r in registros:
        for seg in r["transcricao"]["segmentos"]:
            duracao = seg["end"] - seg["start"]
            if duracao < DURACAO_MINIMA_S:
                continue
            if MASCARA.search(seg["text"]):
                excluidos[r["estado_alvo"]].append(duracao)
                continue
            por_estado[r["estado_alvo"]].append({
                "id": r["id"], "arquivo": r["arquivo"], "canal": r["canal"],
                "estado": r["estado_alvo"], "camada": r["tipo_fonte"],
                "inicio_s": round(seg["start"], 2), "fim_s": round(seg["end"], 2),
                "hipotese_asr": seg["text"].strip(), "referencia_manual": "",
            })

    selecao = []
    print(f"{len(registros)} registros lidos de {args.registros}\n")
    print(f"{'UF':4} {'trechos':>7} {'min':>5} {'arquivos':>8} {'excluídos c/ máscara':>21}")
    # Mesma iteração do notebook: estados na ordem em que aparecem no corpus,
    # embaralhados em sequência sobre um único gerador.
    for uf, itens in por_estado.items():
        random.shuffle(itens)
        acumulado, escolhidos = 0.0, []
        for i in itens:
            if acumulado >= MINUTOS_POR_ESTADO * 60:
                break
            escolhidos.append(i)
            acumulado += i["fim_s"] - i["inicio_s"]
        selecao.extend(escolhidos)
        print(f"{uf:4} {len(escolhidos):>7} {acumulado / 60:>5.1f} "
              f"{len({i['id'] for i in escolhidos}):>8} "
              f"{len(excluidos[uf]):>6} ({sum(excluidos[uf]) / 60:.1f} min)")

    # Código estável por trecho, para conduzir a transcrição por referência, e
    # não por posição na lista: PB-001, PB-002...
    ordem = {uf: i for i, uf in enumerate(ESTADOS_VALIDOS)}
    selecao.sort(key=lambda i: (ordem[i["estado"]], i["id"], i["inicio_s"]))
    contagem: dict[str, int] = defaultdict(int)
    for item in selecao:
        contagem[item["estado"]] += 1
        item["codigo"] = f"{item['estado']}-{contagem[item['estado']]:03d}"
    selecao = [{"codigo": i.pop("codigo"), **i} for i in selecao]

    Path(args.saida).write_text(json.dumps(selecao, ensure_ascii=False, indent=2), encoding="utf-8")
    total_min = sum(i["fim_s"] - i["inicio_s"] for i in selecao) / 60
    print(f"\n{len(selecao)} trechos, {total_min:.1f} min, gravados em {args.saida}")


if __name__ == "__main__":
    main()
