"""
registrar_referencia_wer.py

Grava em `amostra_wer.json` as transcrições manuais de referência produzidas
pela equipe (item 11 do plano de fechamento), a partir de um arquivo JSON com
um código de bloco por chave.

## Por que passar por script

A transcrição chega em lotes, ao longo de dias, e editar `amostra_wer.json` à
mão a cada lote arriscaria corromper o arquivo que sustenta a medição inteira.
O script recusa código inexistente, preserva o que já estava gravado, registra
a data de cada lote e avisa quando um bloco é sobrescrito.

Formato do arquivo de entrada:

    {"PB-B01": "texto transcrito",
     "PB-B03": {"texto": "...", "nota": "duas vozes no bloco"}}

Uso:
    python registrar_referencia_wer.py --arquivo lote_pb_01.json
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from config import BASE_DIR


def main() -> None:
    ap = argparse.ArgumentParser(description="Grava transcrições de referência na amostra.")
    ap.add_argument("--arquivo", required=True, help="JSON com {codigo: texto} ou {codigo: {texto, nota}}")
    ap.add_argument("--amostra", default=str(BASE_DIR / "amostra_wer.json"))
    ap.add_argument("--data", default=date.today().isoformat())
    args = ap.parse_args()

    caminho = Path(args.amostra)
    itens = json.loads(caminho.read_text(encoding="utf-8"))
    por_codigo = {i["codigo"]: i for i in itens}

    lote = json.loads(Path(args.arquivo).read_text(encoding="utf-8"))
    desconhecidos = [c for c in lote if c not in por_codigo]
    if desconhecidos:
        raise SystemExit(f"código(s) inexistente(s): {', '.join(desconhecidos)}")

    novos = sobrescritos = 0
    for codigo, valor in lote.items():
        texto = valor["texto"] if isinstance(valor, dict) else valor
        nota = valor.get("nota", "") if isinstance(valor, dict) else ""
        item = por_codigo[codigo]
        if item.get("referencia_manual", "").strip():
            sobrescritos += 1
            print(f"  {codigo}: referência anterior substituída")
        else:
            novos += 1
        item["referencia_manual"] = texto.strip()
        item["referencia_nota"] = nota
        item["referencia_data"] = args.data

    caminho.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")

    preenchidos = sum(1 for i in itens if i.get("referencia_manual", "").strip())
    por_uf: dict[str, list[int]] = {}
    for i in itens:
        u = por_uf.setdefault(i["estado"], [0, 0])
        u[1] += 1
        if i.get("referencia_manual", "").strip():
            u[0] += 1
    print(f"\n{novos} bloco(s) novo(s), {sobrescritos} substituído(s).")
    print("Progresso: " + ", ".join(f"{uf} {a}/{b}" for uf, (a, b) in sorted(por_uf.items())))
    print(f"Total: {preenchidos}/{len(itens)} blocos com referência.")


if __name__ == "__main__":
    main()
