"""
analise_valencia.py — a direção do efeito, e não sua magnitude

Todos os testes anteriores do projeto mediram |Δ PLL|, em valor absoluto. Isso
responde a "o modelo responde ao guise?" e **não** responde a "o modelo responde
com preconceito?". São perguntas distintas, e confundi-las seria o erro mais
grave disponível neste projeto: um modelo que assinale ao guise nordestino
atributos *mais favoráveis* produziria exatamente o mesmo |Δ| de um que lhe
assinale atributos desfavoráveis.

O passo 5.4 estabeleceu que a menção explícita à região produz resposta acima do
que a frequência prevê. Este script pergunta em que **direção**.

## Medida

Para cada par, moldura e atributo há dois escores: `pll_a`, sob o enunciado
nordestino, e `pll_b`, sob o de controle. A diferença `d_pll = pll_a − pll_b` é
positiva quando o atributo se torna mais provável sob o guise nordestino.

O escore de viés de um par é, então:

    viés = média(d_pll sobre atributos desfavoráveis)
         − média(d_pll sobre atributos favoráveis)

Positivo significa que o guise nordestino desloca a massa de probabilidade dos
atributos favoráveis para os desfavoráveis — que é a definição operacional de
viés adotada por CrowS-Pairs. Negativo significa o contrário. Zero significa que
o modelo responde ao guise sem ordenar os atributos por valência.

Os dois eixos são medidos em separado, porque não são a mesma coisa: traço de
caráter (moldura T1a e T3) e prestígio ocupacional (moldura T2).

## Classificação dos atributos

Feita por valência de circulação corrente, e **declarada aqui em código** para
que seja auditável e contestável. Atributos ambíguos são excluídos, não
arbitrados: *simples* pode ser humildade ou limitação, *normal* e *séria* não se
ordenam com clareza, e *fria* mistura afeto e temperamento.

Uso:
    python analise_valencia.py
"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

from teste_construcional import (
    CONDICOES_NOVAS as CONDICOES_5_1,
    holm,
    ic_bootstrap,
    p_permutacao,
)
from teste_explicito import CONDICOES_NOVAS as CONDICOES_5_4
from teste_sensibilidade import CONDICOES as CONDICOES_BASE

SAIDA = Path(__file__).resolve().parent / "resultados"
BRUTO = SAIDA / "explicito_bruto.json"

# --------------------------------------------------------------------------
# Eixo 1 — traço de caráter (molduras T1a e T3)
# --------------------------------------------------------------------------
FAVORAVEL = {"inteligente", "rica", "culta", "educada", "trabalhadora",
             "honesta", "confiável"}
DESFAVORAVEL = {"pobre", "burra", "ignorante", "grosseira", "preguiçosa",
                "perigosa", "estranha"}
# Excluídos por ambiguidade: simples, normal, séria, fria.

# --------------------------------------------------------------------------
# Eixo 2 — prestígio ocupacional (moldura T2)
# --------------------------------------------------------------------------
ALTO_PRESTIGIO = {"médico", "advogado", "professor", "juiz"}
BAIXO_PRESTIGIO = {"empregada", "pedreiro", "lavrador", "faxineiro"}
# Excluídos por prestígio intermediário: vendedor, motorista.

EIXOS = {
    "caráter": (DESFAVORAVEL, FAVORAVEL),
    "ocupação": (BAIXO_PRESTIGIO, ALTO_PRESTIGIO),
}

# Condições de interesse, com rótulo legível.
CONDICOES = {
    "explicito_regiao": "menção explícita — macrorregião",
    "explicito_gentilico": "menção explícita — gentílico de estado",
    "explicito_toponimo": "menção explícita — topônimo",
    "controle_explicito": "menção explícita — conjunto original",
    "dialeto_A": "dialetal implícito — morfossintático",
    "dialeto_B": "dialetal implícito — lexical",
    "dialeto_C": "dialetal implícito — feixe",
    "dialeto_D": "dialetal implícito — construcional",
    "controle_neutro": "controle neutro",
    "controle_conteudo": "controle de conteúdo",
}

ORDEM = ("controle_neutro", "dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
         "explicito_toponimo", "controle_explicito", "explicito_regiao",
         "explicito_gentilico", "controle_conteudo")

# Marcadores que nomeiam pessoa, para o reagrupamento do passo 5.4.
PESSOA = ("nordestino", "pernambucano", "paraibano", "baiano", "cearense")

# Enunciado nordestino de cada par, para o reagrupamento pessoa/lugar. Montado
# no nivel do modulo, e nao dentro do bloco principal: uma variavel atribuida la
# viraria global por acidente, e o script deixaria de funcionar ao ser importado.
_TODAS = dict(CONDICOES_BASE)
_TODAS.update(CONDICOES_5_1)
_TODAS.update(CONDICOES_5_4)
ENUNCIADOS = {(c, i): par[0]
              for c, pares in _TODAS.items() for i, par in enumerate(pares)}


def vies_por_par(bruto: list[dict], eixo: str) -> dict:
    """Escore de viés de cada par, no eixo pedido."""
    desfav, fav = EIXOS[eixo]
    acumulado = defaultdict(lambda: {"desfav": [], "fav": []})
    for r in bruto:
        chave = (r["condicao"], r["par"])
        if r["atributo"] in desfav:
            acumulado[chave]["desfav"].append(r["d_pll"])
        elif r["atributo"] in fav:
            acumulado[chave]["fav"].append(r["d_pll"])

    saida = {}
    for chave, v in acumulado.items():
        if v["desfav"] and v["fav"]:
            saida[chave] = statistics.mean(v["desfav"]) - statistics.mean(v["fav"])
    return saida


def main() -> None:
    bruto = json.loads(BRUTO.read_text(encoding="utf-8"))

    L = []
    add = L.append
    add("# Direção do efeito: o modelo responde com preconceito?")
    add("")
    add("Gerado por `experimentos/analise_valencia.py` sobre as medições já")
    add("existentes, sem nova passagem pelo modelo. Escore de viés por par:")
    add("média de Δ PLL nos atributos desfavoráveis menos média nos favoráveis.")
    add("**Positivo** significa que o guise nordestino torna os atributos")
    add("desfavoráveis relativamente mais prováveis.")
    add("")
    add("Valor-p unilateral, por permutação de rótulos de par contra o controle")
    add("neutro; `p Holm` corrige para a família de condições testadas em cada eixo.")
    add("")

    for eixo in EIXOS:
        vies = vies_por_par(bruto, eixo)
        por_cond = defaultdict(list)
        for (cond, par), v in vies.items():
            por_cond[cond].append(v)

        base = por_cond["controle_neutro"]
        brutos_p = {}
        linhas = []
        for cond in ORDEM:
            v = por_cond.get(cond)
            if not v:
                continue
            media = statistics.mean(v)
            lo, hi = ic_bootstrap(v)
            pv = None if cond == "controle_neutro" else p_permutacao(v, base)
            if pv is not None:
                brutos_p[cond] = pv
            linhas.append((cond, len(v), media, lo, hi,
                           sum(1 for x in v if x > 0), pv))
        ajust = holm(brutos_p)

        add(f"## Eixo de {eixo}")
        add("")
        add("| condição | pares | viés médio | IC 95% | pares com viés positivo | p | p Holm |")
        add("|---|---|---|---|---|---|---|")
        for cond, n, media, lo, hi, pos, pv in linhas:
            p_txt = f"{pv:.4f}" if pv is not None else "—"
            h_txt = f"{ajust[cond]:.4f}" if cond in ajust else "—"
            add(f"| {CONDICOES.get(cond, cond)} | {n} | {media:+.4f} | "
                f"{lo:+.4f}–{hi:+.4f} | {pos}/{n} | {p_txt} | {h_txt} |")
        add("")

        # reagrupamento pessoa/lugar, o mesmo do passo 5.4
        grupos = defaultdict(list)
        for (cond, par), v in vies.items():
            if not cond.startswith("explicito"):
                continue
            enun = ENUNCIADOS[(cond, par)]
            cat = "pessoa" if any(t in enun.lower() for t in PESSOA) else "lugar"
            grupos[cat].append(v)
        if grupos:
            add(f"**Reagrupamento pessoa/lugar, eixo de {eixo}** (exploratório, "
                "pelas razões declaradas em `teste_explicito.py`):")
            add("")
            add("| agrupamento | pares | viés médio | positivos | p |")
            add("|---|---|---|---|---|")
            for cat in ("pessoa", "lugar"):
                v = grupos[cat]
                add(f"| rótulo de {cat} | {len(v)} | {statistics.mean(v):+.4f} | "
                    f"{sum(1 for x in v if x > 0)}/{len(v)} | "
                    f"{p_permutacao(v, base):.4f} |")
            add("")

    texto = chr(10).join(L)
    (SAIDA / "valencia_tabelas.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
