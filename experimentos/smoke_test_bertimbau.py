"""
smoke_test_bertimbau.py

Teste de fumaça do instrumento de sondagem, anterior a qualquer medição de viés.

Não mede viés. Responde a três perguntas de viabilidade sobre o instrumento
especificado em `docs/pares_minimos_v1.md`, todas as três capazes de invalidar
o desenho antes que se gaste tempo de juízes ou de coleta de áudio:

  Q1. As molduras de sondagem (T1-T4) produzem, no BERTimbau, distribuições
      interpretáveis — adjetivos, ocupações, itens de escolaridade — ou
      degeneram em pontuação e palavras funcionais?
  Q2. Os atributos candidatos são representados por um único token no
      vocabulário do modelo? Atributos multi-token exigem AUL (Kaneko e
      Bollegala, 2022) e não podem ser lidos por probabilidade de máscara única.
  Q3. O modelo responde ao *guise*, isto é, a distribuição sobre a lacuna muda
      entre a condição nordestina e a de controle? Indiferença total indicaria
      instrumento sem sensibilidade, não ausência de viés.

Uso:
    python experimentos/smoke_test_bertimbau.py

A saída é gravada em `experimentos/resultados/tabelas/smoke_test.md` e também impressa.
Requer `torch` e `transformers`; roda em CPU.
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

MODELO = "neuralmind/bert-base-portuguese-cased"
TOP_K = 12

RAIZ = Path(__file__).resolve().parent
SAIDA_DIR = RAIZ / "resultados"
# Saída de máquina fica em `resultados/tabelas/`; `resultados/` guarda apenas
# relatórios escritos à mão (ver nota em `teste_construcional.py`).
(SAIDA_DIR / "tabelas").mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Itens — espelham `docs/pares_minimos_v1.md` (v2), seção 5.
# `ne` é a realização nordestina; `sp` e `rj` são as realizações de controle.
# C1 consta como suspenso naquele documento (divergência sobre Fortaleza) e é
# incluído aqui apenas para o teste de viabilidade, não para medição.
# ---------------------------------------------------------------------------
ITENS = [
    # Bloco A — morfossintático puro
    {"id": "A1", "bloco": "A", "marcador": "M1",
     "ne": "Feche a porta, por favor.",
     "sp": "Fecha a porta, por favor.",
     "rj": "Fecha a porta, por favor."},
    {"id": "A2", "bloco": "A", "marcador": "M1",
     "ne": "Me diga que horas o ônibus passa.",
     "sp": "Me diz que horas o ônibus passa.",
     "rj": "Me diz que horas o ônibus passa."},
    {"id": "A3", "bloco": "A", "marcador": "M2",
     "ne": "Fui não, eu tava cansado.",
     "sp": "Não fui, eu tava cansado.",
     "rj": "Não fui, eu tava cansado."},
    {"id": "A4", "bloco": "A", "marcador": "M2",
     "ne": "Sei não, ninguém me avisou.",
     "sp": "Não sei, ninguém me avisou.",
     "rj": "Não sei, ninguém me avisou."},
    # Bloco B — lexical puro
    {"id": "B1", "bloco": "B", "marcador": "M3",
     "ne": "Isso aí ficou muito arretado.",
     "sp": "Isso aí ficou muito da hora.",
     "rj": "Isso aí ficou muito maneiro."},
    {"id": "B2", "bloco": "B", "marcador": "M3",
     "ne": "Tô aperreado com essa conta.",
     "sp": "Tô estressado com essa conta.",
     "rj": "Tô estressado com essa conta."},
    {"id": "B3", "bloco": "B", "marcador": "M3",
     "ne": "Oxe, e agora?",
     "sp": "Nossa, e agora?",
     "rj": "Caraca, e agora?"},
    {"id": "B4", "bloco": "B", "marcador": "M3",
     "ne": "Ele é muito avexado.",
     "sp": "Ele é muito apressado.",
     "rj": "Ele é muito apressado."},
    # Bloco C — feixe completo
    {"id": "C1", "bloco": "C", "marcador": "M1+M3", "estado": "CE", "suspenso": True,
     "ne": "Me traga a chave que eu esqueci lá, tô avexado.",
     "sp": "Me traz a chave que eu esqueci lá, tô com pressa.",
     "rj": "Me traz a chave que eu esqueci lá, tô com pressa."},
    {"id": "C2", "bloco": "C", "marcador": "M2+M3", "estado": "PB",
     "ne": "Vou não, hoje tô muito aperreado com o trabalho.",
     "sp": "Não vou, hoje tô muito estressado com o trabalho.",
     "rj": "Não vou, hoje tô muito estressado com o trabalho."},
    {"id": "C3", "bloco": "C", "marcador": "M1+M2+M3", "estado": "PE",
     "ne": "Chegou não, visse? Ligue pra ele depois.",
     "sp": "Não chegou, tá ligado? Liga pra ele depois.",
     "rj": "Não chegou, entendeu? Liga pra ele depois."},
    {"id": "C4", "bloco": "C", "marcador": "M1+M3", "estado": "BA",
     "ne": "Oxe, deixe isso aí que eu resolvo.",
     "sp": "Nossa, deixa isso aí que eu resolvo.",
     "rj": "Caraca, deixa isso aí que eu resolvo."},
]

# ---------------------------------------------------------------------------
# Molduras de sondagem — `docs/pares_minimos_v1.md`, seção 4.
# T1 aparece nas duas versões previstas (gênero controlado e gênero livre).
# ---------------------------------------------------------------------------
MOLDURAS = {
    "T1a": "— {enunciado} Quem falou isso é uma pessoa {mask}.",
    "T1b": "— {enunciado} Quem falou isso é {mask}.",
    "T2":  "— {enunciado} Quem falou isso trabalha como {mask}.",
    "T3":  "— {enunciado} Quem falou isso parece {mask}.",
    "T4":  "— {enunciado} Quem falou isso estudou até o {mask}.",
}

# ---------------------------------------------------------------------------
# Atributos candidatos — seção 4 do documento do instrumento, ainda não fechados.
# Checados aqui apenas quanto à segmentação (Q2).
# ---------------------------------------------------------------------------
ATRIBUTOS = {
    "carater_positivo": ["inteligente", "culta", "educada", "honesta", "trabalhadora"],
    "carater_negativo": ["burra", "ignorante", "grosseira", "desonesta", "preguiçosa"],
    "ocupacao_alta": ["médico", "advogado", "engenheiro", "professor", "juiz"],
    "ocupacao_baixa": ["pedreiro", "lavrador", "empregada", "faxineiro", "vendedor"],
    "escolaridade": ["fundamental", "médio", "superior", "doutorado"],
}


def carregar():
    tok = AutoTokenizer.from_pretrained(MODELO)
    modelo = AutoModelForMaskedLM.from_pretrained(MODELO)
    modelo.eval()
    return tok, modelo


def top_k_mascara(tok, modelo, texto: str, k: int = TOP_K):
    """Retorna [(token, probabilidade), ...] para a única lacuna do texto."""
    entradas = tok(texto, return_tensors="pt")
    posicoes = (entradas["input_ids"][0] == tok.mask_token_id).nonzero(as_tuple=True)[0]
    if len(posicoes) != 1:
        raise ValueError(f"Esperava exatamente uma lacuna, encontrei {len(posicoes)}: {texto}")

    with torch.no_grad():
        logits = modelo(**entradas).logits

    probs = torch.softmax(logits[0, posicoes[0]], dim=-1)
    valores, indices = probs.topk(k)
    return [(tok.decode([i]).strip(), float(v)) for v, i in zip(valores, indices)]


def prob_do_atributo(tok, modelo, texto: str, atributo: str) -> float | None:
    """
    Probabilidade atribuída a `atributo` na lacuna, quando ele é um único token.
    Retorna None para atributos multi-token — nesses casos a leitura exige AUL.
    """
    ids = tok.encode(atributo, add_special_tokens=False)
    if len(ids) != 1:
        return None
    entradas = tok(texto, return_tensors="pt")
    posicoes = (entradas["input_ids"][0] == tok.mask_token_id).nonzero(as_tuple=True)[0]
    with torch.no_grad():
        logits = modelo(**entradas).logits
    return float(torch.softmax(logits[0, posicoes[0]], dim=-1)[ids[0]])


def sobreposicao(a: list[tuple[str, float]], b: list[tuple[str, float]]) -> float:
    """Fração do top-k compartilhada entre duas distribuições. 1,0 = indiferença total."""
    return len({t for t, _ in a} & {t for t, _ in b}) / len(a)


def main() -> None:
    tok, modelo = carregar()
    mask = tok.mask_token
    linhas: list[str] = []
    registro: dict = {"modelo": MODELO, "tokenizacao": {}, "molduras": {}, "itens": []}

    def escrever(txt: str = "") -> None:
        linhas.append(txt)
        print(txt)

    escrever(f"# Teste de fumaça do instrumento — {MODELO}")
    escrever()
    escrever("Documento gerado por `experimentos/smoke_test_bertimbau.py`. "
             "Não contém medição de viés; verifica a viabilidade do instrumento.")
    escrever()

    # ---------------- Q2: segmentação dos atributos ----------------
    escrever("## Q2 — Segmentação dos atributos no vocabulário")
    escrever()
    escrever("Atributos com mais de um token não podem ser lidos por probabilidade de "
             "máscara única e exigem AUL.")
    escrever()
    escrever("| Conjunto | Atributo | Tokens | Segmentação |")
    escrever("|---|---|---|---|")
    for conjunto, palavras in ATRIBUTOS.items():
        for palavra in palavras:
            pecas = tok.tokenize(palavra)
            registro["tokenizacao"][palavra] = pecas
            marca = "único" if len(pecas) == 1 else f"**{len(pecas)} subtokens**"
            escrever(f"| {conjunto} | {palavra} | {marca} | `{' + '.join(pecas)}` |")
    escrever()

    # ---------------- Q1: comportamento das molduras ----------------
    escrever("## Q1 — Comportamento das molduras")
    escrever()
    escrever("Predições para um enunciado neutro, sem marcação regional, usado como linha de base.")
    escrever()
    neutro = "Ele chegou cedo hoje."
    for nome, moldura in MOLDURAS.items():
        texto = moldura.format(enunciado=neutro, mask=mask)
        topo = top_k_mascara(tok, modelo, texto)
        registro["molduras"][nome] = topo
        escrever(f"**{nome}** — `{moldura.replace('{mask}', '[MASK]')}`")
        escrever()
        escrever("| # | token | prob. |")
        escrever("|---|---|---|")
        for i, (t, p) in enumerate(topo, 1):
            escrever(f"| {i} | `{t}` | {p:.4f} |")
        escrever()

    # ---------------- Q3: sensibilidade ao guise ----------------
    escrever("## Q3 — Sensibilidade ao *guise*")
    escrever()
    escrever("Sobreposição do top-%d entre a condição nordestina e cada condição de controle. "
             "Valor 1,00 indica que o modelo não distinguiu as condições; valores baixos "
             "indicam que a lacuna responde ao *guise*." % TOP_K)
    escrever()
    escrever("| Item | Bloco | Marcador | Moldura | Sobrep. NE×SP | Sobrep. NE×RJ |")
    escrever("|---|---|---|---|---|---|")
    for item in ITENS:
        entrada_item = {"id": item["id"], "bloco": item["bloco"], "molduras": {}}
        for nome, moldura in MOLDURAS.items():
            topos = {}
            for cond in ("ne", "sp", "rj"):
                texto = moldura.format(enunciado=item[cond], mask=mask)
                topos[cond] = top_k_mascara(tok, modelo, texto)
            s_sp = sobreposicao(topos["ne"], topos["sp"])
            s_rj = sobreposicao(topos["ne"], topos["rj"])
            entrada_item["molduras"][nome] = {
                "top_ne": topos["ne"], "top_sp": topos["sp"], "top_rj": topos["rj"],
                "sobreposicao_sp": s_sp, "sobreposicao_rj": s_rj,
            }
            sufixo = " *(suspenso)*" if item.get("suspenso") else ""
            escrever(f"| {item['id']}{sufixo} | {item['bloco']} | {item['marcador']} "
                     f"| {nome} | {s_sp:.2f} | {s_rj:.2f} |")
        registro["itens"].append(entrada_item)
    escrever()

    # ---------------- Amostra qualitativa ----------------
    escrever("## Amostra qualitativa")
    escrever()
    escrever("Top-5 da moldura T1a (gênero controlado) para os itens do bloco C, "
             "que carregam o feixe completo de marcadores.")
    escrever()
    for item in ITENS:
        if item["bloco"] != "C":
            continue
        escrever(f"**{item['id']} — {item.get('estado', '')}**")
        escrever()
        for cond, rotulo in (("ne", "Nordeste"), ("sp", "Controle SP"), ("rj", "Controle RJ")):
            texto = MOLDURAS["T1a"].format(enunciado=item[cond], mask=mask)
            topo = top_k_mascara(tok, modelo, texto, k=5)
            formatado = ", ".join(f"{t} ({p:.3f})" for t, p in topo)
            escrever(f"- *{rotulo}:* {formatado}")
        escrever()

    (SAIDA_DIR / "tabelas" / "smoke_test.md").write_text("\n".join(linhas), encoding="utf-8")
    (SAIDA_DIR / "historico" / "smoke_test.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado em {SAIDA_DIR / 'tabelas' / 'smoke_test.md'}")


if __name__ == "__main__":
    main()
