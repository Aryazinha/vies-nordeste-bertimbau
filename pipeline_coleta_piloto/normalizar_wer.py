"""
normalizar_wer.py

Normalização de texto para o cálculo do WER (`medir_wer.py`), isolada num
módulo próprio porque é **decisão de método, e não detalhe de implementação**:
cada regra aqui muda o número reportado no artigo e precisa ser declarável.

## Por que normalizar

`jiwer` compara palavras literais. Sem normalização, "Ele disse que sim." e
"ele disse que sim" divergem em 50%, e o WER passa a medir pontuação e
maiúsculas do reconhecedor, não compreensão. O teste de 17/09/2026 mostrou o
mesmo com acento: um bloco caiu de 27% para 7% de erro quando se ignorou
acentuação que o transcritor humano não digitou.

## As regras, todas aplicadas aos dois lados

1. Caixa baixa, pontuação removida, espaços colapsados.
2. Acentos removidos. Custo declarado: conflação de pares como *e*/*é* e
   *esta*/*está*, que deixam de ser distinguíveis. A alternativa — exigir
   acentuação exata de quem transcreve — introduz mais ruído do que remove.
3. Algarismos convertidos por extenso, porque o reconhecedor escreve "20" onde
   o falante disse "vinte"; `%` vira "por cento". O símbolo `R$` é removido, e
   a eventual diferença de "reais" conta como erro — caso raro e declarado.
4. Marcas de trecho inaudível (`[?]`, `[inaudível]`) não são normalizadas
   aqui: `medir_wer.py` trata os blocos que as contêm à parte, porque contá-las
   como erro do reconhecedor puniria a máquina por limite do ouvinte humano, e
   o faria mais onde o áudio é pior.

## A lista de equivalências, e por que ela é opcional

O `faster-whisper` regulariza a ortografia da fala: escreve *para* onde se
disse *pra*, *está* onde se disse *tá*. Isso não é erro de compreensão, mas
conta como erro no WER literal — e, se as formas reduzidas forem mais
frequentes numa variedade, o erro espúrio recai sobre ela, na direção que
favorece a hipótese do projeto. Por decisão da equipe em 17/09/2026, o
resultado é reportado **com e sem** estas equivalências, e a diferença entre os
dois números integra o relato.

A lista é curta de propósito. O teste mostrou que expansões ambiciosas pioram a
medida: mapear *né* para *não é* dobrou as omissões num bloco em que o
reconhecedor simplesmente não transcreveu a palavra.
"""

from __future__ import annotations

import re
import unicodedata

# Formas reduzidas de fala e a grafia plena que o reconhecedor costuma escolher.
EQUIVALENCIAS = {
    "pra": "para", "pro": "para o", "pros": "para os", "pras": "para as",
    "ta": "esta", "tao": "estao", "tava": "estava", "tavam": "estavam",
    "to": "estou", "tou": "estou", "tamos": "estamos",
    "ce": "voce", "ces": "voces", "oce": "voce",
    "num": "nao", "ni": "em", "pramim": "para mim",
}

_EXTENSO_ATE_19 = ["zero", "um", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito",
                   "nove", "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis",
                   "dezessete", "dezoito", "dezenove"]
_DEZENAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta",
            "oitenta", "noventa"]
_CENTENAS = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
             "seiscentos", "setecentos", "oitocentos", "novecentos"]


def por_extenso(n: int) -> str:
    """Inteiro por extenso em português, até 999.999. Suficiente para o corpus."""
    if n < 20:
        return _EXTENSO_ATE_19[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _DEZENAS[d] + (f" e {_EXTENSO_ATE_19[u]}" if u else "")
    if n < 1000:
        c, resto = divmod(n, 100)
        if n == 100:
            return "cem"
        return _CENTENAS[c] + (f" e {por_extenso(resto)}" if resto else "")
    if n < 1_000_000:
        milhares, resto = divmod(n, 1000)
        cabeca = "mil" if milhares == 1 else f"{por_extenso(milhares)} mil"
        if not resto:
            return cabeca
        ligacao = " e " if resto < 100 or resto % 100 == 0 else " "
        return cabeca + ligacao + por_extenso(resto)
    return str(n)


def normalizar(texto: str, equivalencias: bool = False) -> str:
    """Aplica as regras 1 a 3 e, opcionalmente, a lista de equivalências."""
    t = texto.lower()
    t = t.replace("%", " por cento ").replace("r$", " ")
    t = re.sub(r"(\d)[.,](\d{3})\b", r"\1\2", t)          # 1.500 -> 1500
    t = re.sub(r"\d+", lambda m: " " + por_extenso(int(m.group())) + " ", t)
    t = "".join(c for c in unicodedata.normalize("NFD", t)
                if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^0-9a-z\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    if equivalencias:
        t = " ".join(EQUIVALENCIAS.get(p, p) for p in t.split())
    return t
