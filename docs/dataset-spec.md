# Especificação dos Conjuntos de Dados

**Função deste documento.** Consolidar em definição única o que hoje está distribuído entre `CLAUDE.md`, os documentos de `docs/`, o código de `pipeline_coleta_piloto/` e os relatórios de `experimentos/resultados/`. Não introduz decisão nova: onde o material é omisso, o ponto é marcado como `PENDENTE` e permanece omisso.

**Produzido em:** 28/08/2026, por leitura do material existente, sem alteração de arquivo algum. **Revisado em 29/08/2026**, quando o campo `duracao_coletada_s` foi acrescentado ao esquema e preenchido retroativamente, encerrando o primeiro item do registro de pendentes. Os pacotes `piloto_resultados (1).zip` e `(2).zip` não foram abertos em nenhuma das duas ocasiões, por conterem transcrição não anonimizada.

**Convenção de procedência.** Toda afirmação não trivial indica entre parênteses o arquivo e a seção de origem. Valores marcados como *apurados* foram obtidos por leitura direta de `pipeline_coleta_piloto/dataset_raw/metadados.json` e de `pipeline_coleta_piloto/fontes.json`, e não constavam somados em documento algum.

**Os dois conjuntos estão em estados incomparáveis**, e o documento não os apresenta em paralelo por isso. O corpus de áudio tem especificação fechada e execução em curso. O conjunto de pares mínimos tem desenho conceitual, mas nenhuma definição de entrega, e seu conteúdo perdeu sustentação empírica em 28/08/2026 (`docs/roadmap.md`, passo 5.1).

---

# Estado por camada — leia primeiro

Esta seção existe para desfazer uma confusão de leitura que o restante do documento poderia induzir. Um conjunto de dados atravessa **três camadas** — definir, executar e validar —, e o presente documento cobre por inteiro apenas a primeira. Especificação fechada não é conjunto pronto, e a distância entre as duas coisas é, no corpus de áudio, de aproximadamente nove décimos do trabalho.

| Camada | O que é | Corpus de áudio | Pares mínimos |
|---|---|---|---|
| **Definir** | Esquema, critérios de inclusão, meta e regras de publicação | **Fechada** por este documento, ressalvados os pendentes de decisão listados ao final | **Aberta.** As quatro definições de entrega dependem da decisão do passo 5 (Parte 2, §2.1) |
| **Executar** | Coleta, transcrição, diarização e curadoria | **11% da meta vigente** | Sem objeto: não há conteúdo a executar enquanto a família de marcadores não estiver decidida |
| **Validar** | WER e DER contra referência humana; Filtros 1 e 2 | **Não iniciada.** Zero das 2 h de transcrição manual de referência | **Não iniciada.** Nenhum item submetido ao Filtro 1, nenhum juiz consultado (`docs/achados_para_o_artigo.md` §3.3) |

## Camada de execução, em números

Apurado sobre `dataset_raw/metadados.json` e `fontes.json`, contra a meta vigente de 8,3 h de áudio bruto por estado e 50 h no conjunto (§1.5).

| UF | Coletado | Sobre a meta | Canais empregados / disponíveis |
|---|---|---|---|
| PB | 1,15 h | 13,8% | 6 / 12 |
| RJ | 1,01 h | 12,1% | 6 / 17 |
| BA | 1,00 h | 12,1% | 6 / 12 |
| SP | 0,85 h | 10,2% | 6 / 19 |
| CE | 0,79 h | 9,5% | 6 / 16 |
| PE | 0,73 h | 8,8% | 5 / 12 |
| **Total** | **5,52 h** | **11,0%** | **35 / 88** |

Restam cerca de 44 h a coletar, transcrever e diarizar. A camada de validação está integralmente por fazer: o WER estratificado por variedade — que é a única medida capaz de sustentar a afirmação de que a transcrição automática não penaliza a fala nordestina, hoje apoiada apenas em confiança do modelo (`docs/achados_para_o_artigo.md` §2.1) — exige 2 h de transcrição manual de referência, das quais nenhuma foi produzida.

## A circularidade que a tabela não mostra

Uma das pendências não apenas falta: ela **altera o critério de conclusão das outras duas camadas**.

A meta de 50 h não foi escolhida, e sim derivada do requisito de detectar a negação pós-verbal em volume que torne sua ausência informativa (§1.5). O corpus está, portanto, dimensionado para **validar marcadores** — é a função instrumental descrita em §1.1.

Ocorre que o passo 5.1 do roadmap estabeleceu que nenhuma das quatro famílias de marcadores testadas produz resposta no modelo (Parte 2, §2.1). Coletar as 44 h restantes hoje produziria material cuja função de validação está suspensa junto com os marcadores que ele validaria.

E, caso o rumo adotado seja o 5.3 — reposicionar o trabalho como artigo de método e recurso —, o corpus deixa de ser instrumento e passa a entregável autônomo. O critério de conclusão muda por inteiro: deixa de ser a detecção de uma variante rara e passa a ser diversidade de falantes, simetria entre grupos e WER estratificado. Não há razão para supor que o volume resultante seja 50 h, nem que sejam as mesmas 50 h.

**Segue-se a ordenação de trabalho.** Decidir o passo 5 → recalcular o critério de conclusão do corpus conforme a decisão → executar a coleta → validar. As pendências de licença e de ficha de conjunto correm em paralelo, por não dependerem daquela decisão.

---

# Parte 1 — Corpus de áudio

Especificação fechada. Descreve o que já está decidido, implementado e em execução.

## 1.1 Objeto e função

Corpus de fala espontânea regional, coletado de plataformas públicas, cobrindo quatro estados nordestinos — PB, PE, CE, BA — contra um grupo de controle formado por SP e RJ, capital e interior (`CLAUDE.md` §1.4.3).

A função no desenho original é **instrumental**: serve ao Filtro 2 do protocolo de validação, segundo o qual um marcador dialetal só integra o experimento de texto se ocorrer em fala espontânea nas transcrições coletadas para o estado correspondente (`docs/pares_minimos_v1.md` §7). O corpus existe para impedir que o instrumento se apoie em estereótipo de circulação popular em lugar de traço atestado (`CLAUDE.md` Parte 3, validade de construto).

### Decisão de 29/08/2026: o corpus é entregável autônomo

