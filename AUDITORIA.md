# Auditoria de organização e documentação

**Executada em:** 29/08/2026, por leitura do repositório. **Nenhum arquivo foi movido, renomeado, editado ou apagado**, nenhuma dependência foi instalada e nada foi enviado para fora da máquina.

**Escala.** 641 MB no disco, dos quais **2,1 MB versionados** em 61 arquivos. A diferença é a pasta de áudio, corretamente ignorada pelo git.

---

# 1. Estado atual

```
vies-nordeste-bertimbau/
├── .gitignore                     ignora dataset_raw/, CLAUDE.md, zips e caches
├── CLAUDE.md                      protocolo metodológico — FORA do versionamento
├── piloto_resultados (2).zip      52 registros processados, com transcrição não anonimizada
│
├── docs/                          11 arquivos — a camada mais madura do projeto
│   └── *.md, referencias.bib      documentação de pesquisa, toda versionada
│
├── experimentos/                  12 scripts + 21 saídas, tudo no mesmo nível
│   ├── *.py                       medição e derivação de metas, sem ordem legível no nome
│   └── resultados/                relatórios .md e dados .json misturados
│       └── tabelas/               saída de máquina, separada em 29/08/2026

    ATUALIZAÇÃO DE 29/08/2026: as etapas A e B desta proposta foram executadas.
    A raiz ganhou README.md, pyproject.toml e requirements-lock.txt, e
    experimentos/resultados/ foi dividida em relatorios/, tabelas/, dados/ e
    historico/. A árvore acima descreve o estado ANTES dessas mudanças, e é
    conservada como registro do diagnóstico. As etapas C a F seguem pendentes.
│
├── notebooks/
│   ├── README.md                  instruções de execução no Colab
│   └── piloto_colab.ipynb         transcrição e diarização em GPU
│
└── pipeline_coleta_piloto/        código de coleta + 636 MB de dados no mesmo lugar
    ├── *.py                       9 módulos, sem ordem legível no nome
    ├── fontes.json                88 canais verificados — INSUMO, versionado
    ├── plano_*.json               3 planos de coleta — INTERMEDIÁRIO, versionados
    ├── requirements.txt           4 dependências, só as do pipeline
    └── dataset_raw/               636 MB, ignorado pelo git
        ├── audio/                 104 arquivos (52 .wav + 52 .info.json)
        ├── metadados.json         52 registros de coleta
        ├── archive.txt            controle de redownload do yt-dlp
        ├── transcricoes/          VAZIA
        ├── diarizacao/            VAZIA
        └── registros_finais/      VAZIA — o conteúdo está no zip da raiz
```

**Três observações de estrutura, antes do detalhamento:**

1. **Não há README na raiz.** Os dois READMEs existentes estão dentro de subpastas e descrevem etapas, não o projeto.
2. **Código e dados compartilham diretório** em `pipeline_coleta_piloto/`, e o diretório de dados pesa 300 vezes mais que o repositório versionado.
3. **As três pastas de saída do pipeline estão vazias** porque o processamento roda no Colab e os resultados voltam no zip da raiz — arranjo funcional, mas não legível pela árvore.

---

# 2. O que cada arquivo faz

Uma linha por arquivo: o que faz, o que recebe, o que devolve.

## Raiz

| Arquivo | Função |
|---|---|
| `.gitignore` | Exclui do versionamento `dataset_raw/`, `CLAUDE.md`, os zips de resultado e caches do Python. |
| `CLAUDE.md` | Protocolo metodológico, esquema de dados e ameaças à validade; carregado por sessão de assistente. Recebe nada, devolve nada — é documento. **Não versionado.** |
| `piloto_resultados (2).zip` | 52 registros finais em JSON, com transcrição alinhada por palavra e diarização. Produto do notebook. **Não versionado**, por conter transcrição não anonimizada. |

## `docs/` — documentação de pesquisa

