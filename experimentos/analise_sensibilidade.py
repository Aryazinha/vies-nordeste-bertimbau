"""
analise_sensibilidade.py

Complemento ao teste de fumaça. A sobreposição de top-k é medida grosseira:
duas distribuições podem compartilhar os mesmos doze tokens e ainda assim
diferir de forma sistemática nas probabilidades. Este script mede a diferença
de duas maneiras mais sensíveis:

  (a) divergência de Jensen-Shannon sobre a distribuição completa da lacuna,
      entre a condição nordestina e cada condição de controle;
  (b) razão de probabilidade, por atributo-alvo de token único, entre a
      condição nordestina e a de controle — que é a leitura que o experimento
      de fato fará.

Uso:
    python experimentos/analise_sensibilidade.py
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

from smoke_test_bertimbau import ITENS, MOLDURAS, MODELO

RAIZ = Path(__file__).resolve().parent
SAIDA_DIR = RAIZ / "resultados"
# Saída de máquina fica em `resultados/tabelas/`; `resultados/` guarda apenas
# relatórios escritos à mão (ver nota em `teste_construcional.py`).
(SAIDA_DIR / "tabelas").mkdir(parents=True, exist_ok=True)

# Apenas atributos de token único no vocabulário do BERTimbau (ver Q2 do teste
# de fumaça). Os demais exigem AUL e ficam fora desta verificação.
ATRIBUTOS_UNITOKEN = [
    "inteligente", "normal", "estranha", "boa", "má", "séria", "comum",
    "médico", "advogado", "engenheiro", "professor", "juiz", "empregada",
]


def distribuicao(tok, modelo, texto: str) -> torch.Tensor:
    entradas = tok(texto, return_tensors="pt")
    pos = (entradas["input_ids"][0] == tok.mask_token_id).nonzero(as_tuple=True)[0][0]
    with torch.no_grad():
        logits = modelo(**entradas).logits
    return torch.softmax(logits[0, pos], dim=-1)


def js(p: torch.Tensor, q: torch.Tensor) -> float:
    """Divergência de Jensen-Shannon em bits. 0 = distribuições idênticas."""
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = a > 0
        return float((a[mask] * (torch.log2(a[mask]) - torch.log2(b[mask]))).sum())
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def main() -> None:
    tok = AutoTokenizer.from_pretrained(MODELO)
    modelo = AutoModelForMaskedLM.from_pretrained(MODELO)
    modelo.eval()
    mask = tok.mask_token

    ids_attr = {}
    for a in ATRIBUTOS_UNITOKEN:
        ids = tok.encode(a, add_special_tokens=False)
        if len(ids) == 1:
            ids_attr[a] = ids[0]

    linhas: list[str] = []
    registro: dict = {"modelo": MODELO, "js": [], "razoes": []}

    def escrever(t: str = "") -> None:
        linhas.append(t)
        print(t)

    escrever("# Análise de sensibilidade do instrumento")
    escrever()
    escrever("Complemento ao teste de fumaça. Mede a diferença entre condições sobre a "
             "distribuição completa da lacuna, e não apenas sobre o top-k.")
    escrever()

    # ---------------- (a) divergência de Jensen-Shannon ----------------
    escrever("## Divergência de Jensen-Shannon entre condições")
    escrever()
    escrever("Valores em bits. Zero indica distribuições idênticas — o modelo não "
             "distinguiu as condições. Para referência de escala, a última linha traz "
             "a divergência entre dois enunciados de conteúdo proposicional distinto, "
             "que é o teto esperado para uma diferença que o modelo efetivamente percebe.")
    escrever()
    escrever("| Item | Bloco | Marcador | Moldura | JS(NE‖SP) | JS(NE‖RJ) |")
    escrever("|---|---|---|---|---|---|")
    for item in ITENS:
        for nome, moldura in MOLDURAS.items():
            d = {c: distribuicao(tok, modelo, moldura.format(enunciado=item[c], mask=mask))
                 for c in ("ne", "sp", "rj")}
            j_sp, j_rj = js(d["ne"], d["sp"]), js(d["ne"], d["rj"])
            registro["js"].append({"id": item["id"], "moldura": nome,
                                   "js_sp": j_sp, "js_rj": j_rj})
            escrever(f"| {item['id']} | {item['bloco']} | {item['marcador']} | {nome} "
                     f"| {j_sp:.4f} | {j_rj:.4f} |")

    ref_a = MOLDURAS["T1a"].format(enunciado="Ele foi preso ontem à noite.", mask=mask)
    ref_b = MOLDURAS["T1a"].format(enunciado="Ela defendeu a tese no mês passado.", mask=mask)
    js_ref = js(distribuicao(tok, modelo, ref_a), distribuicao(tok, modelo, ref_b))
    registro["js_referencia"] = js_ref
    escrever(f"| *referência de escala* | — | conteúdo distinto | T1a | {js_ref:.4f} | — |")
    escrever()

    # ---------------- (b) razão de probabilidade por atributo ----------------
    escrever("## Razão de probabilidade por atributo, na moldura T1a")
    escrever()
    escrever("Razão entre a probabilidade sob a condição nordestina e sob a condição de "
             "controle de São Paulo. Valores acima de 1 indicam atributo mais provável no "
             "*guise* nordestino. Apenas atributos de token único.")
    escrever()
    cabecalho = "| Item | " + " | ".join(ids_attr) + " |"
    escrever(cabecalho)
    escrever("|---" * (len(ids_attr) + 1) + "|")
    for item in ITENS:
        p_ne = distribuicao(tok, modelo, MOLDURAS["T1a"].format(enunciado=item["ne"], mask=mask))
        p_sp = distribuicao(tok, modelo, MOLDURAS["T1a"].format(enunciado=item["sp"], mask=mask))
        celulas, linha_reg = [], {"id": item["id"]}
        for a, i in ids_attr.items():
            razao = float(p_ne[i] / p_sp[i])
            linha_reg[a] = razao
            celulas.append(f"{razao:.2f}")
        registro["razoes"].append(linha_reg)
        escrever(f"| {item['id']} | " + " | ".join(celulas) + " |")
    escrever()

    (SAIDA_DIR / "tabelas" / "sensibilidade.md").write_text("\n".join(linhas), encoding="utf-8")
    (SAIDA_DIR / "historico" / "sensibilidade.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado em {SAIDA_DIR / 'tabelas' / 'sensibilidade.md'}")


if __name__ == "__main__":
    main()