**A função instrumental descrita acima deixou de ser a principal.** A equipe decidiu que o corpus de áudio passa a **entregável autônomo** — corpus de fala regional publicado por si, e não apenas instrumento de validação de marcadores.

**A razão é o resultado do passo 5.** O corpus fora dimensionado para confirmar marcadores dialetais em fala espontânea, e quatro famílias de marcadores implícitos foram testadas sem que nenhuma produzisse resposta no modelo (`docs/achados_para_o_artigo.md`, item 1.15). Um instrumento de validação sem nada a validar não se sustenta como justificativa de coleta.

**Três consequências, todas registradas nas seções seguintes:**

1. **A meta muda de unidade.** Deixa de ser volume de fala para detectar uma variante rara e passa a ser **cobertura de falantes**. Nova derivação em §1.5.
2. **As definições de entrega passam a valer para ele.** Formato de distribuição, licença e ficha de conjunto — antes exigidas apenas do conjunto de pares mínimos — tornam-se exigíveis também para o corpus.
3. **O Filtro 2 não desaparece, mas deixa de ser o que dimensiona.** Continua sendo o procedimento pelo qual um marcador se confirma em fala real; apenas não é mais a razão de ser do corpus.

## 1.2 Dois registros distintos, e a relação entre eles

O material emprega **dois formatos de registro**, correspondentes a duas etapas. A distinção não está declarada em nenhum documento e foi reconstruída a partir do código; registrá-la é uma das razões de ser deste arquivo.

| Registro | Onde vive | Escrito por | Etapa |
|---|---|---|---|
| **Registro de coleta** | `dataset_raw/metadados.json`, lista única | `coletar_local.py` | Após o download do áudio, antes do processamento |
| **Registro final** | `dataset_raw/registros_finais/{id}.json`, um por vídeo | `pipeline.py`, função `_montar_registro_final` | Após transcrição e diarização |

O registro final é o registro de coleta acrescido de `transcricao` e `diarizacao`, e **sem** o campo `arquivo` (`pipeline_coleta_piloto/pipeline.py`, `_montar_registro_final`). Ambos os registros trazem `duracao_coletada_s`, acrescentado em 29/08/2026 (§1.3). O campo auxiliar `title`, usado apenas na triagem, é removido e não integra o esquema publicado (`pipeline_coleta_piloto/collect.py`, `VideoMetadata`).

O esquema descrito na seção 1.4.1 do `CLAUDE.md` corresponde ao **registro final**, não ao de coleta: lista `transcricao` e `diarizacao`, e não menciona `arquivo` nem `trecho`. O campo `trecho` é extensão posterior, declarada como parte do esquema publicado e não como auxiliar, porque publicar identificador de vídeo sem o recorte utilizado não permitiria reconstruir o material analisado (`pipeline_coleta_piloto/collect.py`, docstring de `VideoMetadata`).

> `PENDENTE:` qual dos dois registros constitui o artefato publicado. A regra de publicação está fixada quanto ao conteúdo — identificadores e código, nunca áudio (`CLAUDE.md` §1.4.2) —, mas nenhum documento declara se o que se publica é o registro de coleta, o registro final, ou ambos.

## 1.3 Esquema do registro de coleta

Nove campos, tal como gravados em `dataset_raw/metadados.json`. Vocabulário controlado conforme `pipeline_coleta_piloto/config.py`.

| Campo | Tipo | Vocabulário controlado | Obrigatório |
|---|---|---|---|
| `id` | string | Identificador de vídeo do YouTube, 11 caracteres. Chave primária do registro (`CLAUDE.md` §1.4.1) | Sim |
| `canal` | string | Livre. Nome do canal de origem, mantido por tratar-se de conteúdo público publicado voluntariamente (`CLAUDE.md` §1.4.2) | Sim |
| `data_upload` | string | Data de publicação no formato `AAAAMMDD`, sem separadores. Declarado `Optional` no código (`collect.py`, `VideoMetadata`) | Não |
| `duracao_s` | inteiro | Segundos. Declarado `Optional` no código | Não |
| `estado_alvo` | string | **Exatamente um de:** `PB`, `PE`, `CE`, `BA`, `SP`, `RJ` (`config.py`, `ESTADOS_VALIDOS`). Os quatro primeiros formam o grupo-alvo, os dois últimos o de controle | Sim |
| `tipo_fonte` | string | **Exatamente um de:** `entrevista_vox_pop`, `podcast_radio_tv_regional`, `vlog_amador` (`config.py`, `TIPOS_FONTE_VALIDOS`) | Sim |
| `trecho` | objeto ou `null` | `null` quando o vídeo foi coletado por inteiro; objeto `{"inicio_s": inteiro, "fim_s": inteiro}` quando apenas um recorte foi baixado. Regra de recorte em 1.4.6 | Sim, admitindo `null` |
| `arquivo` | string | Nome do arquivo de áudio, no formato `{id}.wav` (`coletar_local.py`). Não integra o registro final | Sim |
| `duracao_coletada_s` | inteiro | Segundos de áudio **efetivamente coletados**: `fim_s − inicio_s` quando há recorte, `duracao_s` quando não há. É este o campo a somar para obter o volume do corpus | Sim |

**Estado atual dos valores**, apurado sobre os 52 registros existentes: `estado_alvo` distribui-se em PB 10, CE 10, PE 9, RJ 9, BA 7, SP 7; `tipo_fonte` em `entrevista_vox_pop` 21, `podcast_radio_tv_regional` 20, `vlog_amador` 11; `trecho` é `null` em 38 registros e objeto em 14. Nenhum valor fora do vocabulário controlado.

### Sobre a distinção entre `duracao_s` e `duracao_coletada_s`

Os dois campos coexistem, e confundi-los altera o volume do corpus por um fator de dois. **`duracao_s` é a duração do vídeo de origem; `duracao_coletada_s` é a do áudio que existe em disco.** Divergem sempre que o vídeo excede `LIMITE_TRECHO_S` e apenas um recorte é baixado (§1.4.6). Sobre os 52 registros atuais, a soma de `duracao_s` é de 11,43 h e a de `duracao_coletada_s` é de 5,52 h, que é o valor reportado em todos os documentos do projeto.

