"""
meta_pares_minimos.py — tamanho-alvo do conjunto de pares mínimos

Fecha o item 13 do registro de pendentes de `docs/dataset-spec.md`, que registrava
que o conjunto de pares mínimos não tinha meta **nem critério que a produzisse** —
ao contrário do corpus de áudio, cuja meta saiu de `meta_volume_corpus.py`.

## Por que o critério mudou de forma

Até 29/08/2026 o critério natural seria "quantos pares para detectar o efeito
observado". O passo 5.5 tornou essa formulação inaplicável: não há efeito de
valência a detectar. O único candidato — viés de caráter de +0,1952 na condição
de macrorregião — dissolveu-se ao se controlar o artefato de tokenização, caindo
para +0,0309 justamente quando o poder do teste aumentou.

O critério passa, portanto, a ser o mesmo que produziu a meta do corpus de áudio,
aplicado ao outro conjunto: **quantos pares para que a ausência de efeito seja
informativa**. Um nulo obtido com poder insuficiente não distingue "não há viés"
de "não olhamos direito", e é justamente essa distinção que o artigo precisa
sustentar.

## O insumo, e ele é decisão e não medição

A conta exige um número que nenhuma medição fornece: **o menor efeito de viés que
se queira poder excluir**. É escolha da equipe, e foi tomada em 29/08/2026.

**Decisão registrada: 0,08 em unidade bruta de escore de viés**, o que corresponde
a cerca de 0,7 desvio-padrão do ruído entre pares. As três razões estão na seção
correspondente do relatório gerado.

## A restrição que a conta revelou

O grupo de referência não regional impõe um **teto** ao que é detectável,
independentemente de quantos pares de teste existam: sua própria incerteza não
desaparece. Com os 26 pares de referência atuais, nenhum efeito abaixo de 0,078
é detectável sob correção de multiplicidade, por mais pares de teste que se
acrescentem. Segue-se que o grupo de referência precisa crescer junto com as
condições de teste — exigência que não constava de nenhum plano anterior.

Uso:
    python meta_pares_minimos.py
"""

from __future__ import annotations

import math
import statistics
from pathlib import Path

SAIDA = Path(__file__).resolve().parent / "resultados"

# --------------------------------------------------------------------------
# Insumos medidos
# --------------------------------------------------------------------------
# Desvio-padrão dos escores de viés no grupo de referência não regional, eixo de
# caráter, apurado por `analise_valencia.py` sobre 26 pares.
DP_RUIDO = 0.1182
# Escore de viés do controle positivo — o par de conteúdo proposicional distinto.
CONTROLE_POSITIVO = 0.2352
# O artefato de tokenização que o passo 5.5 desmontou, antes do controle.
ARTEFATO = 0.1952

# --------------------------------------------------------------------------
# Decisão da equipe, 29/08/2026
# --------------------------------------------------------------------------
EFEITO_MINIMO = 0.08             # unidade bruta de escore de viés

PODER = 0.80
ALFA = 0.05
N_CONDICOES = 9                  # família corrigida por Holm no delineamento atual

REFERENCIA_ATUAL = 26
PARES_ATUAIS_POR_CONDICAO = 8


def _z(p: float) -> float:
    return statistics.NormalDist().inv_cdf(p)


def pares_necessarios(d: float, n_ref: int, alfa: float, poder: float = PODER):
    """Pares de teste para atingir `poder`, com grupo de referência de `n_ref`."""
    alvo = (_z(1 - alfa) + _z(poder)) ** 2
    resto = d * d / alvo - 1 / n_ref
    return math.ceil(1 / resto) if resto > 0 else None


def piso_de_efeito(n_ref: int, alfa: float, poder: float = PODER) -> float:
    """Menor `d` detectável com `n_ref` de referência e pares de teste ilimitados."""
    alvo = (_z(1 - alfa) + _z(poder)) ** 2
    return math.sqrt(alvo / n_ref)


