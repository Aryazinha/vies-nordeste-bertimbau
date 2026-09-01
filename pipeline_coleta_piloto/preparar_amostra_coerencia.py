"""
preparar_amostra_coerencia.py

Responde à pendência D-6.2: checagem de coerência dialetal contra falante
migrante. **Não é um detector automático** — e a razão de não ser está
documentada no próprio projeto, não é limitação deste script.

## Por que não existe atalho automático

Duas vias óbvias de automação foram consideradas e as duas falham com base em
achados já registrados:

1. **Densidade de marcadores lexicais regionais** (`arretado`, `oxe`...). O
   item 2.4 de `docs/achados_para_o_artigo.md` mediu **zero** ocorrências
   desses itens em 30 mil palavras de fala nordestina genuína. Um detector
   baseado neles marcaria como suspeito quase todo falante nordestino
   verdadeiro — o sinal é fraco demais até nos falantes que não migraram.
2. **Densidade de contextos de palatalização.** `densidade_palatalizacao.py`
   conta contextos **ortográficos** (`ti`, `di`, `-te`, `-de`), não a
   realização fonética em si — que é o que de fato distingue variedade. Os
   mesmos contextos ortográficos existem em qualquer fala do português,
   nordestina ou não; sem análise acústica do áudio (alinhamento forçado e
   classificação de fone), essa via não separa quem palataliza de quem não
   palataliza.

Forçar um destes dois em produção arriscaria repetir o erro que o passo 5.5 já
corrigiu uma vez: um sinal fraco lido como se fosse forte. A defesa efetiva
continua sendo a que o projeto já registrou — **curadoria manual, ouvindo a
fala**. O que faltava não era o método, era torná-lo executável em vez de
ficar só na frase "curadoria manual deve ser feita".

## O que este script faz

Prepara o material para a curadoria, e não decide nada sozinho:

1. Para cada estado, amostra um número de locutores dimensionado pela mesma
   lógica do resto do projeto — volume suficiente para que a ausência de
   suspeita seja informativa, não silêncio por amostra pequena.
2. Para cada locutor amostrado, recorta o segmento de fala mais longo
   atribuído a ele (o de maior valor para julgar sotaque em pouco tempo de
   escuta).
3. Gera uma planilha de curadoria (`coerencia_{estado}.json`) com um veredito
   em aberto por locutor, para preenchimento humano.

## Dimensionamento da amostra

Mesmo critério de `experimentos/meta_pares_minimos.py`: não se testa a
população inteira, testa-se o suficiente para que a taxa observada de
suspeita seja estimável. Com **20 locutores por estado** (piso já fixado em
`meta_corpus_autonomo.py`) e amostragem de 10, uma taxa real de migração de
15% teria cerca de 80% de chance de produzir ao menos uma detecção — poder
adequado para um primeiro descarte, não para uma medida precisa da taxa.

Uso, no ambiente de processamento (requer áudio e registros finais):
    python preparar_amostra_coerencia.py --estado PE --n 10
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from config import AUDIO_DIR, DIARIZATION_DIR, FINAL_DIR

SEMENTE = 20260831


def locutores_do_estado(estado_alvo: str) -> list[dict]:
    """Um item por locutor com fala suficiente, com o segmento mais longo dele."""
    locutores = []
    for caminho in sorted(FINAL_DIR.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("estado_alvo") != estado_alvo:
            continue
        por_locutor: dict[str, list[tuple[float, float]]] = {}
        for turno in reg["diarizacao"]:
            por_locutor.setdefault(turno["speaker"], []).append((turno["start"], turno["end"]))
        for locutor, turnos in por_locutor.items():
            maior = max(turnos, key=lambda t: t[1] - t[0])
            locutores.append({
                "arquivo_id": reg["id"], "arquivo": reg["arquivo"], "canal": reg["canal"],
                "locutor": locutor, "inicio_s": maior[0], "fim_s": maior[1],
                "duracao_s": round(maior[1] - maior[0], 1),
            })
    return locutores


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--estado", required=True)
    ap.add_argument("--n", type=int, default=10, help="Locutores a amostrar (padrão: 10)")
    args = ap.parse_args()

    todos = [l for l in locutores_do_estado(args.estado) if l["duracao_s"] >= 8.0]
    if not todos:
        raise SystemExit(f"nenhum locutor com fala suficiente encontrado para {args.estado}")

    rng = random.Random(SEMENTE)
    amostra = rng.sample(todos, k=min(args.n, len(todos)))

    for item in amostra:
        item["veredito"] = None  # a preencher: "coerente" | "suspeito" | "inconclusivo"
        item["nota_curador"] = ""

    saida = DIARIZATION_DIR / f"coerencia_{args.estado}.json"
    saida.write_text(json.dumps(amostra, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(amostra)} de {len(todos)} locutores de {args.estado} amostrados.")
    print(f"Planilha em {saida}.")
    print("Para cada item, ouça o trecho [inicio_s, fim_s] do arquivo correspondente")
    print("e preencha 'veredito': coerente, suspeito, ou inconclusivo (áudio insuficiente).")
    print("Nenhum veredito é automático — este script só prepara a amostra.")


if __name__ == "__main__":
    main()