**Origem da distinção.** Até 29/08/2026 existia apenas `duracao_s`, sem que documento algum declarasse seu significado e sem que o nome o desambiguasse. Um consumidor que somasse o campo obteria o dobro do corpus real **sem receber erro** — defeito da classe catalogada em `docs/pendencias.md` §5-A, que produz número plausível em vez de falha.

**Por que um campo novo, e não a redefinição do existente.** Os produtos de transcrição e diarização já gerados foram escritos sob a semântica antiga. Alterar o significado de `duracao_s` em silêncio tornaria os lotes incoerentes entre si, que é exatamente o modo de falha que a correção pretende encerrar. `duracao_s` permanece, portanto, com o significado que sempre teve.

**Implementação.** Função `duracao_coletada_s` em `pipeline_coleta_piloto/collect.py`, empregada por `coletar_local.py` no registro de coleta e por `pipeline.py` no registro final. Os 52 registros existentes foram preenchidos retroativamente, com verificação de que nenhum outro campo se alterou.

## 1.4 Critérios de inclusão

### 1.4.1 Regra de atribuição: pelo canal, nunca pela consulta

O campo `estado_alvo` é atribuído **pelo canal, jamais pela consulta de busca ou pelo título do vídeo** (`docs/fontes_coleta.md` §1). Um canal só entra na lista se satisfizer um destes dois critérios:

- **Vínculo institucional com o estado** — emissora, rádio, jornal ou órgão público ali sediado. Atribuição verificável e estável.
- **Evidência geográfica recorrente no próprio conteúdo** — para criadores independentes, menção repetida a municípios identificáveis do estado nos títulos ou descrições recentes.

Canal que não satisfaça nenhum dos dois é rejeitado, ainda que o conteúdo pareça adequado.

**A regra não é cautela, é correção de um erro medido.** A primeira rodada de levantamento buscou por formulações de conteúdo, e a fórmula jornalística "moradores reclamam da rua" é idêntica em todo o país: a consulta de Pernambuco devolveu TV Gaspar, de Santa Catarina, e TVG Várzea Grande, do Mato Grosso; a da Bahia devolveu Balanço Geral MG; a de São Paulo, SBT MS; a do Ceará, Balanço Geral Joinville (`docs/fontes_coleta.md` §1.1). Rotular `estado_alvo` a partir da consulta introduziria erro de medida na própria variável independente do estudo — não ruído aleatório, mas contaminação sistemática do contraste medido.

### 1.4.2 Camadas de fonte

Duas camadas, com a lógica de diversidade diafásica do C-ORAL-BRASIL (`CLAUDE.md` §1.4.3):

| Camada | `tipo_fonte` correspondente | Proporção prevista | Fundamento |
|---|---|---|---|
| Âncora | `entrevista_vox_pop`, `podcast_radio_tv_regional` | 60% a 70% do volume | Áudio mais limpo, com WER e DER esperados mais baixos |
| Espontânea | `vlog_amador` | 30% a 40% do volume | Fala mais informal, exigindo verificação manual mais criteriosa |

A repartição interna da camada âncora — 35% para vox-pop e 30% para podcast, rádio e TV — consta do cálculo de volume (`experimentos/resultados/historico/meta_volume.md`, tabela de conversão), e é compatível com a faixa de 60% a 70% fixada no protocolo.

**Estado atual**, apurado por horas efetivamente coletadas: `podcast_radio_tv_regional` 34,7%, `vlog_amador` 33,3%, `entrevista_vox_pop` 32,0%. A camada âncora soma 66,7% e a espontânea 33,3%, ambas dentro das faixas previstas.

**Qualificação da camada âncora.** O levantamento mostrou que ela carrega custo não previsto: apresentadores e repórteres empregam variedade de radiodifusão deliberadamente neutralizada, e parte do conteúdo institucional consiste em sabatinas com políticos, cuja fala pública é profissionalmente treinada — exatamente os falantes em que os marcadores dialetais estão mais suprimidos. O que interessa na camada não é o jornalismo de estúdio, e sim os segmentos em que fala gente comum: rádio com participação do ouvinte e vox-pop de reportagem local (`docs/fontes_coleta.md` §2.1).

> `PENDENTE:` a composição entre camadas está sob revisão não decidida. O rádio com participação de ouvinte fornece, por hora coletada, mais falantes distintos que o vlog, com atribuição mais segura, situação jurídica mais clara e áudio melhor; recomenda-se deslocar volume nessa direção, mas a alteração exige revisão formal do protocolo e não deve ser adotada tacitamente (`docs/fontes_coleta.md` §2.4.5; `docs/pendencias.md` D2).

### 1.4.3 As quatro armadilhas que excluem um canal

Quatro classes de canal satisfazem os critérios geográficos e não servem ao propósito, cada uma por motivo distinto (`docs/fontes_coleta.md` §2.4 e §2.5).

**1. Canal itinerante.** Canais de viagem, motovlog, caminhoneiro e entusiasta de transporte percorrem o estado e o citam abundantemente. A menção a *muitos* municípios era, no critério original, o sinal mais forte de pertencimento, quando é a assinatura de quem está de passagem. Caso exemplar: canal aprovado por citar João Pessoa, Campina Grande, Guarabira e Sapé, cujo conteúdo são trajetos rodoviários que atravessam também Rio Grande do Norte e Pernambuco (§2.4.1).

**2. Narração possivelmente sintética.** Canais de formato enumerativo — "as 15 piores cidades de Pernambuco" — citam o estado a cada título e são frequentemente narrados por voz artificial. O risco é de natureza distinta dos demais: introduziria **fala não humana** em corpus destinado a documentar variação humana. Nenhum áudio sintético entra no corpus, e a suspeita basta para excluir (§2.4.2).

**3. Canal sem fala.** Passeios em vídeo — rotulados `walk`, `4K`, `POV` — e montagens com drone percorrem bairros identificáveis e satisfazem plenamente o critério geográfico, sem que ninguém fale (§2.4.3).

**4. Falante migrante.** É a mais grave, e qualitativamente distinta das três anteriores. O canal está corretamente ancorado no estado — o autor mora ali, filma as ruas de lá, cita bairros identificáveis — e ainda assim veicula fala de outra variedade, porque o autor migrou. Dois casos apareceram nomeando-se a si mesmos: "Carioca em SP" e "Viviane Baiana", ambos aprovados pela triagem automática, com evidência geográfica correta (§2.5).

