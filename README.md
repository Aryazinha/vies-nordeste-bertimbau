# Vieses sociolinguísticos no BERTimbau: variedades do Nordeste

Investigação de viés regional no BERTimbau, contrastando variedades de Paraíba, Pernambuco, Ceará e Bahia com um grupo de controle de São Paulo e Rio de Janeiro. O projeto produz **dois conjuntos de dados** e uma série de medições no modelo.

Trabalho de pesquisa acadêmica, em andamento. Este arquivo descreve o repositório; o estado científico está em [`docs/roadmap.md`](docs/roadmap.md).

---

## O que já se estabeleceu

Três resultados que se sustentam mutuamente e **não devem ser citados em separado**:

1. **O modelo não responde à sinalização dialetal implícita.** Quatro famílias de marcadores foram testadas — morfossintática, lexical, feixe combinado e construcional — e nenhuma produz efeito acima do que a frequência lexical prevê. O caso mais limpo é a negação pós-verbal, cujos dois lados empregam as mesmas palavras em ordem diferente.
2. **O modelo responde à menção explícita da região**, acima da reta da frequência, com duas condições sobreviventes à correção de Holm. O efeito concentra-se em **rótulos de pessoa** (*nordestino*, *baiano*) e não de lugar (*Recife*, *Ceará*).
3. **Essa resposta não é depreciativa de forma detectável.** O único viés candidato revelou-se **artefato de tokenização**: caiu de +0,195 para +0,031 ao se restringir a análise a atributos de token único — e a restrição *aumentou* o poder do teste em vez de reduzi-lo.

> **Advertência.** Não afirmar que o BERTimbau não apresenta viés regional. Não detectar não é demonstrar ausência, e o eixo de prestígio ocupacional segue sem medição válida. O filtro do que pode e do que não pode ser escrito está em [`docs/achados_para_o_artigo.md`](docs/achados_para_o_artigo.md), e deve ser consultado antes de qualquer trecho do artigo.

---

## Instalação

