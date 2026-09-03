"""
verificar_reincidencia.py

Responde às pendências D-6.4 e #5 do registro de `docs/dataset-spec.md`: nada
hoje impede que a mesma pessoa apareça em mais de um arquivo do corpus,
violando silenciosamente o teto de 5% por falante fixado em
`docs/fontes_coleta.md`, seção 2.4.5. A diarização rotula locutores **dentro**
de cada arquivo (`SPEAKER_00`, `SPEAKER_01`...); esses rótulos não têm relação
entre arquivos distintos, e o repórter de um canal de vox-pop reaparece em
todo episódio novo sob um rótulo diferente a cada vez.

Este script é a ferramenta da etapa 1 de `docs/plano_corpus/`.

## O método

Comparação de vozes por **embedding de locutor** — um vetor de dimensão fixa
que resume as características da voz de uma pessoa, de tal forma que vozes
parecidas produzem vetores próximos. `pyannote.audio`, já dependência do
projeto para diarização, expõe um modelo de *embedding* pronto
(`pyannote/embedding`), o que evita introduzir uma ferramenta nova.

Passo a passo, por estado:

1. Para cada arquivo já diarizado, extrai-se um *embedding* de cada rótulo de
   locutor, sobre os turnos mais longos daquele rótulo até somar ao menos
   `DURACAO_MINIMA_S` de fala — voz curta demais produz *embedding* pouco
   confiável.
2. Comparam-se todos os pares de *embeddings* do estado por similaridade de
   cosseno.
3. Pares acima do limiar são **candidatos** a mesma pessoa, não conclusão. A
   saída é uma lista para revisão humana, no mesmo espírito da triagem
   automática de canais em `verificar_fontes.py`: reduz esforço, não decide
   sozinha.

## Por que não decidir automaticamente

Embedding de locutor tem falsos positivos — vozes fisiologicamente parecidas
podem ser confundidas — e falsos negativos, sobretudo com pouca fala ou áudio
ruidoso. Fundir dois rótulos por engano apagaria uma pessoa real do corpus;
não fundir dois rótulos da mesma pessoa violaria o teto sem que ninguém
percebesse. Nenhum dos dois erros deve ocorrer silenciosamente.

## O que a saída carrega, e por quê

- **Todos os pares acima de `--limiar-registro`**, e não apenas os acima do
  limiar de decisão, cada um marcado com `acima_do_limiar`. O limiar de 0,75 é
  ponto de partida não validado, e a etapa 1 prevê calibrá-lo descendo a lista
  até que os pares deixem de ser plausíveis. Registrar apenas o que já passou
  no limiar tornaria essa calibração impossível sem nova passagem de GPU.
- **Os segmentos de áudio usados**, em segundos, dos dois lados de cada par. A
  conferência humana consiste em ouvir os dois trechos; sem os tempos, o
  revisor não teria como localizá-los.
- **O canal de cada lado**, com o sinalizador `mesmo_canal`. O padrão esperado
  de reincidência é o apresentador ou repórter do próprio canal.
- **Os rótulos sem embedding**, isto é, com menos de `DURACAO_MINIMA_S` de
  fala. Eles não são falantes verificados nem descartados: são desconhecidos,
  e o seu número limita o que se pode afirmar sobre a contagem final.

## Onde isto roda

Requer `pyannote.audio` e o áudio bruto de cada arquivo, que hoje só coexistem
no ambiente de processamento (Colab), não na máquina local — mesma divisão de
esteira já documentada em `notebooks/README.md`.

Uso, no ambiente de processamento:
    python verificar_reincidencia.py --estado todos --registros dataset_raw/registros_anonimizados
"""

from __future__ import annotations

import argparse
import datetime as _dt
import itertools
import json
import logging
from pathlib import Path

import torch

from config import AUDIO_DIR, DIARIZATION_DIR, ESTADOS_VALIDOS, FINAL_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Limiar de similaridade de cosseno acima do qual dois rótulos são candidatos a
# mesma pessoa. 0,75 é ponto de partida conservador para o modelo de
# `pyannote/embedding` — mais alto reduz falsos positivos e exige mais revisão
# manual; deve ser calibrado com uma amostra conferida à mão antes de confiar
# na lista automaticamente.
LIMIAR_SIMILARIDADE = 0.75

