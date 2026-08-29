"""
teste_construcional.py — passo 5.1 do `docs/roadmap.md`

O teste de sensibilidade (`teste_sensibilidade.py`) estabeleceu dois fatos que
determinam o desenho deste:

1. O guise morfossintático não produz efeito algum — 1,00× o piso.
2. O efeito do guise lexical é reproduzido, quase par a par, por um controle de
   palavras raras não regionais. Nesta métrica, a diferença de escore entre dois
   contextos é dominada pela **frequência** das palavras que os distinguem.

Segue-se que uma comparação de medianas entre condições não decide nada: uma
condição dialetal e um controle de raridade com o mesmo perfil de frequência
produzem o mesmo número por construção. E o pareamento perfeito de frequência,
que resolveria o problema, é inalcançável para marcadores construcionais — os
melhores candidatos apresentam razão de 5 a 11 vezes, faixa em que o próprio
controle de menção explícita já produzia 2,75× o piso.

## O desenho adotado

Em vez de tentar anular a frequência por pareamento, mede-se a lei que ela
impõe e examina-se o resíduo:

- **Conjunto de calibração** — pares **não regionais**, com razões de frequência
  deliberadamente espalhadas. Sobre eles ajusta-se |Δ PLL| mediano contra log₁₀
  da razão de frequência. A reta resultante é a resposta do modelo à raridade, e
  nada mais.
- **Conjunto de teste** — os pares dialetais, incluindo a condição nova
  `dialeto_D`, de marcadores **construcionais**. Para cada um mede-se o resíduo
  contra a reta. Resíduo em torno de zero significa que o par não faz nada que a
  frequência já não explique; resíduo positivo é sinal dialetal.

A hipótese que o passo 5.1 testa é a única pista que a raridade não explicou no
teste anterior: a de que a marcação regional viável está na **construção** e não
na palavra isolada — *menino* e *rapaz* como vocativo, *massa* como avaliativo,
*lhe* como pronome de segunda pessoa. São itens de frequência atestada cuja
marca regional está no uso, o que é justamente o que uma métrica de frequência
não deveria capturar sozinha.

## Sobre a significância

O teste anterior não trazia nenhuma. Aqui a unidade de replicação é o **par**, e
não a medição: as 28 medições de um par compartilham o enunciado e não são
independentes. Todo teste opera, portanto, no nível do par — reamostragem por
conglomerado para o intervalo, e permutação de rótulos de par para o valor-p.

Uso:
    python teste_construcional.py
"""

from __future__ import annotations

import json
import math
import random
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from wordfreq import word_frequency

from metricas import Medidor
from teste_sensibilidade import ATRIBUTOS, CONDICOES, MOLDURAS

SAIDA = Path(__file__).resolve().parent / "resultados"
SAIDA.mkdir(exist_ok=True)
# Saída de máquina fica em subpasta própria. A pasta `resultados/` guarda apenas
# relatórios escritos à mão, e a separação existe porque misturá-los já levou um
# script a sobrescrever uma interpretação (`docs/pendencias.md`, seção 5-A).
TABELAS = SAIDA / "tabelas"
TABELAS.mkdir(parents=True, exist_ok=True)
BRUTO_ANTERIOR = SAIDA / "sensibilidade_bruto.json"

SEMENTE = 20260828
N_PERMUTACOES = 20000
PISO_FREQUENCIA = 1e-8          # 0,01 por milhão, para itens ausentes da fonte

