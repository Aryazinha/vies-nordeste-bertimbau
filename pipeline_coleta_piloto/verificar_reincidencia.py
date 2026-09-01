"""
verificar_reincidencia.py

Responde às pendências D-6.4 e #5 do registro de `docs/dataset-spec.md`: nada
hoje impede que a mesma pessoa apareça em mais de um arquivo do corpus,
violando silenciosamente o teto de 5% por falante fixado em
`docs/fontes_coleta.md`, seção 2.4.5. A diarização rotula locutores **dentro**
de cada arquivo (`SPEAKER_00`, `SPEAKER_01`...); esses rótulos não têm relação
entre arquivos distintos, e o repórter de um canal de vox-pop reaparece em
todo episódio novo sob um rótulo diferente a cada vez.

## O método

Comparação de vozes por **embedding de locutor** — um vetor de dimensão fixa
que resume as características da voz de uma pessoa, de tal forma que vozes
parecidas produzem vetores próximos. `pyannote.audio`, já dependência do
projeto para diarização, expõe um modelo de *embedding* pronto
(`pyannote/embedding`), o que evita introduzir uma ferramenta nova.

Passo a passo, por estado:

1. Para cada arquivo já diarizado, extrai-se um *embedding* de cada rótulo de
   locutor, a partir dos segmentos de fala mais longos atribuídos a ele — voz
   curta demais produz *embedding* pouco confiável.
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

## Onde isto roda

Requer `pyannote.audio` e o áudio bruto de cada arquivo, que hoje só coexistem
no ambiente de processamento (Colab), não nesta máquina — mesma divisão de
esteira já documentada em `notebooks/README.md`. Este script é o companheiro de
`diarize.py` e pressupõe os mesmos registros finais (transcrição + diarização)
já produzidos.

Uso, no ambiente de processamento:
    python verificar_reincidencia.py --estado PE
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging
from pathlib import Path

import torch

from config import DIARIZATION_DIR, FINAL_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Limiar de similaridade de cosseno acima do qual dois rótulos são candidatos a
# mesma pessoa. 0,75 é ponto de partida conservador para o modelo de
# `pyannote/embedding` — mais alto reduz falsos positivos e exige mais revisão
# manual; deve ser calibrado com uma amostra conferida à mão antes de confiar
# na lista automaticamente.
LIMIAR_SIMILARIDADE = 0.75

# Segundos mínimos de fala de um locutor para que seu embedding seja calculado.
# Abaixo disso a voz não fornece sinal suficiente, e comparar seria ruído.
DURACAO_MINIMA_S = 8.0


def _get_modelo_embedding():
    """Carrega o modelo de embedding de locutor do pyannote, uma única vez."""
    from pyannote.audio import Model, Inference
    import os
    token = os.environ.get("HF_TOKEN")
    modelo = Model.from_pretrained("pyannote/embedding", use_auth_token=token)
    return Inference(modelo, window="whole")


def _segmentos_por_locutor(diarizacao: list[dict]) -> dict[str, list[tuple[float, float]]]:
    """Agrupa os turnos de diarização por rótulo de locutor."""
    por_locutor: dict[str, list[tuple[float, float]]] = {}
    for turno in diarizacao:
        por_locutor.setdefault(turno["speaker"], []).append(
            (turno["start"], turno["end"]))
    return por_locutor


def embeddings_do_arquivo(caminho_audio: Path, diarizacao: list[dict], inferencia) -> dict[str, torch.Tensor]:
    """
    Um embedding por locutor do arquivo, sobre o(s) segmento(s) mais longo(s)
    até somar ao menos `DURACAO_MINIMA_S`. Locutores sem fala suficiente são
    omitidos, e não entram na comparação — apareceriam como "sem embedding"
    no relatório, não como "diferente de todos".
    """
    from pyannote.core import Segment
    por_locutor = _segmentos_por_locutor(diarizacao)
    saida = {}
    for locutor, turnos in por_locutor.items():
        turnos_ordenados = sorted(turnos, key=lambda t: t[1] - t[0], reverse=True)
        acumulado, escolhidos = 0.0, []
        for inicio, fim in turnos_ordenados:
            escolhidos.append((inicio, fim))
            acumulado += fim - inicio
            if acumulado >= DURACAO_MINIMA_S:
                break
        if acumulado < DURACAO_MINIMA_S:
            continue
        inicio, fim = escolhidos[0]
        saida[locutor] = inferencia.crop(str(caminho_audio), Segment(inicio, fim))
    return saida


def comparar_estado(estado_alvo: str, audio_dir: Path) -> list[dict]:
    """
    Compara todos os pares de locutores de um estado. Devolve os pares cuja
    similaridade excede `LIMIAR_SIMILARIDADE`, para revisão humana.
    """
    inferencia = _get_modelo_embedding()

    registros = []
    for caminho in sorted(FINAL_DIR.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        if reg.get("estado_alvo") == estado_alvo:
            registros.append(reg)

    todos_embeddings: dict[tuple[str, str], torch.Tensor] = {}
    for reg in registros:
        caminho_audio = audio_dir / reg["arquivo"]
        if not caminho_audio.exists():
            logger.warning("Áudio ausente para %s, pulando.", reg["id"])
            continue
        embs = embeddings_do_arquivo(caminho_audio, reg["diarizacao"], inferencia)
        for locutor, emb in embs.items():
            todos_embeddings[(reg["id"], locutor)] = torch.tensor(emb)

    candidatos = []
    for (a_id, a_loc), (b_id, b_loc) in itertools.combinations(todos_embeddings, 2):
        if a_id == b_id:
            continue  # mesma diarização já garante que são pessoas distintas
        sim = torch.nn.functional.cosine_similarity(
            todos_embeddings[(a_id, a_loc)].unsqueeze(0),
            todos_embeddings[(b_id, b_loc)].unsqueeze(0)).item()
        if sim >= LIMIAR_SIMILARIDADE:
            candidatos.append({
                "estado": estado_alvo, "similaridade": round(sim, 3),
                "arquivo_a": a_id, "locutor_a": a_loc,
                "arquivo_b": b_id, "locutor_b": b_loc,
            })
    candidatos.sort(key=lambda c: -c["similaridade"])
    return candidatos


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--estado", required=True, help="Estado-alvo (PB, PE, CE, BA, SP, RJ)")
    ap.add_argument("--audio-dir", default=None, help="Pasta com os .wav (padrão: AUDIO_DIR de config.py)")
    args = ap.parse_args()

    from config import AUDIO_DIR
    audio_dir = Path(args.audio_dir) if args.audio_dir else AUDIO_DIR

    candidatos = comparar_estado(args.estado, audio_dir)
    saida = DIARIZATION_DIR / f"reincidencia_{args.estado}.json"
    saida.write_text(json.dumps(candidatos, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(candidatos)} par(es) candidato(s) a mesma pessoa em {args.estado}, "
          f"limiar {LIMIAR_SIMILARIDADE}. Gravado em {saida}.")
    print("Revisão humana obrigatória antes de fundir qualquer par de rótulos.")


if __name__ == "__main__":
    main()
