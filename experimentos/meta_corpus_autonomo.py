"""
meta_corpus_autonomo.py — meta de volume do corpus como entregável autônomo

Substitui `meta_volume_corpus.py`, que derivava a meta de uma função que o corpus
deixou de ter. Em 29/08/2026 a equipe decidiu que o corpus de áudio passa de
**instrumento** — servir ao Filtro 2, confirmando marcadores em fala espontânea —
a **entregável autônomo**, isto é, corpus de fala regional publicado por si.

A decisão muda a unidade da meta, e não apenas seu valor.

## Por que a meta antiga não serve mais

A meta de 8,3 h por estado saía do volume necessário para que a **ausência** de
uma variante rara — a negação pós-verbal — fosse informativa. Era a conta certa
para um instrumento de validação: o corpus precisava ser grande o bastante para
que "não ocorreu" significasse alguma coisa.

Um corpus publicado não se justifica assim. Ele é avaliado por **quem está
representado nele**, e a pergunta deixa de ser "quantas horas para detectar uma
variante" e passa a ser "quantos falantes para que o material caracterize uma
variedade, e não um punhado de pessoas".

## A derivação, e ela não é arbitrada

O projeto já fixou, em `docs/fontes_coleta.md` seção 2.4.5, o teto de que
**nenhum indivíduo responde por mais de 5% da fala de um estado**. O teto foi
estabelecido para impedir que um falante loquaz dominasse a amostra de uma
variedade.

Desse teto segue-se um piso aritmético, e não uma escolha: satisfazer 5% exige
**pelo menos 20 falantes distintos por estado**. É o mesmo movimento da meta
anterior — a regra já aceita pelo projeto produz o número, e não o contrário.

## Das pessoas para as horas

As horas passam a ser consequência, e não meta. Convertem-se pelos rendimentos
de falantes por arquivo **medidos** no piloto, e não supostos
(`experimentos/resultados/relatorios/piloto_medicoes.md`, seção 2).

Duas premissas de contagem, declaradas porque alteram o resultado:

1. **Um canal de vlog equivale a um falante**, por mais vídeos que forneça. É a
   premissa já adotada em `docs/fontes_coleta.md` seção 2.4, e é o que torna a
   camada espontânea cara em falantes por hora.
2. **Em podcast, o apresentador repete-se entre episódios.** O primeiro episódio
   de um programa rende os locutores medidos; os seguintes rendem um a menos.

Uso:
    python meta_corpus_autonomo.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

SAIDA = Path(__file__).resolve().parent / "resultados"
FONTES = Path(__file__).resolve().parent.parent / "pipeline_coleta_piloto" / "fontes.json"

TETO_POR_FALANTE = 0.05          # docs/fontes_coleta.md, 2.4.5

# Densidade de contextos de palatalização, MEDIDA sobre as 4,3 h de fala
# atribuída do piloto por `densidade_palatalizacao.py`. Não é suposição.
CONTEXTOS_POR_MINUTO = 13.6
OCORRENCIAS_PARA_TAXA = 10       # mesmo critério de `meta_volume_corpus.py`
ESTADOS = ("PB", "PE", "CE", "BA", "SP", "RJ")

# Locutores por arquivo, medidos no piloto de 27–28/08/2026 sobre 52 arquivos.
LOCUTORES_POR_ARQUIVO = {
    "entrevista_vox_pop": 4.2,
    "podcast_radio_tv_regional": 3.0,
    "vlog_amador": 2.2,
}

# Quantos desses locutores são falantes-alvo novos, a cada arquivo adicional do
# mesmo canal. As justificativas estão no cabeçalho.
FALANTES_NOVOS_POR_ARQUIVO = {
    # o repórter repete-se e não é falante-alvo; os entrevistados variam
    "entrevista_vox_pop": 4.2 - 1.0,
    # o apresentador repete-se entre episódios, mas é falante do estado
    "podcast_radio_tv_regional": 3.0 - 1.0,
    # um canal equivale a um falante, independentemente do número de vídeos
    "vlog_amador": 0.0,
}
FALANTES_PRIMEIRO_ARQUIVO = {
    "entrevista_vox_pop": 4.2,
    "podcast_radio_tv_regional": 3.0,
    "vlog_amador": 1.0,
}

# Duração média coletada por arquivo, apurada de metadados.json em 29/08/2026.
DURACAO_MEDIA_S = 382.0


def piso_de_falantes(teto: float) -> int:
    """Falantes mínimos para que nenhum ultrapasse `teto` da fala do estado."""
    return math.ceil(1 / teto)


def falantes_disponiveis(canais: list[dict]) -> dict:
    """Falantes que o conjunto de canais de um estado pode render, por camada."""
    por_camada: dict[str, int] = {}
    for camada in LOCUTORES_POR_ARQUIVO:
        n = sum(1 for c in canais if c["tipo_fonte"] == camada)
        por_camada[camada] = n
    return por_camada


def main() -> None:
    fontes = json.loads(FONTES.read_text(encoding="utf-8"))
    piso = piso_de_falantes(TETO_POR_FALANTE)

    L: list[str] = []
    add = L.append
    add("# Meta do corpus como entregável autônomo")
    add("")
    add("Gerado por `experimentos/meta_corpus_autonomo.py`. Substitui a meta de")
    add("`meta_volume.md`, derivada de uma função que o corpus deixou de ter.")
    add("")
    add("## O piso de falantes, derivado do teto já vigente")
    add("")
    add(f"O teto de {TETO_POR_FALANTE:.0%} por falante, fixado em `docs/fontes_coleta.md`")
    add(f"seção 2.4.5, exige por aritmética **{piso} falantes distintos por estado**.")
    add("Não é escolha: é o que satisfazer o teto significa.")
    add("")
    add("## Quantos arquivos por estado, e de que camada")
    add("")
    add("Cada canal de vlog rende um falante, quantos vídeos forneça. Vox-pop e")
    add("podcast rendem falantes novos a cada arquivo, descontado o locutor que se")
    add("repete — repórter ou apresentador.")
    add("")
    add("| UF | Canais vox-pop | Canais podcast | Canais vlog | Falantes só de vlog | Arquivos de vox-pop para completar 20 |")
    add("|---|---|---|---|---|---|")

    linhas_uf = []
    for uf in ESTADOS:
        canais = fontes[uf]
        disp = falantes_disponiveis(canais)
        de_vlog = disp["vlog_amador"]                      # 1 falante por canal
        # cada canal de podcast contribui ao menos o apresentador e convidados
        de_podcast = disp["podcast_radio_tv_regional"] * FALANTES_PRIMEIRO_ARQUIVO[
            "podcast_radio_tv_regional"]
        faltam = max(0.0, piso - de_vlog - de_podcast)
        arquivos_voxpop = math.ceil(
            faltam / FALANTES_NOVOS_POR_ARQUIVO["entrevista_vox_pop"]) if faltam else 0
        linhas_uf.append((uf, disp, de_vlog, de_podcast, faltam, arquivos_voxpop))
        add(f"| {uf} | {disp['entrevista_vox_pop']} | "
            f"{disp['podcast_radio_tv_regional']} | {disp['vlog_amador']} | "
            f"{de_vlog} | {arquivos_voxpop} |")
    add("")

    minutos_por_falante = OCORRENCIAS_PARA_TAXA / CONTEXTOS_POR_MINUTO
    add("## O segundo piso: quanta fala por falante")
    add("")
    add("O teto de 5% restringe **quantos** falantes, e nada diz sobre **quanta**")
    add("fala cada um precisa produzir. Sem esse segundo piso a conta permitiria um")
    add("corpus de vinte pessoas com quatro minutos cada, inútil para o marcador de")
    add("áudio do projeto.")
    add("")
    add(f"A densidade de contextos de palatalização foi medida em "
        f"**{CONTEXTOS_POR_MINUTO} por minuto** de fala (`densidade_palatalizacao.md`),")
    add(f"de modo que {OCORRENCIAS_PARA_TAXA} contextos exigem apenas ")
    add(f"**{minutos_por_falante:.1f} minuto de fala por falante** — e trinta contextos,")
    add(f"{30/CONTEXTOS_POR_MINUTO:.1f} minutos.")
    add("")
    add("**O piso de fala por falante é, portanto, folgado, e não é o gargalo.**")
    add("Dos 211 rótulos de locutor do corpus atual, 90 já superam dez contextos.")
    add("")
    add("## Horas implicadas, que agora são consequência e não meta")
    add("")
    add(f"Com duração média de {DURACAO_MEDIA_S/60:.1f} min por arquivo coletado:")
    add("")
    add("| UF | Arquivos estimados | Horas brutas |")
    add("|---|---|---|")
    total_h = 0.0
    for uf, disp, de_vlog, de_podcast, faltam, arq_vox in linhas_uf:
        # um arquivo por canal de vlog, um por canal de podcast, mais os de vox-pop
        arquivos = disp["vlog_amador"] + disp["podcast_radio_tv_regional"] + arq_vox
        horas = arquivos * DURACAO_MEDIA_S / 3600
        total_h += horas
        add(f"| {uf} | {arquivos} | {horas:.1f} h |")
    add(f"| **Total** | — | **{total_h:.1f} h** |")
    add("")
    add("Compare-se com as 50 h da meta anterior e com as 38 h de seu recálculo.")
    add("A diferença não é de precisão, e sim de critério: aquelas mediam volume de")
    add("fala para detectar uma variante; esta mede cobertura de falantes.")
    add("")
    add("## Ressalvas")
    add("")
    add("**Os rendimentos de locutor por arquivo são medianas de 52 arquivos**, e a")
    add("variação entre arquivos é grande — um debate rendeu oito locutores.")
    add("")
    add("**A contagem de falantes distintos não está implementada.** Nada garante,")
    add("hoje, que dois arquivos não contenham a mesma pessoa; a verificação exigiria")
    add("comparação de vozes na diarização (`docs/pendencias.md`, seção 6.4). Até que")
    add("exista, os números abaixo são estimativa e não medição.")
    add("")
    add("**O piso de 20 é mínimo, não alvo.** Satisfazê-lo por pouco deixa o corpus")
    add("no limite exato do teto, sem margem para exclusão de trecho por qualidade.")
    add("")
    add("## O gargalo mudou de lugar, e é este o achado do recálculo")
    add("")
    add("Sob o critério antigo, o que faltava eram **horas**: 5,52 h de 50 h, 11%.")
    add("Sob o critério de entregável autônomo, as horas deixam de ser escassas — a")
    add("densidade medida mostra que um minuto de fala por pessoa basta para o")
    add("marcador, e o corpus atual já tem 90 locutores acima do piso.")
    add("")
    add("**O que falta passa a ser a verificação de que os falantes são pessoas")
    add("distintas.** A diarização rotula locutores dentro de cada arquivo; nada")
    add("garante que o rótulo `SPEAKER_00` de dois arquivos do mesmo canal não seja")
    add("a mesma pessoa — e no caso do repórter ou do apresentador, quase certamente")
    add("é. Os 211 rótulos são, portanto, **limite superior** do número de pessoas,")
    add("e possivelmente muito acima dele.")
    add("")
    add("Segue-se que a pendência 6.4 de `docs/pendencias.md` — comparação de vozes")
    add("entre arquivos, hoje não implementada — deixa de ser melhoria desejável e")
    add("passa a ser **condição para declarar o corpus completo**. Sem ela não é")
    add("possível afirmar que o teto de 5% é respeitado, e o teto é a única regra")
    add("de que a meta inteira deriva.")

    texto = "\n".join(L)
    (SAIDA / "tabelas" / "meta_corpus_autonomo.md").write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
