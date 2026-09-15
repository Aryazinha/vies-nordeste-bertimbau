"""
analise_moldura.py — controle de moldura da menção explícita (`docs/pendencias.md` 2.10)

## A pergunta

O item 1.17 de `docs/achados_para_o_artigo.md` estabelece que a menção explícita
à região produz |Δ PLL| acima do grupo de referência. Os pares que o sustentam
são quase todos enunciados de autoidentificação — *Sou baiano*, *Meu pai é
carioca* —, forma ausente do grupo de referência. Fica sem resposta a objeção de
que esse tipo de enunciado produz |Δ| elevado qualquer que seja o rótulo.

Cada par de teste tem, em `teste_explicito.CONTROLE_MOLDURA`, um gêmeo com a mesma
frase e o mesmo lado de comparação, trocado apenas o rótulo nordestino por um do
Sul (ou do Centro-Oeste). A moldura é idêntica dentro de cada dupla, e a
comparação dentro da dupla a elimina.

## Medida e teste — registrados antes da medição

Para cada frase k: D_k = |Δ| mediano do par de teste − |Δ| mediano do gêmeo.
Positivo significa que o rótulo nordestino produz mais resposta que o rótulo de
controle **na mesma frase**.

Teste unilateral de média de D > 0 por **permutação exata de sinais** no nível da
frase — com oito frases são 256 atribuições, e não há por que amostrá-las —, e
correção de Holm sobre as quatro condições.

**Predições, em `docs/pendencias.md` 2.10:** D > 0 em `explicito_gentilico` e
`explicito_regiao`, se a resposta for específica do Nordeste; D próximo de zero
em `explicito_toponimo`. D próximo de zero nas duas primeiras indicaria resposta a
rótulo regional em enunciado de autoidentificação, e não ao Nordeste.

**Limite de resolução, declarado:** com cinco frases, o menor valor-p exato é
1/32 = 0,031, que a correção de Holm para quatro condições leva a 0,125. A
condição `controle_explicito` não pode, por construção, sobreviver à correção. As
predições não dependem dela.

## O que é secundário, e não foi registrado

- O reagrupamento pessoa/lugar sobre D permanece exploratório: os pares de teste
  são os mesmos que sugeriram aquela hipótese.
- A comparação dos gêmeos com o grupo de referência — se enunciados de
  autoidentificação sem rótulo nordestino já produzem |Δ| elevado — é descritiva.

Uso:
    python analise_moldura.py
"""

from __future__ import annotations

import json
import random
import statistics
from pathlib import Path

from teste_construcional import holm, p_permutacao
from teste_explicito import CALIBRACAO, EXCLUIDOS_DA_CALIBRACAO, TESTE_DO_CONTROLE

SAIDA = Path(__file__).resolve().parent / "resultados"
PARES_MEDIDOS = SAIDA / "dados" / "explicito_pares.json"
TABELA = SAIDA / "tabelas" / "moldura_tabelas.md"

SEMENTE = 20260914
PESSOA = ("nordestino", "pernambucano", "paraibano", "baiano", "cearense",
          "nordestina", "pernambucana", "paraibana", "baiana")

# Frases por condição antes do crescimento de 15/09/2026; as seguintes são as novas.
ORIGINAIS = {"explicito_regiao": 8, "explicito_gentilico": 8, "explicito_toponimo": 8,
             "controle_explicito": 5}
# Efeito específico a excluir, decidido em 2.11.
EFEITO_ALVO = 0.08


def _resumo(teste: str, ds: list[float]) -> dict:
    return {"teste": teste, "n": len(ds), "media": statistics.mean(ds), "ic": ic_media(ds),
            "positivos": sum(1 for d in ds if d > 0), "p": p_sinais_exato(ds)}


N_EXATO_MAXIMO = 20
N_SORTEIOS = 200_000


def p_sinais_exato(ds: list[float]) -> float:
    """
    P(média com sinais permutados ≥ média observada).

    Exato, sobre as 2^n atribuições, até `N_EXATO_MAXIMO` frases; acima disso, por
    sorteio de `N_SORTEIOS` atribuições com semente fixa. Correção de 15/09/2026:
    com o crescimento a 20 frases por condição, o reagrupamento exploratório
    pessoa/lugar passou a ter 30 frases, e 2^30 atribuições não terminam em tempo
    útil. As análises registradas, com até 20 frases por condição, seguem exatas.
    """
    n, observado = len(ds), statistics.mean(ds)
    if n > N_EXATO_MAXIMO:
        rng = random.Random(SEMENTE)
        extremos = sum(
            1 for _ in range(N_SORTEIOS)
            if sum(d if rng.random() < 0.5 else -d for d in ds) / n >= observado - 1e-12)
        return (extremos + 1) / (N_SORTEIOS + 1)
    extremos = 0
    for mascara in range(2 ** n):
        soma = sum(-d if (mascara >> i) & 1 else d for i, d in enumerate(ds))
        if soma / n >= observado - 1e-12:
            extremos += 1
    return extremos / 2 ** n


def ic_media(ds: list[float], n: int = 10000) -> tuple[float, float]:
    """Intervalo de 95% da média de D, por reamostragem de frases."""
    rng = random.Random(SEMENTE)
    medias = sorted(statistics.mean(rng.choices(ds, k=len(ds))) for _ in range(n))
    return medias[int(0.025 * n)], medias[int(0.975 * n)]


