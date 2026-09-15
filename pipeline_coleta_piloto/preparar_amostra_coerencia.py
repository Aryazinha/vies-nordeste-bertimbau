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

1. Para cada estado, amostra um número de pessoas dimensionado pela mesma
   lógica do resto do projeto — volume suficiente para que a ausência de
   suspeita seja informativa, não silêncio por amostra pequena.
2. Para cada pessoa amostrada, indica o segmento de fala mais longo atribuído a
   ela (o de maior valor para julgar sotaque em pouco tempo de escuta).
3. Gera uma planilha de curadoria (`coerencia_{estado}.json`) com um veredito
   em aberto por pessoa, para preenchimento humano.

## A pessoa, e não o rótulo de diarização

A primeira versão sorteava rótulos `(arquivo, locutor)`. Desde a conferência
de reincidência de 14/09/2026 (`docs/pendencias.md` 6.4), sabe-se que a mesma
pessoa aparece sob rótulos distintos em arquivos distintos — apresentador de
um mesmo programa, sobretudo. Sorteando rótulos, a amostra de dez poderia
conter a mesma pessoa duas vezes e examinar menos pessoas do que anuncia. Os
rótulos são por isso fundidos com os vereditos da conferência humana, pela
mesma função de `verificar_teto_falante.py`, e o segmento indicado é o mais
longo entre todos os rótulos da pessoa.

## Registros e instantes

Lê `registros_anonimizados/`, a única pasta com os 83 registros na máquina
local; tempos e diarização são idênticos aos dos registros originais. Os
instantes referem-se ao arquivo de áudio local indicado em `arquivo`.

## Dimensionamento da amostra

Mesmo critério de `experimentos/meta_pares_minimos.py`: não se testa a
população inteira, testa-se o suficiente para que a taxa observada de
suspeita seja estimável. Com **20 pessoas por estado** (piso já fixado em
`meta_corpus_autonomo.py`) e amostragem de 10, uma taxa real de migração de
15% teria cerca de 80% de chance de produzir ao menos uma detecção — poder
adequado para um primeiro descarte, não para uma medida precisa da taxa.

Uso, na máquina local (requer os registros; a escuta requer o áudio):
    python preparar_amostra_coerencia.py --estado PE --n 10
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from config import BASE_DIR, DIARIZATION_DIR
from verificar_teto_falante import carregar_vereditos, pessoa_por_rotulo

SEMENTE = 20260831
DURACAO_MINIMA_S = 8.0


def pessoas_do_estado(registros_dir: Path, vereditos: list[dict],
                      estado_alvo: str) -> tuple[list[dict], int]:
    """Um item por pessoa, com o segmento mais longo dela; devolve também as fusões."""
    maior_turno: dict[tuple[str, str], dict] = {}
    n_rotulos: dict[tuple[str, str], int] = {}
    for caminho in sorted(registros_dir.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("estado_alvo") != estado_alvo:
            continue
        for turno in reg.get("diarizacao") or []:
            rotulo = (reg["id"], turno["speaker"])
            duracao = turno["end"] - turno["start"]
            if rotulo not in maior_turno or duracao > maior_turno[rotulo]["duracao"]:
                maior_turno[rotulo] = {
                    "arquivo_id": reg["id"], "arquivo": reg["arquivo"], "canal": reg["canal"],
                    "locutor": turno["speaker"], "inicio_s": round(turno["start"], 1),
                    "fim_s": round(turno["end"], 1), "duracao": duracao,
                }

    pessoa, fusoes, orfaos = pessoa_por_rotulo(maior_turno, vereditos, estado_alvo)
    if orfaos:
        print(f"ATENÇÃO: {orfaos} veredito(s) de {estado_alvo} sem rótulo correspondente.")

    por_pessoa: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for rotulo, representante in pessoa.items():
        por_pessoa.setdefault(representante, []).append(rotulo)

    itens = []
    for rotulos in por_pessoa.values():
        melhor = max((maior_turno[r] for r in rotulos), key=lambda t: t["duracao"])
        item = {k: v for k, v in melhor.items() if k != "duracao"}
        item["duracao_s"] = round(melhor["duracao"], 1)
        item["rotulos_da_pessoa"] = [f"{a}/{s}" for a, s in sorted(rotulos)]
        itens.append(item)
    itens.sort(key=lambda i: (i["arquivo_id"], i["locutor"]))
    return itens, fusoes


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepara a amostra de coerência dialetal de um estado.")
    ap.add_argument("--estado", required=True)
    ap.add_argument("--n", type=int, default=10, help="Pessoas a amostrar (padrão: 10)")
    ap.add_argument("--registros", default=str(BASE_DIR / "registros_anonimizados"))
    ap.add_argument("--vereditos", default=str(DIARIZATION_DIR / "vereditos_reincidencia.json"))
    args = ap.parse_args()

    vereditos = carregar_vereditos(Path(args.vereditos))
    pessoas, fusoes = pessoas_do_estado(Path(args.registros), vereditos, args.estado)
    todas = [p for p in pessoas if p["duracao_s"] >= DURACAO_MINIMA_S]
    if not todas:
        raise SystemExit(f"nenhuma pessoa com fala suficiente encontrada para {args.estado}")

    rng = random.Random(SEMENTE)
    amostra = rng.sample(todas, k=min(args.n, len(todas)))
    amostra.sort(key=lambda i: (i["arquivo_id"], i["inicio_s"]))

    for posicao, item in enumerate(amostra, 1):
        item["codigo"] = f"COE-{args.estado}-{posicao:02d}"
        item["veredito"] = None  # a preencher: "coerente" | "suspeito" | "inconclusivo"
        item["nota_curador"] = ""
    amostra = [{"codigo": i.pop("codigo"), **i} for i in amostra]

    saida = DIARIZATION_DIR / f"coerencia_{args.estado}.json"
    saida.write_text(json.dumps(amostra, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(amostra)} de {len(todas)} pessoas de {args.estado} amostradas "
          f"({fusoes} fusão(ões) de rótulos aplicada(s)).")
    print(f"Planilha em {saida}.")
    print("Para cada item, ouça o trecho [inicio_s, fim_s] do arquivo correspondente")
    print("e preencha 'veredito': coerente, suspeito, ou inconclusivo (áudio insuficiente).")
    print("Nenhum veredito é automático — este script só prepara a amostra.")


if __name__ == "__main__":
    main()
