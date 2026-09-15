"""
validar_implicitos.py — validação dos 25 pares de sinalização implícita sem juízes
(`docs/pendencias.md` 2.14; item 4 do plano de fechamento do dataset v1)

## O que substitui

O Filtro 1 — cinco juízes falantes nativos por variedade — foi julgado inviável em
15/09/2026. Os pares das condições `dialeto_A` a `dialeto_D` passam a ser validados
por duas evidências que não dependem de pessoas:

1. **Fonte dialetológica** de cada traço, no estado de verificação registrado no
   projeto (`docs/pares_minimos_v1.md` §3; `docs/referencias.bib`).
2. **Ocorrência no corpus de áudio próprio** — o Filtro 2 do protocolo —, sobre as
   transcrições anonimizadas dos 83 arquivos.

## Assimetria, declarada

O corpus tem 7,96 h. A ocorrência pode **confirmar** um traço, mas a ausência não
reprova traço raro: item sem ocorrência é "não confirmado no corpus", e não
reprovado (`docs/pendencias.md` 2.14).

## Busca automática não é confirmação

Expressão regular não separa *visse* discursivo do subjuntivo de *ver*, *lhe* de
segunda pessoa do de terceira, nem imperativo de indicativo. Por isso o script
**não classifica ocorrência como genuína**: conta candidatos e grava os trechos para
conferência humana (item 8 do plano). A classificação final só existe depois dela.

Os trechos contêm transcrição e ficam em `pipeline_coleta_piloto/dataset_raw/`, fora
do versionamento. A tabela versionada traz apenas contagens.

Uso:
    python validar_implicitos.py
"""

from __future__ import annotations

import json
import random
import re
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REGISTROS = RAIZ.parent / "pipeline_coleta_piloto" / "dataset_raw" / "registros_anonimizados"
SAIDA_TABELA = RAIZ / "resultados" / "tabelas" / "filtro2_implicitos.md"
SAIDA_TRECHOS = (RAIZ.parent / "pipeline_coleta_piloto" / "dataset_raw"
                 / "validacao_filtro2" / "trechos_para_conferir.md")

NE, SE = {"PB", "PE", "CE", "BA"}, {"SP", "RJ"}
MAX_TRECHOS = 40          # por traço e por grupo; acima disso, amostra com semente
SEMENTE = 20260915

FONTE_VERIFICADA = "verificada"
FONTE_DESCRITA = "descrita na literatura; referência não localizada no projeto"
FONTE_NENHUMA = "sem fonte"