# --------------------------------------------------------------------------
# Condição nova: marcadores construcionais
#
# Critério de seleção: a marca regional está no **uso** de um item de frequência
# atestada, e não na raridade do item.
#
# Procedência dos marcadores, pela convenção do projeto:
#   `lhe` de 2ª pessoa, `mais` comitativo, `tu` sem flexão — descritos na
#       literatura dialetológica; a conferência das fontes primárias está
#       registrada como pendência.
#   vocativo `menino`/`rapaz`, avaliativo `massa` — candidatos derivados do
#       adendo B de `experimentos/resultados/piloto_medicoes.md`, com
#       distribuição favorável ao Nordeste no corpus próprio e **sem** fonte
#       dialetológica.
#   clivagem `que foi que`, durativo `tá com`, `toda vida` — candidatos sem
#       fonte, a submeter ao Filtro 1.
#
# Nenhum deles está validado. A condição mede se **existe sinal a validar**.
# --------------------------------------------------------------------------
CONSTRUCIONAIS: list[tuple[str, str, str]] = [
    ("lhe acusativo de 2ª pessoa",
     "Eu lhe vi na feira ontem.", "Eu te vi na feira ontem."),
    ("lhe dativo de 2ª pessoa",
     "Amanhã eu lhe ligo, pode deixar.", "Amanhã eu te ligo, pode deixar."),
    ("comitativo com mais",
     "Ela foi mais eu até o centro.", "Ela foi comigo até o centro."),
    ("vocativo menino dirigido a adulto",
     "Menino, olha o preço disso.", "Cara, olha o preço disso."),
    ("vocativo rapaz",
     "Rapaz, eu não sabia de nada.", "Cara, eu não sabia de nada."),
    ("avaliativo massa",
     "A festa ontem foi massa.", "A festa ontem foi legal."),
    ("tu com verbo não flexionado",
     "Tu vai sair hoje à noite?", "Você vai sair hoje à noite?"),
    ("clivagem interrogativa que foi que",
     "Que foi que houve com ele?", "O que houve com ele?"),
    ("durativo tá com",
     "Tá com dois dias que não vejo ele.", "Faz dois dias que não vejo ele."),
    ("toda vida com valor de sempre",
     "Ele foi toda vida assim.", "Ele sempre foi assim."),
]

# --------------------------------------------------------------------------
# Ampliação do conjunto de calibração.
#
# Pares sem qualquer marcação regional, escolhidos para cobrir a faixa de razão
# de frequência em que os marcadores construcionais caem — de cerca de 1× a 50× —,
# que é onde o conjunto anterior era mais pobre. Os quatro últimos perturbam os
# mesmos lugares sintáticos que os pares construcionais, de modo que a reta não
# seja ajustada apenas sobre substituição de substantivo.
# --------------------------------------------------------------------------
CONTROLE_FREQUENCIA: list[tuple[str, str]] = [
    ("Comprei pão na feira hoje.", "Comprei leite na feira hoje."),
    ("Comprei arroz na feira hoje.", "Comprei sal na feira hoje."),
    ("Fechei a porta antes de sair.", "Fechei a janela antes de sair."),
    ("Comprei açúcar na feira hoje.", "Comprei farinha na feira hoje."),
    ("Comprei leite na feira hoje.", "Comprei manteiga na feira hoje."),
    ("Deixei a chave em cima do balcão.", "Deixei a chave em cima da mesa."),
    ("Comprei pão na feira hoje.", "Comprei fermento na feira hoje."),
    ("Ele foi ao mercado de manhã.", "Ele foi ao açougue de manhã."),
    ("Ela foi comigo até o centro.", "Ela foi sozinha até o centro."),
    ("Amanhã eu te ligo, pode deixar.", "Amanhã eu te escrevo, pode deixar."),
    ("Você vai sair hoje à noite?", "Você vai voltar hoje à noite?"),
    ("Ele sempre foi assim.", "Ele nunca foi assim."),
]

CONDICOES_NOVAS = {
    "dialeto_D": [(a, b) for _, a, b in CONSTRUCIONAIS],
    "controle_frequencia": CONTROLE_FREQUENCIA,
}

# Pares sem marcação regional — é sobre eles que a reta é ajustada.
CALIBRACAO = ("controle_neutro", "controle_raridade", "controle_frequencia")
# Pares em que se procura resíduo acima da reta.
#
# Inclui `controle_conteudo`, e a inclusão é deliberada: seus pares diferem por
# proposição inteira, mas a razão de frequência entre os itens que os distinguem
# é **baixa** — de 1,1× a 4,9× —, porque palavras comuns são trocadas por outras
# palavras comuns. É, portanto, um efeito grande onde a frequência prevê efeito
# pequeno, e serve de **controle positivo do método do resíduo**: se a análise
# não atribuir resíduo alto a esta condição, é a análise que está quebrada, e
# não há o que concluir sobre as demais.
TESTE = ("dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
         "controle_explicito", "controle_conteudo")

ORDEM = ("controle_neutro", "controle_frequencia", "controle_raridade",
         "dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
         "controle_explicito", "controle_conteudo")


# ==========================================================================
# Frequência
# ==========================================================================
def _palavras(frase: str) -> list[str]:
    """Palavras em minúscula, com acento preservado — a fonte distingue *moco* de *moço*."""
    return re.findall(r"[^\W\d_]+", frase.lower(), flags=re.UNICODE)