| Arquivo | Função |
|---|---|
| `roadmap.md` | Plano canônico de numeração estável, mais a situação de cada seção do artigo. |
| `achados_para_o_artigo.md` | Filtro editorial: o que pode, o que não pode e o que ainda não pode ser escrito, com a condição que libera cada item. |
| `pendencias.md` | Registro do que está aberto — lacunas, decisões da equipe (D1–D9), verificações devidas e melhorias. |
| `dataset-spec.md` | Especificação dos dois conjuntos: esquema de campos, critérios de inclusão, metas e registro de 14 pendentes. |
| `ficha_conjunto.md` | Ficha no formato *datasheet*, com a seção de usos desaconselhados. Preliminar. |
| `questoes_para_orientacao.md` | Dezoito perguntas fechadas que o projeto não pode decidir sozinho. |
| `pares_minimos_v1.md` | Instrumento de texto: marcadores, molduras, itens e protocolo de validação em dois filtros. |
| `fontes_coleta.md` | Regra de atribuição por canal, armadilhas de seleção e a lista de 88 canais por estado. |
| `fundamentacao_teorica.md` | Revisão de literatura e justificativa metodológica. |
| `stack_tecnica.md` | Parâmetros de `yt-dlp`, `faster-whisper` e `pyannote`, com a justificativa de cada um. |
| `referencias.bib` | Referências em BibTeX, com anotação de procedência e estado de verificação. |

## `pipeline_coleta_piloto/` — coleta de áudio

Ordem real de execução: **`verificar_fontes` → `selecionar_videos` → `coletar_local` → notebook do Colab**.

| Arquivo | Função |
|---|---|
| `config.py` | Centraliza caminhos, vocabulário controlado de estados e camadas, e parâmetros das três ferramentas. Recebe nada; expõe constantes. |
| `verificar_fontes.py` | Triagem automatizada de canais candidatos contra a regra de atribuição. Recebe consultas e um gazeteiro; devolve veredito por canal, com evidência. |
| `selecionar_videos.py` | Converte a lista de canais em plano de coleta, aplicando cota por camada, teto por canal e recorte temporal. Recebe `fontes.json`; devolve `plano_*.json`. |
| `collect.py` | Triagem de metadados e download de áudio via `yt-dlp`, com verificação de que o arquivo existe em disco. Recebe URL, estado e camada; devolve `VideoMetadata` e o `.wav`. |
| `coletar_local.py` | Executa a coleta na máquina local e mescla os metadados com os lotes anteriores. Recebe um `plano_*.json`; devolve áudio em `dataset_raw/audio/` e `metadados.json`. |
| `transcribe.py` | Transcrição com marcação temporal por palavra via `faster-whisper`. Recebe caminho de `.wav`; devolve dicionário de segmentos e palavras. |
| `diarize.py` | Diarização por `pyannote.audio` e atribuição de locutor a cada palavra. Recebe `.wav` e transcrição; devolve turnos e palavras rotuladas. |
| `pipeline.py` | Orquestrador que encadeia coleta, transcrição e diarização num registro final. Recebe lista de vídeos; devolve um JSON por vídeo. **Não é o caminho em uso** — a esteira está dividida entre local e Colab. |
| `fontes.json` | Insumo: 88 canais com identificador, camada, situação e nota de verificação. |
| `plano_piloto.json`, `plano_fatia.json`, `plano_resto.json` | Intermediários gerados por `selecionar_videos.py`, com 51, 18 e 33 vídeos planejados. |
| `requirements.txt` | Quatro dependências do pipeline. **Não cobre as de `experimentos/`.** |
| `README.md` | Descreve a esteira de coleta e a divisão entre ambiente local e GPU. |

## `experimentos/` — medição no modelo

Ordem real de execução: **`smoke_test_bertimbau` → `analise_sensibilidade` → `selecionar_atributos` → `teste_sensibilidade` → `teste_construcional` → `teste_explicito` → `analise_valencia`**. Os três `meta_*` são derivações independentes.

