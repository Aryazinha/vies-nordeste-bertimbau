"""
balanco_participacao.py

Fecha a seção 1.1 de `docs/pendencias.md` do lado do instrumento: mede quanto
do corpus, por estado, é **fala de ouvinte participando** — o registro menos
monitorado do material e, por isso, o mais capaz de desequilibrar a comparação
entre grupos sem que ninguém perceba.

## Por que isto precisa ser medido, e não apenas balanceado por canal

Fala de ouvinte ao telefone é fala não monitorada. Os marcadores regionais que
o projeto investiga — negação pós-verbal, imperativo indicativo — são mais
frequentes em fala informal. Se o grupo nordestino tiver esse tipo de fala e o
grupo de controle não, o contraste medido entre as regiões fica inflado **na
direção que favorece a hipótese do projeto**, que é a pior direção possível
para um viés passar despercebido.

Ter um canal com o formato em cada estado não resolve nada: quarenta minutos
de fala de ouvinte na Bahia contra quatro em São Paulo produzem o mesmo
desequilíbrio, agora escondido atrás de uma contagem de canais simétrica. O
que precisa ser equilibrado — ou descontado na análise — é o **volume por
estado**, e volume só se conta arquivo a arquivo.

## Os dois campos, e por que são dois

- `canal_tem_participacao_ouvinte` vem de `fontes.json` e é fato do canal.
  Custa nada e serve para uma coisa só: dizer ao curador quais arquivos vale a
  pena ouvir.
- `participacao_ouvinte` é fato do arquivo e só se estabelece ouvindo. Nasce
  `nao_verificado` e assim permanece até que alguém o preencha.

Enquanto o segundo campo não for preenchido, este relatório mostra zero em
todos os estados — e isso é resposta correta, não falha: significa que a
quantidade é desconhecida, e não que seja nula.

Uso:
    python balanco_participacao.py                     # relatório
    python balanco_participacao.py --marcar-canal      # preenche o campo herdado do canal
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from config import BASE_DIR, ESTADOS_NORDESTE, ESTADOS_CONTROLE

METADADOS = BASE_DIR / "metadados.json"
FONTES = Path(__file__).resolve().parent / "fontes.json"

# Acima desta razão entre os grupos, o desequilíbrio deixa de ser ruído e passa
# a exigir conduta — equilibrar a coleta ou descontar na análise. Não é limiar
# consagrado: é ponto de atenção, e está aqui para ser discutido, não obedecido.
RAZAO_DE_ALERTA = 1.5


def marca_por_canal() -> dict[str, str]:
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))
    return {c["canal"]: c.get("participacao_ouvinte", "nao_verificado")
            for uf, lista in fontes.items() if uf != "_meta" for c in lista}


def carregar() -> list[dict]:
    if not METADADOS.exists():
        raise SystemExit(f"{METADADOS} não existe — nada coletado ainda.")
    return json.loads(METADADOS.read_text(encoding="utf-8"))


def marcar_canal(registros: list[dict]) -> int:
    """Preenche retroativamente o campo herdado do canal. Não toca no do arquivo."""
    marcas = marca_por_canal()
    n = 0
    for r in registros:
        atual = r.get("canal_tem_participacao_ouvinte")
        novo = marcas.get(r["canal"], "nao_verificado")
        if atual != novo:
            r["canal_tem_participacao_ouvinte"] = novo
            n += 1
        r.setdefault("participacao_ouvinte", "nao_verificado")
    return n


def relatar(registros: list[dict]) -> None:
    por_estado = defaultdict(lambda: {"total_s": 0.0, "ouvinte_s": 0.0,
                                      "candidatos": 0, "arquivos": 0})
    for r in registros:
        uf = r["estado_alvo"]
        dur = float(r.get("duracao_coletada_s") or r.get("duracao_s") or 0)
        e = por_estado[uf]
        e["arquivos"] += 1
        e["total_s"] += dur
        if r.get("participacao_ouvinte") == "sim":
            e["ouvinte_s"] += dur
        if r.get("canal_tem_participacao_ouvinte") == "sim":
            e["candidatos"] += 1

    print("## Volume de fala de ouvinte por estado\n")
    print("| UF | Arquivos | Total | Fala de ouvinte | % | Arquivos a ouvir |")
    print("|---|---|---|---|---|---|")
    for uf in ESTADOS_NORDESTE + ESTADOS_CONTROLE:
        e = por_estado.get(uf)
        if not e:
            print(f"| {uf} | 0 | — | — | — | — |")
            continue
        pct = 100 * e["ouvinte_s"] / e["total_s"] if e["total_s"] else 0
        print(f"| {uf} | {e['arquivos']} | {e['total_s']/60:.0f} min | "
              f"{e['ouvinte_s']/60:.0f} min | {pct:.1f}% | {e['candidatos']} |")

    ne = sum(por_estado[uf]["ouvinte_s"] for uf in ESTADOS_NORDESTE if uf in por_estado)
    se = sum(por_estado[uf]["ouvinte_s"] for uf in ESTADOS_CONTROLE if uf in por_estado)
    ne_tot = sum(por_estado[uf]["total_s"] for uf in ESTADOS_NORDESTE if uf in por_estado)
    se_tot = sum(por_estado[uf]["total_s"] for uf in ESTADOS_CONTROLE if uf in por_estado)

    print("\n## Comparação entre os grupos\n")
    p_ne = 100 * ne / ne_tot if ne_tot else 0
    p_se = 100 * se / se_tot if se_tot else 0
    print(f"- Nordeste: {ne/60:.0f} min de fala de ouvinte em {ne_tot/60:.0f} min ({p_ne:.1f}%)")
    print(f"- Controle: {se/60:.0f} min de fala de ouvinte em {se_tot/60:.0f} min ({p_se:.1f}%)")

    a_ouvir = sum(e["candidatos"] for e in por_estado.values())
    verificados = sum(1 for r in registros if r.get("participacao_ouvinte") != "nao_verificado")

    if verificados == 0:
        print(f"\n**Nenhum arquivo foi verificado por escuta.** Os zeros acima significam "
              f"quantidade desconhecida, não quantidade nula. Há {a_ouvir} arquivo(s) de "
              f"canal com o formato, que são por onde a verificação deve começar.")
        return

    if p_se == 0 and p_ne > 0:
        print(f"\n**ALERTA:** o grupo nordestino tem fala de ouvinte e o de controle não tem "
              f"nenhuma. O contraste regional medido está inflado na direção da hipótese do "
              f"projeto. Equilibrar a coleta ou descontar esses trechos na análise.")
    elif p_se and p_ne / p_se > RAZAO_DE_ALERTA:
        print(f"\n**ALERTA:** o Nordeste tem {p_ne/p_se:.1f}× mais fala de ouvinte, "
              f"proporcionalmente, que o grupo de controle.")
    else:
        print(f"\nProporções compatíveis entre os grupos ({verificados} arquivo(s) verificado(s)).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--marcar-canal", action="store_true",
                    help="Preenche retroativamente o campo herdado do canal")
    args = ap.parse_args()

    registros = carregar()
    if args.marcar_canal:
        n = marcar_canal(registros)
        METADADOS.write_text(json.dumps(registros, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"{n} registro(s) atualizado(s) em {METADADOS.name}.\n")

    relatar(registros)


if __name__ == "__main__":
    main()
