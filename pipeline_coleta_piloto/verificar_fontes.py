"""
verificar_fontes.py

Triagem automatizada da regra de atribuição descrita em `docs/fontes_coleta.md`,
seção 1: `estado_alvo` é atribuído pelo canal, nunca pela consulta de busca.

Para criadores independentes, sem vínculo institucional com o estado, a regra
exige menção recorrente a municípios identificáveis do estado no conteúdo
recente. Este módulo executa essa checagem sobre os títulos dos vídeos mais
recentes de cada canal candidato.

O resultado é uma triagem, não um veredito. Canais aprovados aqui ainda devem
ser inspecionados por uma pessoa antes de entrar em `fontes.json`; o que o
script garante é que nenhum canal entre sem evidência registrada, e que a
evidência fique auditável.

Uso:
    python verificar_fontes.py UCxxxx:CE UCyyyy:PB ...
    python verificar_fontes.py --arquivo candidatos.txt
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter

N_TITULOS = 12          # títulos recentes inspecionados por canal
MIN_MENCOES = 2         # menções necessárias para aceitação automática

# ---------------------------------------------------------------------------
# Municípios de referência por estado. Lista deliberadamente parcial: cobre os
# de maior população e os já observados no levantamento. Ampliar conforme a
# coleta encontrar novos.
# ---------------------------------------------------------------------------
MUNICIPIOS = {
    "PB": ["João Pessoa", "Campina Grande", "Patos", "Sousa", "Cajazeiras", "Guarabira",
           "Bayeux", "Santa Rita", "Cabedelo", "Puxinanã", "Monteiro", "Pombal",
           "Esperança", "Areia", "Sapé", "Itabaiana", "Paraíba"],
    "PE": ["Recife", "Olinda", "Jaboatão", "Caruaru", "Petrolina", "Garanhuns",
           "Serra Talhada", "Vitória de Santo Antão", "Camaragibe", "Paulista",
           "Gravatá", "Sanharó", "Belo Jardim", "Arcoverde", "Salgueiro",
           "Nazaré da Mata", "Pernambuco"],
    "CE": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Sobral", "Crato", "Maracanaú",
           "Quixadá", "Iguatu", "Itapipoca", "Aracati", "Canindé", "Pacujá",
           "Barbalha", "Crateús", "Tianguá", "Cariri", "Ceará"],
    "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari", "Itabuna",
           "Ilhéus", "Juazeiro", "Barreiras", "Jacobina", "Serrolândia",
           "Conceição do Coité", "Lençóis", "Irecê", "Alagoinhas", "Paulo Afonso",
           "Senhor do Bonfim", "Chapada Diamantina", "Bahia"],
    "SP": ["São Paulo", "Campinas", "Ribeirão Preto", "Sorocaba", "Santos",
           "São José do Rio Preto", "Bauru", "Piracicaba", "Osasco", "Guarulhos",
           "Santo André", "São Bernardo", "Marília", "Araraquara", "Jundiaí", "Franca",
           "Presidente Prudente", "Araçatuba", "Limeira", "Taubaté", "Barueri",
           "São José dos Campos", "Diadema", "Mauá", "Carapicuíba", "Itaquaquecetuba",
           # Bairros e distritos da capital — ver nota sobre gazeteiro urbano
           "Tatuapé", "Itaquera", "Capão Redondo", "Brasilândia", "Grajaú",
           "Guaianases", "Sapopemba", "Pirituba", "Cidade Tiradentes",
           "São Miguel Paulista", "Paraisópolis", "Heliópolis", "Jardim Ângela",
           "Campo Limpo", "Butantã", "Ipiranga", "Mooca", "Santo Amaro",
           "Interlagos", "Jabaquara", "Vila Madalena", "Perus", "M'Boi Mirim",
           "Cidade Ademar", "Freguesia do Ó", "Casa Verde", "Vila Prudente",
           "Anália Franco", "Aricanduva", "Parelheiros", "Tremembé",
           # Ambíguos com o Rio — o próprio script exige confirmação extra
           "Penha", "Lapa", "Santana", "Zona Leste", "Zona Norte", "Zona Sul"],
    "RJ": ["Rio de Janeiro", "Niterói", "São Gonçalo", "Duque de Caxias", "Nova Iguaçu",
           "Campos dos Goytacazes", "Petrópolis", "Volta Redonda", "Macaé",
           "Belford Roxo", "Magé", "Itaboraí", "Nilópolis", "Mesquita",
           "Angra dos Reis", "Cabo Frio", "Baixada Fluminense", "São João de Meriti",
           "Nova Friburgo", "Teresópolis", "Queimados", "Japeri", "Maricá",
           "Barra Mansa", "Resende", "Itaguaí", "Seropédica", "Rio das Ostras",
           # Bairros da capital
           "Madureira", "Bangu", "Realengo", "Campo Grande", "Santa Cruz",
           "Jacarepaguá", "Irajá", "Méier", "Tijuca", "Copacabana", "Ipanema",
           "Botafogo", "Flamengo", "Vila Isabel", "Bonsucesso", "Ramos", "Olaria",
           "Cordovil", "Pavuna", "Anchieta", "Guadalupe", "Deodoro",
           "Marechal Hermes", "Cascadura", "Piedade", "Engenho de Dentro",
           "Todos os Santos", "Vila da Penha", "Freguesia", "Recreio", "Barra da Tijuca",
           "Ilha do Governador", "Complexo do Alemão", "Rocinha", "Cidade de Deus",
           "Maré", "Vidigal", "subúrbio carioca",
           # Ambíguos com São Paulo
           "Penha", "Lapa", "Santana", "Zona Leste", "Zona Norte", "Zona Sul"],
}

# Termos geográficos que NÃO identificam estado. A presença deles é justamente
# o que levou à rejeição do canal "Adailton no sertão" (docs/fontes_coleta.md, 1.2).
TERMOS_AMBIGUOS = ["sertão", "roça", "caatinga", "nordeste", "interior", "agreste", "sítio"]

# ---------------------------------------------------------------------------
# Sinais de risco identificados na revisão manual de 27/08/2026, quando se
# constatou que a checagem geográfica sozinha aceitava canais impróprios.
# Ver docs/fontes_coleta.md, seção 2.4.
#
# Presença geográfica não implica residência, nem fala humana, nem fala alguma.
# Estes padrões não rejeitam por si; rebaixam o veredito para REVISAR, porque
# distinguir um morador de um viajante exige julgamento humano.
# ---------------------------------------------------------------------------
SINAIS_DE_RISCO = {
    "itinerante": [
        "viagem", "viajando", "viajei", "motovlog", "rodovia", "br-", "trecho",
        "cruzando", "percorr", "turismo", "guia de viagem", "o que fazer em",
        "vale a pena morar", "onde morar", "caminhoneiro", "carreta", "estrada",
    ],
    "narracao_possivelmente_sintetica": [
        "as 10 melhores", "as 15 piores", "ranking", "proibido", "segredo",
        "voce nao sabia", "top 5", "top 10", "descubra", "voce precisa conhecer",
        "codigo secreto", "a verdade por tras",
    ],
    "possivelmente_sem_fala": [
        "walk", "4k", "pov", "tour pelas principais ruas", "passeando pelo",
        "drone", "imagens de", "timelapse",
    ],
}


def _norm(texto: str) -> str:
    """Minúsculas, sem acento — para casar título e município de forma robusta."""
    s = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# Municípios cujo nome ocorre em mais de um estado da lista. Exigem confirmação
# adicional: ou a sigla do estado no título, ou um segundo município não ambíguo.
_contagem = Counter(_norm(m) for lista in MUNICIPIOS.values() for m in lista)
AMBIGUOS = {m for m, n in _contagem.items() if n > 1}


def titulos_recentes(channel_id: str, n: int = N_TITULOS) -> list[str]:
    """Títulos dos n vídeos mais recentes do canal, via yt-dlp."""
    cmd = [
        "yt-dlp", f"https://www.youtube.com/channel/{channel_id}/videos",
        "--flat-playlist", "-I", f"1:{n}",
        "--extractor-args", "youtube:lang=pt",
        "--print", "%(title)s",
    ]
    try:
        saida = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                               encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return []
    return [linha for linha in saida.stdout.splitlines() if linha.strip()]


def avaliar(channel_id: str, estado: str) -> dict:
    """
    Aplica a regra de atribuição a um canal candidato.

    Devolve o veredito e a evidência que o sustenta, de modo que a decisão
    permaneça auditável mesmo depois de o canal entrar em fontes.json.
    """
    if estado not in MUNICIPIOS:
        raise ValueError(f"Estado fora do escopo do projeto: {estado}")

    titulos = titulos_recentes(channel_id)
    if not titulos:
        return {"channel_id": channel_id, "estado": estado, "veredito": "INDISPONIVEL",
                "motivo": "não foi possível recuperar títulos", "evidencia": []}

    blob = _norm(" | ".join(titulos))

    encontrados, ambiguos_vistos = [], []
    for municipio in MUNICIPIOS[estado]:
        m = _norm(municipio)
        if re.search(rf"\b{re.escape(m)}\b", blob):
            (ambiguos_vistos if m in AMBIGUOS else encontrados).append(municipio)

    tem_sigla = bool(re.search(rf"\b{estado.lower()}\b", blob))
    genericos = [t for t in TERMOS_AMBIGUOS if _norm(t) in blob]

    # Municípios ambíguos só contam se houver sigla do estado ou município próprio.
    if ambiguos_vistos and (tem_sigla or encontrados):
        encontrados.extend(ambiguos_vistos)

    # Sinais de risco: fração dos títulos que casa com cada padrão.
    riscos = {}
    for nome_risco, padroes in SINAIS_DE_RISCO.items():
        n = sum(1 for t in titulos if any(p in _norm(t) for p in padroes))
        if n >= max(2, len(titulos) // 3):
            riscos[nome_risco] = n

    if len(encontrados) >= MIN_MENCOES or (encontrados and tem_sigla):
        if riscos:
            detalhe = "; ".join(f"{k} ({v}/{len(titulos)} títulos)" for k, v in riscos.items())
            return {"channel_id": channel_id, "estado": estado, "veredito": "REVISAR",
                    "motivo": f"geografia confere, mas há sinal de {detalhe}",
                    "evidencia": encontrados, "riscos": riscos,
                    "sigla_no_titulo": tem_sigla, "n_titulos": len(titulos)}
        veredito, motivo = "ACEITO", f"{len(encontrados)} município(s) do estado nos títulos recentes"
    elif encontrados:
        veredito, motivo = "REVISAR", "menção única; confirmar manualmente"
    elif genericos:
        veredito, motivo = ("REJEITADO",
                            f"apenas termos geográficos ambíguos ({', '.join(genericos)}), "
                            "que não identificam estado")
    else:
        veredito, motivo = "REJEITADO", "nenhum marcador geográfico nos títulos recentes"

    return {"channel_id": channel_id, "estado": estado, "veredito": veredito,
            "motivo": motivo, "evidencia": encontrados,
            "sigla_no_titulo": tem_sigla, "n_titulos": len(titulos)}


def main(argv: list[str]) -> None:
    if not argv:
        print(__doc__)
        sys.exit(1)

    if argv[0] == "--arquivo":
        pares = [l.strip() for l in open(argv[1], encoding="utf-8") if l.strip()]
    else:
        pares = argv

    resultados = []
    for par in pares:
        cid, _, uf = par.partition(":")
        r = avaliar(cid, uf.upper())
        resultados.append(r)
        ev = ", ".join(r["evidencia"]) or "—"
        print(f"{r['veredito']:12s} {r['estado']} {r['channel_id']}  [{ev}]  {r['motivo']}")

    print("\n" + json.dumps(resultados, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
