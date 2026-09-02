#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Procura, nos arquivos versionados, nomes que a anonimização mascarou.

## Por que este verificador existe

Em 02/09/2026, ao preparar o envio do repositório, descobriu-se que a
documentação da própria etapa de anonimização citava dezessete nomes que a
etapa havia mascarado — entre eles os de uma prisão, de uma morte em confronto
policial e de um vazamento de foto pessoal. A máscara retira o nome da
transcrição; o documento o devolvia, e acompanhado da descrição do que fora
dito sobre a pessoa, o que é pior que o nome solto.

Nada chegou ao repositório remoto, porque a conferência foi feita antes do
envio. Mas a conferência foi manual, e uma conferência manual só pega o erro
quando alguém lembra de fazê-la.

## O que ele faz, e o que ele deliberadamente não faz

Varre os arquivos sob controle de versão em busca de cada nome com decisão
`mascarar` na planilha de anonimização, e sai com código diferente de zero se
achar algum.

**Ele produz falso positivo, e isso é intencional.** Muitos nomes mascarados
são também topônimo, nome de canal ou sobrenome de autor citado: "Paulo Afonso"
é cidade da Bahia, "Marechal Hermes" é bairro do Rio, "Mário Frade" é nome de
canal, "Santa Rita" é município da Paraíba. O verificador não tenta distinguir
— distinguir exigiria o julgamento que ele existe para provocar. Ele aponta, e
uma pessoa decide.

Por isso a lista de dispensas fica em arquivo à parte e cada entrada carrega o
motivo: uma dispensa sem motivo escrito é indistinguível de um vazamento que
alguém preferiu não olhar.

## Uso

    python verificar_nomes_versionados.py
    python verificar_nomes_versionados.py --proposta caminho/da/planilha.json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Dispensas conferidas em 02/09/2026, com o motivo de cada uma. O nome do canal
# é preservado por decisão do protocolo (§1.4.2), e topônimo não é pessoa.
DISPENSAS = {
    "Afonso": "Paulo Afonso, município da Bahia",
    "Hermes": "Marechal Hermes, bairro do Rio de Janeiro",
    "Rita": "Santa Rita, município da Paraíba",
    "José": "São José de Piranhas (município) e José Rogério Fontenele Bessa (autor do ALECE)",
    "André": "Santo André, município de São Paulo",
    "Mário": "Mário Frade, nome de canal — preservado pelo protocolo",
    "Renato": "Carona Com Renato, nome de canal — preservado pelo protocolo",
    "Juca": "Alô Juca, nome de programa da TV Aratu",
    "Henrique": "Pedro Henrique Sousa dos Santos, autor citado em referencias.bib",
    "Maria": "sobrenome de autora citada em referencias.bib",
    "Lula": "token numa lista de probabilidades do modelo, em smoke_test.json",
}

# Os planos de coleta guardam o título público do vídeo, e alguns títulos
# nomeiam pessoas mascaradas na transcrição. É tensão de desenho registrada em
# docs/pendencias.md, e não descuido: ver o item sobre título de vídeo.
ARQUIVOS_COM_TITULO_PUBLICO = (
    "plano_piloto.json", "plano_resto.json", "plano_fatia.json",
)


def nomes_mascarados(proposta: Path) -> list[str]:
    itens = json.loads(proposta.read_text(encoding="utf-8"))
    nomes = {i["nome_detectado"] for i in itens if i.get("decisao") == "mascarar"}
    return sorted((n for n in nomes if len(n) >= 4), key=len, reverse=True)


def _git(*argumentos: str, cwd: Path | None = None) -> str:
    """Roda git e decodifica a saída como UTF-8.

    O `text=True` sozinho decodifica na codificação do console, que no Windows
    é cp1252 e quebra em caminho acentuado — este repositório vive sob "Área de
    Trabalho". O erro não é silencioso: a leitura estoura antes de qualquer
    verificação, o que é o comportamento certo para uma ferramenta cuja falha
    seria confundida com ausência de vazamento.
    """
    return subprocess.run(["git", *argumentos], capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          cwd=cwd).stdout or ""


def raiz_do_repositorio() -> Path:
    saida = _git("rev-parse", "--show-toplevel").strip()
    return Path(saida) if saida else Path(".")


def arquivos_versionados() -> list[Path]:
    """Todos os arquivos versionados do repositório, e não só os do diretório atual.

    `git ls-files` sem argumento lista a partir do diretório corrente, o que
    faria a varredura passar por 19 arquivos em vez de 78 quando rodada de
    dentro de `pipeline_coleta_piloto/` — e sair verde por não ter olhado.
    """
    raiz = raiz_do_repositorio()
    saida = _git("ls-files", cwd=raiz)
    return [raiz / f for f in saida.splitlines() if f.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--proposta",
                    default="dataset_raw/anonimizacao_proposta.json",
                    help="Planilha de anonimização, de onde saem os nomes")
    args = ap.parse_args()

    caminho = Path(args.proposta)
    if not caminho.exists():
        print(f"planilha não encontrada em {caminho}; nada a verificar.")
        return 0

    nomes = nomes_mascarados(caminho)
    achados: dict[str, list[str]] = {}
    titulos: dict[str, list[str]] = {}

    raiz = raiz_do_repositorio()
    versionados = arquivos_versionados()
    for arquivo in versionados:
        try:
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        encontrados = [
            n for n in nomes
            if n not in DISPENSAS
            and re.search(rf"(?<![\w]){re.escape(n)}(?![\w])", texto)
        ]
        if not encontrados:
            continue
        relativo = str(arquivo.relative_to(raiz)).replace("\\", "/")
        alvo = titulos if arquivo.name in ARQUIVOS_COM_TITULO_PUBLICO else achados
        alvo[relativo] = encontrados

    if titulos:
        print("TÍTULOS PÚBLICOS DE VÍDEO — conhecido e registrado, não bloqueia:")
        for arquivo, ns in sorted(titulos.items()):
            print(f"  {arquivo}: {', '.join(sorted(ns))}")
        print()

    if not achados:
        print(f"{len(nomes)} nome(s) mascarado(s) verificado(s) contra "
              f"{len(versionados)} arquivo(s) versionado(s): nenhum vazamento.")
        return 0

    print("VAZAMENTO: nome mascarado presente em arquivo versionado.")
    for arquivo, ns in sorted(achados.items()):
        print(f"  {arquivo}: {', '.join(sorted(ns))}")
    print()
    print("Descreva a pessoa pelo papel, sem nomeá-la, ou acrescente a dispensa")
    print("em DISPENSAS com o motivo escrito, se for homônimo ou topônimo.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