| Arquivo | Função |
|---|---|
| `metricas.py` | Implementa PLL, AUL e AULA, com mascaramento do alvo por inteiro. Recebe texto e alvo; devolve os escores por token. É a base de todo o resto. |
| `smoke_test_bertimbau.py` | Verifica a viabilidade do instrumento antes de qualquer medição de viés. Devolve `smoke_test.json` e uma tabela. |
| `analise_sensibilidade.py` | Mede divergência de Jensen-Shannon entre condições sobre a distribuição inteira da lacuna. Devolve `sensibilidade.json` e tabela. **Leitura superada** pelos testes calibrados posteriores. |
| `selecionar_atributos.py` | Constrói o conjunto de atributos a partir do vocabulário do modelo, e não da intuição. Devolve `atributos_selecionados.json` e `.md`. |
| `teste_sensibilidade.py` | Passo 5 — testa se o modelo responde a guise dialetal, com controles de piso e teto. Define molduras, atributos e sete condições; devolve `sensibilidade_bruto.json`. |
| `teste_construcional.py` | Passo 5.1 — marcadores construcionais e calibração da lei de frequência. Devolve `construcional_bruto.json`, `construcional_pares.json` e tabela. |
| `teste_explicito.py` | Passo 5.4 — menção explícita à região por granularidade do rótulo. Devolve `explicito_bruto.json`, `explicito_pares.json` e tabela. |
| `analise_valencia.py` | Passo 5.5 — mede a **direção** do efeito, e não sua magnitude, em dois eixos. Recebe as medições existentes; devolve tabela de viés por condição. |
| `densidade_palatalizacao.py` | Conta contextos de palatalização por minuto de fala, lendo o zip em memória. Devolve apenas contagens agregadas. |
| `meta_volume_corpus.py` | Deriva a meta antiga do corpus a partir do requisito do Filtro 2. **Superado** pela mudança de função do corpus. |
| `meta_corpus_autonomo.py` | Deriva a meta vigente do corpus, em cobertura de falantes. Recebe `fontes.json`; devolve tabela por estado. |
| `meta_pares_minimos.py` | Deriva o tamanho-alvo do conjunto de pares a partir do efeito mínimo a excluir. Devolve tabela de custo por poder. |

### `experimentos/resultados/`

| Arquivo | Função |
|---|---|
| `piloto_medicoes.md` | Medições do piloto de coleta: rendimento por camada, diarização, primeira aplicação do Filtro 2. |
| `sensibilidade_guise.md` | Relatório do passo 5, interpretado à mão. |
| `construcional.md` | Relatório do passo 5.1, interpretado à mão. |
| `explicito.md` | Relatório dos passos 5.4 e 5.5, interpretado à mão. É o resultado central. |
| `atributos_selecionados.md` | Conjunto de atributos derivado do vocabulário, com a assimetria de tokenização documentada. |
| `molduras_alternativas.md` | Teste das molduras substitutas para as duas que degeneraram. |
| `meta_volume.md` | Meta antiga do corpus. **Histórica.** |
| `meta_corpus_autonomo.md` | Meta vigente do corpus. |
| `meta_pares_minimos.md` | Meta do conjunto de pares. |
| `densidade_palatalizacao.md` | Densidade de contextos fonéticos por minuto, por camada e por estado. |
| `*_bruto.json`, `*_pares.json` | Medições brutas e agregadas por par — **dados**, não relatórios. 1,0 MB somados. |
| `sensibilidade.json`, `smoke_test.json` | Dados cujos relatórios `.md` foram apagados em 29/08/2026 por estarem superados. **Órfãos.** |
| `tabelas/*.md` | Saída de máquina regerável, separada dos relatórios em 29/08/2026. |

## `notebooks/`

| Arquivo | Função |
|---|---|
| `piloto_colab.ipynb` | Transcrição e diarização em GPU, lendo o áudio do Google Drive. Devolve os registros finais que voltam no zip. |
| `README.md` | Instruções de execução, incluindo o bloqueio de download por IP de datacenter que motivou a divisão da esteira. |

**Nenhum arquivo ficou não identificado.**

---

# 3. Problemas encontrados

Em ordem de consequência para reprodutibilidade.

## 3.1 Não há README na raiz — **crítico**

Quem abre o repositório não encontra o que o projeto é, como instalar, como executar, nem em que ordem. Os dois READMEs existentes estão dentro de subpastas e pressupõem contexto. Para uma submissão que declare reprodutibilidade, é a primeira ausência que um revisor nota.

## 3.2 O ambiente não está fixado — **crítico**