# Piso de registro na saída. Pares entre este valor e o limiar de decisão são
# gravados, marcados como abaixo do limiar, para que a calibração descrita na
# etapa 1 do plano do corpus possa ser feita sobre a mesma execução.
LIMIAR_REGISTRO = 0.50

# Segundos mínimos de fala de um locutor para que seu embedding seja calculado.
# Abaixo disso a voz não fornece sinal suficiente, e comparar seria ruído.
DURACAO_MINIMA_S = 8.0

# Segundos de fala que se procura reunir por locutor quando há material para
# isso. O mínimo acima é critério de admissão, não de qualidade: um locutor com
# cem segundos de fala não tem por que ser resumido em oito. Mais áudio produz
# embedding mais estável, e o custo adicional é desprezível diante do da GPU.
DURACAO_ALVO_S = 30.0


def _get_modelo_embedding():
    """Carrega o modelo de embedding de locutor do pyannote, uma única vez."""
    import os

    from pyannote.audio import Inference, Model

    token = os.environ.get("HF_TOKEN")
    modelo = Model.from_pretrained("pyannote/embedding", use_auth_token=token)
    inferencia = Inference(modelo, window="whole")
    if torch.cuda.is_available():
        inferencia.to(torch.device("cuda"))
    return inferencia


def _segmentos_por_locutor(diarizacao: list[dict]) -> dict[str, list[tuple[float, float]]]:
    """Agrupa os turnos de diarização por rótulo de locutor."""
    por_locutor: dict[str, list[tuple[float, float]]] = {}
    for turno in diarizacao:
        por_locutor.setdefault(turno["speaker"], []).append((turno["start"], turno["end"]))
    return por_locutor


def _selecionar_turnos(turnos: list[tuple[float, float]], minimo: float,
                       alvo: float) -> tuple[list[tuple[float, float]], float]:
    """
    Escolhe os turnos mais longos de um locutor até reunir `alvo` segundos de
    fala, ou até esgotá-los. Devolve os turnos escolhidos, em ordem
    cronológica, e o total obtido. Se toda a fala do locutor não alcançar
    `minimo`, devolve lista vazia — e o locutor fica fora da comparação.
    """
    acumulado, escolhidos = 0.0, []
    for inicio, fim in sorted(turnos, key=lambda t: t[1] - t[0], reverse=True):
        escolhidos.append((inicio, fim))
        acumulado += fim - inicio
        if acumulado >= alvo:
            break
    if acumulado < minimo:
        return [], acumulado
    return sorted(escolhidos), acumulado


def _forma_de_onda(caminho_audio: Path, trechos: list[tuple[float, float]]):
    """
    Concatena os trechos indicados do arquivo numa única forma de onda mono.

    A concatenação é o ponto em que esta versão diverge da anterior, que
    calculava o embedding sobre um único turno — o mais longo. Dos 154 rótulos
    do corpus que alcançam 8 s de fala, 16 só os alcançam somando turnos, e
    nesses o turno isolado mais longo é menor que o mínimo declarado. O
    embedding sairia, nesses casos, de menos áudio do que o próprio critério
    exige, sem que nada no relatório o indicasse.
    """
    import torchaudio

    taxa = torchaudio.info(str(caminho_audio)).sample_rate
    pedacos = []
    for inicio, fim in trechos:
        deslocamento = int(inicio * taxa)
        quadros = int((fim - inicio) * taxa)
        if quadros <= 0:
            continue
        onda, _ = torchaudio.load(str(caminho_audio), frame_offset=deslocamento, num_frames=quadros)
        pedacos.append(onda)
    if not pedacos:
        return None, taxa
    onda = torch.cat(pedacos, dim=1)
    if onda.shape[0] > 1:                     # o pipeline grava mono, mas não custa garantir
        onda = onda.mean(dim=0, keepdim=True)
    return onda, taxa


