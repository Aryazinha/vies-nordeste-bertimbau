# Etapa 2 — Completar a coleta, se faltar

**Condicional.** Só se executa se a etapa 1 apurar menos de 20 falantes distintos em algum estado.

**Estado:** não iniciada, e ainda não se sabe se será necessária. **Onde roda:** máquina local, nunca no Colab.

**Leia antes:** [`01-verificar-falantes.md`](01-verificar-falantes.md), que produz o insumo desta etapa.

---

## Déficit apurado na etapa 1

*A preencher pela sessão que executar a etapa 1.*

| UF | Falantes distintos | Piso | Déficit |
|---|---|---|---|
| PB | — | 20 | — |
| PE | — | 20 | — |
| CE | — | 20 | — |
| BA | — | 20 | — |
| SP | — | 20 | — |
| RJ | — | 20 | — |

---

## 1. A regra que governa esta etapa

**Coletar mais do mesmo canal não resolve.** É o erro natural e o mais provável de se cometer, porque é o caminho mais fácil: os canais já estão levantados e verificados.

Mas o déficit de falantes vem justamente da recorrência — o repórter que reaparece em todo episódio. Baixar mais episódios do mesmo canal acrescenta horas e **não acrescenta pessoas**, além de empurrar aquele falante contra o teto de 5%.

**O déficit se cobre com canal novo.** E há margem: `pipeline_coleta_piloto/fontes.json` traz **152 canais verificados, dos quais apenas 35 foram empregados**.

---

## 2. Rendimento esperado por camada

Do cálculo em `experimentos/meta_corpus_autonomo.py`:

| Camada | Falantes no primeiro arquivo | Novos por arquivo adicional |
|---|---|---|
| `entrevista_vox_pop` | vários | positivo — cada episódio traz entrevistados novos |
| `podcast_radio_tv_regional` | vários | positivo — convidados novos |
| `vlog_amador` | 1 | **zero** — um canal é uma pessoa, por mais vídeos que tenha |

**Consequência prática:** para cobrir déficit de falantes, priorizar **vox-pop e podcast**. Vlog só acrescenta falante quando se acrescenta canal, nunca quando se acrescenta vídeo.

---

## 3. Restrições que não podem ser violadas ao completar

| Restrição | Onde está | O que significa aqui |
|---|---|---|
| Teto de 5% por falante | `docs/fontes_coleta.md`, 2.4.5 | Nenhum falante pode dominar o material de um estado — é a origem do piso de 20 |
| Teto de 35% por canal | `TETO_POR_CANAL` em `selecionar_videos.py` | Um canal não pode responder por mais de 35% do piso do estado |
| Simetria entre grupos | `docs/pendencias.md`, D1 | O que importa é a comparabilidade entre Nordeste e controle, não o máximo por estado. Reforçar só o Nordeste recria a assimetria que a rodada de 31/08 desfez |
| Regra de atribuição | `docs/fontes_coleta.md`, §1 | `estado_alvo` vem do canal, jamais da consulta de busca ou do título do vídeo |
| Participação de ouvinte | `docs/pendencias.md`, 1.1 | Fala de ouvinte é o registro menos monitorado do corpus. Se entrar em volume desigual entre os grupos, infla o contraste regional na direção que favorece a hipótese do projeto. Ver a etapa 3 |

---

## 4. Execução

A coleta roda **na máquina local**, e não no Colab. O motivo está registrado em `notebooks/README.md`: o YouTube recusa downloads originados de datacenter, e a tentativa de 27/08/2026 no Colab resultou em **0 de 51 vídeos**, todos com *"Sign in to confirm you're not a bot"*. O mesmo plano executa normalmente em conexão residencial.

```bash
cd pipeline_coleta_piloto
python selecionar_videos.py --saida plano_complemento.json   # ajustar os filtros ao déficit
python coletar_local.py plano_complemento.json
```

`selecionar_videos.py` exclui automaticamente canais marcados `a_confirmar` e `rejeitado`, e deriva `estado_alvo`, `tipo_fonte` e `canal_tem_participacao_ouvinte` do próprio `fontes.json` — nunca digitados à mão.

**Perda de coleta não é ruído.** Vídeos com restrição etária falham no download, e a restrição recai tipicamente sobre matéria de violência, que é parcela expressiva do vox-pop policial. Perda desigual entre estados é viés de amostragem. Conferir se as falhas se concentram em algum estado ou camada, e registrar (`docs/pendencias.md`, 4.5).

---

## 5. Depois de coletar

O material novo precisa passar pelo mesmo caminho do anterior, na ordem:

1. **Transcrição e diarização** no Colab (`notebooks/piloto_colab.ipynb`) — exigem GPU
2. **Anonimização** dos registros novos (`docs/anonimizacao.md`) — a política das quatro categorias e as listas de exclusão já estão no script, de modo que a revisão dos arquivos novos parte de uma base bem melhor que a primeira
3. **Etapa 1 outra vez**, agora sobre o corpus ampliado — e é ela que diz se o déficit foi coberto

O ciclo pode repetir-se. Só termina quando os seis estados atingem o piso.

---

## 6. Ao terminar

1. Preencher a tabela de déficit no alto deste documento com o resultado da reverificação.
2. Atualizar `docs/dataset-spec.md`, seção "Camada de execução, em números".
3. Registrar em `docs/pendencias.md` qualquer perda concentrada de coleta.
4. Só então ir para [`03-validar.md`](03-validar.md).
