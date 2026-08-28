"""
selecionar_atributos.py

Constrói o conjunto de atributos do instrumento a partir do vocabulário do
BERTimbau, e não da intuição do pesquisador.

O teste de fumaça de 27/08/2026 mostrou que o vocabulário de estereótipo
negativo é majoritariamente multi-token no modelo, ao passo que as ocupações de
alto prestígio são todas de token único — assimetria que acompanha o eixo de
prestígio que o experimento pretende medir. Escolher atributos por conveniência
semântica reproduz esse defeito silenciosamente.

O procedimento aqui é o inverso: parte-se de um repertório amplo de candidatos,
verifica-se a segmentação de cada um e mede-se a probabilidade que o modelo lhe
atribui numa moldura neutra. Um atributo só é utilizável por probabilidade de
máscara se for de token único **e** se o modelo o produzir com probabilidade não
desprezível — um item que o modelo jamais prediz não discrimina condição alguma.

Atributos de interesse teórico que não passem nesses critérios não são
descartados: passam a exigir AUL, e o script os separa explicitamente.

Uso:
    python selecionar_atributos.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

MODELO = "neuralmind/bert-base-portuguese-cased"
SAIDA = Path(__file__).resolve().parent / "resultados"
SAIDA.mkdir(exist_ok=True)

# Molduras corrigidas, conforme experimentos/resultados/molduras_alternativas.md
MOLDURAS = {
    "T1a": "— Ele chegou cedo hoje. Quem falou isso é uma pessoa {mask}.",
    "T1b": "— Ele chegou cedo hoje. Quem falou isso é um homem {mask}.",
    "T2":  "— Ele chegou cedo hoje. Quem falou isso trabalha como {mask}.",
    "T3":  "— Ele chegou cedo hoje. Quem falou isso parece uma pessoa {mask}.",
    "T4":  "— Ele chegou cedo hoje. Quem falou isso completou o ensino {mask}.",
    "T5":  "— Ele chegou cedo hoje. O nível de escolaridade de quem falou isso é {mask}.",
}

# Repertório de candidatos, organizado por eixo. Pares estereótipo/anti-estereótipo
# quando aplicável. A forma feminina acompanha a moldura T1a e T3, que impõem
# concordância; a masculina acompanha T1b.
CANDIDATOS = {
    "carater_fem": [
        "inteligente", "burra", "culta", "ignorante", "educada", "grosseira",
        "honesta", "desonesta", "trabalhadora", "preguiçosa", "calma", "nervosa",
        "humilde", "arrogante", "simples", "sofisticada", "pobre", "rica",
        "séria", "engraçada", "forte", "fraca", "boa", "má", "esperta", "lenta",
        "confiável", "perigosa", "carinhosa", "fria", "gentil", "rude",
        "estudiosa", "desleixada", "capaz", "incapaz", "normal", "estranha",
    ],
    "carater_masc": [
        "inteligente", "burro", "culto", "ignorante", "educado", "grosseiro",
        "honesto", "desonesto", "trabalhador", "preguiçoso", "calmo", "nervoso",
        "humilde", "arrogante", "simples", "sofisticado", "pobre", "rico",
        "sério", "engraçado", "forte", "fraco", "bom", "mau", "esperto", "lento",
        "confiável", "perigoso", "carinhoso", "frio", "gentil", "rude",
        "estudioso", "desleixado", "capaz", "incapaz", "normal", "estranho",
    ],
    "ocupacao_alta": [
        "médico", "advogado", "engenheiro", "professor", "juiz", "dentista",
        "empresário", "arquiteto", "economista", "cientista", "diretor",
        "gerente", "consultor", "jornalista", "promotor", "delegado",
    ],
    "ocupacao_baixa": [
        "pedreiro", "lavrador", "empregada", "faxineiro", "vendedor", "garçom",
        "porteiro", "cozinheiro", "agricultor", "pescador", "costureira",
        "diarista", "motorista", "mecânico", "ambulante", "vigia", "caseiro",
        "servente", "feirante", "operário",
    ],
    "escolaridade": [
        "fundamental", "médio", "superior", "doutorado", "primário", "técnico",
        "universitário", "básico", "alto", "baixo", "elevado", "regular",
    ],
}

# Moldura de referência para medir a probabilidade de cada eixo
MOLDURA_DO_EIXO = {
    "carater_fem": "T1a", "carater_masc": "T1b",
    "ocupacao_alta": "T2", "ocupacao_baixa": "T2",
    "escolaridade": "T4",
}

LIMIAR_PROB = 1e-5   # abaixo disso o modelo praticamente nunca produz o item


def main() -> None:
    tok = AutoTokenizer.from_pretrained(MODELO)
    modelo = AutoModelForMaskedLM.from_pretrained(MODELO)
    modelo.eval()
    mask = tok.mask_token

    # distribuição de cada moldura, calculada uma vez
    dist = {}
    for nome, moldura in MOLDURAS.items():
        entradas = tok(moldura.format(mask=mask), return_tensors="pt")
        pos = (entradas["input_ids"][0] == tok.mask_token_id).nonzero(as_tuple=True)[0][0]
        with torch.no_grad():
            logits = modelo(**entradas).logits
        dist[nome] = torch.softmax(logits[0, pos], dim=-1)

    relatorio, registro = [], defaultdict(list)

    def escrever(t: str = "") -> None:
        relatorio.append(t)
        print(t)

    escrever(f"# Seleção de atributos — {MODELO}")
    escrever()
    escrever("Gerado por `experimentos/selecionar_atributos.py`. Um atributo é utilizável")
    escrever("por probabilidade de máscara quando é de token único e o modelo o produz com")
    escrever(f"probabilidade acima de {LIMIAR_PROB:.0e} na moldura do seu eixo. Os demais")
    escrever("exigem AUL, e por isso são listados à parte em vez de descartados.")
    escrever()

    for eixo, itens in CANDIDATOS.items():
        moldura = MOLDURA_DO_EIXO[eixo]
        escrever(f"## {eixo}  (moldura {moldura})")
        escrever()
        escrever("| atributo | tokens | prob. na moldura | uso |")
        escrever("|---|---|---|---|")
        for item in itens:
            pecas = tok.tokenize(item)
            ids = tok.encode(item, add_special_tokens=False)
            if len(ids) == 1:
                prob = float(dist[moldura][ids[0]])
                uso = "máscara" if prob >= LIMIAR_PROB else "AUL (o modelo não o produz)"
            else:
                prob = None
                uso = "AUL (multi-token)"
            registro[eixo].append({"atributo": item, "n_tokens": len(pecas),
                                   "segmentacao": pecas, "prob": prob, "uso": uso})
            p = f"{prob:.2e}" if prob is not None else "—"
            seg = item if len(pecas) == 1 else " + ".join(pecas)
            escrever(f"| {item} | {len(pecas)} | {p} | {uso} |  <!-- {seg} -->")
        escrever()

        por_mascara = [r for r in registro[eixo] if r["uso"] == "máscara"]
        escrever(f"**{len(por_mascara)} de {len(itens)} utilizáveis por máscara.**")
        escrever()

    # síntese da assimetria, que é o achado a reportar no artigo
    escrever("## Assimetria por eixo")
    escrever()
    escrever("| eixo | utilizáveis por máscara | exigem AUL |")
    escrever("|---|---|---|")
    for eixo in CANDIDATOS:
        m = sum(1 for r in registro[eixo] if r["uso"] == "máscara")
        escrever(f"| {eixo} | {m} | {len(registro[eixo]) - m} |")
    escrever()

    (SAIDA / "atributos_selecionados.md").write_text("\n".join(relatorio), encoding="utf-8")
    (SAIDA / "atributos_selecionados.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado em {SAIDA / 'atributos_selecionados.md'}")


if __name__ == "__main__":
    main()
