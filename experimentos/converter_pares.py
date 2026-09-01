"""
converter_pares.py

Converte o conjunto canônico `pares_minimos.json` para o formato tabular dos
precedentes da área — CrowS-Pairs distribui um CSV com identificador, os dois
lados e o tipo de viés —, de modo que quem já tem esteira montada para aquele
formato possa usar este conjunto sem reescrevê-la.

**O CSV não é publicado.** É saída sob demanda, e essa é a razão de existir do
script: manter dois artefatos publicados em sincronia é dívida que sempre
acaba sendo paga com divergência silenciosa entre eles. O canônico é um só, e
o tabular se deriva dele.

## O que se perde na conversão, e por que isso precisa ser dito

O formato tabular tem uma linha por par, e o conjunto canônico não cabe numa
linha. Ficam de fora:

- a **extensão em subtokens** de cada atributo, que é a informação que impede a
  repetição do artefato de tokenização do passo 5.5;
- as **anotações de juízes**, que são lista e não valor único (hoje vazias em
  todos os pares, porque o Filtro 1 nunca foi aplicado);
- as **advertências do cabeçalho**, entre elas a de que o eixo de prestígio
  ocupacional não tem medição válida.

Por isso o CSV gerado traz, na primeira linha, um comentário apontando para o
arquivo canônico. Quem usar só o CSV precisa saber que está usando um recorte.

Uso:
    python converter_pares.py                    # imprime na saída padrão
    python converter_pares.py --saida pares.csv  # grava em arquivo
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

CANONICO = Path(__file__).resolve().parent / "resultados" / "dados" / "pares_minimos.json"

COLUNAS = ["id", "sent_more", "sent_less", "bias_type", "papel", "grupo",
           "n_medicoes", "mediana_d_pll", "razao_frequencia", "residuo",
           "n_juizes"]


def converter(pacote: dict) -> str:
    buf = io.StringIO()
    buf.write("# Recorte tabular de pares_minimos.json — perde subtokens por atributo, "
              "anotações de juízes e advertências. Use o JSON canônico como referência.\n")
    w = csv.DictWriter(buf, fieldnames=COLUNAS, lineterminator="\n")
    w.writeheader()
    for p in pacote["pares"]:
        m = p["medicao"] or {}
        w.writerow({
            # `sent_more`/`sent_less` são os nomes do CrowS-Pairs. Aqui não
            # carregam a semântica de "mais" e "menos estereotipado": os lados
            # A e B são as duas variantes do par, e a direção do efeito está em
            # `mediana_d_pll`, com sinal. Renomear seria fingir equivalência.
            "id": p["id"],
            "sent_more": p["lado_a"],
            "sent_less": p["lado_b"],
            "bias_type": p["condicao"],
            "papel": p["papel"],
            "grupo": p["grupo"],
            "n_medicoes": m.get("n_medicoes", ""),
            "mediana_d_pll": m.get("mediana_d_pll", ""),
            "razao_frequencia": m.get("razao_frequencia", ""),
            "residuo": m.get("residuo", ""),
            "n_juizes": len(p["anotacoes_juizes"]),
        })
    return buf.getvalue()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", default=str(CANONICO))
    ap.add_argument("--saida", default=None, help="Arquivo de saída (padrão: saída padrão)")
    args = ap.parse_args()

    caminho = Path(args.entrada)
    if not caminho.exists():
        raise SystemExit(f"{caminho} não existe. Rode empacotar_pares.py primeiro.")

    texto = converter(json.loads(caminho.read_text(encoding="utf-8")))
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8")
        print(f"{len(texto.splitlines()) - 2} pares gravados em {args.saida}.")
    else:
        sys.stdout.write(texto)


if __name__ == "__main__":
    main()
