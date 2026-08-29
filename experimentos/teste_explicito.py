"""
teste_explicito.py — passo 5.4 do `docs/roadmap.md`

O passo 5.1 fechou quatro famílias de sinalização dialetal **implícita** sem
encontrar resposta no modelo, e deixou uma única condição com resíduo
consistente acima da reta da frequência: a **menção explícita** à região, com os
cinco pares acima da reta e p = 0,026 — que não sobrevive à correção de Holm com
apenas cinco pares (`experimentos/resultados/relatorios/construcional.md`, seção 4).

Aqueles cinco pares sugeriram um padrão interno que este teste existe para
confirmar ou desmentir: **os dois maiores resíduos eram os que nomeavam a região
como categoria** — "do Nordeste" contra "do Sudeste", "um nordestino" contra "um
paulista" —, enquanto os três que nomeavam estados ficavam próximos de zero.

## A variável de desenho

Se o padrão for real, o efeito deve decrescer à medida que o rótulo se torna mais
específico e mais toponímico. Três condições, oito pares cada, ordenadas por
granularidade:

- **`explicito_regiao`** — macrorregião e seu gentílico: *Nordeste*, *nordestino*.
- **`explicito_gentilico`** — gentílico de estado: *pernambucano*, *baiano*,
  *cearense*, *paraibano*.
- **`explicito_toponimo`** — nome de estado e de capital: *Ceará*, *Pernambuco*,
  *Recife*, *Fortaleza*, *Salvador*.

A predição é ordinal, e é o que torna o teste informativo mesmo com poucos pares:
resíduo decrescente de `explicito_regiao` para `explicito_toponimo`. Um efeito
uniforme nas três condições falsearia a leitura de "categoria regional" e
apontaria para associação com topônimo em geral.

## Forma dos enunciados

Todos os pares são de **autoidentificação em primeira ou terceira pessoa** — "Eu
sou do Nordeste", "Meu pai é baiano" —, e não de menção avulsa. É o análogo
explícito do guise dialetal: o enunciado revela a procedência de quem fala, e a
moldura pergunta que atributo se assinala a essa pessoa.

Os cinco pares originais de `controle_explicito` permanecem no conjunto, medidos
anteriormente e não repetidos aqui, e nenhum enunciado novo os duplica.

## Frequência

A crítica que encerrou o bloco lexical aplica-se aqui com força: *São Paulo* é
cerca de dez vezes mais frequente que *Paraíba*, e ler diferença de escore como
associação regional sem descontar isso mede raridade. O delineamento é o mesmo do
passo 5.1 — calibrar a reta da frequência sobre pares não regionais e ler o
resíduo —, e a seleção dos pares privilegiou deliberadamente contrastes de razão
baixa, que a condição original não tinha: *nordestino* contra *sulista* é 1,9×, e
*pernambucano* contra *paulistano*, 1,1×.

**Uma assimetria do próprio português, que merece registro.** Não há gentílico
corrente para o Sudeste: *sudestino* tem frequência de 0,015 por milhão, contra
4,27 de *nordestino* — razão de 285 vezes. O contraste simétrico é impossível de
construir, e os controles empregados são gentílicos de outras macrorregiões
(*sulista*) ou de estados do Sudeste (*mineiro*, *carioca*, *paulista*).

Uso:
    python teste_explicito.py
"""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from teste_construcional import (
    CONDICOES_NOVAS as CONDICOES_5_1,
    ajustar_reta,
    holm,
    ic_bootstrap,
    medir,
    p_permutacao,
    razao_frequencia,
)
from teste_sensibilidade import CONDICOES as CONDICOES_BASE

SAIDA = Path(__file__).resolve().parent / "resultados"
# Quatro destinos, e a separação não é estética: `relatorios/` guarda texto
# escrito à mão que script algum pode sobrescrever, `tabelas/` guarda saída de
# máquina regerável, `dados/` guarda medição bruta e `historico/` guarda o que
# foi superado. Misturá-los já fez um script apagar uma análise interpretada.
TABELAS = SAIDA / "tabelas"
DADOS = SAIDA / "dados"
for _d in (TABELAS, DADOS):
    _d.mkdir(parents=True, exist_ok=True)
BRUTO_ANTERIOR = DADOS / "construcional_bruto.json"
BRUTO = DADOS / "explicito_bruto.json"