A gravidade é assimétrica e direcional: sendo o vetor migratório dominante no Brasil o Nordeste para o Sudeste, que é o eixo desta pesquisa, um falante nordestino radicado em São Paulo incorporado ao grupo de controle **atenua sistematicamente o contraste que a pesquisa mede**, deslocando o resultado na direção da hipótese nula. O erro produz aparência de ausência de viés.

**Tratamento das quatro.** As três primeiras são detectadas por incidência de sinal nos títulos recentes em `verificar_fontes.py`; quando a incidência atinge um terço dos títulos examinados, o veredito é rebaixado de aceito para **revisar**, e não para rejeitado — deliberadamente, porque o sinal também produz falso positivo, como no canal de Belford Roxo cujos títulos dizem "viajando de carro em Belford Roxo, indo trabalhar", que descreve deslocamento diário e é fonte legítima (§2.4.4). A quarta não tem sinal automático confiável, e sua defesa efetiva é a checagem de coerência dialetal na curadoria manual das transcrições, que opera sobre a fala e não sobre metadados — **e não está implementada** (`docs/pendencias.md` §6.2).

Nenhum canal entra em `fontes.json` sem revisão humana. A triagem automática é redutora de esforço e registro auditável da evidência, não decisão final (§2.4.4). A precisão medida da etapa automatizada é de cerca de 41%: 390 candidatos levantados, 114 aprovados automaticamente, 47 confirmados em revisão humana (§4).

### 1.4.4 Escopo de plataforma

| Plataforma | Decisão | Fundamento |
|---|---|---|
| YouTube | **Adotada** | Coleta sistemática funcional, conteúdo arquivístico estável, identificadores publicáveis |
| Podcast por feed aberto (RSS, Apple Podcasts) | **Adotada** | Publicado com a finalidade explícita de ser baixado; a fonte de situação jurídica mais clara disponível, superior nesse aspecto ao próprio YouTube |
| Spotify | **Excluída** | Áudio protegido e download vedado pelos termos de uso; não há extrator disponível |
| TikTok | **Excluída do corpus principal** | Ver abaixo |
| Instagram | **Excluída do corpus principal** | Mesmos motivos do TikTok, agravados pela exigência de autenticação e pelo extrator inoperante |

(`docs/fontes_coleta.md` §2.3)

**Fundamento da exclusão de TikTok e Instagram** (§2.3.1). O motivo determinante é a **dissociação entre origem do vídeo e origem da voz**: o reaproveitamento de áudio de terceiros é mecanismo central dessas plataformas, de modo que um vídeo publicado por perfil sediado no estado-alvo pode veicular áudio gravado por falante de outra região. Diferentemente da contaminação por consulta de busca, esta **não é detectável por inspeção do perfil ou do conteúdo visual**. Para um corpus cuja variável independente é a procedência da fala, o defeito é incontornável em escala.

Três fatores adicionais, onerosos mas não determinantes: alta incidência de encenação de sotaque com finalidade humorística, que é precisamente a caricatura que a validade de construto exige excluir; sobreposição de música à fala, que degrada transcrição e diarização; e duração típica de 15 a 60 segundos, que eleva o custo de curadoria por hora aproveitável.

**Reabertura condicionada.** Admite-se subcorpus secundário, declarado à parte, caso a diversidade de falantes não se complete pelas fontes adotadas, sob quatro critérios cumulativos: áudio original do próprio autor; ausência de música de fundo; procedência declarada pelo falante ou verificável no perfil; e ao menos 60 segundos de fala contínua. O subcorpus deve ser aplicado **simetricamente aos dois grupos regionais**, sob pena de a diferença observada refletir a plataforma e não a região (§2.3.1). Não reavaliado desde a decisão original (`docs/pendencias.md` D4).

**Canais de arquivo não oficiais estão excluídos.** Republicadores de material de emissoras — "Muito Além do JPB", "Muito Além do CETV" — têm conteúdo adequado, mas a redistribuição por terceiros agrava a exposição de direitos autorais. Havendo canal oficial da emissora, é ele que entra (§2.2).

### 1.4.5 Tetos de concentração

| Teto | Valor | Origem |
|---|---|---|
| Por falante, sobre a fala de um estado | 5% | `docs/fontes_coleta.md` §2.4.5 |
| Por canal, sobre a cota de uma camada | 35% | `selecionar_videos.py`, `TETO_POR_CANAL` |

> `PENDENTE:` o teto por falante não tem verificação implementada. Nada impede que a mesma pessoa apareça em canais distintos — um convidado que circula por vários podcasts regionais, por exemplo —, o que violaria o teto silenciosamente. A detecção exigiria comparação de vozes na etapa de diarização (`docs/pendencias.md` §6.4).

### 1.4.6 Regra de recorte temporal

Fixada em `pipeline_coleta_piloto/selecionar_videos.py`:

| Parâmetro | Valor | Efeito |
|---|---|---|
| `LIMITE_TRECHO_S` | 900 s | Vídeos mais longos que 15 minutos entram como recorte, não por inteiro |
| `TRECHO_S` | 600 s | Duração do recorte |
| `ABERTURA_S` | 120 s | Descarta o início, onde ficam vinheta e escalada |

O início do recorte é `max(ABERTURA_S, duracao_s × 0,05)` e o fim, `min(inicio + TRECHO_S, duracao_s)`. O par resultante é gravado no campo `trecho`.

### 1.4.7 Formato do áudio

WAV, 16 kHz, mono — padrão exigido por `faster-whisper` e `pyannote.audio` (`pipeline_coleta_piloto/config.py`, `YDL_OPTS`).

Parâmetros de processamento, fixados em `config.py` e justificados em `docs/stack_tecnica.md`: transcrição por `faster-whisper` com modelo `large-v3`, `language="pt"`, `beam_size=5`, `word_timestamps=True`, `vad_filter=True` com `min_silence_duration_ms=500`, `condition_on_previous_text=False` e `temperature=0.0` para decodificação determinística; diarização por `pyannote/speaker-diarization-community-1`.

## 1.5 Meta de volume, e de onde ela sai