# (identificador, descrição, pares que o usam, fonte, padrão, nota para a conferência)
TRACOS = [
    # O traço é de PROPORÇÃO, e não de exclusividade (Figuereido, 2025). Por isso a
    # forma de subjuntivo é buscada junto com a de indicativo, como referência, e a
    # tabela reporta a proporção entre as duas. Verbos comuns em início de oração,
    # e não só os cinco das frases do instrumento — a busca restrita a eles rendeu
    # um único candidato. Excluídos por ambiguidade: entre, fala, passa, sente, vem,
    # faz, vê, espera.
    ("imperativo", "imperativo com morfologia de subjuntivo (olhe, veja, diga, traga, deixe…)",
     ["dialeto_A-00", "dialeto_A-01", "dialeto_A-02", "dialeto_C-00", "dialeto_C-02",
      "dialeto_C-03", "dialeto_C-04"],
     FONTE_VERIFICADA + " — Figuereido (2025): 47% de indicativo em Feira de Santana-BA contra 81% em Campinas-SP",
     r"(?:^|[.!?,]\s*|\bme\s+)(olhe|veja|escute|venha|faça|diga|traga|deixe|ligue|pegue|chame|feche|espere)\b",
     "É imperativo (ordem, pedido, chamada de atenção)? Subjuntivo em oração subordinada "
     "(\"que ele diga\") não conta. O traço é de proporção: ocorrer no Sudeste é esperado."),
    ("imperativo_indicativo", "referência: imperativo com morfologia de indicativo (olha, diz, traz, deixa…)",
     [],
     "referência para a proporção do traço anterior",
     r"(?:^|[.!?,]\s*|\bme\s+)(olha|escuta|diz|traz|deixa|liga|pega|chama|fecha)\b",
     "É imperativo (ordem, pedido, chamada de atenção)? 'Ele diz', 'ela liga' não contam."),
    ("negacao_posverbal", "negação pós-verbal: verbo + não, sem não anterior (fui não, sei não)",
     ["dialeto_A-03", "dialeto_A-04", "dialeto_C-01", "dialeto_C-03"],
     FONTE_VERIFICADA + " — Santos e Vitório (2025): produtividade máxima de 5,6%",
     None,   # detectado por função, ver _negacao_posverbal
     "É 'verbo + não' fechando a oração, sem outro 'não' antes? Dupla negação (não sei não) não conta."),
    ("lexico_regional", "arretado, aperreado, avexado, oxe, oxente",
     ["dialeto_B-00", "dialeto_B-01", "dialeto_B-02", "dialeto_B-03", "dialeto_C-00",
      "dialeto_C-01", "dialeto_C-02"],
     FONTE_NENHUMA,
     r"\b(arretad[oa]s?|aperread[oa]s?|avexad[oa]s?|oxe|oxente)\b",
     "É o uso regional da palavra? Anote qual palavra ocorreu."),
    ("visse", "marcador discursivo visse? (Recife)",
     ["dialeto_C-03"],
     FONTE_NENHUMA,
     r"\bvisse\b",
     "É o marcador de fim de frase (\"tá bom, visse?\")? O subjuntivo de ver (\"se você visse\") não conta."),
    ("vocativo_menino", "menino como vocativo dirigido a adulto",
     ["dialeto_B-04", "dialeto_D-03"],
     FONTE_NENHUMA + " (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B)",
     r"(?:^|[.!?]\s*)menin[oa]\s*[,!]",
     "É chamamento ou interjeição (\"Menino, olha isso\")? Referência a uma criança não conta."),
    ("vocativo_rapaz", "rapaz como vocativo ou interjeição",
     ["dialeto_C-04", "dialeto_D-04"],
     FONTE_NENHUMA + " (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B)",
     r"(?:^|[.!?]\s*)rapaz\s*[,!]",
     "É chamamento ou interjeição (\"Rapaz, eu não sabia\")? Referência a um homem jovem não conta."),
    ("lhe_segunda_pessoa", "lhe com referência à segunda pessoa (eu lhe vi, lhe ligo)",
     ["dialeto_D-00", "dialeto_D-01"],
     FONTE_DESCRITA,
     r"\blhe\b",
     "O 'lhe' se refere a quem está ouvindo (você)? 'Lhe' de terceira pessoa (a ele) não conta."),
    ("comitativo_mais", "comitativo com mais (foi mais eu = foi comigo)",
     ["dialeto_D-02"],
     FONTE_DESCRITA,
     r"\b(foi|fui|vai|vou|veio|saiu|andou|tava|estava|ficou)\s+mais\s+(eu|ele|ela|a gente|nós|tu|você)\b",
     "Significa 'junto com'? Comparação (\"foi mais ele que ela\") não conta."),
    ("massa_avaliativo", "massa como avaliativo (a festa foi massa)",
     ["dialeto_D-05"],
     FONTE_NENHUMA + " (candidato derivado do corpus próprio, piloto_medicoes.md, adendo B)",
     r"\b(é|foi|tá|ta|muito|mó|que|bem)\s+massa\b",
     "Significa 'legal, bom'? Massa de comida, de pessoas ou física não conta."),
    ("tu_sem_flexao", "tu com verbo em terceira pessoa (tu vai, tu foi)",
     ["dialeto_D-06"],
     FONTE_DESCRITA + "; registrado também no Rio de Janeiro (docs/pares_minimos_v1.md, M4)",
     r"\btu\s+(vai|foi|é|tem|quer|sabe|pode|viu|fez|tá|está|faz|acha|gosta|disse|mora|vem|trabalha)\b",
     "É 'tu' com verbo sem -s? Ocorrer no Rio é esperado e está declarado."),
    ("que_foi_que", "clivagem interrogativa que foi que",
     ["dialeto_D-07"],
     FONTE_NENHUMA,
     r"\bque foi que\b",
     "É pergunta do tipo \"que foi que houve?\"?"),
    ("ta_com_tempo", "durativo tá com + tempo (tá com dois dias que)",
     ["dialeto_D-08"],
     FONTE_NENHUMA,
     r"\b(tá|ta|está)\s+com\s+\w+\s+(dias?|anos?|meses|mês|semanas?|horas?)\b",
     "Significa 'faz tanto tempo que'? 'Tá com dois anos de idade' não conta."),
    ("toda_vida", "toda vida com valor de sempre",
     ["dialeto_D-09"],
     FONTE_NENHUMA,
     r"\btoda vida\b",
     "Significa 'sempre'? 'A vida toda' com sentido literal de duração conta como dúvida; anote."),
]

