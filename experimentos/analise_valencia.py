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
TABELAS = SAIDA / "tabelas"          # ver nota em `teste_construcional.py`
TABELAS.mkdir(parents=True, exist_ok=True)
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

# --------------------------------------------------------------------------
# Eixo 1 restrito — controle do artefato de segmentação (passo 5.5b)
#
# O item 1.1 de `docs/achados_para_o_artigo.md` estabelece que a fragmentação em
# subtokens acompanha o eixo de prestígio no vocabulário do BERTimbau. O
# mascaramento do alvo por inteiro foi adotado para neutralizar isso, e pode não
# bastar. A verificação direta é restringir a análise a atributos de token único.
#
# **No eixo de ocupação a verificação não é executável**, e a impossibilidade é o
# próprio item 1.1 em ação: das quatro ocupações de alto prestígio, as quatro são
# de token único; das quatro de baixo, apenas *empregada* — que é também a única
# do feminino, de modo que restringir trocaria o confundidor de segmentação pelo
# de gênero. Não há do que restringir. Aquele eixo exige AUL, e não PLL.
#
# **No eixo de caráter a verificação é executável**, porque a tokenização é
# aproximadamente balanceada: três de sete favoráveis e três de sete
# desfavoráveis são de token único, com média de 1,57 contra 1,86 tokens.
# --------------------------------------------------------------------------
FAVORAVEL_1TOKEN = {"confiável", "inteligente", "rica"}
DESFAVORAVEL_1TOKEN = {"estranha", "perigosa", "pobre"}

EIXOS = {
    "caráter": (DESFAVORAVEL, FAVORAVEL),
    "caráter, restrito a token único": (DESFAVORAVEL_1TOKEN, FAVORAVEL_1TOKEN),
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
    "controle_frequencia": "controle de frequência",
    "calibracao_extra": "calibração extra",
    "controle_raridade": "controle de raridade",
    "controle_conteudo": "controle de conteúdo",
}

# --------------------------------------------------------------------------
# Grupo de referência da permutação.
#
# A primeira versão deste script empregava apenas `controle_neutro`, de cinco
# pares. Foi erro de desenho, e o sintoma foi inequívoco: o controle positivo
# apresentava as maiores magnitudes brutas das duas tabelas e ainda assim não
# sobrevivia à correção de Holm. Com cinco pares no grupo de referência a
# distribuição nula da permutação não tem resolução, e nenhuma condição pode
# atingir significância depois de corrigida para nove comparações.
#
# A referência correta são **todos** os pares não regionais já medidos, que é a
# mesma escolha feita para calibrar a reta da frequência em `teste_construcional`
# e em `teste_explicito`. São 26, e a hipótese que os qualifica é explícita e
# verificável: um par sem marcação regional não tem razão para deslocar a
# valência dos atributos, de modo que seu viés esperado é zero. O relatório
# reporta média e dispersão do grupo justamente para que essa hipótese possa ser
# conferida, e não apenas assumida.
#
# `controle_neutro` permanece como linha da tabela, agora testado contra o grupo
# do qual faz parte. Deve resultar não significativo, e é a verificação de
# sanidade do procedimento.
# --------------------------------------------------------------------------
REFERENCIA = ("controle_neutro", "controle_frequencia", "calibracao_extra",
              "controle_raridade")

ORDEM = ("controle_neutro", "controle_frequencia", "calibracao_extra",
         "controle_raridade", "dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
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
    add("Valor-p unilateral, por permutação de rótulos de par contra o grupo de")
    add("referência de pares não regionais; `p Holm` corrige para a família de")
    add("condições testadas em cada eixo. As condições que compõem o próprio grupo")
    add("de referência não são testadas, com a exceção deliberada do controle")
    add("neutro, que serve de verificação de sanidade e deve resultar não")
    add("significativo.")
    add("")

    for eixo in EIXOS:
        vies = vies_por_par(bruto, eixo)
        por_cond = defaultdict(list)
        for (cond, par), v in vies.items():
            por_cond[cond].append(v)

        base = [v for (cond, _), v in vies.items() if cond in REFERENCIA]
        brutos_p = {}
        linhas = []
        for cond in ORDEM:
            v = por_cond.get(cond)
            if not v:
                continue
            media = statistics.mean(v)
            lo, hi = ic_bootstrap(v)
            # Condições do próprio grupo de referência não entram na família de
            # testes: seriam confrontadas consigo mesmas. `controle_neutro` é a
            # exceção deliberada, como verificação de sanidade.
            testar = cond not in REFERENCIA or cond == "controle_neutro"
            pv = p_permutacao(v, base) if testar else None
            if pv is not None and cond != "controle_neutro":
                brutos_p[cond] = pv
            linhas.append((cond, len(v), media, lo, hi,
                           sum(1 for x in v if x > 0), pv))
        ajust = holm(brutos_p)

        add(f"## Eixo de {eixo}")
        add("")
        add(f"Grupo de referência: {len(base)} pares não regionais, viés médio "
            f"{statistics.mean(base):+.4f}, desvio-padrão {statistics.pstdev(base):.4f}. "
            "A proximidade da média a zero é o que autoriza usá-lo como nulo.")
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
    (TABELAS / "valencia_tabelas.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