Requer **Python 3.12**.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[coleta,medicao]"
```

Para reproduzir exatamente os resultados publicados, use as versões travadas:

```bash
pip install -r requirements-lock.txt
```

**Duas frentes com dependências distintas.** A coleta de áudio precisa de `yt-dlp`, `faster-whisper` e `pyannote.audio`; a medição no modelo precisa de `torch`, `transformers` e `wordfreq`. Instale apenas o extra de que precisar — `pip install -e ".[medicao]"` basta para reexecutar todas as medições, que rodam em CPU.

**Dois requisitos externos ao Python:**

- **`ffmpeg`** no caminho do sistema, para a conversão de áudio.
- **Um runtime de JavaScript** — `deno`, `node` ou `bun` —, sem o qual o download do YouTube devolve HTTP 403. A extração de metadados continua funcionando sem ele, o que mascara a falha.
- **Token do Hugging Face** na variável de ambiente `HF_TOKEN`, para a diarização. Nunca fixado em código.

---

## Ordem de execução

Os scripts têm dependência rígida entre si e devem ser executados nesta ordem. Todos gravam em `experimentos/resultados/` ou em `pipeline_coleta_piloto/dataset_raw/`.

### Coleta de áudio

| Ordem | Comando | O que faz |
|---|---|---|
| 1 | `python pipeline_coleta_piloto/verificar_fontes.py` | Triagem de canais candidatos contra a regra de atribuição |
| 2 | `python pipeline_coleta_piloto/selecionar_videos.py` | Converte a lista de canais em plano de coleta |
| 3 | `python pipeline_coleta_piloto/coletar_local.py <plano>` | Baixa o áudio e grava os metadados |
| 4 | `notebooks/piloto_colab.ipynb` | Transcrição e diarização em GPU |

**A esteira é dividida de propósito.** A coleta roda em máquina local porque o YouTube bloqueia downloads originados de datacenter; o processamento roda no Colab porque transcrever com `large-v3` em CPU é inviável.

### Medição no modelo

| Ordem | Comando | O que faz |
|---|---|---|
| 1 | `python experimentos/smoke_test_bertimbau.py` | Viabilidade do instrumento, antes de qualquer medição de viés |
| 2 | `python experimentos/selecionar_atributos.py` | Constrói os atributos a partir do vocabulário do modelo |
| 3 | `python experimentos/teste_sensibilidade.py` | Passo 5 — o modelo responde a guise dialetal? |
| 4 | `python experimentos/teste_construcional.py` | Passo 5.1 — marcadores construcionais e calibração da frequência |
| 5 | `python experimentos/teste_explicito.py` | Passo 5.4 — menção explícita, por granularidade do rótulo |
| 6 | `python experimentos/analise_valencia.py` | Passo 5.5 — a **direção** do efeito, e não sua magnitude |

Os scripts de medição **reaproveitam medições em disco**: reexecutar um deles depois de alterar apenas a análise não recarrega o modelo nem repete medição alguma.

### Derivações independentes

Não dependem dos anteriores e podem ser rodadas a qualquer momento:

```bash
python experimentos/meta_corpus_autonomo.py       # meta do corpus, em cobertura de falantes
python experimentos/meta_pares_minimos.py         # tamanho-alvo do conjunto de pares
python experimentos/densidade_palatalizacao.py    # contextos fonéticos por minuto de fala
```

---

## Mapa do repositório

| Pasta | Conteúdo |
|---|---|
| [`docs/`](docs/) | Documentação de pesquisa: plano, filtro editorial, pendências, especificação do dataset, ficha, instrumento, fontes e fundamentação |
| [`experimentos/`](experimentos/) | Métricas, testes no modelo e derivações de meta |
| `experimentos/resultados/relatorios/` | Relatórios interpretados à mão — nenhum script os sobrescreve |
| `experimentos/resultados/tabelas/` | Saída de máquina, regerável a qualquer momento |
| `experimentos/resultados/dados/` | Medições brutas e agregadas por par |
| `experimentos/resultados/historico/` | Material superado, conservado com data |
| [`pipeline_coleta_piloto/`](pipeline_coleta_piloto/) | Coleta de áudio: triagem, planejamento, download, transcrição e diarização |
| [`notebooks/`](notebooks/) | Execução em GPU |
| `AUDITORIA.md` | Diagnóstico de organização e proposta de reestruturação |

**Documentos por onde começar**, nesta ordem: [`docs/roadmap.md`](docs/roadmap.md) para o estado geral, [`docs/achados_para_o_artigo.md`](docs/achados_para_o_artigo.md) para o que é publicável, e `experimentos/resultados/relatorios/explicito.md` para o resultado central.

---

## Dados

**O áudio não está no repositório**, e não será redistribuído. `pipeline_coleta_piloto/dataset_raw/` pesa cerca de 636 MB e é ignorada pelo git.

O compromisso de reprodutibilidade é publicar **identificadores de vídeo e código de coleta**, o que permite reconstruir o material sem violar direitos de terceiros. O campo `trecho` integra o esquema publicado justamente por isso: um identificador sem o recorte utilizado não permite reconstruir o que foi analisado.

**Duas armadilhas do esquema, para quem for consumir os dados:**

- `duracao_s` é a duração do **vídeo de origem**; `duracao_coletada_s` é a do **áudio em disco**. Somar o primeiro devolve o dobro do corpus real.
- Os rótulos de locutor são atribuídos **dentro de cada arquivo**. O mesmo repórter reaparece entre arquivos do mesmo canal, de modo que a contagem de rótulos é limite superior do número de pessoas.

A especificação completa está em [`docs/dataset-spec.md`](docs/dataset-spec.md), e a ficha no formato *datasheet* em [`docs/ficha_conjunto.md`](docs/ficha_conjunto.md) — cuja seção de **usos desaconselhados** deve ser lida antes de qualquer reaproveitamento.

---

## Estado e limitações

O corpus de áudio está em coleta. O conjunto de pares mínimos **não está constituído**: há doze itens rascunhados, nenhum validado por juízes, e a meta foi fixada em 37 pares por condição mais 80 no grupo de referência.

Nenhum item passou pelo protocolo de validação, e o eixo de prestígio ocupacional não é mensurável por pseudo-verossimilhança neste modelo — exige AUL, e é a última medição pendente.

O que está aberto está em [`docs/pendencias.md`](docs/pendencias.md). As questões que o projeto não pode decidir sozinho estão em [`docs/questoes_para_orientacao.md`](docs/questoes_para_orientacao.md).

---

## Convenções do repositório

**Procedência.** Toda afirmação de terceiros nos documentos recebe marca de *fonte verificada* ou *fonte secundária*. Nenhum dado secundário vai ao artigo sem conferência contra a fonte primária.

**Relatórios contra tabelas.** Os relatórios interpretados são escritos à mão e **nunca sobrescritos** por script; a saída de máquina fica em `tabelas/`, e é regerável. A separação existe porque a ausência dela já fez um script apagar uma análise.

**Numeração.** O plano canônico usa numeração estável em `docs/roadmap.md`; passos concluídos permanecem na tabela e nunca são renumerados. As decisões pendentes usam prefixo `D` em `docs/pendencias.md`, para não colidir com os passos.
