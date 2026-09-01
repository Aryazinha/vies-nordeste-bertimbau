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
from collections import Counter, defaultdict
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
# Qualificadores que **precedem** o nome no texto e o marcam como figura
# pública. Ficam fora da entidade que o reconhecedor devolve — ele captura
# "Felca", não "O influenciador Felca" —, e por isso precisam ser procurados no
# contexto, e não no nome. Foi assim que Felca escapou na primeira versão.
#
# Duas famílias, e a distinção entre elas é o que a regra do protocolo protege:
#
# - **cargo e autoridade**: quem exerce função pública, citado no exercício dela;
# - **notoriedade**: quem é conhecido do público e é citado pelo trabalho que o
#   tornou conhecido.
#
# Deliberadamente **fora** da lista: empresário, comerciante, morador, motorista,
# professor, estudante, aposentado, vítima, suspeito. Ser descrito por ocupação
# não faz de ninguém figura pública — é o caso mais comum de pessoa comum
# nomeada num telejornal, e é exatamente quem a regra protege.
QUALIFICADORES_PUBLICOS = (
    # cargo e autoridade
    "deputado", "deputada", "senador", "senadora", "vereador", "vereadora",
    "prefeito", "prefeita", "governador", "governadora", "presidente",
    "ministro", "ministra", "juiz", "juíza", "desembargador", "delegado",
    "delegada", "procurador", "promotor", "secretário", "secretária",
    # notoriedade
    "influenciador", "influenciadora", "influencer", "youtuber", "cantor",
    "cantora", "ator", "atriz", "artista", "jogador", "jogadora", "escritor",
    "escritora", "humorista", "músico", "compositor", "técnico do",
)

# Contexto que **desqualifica** a exceção de figura pública. Ser conhecido do
# público não retira a proteção sobre o que é matéria criminal ou de saúde: a
# regra do protocolo protege a esfera privada, e é justamente onde a menção
# fere que ela mais precisa valer.
#
# Encontrado em 01/09/2026, ao conferir a lista: "o influenciador Ítalo Santos
# e o companheiro Israel foram presos" tinha sido classificado como figura
# pública, e portanto preservado. O qualificador estava lá, mas o que a frase
# noticia é prisão — publicar o nome seria o oposto do que a regra pretende.
CONTEXTO_QUE_REMOVE_EXCECAO = (
    "preso", "presa", "presos", "detido", "detida", "acusado", "acusada",
    "suspeito", "suspeita", "investigado", "investigada", "condenado",
    "condenada", "réu", "ré", "indiciado", "homicídio", "assassinato",
    "estupro", "abuso", "tráfico", "crime", "delegacia", "presídio",
    "cadeia", "prisão", "denunciado", "denunciada", "vítima", "morreu",
    "internado", "internada", "diagnóstico", "doença",
)

CARGOS_PUBLICOS = ("deputado", "deputada", "vereador", "vereadora", "prefeito",
                   "prefeita", "governador", "governadora", "senador", "senadora",
                   "ministro", "ministra", "presidente", "delegado", "delegada",
                   "secretário", "secretária", "juiz", "juíza", "desembargador")

# --------------------------------------------------------------------------
# Política das quatro categorias, aprovada pela equipe em 01/09/2026
# --------------------------------------------------------------------------
# A regra do protocolo — mascarar nome de terceiro, não o do autor do vídeo —
# foi escrita pensando em vlog, onde alguém cita um amigo. A primeira varredura
# real mostrou que 80% dos nomes vêm de telejornal e vox-pop, onde o padrão de
# nomeação é outro: repórter se identifica, político é citado, entrevistado é
# nomeado no ar. Daí quatro categorias, e não uma:
#
#   autor_ou_equipe  -> manter   (repórter e apresentador são o análogo do autor)
#   figura_publica   -> manter   (cargo público em papel público)
#   nao_pessoa       -> manter   (mascarar corromperia o corpus)
#   terceiro         -> mascarar (entrevistado nomeado, citado em vlog — o caso da regra)
#
# Nenhuma classificação decide sozinha: todas viram sugestão, e a fase de
# aplicação segue recusando-se a gravar enquanto houver item não confirmado.
DECISAO_POR_CATEGORIA = {
    "autor_ou_equipe": "manter",
    "figura_publica": "manter",
    "nao_pessoa": "manter",
    "terceiro": "mascarar",
}

# Fórmulas com que jornalista se identifica ou é passado a palavra. Aparecem no
# contexto da menção, não no nome, e por isso são checadas sobre o trecho.
FORMULAS_DE_EQUIPE = (
    "com você", "com vocês", "traz o", "traz a", "direto de", "direto do",
    "nossa reportagem", "a reportagem de", "repórter", "reportagem do",
    "apresenta", "aqui é o", "aqui é a", "eu sou o", "eu sou a",
    "está no ar", "no comando", "ao vivo com", "passo a palavra",
    "informações com", "quem traz", "acompanha", "boa noite a todos",
    # Posse + função: "nosso cinegrafista Diego Azevedo" identifica equipe do
    # próprio canal tão claramente quanto a passagem de palavra, e foi o padrão
    # que mais escapou na primeira classificação.
    "nosso repórter", "nossa repórter", "nosso cinegrafista", "nossa equipe",
    "nosso comentarista", "nossa comentarista", "nosso colunista",
    "nossa colunista", "nosso produtor", "nossa produção", "nosso apresentador",
    "nossa apresentadora", "nosso correspondente", "nosso analista",
)

