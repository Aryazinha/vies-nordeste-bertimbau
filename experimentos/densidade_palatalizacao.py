"""
densidade_palatalizacao.py — quantos contextos de palatalização há por minuto de fala

Insumo que faltava para completar `meta_corpus_autonomo.py`. O teto de 5% por
falante impõe um piso de falantes por estado, mas nada diz sobre **quanta fala
por falante** é necessária. Para o corpus servir ao marcador de áudio do projeto
— a palatalização de /t,d/ diante de /i/, seção 1.4.3 do `CLAUDE.md` —, cada
falante precisa produzir contextos suficientes para que sua taxa seja estimável.

Este script mede a densidade desses contextos na fala já transcrita, por falante
e por minuto, para que o piso deixe de ser suposto e passe a ser derivado.

## O que conta como contexto

A palatalização em português brasileiro incide sobre /t,d/ seguidos de [i]. Na
ortografia isso aparece de duas formas, e ignorar a segunda subestimaria a
densidade pela metade:

- **Contexto explícito** — as sequências `ti` e `di`, como em *tia*, *dia*,
  *sentir*, *pedir*.
- **Contexto por redução** — `te` e `de` em final de palavra átono, que se
  realizam como [tʃi] e [dʒi] na maior parte do país: *gente*, *pode*, *cidade*,
  *tarde*. É o contexto mais frequente na fala corrente.

Ambos são contados, e separadamente, porque a literatura dialetológica costuma
reportá-los à parte.

## Privacidade

O script lê os registros finais **de dentro do arquivo compactado, em memória**,
sem extrair nada para o disco, e emite apenas contagens agregadas. Nenhum trecho
de transcrição é gravado ou impresso, o que preserva o compromisso da seção 1.4.2
do `CLAUDE.md` — as transcrições não estão anonimizadas.

Uso:
    python densidade_palatalizacao.py [caminho_do_zip]
"""

from __future__ import annotations

import json
import re
import statistics
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = Path(__file__).resolve().parent / "resultados"
ZIP_PADRAO = RAIZ / "piloto_resultados (2).zip"

# Ocorrência mínima para estimar uma taxa por falante. Mesmo critério adotado em
# `meta_volume_corpus.py` para a negação pós-verbal: presença ou ausência bastam
# para constatar, mas comparar grupos exige estimar a taxa em cada um.
OCORRENCIAS_PARA_TAXA = 10

_EXPLICITO = re.compile(r"[td]i", re.IGNORECASE)
_REDUZIDO = re.compile(r"[td]es?$", re.IGNORECASE)


def _sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def contextos(palavra: str) -> tuple[int, int]:
    """Contextos de palatalização numa palavra: (explícitos, por redução)."""
    limpa = _sem_acento(re.sub(r"[^\w]", "", palavra, flags=re.UNICODE)).lower()
    if not limpa:
        return 0, 0
    explicitos = len(_EXPLICITO.findall(limpa))
    # `de`/`te` final átono. Excluem-se monossílabos tônicos como `de` preposição,
    # que não reduz da mesma maneira, e formas em que o `e` final é acentuado.
    reduzidos = 1 if (len(limpa) > 3 and _REDUZIDO.search(limpa)) else 0
    return explicitos, reduzidos