`requirements.txt` cobre apenas o pipeline de coleta, com quatro pacotes em piso mínimo (`>=`). As dependências de `experimentos/` — `torch`, `transformers`, `wordfreq` — **não estão declaradas em lugar nenhum**. Não há versão de Python fixada, nem arquivo de ambiente, nem versões travadas. Duas execuções em máquinas diferentes podem divergir sem aviso, e `wordfreq` é fonte de números que vão ao artigo.

## 3.3 O protocolo metodológico está fora do versionamento — **crítico**

`CLAUDE.md` contém o esquema de dados, o protocolo de coleta e as ameaças à validade, e é citado por praticamente todos os documentos e por vários módulos de código. Quem clonar o repositório encontra dezenas de referências a um arquivo ausente. Registrado como decisão pendente D3.

## 3.4 A ordem de execução não é legível — **alto**

Doze scripts em `experimentos/` e nove em `pipeline_coleta_piloto/`, todos no mesmo nível e nomeados por assunto. A ordem correta existe e é rígida — há uma cadeia de importação em que `teste_explicito` importa `teste_construcional`, que importa `teste_sensibilidade`, que importa `metricas` —, mas só é descobrível lendo os arquivos.

## 3.5 Dados e código no mesmo diretório — **alto**

`pipeline_coleta_piloto/` contém 636 MB de áudio ao lado dos módulos. O `.gitignore` resolve o versionamento, não a legibilidade: a pasta de código é indistinguível da pasta de dados.

Em `experimentos/resultados/`, dados (`*.json`, 1,0 MB) e relatórios interpretados (`*.md`) convivem no mesmo nível, ainda que a saída de máquina já tenha sido separada em `tabelas/`.

## 3.6 Definições de dados vivem dentro do código de medição — **alto**

As condições experimentais — enunciados, molduras, atributos, classificação de valência — estão declaradas como constantes dentro dos scripts, e são importadas de um script para outro. Isso torna o conjunto de estímulos inseparável do código que o mede, e o próprio `docs/dataset-spec.md` registra que o formato de publicação dos pares mínimos ainda não existe. **Publicar o dataset exigirá extraí-las.**

## 3.7 Dois artefatos de dados órfãos — **médio**

`sensibilidade.json` e `smoke_test.json` permanecem versionados, mas os relatórios que os interpretavam foram apagados em 29/08/2026 por estarem superados. São regeráveis pelos scripts que os escrevem.

## 3.8 Três pastas de saída permanentemente vazias — **médio**

`transcricoes/`, `diarizacao/` e `registros_finais/` são criadas por `config.py` e nunca preenchidas, porque o processamento migrou para o Colab. Sugerem uma esteira que não é a que se executa.

## 3.9 Artefatos intermediários versionados junto com insumos — **baixo**

`fontes.json` é insumo curado e deve ser versionado. `plano_piloto.json`, `plano_fatia.json` e `plano_resto.json` são saída de `selecionar_videos.py` e estão versionados no mesmo nível, sem distinção.

## 3.10 Um orquestrador que não é o caminho em uso — **baixo**

`pipeline.py` encadeia coleta, transcrição e diarização em processo único. A esteira real está dividida entre `coletar_local.py` e o notebook. O módulo não está marcado como alternativo.

## 3.11 Não há testes automatizados — **declarado, não priorizado**

Nenhum teste unitário ou de regressão. Dado o histórico de oito falhas silenciosas catalogadas em `docs/pendencias.md`, seção 5-A, é ausência relevante — mas corrigi-la é projeto próprio, e não parte de uma reorganização.

---

# 4. Reestruturação proposta

## 4.1 Árvore alvo

