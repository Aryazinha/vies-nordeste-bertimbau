# Etapa 3 — Validar o corpus

**Objetivo.** Produzir as três medidas que sustentam as afirmações que o artigo fará sobre o corpus. Sem elas, o conjunto existe mas não é defensável.

**Estado:** não iniciada. **Pré-requisito:** a composição do corpus precisa estar **estável** — etapa 1 concluída e, se necessária, etapa 2 também. As amostras desta etapa são extraídas do corpus final; extraí-las antes obrigaria a refazê-las.

---

## Por que esta etapa não é formalidade

O projeto compara fala nordestina e fala do Sudeste. Cada uma das três medições abaixo existe para excluir uma explicação alternativa que, se não for excluída, derruba o resultado:

| Medição | A explicação alternativa que ela exclui |
|---|---|
| WER estratificado | "A diferença observada é erro do transcritor, não do modelo estudado" |
| Coerência dialetal | "Parte dos falantes ditos nordestinos migrou do Sudeste" |
| Participação de ouvinte | "O Nordeste foi gravado em situação mais informal que o controle" |

As três compartilham um traço: **o erro que produzem empurra o resultado na direção que favorece a hipótese do projeto.** É a pior direção para um viés passar despercebido, e a razão de nenhuma delas poder ser dispensada.

---

## 3.1 WER estratificado por variedade

**Adiado deliberadamente pela equipe em 31/08/2026.** Segue pendente por decisão, não por esquecimento.

**O que mede.** A taxa de erro da transcrição automática, **por estado**. Nunca só a média geral: o que importa é se o `faster-whisper` erra mais na fala nordestina que na sudestina. Se errar, a diferença medida entre as regiões seria viés de ferramenta apresentando-se como resultado sobre o modelo-alvo.

Medido corretamente, o WER estratificado é **resultado publicável por si só**, e não apenas controle de qualidade.

**O que existe.** O notebook gera `amostra_wer.json`, com até 20 minutos de trechos por estado, cada um trazendo `hipotese_asr` — o que o modelo transcreveu — e `referencia_manual` em branco. `pipeline_coleta_piloto/medir_wer.py` fecha a conta com a biblioteca `jiwer`, e informa quantos trechos ainda faltam preencher em vez de tratá-los como acerto.

**O que falta.** Trabalho humano: ouvir cada trecho e digitar exatamente o que foi dito, sem corrigir gramática nem expandir números por extenso, mantendo a convenção ortográfica do restante.

**Custo estimado:** 2 h de áudio ao todo; transcrição manual cuidadosa de fala espontânea com ruído leva de 4 a 8 vezes o tempo do áudio, o que dá **8 a 16 horas**. Divisível entre pessoas, porque os seis estados são arquivos independentes.

**Ressalva de dimensionamento:** os 20 minutos por estado são recomendação de bom senso registrada em `experimentos/meta_volume_corpus.py`, e **não** cálculo de poder como os que o projeto usa para os pares mínimos.

```bash
pip install jiwer
python medir_wer.py --entrada amostra_wer.json
```

---

## 3.2 Coerência dialetal — falante migrante

**O que mede.** Se os falantes atribuídos a um estado de fato falam a variedade daquele estado.

**Por que não é automatizável, e isso foi testado.** Duas vias foram consideradas e descartadas com base em achados do próprio projeto:

1. **Densidade de marcadores lexicais.** O item 2.4 de `docs/achados_para_o_artigo.md` mediu **zero** ocorrências desses itens em 30 mil palavras de fala nordestina genuína. Um detector assim marcaria como suspeito quase todo falante nordestino verdadeiro.
2. **Densidade de contextos de palatalização.** `densidade_palatalizacao.py` conta contextos **ortográficos**, não a realização fonética. Os mesmos contextos existem em qualquer fala do português.

A defesa efetiva é **curadoria manual, ouvindo**. `pipeline_coleta_piloto/preparar_amostra_coerencia.py` torna isso executável: amostra 10 locutores por estado, recorta o segmento mais longo de cada um e gera uma planilha com veredito em aberto — `coerente`, `suspeito` ou `inconclusivo`.

**Dimensionamento:** com 20 locutores por estado e amostra de 10, uma taxa real de migração de 15% teria cerca de 80% de chance de produzir ao menos uma detecção. É poder adequado para primeiro descarte, **não** para medir a taxa.

**A ameaça é direcional, e o documento precisa dizê-lo.** O vetor migratório dominante é Nordeste → Sudeste. Um falante migrado atenua o contraste medido e produz **aparência de ausência de viés** — ou seja, empurra na direção do resultado que o projeto encontrou.

```bash
python preparar_amostra_coerencia.py --estado PE --n 10
```

Requer o áudio, portanto o mesmo ambiente da etapa 1.

---

## 3.3 Participação de ouvinte

**O que mede.** Quanto do material, por estado, é fala de ouvinte participando de programa de rádio — o registro menos monitorado do corpus.

**Por que importa.** Os marcadores regionais que o projeto investiga são mais frequentes em fala informal. Se o grupo nordestino tiver esse tipo de fala e o controle não, o contraste entre as regiões fica inflado.

**O que já se sabe.** O formato foi confirmado em quatro canais — PE, CE e dois na BA — e em nenhum de PB, SP ou RJ. A busca dirigida por equivalentes em SP e RJ **falhou por razão estrutural**, não por falta de esforço: nas duas capitais, os programas de participação pertencem a redes nacionais, cujos ouvintes ligam do país inteiro e que por isso não satisfazem a regra de atribuição por estado.

**Consequência de método:** a simetria não é obtenível por busca, e por isso tem de ser obtida por **medida e desconto**.

**O que existe.** Dois campos, e a distinção entre eles é o ponto:

- `canal_tem_participacao_ouvinte`, herdado de `fontes.json`, que diz quais arquivos vale a pena ouvir;
- `participacao_ouvinte`, fato do arquivo, que só se estabelece ouvindo e nasce `nao_verificado`.

`pipeline_coleta_piloto/balanco_participacao.py` relata o volume por estado e compara os grupos.

**O trabalho é pequeno hoje.** Dos 52 arquivos coletados, **apenas um** vem de canal com o formato — 8,6 min da TV Aratu, na Bahia. A ameaça é **prospectiva**: incide sobre a coleta futura, se as rádios de participação passarem a ser exploradas.

```bash
python balanco_participacao.py                  # relatório
python balanco_participacao.py --marcar-canal   # repropaga a marca herdada do canal
```

---

## Ao terminar

1. Registrar as três medidas neste documento, com data.
2. Atualizar `docs/ficha_conjunto.md` — A.4 traz o WER como não medido.
3. Atualizar `docs/dataset-spec.md`, camada de validação, e `docs/pendencias.md` (4.9, 6.2, 1.1).
4. Levar o WER estratificado a `docs/achados_para_o_artigo.md`: é resultado, e não apenas controle.

**Advertência de escrita, que vale para as três.** Nenhuma dessas medições autoriza afirmar que o corpus é representativo da fala de um estado. Ele documenta fala pública de determinados canais. A distinção está em `docs/ficha_conjunto.md`, entre os usos desaconselhados, e não deve ser afrouxada porque as medições saíram favoráveis.