**A meta não é arbitrada.** Deriva do requisito estatístico do Filtro 2: o volume de fala necessário para que a **ausência** de uma variante seja informativa, e não mera insuficiência amostral (`experimentos/meta_volume_corpus.py`, resultado em `experimentos/resultados/historico/meta_volume.md`).

**Suposições declaradas**, todas a recalibrar, exceto a última: 130 palavras por minuto, 9 palavras por oração, 5% de orações negadas, e produtividade da negação pós-verbal de 5,6% — este último o máximo observado por Santos e Vitório (2025). Disso resultam 43 contextos de negação por hora de fala do locutor-alvo, e 2,4 ocorrências esperadas da variante por hora.

| Critério de decisão do Filtro 2 | Horas de fala-alvo por estado |
|---|---|
| Detectar ao menos 1 ocorrência com 90% de confiança | 0,9 h |
| Detectar ao menos 1 ocorrência com 95% de confiança | 1,2 h |
| Detectar ao menos 1 ocorrência com 99% de confiança | 1,8 h |
| Esperar 5 ocorrências (estimativa de taxa) | 2,1 h |
| **Esperar 10 ocorrências (comparação entre estados) — critério recomendado** | **4,1 h** |

O critério recomendado é o último, pela seguinte razão: presença ou ausência basta para promover um marcador, mas a comparação entre Nordeste e grupo de controle exige **estimar a taxa em cada grupo**, e não apenas constatar ocorrência. Com esse volume, a probabilidade de zero ocorrências, se a variante tiver a produtividade suposta, é de 0,0033% — e a ausência passa a ser evidência, que é a condição para o Filtro 2 significar alguma coisa.

**Conversão para áudio bruto.** Fala do locutor-alvo é menos que áudio gravado: descontam-se vinheta, música, silêncio e turnos de locutores de outra variedade.

| Camada | Composição | Rendimento suposto | Fala-alvo por estado | Áudio bruto por estado |
|---|---|---|---|---|
| `entrevista_vox_pop` | 35% | 35% | 1,4 h | 4,1 h |
| `podcast_radio_tv_regional` | 30% | 60% | 1,2 h | 2,1 h |
| `vlog_amador` | 35% | 70% | 1,4 h | 2,1 h |
| **Total** | 100% | — | **4,1 h** | **8,3 h** |

**Meta vigente: 8,3 h de áudio bruto por estado, 50 h no conjunto dos seis**, equivalentes a 25 h de fala-alvo.

> **Substituída em 29/08/2026.** Com o corpus decidido como entregável autônomo (§1.1), a meta acima deixa de valer: ela derivava da função de validar marcadores. A meta vigente está em `experimentos/resultados/tabelas/meta_corpus_autonomo.md`, e muda de unidade — passa de horas de fala para **cobertura de falantes**. O teto de 5% por falante, já fixado, impõe por aritmética ao menos **20 falantes distintos por estado**; e a densidade de contextos de palatalização, **medida em 13,6 por minuto** (`densidade_palatalizacao.md`), mostra que um minuto de fala por pessoa basta para o marcador de áudio. O gargalo deixa de ser horas e passa a ser a verificação de que os falantes são pessoas distintas, hoje não implementada (`docs/pendencias.md`, seção 6.4).
>
> A conta antiga é conservada abaixo como histórico, e a revisão para 38 h que ela previa perde objeto.
>
> `HISTÓRICO:` existe uma revisão da meta que **não foi adotada**. O piloto mediu rendimentos por camada muito superiores aos supostos — 91,8% em vox-pop contra 35%, 87,3% em podcast contra 60%, 85,1% em vlog contra 70% —, o que reduziria a meta para cerca de 6,4 h por estado e 38 h no total. A revisão está registrada em estado **condicional**, e depende de uma verificação ainda não feita: a de que o locutor dominante da camada de vox-pop é o repórter, e não um entrevistado loquaz. Dessa suposição depende toda a estimativa de fala aproveitável (`docs/achados_para_o_artigo.md` §2.2 e §2.3). Enquanto não verificada, a meta vigente é 50 h.

**Amostra de verificação manual.** Independente do volume total, o cálculo de WER e DER exige transcrição manual de referência: 20 minutos por estado, estratificados entre as camadas, totalizando 2 h de transcrição manual (`experimentos/resultados/historico/meta_volume.md`). É o suficiente para estimar WER por variedade, que é ameaça à validade registrada na Parte 3 do `CLAUDE.md` e resultado publicável por si só.

## 1.6 Anonimização e publicação

Regras fixadas em `CLAUDE.md` §1.4.2:

- **Nomes próprios de terceiros** mencionados nas transcrições — não o autor do vídeo — são mascarados antes de qualquer publicação do conjunto.
- **O áudio bruto não é redistribuído.** Publicam-se os identificadores de vídeo e o código de coleta, o que preserva a reprodutibilidade sem violar direitos autorais ou os termos de uso da plataforma.
- **O nome do canal é mantido**, por tratar-se de conteúdo público publicado voluntariamente.
- **Não se coleta geolocalização precisa**; registra-se apenas o estado-alvo, já conhecido pela origem ou temática do canal.
- Não se coleta dado pessoal sensível: registra-se apenas o que já está publicamente disponível nos metadados do vídeo (`CLAUDE.md` §1.4.1).

A regra de publicar identificador em vez de áudio é o que torna o campo `trecho` parte do esquema publicado e não auxiliar: identificador de vídeo sem o recorte utilizado não permite reconstruir o material analisado (`collect.py`, `VideoMetadata`).

> `PENDENTE:` a licença sob a qual o conjunto — identificadores, código e transcrições anonimizadas — será distribuído não está definida em nenhum documento. O material registra apenas a obrigação de verificar termos de serviço e licença do conteúdo de origem antes de redistribuir (`docs/stack_tecnica.md` §2.1) e a licença CC-BY-4.0 do modelo de diarização empregado (§2.3). Nada declara a licença dos artefatos do próprio projeto.

> `PENDENTE:` não existe ficha de conjunto de dados (*datasheet*) para o corpus de áudio. Ver Parte 2, item 2.2.4, onde a mesma lacuna é registrada para os pares mínimos — inclusive quanto a usos desaconselhados, que aqui têm objeto próprio, já que um corpus de fala rotulado por procedência regional se presta a treinar classificador de origem de falantes.

## 1.7 Estado de execução