def razao_frequencia(lado_a: str, lado_b: str):
    """
    Razão de frequência entre os itens que distinguem os dois lados.

    Toma a diferença de multiconjunto em cada direção, calcula a média
    geométrica das frequências de cada lado e devolve a razão maior sobre menor.
    A média geométrica é a escolha correta porque a frequência lexical é
    aproximadamente log-normal, e é a escala em que a regressão opera.

    Dois casos de borda, tratados de modo distinto:

    - **Nenhum lado tem item exclusivo** — os dois enunciados empregam as mesmas
      palavras e diferem apenas na **ordem**, como em "fui não" contra "não fui".
      Longe de indefinido, é o pareamento de frequência perfeito, e a razão é
      1,0. Estes são os pares mais informativos do conjunto, porque neles a
      explicação por raridade está excluída por construção.
    - **Apenas um lado tem item exclusivo** — houve pura adição de palavra, e a
      razão não é definível. Devolve `None`.
    """
    ca, cb = Counter(_palavras(lado_a)), Counter(_palavras(lado_b))
    so_a, so_b = list((ca - cb).elements()), list((cb - ca).elements())
    if not so_a and not so_b:
        return 1.0, [], []
    if not so_a or not so_b:
        return None

    def media_geometrica(palavras: list[str]) -> float:
        logs = [math.log(max(word_frequency(p, "pt"), PISO_FREQUENCIA)) for p in palavras]
        return math.exp(sum(logs) / len(logs))

    fa, fb = media_geometrica(so_a), media_geometrica(so_b)
    return max(fa, fb) / min(fa, fb), so_a, so_b


# ==========================================================================
# Medição
# ==========================================================================
def medir(condicoes: dict) -> list[dict]:
    medidor = Medidor()
    print(f"dispositivo: {medidor.device}\n")
    bruto: list[dict] = []
    for condicao, pares in condicoes.items():
        print(f"{condicao} ({len(pares)} pares)")
        for i, (lado_a, lado_b) in enumerate(pares):
            for moldura_id, moldura in MOLDURAS.items():
                for atributo in ATRIBUTOS[moldura_id]:
                    try:
                        ea = medidor.escore(
                            moldura.format(enunciado=lado_a, atributo=atributo),
                            atributo, apenas_pll=True)
                        eb = medidor.escore(
                            moldura.format(enunciado=lado_b, atributo=atributo),
                            atributo, apenas_pll=True)
                    except ValueError as exc:
                        print(f"    [pulado] {atributo}: {exc}")
                        continue
                    bruto.append({
                        "condicao": condicao, "par": i, "moldura": moldura_id,
                        "atributo": atributo, "n_tokens": ea.n_tokens,
                        "pll_a": ea.pll, "pll_b": eb.pll, "d_pll": ea.pll - eb.pll,
                    })
        print(f"    {sum(1 for r in bruto if r['condicao'] == condicao)} medições")
    return bruto


# ==========================================================================
# Estatística — toda ela no nível do par
# ==========================================================================
def ajustar_reta(xs: list[float], ys: list[float]):
    """
    Mínimos quadrados de y = a + b·x. Devolve (a, b, R², p do coeficiente).

    O valor-p do coeficiente angular vem do teste t usual, e é informação
    necessária: uma reta com R² baixo pode ainda descrever inclinação real, e a
    leitura do resíduo depende de a reta significar alguma coisa.
    """
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx else 0.0
    a = my - b * mx
    sqt = sum((y - my) ** 2 for y in ys)
    sqr = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    r2 = (1 - sqr / sqt) if sqt else 0.0

    gl = n - 2
    if gl <= 0 or sxx == 0 or sqr == 0:
        return a, b, r2, float("nan")
    erro_padrao = math.sqrt((sqr / gl) / sxx)
    t = b / erro_padrao
    # Sobrevivência bicaudal da t de Student, pela função beta incompleta
    x = gl / (gl + t * t)
    p = _beta_incompleta_regularizada(gl / 2, 0.5, x)
    return a, b, r2, p


