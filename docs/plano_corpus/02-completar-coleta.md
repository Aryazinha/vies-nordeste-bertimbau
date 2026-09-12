# Etapa 2 — Completar a coleta

**Necessária, por decisão de 10/09/2026.** Previa-se condicional — só se a etapa 1 apurasse menos de 20 falantes distintos em algum estado —, e por esse critério não seria: todos os estados o superam. O que a tornou necessária foi a mudança do critério, depois de a etapa 1 mostrar que o piso de falantes não garante o teto de 5% de que deriva ([`01-verificar-falantes.md`](01-verificar-falantes.md), seção 7.1).

**Estado:** não iniciada. **Onde roda:** máquina local, nunca no Colab.

**Leia antes:** [`01-verificar-falantes.md`](01-verificar-falantes.md), que produz o insumo desta etapa — em especial a seção 7.1.

---

## Déficit apurado na etapa 1 — 10/09/2026

**O critério mudou, e o déficit se mede nele.** Não basta alcançar 20 pessoas distintas: exigem-se 20 pessoas que conservem ao menos 0,7 minuto de fala depois de aplicado o teto de 5% por recorte. A consequência prática orienta toda esta etapa: **o que falta é pessoa, e não hora.** Acrescentar fala a quem já fala muito não ajuda, porque o excedente é recortado.

| UF | Falantes distintos | Pessoas úteis após o recorte | Piso | Pessoas novas necessárias |
|---|---|---|---|---|
| PB | 26 | 20 | 20 | 0 |
| PE | 27 | 17 | 20 | 3 |
| CE | 22 | 0 | 20 | 5 |
| BA | 22 | 0 | 20 | 5 |
| SP | 21 | 0 | 20 | 8 |
| RJ | 30 | 14 | 20 | 6 |
| **Total** | **148** | — | — | **27** |

Números de 12/09/2026, de `pipeline_coleta_piloto/verificar_teto_falante.py --vereditos`, **com as seis fusões da conferência aplicadas**. Elas confirmaram o efeito previsto: PB perdeu uma pessoa útil e ficou **exatamente no piso**, sem margem alguma, e PE passou de duas pessoas novas a três.

"Pessoas novas necessárias" é o menor número de falantes novos, cada um com ao menos um minuto de fala, que eleva a 20 as pessoas úteis. Um estado com zero pessoas úteis não precisa de vinte novas porque cada pessoa acrescentada eleva o volume admissível e, com ele, a fatia de todas as outras, de modo que falantes já presentes passam a alcançar o segundo piso. Pela mesma razão o resultado é idêntico supondo de um a três minutos por pessoa nova: o que excede a fatia é recortado.

**Duas observações para o planejamento.** Primeira: quase metade do déficit — 14 das 26 pessoas — está no grupo de controle, SP e RJ, o que é compatível com a restrição de simetria da seção 3, e não a agrava. Segunda: "pessoa nova" significa falante com turno de fala real, de ao menos um minuto; o transeunte de uma frase no vox-pop não conta, por mais numeroso que seja.

### Precondição: fechar o valor do teto antes de coletar

O déficit acima vale para o teto de 5%, cujo valor **não tem fundamento documentado** no projeto (`docs/pendencias.md`, D-6.4). E é o valor que decide o tamanho desta etapa:

| Teto | Piso de pessoas úteis | Pessoas novas necessárias |
|---|---|---|
| 10% | 10 | 0 — coleta concluída |
| 5% | 20 | 27 |
| 3% | 34 | 111 |

Medido por `pipeline_coleta_piloto/verificar_teto_falante.py --teto --vereditos`, com as fusões aplicadas. Pela decisão registrada em `CLAUDE.md` de fechar a camada de definição do dataset antes de qualquer execução de coleta, **esta etapa não deve começar** sem que o valor seja fundamentado em literatura ou declarado, com esta tabela ao lado, como convenção do projeto.

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

4. **Verificação do teto** com `pipeline_coleta_piloto/verificar_teto_falante.py --vereditos`, que diz se o critério adotado em 10/09/2026 foi atingido. A etapa 1 sozinha não basta: ela conta pessoas distintas, e o critério exige 20 pessoas que conservem o segundo piso de fala depois do recorte pelo teto.

O ciclo pode repetir-se. Só termina quando os seis estados atingem esse critério.

---

## 6. Ao terminar

1. Preencher a tabela de déficit no alto deste documento com o resultado da reverificação.
2. Atualizar `docs/dataset-spec.md`, seção "Camada de execução, em números".
3. Registrar em `docs/pendencias.md` qualquer perda concentrada de coleta.
4. Só então ir para [`03-validar.md`](03-validar.md).