# Um nome que reaparece em arquivos distintos do MESMO canal é, quase sempre,
# quem trabalha ali — o entrevistado aparece uma vez e some. É o sinal mais
# barato e mais confiável disponível sem ouvir o áudio.
MIN_ARQUIVOS_PARA_EQUIPE = 2

# Distância máxima, em caracteres, entre a fórmula jornalística e a menção do
# nome para que uma explique a outra. Sem esta restrição a heurística disparava
# sobre a janela inteira e produzia erro grosseiro: em 01/09/2026 classificou
# "Meu Deus" como equipe do canal porque "nossa produção" aparecia na mesma
# frase, sem relação alguma com a interjeição.
DISTANCIA_MAXIMA_FORMULA = 45

# Palavras que antecedem o nome e que o reconhecedor engloba na entidade.
# "Meu Deus" precisa cair na lista de não-pessoas tanto quanto "Deus".
PREFIXOS_A_IGNORAR = ("meu", "minha", "nosso", "nossa", "o", "a", "os", "as",
                      "seu", "sua", "dona", "seu ", "dom", "dr", "dra")

# Camadas em que o padrão de nomeação é jornalístico. Num vlog, nome repetido é
# tão provavelmente um parente quanto um colega de trabalho, e a heurística de
# recorrência não vale.
CAMADAS_JORNALISTICAS = ("entrevista_vox_pop", "podcast_radio_tv_regional")

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
    """
    Nomes de pessoa detectados, com os trechos em que aparecem.

    O contexto inclui o segmento anterior e o seguinte, e não apenas aquele em
    que o nome caiu. A primeira revisão mostrou por quê: um quarto dos itens
    vinha com trecho curto demais para julgar — "um, manda a Matias" não diz se
    Matias é pessoa, bairro ou erro de transcrição —, e sem a vizinhança quem
    revisa teria de abrir o vídeo. A janela transforma a revisão em leitura, que
    é o que ela precisa ser para caber no tempo de alguém.
    """
    segmentos = [s["text"].strip() for s in reg["transcricao"]["segmentos"]]
    achados: dict[str, list[str]] = defaultdict(list)
    for i, texto in enumerate(segmentos):
        if not texto:
            continue
        for ent in nlp(texto).ents:
            if ent.label_ != "PER":
                continue
            nome = ent.text.strip()
            if len(nome) < 2:
                continue
            if len(achados[nome]) < CONTEXTOS_POR_NOME:
                janela = segmentos[max(0, i - 1): i + 2]
                achados[nome].append(" ".join(x for x in janela if x))
    return achados


def _qualificador_publico(nome: str, contextos: list[str]) -> str | None:
    """Qualificador de figura pública imediatamente antes da menção do nome."""
    alvo = nome.lower()
    for ctx in contextos:
        baixo = ctx.lower()
        inicio = baixo.find(alvo)
        if inicio < 0:
            continue
        antes = baixo[max(0, inicio - 30):inicio]
        for q in QUALIFICADORES_PUBLICOS:
            pos = antes.find(q)
            if pos < 0:
                continue
            # "jogador do Caxias" nomeia o clube, não o jogador: quando o
            # qualificador é seguido de "do"/"da" logo antes do nome, o que vem
            # depois é a instituição a que a pessoa pertence.
            entre = antes[pos + len(q):].strip()
            if entre in ("do", "da", "dos", "das"):
                continue
            return q
    return None


def _formula_perto_do_nome(nome: str, contextos: list[str]) -> str | None:
    """
    Fórmula jornalística a até `DISTANCIA_MAXIMA_FORMULA` caracteres da menção.

    A proximidade é o que distingue "nosso repórter Diego Azevedo", em que a
    fórmula qualifica o nome, de "Meu Deus. Mas a nossa produção...", em que as
    duas coisas apenas dividem a frase.
    """
    alvo = nome.lower()
    for ctx in contextos:
        baixo = ctx.lower()
        inicio = baixo.find(alvo)
        if inicio < 0:
            continue
        janela = baixo[max(0, inicio - DISTANCIA_MAXIMA_FORMULA):
                       inicio + len(alvo) + DISTANCIA_MAXIMA_FORMULA]
        for f in FORMULAS_DE_EQUIPE:
            if f in janela:
                return f
    return None


