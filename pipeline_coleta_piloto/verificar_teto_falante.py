"""
verificar_teto_falante.py

Verifica o teto de 5% por falante — "nenhum indivíduo responde por mais de 5%
da fala de um estado" (`docs/dataset-spec.md` §1.4.5) — sobre o corpus
diarizado, depois das fusões confirmadas na conferência humana de
`verificar_reincidencia.py`.

## Por que o piso de 20 falantes não basta

O piso de 20 falantes distintos por estado deriva do teto por aritmética: com
menos de 20 pessoas, alguma responde necessariamente por mais de 5% da fala. A
recíproca não vale. Vinte pessoas satisfazem o teto apenas se a fala se
distribuir entre elas de modo suficientemente uniforme — e em telejornal e
podcast ela não se distribui, porque apresentador e repórter falam muito mais
que o entrevistado. A etapa 1 de `docs/plano_corpus/` verificava apenas o piso;
este script verifica a regra de que o piso deriva.

## O que mede, por estado

1. A participação de cada pessoa na fala do estado, e quantas excedem o teto.
2. O volume máximo que o estado conserva quando o teto é aplicado **por
   recorte**: o maior total T tal que, limitada cada pessoa a 5% de T, a soma
   das contribuições ainda alcance T. Com menos de 20 pessoas, T é zero — o
   teto é insatisfazível, qualquer que seja o recorte.
3. A fatia máxima por pessoa nesse corpus recortado, comparada ao segundo piso
   de `experimentos/resultados/tabelas/meta_corpus_autonomo.md` — 0,7 minuto de
   fala por falante, o necessário para dez contextos de palatalização.
4. Quantas pessoas conservam ao menos esse segundo piso depois do recorte. É
   este, e não a contagem bruta de pessoas, o número que precisa alcançar 20 —
   critério de conclusão adotado em 10/09/2026
   (`docs/plano_corpus/01-verificar-falantes.md`, seção 7.1).
5. Quantas pessoas **novas** faltam para que o item 4 alcance 20, supondo que
   cada uma traga `--fala-pessoa-nova` minutos de fala. É o déficit que orienta
   a etapa 2 de `docs/plano_corpus/`.

O recorte é **uma** interpretação operacional do teto, e não a única: a regra
fixa o limite, mas não diz se ele se cumpre descartando fala excedente ou
coletando mais falantes. É, contudo, a interpretação que mede o corpus tal como
está, sem supor coleta adicional.

## Por que o déficit se mede em pessoas, e não em horas

Acrescentar fala a quem já excede o teto não acrescenta nada, porque o
excedente é recortado. Acrescentar uma pessoa, ao contrário, eleva o volume
admissível e, com ele, a fatia de todas as outras — de modo que pessoas já
presentes, antes abaixo do segundo piso, passam a alcançá-lo. Por isso um
estado com zero pessoas úteis pode precisar de bem menos que vinte pessoas
novas, e por isso o resultado quase não depende da fala suposta para cada
pessoa nova, desde que ela exceda a fatia: o excesso é recortado.

## A pessoa, e não o rótulo

Sem `--vereditos`, cada rótulo de diarização conta como uma pessoa, e o
resultado é **limite inferior** da violação: fundir rótulos da mesma pessoa só
aumenta a participação dela. Com `--vereditos`, os pares confirmados como
mesma pessoa são fundidos por componentes conexos, como na apuração do
notebook `notebooks/verificar_falantes_colab.ipynb`, e pelo mesmo motivo: três
pares confirmados sobre a mesma voz descrevem uma pessoa, não três fusões.

Entram todos os rótulos, inclusive os de menos de 8 s de fala que a comparação
de vozes deixa de fora. Eles contam como pessoas distintas, o que é a hipótese
favorável ao teto — e o efeito é desprezível, porque cada um contribui com no
máximo a própria fala.

Uso:
    python verificar_teto_falante.py --registros dataset_raw/registros_anonimizados
    python verificar_teto_falante.py --registros dataset_raw/registros_anonimizados --vereditos dataset_raw/diarizacao/vereditos_reincidencia.json
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from config import ESTADOS_VALIDOS, FINAL_DIR

# "Nenhum indivíduo responde por mais de 5% da fala de um estado"
# (docs/dataset-spec.md §1.4.5). O valor não tem fundamento documentado no
# projeto: está registrado como pendência em docs/pendencias.md, D-6.4.
TETO = 0.05

# Segundo piso de meta_corpus_autonomo.md: dez contextos de palatalização, à
# densidade medida de 13,6 por minuto de fala.
MINUTOS_POR_FALANTE = 0.7

# Fala suposta para cada pessoa nova na simulação do déficit. Um minuto fica
# abaixo da mediana observada entre os falantes que não excedem o teto
# (1,25 min, em 10/09/2026), e a simulação dá o mesmo resultado de 1 a 3 min.
FALA_PESSOA_NOVA_MIN = 1.0


def fala_por_rotulo(registros_dir: Path) -> dict[str, dict[tuple[str, str], float]]:
    """Segundos de fala de cada rótulo `(arquivo, locutor)`, agrupados por estado."""
    fala: dict[str, dict[tuple[str, str], float]] = defaultdict(lambda: defaultdict(float))
    for caminho in sorted(registros_dir.glob("*.json")):
        reg = json.loads(caminho.read_text(encoding="utf-8"))
        for turno in reg.get("diarizacao") or []:
            fala[reg["estado_alvo"]][(reg["id"], turno["speaker"])] += turno["end"] - turno["start"]
    return fala


def carregar_vereditos(caminho: Path | None) -> list[dict]:
    """Vereditos da conferência humana; o notebook os grava como dicionário por par."""
    if caminho is None:
        return []
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    return list(dados.values()) if isinstance(dados, dict) else list(dados)


def fala_por_pessoa(fala_estado: dict[tuple[str, str], float], vereditos: list[dict],
                    estado: str) -> tuple[list[float], int, int]:
    """
    Funde os rótulos confirmados como mesma pessoa e devolve a fala de cada
    pessoa, o número de fusões efetivas e o de vereditos sem rótulo
    correspondente — que não podem ser descartados em silêncio.
    """
    pai = {rotulo: rotulo for rotulo in fala_estado}

    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]
            x = pai[x]
        return x

    fusoes, orfaos = 0, 0
    for v in vereditos:
        if v.get("estado") != estado or v.get("veredito") != "mesma_pessoa":
            continue
        a, b = tuple(v["rotulo_a"]), tuple(v["rotulo_b"])
        if a not in pai or b not in pai:
            orfaos += 1
            continue
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            pai[ra] = rb
            fusoes += 1

    por_pessoa: dict[tuple[str, str], float] = defaultdict(float)
    for rotulo, segundos in fala_estado.items():
        por_pessoa[raiz(rotulo)] += segundos
    return list(por_pessoa.values()), fusoes, orfaos


def volume_sob_teto(falas: list[float], teto: float) -> float:
    """
    Maior total T tal que `sum(min(s, teto * T)) >= T`.

    A função g(T) = sum(min(s, teto*T)) - T é côncava e nula em T = 0, de modo
    que o conjunto em que é não negativa é um intervalo [0, T*], e a bisseção
    sobre o predicado encontra o extremo. Com menos de 1/teto pessoas, a
    inclinação em zero não é positiva e T* = 0: o teto não pode ser satisfeito.
    """
    baixo, alto = 0.0, sum(falas)
    for _ in range(200):
        meio = (baixo + alto) / 2
        if sum(min(s, teto * meio) for s in falas) >= meio:
            baixo = meio
        else:
            alto = meio
    return baixo


def pessoas_uteis(falas: list[float], teto: float, minutos_por_falante: float) -> int:
    """Pessoas que conservam ao menos o segundo piso depois do recorte pelo teto."""
    fatia = teto * volume_sob_teto(falas, teto)
    piso_s = minutos_por_falante * 60
    return sum(1 for s in falas if min(s, fatia) >= piso_s)


def pessoas_novas_necessarias(falas: list[float], teto: float, minutos_por_falante: float,
                              minutos_pessoa_nova: float, alvo: int,
                              limite: int = 500) -> int | None:
    """
    Menor número de pessoas novas, cada uma com `minutos_pessoa_nova` de fala,
    que eleva a `alvo` as pessoas úteis. Devolve None se nem `limite` pessoas
    bastarem — o que ocorre quando a fala suposta para a pessoa nova fica abaixo
    do próprio segundo piso, e ela nunca poderia ser útil.
    """
    nova = minutos_pessoa_nova * 60
    for n in range(limite + 1):
        if pessoas_uteis(falas + [nova] * n, teto, minutos_por_falante) >= alvo:
            return n
    return None


def analisar_estado(falas: list[float], teto: float, minutos_por_falante: float) -> dict:
    total = sum(falas)
    participacoes = sorted((s / total for s in falas), reverse=True) if total else []
    acima = [p for p in participacoes if p > teto]
    volume = volume_sob_teto(falas, teto)
    return {
        "pessoas": len(falas),
        "fala_total_min": round(total / 60, 1),
        "pessoas_acima_do_teto": len(acima),
        "maior_participacao_pct": round(participacoes[0] * 100, 1) if participacoes else 0.0,
        "fala_concentrada_acima_do_teto_pct": round(sum(acima) * 100, 1),
        "volume_sob_teto_min": round(volume / 60, 1),
        "volume_conservado_pct": round(volume / total * 100, 1) if total else 0.0,
        "fatia_maxima_por_pessoa_min": round(teto * volume / 60, 2),
        "pessoas_com_segundo_piso_apos_recorte": pessoas_uteis(falas, teto, minutos_por_falante),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Verificação do teto de 5% por falante.")
    ap.add_argument("--registros", default=None,
                    help="Pasta com os registros diarizados (padrão: FINAL_DIR de config.py). "
                         "No corpus atual, use dataset_raw/registros_anonimizados.")
    ap.add_argument("--vereditos", default=None,
                    help="vereditos_reincidencia.json da conferência humana. Sem ele, cada "
                         "rótulo conta como uma pessoa, e o resultado é limite inferior da violação.")
    ap.add_argument("--teto", type=float, default=TETO, help=f"Teto por pessoa (padrão: {TETO})")
    ap.add_argument("--minutos-por-falante", type=float, default=MINUTOS_POR_FALANTE,
                    help=f"Segundo piso, em minutos de fala (padrão: {MINUTOS_POR_FALANTE})")
    ap.add_argument("--fala-pessoa-nova", type=float, default=FALA_PESSOA_NOVA_MIN,
                    help=f"Minutos de fala supostos por pessoa nova no cálculo do déficit "
                         f"(padrão: {FALA_PESSOA_NOVA_MIN})")
    ap.add_argument("--saida", default=None, help="Grava o resultado em JSON neste caminho.")
    args = ap.parse_args()

    registros_dir = Path(args.registros) if args.registros else FINAL_DIR
    if not registros_dir.is_dir() or not any(registros_dir.glob("*.json")):
        raise SystemExit(
            f"Nenhum registro JSON em {registros_dir}. "
            "A pasta padrão `registros_finais/` está vazia neste corpus: passe "
            "--registros dataset_raw/registros_anonimizados."
        )
    vereditos = carregar_vereditos(Path(args.vereditos) if args.vereditos else None)
    fala = fala_por_rotulo(registros_dir)
    # Arredondamento para cima, e não para o mais próximo: a 3%, 33 pessoas
    # somam no máximo 99% da fala, e o piso é 34. A 5% os dois coincidem em 20,
    # o que escondia o erro. O desconto mínimo absorve 1/0,05 não ser exato em
    # ponto flutuante.
    piso_pessoas = math.ceil(1 / args.teto - 1e-9)

    print(f"Teto de {args.teto:.0%} por pessoa; segundo piso de {args.minutos_por_falante} min por falante.")
    print("Fusões aplicadas a partir dos vereditos." if vereditos
          else "SEM vereditos: cada rótulo conta como uma pessoa (limite inferior da violação).")
    print()
    print(f"{'UF':4} {'pessoas':>7} {'fusões':>6} {'>teto':>5} {'maior':>6} {'concentr.':>9} "
          f"{'bruto':>7} {'c/ teto':>8} {'conserv.':>8} {'fatia/p':>8} {'úteis':>6} {'faltam':>6}")

    resultado = {}
    for uf in ESTADOS_VALIDOS:
        falas, fusoes, orfaos = fala_por_pessoa(fala.get(uf, {}), vereditos, uf)
        r = analisar_estado(falas, args.teto, args.minutos_por_falante)
        faltam = pessoas_novas_necessarias(falas, args.teto, args.minutos_por_falante,
                                           args.fala_pessoa_nova, piso_pessoas)
        r.update({"fusoes": fusoes, "vereditos_orfaos": orfaos, "pessoas_novas_necessarias": faltam})
        resultado[uf] = r
        print(f"{uf:4} {r['pessoas']:>7} {fusoes:>6} {r['pessoas_acima_do_teto']:>5} "
              # Uma casa decimal, igual à do valor gravado: arredondar de novo na
              # exibição levava 71,45% a aparecer como 72%.
              f"{r['maior_participacao_pct']:>5.1f}% {r['fala_concentrada_acima_do_teto_pct']:>8.1f}% "
              f"{r['fala_total_min']:>5.1f}mi {r['volume_sob_teto_min']:>6.1f}mi "
              f"{r['volume_conservado_pct']:>7.0f}% {r['fatia_maxima_por_pessoa_min']:>6.2f}mi "
              f"{r['pessoas_com_segundo_piso_apos_recorte']:>6} "
              f"{faltam if faltam is not None else 'n/d':>6}")
        if orfaos:
            print(f"     ATENÇÃO: {orfaos} veredito(s) sem rótulo correspondente, não aplicado(s).")

    print()
    print("maior      = participação da pessoa que mais fala, na fala do estado")
    print("concentr.  = fala somada das pessoas acima do teto")
    print("c/ teto    = volume que o estado conserva com o teto aplicado por recorte")
    print("fatia/p    = o máximo que qualquer pessoa pode contribuir nesse volume")
    print(f"úteis      = pessoas que conservam ao menos {args.minutos_por_falante} min após o recorte; "
          f"precisa alcançar {piso_pessoas}")
    print(f"faltam     = pessoas novas, com {args.fala_pessoa_nova} min de fala cada, para chegar a "
          f"{piso_pessoas} úteis")

    if args.saida:
        Path(args.saida).write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nGravado em {args.saida}")


if __name__ == "__main__":
    main()
