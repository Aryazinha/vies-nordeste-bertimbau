"""
registrar_coerencia.py

Grava na planilha `coerencia_{UF}.json` os vereditos da escuta de coerência
dialetal — item 10 do plano de fechamento, condição C5 de
`docs/criterio_conclusao_v1.md`.

## A forma do comando segue a forma da conferência

A escuta é conduzida em conversa, e quem ouve informa apenas os itens que
**não** são coerentes, contando os demais como coerentes — método adotado em
15/09/2026, depois de a conferência por arquivo de colunas a preencher se
mostrar confusa. O comando reproduz isso: nomeiam-se os suspeitos e os
inconclusivos, e `--resto-coerente` fecha o restante do estado.

Sem `--resto-coerente`, apenas os itens nomeados são alterados, e os demais
permanecem sem veredito — o que serve para registrar uma escuta parcial sem
afirmar o que não foi ouvido.

Uso:
    python registrar_coerencia.py --estado PB --suspeito COE-PB-04 \
        --inconclusivo COE-PB-06 --resto-coerente
    python registrar_coerencia.py --estado PB --resto-coerente
"""

from __future__ import annotations

import argparse
import json
from datetime import date

from config import DIARIZATION_DIR


def main() -> None:
    ap = argparse.ArgumentParser(description="Registra os vereditos de coerência dialetal.")
    ap.add_argument("--estado", required=True)
    ap.add_argument("--suspeito", nargs="*", default=[], help="Códigos com veredito 'suspeito'")
    ap.add_argument("--inconclusivo", nargs="*", default=[],
                    help="Códigos com veredito 'inconclusivo'")
    ap.add_argument("--coerente", nargs="*", default=[], help="Códigos com veredito 'coerente'")
    ap.add_argument("--resto-coerente", action="store_true",
                    help="Marca como 'coerente' todo item do estado ainda sem veredito")
    ap.add_argument("--nota", default="", help="Nota aplicada aos itens nomeados")
    ap.add_argument("--data", default=date.today().isoformat())
    args = ap.parse_args()

    planilha = DIARIZATION_DIR / f"coerencia_{args.estado}.json"
    if not planilha.exists():
        raise SystemExit(f"{planilha} não existe.")
    itens = json.loads(planilha.read_text(encoding="utf-8"))
    por_codigo = {i["codigo"]: i for i in itens}

    nomeados = {c: "suspeito" for c in args.suspeito}
    nomeados.update({c: "inconclusivo" for c in args.inconclusivo})
    nomeados.update({c: "coerente" for c in args.coerente})

    desconhecidos = [c for c in nomeados if c not in por_codigo]
    if desconhecidos:
        raise SystemExit(f"código(s) inexistente(s) em {planilha.name}: {', '.join(desconhecidos)}")

    for codigo, veredito in nomeados.items():
        item = por_codigo[codigo]
        item["veredito"] = veredito
        item["nota_curador"] = args.nota
        item["verificado_em"] = args.data

    if args.resto_coerente:
        for item in itens:
            if item.get("veredito") is None:
                item["veredito"] = "coerente"
                item["verificado_em"] = args.data

    planilha.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")

    contagem = {v: sum(1 for i in itens if i.get("veredito") == v)
                for v in ("coerente", "suspeito", "inconclusivo")}
    sem = sum(1 for i in itens if i.get("veredito") is None)
    print(f"{args.estado}: " + ", ".join(f"{n} {v}" for v, n in contagem.items())
          + (f", {sem} sem veredito" if sem else ""))
    for i in itens:
        if i.get("veredito") in ("suspeito", "inconclusivo"):
            print(f"  {i['codigo']}  {i['veredito']}  {i['canal']}  {i['arquivo_id']}")
    print(f"Gravado em {planilha}.")


if __name__ == "__main__":
    main()