**Fontes.** 88 canais em `pipeline_coleta_piloto/fontes.json`, apurados: 77 com situação `verificado` e 11 com `a_confirmar`. Cada entrada traz `canal`, `channel_id`, `tipo_fonte`, `situacao` e `nota`.

| UF | vox-pop | podcast/rádio/TV | vlog | Total |
|---|---|---|---|---|
| PB | 2 | 3 | 7 | 12 |
| PE | 3 | 5 | 4 | 12 |
| CE | 4 | 4 | 8 | 16 |
| BA | 2 | 4 | 6 | 12 |
| SP | 2 | 4 | 13 | 19 |
| RJ | 2 | 2 | 13 | 17 |
| **Total** | **15** | **22** | **51** | **88** |

(`docs/fontes_coleta.md` §4; contagens conferidas contra `fontes.json`)

**Material coletado**, apurado sobre `metadados.json`: 52 trechos, 5,52 h de áudio efetivamente coletado, distribuídas em PB 1,15 h, RJ 1,01 h, BA 1,00 h, SP 0,85 h, CE 0,79 h, PE 0,73 h. A esteira está validada de ponta a ponta, dividida entre coleta local e processamento em GPU (`docs/roadmap.md`, passo 4.3).

O diretório `dataset_raw/registros_finais/` está **vazio**, e os diretórios `transcricoes/` e `diarizacao/` também. Os produtos de transcrição e diarização do lote executado encontram-se nos pacotes `piloto_resultados (1).zip` e `(2).zip`, na raiz do projeto, mantidos fora do versionamento por conterem transcrição não anonimizada. Não foram abertos na produção deste documento.

> `PENDENTE:` os 11 canais marcados `a_confirmar` exigem inspeção de conteúdo antes da coleta (`docs/fontes_coleta.md` §4).

> `PENDENTE:` a simetria de composição entre os grupos não está decidida. O grupo de controle dispõe de treze vozes por estado na camada de vlog, contra quatro a oito nos estados nordestinos, sendo Pernambuco o mais frágil. Para o experimento importa a simetria entre grupos, não o máximo disponível em cada um. Duas condutas admissíveis, e a escolha cabe à equipe: limitar todos os estados ao patamar do mais fraco, ou reforçar PE e BA antes de coletar (`docs/fontes_coleta.md` §4; `docs/pendencias.md` D1).

---

# Parte 2 — Pares mínimos (EM ABERTO)

Esta parte **não é uma especificação**. Registra o que existe, o que falta, e por que o que falta não pode ser preenchido agora.

## 2.1 Por que está em aberto

O conjunto de pares mínimos é, pelo princípio de ordenação do projeto, a contribuição publicável: a lacuna identificada na literatura é a inexistência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro, e os precedentes diretos são artigos de conjunto de dados (`docs/roadmap.md`, "Princípio de ordenação").

Ocorre que **o conteúdo perdeu sustentação empírica em 28/08/2026**. Quatro famílias de sinalização dialetal implícita foram testadas contra a mesma calibração, e nenhuma produz resposta acima do que a frequência lexical prevê (`docs/achados_para_o_artigo.md` §1.15):

| Família | Pares | Resíduo médio | p Holm |
|---|---|---|---|
| morfossintática — imperativo e negação | 5 | −0,0608 | 1,0000 |
| lexical — itens regionais | 5 | +0,0447 | 0,5064 |
| feixe combinado | 5 | −0,0063 | 1,0000 |
| construcional | 10 | −0,0141 | 1,0000 |

O nulo é legível, e não indício de aparelho quebrado: o controle de conteúdo proposicional produz resíduo de +0,3597 com p = 0,0003 após correção de Holm, e o confundidor de frequência está descontado por calibração explícita sobre 22 pares não regionais (`experimentos/resultados/relatorios/construcional.md`).

**Consequência para esta especificação.** Sem a decisão do passo 5 do roadmap — trocar de modelo ou de métrica (5.2), reposicionar como artigo de método e recurso (5.3), ou levar a menção explícita a volume (5.4) — não há critério para dizer o que o conjunto contém, e sem isso não há como fixar tamanho-alvo nem esquema de registro. Fixá-los agora seria arbitrar (`docs/pendencias.md`, D5 e D7).

## 2.2 As quatro definições ausentes

Reproduzidas de `docs/pendencias.md` D7. As quatro são exigidas em submissão a veículo que aceite artigo de recurso.

### 2.2.1 Tamanho-alvo — DECIDIDO em 29/08/2026

**Meta: 37 pares por condição de teste e 80 pares no grupo de referência não regional**, o que perfaz entre 228 e 265 pares conforme o conjunto tenha quatro ou cinco condições. Hoje há oito e vinte e seis, respectivamente.

Derivação reproduzível em `experimentos/meta_pares_minimos.py`, com relatório em `experimentos/resultados/tabelas/meta_pares_minimos.md`. O raciocínio, em resumo:

**A pergunta mudou de forma.** Não é "quantos pares para detectar o efeito", porque o passo 5.5 estabeleceu que não há efeito de valência a detectar — o único candidato dissolveu-se ao se controlar o artefato de tokenização. É **quantos pares para que a ausência de efeito seja informativa**, mesma lógica de que saiu a meta do corpus de áudio. Um nulo obtido sem poder não distingue "não há viés" de "não olhamos direito", e é essa distinção que a seção de Resultados precisa sustentar.

**O insumo é decisão, não medição: o menor efeito de viés que se queira poder excluir.** A equipe fixou **0,08 em unidade bruta de escore de viés**, cerca de 0,7 desvio-padrão do ruído entre pares. Três razões:

1. **É metade do artefato que o próprio projeto desmontou.** O falso viés de tokenização media 0,195 antes do controle (`docs/achados_para_o_artigo.md`, item 1.1). Poder excluir 0,08 autoriza a afirmação verificável de que, houvesse viés com metade daquela força, ele teria sido detectado — e não mera retórica de cautela.
2. **Guarda margem de quase três vezes para o controle positivo**, que produz 0,235. Uma alegação de poder vale o quanto for a distância entre o que se pretende excluir e o que o instrumento comprovadamente detecta.
3. **É alcançável.** Descer a 0,059 exigiria 108 pares por condição; subir a 0,095 pouparia catorze, ao custo de só poder excluir viés grande.

