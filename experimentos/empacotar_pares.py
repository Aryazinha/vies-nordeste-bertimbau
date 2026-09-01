"""
empacotar_pares.py

Encerra o item 14 do registro de `docs/dataset-spec.md`: o conjunto de pares
mínimos não tinha formato de publicação. Até 01/09/2026 ele existia apenas
como listas embutidas no código de três módulos — `teste_sensibilidade.py`,
`teste_construcional.py` e `teste_explicito.py` —, de modo que quem baixasse o
repositório recebia scripts, e não um conjunto de dados.

## O que este script produz

Um arquivo canônico único, `experimentos/resultados/dados/pares_minimos.json`,
com **um registro por par**. Decisões de formato tomadas pela equipe em
01/09/2026:

- **JSON como formato canônico**, e não CSV, porque um par tem estrutura
  aninhada — lista de atributos com extensão em subtokens, anotações de vários
  juízes — que não cabe numa linha de planilha. O formato tabular dos
  precedentes sai de `converter_pares.py`, sob demanda, em vez de ser um
  segundo artefato publicado a manter em sincronia.
- **Os pares de resultado nulo entram no conjunto.** O nulo bem controlado das
  quatro famílias de sinalização dialetal é um dos resultados do trabalho
  (`docs/achados_para_o_artigo.md`), e sem os pares ninguém pode verificá-lo.

## Por que o campo de subtokens não é enfeite

Cada par carrega, por moldura, a extensão em subtokens de cada atributo com
que foi medido. Foi exatamente uma diferença de extensão que produziu o viés
aparente de +0,195 no eixo de caráter, desfeito no passo 5.5 ao se restringir
a medição a atributos de token único. Publicar o conjunto sem essa informação
convidaria o próximo trabalho a repetir o erro sem meio de perceber.

## Sobre a duplicação com o código

A fonte da verdade continua sendo o código, e este script deriva o arquivo
dela. Para que os dois não divirjam em silêncio — o padrão de falha silenciosa
da seção 5-A de `docs/pendencias.md` —, o modo `--verificar` refaz a derivação
e falha se o arquivo em disco não corresponder ao que o código define.

Uso:
    python empacotar_pares.py              # gera o arquivo
    python empacotar_pares.py --verificar  # falha se o arquivo divergir do código
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from teste_sensibilidade import ATRIBUTOS, CONDICOES, MOLDURAS
from teste_explicito import CONDICOES_5_1, CONDICOES_NOVAS, NOMES, CALIBRACAO, TESTE

DADOS = Path(__file__).resolve().parent / "resultados" / "dados"
SAIDA = DADOS / "pares_minimos.json"
BRUTO = DADOS / "explicito_bruto.json"
PARES_MEDIDOS = DADOS / "explicito_pares.json"

VERSAO_ESQUEMA = "1.0"

# Papel de cada condição no desenho. Sem isto, quem receber o conjunto não tem
# como saber que `controle_raridade` existe para separar raridade de região.
PAPEL = {
    "controle_neutro": "piso: os dois lados diferem em item trivial, sem carga regional",
    "controle_frequencia": "calibração: pares não regionais usados para ajustar a reta da frequência",
    "calibracao_extra": "calibração: ampliação do conjunto de ajuste da reta",
    "controle_raridade": "controle: item raro não regional, para separar raridade de procedência",
    "controle_explicito": "controle: menção explícita não regional",
    "controle_conteudo": "controle positivo: diferença de conteúdo que o modelo deve detectar",
    "dialeto_A": "teste: sinalização dialetal morfossintática (imperativo e negação)",
    "dialeto_B": "teste: sinalização dialetal lexical",
    "dialeto_C": "teste: feixe de marcadores combinados",
    "dialeto_D": "teste: sinalização dialetal construcional, de frequência atestada",
    "explicito_regiao": "teste: menção explícita à macrorregião",
    "explicito_gentilico": "teste: menção explícita por gentílico de estado (rótulo de pessoa)",
    "explicito_toponimo": "teste: menção explícita por topônimo (rótulo de lugar)",
}


def condicoes_do_codigo() -> dict:
    todas = dict(CONDICOES)
    todas.update(CONDICOES_5_1)
    todas.update(CONDICOES_NOVAS)
    return todas


def subtokens_por_moldura(bruto: list[dict]) -> dict:
    """
    Extensão em subtokens de cada atributo, por moldura, tal como o modelo
    segmentou. Vem da medição já registrada, e não de nova tokenização, para
    que o conjunto publicado descreva o que de fato foi medido.
    """
    visto: dict[str, dict[str, int]] = defaultdict(dict)
    for r in bruto:
        visto[r["moldura"]][r["atributo"]] = r["n_tokens"]
    return visto


def medicoes_por_par(pares_medidos: list[dict]) -> dict:
    return {(p["condicao"], p["par"]): p for p in pares_medidos}


def construir() -> dict:
    todas = condicoes_do_codigo()
    bruto = json.loads(BRUTO.read_text(encoding="utf-8"))
    medidos = medicoes_por_par(json.loads(PARES_MEDIDOS.read_text(encoding="utf-8")))
    subtok = subtokens_por_moldura(bruto)

    registros = []
    for condicao, pares in todas.items():
        for i, (lado_a, lado_b) in enumerate(pares):
            m = medidos.get((condicao, i))
            registros.append({
                "id": f"{condicao}-{i:02d}",
                "condicao": condicao,
                "papel": PAPEL.get(condicao, ""),
                "grupo": ("calibracao" if condicao in CALIBRACAO
                          else "teste" if condicao in TESTE else "outro"),
                "lado_a": lado_a,
                "lado_b": lado_b,
                # O par não é atribuído a um estado: as condições agrupam por
                # família de marcador, não por unidade da federação. Onde a
                # atribuição existe, ela está em docs/pares_minimos_v1.md, e não
                # foi transposta para cá para não inventar vínculo.
                "estado_alvo": None,
                "medicao": None if not m else {
                    "n_medicoes": m["n"],
                    "mediana_d_pll": m["mediana"],
                    "razao_frequencia": m.get("razao"),
                    "previsto_pela_reta": m.get("previsto"),
                    "residuo": m.get("residuo"),
                },
                # Filtro 1 nunca foi aplicado e nenhum juiz foi consultado
                # (docs/achados_para_o_artigo.md §3.3). O campo existe vazio
                # para que a lacuna fique visível no próprio dado.
                "anotacoes_juizes": [],
            })

    return {
        "_meta": {
            "versao_esquema": VERSAO_ESQUEMA,
            "gerado_por": "experimentos/empacotar_pares.py",
            "licenca": "CC BY 4.0 (ver LICENSE-DATA.md)",
            "modelo_medido": "neuralmind/bert-base-portuguese-cased",
            "n_pares": len(registros),
            "n_condicoes": len(todas),
            "molduras": MOLDURAS,
            "atributos_por_moldura": ATRIBUTOS,
            "subtokens_por_moldura": subtok,
            "nomes_de_condicao": NOMES,
            "advertencias": [
                "Os pares de resultado nulo integram o conjunto por decisão da equipe: "
                "o nulo controlado das quatro famílias de sinalização dialetal é um dos "
                "resultados do trabalho, e sem os pares ele não é verificável.",
                "A extensão em subtokens está publicada porque foi uma diferença de "
                "extensão que produziu o viés aparente de +0,195 no eixo de caráter, "
                "desfeito ao se restringir a medição a atributos de token único. "
                "Qualquer conjunto derivado deve balancear subtokens entre os polos.",
                "Nenhum item foi validado por juízes falantes nativos: o campo "
                "'anotacoes_juizes' está vazio em todos os pares, e não por omissão "
                "do empacotamento.",
                "O eixo de prestígio ocupacional (moldura T2) não tem medição válida "
                "por PLL, e exige AUL. Ver docs/achados_para_o_artigo.md.",
            ],
        },
        "pares": registros,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verificar", action="store_true",
                    help="Não escreve; falha se o arquivo em disco divergir do código")
    args = ap.parse_args()

    pacote = construir()
    texto = json.dumps(pacote, ensure_ascii=False, indent=2) + "\n"

    if args.verificar:
        if not SAIDA.exists():
            raise SystemExit(f"{SAIDA} não existe. Rode sem --verificar para gerar.")
        if SAIDA.read_text(encoding="utf-8") != texto:
            raise SystemExit(
                f"{SAIDA.name} DIVERGE do que o código define. O conjunto publicado "
                "deixou de corresponder ao instrumento medido — regenere e confira "
                "o que mudou antes de publicar.")
        print(f"{SAIDA.name} confere com o código: {pacote['_meta']['n_pares']} pares.")
        return

    SAIDA.write_text(texto, encoding="utf-8")
    m = pacote["_meta"]
    print(f"{m['n_pares']} pares em {m['n_condicoes']} condições gravados em {SAIDA}.")
    sem_medicao = sum(1 for p in pacote["pares"] if p["medicao"] is None)
    if sem_medicao:
        print(f"AVISO: {sem_medicao} par(es) sem medição associada.")
    print("Nenhum par tem anotação de juiz — o Filtro 1 nunca foi aplicado.")


if __name__ == "__main__":
    main()