def classificar(nome: str, contextos: list[str], canal: str, tipo_fonte: str,
                permitidos: set[str], n_arquivos_do_nome: int) -> tuple[str, str]:
    """
    Aplica a política das quatro categorias. Devolve (categoria, motivo).

    A ordem importa: `nao_pessoa` vem primeiro porque mascarar ali corromperia
    o corpus, e `terceiro` fica por último como padrão — na dúvida, protege-se.
    """
    nl = nome.lower().strip()

    # "Meu Deus" e "Deus" são a mesma coisa para efeito de máscara.
    nucleo = nl
    for pref in PREFIXOS_A_IGNORAR:
        if nucleo.startswith(pref + " "):
            nucleo = nucleo[len(pref) + 1:].strip()
            break

    if nl in NAO_SAO_PESSOAS or nucleo in NAO_SAO_PESSOAS:
        return "nao_pessoa", "não é nome de pessoa — mascarar corromperia o corpus"

    if any(nl.startswith(c + " ") for c in CARGOS_PUBLICOS):
        return "figura_publica", "citado por cargo público em papel público"

    qual = _qualificador_publico(nome, contextos)
    if qual:
        blob = " ".join(contextos).lower()
        grave = [g for g in CONTEXTO_QUE_REMOVE_EXCECAO
                 if re.search(rf"\b{re.escape(g)}\b", blob)]
        if grave:
            return ("terceiro",
                    f"qualificado como figura pública ({qual!r}), mas a menção é "
                    f"matéria sensível ({grave[0]!r}) — a exceção não se aplica")
        return "figura_publica", f"qualificado como figura pública no texto ({qual!r})"

    partes = {p.lower() for p in re.findall(r"\w+", nome)}
    if partes & permitidos:
        return "autor_ou_equipe", "coincide com o nome do canal — provável autor"

    if tipo_fonte in CAMADAS_JORNALISTICAS:
        if n_arquivos_do_nome >= MIN_ARQUIVOS_PARA_EQUIPE:
            return ("autor_ou_equipe",
                    f"reaparece em {n_arquivos_do_nome} arquivos do mesmo canal — "
                    "padrão de quem trabalha ali, não de entrevistado")
        achada = _formula_perto_do_nome(nome, contextos)
        if achada:
            return ("autor_ou_equipe",
                    f"fórmula jornalística junto ao nome ({achada!r})")

    return "terceiro", "terceiro nomeado — é o caso que a regra do protocolo protege"


def propor(registros: list[tuple[str, dict]], autores: dict[str, list[str]],
           saida: Path) -> None:
    """
    Fase 1 — monta a planilha de revisão humana.

    Roda em dois passes porque a recorrência de um nome entre arquivos do mesmo
    canal só é conhecida depois de varrer todos: é justamente esse sinal que
    separa o repórter, que reaparece, do entrevistado, que aparece uma vez.
    """
    nlp = _get_ner()

    # Passe 1 — detecção
    achados = []
    for nome_arquivo, reg in registros:
        for nome, contextos in nomes_do_registro(reg, nlp).items():
            achados.append((nome_arquivo, reg, nome, contextos))

    # Quantos arquivos distintos do mesmo canal mencionam cada nome
    por_canal_nome: dict[tuple[str, str], set[str]] = defaultdict(set)
    for nome_arquivo, reg, nome, _ in achados:
        por_canal_nome[(reg.get("canal", ""), nome)].add(nome_arquivo)

    # Passe 2 — classificação
    itens = []
    for nome_arquivo, reg, nome, contextos in achados:
        canal = reg.get("canal", "")
        permitidos = _tokens_do_canal(canal) | {n.lower() for n in autores.get(canal, [])}
        n_arq = len(por_canal_nome[(canal, nome)])
        categoria, motivo = classificar(nome, contextos, canal,
                                        reg.get("tipo_fonte", ""), permitidos, n_arq)
        sugestao = DECISAO_POR_CATEGORIA[categoria]
        itens.append({
            "arquivo": nome_arquivo,
            "id": reg.get("id"),
            "canal": canal,
            "estado_alvo": reg.get("estado_alvo"),
            "tipo_fonte": reg.get("tipo_fonte"),
            "nome_detectado": nome,
            "categoria": categoria,
            "arquivos_do_canal_com_este_nome": n_arq,
            "sugestao": sugestao,
            "motivo_sugestao": motivo,
            "contextos": contextos,
            "decisao": sugestao,      # a revisar: "mascarar" | "manter"
            "confirmado": False,      # a pessoa que revisou marca true
        })

    saida.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")

    por_cat = Counter(i["categoria"] for i in itens)
    n_mascarar = sum(1 for i in itens if i["sugestao"] == "mascarar")
    print(f"{len(itens)} nome(s) detectado(s) em {len(registros)} arquivo(s).")
    print()
    print("Por categoria:")
    for cat, n in por_cat.most_common():
        print(f"  {n:4d}  {cat}  ->  {DECISAO_POR_CATEGORIA[cat]}")
    print()
    print(f"{n_mascarar} para mascarar, {len(itens) - n_mascarar} para manter.")
    print(f"Planilha em {saida}.")
    print("Revise — ajuste 'decisao' e marque 'confirmado': true.")
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