**Uma restrição que a conta revelou, e que não constava de plano anterior.** O grupo de referência impõe **teto** ao que é detectável, por mais pares de teste que se acrescentem, porque sua própria incerteza não desaparece. Com os 26 pares de referência atuais, nenhum efeito abaixo de 0,078 é detectável sob correção de multiplicidade. **O grupo de referência precisa crescer junto com as condições de teste** — daí a meta de 80, e não apenas a de 37 por condição.

**Restrição de conteúdo, que precede o tamanho.** Qualquer conjunto futuro deve balancear a extensão em subtokens entre os polos do eixo medido, sob pena de reproduzir o artefato de que a decisão acima toma a medida.

### 2.2.2 Formato de publicação — `PENDENTE`

Não há esquema de registro definido: nem campos, nem tipos, nem codificação, nem unidade de linha. O CrowS-Pairs distribui pares com identificador, os dois lados, tipo de viés e anotações de juízes; nada equivalente foi especificado neste projeto.

### 2.2.3 Licença — `PENDENTE`

Não decidida. A questão é distinta da do áudio, cuja conduta está fixada — publicar identificadores e código, não mídia. Os pares mínimos são texto de autoria do projeto e admitem licenciamento permissivo, mas a decisão não foi tomada nem registrada.

### 2.2.4 Ficha de conjunto de dados — RASCUNHADA em 29/08/2026

Existe em `docs/ficha_conjunto.md`, em estado **preliminar**, cobrindo os dois conjuntos em separado e no formato consolidado por Gebru et al. Seis lacunas ficam declaradas ao final dela, e duas dependem de consulta externa à equipe técnica.

Segue por escrever. É prática consolidada em publicação de recurso, e descreve motivação, composição, processo de coleta, usos pretendidos e **usos desaconselhados**. Este último item é particularmente pertinente: um conjunto de enunciados dialetais rotulados por região presta-se a uso indevido como classificador de procedência de falantes.

## 2.3 O que já está especificado, e é aproveitável: o protocolo de validação

O protocolo de validação **está fechado e não depende da decisão do passo 5**. Reproduz-se aqui na íntegra, por ser a parte do conjunto que sobrevive a qualquer dos rumos (`docs/pares_minimos_v1.md` §7).

**Dois filtros independentes e cumulativos. Um item integra o experimento apenas se aprovado em ambos.**

**Filtro 1 — juízes falantes nativos.** Mínimo de **cinco juízes por variedade** (CE, PB, PE, BA, SP, RJ). Os enunciados são apresentados **embaralhados, sem indicação da condição** a que pertencem. Cada juiz responde a três perguntas:

1. **Escolha forçada:** de qual estado é, mais provavelmente, quem falou isso? O item é aprovado se a maioria identificar a variedade-alvo.
2. **Naturalidade,** em escala de 1 a 5: uma pessoa dessa região diria isso naturalmente? Reprovado se a mediana for inferior a 4.
3. **Caricatura,** dicotômica: isso soa como imitação ou estereótipo? **Reprovação automática** se dois ou mais juízes responderem afirmativamente.

**Filtro 2 — ocorrência em corpus de fala espontânea.** Um marcador candidato só é promovido a confirmado se ocorrer em fala espontânea nas transcrições coletadas para o estado correspondente. Marcador ausente do corpus não integra o experimento. É a função que a Parte 1 deste documento atribui ao corpus de áudio.

**Calibração do Filtro 2 para variantes raras.** A negação pós-verbal tem produtividade da ordem de 5%. Antes de aplicar o filtro, deve-se estimar o volume de fala necessário para que a ausência de ocorrências seja informativa; do contrário, o filtro reprovaria o marcador por insuficiência amostral e não por inadequação. O mesmo cuidado vale para itens lexicais de baixa frequência. O cálculo correspondente está em 1.5 desta especificação.

**Estado de aplicação.** Nenhum item passou pelo Filtro 1 — nenhum juiz foi consultado (`docs/achados_para_o_artigo.md` §3.3). O passo 3 do roadmap está **suspenso**, e deliberadamente: convocar juízes exige um conjunto de itens que valha a pena validar, e validar itens que não medem nada gastaria a disponibilidade dos juízes sem contrapartida (`docs/roadmap.md`, passo 3).

## 2.4 Princípios de desenho já fixados

Também independem da decisão do passo 5, e devem ser preservados em qualquer reformulação (`docs/pares_minimos_v1.md` §2):

- **O guise é um feixe de marcadores, não um traço isolado.** Com marcador único, qualquer diferença medida é indistinguível do efeito daquele item específico — sua frequência no corpus de treinamento, sua polissemia ou sua segmentação em subtokens.
- **O feixe deve ser decomponível**, em blocos morfossintático, lexical e combinado, para permitir atribuir o efeito à sua origem.
- **Conteúdo proposicional e moldura sintática idênticos entre condições.** Variam apenas os traços sob teste.
- **A lacuna mascarada situa-se fora da região marcada**, e na mesma posição relativa em todas as condições.
- **Ambos os lados marcados**, sempre que houver equivalente: o contraste pretendido é entre variedade nordestina e variedade sudestina, não entre variedade regional e norma padrão, que mediria outra coisa. Sem equivalente sudestino, o enunciado de controle é anotado `[NEUTRO]` e analisado à parte.
- **Vedação a grafia caricata.** Transcrições do tipo *tchia*, *muié* ou *cumé que é* não integram o instrumento: representam fenômeno fonético em ortografia deformada, o que introduz simultaneamente raridade de segmentação e caricatura. Traço fonético valida-se em áudio, não em texto.

Acrescentem-se duas exigências metodológicas estabelecidas por medição própria em 28/08/2026, que qualquer versão futura do conjunto deve satisfazer:

- **A unidade de replicação é o par, não a medição.** As medições de um mesmo par compartilham o enunciado e não são independentes; tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza (`docs/achados_para_o_artigo.md` §1.16).
- **A comparação entre guises exige calibração explícita da resposta à frequência.** O ruído no nível do par é da ordem do efeito procurado — desvio-padrão de 0,0618 contra mediana de 0,1360 —, de modo que o pareamento de frequência, sozinho, não basta (`docs/achados_para_o_artigo.md` §1.14, revisão).