def main() -> None:
    d_alvo = EFEITO_MINIMO / DP_RUIDO
    alfa_holm = ALFA / N_CONDICOES

    L: list[str] = []
    add = L.append
    add("# Meta do conjunto de pares mínimos")
    add("")
    add("Gerado por `experimentos/meta_pares_minimos.py`. Fecha o item 13 do")
    add("registro de pendentes de `docs/dataset-spec.md`.")
    add("")
    add("## A pergunta que a meta responde")
    add("")
    add("Não é \"quantos pares para detectar o efeito\", porque o passo 5.5")
    add("estabeleceu que não há efeito de valência a detectar. É **quantos pares")
    add("para que a ausência de efeito seja informativa** — a mesma lógica de que")
    add("saiu a meta do corpus de áudio, aplicada ao outro conjunto.")
    add("")
    add("Um nulo obtido sem poder não distingue \"não há viés\" de \"não olhamos")
    add("direito\", e é essa distinção que a seção de Resultados precisa sustentar.")
    add("")
    add("## A decisão, e por que este número")
    add("")
    add(f"**Excluir efeitos de viés acima de {EFEITO_MINIMO:.2f}** em unidade bruta,")
    add(f"equivalente a d = {d_alvo:.2f} desvios-padrão do ruído entre pares")
    add(f"({DP_RUIDO:.4f}). Decidido pela equipe em 29/08/2026. Três razões:")
    add("")
    add(f"**1. É cerca de metade do artefato que o projeto desmontou.** O falso viés")
    add(f"de tokenização media {ARTEFATO:.4f} antes do controle")
    add("(`docs/achados_para_o_artigo.md`, item 1.1). Poder excluir "
        f"{EFEITO_MINIMO:.2f} autoriza a afirmação de que, houvesse viés com metade")
    add("da força daquele artefato, ele teria sido detectado. É afirmação verificável,")
    add("e não retórica de cautela.")
    add("")
    add(f"**2. Guarda margem de {CONTROLE_POSITIVO/EFEITO_MINIMO:.1f} vezes para o")
    add(f"controle positivo**, que produz {CONTROLE_POSITIVO:.4f}. Uma alegação de")
    add("poder é tão boa quanto a distância entre o que se quer excluir e o que o")
    add("instrumento comprovadamente detecta.")
    add("")
    add("**3. É alcançável.** Ver a tabela de custo abaixo: descer para 0,059 quase")
    add("quadruplica o trabalho por ganho argumentativo pequeno, e subir para 0,095")
    add("economiza pouco ao custo de só poder excluir viés grande.")
    add("")
    add("## Custo em pares, por poder de 80%")
    add("")
    add("| Excluir acima de | d | α = 0,05, ref. 50 | α = 0,05, ref. 80 | Holm, ref. 50 | Holm, ref. 80 |")
    add("|---|---|---|---|---|---|")
    for bruto in (0.059, 0.071, EFEITO_MINIMO, 0.095, 0.118):
        d = bruto / DP_RUIDO
        celulas = []
        for alfa in (ALFA, alfa_holm):
            for nref in (50, 80):
                k = pares_necessarios(d, nref, alfa)
                celulas.append(str(k) if k and k <= 400 else "inviável")
        marca = " **" if abs(bruto - EFEITO_MINIMO) < 1e-9 else " "
        rot = f"**{bruto:.3f}**" if marca == " **" else f"{bruto:.3f}"
        add(f"| {rot} | {d:.2f} | " + " | ".join(celulas) + " |")
    add("")
    add(f"**Meta adotada: {pares_necessarios(d_alvo, 80, alfa_holm)} pares por")
    add(f"condição e {80} pares no grupo de referência não regional.**")
    add(f"Hoje há {PARES_ATUAIS_POR_CONDICAO} e {REFERENCIA_ATUAL}, respectivamente.")
    add("")
    add("## A restrição que a conta revelou, e não constava de plano anterior")
    add("")
    add("O grupo de referência impõe um **teto** ao que é detectável, qualquer que")
    add("seja o número de pares de teste: sua própria incerteza não desaparece.")
    add("")
    add("| Pares de referência | Menor efeito detectável, α = 0,05 | Sob correção de Holm |")
    add("|---|---|---|")
    for nref in (REFERENCIA_ATUAL, 50, 80, 120):
        d1, d2 = piso_de_efeito(nref, ALFA), piso_de_efeito(nref, alfa_holm)
        marca = " (atual)" if nref == REFERENCIA_ATUAL else ""
        add(f"| {nref}{marca} | {d1*DP_RUIDO:.3f} | {d2*DP_RUIDO:.3f} |")
    add("")
    add(f"Com os {REFERENCIA_ATUAL} pares de referência atuais, **nenhum efeito abaixo")
    add(f"de {piso_de_efeito(REFERENCIA_ATUAL, alfa_holm)*DP_RUIDO:.3f} é detectável**")
    add("sob correção de multiplicidade, por mais pares de teste que se acrescentem.")
    add("O grupo de referência precisa crescer junto com as condições de teste, e")
    add("isso não constava de nenhum plano anterior do projeto.")
    add("")
    add("## Volume total implicado")
    add("")
    k = pares_necessarios(d_alvo, 80, alfa_holm)
    for n_cond in (4, 5):
        add(f"- Com {n_cond} condições de teste: {n_cond} × {k} + 80 = "
            f"**{n_cond * k + 80} pares** no conjunto.")
    add("")
    add("Para calibrar, o CrowS-Pairs distribui 1.508 pares. O conjunto proposto")
    add("fica em cerca de um sexto disso, com delineamento consideravelmente mais")
    add("controlado — calibração explícita da frequência, estatística por")
    add("conglomerado e balanceamento de subtokens.")
    add("")
    add("## Restrição de conteúdo, que precede o tamanho")
    add("")
    add("Qualquer conjunto futuro deve **balancear a extensão em subtokens entre os")
    add("polos do eixo medido**, sob pena de reproduzir o artefato que produziu viés")
    add("aparente a p = 0,049 e o desfez ao ser controlado. No eixo de prestígio")
    add("ocupacional o balanceamento é impossível neste modelo, e a medição exige")
    add("AUL (`docs/achados_para_o_artigo.md`, itens 1.1 e 1.20).")
    add("")
    add("## Ressalvas")
    add("")
    add("**A conta de poder é a de um teste t de duas amostras**, e o teste")
    add("efetivamente empregado é de permutação. A aproximação é adequada para")
    add("dimensionamento e tende a ser levemente conservadora.")
    add("")
    add(f"**O desvio-padrão do ruído vem de {REFERENCIA_ATUAL} pares** e é ele próprio")
    add("uma estimativa. Um grupo de referência maior a tornará mais precisa, e a")
    add("meta deve ser reconferida quando isso ocorrer.")
    add("")
    add("**A correção de Holm supõe nove condições**, que é o delineamento atual.")
    add("Reduzir o número de condições reduz o custo por condição.")

    texto = "\n".join(L)
    (SAIDA / "tabelas" / "meta_pares_minimos.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