def main() -> None:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else ZIP_PADRAO
    if not caminho.exists():
        raise SystemExit(f"arquivo não encontrado: {caminho}")

    # (id, estado, camada, falante) -> métricas
    por_falante: dict[tuple, dict] = defaultdict(
        lambda: {"palavras": 0, "explicitos": 0, "reduzidos": 0, "segundos": 0.0})
    por_estado_arquivos: dict[str, set] = defaultdict(set)

    with zipfile.ZipFile(caminho) as z:
        for nome in z.namelist():
            if not nome.endswith(".json"):
                continue
            reg = json.loads(z.read(nome))
            uf, camada = reg["estado_alvo"], reg["tipo_fonte"]
            por_estado_arquivos[uf].add(reg["id"])
            for seg in reg["transcricao"]["segmentos"]:
                for w in seg.get("words") or []:
                    falante = w.get("speaker") or "DESCONHECIDO"
                    chave = (reg["id"], uf, camada, falante)
                    e, r = contextos(w["word"])
                    d = por_falante[chave]
                    d["palavras"] += 1
                    d["explicitos"] += e
                    d["reduzidos"] += r
                    dur = (w.get("end") or 0) - (w.get("start") or 0)
                    d["segundos"] += max(0.0, dur)

    # ------------------------------------------------------------------
    L: list[str] = []
    add = L.append
    add("# Densidade de contextos de palatalização na fala coletada")
    add("")
    add("Gerado por `experimentos/densidade_palatalizacao.py` sobre os registros")
    add("finais do piloto, lidos em memória a partir do arquivo compactado. Apenas")
    add("contagens agregadas: nenhum trecho de transcrição é gravado.")
    add("")

    todos = list(por_falante.values())
    palavras = sum(d["palavras"] for d in todos)
    explicitos = sum(d["explicitos"] for d in todos)
    reduzidos = sum(d["reduzidos"] for d in todos)
    segundos = sum(d["segundos"] for d in todos)

    add("## Densidade agregada")
    add("")
    add("| Medida | Valor |")
    add("|---|---|")
    add(f"| Palavras transcritas | {palavras:,} |".replace(",", "."))
    add(f"| Tempo de fala atribuído | {segundos/3600:.2f} h |")
    add(f"| Contextos explícitos (*ti*, *di*) | {explicitos:,} |".replace(",", "."))
    add(f"| Contextos por redução (*-te*, *-de* final) | {reduzidos:,} |".replace(",", "."))
    add(f"| **Total de contextos** | **{explicitos + reduzidos:,}** |".replace(",", "."))
    add("")
    if segundos:
        por_min = (explicitos + reduzidos) / (segundos / 60)
        add(f"**{por_min:.1f} contextos por minuto de fala**, dos quais "
            f"{explicitos/(segundos/60):.1f} explícitos e {reduzidos/(segundos/60):.1f} por redução.")
        add(f"Equivale a um contexto a cada {60/por_min:.1f} segundos de fala.")
    add("")

    add("## Por camada")
    add("")
    add("| Camada | Falantes | Palavras | Contextos por minuto |")
    add("|---|---|---|---|")
    por_camada = defaultdict(lambda: {"n": 0, "palavras": 0, "ctx": 0, "seg": 0.0})
    for (_, _, camada, _), d in por_falante.items():
        c = por_camada[camada]
        c["n"] += 1
        c["palavras"] += d["palavras"]
        c["ctx"] += d["explicitos"] + d["reduzidos"]
        c["seg"] += d["segundos"]
    for camada, c in sorted(por_camada.items()):
        pm = c["ctx"] / (c["seg"] / 60) if c["seg"] else 0
        add(f"| `{camada}` | {c['n']} | {c['palavras']} | {pm:.1f} |")
    add("")

    add("## O piso de fala por falante, agora derivável")
    add("")
    add(f"Estimar a taxa de palatalização de um falante exige ao menos")
    add(f"{OCORRENCIAS_PARA_TAXA} contextos, pelo mesmo critério que")
    add("`meta_volume_corpus.py` aplicou à negação pós-verbal: constatar presença")
    add("basta com um, comparar grupos exige estimar a taxa.")
    add("")
    if segundos:
        seg_por_falante = OCORRENCIAS_PARA_TAXA / (por_min / 60)
        add(f"Com {por_min:.1f} contextos por minuto, isso significa "
            f"**{seg_por_falante:.0f} segundos, ou {seg_por_falante/60:.1f} minutos "
            "de fala por falante**.")
        add("")
        add("| Ocorrências desejadas | Fala por falante |")
        add("|---|---|")
        for n in (10, 20, 30, 50):
            add(f"| {n} | {n/(por_min/60)/60:.1f} min |")
    add("")

    add("## Quantos falantes do corpus atual já satisfazem o piso")
    add("")
    faixas = defaultdict(int)
    for d in todos:
        ctx = d["explicitos"] + d["reduzidos"]
        if ctx >= 50:
            faixas["50 ou mais"] += 1
        elif ctx >= 30:
            faixas["30 a 49"] += 1
        elif ctx >= 10:
            faixas["10 a 29"] += 1
        else:
            faixas["menos de 10"] += 1
    add("| Contextos do falante | Falantes |")
    add("|---|---|")
    for faixa in ("50 ou mais", "30 a 49", "10 a 29", "menos de 10"):
        add(f"| {faixa} | {faixas[faixa]} |")
    add("")
    aptos = sum(v for k, v in faixas.items() if k != "menos de 10")
    add(f"**{aptos} de {len(todos)} falantes** têm hoje material suficiente para "
        f"que sua taxa seja estimável com {OCORRENCIAS_PARA_TAXA} ocorrências.")
    add("")

    add("## Por estado")
    add("")
    add("| UF | Arquivos | Falantes | Falantes com 10+ contextos |")
    add("|---|---|---|---|")
    por_uf = defaultdict(lambda: {"falantes": 0, "aptos": 0})
    for (_, uf, _, _), d in por_falante.items():
        por_uf[uf]["falantes"] += 1
        if d["explicitos"] + d["reduzidos"] >= OCORRENCIAS_PARA_TAXA:
            por_uf[uf]["aptos"] += 1
    for uf in sorted(por_uf):
        add(f"| {uf} | {len(por_estado_arquivos[uf])} | "
            f"{por_uf[uf]['falantes']} | {por_uf[uf]['aptos']} |")
    add("")

    add("## Ressalvas")
    add("")
    add("**A contagem é ortográfica, não fonética.** Mede contextos em que a")
    add("palatalização *pode* ocorrer, e não ocorrências dela — a realização exige")
    add("análise do áudio. É exatamente o que a meta precisa: quantas oportunidades")
    add("de observação o corpus oferece.")
    add("")
    add("**O contexto por redução é aproximado.** A regra adotada — `-te`/`-de`")
    add("final em palavra de mais de três letras — inclui casos que não reduzem e")
    add("exclui outros que reduzem. O erro é de segunda ordem para dimensionamento.")
    add("")
    add("**Falantes não são pessoas distintas entre arquivos.** A diarização rotula")
    add("locutores dentro de cada arquivo; o mesmo indivíduo em dois arquivos conta")
    add("duas vezes. Ver `docs/pendencias.md`, seção 6.4.")

    texto = "\n".join(L)
    (SAIDA / "densidade_palatalizacao.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
