"""
anonimizar_transcricao.py

Implementa a anonimização exigida pela seção 1.4.2 do protocolo
(`docs/protocolo.md`): nomes próprios **de terceiros** mencionados nas
transcrições são mascarados antes de qualquer publicação do conjunto; o nome
do autor do vídeo, não. É pré-condição técnica da decisão de 31/08/2026, que
autorizou publicar as transcrições desde que anonimizadas
(`docs/ficha_conjunto.md`, A.6).

## Por que o script não decide sozinho

Mesma razão de `verificar_reincidencia.py` e `preparar_amostra_coerencia.py`:
o erro automático aqui é assimétrico e caro. Um nome que escapa da máscara é
dado pessoal publicado; uma palavra comum mascarada por engano é corpus
corrompido em silêncio. Três fontes de erro são esperadas, e nenhuma é
hipotética:

1. **O reconhecedor de entidades é treinado em texto formal.** Os modelos de
   português do spaCy vêm de corpora jornalísticos; a entrada aqui é fala
   espontânea de rua, transcrita por ASR, com pontuação e capitalização
   irregulares. O desempenho é pior do que a documentação do modelo sugere.
2. **Apelido regional não é nome próprio para o modelo.** Tratamento, alcunha
   e forma reduzida ("seu Zé", "Nêga") são exatamente o que a fala espontânea
   usa e o que o reconhecedor mais perde.
3. **Falso positivo por capitalização.** Palavra comum em início de frase, ou
   topônimo, entra como pessoa com frequência.

Por isso a operação tem duas fases, e a segunda **recusa-se a executar**
enquanto houver item não conferido por uma pessoa.

## As duas fases

    # 1. propõe: varre as transcrições e monta a lista para revisão
    python anonimizar_transcricao.py --fase propor --entrada "piloto_resultados (2).zip"

    # (uma pessoa abre anonimizacao_proposta.json, ajusta 'decisao' e
    #  marca 'confirmado': true em cada item)

    # 2. aplica: grava cópias anonimizadas, sem tocar no original
    python anonimizar_transcricao.py --fase aplicar --entrada "piloto_resultados (2).zip"

O original nunca é sobrescrito: a fase de aplicação escreve em um diretório de
saída próprio. O material bruto continua fora do versionamento, como sempre
esteve.

## Quem é o autor, e por que isso não se resolve sozinho

A regra manda preservar o nome do autor do vídeo e mascarar o de terceiros.
`fontes.json` registra o nome do **canal**, que nem sempre é o nome da pessoa
("Vlog com Diogo" sugere Diogo; "38313067" não sugere nada). O script usa os
tokens do nome do canal apenas para **sugerir** `manter`, e a sugestão é
palpite explícito, a ser confirmado. Uma lista curada pode ser fornecida em
`--autores autores.json`, no formato `{"nome do canal": ["Diogo", "Diogo Silva"]}`.

## Convenção de máscara

Por padrão, cada nome distinto de um mesmo arquivo recebe um marcador estável
— `[NOME_1]`, `[NOME_2]` —, o que preserva a estrutura do discurso (duas
menções ao mesmo referente continuam ligadas) sem identificar ninguém. É
informação que interessa a uso linguístico do corpus e que o marcador único
destruiria. Para uniformizar tudo em `[NOME]`, use `--placeholder-unico`.

A máscara é aplicada tanto ao texto do segmento quanto à lista de palavras com
marcação temporal — se só o primeiro fosse tratado, o nome continuaria legível
no segundo. Como cada palavra é uma entrada própria, um nome composto produz
marcadores repetidos em sequência no nível da palavra ("Maria da Silva" vira
`[NOME_1] [NOME_1]`, sem o conectivo). É consequência do alinhamento por
palavra, não defeito: cada entrada preserva o seu próprio par de tempos.

Instalação da dependência:
    pip install spacy && python -m spacy download pt_core_news_lg
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

# Conectivos que compõem nome próprio ("Maria da Silva") mas que, isolados,
# não devem ser mascarados no nível da palavra — mascará-los apagaria
# preposições do corpus inteiro.
CONECTIVOS = {"da", "de", "do", "das", "dos", "e"}

# Palavras genéricas de nome de canal. Sem esta lista, "Vlog com Diogo" ofereceria
# "vlog" e "com" como possíveis nomes do autor, e qualquer terceiro assim chamado
# na fala seria sugerido para *preservar* — erro na direção perigosa.
GENERICOS_DE_CANAL = {
    "vlog", "vlogs", "canal", "oficial", "tv", "tve", "web", "rádio", "radio",
    "podcast", "com", "por", "the", "meu", "minha", "nosso", "nossa", "news",
    "notícias", "noticias", "jornal", "programa", "produções", "producoes",
    "filmes", "vida", "mundo", "brasil", "br", "hd", "top", "real",
}

# Quantos trechos de contexto acompanham cada nome na planilha de revisão.
# Suficiente para julgar se é pessoa, sem despejar a transcrição inteira.
CONTEXTOS_POR_NOME = 3

# Falsos positivos observados na primeira varredura real, em 01/09/2026: o
# reconhecedor marcou como pessoa 21 ocorrências de palavra que pessoa não é.
# Mascará-las não seria apenas esforço desperdiçado de revisão — seria
# **corromper o corpus**, porque `Deus`, `rapaz` e `oxe` são material
# linguístico do próprio objeto de estudo, e não dado pessoal a proteger.
NAO_SAO_PESSOAS = {
    # interjeição e vocativo, frequentes na fala nordestina que o projeto estuda
    "rapaz", "oxe", "eita", "vixe", "menino", "mainha", "painho", "visse",
    "bora", "certo", "pronto", "valeu", "olha", "opa",
    # religioso, que o reconhecedor toma por antropônimo
    "deus", "jesus", "cristo", "senhor", "nossa senhora", "maria santíssima",
    # plataformas e marcas
    "instagram", "youtube", "whatsapp", "facebook", "tiktok", "google",
    "uber", "ifood", "pix", "globo", "sbt", "record", "band",
    # topônimos e gentílicos que o modelo às vezes classifica como pessoa
    "brasil", "nordeste", "sudeste", "sertão", "agreste",
}

# Nome de figura pública em papel público não é o que a seção 1.4.2 do
# protocolo manda proteger — a regra visa terceiro identificável na fala
# cotidiana, não o presidente citado num telejornal. Mascarar essas menções
# destruiria o sentido do trecho sem proteger ninguém. A sugestão é `manter`,
# e a decisão continua sendo de quem revisa.
CARGOS_PUBLICOS = ("deputado", "deputada", "vereador", "vereadora", "prefeito",
                   "prefeita", "governador", "governadora", "senador", "senadora",
                   "ministro", "ministra", "presidente", "delegado", "delegada",
                   "secretário", "secretária", "juiz", "juíza", "desembargador")

ARQUIVO_PROPOSTA = "anonimizacao_proposta.json"


def _get_ner():
    """Carrega o reconhecedor de entidades do spaCy, preferindo o modelo maior."""
    import spacy
    for modelo in ("pt_core_news_lg", "pt_core_news_sm"):
        try:
            nlp = spacy.load(modelo, disable=["lemmatizer", "textcat"])
            if modelo.endswith("_sm"):
                print("AVISO: usando pt_core_news_sm, menos preciso que pt_core_news_lg. "
                      "A revisão humana passa a ser ainda mais necessária.")
            return nlp
        except OSError:
            continue
    raise SystemExit(
        "Nenhum modelo de português do spaCy encontrado. Instale com:\n"
        "    python -m spacy download pt_core_news_lg")


def carregar_registros(entrada: Path) -> list[tuple[str, dict]]:
    """Lê os registros finais de um .zip ou de um diretório. Devolve (nome, registro)."""
    if entrada.suffix == ".zip":
        with zipfile.ZipFile(entrada) as z:
            return [(n, json.loads(z.read(n)))
                    for n in sorted(z.namelist()) if n.endswith(".json")]
    if entrada.is_dir():
        return [(c.name, json.loads(c.read_text(encoding="utf-8")))
                for c in sorted(entrada.glob("*.json"))]
    raise SystemExit(f"{entrada} não é .zip nem diretório.")


def _tokens_do_canal(canal: str) -> set[str]:
    """Tokens do nome do canal que podem ser o nome do autor — palpite, não fato."""
    return {t.lower() for t in re.findall(r"\w+", canal)
            if len(t) > 2 and t.lower() not in CONECTIVOS
            and t.lower() not in GENERICOS_DE_CANAL and not t.isdigit()}


def nomes_do_registro(reg: dict, nlp) -> dict[str, list[str]]:
    """Nomes de pessoa detectados, com os trechos em que aparecem."""
    achados: dict[str, list[str]] = defaultdict(list)
    for seg in reg["transcricao"]["segmentos"]:
        texto = seg["text"].strip()
        if not texto:
            continue
        for ent in nlp(texto).ents:
            if ent.label_ != "PER":
                continue
            nome = ent.text.strip()
            if len(nome) < 2:
                continue
            if len(achados[nome]) < CONTEXTOS_POR_NOME:
                achados[nome].append(texto)
    return achados


def propor(registros: list[tuple[str, dict]], autores: dict[str, list[str]],
           saida: Path) -> None:
    """Fase 1 — monta a planilha de revisão humana."""
    nlp = _get_ner()
    itens = []
    for nome_arquivo, reg in registros:
        canal = reg.get("canal", "")
        permitidos = _tokens_do_canal(canal) | {
            n.lower() for n in autores.get(canal, [])}
        for nome, contextos in nomes_do_registro(reg, nlp).items():
            nl = nome.lower().strip()
            partes = {p.lower() for p in re.findall(r"\w+", nome)}
            if nl in NAO_SAO_PESSOAS:
                sugestao, motivo = "manter", "não é nome de pessoa — mascarar corromperia o corpus"
            elif any(nl.startswith(c + " ") for c in CARGOS_PUBLICOS):
                sugestao, motivo = "manter", "figura pública em papel público; a regra visa terceiro na fala cotidiana"
            elif partes & permitidos:
                sugestao, motivo = "manter", "coincide com o nome do canal — provável autor"
            else:
                sugestao, motivo = "mascarar", "não coincide com o nome do canal"
            itens.append({
                "arquivo": nome_arquivo,
                "id": reg.get("id"),
                "canal": canal,
                "estado_alvo": reg.get("estado_alvo"),
                "nome_detectado": nome,
                "sugestao": sugestao,
                "motivo_sugestao": motivo,
                "contextos": contextos,
                "decisao": sugestao,      # a revisar: "mascarar" | "manter"
                "confirmado": False,      # a pessoa que revisou marca true
            })

    saida.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")
    n_mascarar = sum(1 for i in itens if i["sugestao"] == "mascarar")
    print(f"{len(itens)} nome(s) detectado(s) em {len(registros)} arquivo(s): "
          f"{n_mascarar} sugerido(s) para máscara, {len(itens) - n_mascarar} para manter.")
    print(f"Planilha em {saida}.")
    print("Revise cada item — ajuste 'decisao' e marque 'confirmado': true.")
    print("A fase de aplicação recusa-se a rodar enquanto houver item não confirmado.")


def _mascarar_texto(texto: str, mapa: dict[str, str]) -> str:
    """Substitui cada nome e cada parte dele pelo marcador correspondente."""
    for nome, marcador in mapa.items():
        texto = re.sub(rf"\b{re.escape(nome)}\b", marcador, texto, flags=re.IGNORECASE)
        for parte in re.findall(r"\w+", nome):
            if parte.lower() in CONECTIVOS or len(parte) < 3:
                continue
            texto = re.sub(rf"\b{re.escape(parte)}\b", marcador, texto, flags=re.IGNORECASE)
    return texto


def aplicar(registros: list[tuple[str, dict]], proposta: list[dict],
            destino: Path, placeholder_unico: bool) -> None:
    """Fase 2 — grava cópias anonimizadas, após conferir que tudo foi revisado."""
    pendentes = [i for i in proposta if not i.get("confirmado")]
    if pendentes:
        raise SystemExit(
            f"{len(pendentes)} de {len(proposta)} item(ns) sem 'confirmado': true. "
            "Nada foi escrito. Conclua a revisão antes de aplicar.")

    por_arquivo: dict[str, list[str]] = defaultdict(list)
    for item in proposta:
        if item["decisao"] == "mascarar":
            por_arquivo[item["arquivo"]].append(item["nome_detectado"])

    destino.mkdir(parents=True, exist_ok=True)
    total_nomes = 0
    for nome_arquivo, reg in registros:
        nomes = sorted(set(por_arquivo.get(nome_arquivo, [])), key=len, reverse=True)
        mapa = {n: ("[NOME]" if placeholder_unico else f"[NOME_{i}]")
                for i, n in enumerate(nomes, start=1)}
        total_nomes += len(mapa)

        for seg in reg["transcricao"]["segmentos"]:
            seg["text"] = _mascarar_texto(seg["text"], mapa)
            for palavra in seg.get("words", []):
                palavra["word"] = _mascarar_texto(palavra["word"], mapa)

        reg["anonimizado"] = True
        reg["nomes_mascarados"] = len(mapa)

        # Verificação de sobrevivência: nome que resistiu à máscara é vazamento,
        # e a falha deve ser ruidosa. Casos esperados aqui são nome grafado de
        # forma diferente no nível da palavra e da frase.
        corpo = json.dumps(reg, ensure_ascii=False)
        sobreviventes = [n for n in nomes
                         if re.search(rf"\b{re.escape(n)}\b", corpo, flags=re.IGNORECASE)]
        if sobreviventes:
            raise SystemExit(
                f"{nome_arquivo}: {sobreviventes} sobreviveram à máscara. "
                "Nada mais foi escrito — corrija o script antes de prosseguir.")

        (destino / nome_arquivo).write_text(
            json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(registros)} arquivo(s) anonimizado(s) em {destino}, "
          f"{total_nomes} nome(s) mascarado(s) ao todo.")
    print("O material original não foi alterado.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fase", required=True, choices=["propor", "aplicar"])
    ap.add_argument("--entrada", required=True,
                    help="Zip de resultados ou diretório de registros finais")
    ap.add_argument("--proposta", default=ARQUIVO_PROPOSTA,
                    help=f"Planilha de revisão (padrão: {ARQUIVO_PROPOSTA})")
    ap.add_argument("--destino", default="registros_anonimizados",
                    help="Diretório de saída da fase 'aplicar'")
    ap.add_argument("--autores", default=None,
                    help="JSON com nomes de autor por canal, a preservar")
    ap.add_argument("--placeholder-unico", action="store_true",
                    help="Usa [NOME] para todos, em vez de [NOME_1], [NOME_2]...")
    args = ap.parse_args()

    registros = carregar_registros(Path(args.entrada))
    if not registros:
        raise SystemExit(f"nenhum registro encontrado em {args.entrada}")

    if args.fase == "propor":
        autores = json.loads(Path(args.autores).read_text(encoding="utf-8")) if args.autores else {}
        propor(registros, autores, Path(args.proposta))
    else:
        caminho = Path(args.proposta)
        if not caminho.exists():
            raise SystemExit(f"{caminho} não existe. Rode a fase 'propor' primeiro.")
        aplicar(registros, json.loads(caminho.read_text(encoding="utf-8")),
                Path(args.destino), args.placeholder_unico)


if __name__ == "__main__":
    main()