def embeddings_do_arquivo(caminho_audio: Path, diarizacao: list[dict], inferencia,
                          duracao_minima: float, duracao_alvo: float) -> tuple[dict, list[dict]]:
    """
    Um embedding por locutor do arquivo. Devolve dois resultados: os rótulos
    com embedding e os rótulos descartados por falta de fala — que precisam ser
    contados, e não silenciosamente omitidos.
    """
    com_embedding, sem_embedding = {}, []
    for locutor, turnos in _segmentos_por_locutor(diarizacao).items():
        escolhidos, total = _selecionar_turnos(turnos, duracao_minima, max(duracao_alvo, duracao_minima))
        if not escolhidos:
            sem_embedding.append({
                "locutor": locutor,
                "fala_total_s": round(total, 2),
                "turnos": len(turnos),
            })
            continue
        onda, taxa = _forma_de_onda(caminho_audio, escolhidos)
        if onda is None:
            sem_embedding.append({"locutor": locutor, "fala_total_s": 0.0, "turnos": len(turnos)})
            continue
        vetor = inferencia({"waveform": onda, "sample_rate": taxa})
        com_embedding[locutor] = {
            "vetor": torch.as_tensor(vetor).flatten().float(),
            "segundos_usados": round(sum(f - i for i, f in escolhidos), 2),
            "segmentos_usados": [[round(i, 2), round(f, 2)] for i, f in escolhidos],
            "fala_total_s": round(sum(f - i for i, f in turnos), 2),
        }
    return com_embedding, sem_embedding


