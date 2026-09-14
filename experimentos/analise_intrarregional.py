"""
analise_intrarregional.py — controle intrarregional da menção explícita (`docs/pendencias.md` 2.11)

## A pergunta

O controle de moldura (`analise_moldura.py`) mostrou que o rótulo nordestino não
produz mais resposta que um rótulo do Sul na mesma frase. Fica por separar se o
modelo responde a **diferença de região** entre os lados do par, ou a **qualquer
troca de rótulo geográfico** num enunciado sobre a pessoa.

Cada par de teste tem agora dois gêmeos, na mesma frase e com o mesmo lado de
comparação: o inter-regional de 2.10 (`CONTROLE_MOLDURA`), com rótulo de outra
região, e o intrarregional (`CONTROLE_INTRARREGIONAL`), com rótulo da mesma região
do lado de comparação.

## Medida primária e teste — registrados antes da medição

Para cada frase k: E_k = |Δ| do gêmeo inter-regional − |Δ| do gêmeo intrarregional.
Positivo significa que trocar por rótulo de outra região produz mais resposta que
trocar por rótulo da mesma região. Teste unilateral de média de E > 0 por
permutação exata de sinais no nível da frase; Holm sobre as quatro condições.

**Predições, em `docs/pendencias.md` 2.11:** E > 0 em `explicito_gentilico` e
`explicito_regiao`, se o modelo responde a diferença de região; E próximo de zero,
se responde a qualquer troca de rótulo geográfico.

## Secundárias, registradas como tais

- D₂ = |Δ| do par de teste − |Δ| do gêmeo intrarregional, mesmo teste e correção.
- |Δ| dos gêmeos intrarregionais contra o grupo de referência, descritivo.

**Limite de resolução:** com cinco frases, o menor p exato é 0,031, e
`controle_explicito` não sobrevive à correção por construção.

Uso:
    python analise_intrarregional.py
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

from analise_moldura import ic_media, p_sinais_exato
from teste_construcional import holm, p_permutacao
from teste_explicito import (CALIBRACAO, EXCLUIDOS_DA_CALIBRACAO, TESTE_DO_CONTROLE,
                             TESTE_DO_INTRA)

SAIDA = Path(__file__).resolve().parent / "resultados"
PARES_MEDIDOS = SAIDA / "dados" / "explicito_pares.json"
TABELA = SAIDA / "tabelas" / "intrarregional_tabelas.md"


def tabela_pareada(add, titulo: str, series: dict[str, list[float]]) -> None:
    linhas = []
    for teste, ds in series.items():
        linhas.append((teste, len(ds), statistics.mean(ds), ic_media(ds),
                       sum(1 for d in ds if d > 0), p_sinais_exato(ds)))
    ajustados = holm({t: p for t, _, _, _, _, p in linhas})
    add(f"## {titulo}")
    add("")
    add("| condição de teste | frases | média | IC 95% | > 0 | p exato | p Holm |")
    add("|---|---|---|---|---|---|---|")
    for teste, n, media, ic, pos, p in linhas:
        add(f"| `{teste}` | {n} | {media:+.4f} | {ic[0]:+.4f}–{ic[1]:+.4f} | "
            f"{pos}/{n} | {p:.4f} | {ajustados[teste]:.4f} |")
    add("")


def main() -> None:
    pares = json.loads(PARES_MEDIDOS.read_text(encoding="utf-8"))
    por_chave = {(p["condicao"], p["par"]): p for p in pares}
    inter_de = {teste: controle for controle, teste in TESTE_DO_CONTROLE.items()}

    e_series, d2_series, detalhe = {}, {}, []
    for intra, teste in TESTE_DO_INTRA.items():
        inter = inter_de[teste]
        es, d2s, i = [], [], 0
        while (teste, i) in por_chave:
            t, g1, g2 = por_chave[(teste, i)], por_chave.get((inter, i)), por_chave.get((intra, i))
            if g1 is None or g2 is None:
                raise SystemExit(f"{teste}-{i:02d}: gêmeo sem medição; rode teste_explicito.py")
            e, d2 = g1["mediana"] - g2["mediana"], t["mediana"] - g2["mediana"]
            es.append(e)
            d2s.append(d2)
            detalhe.append((teste, i, t["a"], g1["a"], g2["a"], t["mediana"],
                            g1["mediana"], g2["mediana"], e))
            i += 1
        e_series[teste], d2_series[teste] = es, d2s

    L = []
    add = L.append
    add("# Controle intrarregional da menção explícita")
    add("")
    add("Gerado por `experimentos/analise_intrarregional.py`. Desenho e predições em")
    add("`docs/pendencias.md` 2.11. Teste unilateral por permutação exata de sinais no")
    add("nível da frase; Holm sobre as quatro condições.")
    add("")
    tabela_pareada(add, "Resultado registrado — E = |Δ| inter-regional − |Δ| intrarregional",
                   e_series)
    tabela_pareada(add, "Secundário registrado — D₂ = |Δ| teste − |Δ| intrarregional",
                   d2_series)

    add("## Por frase")
    add("")
    add("| condição | # | teste | gêmeo inter-regional | gêmeo intrarregional | "
        "\\|Δ\\| teste | \\|Δ\\| inter | \\|Δ\\| intra | E |")
    add("|---|---|---|---|---|---|---|---|---|")
    for teste, i, ta, g1a, g2a, mt, m1, m2, e in detalhe:
        add(f"| `{teste}` | {i} | {ta} | {g1a} | {g2a} | {mt:.4f} | {m1:.4f} | {m2:.4f} | {e:+.4f} |")
    add("")

    calib = [p for p in pares if p["condicao"] in CALIBRACAO and p.get("residuo") is not None
             and (p["condicao"], p["par"]) not in EXCLUIDOS_DA_CALIBRACAO]
    ref = [p["mediana"] for p in calib]
    add("## Secundário registrado, descritivo: gêmeos intrarregionais contra o grupo de referência")
    add("")
    add(f"Grupo de referência: {len(ref)} pares, mediana de |Δ| {statistics.median(ref):.4f}. "
        "Permutação unilateral de rótulos de par, sobre |Δ|.")
    add("")
    add("| gêmeos intrarregionais de | frases | mediana \\|Δ\\| | média \\|Δ\\| | p |")
    add("|---|---|---|---|---|")
    for intra, teste in TESTE_DO_INTRA.items():
        v = [p["mediana"] for p in pares if p["condicao"] == intra]
        add(f"| `{teste}` | {len(v)} | {statistics.median(v):.4f} | {statistics.mean(v):.4f} | "
            f"{p_permutacao(v, ref):.4f} |")
    add("")

    texto = chr(10).join(L)
    TABELA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
