"""
preparar_clipes_coerencia.py

Recorta em arquivos próprios os trechos da amostra de coerência dialetal
(`coerencia_{UF}.json`, produzido por `preparar_amostra_coerencia.py`), um por
pessoa, nomeados pelo código do item — item 10 do plano de fechamento,
condição C5 de `docs/criterio_conclusao_v1.md`.

## Por que recortar, se a planilha já traz arquivo e instantes

A curadoria é trabalho humano de escuta, e a planilha obrigava quem ouve a
abrir o arquivo de origem, localizar o instante e repetir isso sessenta vezes.
O recorte elimina a etapa de navegação: cada pessoa da amostra vira um arquivo
de dez a sessenta segundos, e a escuta passa a ser abrir a pasta e ouvir na
ordem. O veredito continua humano e continua sendo registrado na planilha.

O recorte é operação de conveniência: não altera a amostra, não reencontra
locutor nem reinterpreta a diarização, e os arquivos gerados são descartáveis
— basta rodar de novo para reconstruí-los.

Os clipes contêm fala e são gravados em `dataset_raw/`, fora do versionamento.

Uso:
    python preparar_clipes_coerencia.py --estado PB
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from config import AUDIO_DIR, BASE_DIR, DIARIZATION_DIR


def main() -> None:
    ap = argparse.ArgumentParser(description="Recorta os trechos da amostra de coerência.")
    ap.add_argument("--estado", required=True)
    ap.add_argument("--margem", type=float, default=0.0,
                    help="Segundos de folga antes e depois (padrão: 0; a folga pode "
                         "trazer outra voz para dentro do trecho)")
    args = ap.parse_args()

    planilha = DIARIZATION_DIR / f"coerencia_{args.estado}.json"
    if not planilha.exists():
        raise SystemExit(f"{planilha} não existe — rode preparar_amostra_coerencia.py antes.")
    itens = json.loads(planilha.read_text(encoding="utf-8"))

    destino = BASE_DIR / "escuta_coerencia" / args.estado
    destino.mkdir(parents=True, exist_ok=True)

    for item in itens:
        origem = AUDIO_DIR / item["arquivo"]
        if not origem.exists():
            print(f"{item['codigo']}: áudio ausente ({item['arquivo']}), pulado.")
            continue
        inicio = max(0.0, item["inicio_s"] - args.margem)
        fim = item["fim_s"] + args.margem
        saida = destino / f"{item['codigo']}.wav"
        subprocess.run(
            ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", str(origem),
             "-ss", f"{inicio:.2f}", "-to", f"{fim:.2f}", "-acodec", "pcm_s16le", str(saida)],
            check=True,
        )
        print(f"{item['codigo']}  {item['duracao_s']:5.1f} s  {item['canal']}")

    print(f"\n{len(itens)} clipe(s) em {destino}")
    print("Ouça na ordem e registre o veredito de cada um na planilha "
          f"({planilha.name}), por `registrar_coerencia.py`.")


if __name__ == "__main__":
    main()
