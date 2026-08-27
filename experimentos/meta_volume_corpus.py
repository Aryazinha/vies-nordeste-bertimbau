"""
meta_volume_corpus.py

Deriva a meta de volume do corpus de áudio (passo 4.2 do roadmap) a partir do
que o Filtro 2 do protocolo de validação exige, em vez de arbitrá-la.

O Filtro 2 promove um marcador candidato a confirmado se ele ocorrer em fala
espontânea do estado correspondente. Para variantes raras, isso impõe uma
condição estatística: o corpus precisa ser grande o bastante para que a
AUSÊNCIA de ocorrências seja informativa. Do contrário o filtro reprovaria o
marcador por insuficiência amostral, e não por inadequação — erro que
invalidaria a etapa de validação inteira.

O caso dimensionante é a negação pós-verbal (marcador M2), cuja produtividade
máxima observada na meta-análise de Santos e Vitório (2025) é de 5,6%.

Todos os parâmetros de fala são declarados como suposições explícitas e devem
ser recalibrados com as primeiras horas transcritas do piloto.
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Suposições sobre a fala. A recalibrar com o piloto.
# ---------------------------------------------------------------------------
PALAVRAS_POR_MINUTO = 130      # fala espontânea; ordem de grandeza usual
PALAVRAS_POR_ORACAO = 9        # oração como unidade de contexto de negação
PROP_ORACOES_NEGADAS = 0.05    # proporção de orações com negação sentencial

# Produtividade da variante-alvo entre os contextos de negação.
P_POS_VERBAL = 0.056           # Santos e Vitório (2025), máximo observado

# Fração do áudio bruto que sobra como fala do locutor-alvo, após descontar
# vinheta, música, silêncio e turnos de locutores de outra variedade
# (repórter, apresentador). Estimativas conservadoras por camada.
RENDIMENTO = {
    "entrevista_vox_pop": 0.35,
    "podcast_radio_tv_regional": 0.60,
    "vlog_amador": 0.70,
}

# Composição por camada, conforme seção 1.4.3 do CLAUDE.md.
COMPOSICAO = {
    "entrevista_vox_pop": 0.35,
    "podcast_radio_tv_regional": 0.30,
    "vlog_amador": 0.35,
}

ESTADOS = ["PB", "PE", "CE", "BA", "SP", "RJ"]


def contextos_por_hora() -> float:
    palavras = PALAVRAS_POR_MINUTO * 60
    oracoes = palavras / PALAVRAS_POR_ORACAO
    return oracoes * PROP_ORACOES_NEGADAS


def n_para_detectar(p: float, confianca: float) -> int:
    """Contextos necessários para observar ao menos uma ocorrência com dada confiança."""
    return math.ceil(math.log(1 - confianca) / math.log(1 - p))


def n_para_k_esperado(p: float, k: int) -> int:
    """Contextos necessários para que o número esperado de ocorrências seja k."""
    return math.ceil(k / p)


def prob_zero(p: float, n: int) -> float:
    return (1 - p) ** n


def main() -> None:
    ctx_h = contextos_por_hora()
    print("# Meta de volume do corpus de áudio — passo 4.2")
    print()
    print("Derivada do requisito estatístico do Filtro 2. Gerado por "
          "`experimentos/meta_volume_corpus.py`.")
    print()

    print("## Suposições declaradas")
    print()
    print("| Parâmetro | Valor | Origem |")
    print("|---|---|---|")
    print(f"| Palavras por minuto | {PALAVRAS_POR_MINUTO} | suposição, a recalibrar com o piloto |")
    print(f"| Palavras por oração | {PALAVRAS_POR_ORACAO} | suposição, a recalibrar com o piloto |")
    print(f"| Proporção de orações negadas | {PROP_ORACOES_NEGADAS:.0%} | suposição, a recalibrar com o piloto |")
    print(f"| Produtividade da negação pós-verbal | {P_POS_VERBAL:.1%} | Santos e Vitório (2025), máximo observado |")
    print()
    print(f"Disso resulta **{ctx_h:.0f} contextos de negação por hora** de fala do locutor-alvo, "
          f"e portanto {ctx_h * P_POS_VERBAL:.1f} ocorrência(s) esperada(s) da variante por hora.")
    print()

    print("## Volume necessário por estado, segundo o critério adotado")
    print()
    print("| Critério de decisão do Filtro 2 | Contextos | Horas de fala-alvo |")
    print("|---|---|---|")
    for rot, n in [
        ("Detectar ao menos 1 ocorrência com 90% de confiança", n_para_detectar(P_POS_VERBAL, 0.90)),
        ("Detectar ao menos 1 ocorrência com 95% de confiança", n_para_detectar(P_POS_VERBAL, 0.95)),
        ("Detectar ao menos 1 ocorrência com 99% de confiança", n_para_detectar(P_POS_VERBAL, 0.99)),
        ("Esperar 5 ocorrências (estimativa de taxa, não só presença)", n_para_k_esperado(P_POS_VERBAL, 5)),
        ("Esperar 10 ocorrências (comparação entre estados)", n_para_k_esperado(P_POS_VERBAL, 10)),
    ]:
        print(f"| {rot} | {n} | **{n / ctx_h:.1f} h** |")
    print()

    n_rec = n_para_k_esperado(P_POS_VERBAL, 10)
    h_alvo = n_rec / ctx_h
    print(f"**Critério recomendado:** esperar 10 ocorrências, isto é, "
          f"**{h_alvo:.1f} h de fala do locutor-alvo por estado**. Justificativa: presença ou "
          f"ausência é suficiente para promover um marcador, mas a comparação entre Nordeste e "
          f"grupo de controle exige estimar a taxa em cada grupo, não apenas constatar ocorrência. "
          f"Com esse volume, a probabilidade de zero ocorrências, se a variante de fato tiver a "
          f"produtividade suposta, é de {prob_zero(P_POS_VERBAL, n_rec):.4%} — a ausência passa a "
          f"ser evidência, que é a condição para o Filtro 2 significar alguma coisa.")
    print()

    print("## Conversão para áudio bruto a coletar")
    print()
    print("Fala do locutor-alvo é menos que áudio gravado: descontam-se vinheta, música, "
          "silêncio e turnos de locutores de outra variedade. Os rendimentos abaixo são "
          "conservadores e devem ser medidos na verificação manual do piloto.")
    print()
    print("| Camada | Composição | Rendimento | Fala-alvo por estado | Áudio bruto por estado |")
    print("|---|---|---|---|---|")
    total_bruto = 0.0
    for camada, frac in COMPOSICAO.items():
        alvo = h_alvo * frac
        bruto = alvo / RENDIMENTO[camada]
        total_bruto += bruto
        print(f"| `{camada}` | {frac:.0%} | {RENDIMENTO[camada]:.0%} | {alvo:.1f} h | {bruto:.1f} h |")
    print(f"| **Total** | 100% | — | **{h_alvo:.1f} h** | **{total_bruto:.1f} h** |")
    print()
    print(f"Para os {len(ESTADOS)} estados ({', '.join(ESTADOS)}): "
          f"**{total_bruto * len(ESTADOS):.0f} h de áudio bruto**, "
          f"{h_alvo * len(ESTADOS):.0f} h de fala-alvo.")
    print()

    print("## Consequência para o processamento")
    print()
    print(f"Transcrever {total_bruto * len(ESTADOS):.0f} h com `large-v3` é inviável em CPU. "
          "Em GPU, o `faster-whisper` opera bem acima do tempo real, o que põe a transcrição "
          "na ordem de poucas horas de máquina. A coleta deve, portanto, ser planejada para "
          "ambiente com GPU desde o início, e não migrada para lá depois.")
    print()
    print("## Amostra de verificação manual")
    print()
    print("Independente do volume total, o cálculo de WER e DER exige transcrição manual de "
          "referência. Recomenda-se 20 minutos por estado, estratificados entre as camadas — "
          f"{20 * len(ESTADOS) / 60:.0f} h de transcrição manual ao todo. É o suficiente para "
          "estimar WER por variedade, que é a ameaça à validade registrada na Parte 3 do "
          "`CLAUDE.md` e um resultado publicável por si só.")


if __name__ == "__main__":
    main()
