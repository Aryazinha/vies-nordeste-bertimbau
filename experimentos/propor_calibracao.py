"""
propor_calibracao.py

Propõe pares de calibração — não regionais — para levar o grupo de referência
dos 26 atuais aos 80 exigidos por `experimentos/resultados/tabelas/meta_pares_minimos.md`.

## Por que o grupo de referência é o gargalo, e não as condições de teste

O grupo de referência calibra a reta da frequência, e a sua própria incerteza
impõe **teto** ao que o conjunto inteiro pode excluir: com 26 pares, nenhum
efeito abaixo de 0,078 é detectável sob correção de multiplicidade, por mais
pares de teste que se acrescentem. Aos 80, o teto cai a 0,045, abaixo da meta
de 0,08 fixada pela equipe. Crescer o grupo de teste antes disso seria
trabalho sem efeito sobre a afirmação que o artigo precisa sustentar.

## O que o script faz, e o que deixa para a pessoa

Gera candidatos por combinação controlada de **moldura de enunciado** e
**item lexical**, e mede cada candidato em três dimensões antes de propô-lo.
Não decide: grava uma planilha para revisão, no mesmo espírito de
`verificar_reincidencia.py` e `anonimizar_transcricao.py`.

As três medidas, e por que cada uma:

1. **Razão de frequência**, pela mesma função de `teste_construcional.py` — e
   não uma reimplementação, para que as duas não divirjam em silêncio. É a
   variável que a calibração ajusta, e o conjunto precisa de **dispersão**:
   pares todos próximos de 1,0 não determinam a inclinação da reta.
2. **Diferença de subtokens entre os lados.** A advertência publicada com o
   conjunto — "qualquer conjunto derivado deve balancear subtokens entre os
   polos" — nasceu do artefato de +0,195 desfeito no passo 5.5. Ali a
   assimetria estava nos atributos; aqui pode estar no próprio enunciado, e o
   efeito seria o mesmo: diferença de extensão lida como diferença de escore.
3. **Ineditismo.** Um par já presente no conjunto canônico não acrescenta
   informação, e repetir enunciado entre condições contaminaria a calibração.

## A restrição de conteúdo

Os itens são de vocabulário corrente e **sem carga regional**: é o que
distingue o grupo de referência das condições de teste. Um item regional aqui
inverteria o papel do grupo, que existe justamente para medir o que a
frequência explica quando região não está em jogo.

Uso:
    python propor_calibracao.py --n 54
    python propor_calibracao.py --n 54 --saida resultados/dados/calibracao_proposta.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from wordfreq import word_frequency

from teste_construcional import razao_frequencia

RAIZ = Path(__file__).resolve().parent
CANONICO = RAIZ / "resultados" / "dados" / "pares_minimos.json"
SAIDA_PADRAO = RAIZ / "resultados" / "dados" / "calibracao_proposta.json"

MODELO = "neuralmind/bert-base-portuguese-cased"

# Moldura de enunciado e itens que a preenchem. Os itens de cada lista foram
# escolhidos para que **toda** combinação produza enunciado natural — geração
# combinatória sem essa curadoria produz frase esquisita, e frase esquisita
# mede a estranheza, não a frequência.
MOLDURAS = {
    "compra": ("Comprei {item} na feira hoje.",
               ["pão", "leite", "arroz", "sal", "açúcar", "farinha", "fermento",
                "manteiga", "queijo", "café", "feijão", "macarrão", "vinagre",
                "canela", "gengibre", "alecrim", "orégano", "cravo"]),
    "fechar": ("Fechei a {item} antes de sair.",
               ["porta", "janela", "gaveta", "cortina", "torneira", "persiana"]),
    "guardar": ("Guardei {item} no armário da cozinha.",
                ["o pão", "o arroz", "o açúcar", "a farinha", "o fermento",
                 "a panela", "a peneira", "o coador", "o escorredor"]),
    "esquecer": ("Ela esqueceu {item} dentro do carro.",
                 ["a bolsa", "o casaco", "a chave", "o guarda-chuva", "o celular",
                  "a carteira", "o cachecol", "a sombrinha"]),
    "levar": ("O menino levou {item} para a escola.",
              ["o caderno", "a mochila", "o lanche", "a régua", "o estojo",
               "o compasso", "o transferidor"]),
    "horario": ("O ônibus passa às {item}.",
                ["sete horas", "oito horas", "nove horas", "onze horas",
                 "cinco horas", "quatro horas"]),
}

# Faixas de razão de frequência a cobrir. A reta precisa de pontos espalhados:
# um conjunto concentrado perto de 1,0 ajusta o intercepto e não a inclinação.
FAIXAS = [(1.0, 1.5), (1.5, 3.0), (3.0, 8.0), (8.0, 25.0), (25.0, 100.0), (100.0, 1e9)]

# Diferença máxima de subtokens entre os itens que distinguem os dois lados.
MAX_DIFERENCA_SUBTOKENS = 1


def _tokenizador():
    import os

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(MODELO)


def _subtokens(tok, itens: list[str]) -> int:
    return sum(len(tok.tokenize(p)) for p in itens)


def pares_existentes() -> set[tuple[str, str]]:
    """Pares já no conjunto canônico, em ambas as ordens."""
    dados = json.loads(CANONICO.read_text(encoding="utf-8"))
    existentes = set()
    for par in dados["pares"]:
        existentes.add((par["lado_a"], par["lado_b"]))
        existentes.add((par["lado_b"], par["lado_a"]))
    return existentes


def candidatos(tok) -> list[dict]:
    """Todos os pares possíveis dentro de cada moldura, já medidos."""
    existentes = pares_existentes()
    saida = []
    for nome, (moldura, itens) in MOLDURAS.items():
        for i, item_a in enumerate(itens):
            for item_b in itens[i + 1:]:
                lado_a = moldura.format(item=item_a)
                lado_b = moldura.format(item=item_b)
                if (lado_a, lado_b) in existentes:
                    continue
                medida = razao_frequencia(lado_a, lado_b)
                if medida is None:
                    continue                   # pura adição de palavra: razão indefinida
                razao, so_a, so_b = medida
                sub_a, sub_b = _subtokens(tok, so_a), _subtokens(tok, so_b)
                saida.append({
                    "moldura": nome,
                    "lado_a": lado_a,
                    "lado_b": lado_b,
                    "itens_a": so_a,
                    "itens_b": so_b,
                    "razao_frequencia": round(razao, 3),
                    "subtokens_a": sub_a,
                    "subtokens_b": sub_b,
                    "diferenca_subtokens": abs(sub_a - sub_b),
                    "freq_a": word_frequency(" ".join(so_a), "pt"),
                    "freq_b": word_frequency(" ".join(so_b), "pt"),
                })
    return saida


def selecionar(cands: list[dict], n: int, max_dif: int) -> list[dict]:
    """
    Escolhe `n` candidatos cobrindo as faixas de razão de frequência, em
    rodízio entre elas e entre as molduras.

    O rodízio entre molduras existe para que a calibração não descreva uma
    única construção sintática: uma reta ajustada sobre dez variantes de
    "Comprei X na feira" mede aquela moldura, e é aplicada a enunciados de
    forma bem diversa.
    """
    elegiveis = [c for c in cands if c["diferenca_subtokens"] <= max_dif]
    por_faixa: dict[tuple, list[dict]] = {f: [] for f in FAIXAS}
    for c in elegiveis:
        for faixa in FAIXAS:
            if faixa[0] <= c["razao_frequencia"] < faixa[1]:
                por_faixa[faixa].append(c)
                break
    for faixa, lista in por_faixa.items():
        # Ordem determinística: por moldura e depois por razão, para que a
        # seleção não dependa da ordem de iteração de dicionário.
        lista.sort(key=lambda c: (c["moldura"], c["razao_frequencia"]))

    escolhidos, usados_por_moldura = [], {}
    while len(escolhidos) < n:
        progrediu = False
        for faixa in FAIXAS:
            lista = por_faixa[faixa]
            if not lista or len(escolhidos) >= n:
                continue
            # dentro da faixa, prefere a moldura menos usada até agora
            lista.sort(key=lambda c: usados_por_moldura.get(c["moldura"], 0))
            escolha = lista.pop(0)
            usados_por_moldura[escolha["moldura"]] = usados_por_moldura.get(escolha["moldura"], 0) + 1
            escolhidos.append(escolha)
            progrediu = True
        if not progrediu:
            break
    return escolhidos


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=54,
                    help="pares a propor (padrão: 54, que leva o grupo de 26 a 80)")
    ap.add_argument("--max-diferenca-subtokens", type=int, default=MAX_DIFERENCA_SUBTOKENS,
                    help=f"diferença máxima de subtokens entre os lados (padrão: {MAX_DIFERENCA_SUBTOKENS})")
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    args = ap.parse_args()

    tok = _tokenizador()
    cands = candidatos(tok)
    escolhidos = selecionar(cands, args.n, args.max_diferenca_subtokens)

    print(f"{len(cands)} candidato(s) possível(is); {len(escolhidos)} proposto(s).")
    print()
    print(f"{'moldura':10} {'razão':>8} {'sub':>5}  enunciados")
    for c in escolhidos:
        print(f"{c['moldura']:10} {c['razao_frequencia']:>8.2f} "
              f"{c['subtokens_a']}/{c['subtokens_b']:<3}  {c['lado_a']}  ||  {c['lado_b']}")

    from collections import Counter
    faixas = Counter()
    for c in escolhidos:
        for f in FAIXAS:
            if f[0] <= c["razao_frequencia"] < f[1]:
                faixas[f"{f[0]:g}–{f[1]:g}" if f[1] < 1e9 else f"> {f[0]:g}"] += 1
                break
    print()
    print("dispersão por faixa de razão de frequência:", dict(faixas))
    print("molduras:", dict(Counter(c["moldura"] for c in escolhidos)))

    if len(escolhidos) < args.n:
        print(f"\nATENÇÃO: só {len(escolhidos)} de {args.n} puderam ser propostos "
              "sem violar a restrição de subtokens. Amplie as listas de itens em "
              "MOLDURAS ou afrouxe --max-diferenca-subtokens, declarando a mudança.")

    Path(args.saida).write_text(
        json.dumps({"_meta": {"gerado_por": "propor_calibracao.py",
                              "max_diferenca_subtokens": args.max_diferenca_subtokens,
                              "n_propostos": len(escolhidos),
                              "revisao": "pendente"},
                    "pares": escolhidos}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nGravado em {args.saida}. Revisão humana antes de incorporar ao conjunto.")


if __name__ == "__main__":
    main()