def _carregar_registros(registros_dir: Path, estado_alvo: str) -> list[dict]:
    """Registros diarizados de um estado, lidos da pasta indicada."""
    registros = []
    for caminho in sorted(registros_dir.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("estado_alvo") == estado_alvo:
            registros.append(reg)
    return registros


def comparar_estado(estado_alvo: str, audio_dir: Path, registros_dir: Path, inferencia,
                    limiar: float, limiar_registro: float, duracao_minima: float,
                    duracao_alvo: float = DURACAO_ALVO_S) -> dict:
    """
    Compara todos os pares de locutores de um estado. Devolve o relatório
    completo: resumo, rótulos com e sem embedding, e os pares ordenados por
    similaridade decrescente.
    """
    registros = _carregar_registros(registros_dir, estado_alvo)
    if not registros:
        logger.warning("Nenhum registro com estado_alvo=%s em %s.", estado_alvo, registros_dir)

    rotulos: dict[tuple[str, str], dict] = {}
    sem_embedding: list[dict] = []
    arquivos_lidos = 0

    for reg in registros:
        caminho_audio = audio_dir / reg["arquivo"]
        if not caminho_audio.exists():
            logger.warning("Áudio ausente para %s: o arquivo inteiro fica fora da comparação.", reg["id"])
            continue
        arquivos_lidos += 1
        com, sem = embeddings_do_arquivo(caminho_audio, reg["diarizacao"], inferencia,
                                         duracao_minima, duracao_alvo)
        for locutor, dados in com.items():
            rotulos[(reg["id"], locutor)] = {**dados, "canal": reg.get("canal", "")}
        for item in sem:
            sem_embedding.append({"arquivo": reg["id"], "canal": reg.get("canal", ""), **item})
        logger.info("%s | %s: %d rótulo(s) com embedding, %d sem.",
                    estado_alvo, reg["id"], len(com), len(sem))

    pares = []
    for chave_a, chave_b in itertools.combinations(rotulos, 2):
        if chave_a[0] == chave_b[0]:
            continue  # a própria diarização já os separou dentro do arquivo
        similaridade = torch.nn.functional.cosine_similarity(
            rotulos[chave_a]["vetor"].unsqueeze(0),
            rotulos[chave_b]["vetor"].unsqueeze(0)).item()
        if similaridade < limiar_registro:
            continue
        a, b = rotulos[chave_a], rotulos[chave_b]
        pares.append({
            "similaridade": round(similaridade, 4),
            "acima_do_limiar": similaridade >= limiar,
            "mesmo_canal": a["canal"] == b["canal"],
            "arquivo_a": chave_a[0], "locutor_a": chave_a[1],
            "canal_a": a["canal"], "segmentos_a": a["segmentos_usados"],
            "arquivo_b": chave_b[0], "locutor_b": chave_b[1],
            "canal_b": b["canal"], "segmentos_b": b["segmentos_usados"],
            # Preenchido na conferência humana: "mesma_pessoa" ou "pessoas_distintas".
            "veredito_humano": None,
        })
    pares.sort(key=lambda p: -p["similaridade"])

    return {
        "estado": estado_alvo,
        "gerado_em": _dt.datetime.now().isoformat(timespec="seconds"),
        "parametros": {
            "limiar_similaridade": limiar,
            "limiar_registro": limiar_registro,
            "duracao_minima_s": duracao_minima,
            "duracao_alvo_s": duracao_alvo,
            "registros_dir": str(registros_dir),
        },
        "resumo": {
            "arquivos": arquivos_lidos,
            "rotulos_com_embedding": len(rotulos),
            "rotulos_sem_embedding": len(sem_embedding),
            "pares_acima_do_limiar": sum(1 for p in pares if p["acima_do_limiar"]),
            "pares_registrados": len(pares),
            # Teto, e não resultado: a conferência humana só pode reduzi-lo.
            "teto_de_falantes": len(rotulos),
        },
        "rotulos": [
            {"arquivo": arquivo, "locutor": locutor, "canal": dados["canal"],
             "fala_total_s": dados["fala_total_s"], "segundos_usados": dados["segundos_usados"],
             "segmentos_usados": dados["segmentos_usados"]}
            for (arquivo, locutor), dados in sorted(rotulos.items())
        ],
        "rotulos_sem_embedding": sem_embedding,
        "pares": pares,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Verificação de reincidência de falantes entre arquivos.")
    ap.add_argument("--estado", required=True,
                    help="Estado-alvo (PB, PE, CE, BA, SP, RJ) ou 'todos'")
    ap.add_argument("--registros", default=None,
                    help="Pasta com os registros diarizados (padrão: FINAL_DIR de config.py). "
                         "No corpus atual, use dataset_raw/registros_anonimizados.")
    ap.add_argument("--audio-dir", default=None,
                    help="Pasta com os .wav (padrão: AUDIO_DIR de config.py)")
    ap.add_argument("--saida-dir", default=None,
                    help="Pasta de saída (padrão: DIARIZATION_DIR de config.py)")
    ap.add_argument("--limiar", type=float, default=LIMIAR_SIMILARIDADE,
                    help=f"Limiar de decisão (padrão: {LIMIAR_SIMILARIDADE})")
    ap.add_argument("--limiar-registro", type=float, default=LIMIAR_REGISTRO,
                    help=f"Piso de registro dos pares na saída (padrão: {LIMIAR_REGISTRO})")
    ap.add_argument("--duracao-minima", type=float, default=DURACAO_MINIMA_S,
                    help=f"Segundos mínimos de fala por rótulo (padrão: {DURACAO_MINIMA_S})")
    ap.add_argument("--duracao-alvo", type=float, default=DURACAO_ALVO_S,
                    help=f"Segundos de fala a reunir por rótulo, quando houver (padrão: {DURACAO_ALVO_S})")
    args = ap.parse_args()

    audio_dir = Path(args.audio_dir) if args.audio_dir else AUDIO_DIR
    registros_dir = Path(args.registros) if args.registros else FINAL_DIR
    saida_dir = Path(args.saida_dir) if args.saida_dir else DIARIZATION_DIR
    saida_dir.mkdir(parents=True, exist_ok=True)

    if not registros_dir.is_dir() or not any(registros_dir.glob("*.json")):
        raise SystemExit(
            f"Nenhum registro JSON em {registros_dir}. "
            "A pasta padrão `registros_finais/` está vazia neste corpus: passe "
            "--registros dataset_raw/registros_anonimizados."
        )

    estados = ESTADOS_VALIDOS if args.estado.lower() in ("todos", "all") else [args.estado.upper()]
    inferencia = _get_modelo_embedding()

    resumo_geral = {}
    for estado in estados:
        relatorio = comparar_estado(estado, audio_dir, registros_dir, inferencia,
                                    args.limiar, args.limiar_registro, args.duracao_minima,
                                    args.duracao_alvo)
        saida = saida_dir / f"reincidencia_{estado}.json"
        saida.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
        resumo_geral[estado] = relatorio["resumo"]
        print(f"{estado}: {relatorio['resumo']['pares_acima_do_limiar']} par(es) acima do limiar "
              f"{args.limiar}, {relatorio['resumo']['pares_registrados']} registrado(s), "
              f"teto de {relatorio['resumo']['teto_de_falantes']} falante(s). -> {saida}")

    (saida_dir / "reincidencia_resumo.json").write_text(
        json.dumps(resumo_geral, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nRevisão humana obrigatória antes de fundir qualquer par de rótulos.")
    print("O teto acima não desconta fusões: só a conferência humana produz a contagem final.")


if __name__ == "__main__":
    main()
