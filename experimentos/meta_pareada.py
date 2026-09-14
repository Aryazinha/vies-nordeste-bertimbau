"""
meta_pareada.py — meta de frases por condição no desenho pareado (`docs/pendencias.md` 2.11, parte b)

## Por que uma segunda meta

`meta_pares_minimos.py` dimensiona a análise de **direção**: escore de viés,
condição de teste contra grupo de referência, duas amostras independentes. A
pergunta que decide a interpretação da menção explícita passou a ser a de
**especificidade** (`docs/achados_para_o_artigo.md` 1.17): D = |Δ| do par de teste
− |Δ| do gêmeo na mesma frase, uma amostra pareada por frase.

O pareamento remove a variância de moldura, de modo que a dispersão relevante é a
de D, e não a de |Δ|. Ela é estimada nos 29 gêmeos de moldura já medidos.

## A conta

Teste unilateral de média de D > 0, com poder de 80%. O tamanho é dado pela
aproximação normal com a correção de Guenther para a distribuição t:

    n = ((z₁₋α + z₁₋β) · σ / δ)² + z₁₋α² / 2

Com correção de Holm sobre quatro condições, dimensiona-se com α/4 — o limiar
enfrentado pelo menor valor-p da família, e portanto conservador. O teste
efetivamente empregado é de permutação exata de sinais; a aproximação serve ao
dimensionamento.

**O efeito-alvo δ é decisão da equipe**, como foi o 0,08 da meta de direção. Este
script tabela as opções e não escolhe.

Uso:
    python meta_pareada.py
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

from teste_explicito import TESTE_DO_CONTROLE

SAIDA = Path(__file__).resolve().parent / "resultados"
PARES_MEDIDOS = SAIDA / "dados" / "explicito_pares.json"
TABELA = SAIDA / "tabelas" / "meta_pareada.md"

PODER = 0.80
ALFA = 0.05
N_CONDICOES = 4
EFEITOS = (0.03, 0.05, 0.08, 0.10)
FRASES = (8, 16, 24, 40)

Z = statistics.NormalDist()


def frases_necessarias(delta: float, sigma: float, alfa: float) -> int:
    za, zb = Z.inv_cdf(1 - alfa), Z.inv_cdf(PODER)
    return math.ceil(((za + zb) * sigma / delta) ** 2 + za ** 2 / 2)


def menor_efeito(n: int, sigma: float, alfa: float) -> float:
    za, zb = Z.inv_cdf(1 - alfa), Z.inv_cdf(PODER)
    return (za + zb) * sigma / math.sqrt(max(n - za ** 2 / 2, 1))


def main() -> None:
    pares = json.loads(PARES_MEDIDOS.read_text(encoding="utf-8"))
    por_chave = {(p["condicao"], p["par"]): p["mediana"] for p in pares}

    ds_por_condicao = {}
    for controle, teste in TESTE_DO_CONTROLE.items():
        ds, i = [], 0
        while (teste, i) in por_chave:
            ds.append(por_chave[(teste, i)] - por_chave[(controle, i)])
            i += 1
        ds_por_condicao[teste] = ds

    # Desvio-padrão combinado, ponderado por graus de liberdade.
    soma, gl = 0.0, 0
    for ds in ds_por_condicao.values():
        soma += statistics.variance(ds) * (len(ds) - 1)
        gl += len(ds) - 1
    sigma_comb = math.sqrt(soma / gl)
    alfa_holm = ALFA / N_CONDICOES

    L = []
    add = L.append
    add("# Meta de frases por condição no desenho pareado")
    add("")
    add("Gerado por `experimentos/meta_pareada.py`. Estatística: D = |Δ| teste − |Δ| gêmeo,")
    add("pareada por frase. Poder de 80%, teste unilateral. Decisão do efeito-alvo pendente")
    add("da equipe (`docs/pendencias.md` 2.11, parte b).")
    add("")
    add("## Dispersão de D nos gêmeos de moldura")
    add("")
    add("| condição | frases | D médio | desvio-padrão |")
    add("|---|---|---|---|")
    for teste, ds in ds_por_condicao.items():
        add(f"| `{teste}` | {len(ds)} | {statistics.mean(ds):+.4f} | {statistics.stdev(ds):.4f} |")
    add(f"| **combinado** | {sum(len(d) for d in ds_por_condicao.values())} | — | **{sigma_comb:.4f}** |")
    add("")
    add("A dispersão é heterogênea: o gentílico tem desvio-padrão várias vezes maior que o")
    add("topônimo. Dimensionar pelo combinado subestima o necessário no gentílico; a última")
    add("coluna da tabela seguinte dimensiona pelo maior desvio-padrão observado.")
    add("")

    sigma_max = max(statistics.stdev(ds) for ds in ds_por_condicao.values())
    add("## Frases necessárias por condição")
    add("")
    add(f"| efeito específico a excluir (δ) | α = 0,05, σ combinado | Holm (α/{N_CONDICOES}), σ combinado | "
        f"Holm, σ máximo ({sigma_max:.3f}) |")
    add("|---|---|---|---|")
    for delta in EFEITOS:
        add(f"| {delta:.2f} | {frases_necessarias(delta, sigma_comb, ALFA)} | "
            f"{frases_necessarias(delta, sigma_comb, alfa_holm)} | "
            f"{frases_necessarias(delta, sigma_max, alfa_holm)} |")
    add("")

    add("## Menor efeito específico detectável, por número de frases")
    add("")
    add("| frases por condição | Holm, σ combinado | Holm, σ máximo |")
    add("|---|---|---|")
    for n in FRASES:
        marca = " (atual)" if n == 8 else ""
        add(f"| {n}{marca} | {menor_efeito(n, sigma_comb, alfa_holm):.3f} | "
            f"{menor_efeito(n, sigma_max, alfa_holm):.3f} |")
    add("")
    add("## Custo implicado")
    add("")
    add("Cada frase de teste nasce com um gêmeo inter-regional e, se o controle intrarregional")
    add("se mostrar informativo, também com um intrarregional: duas ou três medições de par por")
    add("frase, a 28 medições cada.")
    add("")

    texto = chr(10).join(L)
    TABELA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
