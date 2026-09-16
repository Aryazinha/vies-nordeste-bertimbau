"""
registrar_participacao.py

Grava em `dataset_raw/metadados.json` o resultado da escuta de um arquivo
quanto à participação de ouvinte — condição C4 de
`docs/criterio_conclusao_v1.md`, item 9 do plano de fechamento.

## Por que existe um script para uma edição de três campos

O campo `participacao_ouvinte` é **fato do arquivo, estabelecido por escuta
humana** (`balanco_participacao.py`), e não se deduz de metadado nenhum.
Editá-lo à mão no JSON não deixa registro de quando a escuta ocorreu nem do
que foi ouvido, e um erro de digitação em `metadados.json` afeta todo o
pipeline. O script grava sempre os mesmos campos, na mesma forma, e recusa
identificador inexistente.

## Os campos gravados

- `participacao_ouvinte`: `sim`, `nao` ou `inconclusivo`. Nasce
  `nao_verificado` e só muda aqui.
- `participacao_ouvinte_s`: **segundos de fala de ouvinte**, e não a duração do
  arquivo. A distinção é o ponto: no primeiro arquivo ouvido, 43 s de ligação
  num arquivo de 516 s, contar o arquivo inteiro multiplicaria por doze o
  volume atribuído à Bahia e produziria alerta de desequilíbrio onde não há.
- `participacao_ouvinte_nota`: o que foi ouvido, em uma linha, sem reproduzir
  fala.
- `participacao_ouvinte_verificado_em`: data da escuta, `AAAA-MM-DD`.

Uso:
    python registrar_participacao.py --id kMd1ga7Tz5g --participacao sim \
        --segundos 43 --nota "voz de ouvinte ao telefone, 4:40-5:23"
    python registrar_participacao.py --id Z_ZLH1hratI --participacao nao
"""

from __future__ import annotations

import argparse
import json
from datetime import date

from config import BASE_DIR

METADADOS = BASE_DIR / "metadados.json"
VALORES = ("sim", "nao", "inconclusivo")


def main() -> None:
    ap = argparse.ArgumentParser(description="Registra a escuta de participação de ouvinte.")
    ap.add_argument("--id", required=True, help="Identificador do vídeo, chave do registro")
    ap.add_argument("--participacao", required=True, choices=VALORES)
    ap.add_argument("--segundos", type=float, default=None,
                    help="Segundos de fala de ouvinte (obrigatório quando --participacao sim)")
    ap.add_argument("--nota", default="", help="O que foi ouvido, em uma linha")
    ap.add_argument("--data", default=date.today().isoformat(), help="Data da escuta (AAAA-MM-DD)")
    args = ap.parse_args()

    if args.participacao == "sim" and args.segundos is None:
        raise SystemExit("--segundos é obrigatório quando a participação é 'sim': "
                         "o volume por estado conta segundos de fala de ouvinte, "
                         "não a duração do arquivo.")

    registros = json.loads(METADADOS.read_text(encoding="utf-8"))
    alvo = [r for r in registros if r["id"] == args.id]
    if not alvo:
        raise SystemExit(f"nenhum registro com id {args.id} em {METADADOS}")
    reg = alvo[0]

    anterior = reg.get("participacao_ouvinte", "nao_verificado")
    reg["participacao_ouvinte"] = args.participacao
    reg["participacao_ouvinte_s"] = float(args.segundos or 0)
    reg["participacao_ouvinte_nota"] = args.nota
    reg["participacao_ouvinte_verificado_em"] = args.data

    METADADOS.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{args.id} ({reg['estado_alvo']}, {reg['canal']}): "
          f"{anterior} -> {args.participacao}, {reg['participacao_ouvinte_s']:.0f} s "
          f"de fala de ouvinte em {reg.get('duracao_coletada_s') or reg['duracao_s']} s de arquivo.")
    print(f"Gravado em {METADADOS}. Rode `python balanco_participacao.py` para o relatório.")


if __name__ == "__main__":
    main()
