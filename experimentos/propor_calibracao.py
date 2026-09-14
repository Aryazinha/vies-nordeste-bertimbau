"""
propor_calibracao.py

Propõe pares de calibração — não regionais — para levar o grupo de referência
aos 80 pares distintos exigidos por
`experimentos/resultados/tabelas/meta_pares_minimos.md`.

## Por que o grupo de referência é o gargalo, e não as condições de teste

O grupo de referência calibra a reta da frequência, e a sua própria incerteza
impõe **teto** ao que o conjunto inteiro pode excluir: com 26 pares, nenhum
efeito abaixo de 0,078 é detectável sob correção de multiplicidade, por mais
pares de teste que se acrescentem. Aos 80, o teto cai a 0,045, abaixo da meta
de 0,08 fixada pela equipe.

## Por que 55, e não 54

O grupo tem 26 entradas, mas 25 pares distintos: `controle_frequencia-05` é
`controle_neutro-03` com os lados invertidos, e está marcado como excluído da
calibração (`docs/pendencias.md` 2.8).

## Revisão de 14/09/2026: uma frase, um par

A primeira versão deste script formava **todas** as combinações de itens dentro
de seis molduras. A mesma frase comparecia então em até cinco pares, e dez
frases propostas já constavam do conjunto canônico; ligando os pares por frase
compartilhada, os 80 resultantes formavam apenas 20 grupos. Pares que
compartilham um lado compartilham o termo de pseudo-verossimilhança daquele
lado e não são replicações independentes — a objeção de
`docs/achados_para_o_artigo.md` §1.16, deslocada da medição para o par —, e o
teto de detecção, que supõe independência, ficaria superestimado.

Esta versão impõe quatro regras, verificadas por asserção antes da gravação:

1. **Cada frase comparece em um único par**, e em nenhum lado do conjunto
   canônico.
2. **No máximo `MAX_POR_MOLDURA` pares por moldura**, com molduras distintas das
   já presentes no grupo de referência, para que a reta não descreva uma
   construção sintática particular.
3. **O artigo pertence à moldura.** Os itens de cada lista têm o mesmo gênero,
   de modo que os lados diferem por uma única palavra. Na versão anterior,
   *o casaco* contra *a carteira* fazia o artigo entrar na média geométrica da
   razão de frequência e atenuá-la.
4. **Diferença de subtokens de no máximo um** entre os itens que distinguem os
   lados. A reta é ajustada sobre |Δ PLL| da frase inteira, e cada subtoken a
   mais é um termo a mais nessa soma.

## Revisão humana, e por que ela trava a seleção

A decisão sobre cada par proposto fica em `resultados/dados/calibracao_revisao.json`:
pares aprovados, pares rejeitados com o motivo, e **itens vetados** — palavras
excluídas de toda moldura, em geral por segundo sentido corrente que inflaria a
razão de frequência (*violeta*, cor e nome próprio) ou por designarem ocupação
(*chaveiro*).

Quando o arquivo existe, os pares aprovados entram na seleção **já fixados**, e
o script completa apenas as vagas restantes. Sem a trava, retirar um item e
repetir a seleção reorganizaria a lista inteira e desfaria a revisão já feita.
Os identificadores (`moldura-índice`) nunca são reaproveitados: um par novo
recebe índice acima de todos os já atribuídos àquela moldura, inclusive os de
pares rejeitados.

A seleção das vagas restantes preenche primeiro a faixa de razão com menos
pares, de modo que a rejeição concentrada numa faixa seja compensada nela.

## O que o script faz, e o que deixa para a pessoa

Gera candidatos por moldura, mede cada um e seleciona. Não decide: grava uma
proposta para revisão humana. **Não mede no modelo** — a medição, de 28
atributos por par, é etapa posterior, e só se executa sobre a lista aprovada.

## A restrição de conteúdo

Os itens são de vocabulário corrente, sem carga regional conhecida e sem
referência a pessoa ou ocupação, que interagiria com as molduras de atributo
(*Quem falou isso trabalha como...*). A ausência de carga regional é juízo dos
autores e não foi validada por juízes (Filtro 1).

Uso:
    python propor_calibracao.py
    python propor_calibracao.py --n 55 --saida resultados/dados/calibracao_proposta.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from wordfreq import word_frequency

from teste_construcional import razao_frequencia

RAIZ = Path(__file__).resolve().parent
CANONICO = RAIZ / "resultados" / "dados" / "pares_minimos.json"
REVISAO = RAIZ / "resultados" / "dados" / "calibracao_revisao.json"
SAIDA_PADRAO = RAIZ / "resultados" / "dados" / "calibracao_proposta.json"

MODELO = "neuralmind/bert-base-portuguese-cased"

# Moldura de enunciado e itens que a preenchem. Três exigências de curadoria:
# toda combinação produz enunciado natural; todos os itens de uma lista têm o
# gênero do artigo da moldura; e cada lista mistura itens comuns e raros, para
# que a mesma moldura possa contribuir com pares de razão baixa e alta.
# Itens vetados na revisão humana permanecem nas listas e são filtrados a partir
# de `REVISAO`, para que a lista original continue legível no histórico.
MOLDURAS = {
    "parede":      ("Ele pendurou o {item} na parede da sala.",
                    ["quadro", "relógio", "espelho", "calendário", "mapa", "pôster",
                     "diploma", "termômetro"]),
    "mesa":        ("Ela deixou a {item} em cima da mesa.",
                    ["caneta", "xícara", "tesoura", "lanterna", "calculadora", "lupa",
                     "agenda", "apostila", "pinça", "espátula"]),
    "conserto":    ("Meu pai consertou o {item} no fim de semana.",
                    ["carro", "portão", "telhado", "chuveiro", "ventilador",
                     "liquidificador", "aspirador", "interfone", "aquecedor"]),
    "perda":       ("Perdi o {item} no caminho de casa.",
                    ["documento", "cartão", "boné", "isqueiro", "crachá", "chaveiro",
                     "bilhete", "ingresso"]),
    "aula":        ("Na aula de hoje usamos um {item}.",
                    ["computador", "dicionário", "mapa", "globo", "microscópio",
                     "projetor", "telescópio", "cronômetro", "metrônomo"]),
    "varanda":     ("Ela regou a {item} da varanda.",
                    ["planta", "samambaia", "orquídea", "roseira", "violeta", "begônia",
                     "hortênsia", "azaleia"]),
    "banheiro":    ("Troquei a {item} do banheiro.",
                    ["lâmpada", "pia", "toalha", "torneira", "descarga", "banheira",
                     "saboneteira", "fechadura"]),
    "vizinho":     ("O vizinho comprou um {item} novo.",
                    ["carro", "sofá", "computador", "fogão", "aspirador", "patinete",
                     "triciclo", "barco"]),
    "escritorio":  ("Esqueci o {item} no escritório.",
                    ["celular", "casaco", "carregador", "caderno", "envelope",
                     "grampeador", "crachá", "estojo"]),
    "desenho":     ("A menina desenhou um {item} no caderno.",
                    ["gato", "cavalo", "barco", "castelo", "foguete", "dinossauro",
                     "girassol", "unicórnio", "pinguim", "flamingo"]),
    "zoologico":   ("Vimos um {item} no zoológico.",
                    ["leão", "elefante", "macaco", "tigre", "camelo", "hipopótamo",
                     "rinoceronte", "tamanduá", "suricato"]),
    "instrumento": ("Ele tocou {item} na festa da escola.",
                    ["violão", "piano", "bateria", "flauta", "violino", "saxofone",
                     "clarinete", "trompete", "harpa", "oboé"]),
    "filme":       ("Assistimos a um filme de {item} ontem.",
                    ["ação", "terror", "comédia", "suspense", "aventura", "faroeste",
                     "animação", "drama", "mistério"]),
    "louca":       ("Quebrei o {item} enquanto lavava a louça.",
                    ["prato", "copo", "pote", "bule", "jarro", "pires", "cálice",
                     "açucareiro"]),
    "chuva":       ("Choveu muito na {item} passada.",
                    ["semana", "madrugada", "noite", "quinta", "sexta", "quarta"]),
    "bairro":      ("Ele mora perto de uma {item}.",
                    ["escola", "praça", "igreja", "farmácia", "padaria", "lavanderia",
                     "biblioteca", "academia", "floricultura", "marcenaria"]),
    "presente":    ("Dei um {item} de presente para ela.",
                    ["livro", "perfume", "relógio", "colar", "anel", "broche",
                     "pingente", "chaveiro", "bracelete"]),
    "gato":        ("O gato dormiu em cima do {item}.",
                    ["sofá", "tapete", "armário", "travesseiro", "edredom",
                     "computador", "baú"]),
    "pintura":     ("Pintamos a {item} de azul.",
                    ["parede", "cerca", "cadeira", "grade", "estante", "cômoda",
                     "prateleira", "escrivaninha", "penteadeira"]),
    "viagem":      ("Levamos a {item} na viagem.",
                    ["mala", "câmera", "barraca", "mochila", "bicicleta", "prancha",
                     "garrafa", "toalha"]),
}

# Faixas de razão de frequência a cobrir. A reta precisa de pontos espalhados:
# um conjunto concentrado perto de 1,0 ajusta o intercepto e não a inclinação.
FAIXAS = [(1.0, 1.5), (1.5, 3.0), (3.0, 8.0), (8.0, 25.0), (25.0, 100.0), (100.0, 1e9)]

MAX_DIFERENCA_SUBTOKENS = 1
MAX_POR_MOLDURA = 3


def _tokenizador():
    import os

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(MODELO)


def _palavras(frase: str) -> list[str]:
    return re.findall(r"[^\W\d_]+", frase.lower(), flags=re.UNICODE)


def _faixa(razao: float) -> tuple[float, float]:
    return next(f for f in FAIXAS if f[0] <= razao < f[1])


def _rotulo_faixa(f: tuple[float, float]) -> str:
    return f"{f[0]:g}–{f[1]:g}" if f[1] < 1e9 else f"> {f[0]:g}"


def canonico() -> tuple[set[str], set[str]]:
    """Frases já presentes em qualquer lado do conjunto, e palavras dos atributos."""
    dados = json.loads(CANONICO.read_text(encoding="utf-8"))
    frases = {p[lado] for p in dados["pares"] for lado in ("lado_a", "lado_b")}
    atributos = {a.lower() for lista in dados["_meta"]["atributos_por_moldura"].values()
                 for a in lista}
    return frases, atributos


def revisao() -> dict:
    """Decisões humanas já tomadas. Arquivo ausente equivale a revisão nenhuma."""
    if not REVISAO.exists():
        return {"itens_vetados": {}, "pares": []}
    return json.loads(REVISAO.read_text(encoding="utf-8"))


def validar_molduras(atributos: set[str]) -> None:
    """Falha cedo em erro de curadoria que a seleção não detectaria."""
    for nome, (moldura, itens) in MOLDURAS.items():
        assert len(itens) == len(set(itens)), f"{nome}: item repetido"
        for item in itens:
            assert len(_palavras(item)) == 1, f"{nome}: '{item}' não é palavra única"
            assert item.lower() not in atributos, f"{nome}: '{item}' coincide com atributo"
            assert item.lower() not in _palavras(moldura.format(item="")), \
                f"{nome}: '{item}' já ocorre na moldura"


def medir_par(tok, nome: str, item_a: str, item_b: str) -> dict:
    moldura = MOLDURAS[nome][0]
    lado_a, lado_b = moldura.format(item=item_a), moldura.format(item=item_b)
    razao, so_a, so_b = razao_frequencia(lado_a, lado_b)
    sub_a, sub_b = len(tok.tokenize(item_a)), len(tok.tokenize(item_b))
    return {
        "moldura": nome,
        "lado_a": lado_a,
        "lado_b": lado_b,
        "itens_a": so_a,
        "itens_b": so_b,
        "razao_frequencia": round(razao, 3),
        "subtokens_a": sub_a,
        "subtokens_b": sub_b,
        "diferenca_subtokens": abs(sub_a - sub_b),
        "freq_a": word_frequency(item_a, "pt"),
        "freq_b": word_frequency(item_b, "pt"),
    }


def candidatos(tok, frases_canonicas: set[str], vetados: set[str]) -> list[dict]:
    """Todos os pares possíveis dentro de cada moldura, sem itens vetados, já medidos."""
    saida = []
    for nome, (moldura, itens) in MOLDURAS.items():
        itens = [i for i in itens if i not in vetados]
        for i, item_a in enumerate(itens):
            for item_b in itens[i + 1:]:
                if (moldura.format(item=item_a) in frases_canonicas
                        or moldura.format(item=item_b) in frases_canonicas):
                    continue
                saida.append(medir_par(tok, nome, item_a, item_b))
    return saida


def selecionar(cands: list[dict], n: int, max_dif: int, max_moldura: int,
               travados: list[dict]) -> list[dict]:
    """
    Completa os `travados` até `n` pares, sem reutilizar frase e sem exceder
    `max_moldura` pares por moldura.

    A cada vaga, escolhe a faixa de razão com menos pares que ainda tenha
    candidato admissível; dentro dela, a moldura menos usada. A ordem de
    desempate — moldura, depois razão — é fixa, para que a seleção não dependa
    da ordem de iteração.
    """
    escolhidos = list(travados)
    frases_usadas = {c[lado] for c in travados for lado in ("lado_a", "lado_b")}
    uso = Counter(c["moldura"] for c in travados)
    por_faixa = Counter(_faixa(c["razao_frequencia"]) for c in travados)

    def admissivel(c: dict) -> bool:
        return (c["diferenca_subtokens"] <= max_dif
                and uso[c["moldura"]] < max_moldura
                and c["lado_a"] not in frases_usadas
                and c["lado_b"] not in frases_usadas)

    while len(escolhidos) < n:
        escolha = None
        for faixa in sorted(FAIXAS, key=lambda f: (por_faixa[f], FAIXAS.index(f))):
            livres = [c for c in cands if _faixa(c["razao_frequencia"]) == faixa and admissivel(c)]
            if livres:
                escolha = min(livres, key=lambda c: (uso[c["moldura"]], c["moldura"],
                                                     c["razao_frequencia"]))
                break
        if escolha is None:
            break
        escolhidos.append(escolha)
        frases_usadas.update((escolha["lado_a"], escolha["lado_b"]))
        uso[escolha["moldura"]] += 1
        por_faixa[_faixa(escolha["razao_frequencia"])] += 1
    return escolhidos


def atribuir_ids(escolhidos: list[dict], rev: dict) -> None:
    """Novos pares recebem índice acima de todo índice já usado na moldura."""
    maior = Counter()
    for p in rev["pares"]:
        nome, indice = p["id"].rsplit("-", 1)
        maior[nome] = max(maior[nome], int(indice))
    for c in escolhidos:
        if "id" not in c:
            maior[c["moldura"]] += 1
            c["id"] = f"{c['moldura']}-{maior[c['moldura']]}"
            c["revisao"] = "pendente"


def verificar(escolhidos: list[dict], frases_canonicas: set[str], max_moldura: int,
              rev: dict) -> None:
    """As regras do cabeçalho, conferidas sobre a saída e não sobre a intenção."""
    frases = [c[lado] for c in escolhidos for lado in ("lado_a", "lado_b")]
    assert len(frases) == len(set(frases)), "frase repetida entre pares propostos"
    assert not set(frases) & frases_canonicas, "frase proposta já consta do conjunto canônico"
    assert max(Counter(c["moldura"] for c in escolhidos).values()) <= max_moldura
    vetados = set(rev["itens_vetados"])
    for c in escolhidos:
        assert not set(c["itens_a"] + c["itens_b"]) & vetados, f"{c['id']}: item vetado"
    ids = [c["id"] for c in escolhidos]
    assert len(ids) == len(set(ids)), "identificador repetido"
    aprovados = {p["id"] for p in rev["pares"] if p["decisao"] == "aprovado"}
    assert aprovados <= set(ids), "par aprovado ausente da saída"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=55,
                    help="pares a propor (padrão: 55, que leva o grupo de 25 pares distintos a 80)")
    ap.add_argument("--max-diferenca-subtokens", type=int, default=MAX_DIFERENCA_SUBTOKENS)
    ap.add_argument("--max-por-moldura", type=int, default=MAX_POR_MOLDURA)
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    args = ap.parse_args()

    frases_canonicas, atributos = canonico()
    validar_molduras(atributos)
    rev = revisao()
    tok = _tokenizador()

    travados = []
    for p in rev["pares"]:
        if p["decisao"] == "aprovado":
            par = medir_par(tok, p["moldura"], p["item_a"], p["item_b"])
            par.update(id=p["id"], revisao="aprovado")
            travados.append(par)

    cands = candidatos(tok, frases_canonicas, set(rev["itens_vetados"]))
    escolhidos = selecionar(cands, args.n, args.max_diferenca_subtokens,
                            args.max_por_moldura, travados)
    atribuir_ids(escolhidos, rev)
    verificar(escolhidos, frases_canonicas, args.max_por_moldura, rev)

    novos = [c for c in escolhidos if c["revisao"] == "pendente"]
    print(f"{len(cands)} candidato(s) possível(is); {len(travados)} aprovado(s) "
          f"travado(s); {len(novos)} novo(s) a revisar.")
    print()
    print(f"{'id':15} {'razão':>8} {'sub':>5}  enunciados")
    for c in novos:
        print(f"{c['id']:15} {c['razao_frequencia']:>8.2f} "
              f"{c['subtokens_a']}/{c['subtokens_b']:<3}  {c['lado_a']}  ||  {c['lado_b']}")

    faixas = Counter(_rotulo_faixa(_faixa(c["razao_frequencia"])) for c in escolhidos)
    faixas = {_rotulo_faixa(f): faixas[_rotulo_faixa(f)] for f in FAIXAS}
    print()
    print("dispersão por faixa de razão de frequência:", faixas)
    print("molduras:", dict(Counter(c["moldura"] for c in escolhidos)))

    if len(escolhidos) < args.n:
        print(f"\nATENÇÃO: só {len(escolhidos)} de {args.n} puderam ser propostos "
              "sob as regras. Amplie MOLDURAS, declarando a mudança, em vez de "
              "afrouxar a regra de uma frase por par.")

    Path(args.saida).write_text(
        json.dumps({"_meta": {"gerado_por": "propor_calibracao.py",
                              "regras": {"uma_frase_por_par": True,
                                         "max_por_moldura": args.max_por_moldura,
                                         "max_diferenca_subtokens": args.max_diferenca_subtokens},
                              "revisao_aplicada": REVISAO.name if REVISAO.exists() else None,
                              "n_propostos": len(escolhidos),
                              "n_aprovados": len(travados),
                              "n_pendentes": len(novos),
                              "dispersao_por_faixa": faixas,
                              "medido_no_modelo": False},
                    "pares": escolhidos}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"\nGravado em {args.saida}. Revisão humana dos pendentes antes de incorporar.")


if __name__ == "__main__":
    main()
