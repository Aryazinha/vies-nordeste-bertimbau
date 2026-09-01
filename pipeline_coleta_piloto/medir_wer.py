"""
medir_wer.py

Completa a pendência A.4 da ficha do conjunto (`docs/ficha_conjunto.md`): mede
a Taxa de Erro de Palavra (WER) da transcrição automática, por estado, uma vez
preenchido manualmente o campo `referencia_manual` de `amostra_wer.json`.

## Por que a medição não é automática

WER exige uma transcrição humana de referência para comparar contra a
transcrição do `faster-whisper`; não há atalho. O notebook
(`notebooks/piloto_colab.ipynb`, célula 6.4) já prepara a amostra — até 20
minutos de trechos por estado, cada um com `hipotese_asr` (o que o modelo
transcreveu) e `referencia_manual` em branco —, mas alguém precisa ouvir cada
trecho e digitar o que de fato foi dito. Esse trabalho é humano; o que faltava
não era o método, era o script que fecha a conta depois que ele for feito.

A comparação é sempre **por estado**, nunca só a média geral: a ameaça
"Qualidade da transcrição automática" (Parte 3 do `CLAUDE.md`) registra que
erro maior para fala nordestina seria viés de ferramenta, não do modelo-alvo
— e, medido corretamente, o WER estratificado é resultado publicável por si
só, não apenas controle de qualidade.

## Passo a passo, para quem for preencher a amostra

1. Gere ou recupere `amostra_wer.json` (produzido pela célula 6.4 do notebook
   Colab; é baixado separadamente do zip principal de resultados).
2. Para cada item, ouça o trecho [`inicio_s`, `fim_s`] do arquivo `id`
   correspondente e digite exatamente o que foi dito em `referencia_manual`
   — sem corrigir gramática, sem expandir números por extenso, mantendo a
   mesma convenção ortográfica do restante da transcrição automática.
3. Rode este script sobre o arquivo preenchido.

Uso:
    pip install jiwer
    python medir_wer.py --entrada amostra_wer.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import jiwer


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", default="amostra_wer.json",
                     help="Caminho do amostra_wer.json preenchido (padrão: amostra_wer.json)")
    args = ap.parse_args()

    caminho = Path(args.entrada)
    itens = json.loads(caminho.read_text(encoding="utf-8"))

    pendentes = [i for i in itens if not i.get("referencia_manual", "").strip()]
    prontos = [i for i in itens if i.get("referencia_manual", "").strip()]

    if pendentes:
        por_estado_pend: dict[str, int] = defaultdict(int)
        for i in pendentes:
            por_estado_pend[i["estado"]] += 1
        print(f"{len(pendentes)} de {len(itens)} trechos ainda sem referencia_manual, "
              f"excluídos do cálculo (preencha e rode de novo para incluí-los):")
        for uf, n in sorted(por_estado_pend.items()):
            print(f"  {uf}: {n} pendente(s)")
        print()

    if not prontos:
        raise SystemExit("Nenhum trecho com referencia_manual preenchida — nada a medir.")

    por_estado: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"refs": [], "hips": []})
    for i in prontos:
        por_estado[i["estado"]]["refs"].append(i["referencia_manual"])
        por_estado[i["estado"]]["hips"].append(i["hipotese_asr"])

    print(f"WER por estado ({len(prontos)} trechos com referência preenchida):\n")
    for uf in sorted(por_estado):
        refs, hips = por_estado[uf]["refs"], por_estado[uf]["hips"]
        wer = jiwer.wer(refs, hips)
        print(f"  {uf}: WER = {wer:.3f}  ({len(refs)} trechos)")

    wer_geral = jiwer.wer(
        [i["referencia_manual"] for i in prontos],
        [i["hipotese_asr"] for i in prontos],
    )
    print(f"\n  Geral: WER = {wer_geral:.3f}")
    print("\nO número geral não é o resultado a reportar — o que importa é a comparação")
    print("entre estados (ver a ameaça 'Qualidade da transcrição automática', Parte 3 do CLAUDE.md).")


if __name__ == "__main__":
    main()
