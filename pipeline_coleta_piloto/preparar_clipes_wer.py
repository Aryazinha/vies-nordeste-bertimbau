"""
preparar_clipes_wer.py

Recorta em arquivos próprios os trechos de `amostra_wer.json`, nomeados pelo
código do trecho, para a transcrição manual do item 11 do plano de fechamento
(condição C6 de `docs/criterio_conclusao_v1.md`).

## Por que recortar

A transcrição é trabalho humano de escuta repetido 900 vezes. Obrigar quem
transcreve a abrir o arquivo de origem e localizar o instante a cada trecho
acrescenta uma etapa de navegação a cada item, sem contrapartida. Recortado, o
trabalho é abrir a pasta e ouvir na ordem. Mesma razão de
`preparar_clipes_coerencia.py`.

**A hipótese do ASR não acompanha o clipe, e isso é deliberado:** quem
transcreve não pode ver o que a máquina escreveu, sob pena de ancorar a
transcrição de referência na saída que ela deveria avaliar.

Os clipes contêm fala e ficam em `dataset_raw/`, fora do versionamento. São
descartáveis: basta rodar de novo.

Uso:
    python preparar_clipes_wer.py --estado PB
    python preparar_clipes_wer.py --codigos PB-001 CE-004 --pasta teste
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from config import AUDIO_DIR, BASE_DIR


def main() -> None:
    ap = argparse.ArgumentParser(description="Recorta os trechos da amostra do WER.")
    ap.add_argument("--estado", help="Recorta todos os trechos do estado")
    ap.add_argument("--codigos", nargs="*", default=[], help="Recorta apenas estes códigos")
    ap.add_argument("--pasta", default=None,
                    help="Subpasta de destino (padrão: o estado do trecho)")
    ap.add_argument("--amostra", default=str(BASE_DIR / "amostra_wer.json"))
    args = ap.parse_args()

    if not args.estado and not args.codigos:
        raise SystemExit("informe --estado ou --codigos")

    itens = json.loads(Path(args.amostra).read_text(encoding="utf-8"))
    alvo = [i for i in itens
            if (args.estado and i["estado"] == args.estado) or i["codigo"] in args.codigos]
    if not alvo:
        raise SystemExit("nenhum trecho corresponde ao pedido")

    for item in alvo:
        origem = AUDIO_DIR / item["arquivo"]
        if not origem.exists():
            print(f"{item['codigo']}: áudio ausente, pulado.")
            continue
        destino = BASE_DIR / "escuta_wer" / (args.pasta or item["estado"])
        destino.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", str(origem),
             "-ss", f"{item['inicio_s']:.2f}", "-to", f"{item['fim_s']:.2f}",
             "-acodec", "pcm_s16le", str(destino / f"{item['codigo']}.wav")],
            check=True,
        )
        print(f"{item['codigo']}  {item['fim_s'] - item['inicio_s']:5.1f} s  "
              f"{item['estado']}  {item['camada']}")

    print(f"\n{len(alvo)} clipe(s) recortado(s).")


if __name__ == "__main__":
    main()