# --------------------------------------------------------------------------
# Nível 1 — macrorregião e gentílico de macrorregião
# --------------------------------------------------------------------------
EXPLICITO_REGIAO: list[tuple[str, str]] = [
    ("Eu sou do Nordeste.", "Eu sou do Sudeste."),
    ("Minha família é toda do Nordeste.", "Minha família é toda do Sudeste."),
    ("Vim do Nordeste faz dez anos.", "Vim do Sudeste faz dez anos."),
    ("Aqui no Nordeste é assim.", "Aqui no Sudeste é assim."),
    ("Sou nordestino, nascido e criado.", "Sou sulista, nascido e criado."),
    ("Sou nordestino e tenho orgulho.", "Sou mineiro e tenho orgulho."),
    ("Todo nordestino sabe disso.", "Todo gaúcho sabe disso."),
    ("Ele é nordestino como eu.", "Ele é carioca como eu."),
]

# --------------------------------------------------------------------------
# Nível 2 — gentílico de estado
# --------------------------------------------------------------------------
EXPLICITO_GENTILICO: list[tuple[str, str]] = [
    ("Sou pernambucano, nascido e criado.", "Sou paulistano, nascido e criado."),
    ("Sou paraibano, para você saber.", "Sou paulistano, para você saber."),
    ("Meu pai é baiano.", "Meu pai é carioca."),
    ("Sou baiano, e minha família também.", "Sou fluminense, e minha família também."),
    ("Sou cearense, moro aqui faz tempo.", "Sou carioca, moro aqui faz tempo."),
    ("Todo cearense conhece essa história.", "Todo paulista conhece essa história."),
    ("Ele é paraibano igual a mim.", "Ele é carioca igual a mim."),
    ("Aqui em casa é tudo pernambucano.", "Aqui em casa é tudo paulista."),
]

# --------------------------------------------------------------------------
# Nível 3 — nome de estado e de capital
# --------------------------------------------------------------------------
EXPLICITO_TOPONIMO: list[tuple[str, str]] = [
    ("Eu sou do Ceará.", "Eu sou do Rio."),
    ("Eu sou de Pernambuco.", "Eu sou de São Paulo."),
    ("Passei a vida toda na Bahia.", "Passei a vida toda no Rio."),
    ("Moro em Recife desde criança.", "Moro em Santos desde criança."),
    ("Moro em Fortaleza desde criança.", "Moro em Niterói desde criança."),
    ("Nasci em Salvador.", "Nasci em Campinas."),
    ("Trabalhei muitos anos em Recife.", "Trabalhei muitos anos em Niterói."),
    ("Minha mãe nasceu em João Pessoa.", "Minha mãe nasceu em Niterói."),
]

# --------------------------------------------------------------------------
# Reforço da calibração na faixa de 20× a 50×, onde caem os pares toponímicos e
# onde o conjunto anterior tinha poucos pontos. Sem marcação regional.
# --------------------------------------------------------------------------
CALIBRACAO_EXTRA: list[tuple[str, str]] = [
    ("Comprei leite na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei açúcar na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei arroz na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei pão na feira hoje.", "Comprei manteiga na feira hoje."),
]

CONDICOES_NOVAS = {
    "explicito_regiao": EXPLICITO_REGIAO,
    "explicito_gentilico": EXPLICITO_GENTILICO,
    "explicito_toponimo": EXPLICITO_TOPONIMO,
    "calibracao_extra": CALIBRACAO_EXTRA,
}

CALIBRACAO = ("controle_neutro", "controle_raridade", "controle_frequencia",
              "calibracao_extra")
TESTE = ("dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
         "controle_explicito", "explicito_regiao", "explicito_gentilico",
         "explicito_toponimo", "controle_conteudo")

ORDEM = ("controle_neutro", "controle_frequencia", "calibracao_extra",
         "controle_raridade", "dialeto_A", "dialeto_D", "dialeto_C", "dialeto_B",
         "explicito_toponimo", "explicito_gentilico", "controle_explicito",
         "explicito_regiao", "controle_conteudo")

# Rótulo legível para o relatório
NOMES = {
    "explicito_regiao": "menção explícita — macrorregião",
    "explicito_gentilico": "menção explícita — gentílico de estado",
    "explicito_toponimo": "menção explícita — topônimo",
    "controle_explicito": "menção explícita — conjunto original",
}