```
vies-nordeste-bertimbau/
├── README.md                      NOVO — o que é, como instalar, como executar, em que ordem
├── CITATION.cff                   NOVO — como citar o trabalho e o dataset
├── pyproject.toml                 NOVO — dependências e versão de Python, num só lugar
├── requirements-lock.txt          NOVO — versões exatas, geradas do ambiente que produziu os resultados
├── .gitignore
│
├── docs/                          INALTERADO — a camada já madura
│   ├── protocolo.md               NOVO — partes públicas do CLAUDE.md (decisão D3)
│   └── (os 11 arquivos atuais)
│
├── dados/                         NOVO — tudo que é dado, separado de todo código
│   ├── fontes/fontes.json         insumo curado
│   ├── planos/plano_*.json        intermediários de planejamento
│   ├── estimulos/                 NOVO — condições extraídas do código (ver 4.3)
│   └── bruto/                     dataset_raw/ atual, ignorado pelo git
│
├── src/                           NOVO — todo o código importável
│   ├── coleta/                    módulos do pipeline_coleta_piloto/
│   └── medicao/                   metricas.py e utilidades compartilhadas
│
├── scripts/                       NOVO — pontos de entrada, numerados na ordem de execução
│   ├── 10_verificar_fontes.py
│   ├── 11_selecionar_videos.py
│   ├── 12_coletar_local.py
│   ├── 20_smoke_test.py
│   ├── 21_selecionar_atributos.py
│   ├── 30_teste_sensibilidade.py
│   ├── 31_teste_construcional.py
│   ├── 32_teste_explicito.py
│   ├── 33_analise_valencia.py
│   ├── 40_meta_corpus.py
│   ├── 41_meta_pares.py
│   └── 42_densidade_palatalizacao.py
│
├── notebooks/                     INALTERADO
│
└── resultados/
    ├── relatorios/*.md            interpretados à mão, nunca sobrescritos
    ├── tabelas/*.md               saída de máquina, regerável
    ├── dados/*.json               medições brutas e agregadas
    └── historico/                 medições superadas, conservadas com data
```

## 4.2 Movimentações, origem → destino

**Código do pipeline**

| Origem | Destino |
|---|---|
| `pipeline_coleta_piloto/config.py` | `src/coleta/config.py` |
| `pipeline_coleta_piloto/collect.py` | `src/coleta/collect.py` |
| `pipeline_coleta_piloto/transcribe.py` | `src/coleta/transcribe.py` |
| `pipeline_coleta_piloto/diarize.py` | `src/coleta/diarize.py` |
| `pipeline_coleta_piloto/pipeline.py` | `src/coleta/pipeline.py` (com nota de que não é o caminho em uso) |
| `pipeline_coleta_piloto/verificar_fontes.py` | `scripts/10_verificar_fontes.py` |
| `pipeline_coleta_piloto/selecionar_videos.py` | `scripts/11_selecionar_videos.py` |
| `pipeline_coleta_piloto/coletar_local.py` | `scripts/12_coletar_local.py` |

**Código de medição**

| Origem | Destino |
|---|---|
| `experimentos/metricas.py` | `src/medicao/metricas.py` |
| `experimentos/smoke_test_bertimbau.py` | `scripts/20_smoke_test.py` |
| `experimentos/selecionar_atributos.py` | `scripts/21_selecionar_atributos.py` |
| `experimentos/teste_sensibilidade.py` | `scripts/30_teste_sensibilidade.py` |
| `experimentos/teste_construcional.py` | `scripts/31_teste_construcional.py` |
| `experimentos/teste_explicito.py` | `scripts/32_teste_explicito.py` |
| `experimentos/analise_valencia.py` | `scripts/33_analise_valencia.py` |
| `experimentos/meta_corpus_autonomo.py` | `scripts/40_meta_corpus.py` |
| `experimentos/meta_pares_minimos.py` | `scripts/41_meta_pares.py` |
| `experimentos/densidade_palatalizacao.py` | `scripts/42_densidade_palatalizacao.py` |
| `experimentos/analise_sensibilidade.py` | `scripts/historico/analise_sensibilidade.py` |
| `experimentos/meta_volume_corpus.py` | `scripts/historico/meta_volume_corpus.py` |

**Dados**

| Origem | Destino |
|---|---|
| `pipeline_coleta_piloto/fontes.json` | `dados/fontes/fontes.json` |
| `pipeline_coleta_piloto/plano_*.json` | `dados/planos/` |
| `pipeline_coleta_piloto/dataset_raw/` | `dados/bruto/` |
| `experimentos/resultados/*_bruto.json`, `*_pares.json` | `resultados/dados/` |
| `experimentos/resultados/atributos_selecionados.json` | `resultados/dados/` |
| `experimentos/resultados/sensibilidade.json`, `smoke_test.json` | `resultados/historico/` |

**Relatórios**