def _beta_incompleta_regularizada(a: float, b: float, x: float) -> float:
    """I_x(a, b), por fração continuada de Lentz. Evita dependência de SciPy."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln_frente = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                 + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return math.exp(ln_frente) * _fracao_continuada(a, b, x) / a
    return 1 - math.exp(ln_frente) * _fracao_continuada(b, a, 1 - x) / b


def _fracao_continuada(a: float, b: float, x: float, iteracoes: int = 300) -> float:
    minusculo, eps = 1e-300, 3e-16
    c, d = 1.0, 1 - (a + b) * x / (a + 1)
    d = 1 / (minusculo if abs(d) < minusculo else d)
    h = d
    for m in range(1, iteracoes + 1):
        m2 = 2 * m
        for num in (m * (b - m) * x / ((a + m2 - 1) * (a + m2)),
                    -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1))):
            d = 1 + num * d
            d = 1 / (minusculo if abs(d) < minusculo else d)
            c = 1 + num / (minusculo if abs(c) < minusculo else c)
            h *= d * c
            if abs(d * c - 1) < eps:
                return h
    return h


def holm(ps: dict[str, float]) -> dict[str, float]:
    """
    Correção de Holm-Bonferroni sobre a família de condições testadas.

    Seis condições são confrontadas com a mesma calibração, e relatar apenas o
    valor-p bruto de cada uma inflaria a taxa de erro da família. Holm é
    preferido a Bonferroni por ser uniformemente mais potente sem custo de
    hipótese.
    """
    ordenados = sorted(ps.items(), key=lambda kv: kv[1])
    n, saida, maximo = len(ordenados), {}, 0.0
    for i, (chave, p) in enumerate(ordenados):
        maximo = max(maximo, min(1.0, (n - i) * p))
        saida[chave] = maximo
    return saida


def ic_bootstrap(valores: list[float], n: int = 10000):
    """Intervalo de 95% da mediana, por reamostragem **de pares**."""
    rng = random.Random(SEMENTE)
    medianas = sorted(
        statistics.median(rng.choices(valores, k=len(valores))) for _ in range(n))
    return medianas[int(0.025 * n)], medianas[int(0.975 * n)]


def p_permutacao(residuos_teste: list[float], residuos_calibracao: list[float]) -> float:
    """
    Valor-p unilateral para "o resíduo médio da condição está acima do da calibração".

    Permuta os rótulos de par entre as duas amostras. Unilateral porque a
    hipótese é direcional: sinal dialetal só pode elevar o efeito acima do que a
    frequência prevê, e um resíduo negativo não constitui evidência a favor.
    """
    rng = random.Random(SEMENTE)
    observado = statistics.mean(residuos_teste) - statistics.mean(residuos_calibracao)
    conjunto = list(residuos_teste) + list(residuos_calibracao)
    k = len(residuos_teste)
    extremos = 0
    for _ in range(N_PERMUTACOES):
        rng.shuffle(conjunto)
        dif = statistics.mean(conjunto[:k]) - statistics.mean(conjunto[k:])
        if dif >= observado:
            extremos += 1
    return (extremos + 1) / (N_PERMUTACOES + 1)


# ==========================================================================
def main() -> None:
    # ---- medição, reaproveitando tudo que já está em disco -----------------
    # Idempotente por construção: mede apenas as condições ausentes do arquivo
    # bruto. Reexecutar o script depois de alterar somente a análise não
    # recarrega o modelo nem repete medição alguma.
    caminho_bruto = SAIDA / "construcional_bruto.json"
    if caminho_bruto.exists():
        bruto = json.loads(caminho_bruto.read_text(encoding="utf-8"))
    else:
        bruto = json.loads(BRUTO_ANTERIOR.read_text(encoding="utf-8"))
    ja_medidas = {r["condicao"] for r in bruto}
    faltantes = {c: p for c, p in CONDICOES_NOVAS.items() if c not in ja_medidas}
    if faltantes:
        bruto += medir(faltantes)
        caminho_bruto.write_text(json.dumps(bruto, ensure_ascii=False), encoding="utf-8")
    else:
        print("medições já em disco; apenas reanalisando" + chr(10))

    todas = dict(CONDICOES)
    todas.update(CONDICOES_NOVAS)

    # ---- agregação por par -------------------------------------------------
    por_par = defaultdict(list)
    for r in bruto:
        por_par[(r["condicao"], r["par"])].append(abs(r["d_pll"]))

    pares: list[dict] = []
    for (condicao, i), valores in sorted(por_par.items()):
        lado_a, lado_b = todas[condicao][i]
        rz = razao_frequencia(lado_a, lado_b)
        pares.append({
            "condicao": condicao, "par": i, "a": lado_a, "b": lado_b,
            "n": len(valores), "mediana": statistics.median(valores),
            "razao": rz[0] if rz else None,
            "so_a": rz[1] if rz else [], "so_b": rz[2] if rz else [],
        })


    # O piso é a mediana das medianas de par do controle neutro, e não a mediana
    # das medições. As duas diferem, e misturá-las faria o próprio controle
    # neutro aparecer como 1,25× de si mesmo. A unidade tem de ser a mesma no
    # numerador e no denominador.
    piso = statistics.median(
        [p["mediana"] for p in pares if p["condicao"] == "controle_neutro"])

    # ---- reta da frequência, ajustada só sobre pares não regionais ----------
    calib = [p for p in pares if p["condicao"] in CALIBRACAO and p["razao"]]
    xs = [math.log10(p["razao"]) for p in calib]
    ys = [p["mediana"] for p in calib]
    a, b, r2, p_inclinacao = ajustar_reta(xs, ys)

    for p in pares:
        if p["razao"]:
            p["previsto"] = a + b * math.log10(p["razao"])
            p["residuo"] = p["mediana"] - p["previsto"]
        else:
            p["previsto"] = p["residuo"] = None

    res_calib = [p["residuo"] for p in calib]

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
            "condicao": cond, "n_pares": len(do_cond),
            "mediana": med, "ic": (lo, hi), "sobre_piso": med / piso,
            "razao_mediana": (statistics.median([p["razao"] for p in com_razao])
                              if com_razao else None),
            "residuo": (statistics.mean([p["residuo"] for p in com_razao])
                        if com_razao else None),
            # Quantos pares da condição ficam acima da reta. A consistência de
            # sinal é mais informativa que a média quando os pares são poucos:
            # cinco resíduos positivos em cinco pares têm probabilidade 1/32 sob
            # a hipótese de sinal aleatório, ainda que nenhum deles seja grande.
            "positivos": sum(1 for p in com_razao if p["residuo"] > 0),
            "com_razao": len(com_razao),
            "p": None,
        }
        if cond in TESTE and com_razao:
            linha["p"] = p_permutacao([p["residuo"] for p in com_razao], res_calib)
        resumo.append(linha)

    ajustados = holm({r["condicao"]: r["p"] for r in resumo if r["p"] is not None})
    for r in resumo:
        r["p_holm"] = ajustados.get(r["condicao"])

    dp_calib = statistics.pstdev(res_calib)

    # ---- relatório ---------------------------------------------------------
    L: list[str] = []
    add = L.append
    add("# Marcadores construcionais e a lei de frequência")
    add("")
    add("Gerado por `experimentos/teste_construcional.py`. Valores em |Δ PLL| por")
    add("token, com o alvo mascarado por inteiro. O piso é a mediana da condição")
    add("de controle neutro. A unidade de replicação é o **par**; medianas por")
    add("condição são medianas de medianas de par, e o intervalo de 95% vem de")
    add("reamostragem por conglomerado sobre os pares.")
    add("")
    add(f"**Reta da frequência**, ajustada sobre {len(calib)} pares não regionais:")
    add(f"|Δ| = {a:.4f} + {b:.4f} · log10(razão de frequência), "
        f"com R² = {r2:.3f} e p = {p_inclinacao:.4f} para a inclinação.")
    add("")
    add(f"O desvio-padrão dos resíduos de calibração é {dp_calib:.4f}, contra")
    add(f"mediana de {statistics.median(ys):.4f} nos mesmos pares. É a escala do")
    add("ruído no nível do par, e é contra ela que todo resíduo abaixo deve ser lido.")
    add("")
    add("O resíduo é o quanto a condição excede o que a frequência sozinha prevê.")
    add("O valor-p é unilateral, por permutação de rótulos de par contra os pares")
    add("de calibração; `p Holm` é o mesmo valor corrigido para as seis condições")
    add("confrontadas com a mesma calibração.")
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
    add("## Pares construcionais, um a um")
    add("")
    add("| construção | razão | \\|Δ\\| mediano | previsto pela frequência | resíduo |")
    add("|---|---|---|---|---|")
    d_pares = [p for p in pares if p["condicao"] == "dialeto_D"]
    for (nome, _, _), p in zip(CONSTRUCIONAIS, d_pares):
        rz = f"{p['razao']:.1f}×" if p["razao"] else "—"
        pr = f"{p['previsto']:.4f}" if p["previsto"] is not None else "—"
        rs = f"{p['residuo']:+.4f}" if p["residuo"] is not None else "—"
        add(f"| {nome} | {rz} | {p['mediana']:.4f} | {pr} | {rs} |")
    add("")

    texto = "\n".join(L)
    # Saída de máquina, regerável. O relatório interpretado vive em
    # `construcional.md`, escrito à mão sobre estes números, e o script não o
    # toca: gravar interpretação no mesmo caminho que a tabela faria a
    # reexecução apagá-la sem aviso.
    (TABELAS / "construcional_tabelas.md").write_text(texto, encoding="utf-8")
    (SAIDA / "construcional_pares.json").write_text(
        json.dumps(pares, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n" + texto)


if __name__ == "__main__":
    main()
