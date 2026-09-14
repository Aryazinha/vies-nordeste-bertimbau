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

Medido por `pipeline_coleta_piloto/verificar_teto_falante.py --teto --vereditos`, com as fusões aplicadas.

**Precondição satisfeita em 12/09/2026:** o teto permanece em **5%**, declarado como convenção do projeto, com esta tabela a acompanhá-lo sempre que o valor for citado (`docs/dataset-spec.md` §1.4.5). **A etapa 2 está liberada para execução, com déficit de 27 pessoas.**

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
python selecionar_videos.py --deficit PE=3 CE=5 BA=5 SP=8 RJ=6 \
    --excluir-usados --saida plano_etapa2.json
python coletar_local.py plano_etapa2.json
```

**Os dois parâmetros foram acrescentados em 12/09/2026, e cada um corrige uma falha que o plano desta etapa previa em prosa mas o código não impedia:**

- `--excluir-usados` retira do plano os 35 canais que já estão no corpus. Sem ele, o seletor voltaria aos mesmos canais, e o resultado seria horas a mais da mesma pessoa — exatamente o erro descrito na seção 1.
- `--deficit` substitui a meta em horas por uma meta em **pessoas**, convertida em arquivos pelo rendimento medido sobre os 52 arquivos já coletados: 2,0 pessoas com ao menos 0,7 min de fala por arquivo de vox-pop, 1,5 por arquivo de podcast, 1,0 por canal de vlog. O vlog fica fora da conversão: rende uma pessoa por **canal**, não por arquivo.

Aplica-se ainda uma margem de 1,5× sobre o déficit (`--margem`), porque o piso de 20 é mínimo e não alvo: coletar o número exato deixaria o corpus sem folga para arquivo perdido no download, falante abaixo do segundo piso ou trecho descartado por qualidade.

### Plano gerado — 12/09/2026

| | Trechos | Horas | Canais | Pessoas esperadas |
|---|---|---|---|---|
| `plano_etapa2.json` — **a executar** | 25 | 1,86 | 25 | ~45 |
| `plano_etapa2_completo.json` — variante ampla | 43 | 3,91 | 39 | ~76 |

Distribuição do plano a executar: PE 3 trechos, CE 5, BA 5, SP 7, RJ 5. Nenhum dos 25 canais figura no corpus atual.

**Por que houve duas variantes, e por que a menor foi escolhida.** A fase de cobertura mínima de `planejar_camada` garante um vídeo por canal disponível — política correta para diversidade, que aqui produziu 43 trechos para um déficit de 27 pessoas. O custo do excedente não é a coleta, que é automática, mas a **revisão humana de anonimização**, que foi o trabalho mais pesado da rodada anterior. Decidiu-se, em 12/09/2026, pelo plano ajustado ao déficit com a margem de 1,5×.

O ajuste está no código, e não em recorte manual: `ajustar_ao_deficit` toma **um arquivo por canal**, alternando vox-pop e podcast, até o rendimento esperado alcançar o alvo. Um arquivo por canal é o que maximiza pessoas por arquivo coletado — o segundo arquivo de um canal traz de novo o apresentador, que é a recorrência de onde o déficit veio. `--sem-ajuste` reproduz a variante ampla.

### Coleta executada — 12/09/2026

**25 de 25 trechos coletados, nenhuma falha de download.** O corpus passa de 52 para **77 arquivos**, com 1,84 h novas, distribuídas em PE 3, CE 5, BA 5, SP 7 e RJ 5, vindas de **25 canais distintos, todos novos**. Não houve perda concentrada em estado ou camada — a verificação exigida na seção 4, cujo motivo é que perda desigual entre grupos é viés de amostragem, e não ruído.

**Uma falha silenciosa ocorreu e foi corrigida.** O plano incluiu um vídeo que já estava no corpus: o canal figura como "TV Câmara São Paulo" em `fontes.json` e como "TV CÂMARA SÃO PAULO" nos registros da primeira rodada, e a exclusão de canais já usados comparava os nomes literalmente. O sintoma foi indireto — a fusão dos metadados somou 52 e 25 e resultou 76, não 77 —, e o efeito seria SP receber seis arquivos úteis em vez de sete, sem que nada no plano o indicasse.

Duas barreiras foram acrescentadas a `selecionar_videos.py`, e a segunda existe porque a primeira pode falhar de outro modo:

1. `normalizar_canal` compara nomes sem acento e sem caixa, e `canais_ja_usados` passa a ler também `metadados.json` — que é onde o canal aparece na janela entre a coleta e o processamento, quando o registro diarizado ainda não existe.
2. `videos_ja_coletados` exclui por identificador de vídeo, independentemente do nome do canal.

O arquivo faltante de SP foi reposto por `plano_etapa2_complemento.json`, de canal novo, o que restabelece os sete previstos.

### Processamento e anonimização — 12/09/2026

Transcrição e diarização dos 25 arquivos executadas no Colab, com o notebook ajustado para processar apenas o que ainda não tinha registro — a esteira passou a ser incremental, e reprocessar os 52 antigos custaria GPU sem produzir nada.

Anonimização concluída no mesmo dia (`docs/anonimizacao.md`, seção 8): 153 nomes detectados, 89 mascarados, 64 mantidos. O corpus anonimizado passa a ter **77 arquivos**.

**Situação do teto, com o corpus ampliado e as fusões conhecidas:**

| UF | Pessoas | Acima do teto | Com o teto aplicado | Fatia por pessoa | Pessoas úteis | Faltam |
|---|---|---|---|---|---|---|
| PB | 28 | 9 | 29,3 min | 1,46 min | 20 | 0 |
| PE | 34 | 8 | 35,4 min | 1,77 min | 22 | 0 |
| CE | 43 | 4 | 63,6 min | 3,18 min | 27 | 0 |
| BA | 35 | 6 | 37,4 min | 1,87 min | 22 | 0 |
| SP | 44 | 7 | 47,0 min | 2,35 min | 21 | 0 |
| RJ | 46 | 5 | 35,8 min | 1,79 min | 20 | 0 |

**Nenhum estado tem déficit — mas o número ainda não é final.** As fusões aplicadas são as da conferência de 10/09, que só cobria os 52 arquivos antigos; as vozes dos 25 novos ainda não foram comparadas com nada. **PB e RJ estão exatamente no piso**, de modo que uma única fusão em qualquer um deles o derruba. Fechar exige repetir a etapa 1 sobre os 77, que é o passo seguinte previsto na seção 5.

---

## Etapa concluída — 14/09/2026

A etapa 1 foi repetida sobre os 77 arquivos e a conferência humana, completada. **O critério adotado em 12/09/2026 está satisfeito nos seis estados.**

| UF | Vozes | Fusões | Pessoas distintas | Pessoas úteis sob o teto | Piso | Margem |
|---|---|---|---|---|---|---|
| PB | 30 | 4 | 26 | 20 | 20 | **0** |
| PE | 33 | 2 | 31 | 21 | 20 | +1 |
| CE | 38 | 1 | 37 | 27 | 20 | +7 |
| BA | 32 | 0 | 32 | 22 | 20 | +2 |
| SP | 40 | 0 | 40 | 21 | 20 | +1 |
| RJ | 41 | 0 | 41 | 20 | 20 | **0** |
| **Total** | **214** | **7** | **207** | — | **120** | — |

Corpus final: **77 arquivos, 7,36 h, 59 canais distintos** — 36 de vox-pop, 30 de podcast, rádio e TV, 11 de vlog. Contra os 52 arquivos, 5,52 h e 35 canais de antes da etapa.

**O que a etapa 2 entregou, em pessoas:** de 148 para 207 falantes distintos, e — o número que o critério mede — de 63 para 131 pessoas que conservam fala suficiente depois do recorte pelo teto. SP saiu de zero pessoas úteis para 21, CE de zero para 27.

### A ressalva que fica, e ela não é pequena

**PB e RJ ficaram exatamente em 20, sem margem alguma.** O critério está satisfeito, mas no limite exato: a exclusão de um único falante — por qualidade de áudio, por suspeita de migração (`docs/pendencias.md`, D-6.2) ou por revisão de coerência dialetal na etapa 3 — derruba qualquer um dos dois abaixo do piso e reabre esta etapa.

É exatamente o risco que `meta_corpus_autonomo.md` antecipa ao dizer que "o piso de 20 é mínimo, não alvo". PB não recebeu arquivo algum nesta rodada, porque entrou nela sem déficit; RJ recebeu cinco e chegou a 20 na conta exata.

**Encaminhamento sugerido, a decidir pela equipe:** uma rodada curta para PB e RJ, de três a quatro canais novos cada, antes da etapa 3. Custa pouco — o seletor já exclui canais usados, e restam canais verificados não empregados nos dois estados — e compra margem para as exclusões que a etapa 3 previsivelmente produzirá. Executar a etapa 3 sobre um corpus sem margem significa arriscar refazer as duas etapas anteriores por causa de um descarte.

### Rodada de margem para PB e RJ — 14/09/2026

Executada, por decisão da equipe, antes da etapa 3. **6 arquivos, 0,59 h, 6 canais novos**; o corpus vai a **83 arquivos**.

| UF | Trechos | Composição | Pessoas esperadas |
|---|---|---|---|
| PB | 3 | 2 vox-pop, 1 podcast | ~5,5 |
| RJ | 3 | 1 vox-pop, 1 podcast, 1 vlog | ~4,5 |

**RJ obrigou a mudar o seletor, e a mudança tem razão de método.** O estado tinha apenas **um** canal de vox-pop e **um** de podcast ainda não empregados, contra onze de vlog. A conversão de déficit em arquivos ignorava o vlog — regra correta na rodada anterior, onde havia canais de sobra nas camadas de melhor rendimento, e errada aqui: RJ pediria três pessoas, encontraria dois canais e pararia, sem que nada indicasse que a meta era inalcançável pelo caminho preferido.

O vlog passa a ser **reserva**, e não alternativa: `ORDEM_DAS_CAMADAS` consome vox-pop e podcast em rodízio e só recorre ao vlog quando ambos se esgotam. A justificativa é a mesma que o mantinha fora — um canal de vlog é uma pessoa, por mais vídeos que tenha —, mas ela corta nos dois sentidos: quando o que falta é *uma* pessoa e não há mais entrevista disponível, um canal de vlog novo entrega exatamente isso.

**Uma falha de download, e ela não era viés.** O vox-pop de RJ falhou na primeira tentativa e foi coletado na retentativa, sem alteração de parâmetro — falha passageira de rede, não recusa da plataforma. A conferência importava porque a perda recaía sobre o único estado com apenas um canal disponível naquela camada, e perda concentrada em um grupo é viés de amostragem (seção 4).

Digno de registro para a etapa 3: o vídeo de vox-pop de RJ é de canal carioca, mas seu assunto é Campos do Jordão, em São Paulo. A regra de atribuição do projeto deriva `estado_alvo` do canal, e não do conteúdo; o caso é candidato natural à checagem de coerência dialetal prevista naquela etapa.

#### Resultado da rodada de margem

Os 6 arquivos foram transcritos, diarizados e anonimizados. **A margem pretendida foi obtida:**

| UF | Pessoas úteis antes | Depois | Margem sobre o piso |
|---|---|---|---|
| PB | 20 | **23** | +3 |
| RJ | 20 | **23** | +3 |

Os demais estados não se alteram: PE 21, CE 27, BA 22, SP 21.

Corpus após a rodada: **83 arquivos, 7,96 h, 65 canais** — 39 de vox-pop, 32 de podcast, rádio e TV, 12 de vlog.

**A anonimização dos 6 confirmou o padrão da rodada anterior, agora em escala menor:** dos 22 nomes detectados, apenas 4 foram mascarados. O detector confundiu com pessoa privada uma instituição (`Draco`, delegacia), um hospital (`Trauma`), duas figuras históricas da engenharia (`Costa Nunes`, `Manuel Rocha`), um serviço creditado (`Carlos Drone BH`), um verbo (`nominei`) e três expressões correntes (`Deus der`, `Senhor Jesus`, `Homicidas`). Em sentido inverso, `Roberto` fora classificado como equipe do canal e é um jogador citado por outro — foi mascarado na revisão.

**Ressalva:** as vozes dos 6 arquivos novos ainda não passaram pela comparação da etapa 1, de modo que os números acima não descontam eventuais fusões entre eles e o corpus existente. A margem de +3 absorve até três fusões por estado sem que o piso seja perdido, mas fechar o corpus exige uma última passagem da etapa 1 sobre os 83.

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