| Origem | Destino |
|---|---|
| `experimentos/resultados/*.md` (interpretados) | `resultados/relatorios/` |
| `experimentos/resultados/tabelas/*.md` | `resultados/tabelas/` |
| `experimentos/resultados/historico/meta_volume.md` | `resultados/historico/` |

**Novos, a escrever**

| Arquivo | Conteúdo |
|---|---|
| `README.md` | Objeto do projeto, instalação, ordem de execução, mapa das pastas, estado atual, como citar |
| `pyproject.toml` | Dependências das duas frentes num só lugar, com versão de Python |
| `requirements-lock.txt` | Versões exatas do ambiente que produziu os resultados publicados |
| `CITATION.cff` | Metadados de citação do trabalho e do dataset |
| `docs/protocolo.md` | Partes públicas do `CLAUDE.md`, resolvendo a decisão D3 |

## 4.3 Três consequências que exigem trabalho além de mover arquivos

**As importações quebram.** Nove módulos importam por nome simples — `from config import ...`, `from metricas import ...` —, o que só funciona porque estão lado a lado. Mover para `src/` exige converter em pacote e ajustar cada importação. É mecânico, mas não é `git mv`.

**Os caminhos de dados quebram.** `config.py` ancora `dataset_raw/` no diretório do módulo. Mover o código sem mover o dado, ou o inverso, quebra a âncora — que é precisamente o defeito já catalogado, quando uma execução criou uma segunda pasta de dados vazia.

**A extração dos estímulos é reestruturação de conteúdo, não de arquivos.** O item 3.6 propõe tirar as condições experimentais de dentro dos scripts e pô-las em `dados/estimulos/`. Isso muda o modo como os scripts são escritos e **deve ser tratado como etapa separada**, depois da mudança de pastas, e alinhada com a decisão de formato de publicação dos pares mínimos, ainda pendente.

## 4.4 Ordem sugerida, e o que fazer em cada etapa

| Etapa | O que | Risco |
|---|---|---|
| **A** | ~~Escrever `README.md`, `pyproject.toml` e `requirements-lock.txt`~~ — **executada em 29/08/2026** | Nenhum — só acrescenta |
| **B** | ~~Reorganizar `resultados/`~~ — **executada em 29/08/2026**; foram dez scripts e não cinco, e a varredura de referências alcançou treze arquivos | Baixo — ajustar caminhos de saída |
| **C** | Criar `src/` e `scripts/`, com `git mv` e conversão em pacote | Médio — reescrever importações; rodar tudo depois |
| **D** | Mover os dados para `dados/` e reancorar `config.py` | Médio — verificar que a coleta ainda encontra o áudio |
| **E** | Resolver D3 escrevendo `docs/protocolo.md` | Baixo — decisão pendente da equipe |
| **F** | Extrair os estímulos para `dados/estimulos/` | Alto — depende de decisão de formato ainda em aberto |

**Recomendação:** executar A e B agora, que resolvem os dois problemas críticos de documentação e o de mistura em `resultados/` sem tocar em importação nem em caminho de dados. C e D exigem uma janela em que se possa reexecutar tudo para conferir. E depende de decisão sua. **F não deve ser feita antes de a pendência de formato ser fechada.**

---

# Resumo

Auditei 61 arquivos versionados e 641 MB no disco, sem alterar nada. Todos foram identificados; nenhum ficou sem função determinada.

A documentação de pesquisa é a camada mais madura do projeto e não precisa de reorganização. O que falta é a camada de engenharia: **não há README na raiz, o ambiente não está fixado — `torch`, `transformers` e `wordfreq` não constam de nenhum arquivo de dependências — e o protocolo metodológico está fora do versionamento**, sendo citado por quase todo o resto.

Somam-se três problemas de legibilidade: a ordem de execução dos vinte e um scripts só é descobrível lendo o código, dados e código dividem diretório, e as condições experimentais vivem dentro dos scripts de medição, o que impedirá publicar o conjunto de pares sem extraí-las.

Proponho seis etapas, das quais **as duas primeiras são seguras e resolvem os problemas críticos**; as duas seguintes exigem reescrever importações e reancorar caminhos; a quinta depende de decisão sua; e a sexta não deve ser tentada antes de a pendência de formato ser fechada.