PARES_ESPERADOS = {f"dialeto_{b}-{i:02d}" for b in "ABC" for i in range(5)} | \
                  {f"dialeto_D-{i:02d}" for i in range(10)}


def _tokens(texto: str) -> list[str]:
    return re.findall(r"[^\W\d_]+|[.!?,;]", texto.lower(), flags=re.UNICODE)


def _negacao_posverbal(texto: str) -> list[tuple[int, int]]:
    """
    'não' seguido de pontuação ou fim do trecho, colado a uma palavra anterior.

    Primeira versão, de 15/09/2026, rendeu majoritariamente falsos positivos de
    resposta e de advérbio (*Eu disse, não*; *Ainda não*; *Agora não*). A negação
    pós-verbal verdadeira (*sei não*, *se garante não?*, *parece não*) não tem vírgula
    antes do 'não' nem advérbio ou pronome colado a ele, e não é dupla negação —
    daí as exclusões. Continua sendo aproximação: a conferência humana decide.
    """
    excluidas = {"não", "que", "e", "ou", "mas", "sim", "porque", "se", "né", "ainda",
                 "agora", "já", "ali", "aqui", "lá", "hoje", "eu", "ele", "ela", "você",
                 "a", "o", "gente", "nós", "eles", "elas", "ah", "é"} - {"é"}
    negativos = {"não", "nunca", "nem", "ninguém", "nada", "jamais"}
    achados = []
    for m in re.finditer(r"\bnão\b(?=\s*[.!?,;]|\s*$)", texto, flags=re.IGNORECASE):
        prefixo = texto[:m.start()]
        if re.search(r"[,;:]\s*$", prefixo):
            continue
        antes = re.findall(r"[^\W\d_]+", prefixo.lower())
        if not antes or antes[-1] in excluidas:
            continue
        if negativos & set(antes[-6:]):
            continue
        achados.append((m.start(), m.end()))
    return achados


def _locutor(segmento: dict) -> str:
    falas = Counter(w.get("speaker") for w in segmento.get("words", []) if w.get("speaker"))
    return falas.most_common(1)[0][0] if falas else "?"


