"""
coletar_local.py

Executa a coleta de áudio na máquina local e grava, junto do áudio, os metadados
necessários para que o processamento prossiga em outro ambiente.

**Por que a coleta é local e o processamento não.** O YouTube recusa downloads
originados de datacenter, respondendo "Sign in to confirm you're not a bot". A
tentativa de coletar no Google Colab em 27/08/2026 resultou em 0 de 51 vídeos.
Conexão residencial não sofre esse bloqueio. Por outro lado, a transcrição com
`large-v3` e a diarização exigem GPU, indisponível na máquina local. A esteira
divide-se, portanto, em duas metades, cada uma no ambiente em que funciona:

    coleta (aqui)  ->  Google Drive  ->  transcrição e diarização (Colab)

Este módulo cobre a primeira metade. Ver `notebooks/piloto_colab.ipynb` para a
segunda e `docs/pendencias.md`, seção 4.8, para o registro da limitação.

Uso:
    python selecionar_videos.py --piloto --max-canais 2 --saida plano_piloto.json
    python coletar_local.py plano_piloto.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from config import AUDIO_DIR, BASE_DIR
from collect import coletar_lote

METADADOS = BASE_DIR / "metadados.json"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano", help="arquivo gerado por selecionar_videos.py")
    ap.add_argument("--limite", type=int, default=None,
                    help="processa apenas os N primeiros trechos, para ensaio")
    args = ap.parse_args()

    specs = json.loads(Path(args.plano).read_text(encoding="utf-8"))["specs"]
    if args.limite:
        specs = specs[:args.limite]

    print(f"{len(specs)} trechos planejados\n")
    metas = coletar_lote(specs)

    # Persiste os metadados ao lado do áudio. Sem isso, o ambiente de
    # processamento receberia arquivos .wav sem saber a que estado, camada ou
    # canal cada um pertence — e a atribuição regional é a variável do estudo.
    registros = []
    for m in metas:
        d = asdict(m)
        d.pop("title", None)
        d["arquivo"] = f"{m.id}.wav"
        registros.append(d)

    METADADOS.write_text(json.dumps(registros, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    tamanho = sum(f.stat().st_size for f in AUDIO_DIR.glob("*.wav")) / 1024**2
    faltaram = len(specs) - len(metas)

    print(f"\n{len(metas)}/{len(specs)} coletados")
    if faltaram:
        print(f"{faltaram} falharam — as causas foram registradas acima, por vídeo. "
              "Verifique se a perda se concentra em algum estado ou camada: "
              "perda desigual entre grupos é viés de amostragem, não ruído.")
    print(f"Áudio em {AUDIO_DIR} ({tamanho:.0f} MB)")
    print(f"Metadados em {METADADOS}")
    print("\nPróximo passo: enviar a pasta dataset_raw para o Google Drive e "
          "executar notebooks/piloto_colab.ipynb.")


if __name__ == "__main__":
    main()