def main() -> None:
    if BRUTO.exists():
        bruto = json.loads(BRUTO.read_text(encoding="utf-8"))
    else:
        bruto = json.loads(BRUTO_ANTERIOR.read_text(encoding="utf-8"))

    ja_medidas = {r["condicao"] for r in bruto}
    faltantes = {c: p for c, p in CONDICOES_NOVAS.items() if c not in ja_medidas}
    if faltantes:
        bruto += medir(faltantes)
        BRUTO.write_text(json.dumps(bruto, ensure_ascii=False), encoding="utf-8")
    else:
        print("medições já em disco; apenas reanalisando" + chr(10))

    todas = dict(CONDICOES_BASE)
    todas.update(CONDICOES_5_1)
    todas.update(CONDICOES_NOVAS)

    # ---- agregação por par -------------------------------------------------
    por_par = defaultdict(list)
    for r in bruto:
        por_par[(r["condicao"], r["par"])].append(abs(r["d_pll"]))

    pares = []
    for (condicao, i), valores in sorted(por_par.items()):
        lado_a, lado_b = todas[condicao][i]
        rz = razao_frequencia(lado_a, lado_b)
        pares.append({
            "condicao": condicao, "par": i, "a": lado_a, "b": lado_b,
            "n": len(valores), "mediana": statistics.median(valores),
            "razao": rz[0] if rz else None,
        })

    piso = statistics.median(
        [p["mediana"] for p in pares if p["condicao"] == "controle_neutro"])

    # ---- reta da frequência ------------------------------------------------
    calib = [p for p in pares if p["condicao"] in CALIBRACAO and p["razao"]]
    xs = [math.log10(p["razao"]) for p in calib]
    ys = [p["mediana"] for p in calib]
    a, b, r2, p_incl = ajustar_reta(xs, ys)

    for p in pares:
        if p["razao"]:
            p["previsto"] = a + b * math.log10(p["razao"])
            p["residuo"] = p["mediana"] - p["previsto"]
        else:
            p["previsto"] = p["residuo"] = None

    res_calib = [p["residuo"] for p in calib]
    dp_calib = statistics.pstdev(res_calib)

    # ---- por condição ------------------------------------------------------
    resumo = []
    for cond in ORDEM:
        do_cond = [p for p in pares if p["condicao"] == cond]
        if not do_cond:
            continue
        medianas = [p["mediana"] for p in do_cond]
        med = statistics.median(medianas)
        lo, hi = ic_bootstrap(medianas)
        com_razao = [p for p in do_cond if p["residuo"] is not None]
        linha = {
            "condicao": cond, "n_pares": len(do_cond), "mediana": med,
            "ic": (lo, hi), "sobre_piso": med / piso,
            "razao_mediana": (statistics.median([p["razao"] for p in com_razao])
                              if com_razao else None),
            "residuo": (statistics.mean([p["residuo"] for p in com_razao])
                        if com_razao else None),
            "positivos": sum(1 for p in com_razao if p["residuo"] > 0),
            "com_razao": len(com_razao), "p": None,
        }
        if cond in TESTE and com_razao:
            linha["p"] = p_permutacao([p["residuo"] for p in com_razao], res_calib)
        resumo.append(linha)

    ajustados = holm({r["condicao"]: r["p"] for r in resumo if r["p"] is not None})
    for r in resumo:
        r["p_holm"] = ajustados.get(r["condicao"])

    # ---- relatório ---------------------------------------------------------
    L = []
    add = L.append
    add("# Menção explícita à região, por granularidade do rótulo")
    add("")
    add("Gerado por `experimentos/teste_explicito.py`. Valores em |Δ PLL| por token,")
    add("com o alvo mascarado por inteiro. A unidade de replicação é o par.")
    add("")
    add(f"**Reta da frequência**, ajustada sobre {len(calib)} pares não regionais:")
    add(f"|Δ| = {a:.4f} + {b:.4f} · log10(razão), R² = {r2:.3f}, p = {p_incl:.4f} para a inclinação.")
    add(f"Desvio-padrão dos resíduos de calibração: {dp_calib:.4f}.")
    add("")
    add("| condição | pares | mediana \\|Δ\\| | IC 95% | sobre o piso | razão med. | resíduo médio | acima da reta | p | p Holm |")
    add("|---|---|---|---|---|---|---|---|---|---|")
    for r in resumo:
        rz = f"{r['razao_mediana']:.1f}×" if r["razao_mediana"] else "—"
        rs = f"{r['residuo']:+.4f}" if r["residuo"] is not None else "—"
        sg = f"{r['positivos']}/{r['com_razao']}" if r["com_razao"] else "—"
        pv = f"{r['p']:.4f}" if r["p"] is not None else "—"
        ph = f"{r['p_holm']:.4f}" if r.get("p_holm") is not None else "—"
        add(f"| `{r['condicao']}` | {r['n_pares']} | {r['mediana']:.4f} | "
            f"{r['ic'][0]:.4f}–{r['ic'][1]:.4f} | {r['sobre_piso']:.2f}× | {rz} | "
            f"{rs} | {sg} | {pv} | {ph} |")
    add("")

    for cond in ("explicito_regiao", "explicito_gentilico", "explicito_toponimo"):
        add(f"## {NOMES[cond]}")
        add("")
        add("| enunciado nordestino | controle | razão | \\|Δ\\| | previsto | resíduo |")
        add("|---|---|---|---|---|---|")
        for p in [q for q in pares if q["condicao"] == cond]:
            rz = f"{p['razao']:.1f}×" if p["razao"] else "—"
            pr = f"{p['previsto']:.4f}" if p["previsto"] is not None else "—"
            rs = f"{p['residuo']:+.4f}" if p["residuo"] is not None else "—"
            add(f"| {p['a']} | {p['b']} | {rz} | {p['mediana']:.4f} | {pr} | {rs} |")
        add("")

    # ----------------------------------------------------------------------
    # Reagrupamento exploratório: pessoa contra lugar
    #
    # DECLARADO COMO POSTERIOR AOS DADOS. A predição registrada no cabeçalho
    # deste arquivo era ordinal por granularidade — macrorregião acima de
    # gentílico, gentílico acima de topônimo —, e não foi o que se observou: o
    # gentílico de estado supera a macrorregião. A inspeção por par mostra que o
    # corte não é de granularidade, e sim de **categoria do rótulo**: enunciados
    # que nomeiam uma pessoa (*nordestino*, *baiano*, *cearense*) contra
    # enunciados que nomeiam um lugar (*Nordeste*, *Bahia*, *Recife*).
    #
    # O corte atravessa a condição `explicito_regiao`, cujos quatro primeiros
    # pares nomeiam lugar e cujos quatro últimos nomeiam pessoa — razão pela qual
    # o reagrupamento não podia ser lido na tabela por condição.
    #
    # O valor-p abaixo **não tem o mesmo estatuto** dos da tabela anterior: a
    # hipótese foi formulada depois de ver os dados. Vale como magnitude de
    # efeito a testar em conjunto novo, não como teste confirmatório.
    # ----------------------------------------------------------------------
    PESSOA = {"nordestino", "pernambucano", "paraibano", "baiano", "cearense"}
    LUGAR = {"nordeste", "ceará", "pernambuco", "bahia", "recife",
             "fortaleza", "salvador", "joão"}

    def categoria(par: dict) -> str | None:
        if par["condicao"] not in ("explicito_regiao", "explicito_gentilico",
                                   "explicito_toponimo"):
            return None
        rz = razao_frequencia(par["a"], par["b"])
        alvo = set(rz[1]) if rz else set()
        if alvo & PESSOA:
            return "pessoa"
        if alvo & LUGAR:
            return "lugar"
        return None

    grupos = defaultdict(list)
    for p in pares:
        cat = categoria(p)
        if cat and p["residuo"] is not None:
            grupos[cat].append(p["residuo"])

    add("## Reagrupamento exploratório: rótulo de pessoa contra rótulo de lugar")
    add("")
    add("**Posterior aos dados.** A predição registrada era ordinal por")
    add("granularidade e não se confirmou nessa forma. Os valores abaixo indicam")
    add("magnitude a testar em conjunto novo, e não constituem teste confirmatório.")
    add("")
    add("| agrupamento | pares | resíduo médio | acima da reta | p (exploratório) |")
    add("|---|---|---|---|---|")
    for cat in ("pessoa", "lugar"):
        v = grupos[cat]
        pv = p_permutacao(v, res_calib)
        add(f"| rótulo de {cat} | {len(v)} | {statistics.mean(v):+.4f} | "
            f"{sum(1 for x in v if x > 0)}/{len(v)} | {pv:.4f} |")
    add("")
    p_entre = p_permutacao(grupos["pessoa"], grupos["lugar"])
    add(f"Diferença entre os dois agrupamentos: p = {p_entre:.4f}, por permutação")
    add("direta de rótulos de par entre eles.")
    add("")

    texto = chr(10).join(L)
    # Saída de máquina, regerável. O relatório interpretado é `explicito.md`,
    # escrito à mão sobre estes números, e o script não o toca.
    (TABELAS / "explicito_tabelas.md").write_text(texto, encoding="utf-8")
    (DADOS / "explicito_pares.json").write_text(
        json.dumps(pares, ensure_ascii=False, indent=1), encoding="utf-8")
    print(chr(10) + texto)


if __name__ == "__main__":
    main()