def main() -> None:
    cobertos = {p for _, _, pares, *_ in TRACOS for p in pares}
    assert cobertos == PARES_ESPERADOS, f"pares sem traço: {PARES_ESPERADOS - cobertos}"

    arquivos = sorted(REGISTROS.glob("*.json"))
    assert arquivos, f"nenhuma transcrição em {REGISTROS}"

    palavras = Counter()
    ocorrencias = {t[0]: {"NE": [], "SE": []} for t in TRACOS}
    for arq in arquivos:
        reg = json.loads(arq.read_text(encoding="utf-8"))
        grupo = "NE" if reg["estado_alvo"] in NE else "SE" if reg["estado_alvo"] in SE else None
        if grupo is None:
            continue
        for seg in reg["transcricao"]["segmentos"]:
            texto = seg["text"].strip()
            palavras[grupo] += len(re.findall(r"[^\W\d_]+", texto))
            for ident, _, _, _, padrao, _ in TRACOS:
                if padrao is None:
                    spans = _negacao_posverbal(texto)
                else:
                    spans = [(m.start(), m.end())
                             for m in re.finditer(padrao, texto, flags=re.IGNORECASE)]
                for ini, fim in spans:
                    ocorrencias[ident][grupo].append({
                        "estado": reg["estado_alvo"], "id": reg["id"], "canal": reg.get("canal", "?"),
                        "tempo": f"{int(seg['start'] // 60):02d}:{int(seg['start'] % 60):02d}",
                        "locutor": _locutor(seg),
                        "trecho": texto[:ini] + "**" + texto[ini:fim] + "**" + texto[fim:],
                    })

    def taxa(n: int, grupo: str) -> float:
        return n / palavras[grupo] * 100_000 if palavras[grupo] else 0.0

    # ---- tabela versionada: só contagens ----------------------------------
    L = ["# Validação dos pares de sinalização implícita — fonte e corpus", "",
         "Gerado por `experimentos/validar_implicitos.py`. Substitui o Filtro 1 (juízes),",
         "inviável, conforme `docs/pendencias.md` 2.14. **Contagens de candidatos por busca",
         "automática, antes da conferência humana** — não são ocorrências confirmadas.", "",
         f"Corpus: {len(arquivos)} arquivos; {palavras['NE']:,} palavras do Nordeste e "
         f"{palavras['SE']:,} do Sudeste. Taxas por 100 mil palavras.".replace(",", "."), "",
         "A coluna de arquivos importa tanto quanto a de candidatos: vários candidatos",
         "num único arquivo podem ser um único falante.", "",
         "| traço | pares | fonte | candidatos NE (arquivos) | por 100 mil | candidatos SE (arquivos) | por 100 mil | situação provisória |",
         "|---|---|---|---|---|---|---|---|"]
    for ident, descricao, pares, fonte, _, _ in TRACOS:
        ne, se = len(ocorrencias[ident]["NE"]), len(ocorrencias[ident]["SE"])
        arq_ne = len({o["id"] for o in ocorrencias[ident]["NE"]})
        arq_se = len({o["id"] for o in ocorrencias[ident]["SE"]})
        if not pares:
            situacao = "referência"
        elif ne == 0:
            situacao = "não confirmado no corpus"
        elif taxa(se, "SE") >= taxa(ne, "NE"):
            situacao = "a conferir; candidatos também no SE em taxa igual ou maior"
        else:
            situacao = "a conferir"
        if pares and ne and arq_ne == 1:
            situacao += "; um único arquivo no NE"
        L.append(f"| {descricao} | {len(pares)} | {fonte} | {ne} ({arq_ne}) | {taxa(ne, 'NE'):.1f} | "
                 f"{se} ({arq_se}) | {taxa(se, 'SE'):.1f} | {situacao} |")
    sub = {g: len(ocorrencias["imperativo"][g]) for g in ("NE", "SE")}
    ind = {g: len(ocorrencias["imperativo_indicativo"][g]) for g in ("NE", "SE")}
    prop = {g: (f"{sub[g] / (sub[g] + ind[g]):.0%}" if sub[g] + ind[g] else "—") for g in ("NE", "SE")}
    L += ["", f"**Imperativo, proporção de forma de subjuntivo entre os candidatos:** "
              f"NE {prop['NE']} ({sub['NE']} de {sub['NE'] + ind['NE']}), "
              f"SE {prop['SE']} ({sub['SE']} de {sub['SE'] + ind['SE']}). "
              "Pela fonte, espera-se proporção maior no Nordeste. Valor antes da conferência."]
    L += ["", "## Pares e traços", "",
          "Um par de feixe (`dialeto_C`) só é confirmado se todos os seus traços o forem.", "",
          "| par | traços |", "|---|---|"]
    por_par = {}
    for ident, _, pares, *_ in TRACOS:
        for p in pares:
            por_par.setdefault(p, []).append(ident)
    for p in sorted(por_par):
        L.append(f"| `{p}` | {', '.join(por_par[p])} |")
    SAIDA_TABELA.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- trechos para conferência: fora do versionamento ------------------
    rng = random.Random(SEMENTE)
    T = ["# Trechos para conferir — validação dos pares implícitos", "",
         "Item 8 do plano de fechamento do dataset v1. **Não versionar:** contém transcrição.", "",
         "Para cada trecho, preencha a última coluna com **sim** (o traço ocorre de fato, no uso",
         "descrito) ou **não**. Se houver dúvida, escreva **?** e uma nota curta.", ""]
    for ident, descricao, _, _, _, nota in TRACOS:
        T += [f"## {descricao}", "", f"**Como decidir:** {nota}", ""]
        for grupo in ("NE", "SE"):
            lista = ocorrencias[ident][grupo]
            if not lista:
                T += [f"*{grupo}: nenhum candidato.*", ""]
                continue
            mostrados = lista if len(lista) <= MAX_TRECHOS else rng.sample(lista, MAX_TRECHOS)
            aviso = "" if len(lista) <= MAX_TRECHOS else f" — amostra de {MAX_TRECHOS} em {len(lista)}"
            T += [f"### {grupo}: {len(lista)} candidato(s){aviso}", "",
                  "| # | UF | arquivo | tempo | locutor | trecho | genuíno? |", "|---|---|---|---|---|---|---|"]
            for k, o in enumerate(mostrados, 1):
                trecho = o["trecho"].replace("|", "/")
                T.append(f"| {k} | {o['estado']} | {o['id']} | {o['tempo']} | {o['locutor']} | {trecho} |  |")
            T.append("")
    SAIDA_TRECHOS.parent.mkdir(parents=True, exist_ok=True)
    SAIDA_TRECHOS.write_text("\n".join(T) + "\n", encoding="utf-8")

    print(SAIDA_TABELA.read_text(encoding="utf-8"))
    print(f"Trechos para conferência em {SAIDA_TRECHOS}")


if __name__ == "__main__":
    main()
