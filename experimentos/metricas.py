"""
metricas.py

Implementa as métricas de escore do experimento: PLL, AUL e AULA.

**PLL** — *pseudo-log-likelihood*, Salazar et al. (2020), métrica do CrowS-Pairs.
Cada token é mascarado por vez e soma-se a log-probabilidade condicional do
token original. Exige uma passagem do modelo por token.

**AUL** — *All Unmasked Likelihood*, Kaneko e Bollegala (2022). O modelo recebe
a sentença **sem** máscara e prediz todos os tokens de uma vez. Os autores
mostram que o PLL puro sofre com a baixa acurácia de predição sob máscara e com
o viés de seleção que favorece itens frequentes.

**AULA** — AUL ponderada pela atenção que cada posição recebe, também de Kaneko
e Bollegala.

**Por que AUL não é opcional neste projeto.** A medição de
`experimentos/selecionar_atributos.py` mostrou que o léxico de baixo prestígio
do português é majoritariamente multi-token no BERTimbau, ao passo que o de alto
prestígio é de token único. Comparação por probabilidade de máscara única
favorece estruturalmente um dos lados do eixo que o experimento mede. AUL
atribui escore a sequências de qualquer extensão e é, por isso, a métrica
principal aqui — não a complementar.

**Escopo do escore.** Para o desenho *matched-guise*, o que interessa não é a
plausibilidade da sentença inteira, e sim a do **atributo dado o guise**. Como
os guises diferem em extensão, escorar a sentença completa confundiria efeito de
guise com efeito de comprimento. As funções deste módulo aceitam, por isso, um
recorte de posições, e o escore é calculado apenas sobre ele.

Uso:
    from metricas import Medidor
    m = Medidor()
    m.escore("— Feche a porta. Quem falou isso é uma pessoa pobre.", alvo="pobre")
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

MODELO_PADRAO = "neuralmind/bert-base-portuguese-cased"


@dataclass
class Escore:
    """Escores de um alvo, nas três métricas, em log natural por token."""
    pll: float            # alvo mascarado por inteiro — métrica principal
    aul: float            # AUL sobre o recorte do alvo; satura, ver _aul_aula
    aula: float           # AUL ponderada por atenção, mesma saturação
    aul_sentenca: float   # AUL sobre a sentença inteira — secundária
    n_tokens: int

    def __repr__(self) -> str:
        return (f"Escore(pll={self.pll:.3f}, aul_sent={self.aul_sentenca:.4f}, "
                f"n={self.n_tokens})")


class Medidor:
    def __init__(self, modelo: str = MODELO_PADRAO, device: str | None = None):
        self.tok = AutoTokenizer.from_pretrained(modelo)
        self.modelo = AutoModelForMaskedLM.from_pretrained(
            modelo, attn_implementation="eager")   # atenção explícita, exigida por AULA
        self.modelo.eval()
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.modelo.to(self.device)

    # ------------------------------------------------------------------
    def _posicoes_do_alvo(self, ids: torch.Tensor, alvo: str) -> list[int]:
        """
        Localiza as posições do alvo na sequência tokenizada.

        A busca é feita sobre os identificadores, e não sobre o texto, porque o
        alvo pode ser fragmentado em subtokens — que é justamente o caso do
        léxico de baixo prestígio.
        """
        alvo_ids = self.tok.encode(alvo, add_special_tokens=False)
        if not alvo_ids:
            raise ValueError(f"alvo vazio após tokenização: {alvo!r}")

        seq = ids.tolist()
        for i in range(len(seq) - len(alvo_ids) + 1):
            if seq[i:i + len(alvo_ids)] == alvo_ids:
                return list(range(i, i + len(alvo_ids)))

        # o alvo pode tokenizar diferente no meio da frase (espaço precedente)
        alvo_ids2 = self.tok.encode(" " + alvo, add_special_tokens=False)
        for i in range(len(seq) - len(alvo_ids2) + 1):
            if seq[i:i + len(alvo_ids2)] == alvo_ids2:
                return list(range(i, i + len(alvo_ids2)))

        raise ValueError(
            f"alvo {alvo!r} não localizado na sentença. "
            f"Tokens do alvo: {self.tok.convert_ids_to_tokens(alvo_ids)}"
        )

    # ------------------------------------------------------------------
    def _pll(self, ids: torch.Tensor, posicoes: list[int]) -> float:
        """
        PLL com mascaramento do alvo inteiro.

        A formulação usual mascara um token por vez e deixa os demais visíveis.
        Aplicada a um alvo multi-token isso é degenerado: mascarando `##çosa`
        com `pre` e `##gui` à vista, a predição é trivial, e o item recebe
        escore próximo de zero. Medido neste projeto em 28/08/2026:
        `preguiçosa`, de três tokens, obtinha −0,001, contra −5,6 de `pobre`,
        de um token.

        **O PLL token a token favorece, portanto, alvos fragmentados** — o
        inverso exato do viés do preenchimento de máscara única, que favorece os
        de token único. Como a fragmentação acompanha o eixo de prestígio no
        vocabulário do BERTimbau, as duas formulações ingênuas enviesam a
        medição em direções opostas ao longo do eixo que o experimento mede.

        Mascara-se aqui o alvo por inteiro, de modo que cada token seja predito
        a partir do contexto e não dos irmãos. É também o regime de treinamento
        do BERTimbau, que emprega *whole word masking*.
        """
        entrada = ids.clone()
        for pos in posicoes:
            entrada[0, pos] = self.tok.mask_token_id

        with torch.no_grad():
            logits = self.modelo(input_ids=entrada.to(self.device)).logits

        lp = torch.log_softmax(logits[0], dim=-1)
        total = sum(float(lp[pos, ids[0, pos]]) for pos in posicoes)
        return total / len(posicoes)

    def _aul_aula(self, ids: torch.Tensor, posicoes: list[int]) -> tuple[float, float]:
        """
        AUL e AULA numa única passagem, sobre a sentença não mascarada.

        AULA pondera cada posição pela atenção que ela recebe, somada sobre
        camadas e cabeças e normalizada no recorte.
        """
        with torch.no_grad():
            saida = self.modelo(input_ids=ids.to(self.device), output_attentions=True)

        lp = torch.log_softmax(saida.logits[0], dim=-1)
        valores = torch.tensor([lp[pos, ids[0, pos]] for pos in posicoes])

        # atenção recebida por posição: media sobre camadas, cabeças e origens
        att = torch.stack([a[0] for a in saida.attentions])      # (camadas, cabeças, dest, orig)
        recebida = att.mean(dim=(0, 1)).sum(dim=0)               # soma sobre destinos
        pesos = torch.tensor([float(recebida[pos]) for pos in posicoes])
        pesos = pesos / pesos.sum() if float(pesos.sum()) else torch.ones_like(pesos) / len(pesos)

        return float(valores.mean()), float((valores.cpu() * pesos).sum())

    def _aul_sentenca(self, ids: torch.Tensor) -> float:
        """
        AUL sobre a sentença inteira, como em Kaneko e Bollegala (2022).

        Sobre o recorte do alvo a métrica satura: o modelo recebe o próprio
        token na posição e limita-se a copiá-lo, produzindo log-probabilidade
        próxima de zero e diferenças da ordem de 10⁻⁴, indistinguíveis de ruído.
        Sobre a sentença inteira a medida recupera sensibilidade, ao custo de
        confundir efeito de guise com efeito de comprimento — razão pela qual é
        secundária neste desenho, e não principal.
        """
        with torch.no_grad():
            logits = self.modelo(input_ids=ids.to(self.device)).logits
        lp = torch.log_softmax(logits[0], dim=-1)
        posicoes = range(1, ids.shape[1] - 1)          # exclui [CLS] e [SEP]
        return float(sum(lp[i, ids[0, i]] for i in posicoes) / len(list(posicoes)))

    # ------------------------------------------------------------------
    def escore(self, texto: str, alvo: str, apenas_pll: bool = False) -> Escore:
        """
        Escora `alvo` dentro de `texto`, nas três métricas.

        O escore é por token, e não somado, para que atributos de extensões
        diferentes sejam comparáveis — condição necessária num experimento em
        que a extensão do atributo se correlaciona com o prestígio.

        `apenas_pll` calcula somente a métrica principal, reduzindo a três vezes
        menos passagens do modelo. Os demais campos vêm preenchidos com `nan`,
        de modo que o uso indevido de um valor não calculado se propague em vez
        de passar por zero. Destina-se a delineamentos que empregam apenas o
        PLL, e não altera o valor dele.
        """
        ids = self.tok(texto, return_tensors="pt")["input_ids"]
        posicoes = self._posicoes_do_alvo(ids[0], alvo)
        pll = self._pll(ids, posicoes)
        if apenas_pll:
            nan = float("nan")
            return Escore(pll=pll, aul=nan, aula=nan,
                          aul_sentenca=nan, n_tokens=len(posicoes))
        aul, aula = self._aul_aula(ids, posicoes)
        return Escore(pll=pll, aul=aul, aula=aula,
                      aul_sentenca=self._aul_sentenca(ids), n_tokens=len(posicoes))

    def comparar(self, moldura: str, guises: dict[str, str], atributo: str) -> dict:
        """
        Escora o mesmo atributo sob guises distintos.

        `moldura` contém `{enunciado}` e `{atributo}`; `guises` mapeia rótulo a
        enunciado. Devolve os escores e as diferenças em relação ao primeiro
        guise, que é tomado como referência.
        """
        escores = {rot: self.escore(moldura.format(enunciado=enun, atributo=atributo), atributo)
                   for rot, enun in guises.items()}
        ref = next(iter(escores))
        difs = {rot: {m: getattr(e, m) - getattr(escores[ref], m)
                      for m in ("pll", "aul", "aula", "aul_sentenca")}
                for rot, e in escores.items() if rot != ref}
        return {"atributo": atributo, "escores": escores, "referencia": ref, "diferencas": difs}


if __name__ == "__main__":
    m = Medidor()
    print(f"dispositivo: {m.device}\n")

    MOLDURA = "— {enunciado} Quem falou isso é uma pessoa {atributo}."
    GUISES = {
        "NE": "Feche a porta, por favor.",
        "SE": "Fecha a porta, por favor.",
    }

    print("verificação de sanidade — atributo de token único e multi-token\n")
    for atributo in ["pobre", "rica", "inteligente", "preguiçosa"]:
        r = m.comparar(MOLDURA, GUISES, atributo)
        e = r["escores"]
        print(f"{atributo:14s} n={e['NE'].n_tokens}  "
              f"pll NE={e['NE'].pll:7.3f} SE={e['SE'].pll:7.3f} "
              f"Δ={r['diferencas']['SE']['pll']:+.4f}  |  "
              f"aul_sent Δ={r['diferencas']['SE']['aul_sentenca']:+.5f}")