def main() -> None:
    pares = json.loads(PARES_MEDIDOS.read_text(encoding="utf-8"))
    por_chave = {(p["condicao"], p["par"]): p for p in pares}

    L = []
    add = L.append
    add("# Controle de moldura da menção explícita")
    add("")
    add("Gerado por `experimentos/analise_moldura.py`. D = |Δ| do par de teste menos |Δ|")
    add("do gêmeo com a mesma frase e rótulo de outra região. Positivo: o rótulo")
    add("nordestino produz mais resposta que o de controle na mesma frase. Teste")
    add("unilateral por permutação exata de sinais no nível da frase; Holm sobre as")
    add("quatro condições. Desenho e predições em `docs/pendencias.md` 2.10.")
    add("")

    resumo, detalhe, ds_por_condicao = [], [], {}
    for controle, teste in TESTE_DO_CONTROLE.items():
        ds, i = [], 0
        while (teste, i) in por_chave:
            t, c = por_chave[(teste, i)], por_chave.get((controle, i))
            if c is None:
                raise SystemExit(f"{controle}-{i:02d} sem medição: rode teste_explicito.py")
            d = t["mediana"] - c["mediana"]
            ds.append(d)
            detalhe.append((teste, i, t["a"], c["a"], t["mediana"], c["mediana"], d))
            i += 1
        ds_por_condicao[teste] = ds
        resumo.append({"teste": teste, "n": len(ds), "media": statistics.mean(ds),
                       "ic": ic_media(ds), "positivos": sum(1 for d in ds if d > 0),
                       "p": p_sinais_exato(ds)})

    def tabela(titulo: str, linhas: list[dict]) -> None:
        # Regras de decisão registradas em `docs/pendencias.md` 2.12: especificidade
        # detectada se p Holm < 0,05; efeito acima de 0,08 excluído se não detectada
        # e o limite superior do IC 95% ficar abaixo de 0,08; inconclusivo no resto.
        ajust = holm({r["teste"]: r["p"] for r in linhas})
        add(f"## {titulo}")
        add("")
        add("| condição de teste | frases | D médio | IC 95% | D > 0 | p exato | p Holm | leitura |")
        add("|---|---|---|---|---|---|---|---|")
        for r in linhas:
            if ajust[r["teste"]] < 0.05:
                leitura = "especificidade detectada"
            elif r["ic"][1] < EFEITO_ALVO:
                leitura = f"exclui D > {EFEITO_ALVO:.2f}"
            else:
                leitura = "inconclusivo"
            add(f"| `{r['teste']}` | {r['n']} | {r['media']:+.4f} | "
                f"{r['ic'][0]:+.4f}–{r['ic'][1]:+.4f} | {r['positivos']}/{r['n']} | "
                f"{r['p']:.4f} | {ajust[r['teste']]:.4f} | {leitura} |")
        add("")

    tabela("Resultado registrado — todas as frases", resumo)
    novos = [_resumo(t, ds[ORIGINAIS[t]:]) for t, ds in ds_por_condicao.items()
             if len(ds) - ORIGINAIS[t] >= 2]
    if novos:
        tabela("Secundário registrado — só as frases acrescentadas em 15/09/2026", novos)

    add("## Por frase")
    add("")
    add("| condição | # | enunciado de teste | enunciado gêmeo | \\|Δ\\| teste | \\|Δ\\| gêmeo | D |")
    add("|---|---|---|---|---|---|---|")
    for teste, i, ta, ca, mt, mc, d in detalhe:
        add(f"| `{teste}` | {i} | {ta} | {ca} | {mt:.4f} | {mc:.4f} | {d:+.4f} |")
    add("")

    # ---- secundário: reagrupamento pessoa/lugar sobre D (exploratório) --------
    grupos = {"pessoa": [], "lugar": []}
    for teste, i, ta, _, _, _, d in detalhe:
        if teste.startswith("explicito"):
            grupos["pessoa" if any(w in ta.lower() for w in PESSOA) else "lugar"].append(d)
    add("## Secundário, não registrado: pessoa contra lugar, sobre D")
    add("")
    add("Exploratório — os pares de teste são os que sugeriram a hipótese.")
    add("")
    add("| agrupamento | frases | D médio | D > 0 | p exato |")
    add("|---|---|---|---|---|")
    for nome, ds in grupos.items():
        add(f"| rótulo de {nome} | {len(ds)} | {statistics.mean(ds):+.4f} | "
            f"{sum(1 for d in ds if d > 0)}/{len(ds)} | {p_sinais_exato(ds):.4f} |")
    add("")

    # ---- secundário: gêmeos contra o grupo de referência (descritivo) --------
    calib = [p for p in pares if p["condicao"] in CALIBRACAO and p.get("residuo") is not None
             and (p["condicao"], p["par"]) not in EXCLUIDOS_DA_CALIBRACAO]
    ref = [p["mediana"] for p in calib]
    add("## Secundário, não registrado: os gêmeos contra o grupo de referência")
    add("")
    add("Pergunta se enunciados de autoidentificação **sem** rótulo nordestino já")
    add(f"produzem |Δ| elevado. Grupo de referência: {len(ref)} pares, mediana de |Δ| "
        f"{statistics.median(ref):.4f}. Permutação unilateral de rótulos de par, "
        "sobre |Δ| e não sobre resíduo; descritivo.")
    add("")
    add("| gêmeos de | frases | mediana \\|Δ\\| | média \\|Δ\\| | p |")
    add("|---|---|---|---|---|")
    for controle, teste in TESTE_DO_CONTROLE.items():
        v = [p["mediana"] for p in pares if p["condicao"] == controle]
        add(f"| `{teste}` | {len(v)} | {statistics.median(v):.4f} | {statistics.mean(v):.4f} | "
            f"{p_permutacao(v, ref):.4f} |")
    add("")

    texto = chr(10).join(L)
    TABELA.write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
