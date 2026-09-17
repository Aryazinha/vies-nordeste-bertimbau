"""
medir_wer.py

Mede a Taxa de Erro de Palavra (WER) da transcrição automática, **por estado**,
sobre `amostra_wer.json` com o campo `referencia_manual` preenchido à mão
(item 11 do plano de fechamento; condição C6 de `docs/criterio_conclusao_v1.md`).

## Por que a medição não é automática

WER exige transcrição humana de referência; não há atalho. `preparar_amostra_wer.py`
sorteia os blocos e `preparar_clipes_wer.py` os recorta em arquivos próprios,
mas alguém precisa ouvir e digitar. O que este script faz é fechar a conta
depois, sob regras declaradas.

## O que este script reporta, e por quê

1. **WER por estado**, nunca apenas o agregado: a ameaça registrada na Parte 3
   do `CLAUDE.md` é o erro ser maior para a fala nordestina, o que seria viés
   de ferramenta apresentando-se como resultado sobre o modelo-alvo.
2. **WER por estado e camada de fonte.** A amostra não é estratificada por
   camada (`docs/pendencias.md` 4.11), e a entrevista de rua, mais ruidosa,
   pesa de modo desigual entre os estados. Sem este recorte, composição de
   amostra pode ser lida como diferença de variedade.
3. **Dois números: com e sem equivalências de fala reduzida** (decisão da
   equipe em 17/09/2026; ver `normalizar_wer.py`). A diferença entre eles mede
   o quanto do erro é regularização ortográfica do reconhecedor, e não falha de
   compreensão.
4. **Blocos com trecho inaudível à parte.** Onde o ouvinte humano marcou `[?]`
   ou `[inaudível]`, o bloco sai do cálculo principal e é contado em separado:
   tratá-lo como erro puniria a máquina por limite do ouvinte, e o faria mais
   onde o áudio é pior — na direção que favorece a hipótese do projeto.
5. **Blocos ainda sem referência**, explicitamente, para que amostra incompleta
   nunca seja lida como amostra medida.

Uso:
    pip install jiwer
    python medir_wer.py
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import jiwer

from config import BASE_DIR, ESTADOS_NORDESTE, ESTADOS_CONTROLE
from normalizar_wer import normalizar

INAUDIVEL = re.compile(r"\[\s*(\?|inaud[ií]vel)\s*\]", re.IGNORECASE)


def wer_de(pares: list[tuple[str, str]], equivalencias: bool) -> float | None:
    if not pares:
        return None
    refs = [normalizar(r, equivalencias) for r, _ in pares]
    hips = [normalizar(h, equivalencias) for _, h in pares]
    return jiwer.wer(refs, hips)


def linha(rotulo: str, pares: list[tuple[str, str]]) -> str:
    literal, equiv = wer_de(pares, False), wer_de(pares, True)
    palavras = sum(len(normalizar(r).split()) for r, _ in pares)
    return (f"  {rotulo:28} {len(pares):>4} blocos {palavras:>6} palavras "
            f"  WER {literal:.3f}  |  com equivalências {equiv:.3f}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Calcula o WER por estado.")
    ap.add_argument("--entrada", default=str(BASE_DIR / "amostra_wer.json"))
    args = ap.parse_args()

    itens = json.loads(Path(args.entrada).read_text(encoding="utf-8"))

    pendentes = [i for i in itens if not i.get("referencia_manual", "").strip()]
    preenchidos = [i for i in itens if i.get("referencia_manual", "").strip()]
    inaudiveis = [i for i in preenchidos if INAUDIVEL.search(i["referencia_manual"])]
    prontos = [i for i in preenchidos if i not in inaudiveis]

    if pendentes:
        por_uf = defaultdict(int)
        for i in pendentes:
            por_uf[i["estado"]] += 1
        print(f"{len(pendentes)} de {len(itens)} blocos ainda sem referência manual, "
              f"fora do cálculo:")
        print("  " + ", ".join(f"{uf}: {n}" for uf, n in sorted(por_uf.items())) + "\n")

    if not prontos:
        raise SystemExit("Nenhum bloco com referência preenchida — nada a medir.")

    por_estado: dict[str, list[tuple[str, str]]] = defaultdict(list)
    por_estado_camada: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for i in prontos:
        par = (i["referencia_manual"], i["hipotese_asr"])
        por_estado[i["estado"]].append(par)
        por_estado_camada[(i["estado"], i["camada"])].append(par)

    print(f"WER por estado ({len(prontos)} blocos medidos):\n")
    for uf in ESTADOS_NORDESTE + ESTADOS_CONTROLE:
        if uf in por_estado:
            print(linha(uf, por_estado[uf]))

    print("\nPor estado e camada de fonte:\n")
    for (uf, camada), pares in sorted(por_estado_camada.items()):
        print(linha(f"{uf} / {camada}", pares))

    ne = [p for uf in ESTADOS_NORDESTE for p in por_estado.get(uf, [])]
    se = [p for uf in ESTADOS_CONTROLE for p in por_estado.get(uf, [])]
    print("\nComparação entre os grupos:\n")
    if ne:
        print(linha("Nordeste", ne))
    if se:
        print(linha("Controle (SP, RJ)", se))
    if ne and se:
        d_lit = wer_de(ne, False) - wer_de(se, False)
        d_eq = wer_de(ne, True) - wer_de(se, True)
        print(f"\n  Diferença Nordeste − Controle: {d_lit:+.3f} literal, {d_eq:+.3f} com equivalências.")
        print("  Diferença positiva significa transcrição pior para a fala nordestina.")

    if inaudiveis:
        por_uf = defaultdict(int)
        for i in inaudiveis:
            por_uf[i["estado"]] += 1
        print(f"\n{len(inaudiveis)} bloco(s) com marca de inaudível, fora do cálculo acima: "
              + ", ".join(f"{uf}: {n}" for uf, n in sorted(por_uf.items())))
        print("  A distribuição dessas marcas entre estados é resultado por si só:")
        print("  mede o que o ouvinte humano não entendeu, não o que a máquina errou.")

    print("\nO número geral não é o resultado a reportar — o que importa é a comparação")
    print("entre estados e a ressalva de camada (ver docs/pendencias.md 4.11).")


if __name__ == "__main__":
    main()