## 2.5 Conteúdo existente

Doze itens rascunhados em três blocos — A morfossintático puro (4 itens), B lexical puro (4 itens), C feixe completo por estado (4 itens) —, dos quais um está suspenso por pendência bibliográfica não resolvida quanto à direção do marcador do imperativo em Fortaleza (`docs/pares_minimos_v1.md` §5 e §3.2). Nenhum validado.

Acrescentam-se dez marcadores construcionais formulados em 28/08/2026 (`experimentos/teste_construcional.py`, `CONSTRUCIONAIS`), que **não são itens de instrumento**: foram formulados para testar a existência de sinal, e três deles têm respaldo dialetológico cuja conferência em fonte primária permanece pendente, enquanto os demais são candidatos derivados do corpus próprio ou sem fonte alguma (`docs/pendencias.md` D6).

Registre-se uma ressalva de construto identificada na formulação: *tu* com verbo não flexionado ocorre também no Rio de Janeiro, que integra o grupo de controle, e o item não serve para separar os grupos deste desenho, ainda que a construção seja legítima (`docs/pendencias.md` D6).

**Pernambuco continua sem marcador morfossintático próprio.** Recife apresenta uso simétrico do imperativo, sem predominância, de modo que o marcador não distingue o estado do grupo de controle. É o único dos quatro estados-alvo nessa situação, e a coincidência é incômoda porque Pernambuco é também o estado mais frágil na camada de vlog do corpus de áudio (`docs/pares_minimos_v1.md` §6; `docs/fontes_coleta.md` §4).

---

## Registro de pendentes

Consolidação dos pontos marcados `PENDENTE` acima, para leitura em bloco.

| # | Pendente | Parte | Onde se resolve |
|---|---|---|---|
| 1 | ~~Semântica de `duracao_s`~~ — **encerrado em 29/08/2026** pelo campo `duracao_coletada_s` (§1.3) | 1.3 | — |
| 2 | Qual registro constitui o artefato publicado — o de coleta, o final, ou ambos | 1.2 | Decisão da equipe |
| 3 | ~~Função do corpus~~ — **decidido em 29/08/2026**: entregável autônomo (§1.1) | 1.1 | — |
| 4 | Composição entre camadas sob revisão não decidida | 1.4.2 | `docs/pendencias.md` D2 |
| 5 | Teto de 5% por falante sem verificação implementada | 1.4.5 | `docs/pendencias.md` §6.4 |
| 6 | Checagem de coerência dialetal contra falante migrante não implementada | 1.4.3 | `docs/pendencias.md` §6.2 |
| 7 | Meta de volume do corpus — **recalculada em 29/08/2026** sob o novo critério (§1.5); o que resta é a verificação de falantes distintos | 1.5 | `docs/pendencias.md` §6.4 |
| 8 | Licença dos artefatos do projeto não definida, para nenhum dos dois conjuntos | 1.6, 2.2.3 | Decisão da equipe |
| 9 | Ficha de conjunto de dados — **rascunhada em 29/08/2026** em `docs/ficha_conjunto.md`, preliminar, com seis lacunas declaradas | 1.6, 2.2.4 | Revisão da equipe |
| 10 | Onze canais marcados `a_confirmar` | 1.7 | Inspeção de conteúdo |
| 11 | Simetria de composição entre grupos não decidida | 1.7 | `docs/pendencias.md` D1 |
| 12 | Subcorpus de TikTok não reavaliado desde a exclusão | 1.4.4 | `docs/pendencias.md` D4 |
| 13 | ~~Tamanho-alvo dos pares mínimos~~ — **decidido em 29/08/2026**: 37 por condição e 80 de referência, para excluir efeitos acima de 0,08 (§2.2.1) | 2.2.1 | — |
| 14 | Formato de publicação dos pares mínimos inexistente | 2.2.2 | Decisão da equipe; deixa de depender do passo 5 |

### Nota de 29/08/2026 — o tamanho-alvo passa a ser derivável

O item 13 registrava que, ao contrário do corpus de áudio, o conjunto de pares mínimos não tinha meta **nem critério que a produzisse**. Duas coisas mudaram com o passo 5.4:

**Sabe-se o que o conjunto contém.** A menção explícita à região produz resposta acima da reta da frequência, concentrada em rótulos de pessoa, e sobrevive à correção de multiplicidade (`docs/achados_para_o_artigo.md` §1.17). A sinalização implícita, em quatro famílias, não produz. O conteúdo do conjunto deixa de ser indeterminado.

**Existe um critério estatístico disponível, e é o mesmo do corpus de áudio.** A meta do corpus foi derivada do volume necessário para que a ausência de uma variante rara fosse informativa (§1.5). O análogo aqui é o número de pares necessário para que a **análise de direção** — se a resposta é depreciativa, e não apenas diferente — atinja poder suficiente. O passo 5.5 do roadmap produzirá a estimativa de tamanho de efeito que essa conta exige.

Enquanto essa estimativa não existir, o tamanho-alvo continua sem número. O que mudou é que deixou de faltar o critério, e passou a faltar apenas o insumo dele.

**Complemento de 29/08/2026, depois do passo 5.5.** A estimativa foi produzida, e é negativa: nenhum viés de valência sobrevive ao controle do artefato de tokenização (`docs/achados_para_o_artigo.md` §1.19). Não há, portanto, tamanho de efeito para o qual dimensionar.

O critério não desaparece por isso — muda de forma. Deixa de ser "quantos pares para detectar o efeito observado" e passa a ser **"quantos pares para que a ausência de efeito seja informativa"**, que é exatamente a mesma lógica de que saiu a meta do corpus de áudio: o volume em que zero ocorrências deixa de significar amostra pequena. O insumo passa a ser o menor efeito que se queira poder excluir, e essa é decisão da equipe, não medição.

Registre-se ainda uma restrição de conteúdo que o passo 5.5 impôs e que precede o tamanho: qualquer conjunto futuro deve **balancear a extensão em subtokens entre os polos do eixo medido**, sob pena de reproduzir o artefato que produziu um viés aparente a p = 0,049 e o desfez ao ser controlado. Para o eixo de prestígio ocupacional, o balanceamento é impossível neste modelo, e a medição exige AUL (§1.20 daquele documento).
