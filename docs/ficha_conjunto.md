# Ficha dos Conjuntos de Dados

**Função deste documento.** Ficha de conjunto de dados no formato consolidado por Gebru et al., *Datasheets for Datasets*, adotado como requisito de publicação de recurso pelos veículos a que o projeto se destina. Responde, para cada conjunto, às perguntas que um terceiro precisa ter respondidas antes de usá-lo — e, sobretudo, àquelas que o desaconselhariam de usá-lo.

**Rascunhada em:** 29/08/2026. **Estado: preliminar.** Redigida a partir do material existente, com as lacunas marcadas em vez de preenchidas. Não substitui revisão da equipe, e três de suas seções dependem de decisões ainda não tomadas, identificadas ao longo do texto.

**Escopo.** O projeto produz **dois** conjuntos, em estados muito distintos:

| Conjunto | Situação |
|---|---|
| **Corpus de fala regional** | Existe. 52 trechos, 5,52 h, seis estados. Coleta em curso |
| **Pares mínimos** | Não constituído. Doze itens rascunhados, nenhum validado. Meta fixada em 29/08/2026 |

A ficha trata os dois em separado, porque suas respostas divergem em quase todas as perguntas.

---

# Parte A — Corpus de fala regional

## A.1 Motivação

**Para que o conjunto foi criado?** Para documentar variação dialetal em fala espontânea de quatro estados nordestinos — Paraíba, Pernambuco, Ceará e Bahia — contra um grupo de controle de São Paulo e Rio de Janeiro, e permitir verificar empiricamente se marcadores dialetais descritos na literatura ocorrem em fala pública contemporânea.

**Que lacuna preenche?** A dialetologia brasileira dispõe de atlas linguísticos com metodologia de amostragem transparente, mas de assimetria temporal considerável — o Atlas Prévio dos Falares Baianos é de 1963 e o da Paraíba de 1984, contra 2010 do cearense. Marcadores extraídos das fontes mais antigas exigem confirmação em fala contemporânea, e não havia corpus disponível para isso nos estados-alvo.

**Quem criou e com que financiamento?** Projeto de pesquisa acadêmica individual, sem financiamento externo declarado. `PENDENTE:` vinculação institucional a declarar.

**Mudança de função registrada.** Até 29/08/2026 o corpus era **instrumento**: servia ao segundo filtro de validação do instrumento de texto, confirmando que um marcador ocorre em fala real antes de integrar o experimento. Nessa data a equipe decidiu tratá-lo como **entregável autônomo**, pela razão registrada em `docs/dataset-spec.md` §1.1 — quatro famílias de marcadores dialetais implícitos foram testadas sem que nenhuma produzisse resposta no modelo, e um instrumento de validação sem nada a validar não sustenta a coleta.

## A.2 Composição

**O que cada instância representa?** Um trecho de áudio de vídeo público, com transcrição alinhada por palavra e rótulo de locutor por segmento.

**Quantas instâncias?** 52 registros, correspondentes a 5,52 h de áudio efetivamente coletado. A duração dos vídeos de origem soma 11,43 h; a diferença resulta de 14 vídeos longos dos quais se coletou apenas um recorte de dez minutos.

> **Advertência a quem consumir o conjunto.** Os campos `duracao_s` e `duracao_coletada_s` significam coisas diferentes — duração do vídeo de origem e duração do áudio em disco. Somar o primeiro devolve o dobro do corpus real.

**Distribuição por estado e camada:**

| UF | Trechos | Horas coletadas |
|---|---|---|
| PB | 10 | 1,15 |
| CE | 10 | 0,79 |
| PE | 9 | 0,73 |
| RJ | 9 | 1,01 |
| BA | 7 | 1,00 |
| SP | 7 | 0,85 |

| Camada | Trechos | Proporção do tempo |
|---|---|---|
| `entrevista_vox_pop` | 21 | 32,0% |
| `podcast_radio_tv_regional` | 20 | 34,7% |
| `vlog_amador` | 11 | 33,3% |

**Que dados cada instância contém?** Nove campos, especificados em `docs/dataset-spec.md` §1.3: identificador do vídeo, canal, data de publicação, duração de origem, duração coletada, estado-alvo, tipo de fonte, recorte temporal e nome do arquivo. Os registros processados acrescentam transcrição com marcação temporal por palavra e diarização por locutor.

**Há rótulos?** Sim, e três deles são atribuídos e não observados: `estado_alvo`, `tipo_fonte` e o rótulo de locutor. O primeiro é atribuído **pelo canal**, nunca pela consulta de busca — ver A.3.

**Falta informação em alguma instância?** `data_upload` e `duracao_s` são opcionais no esquema. Nos 52 registros atuais, nenhum está ausente.

**Há redundância entre instâncias?** Sim, e é relevante. Trinta e cinco canais distintos fornecem os 52 trechos, de modo que alguns canais contribuem com mais de um vídeo. Mais grave: **os 211 rótulos de locutor produzidos pela diarização são limite superior do número de pessoas**, porque a diarização opera dentro de cada arquivo e o mesmo repórter ou apresentador reaparece entre arquivos do mesmo canal. Não há hoje verificação de identidade de falante entre arquivos.

**O conjunto é auto-contido?** Não. Depende de vídeos hospedados no YouTube, que podem tornar-se indisponíveis. Um vídeo do plano do piloto já se tornou indisponível entre o planejamento e a coleta.

**Contém dados confidenciais, sensíveis ou ofensivos?** Não intencionalmente. Registra-se apenas o que já está publicamente disponível. Contudo:

- As transcrições **não estão anonimizadas** e podem conter nomes próprios de terceiros mencionados em fala. O protocolo exige mascará-los antes de publicar, e **esse passo não está implementado**.
- Parte do material provém de telejornalismo policial, e pode conter relatos de violência e crime.
- Os falantes **não consentiram** para fins de pesquisa. Falaram em contexto público, para outra finalidade.

## A.3 Processo de coleta

**Como os dados foram obtidos?** Por download de áudio de vídeos públicos do YouTube, com `yt-dlp`, convertidos a WAV 16 kHz mono. Vídeos com mais de quinze minutos entram como recorte de dez minutos, descartados os dois primeiros minutos, onde ficam vinheta e escalada.

**Como as fontes foram selecionadas?** Por curadoria de canais, e não por consulta de conteúdo. A regra é a de A.3.1, e existe porque o método alternativo falhou de modo documentado.

### A.3.1 A regra de atribuição, e o erro que a motivou

O `estado_alvo` é atribuído **pelo canal**. Um canal entra na lista se tiver vínculo institucional com o estado — emissora, rádio, jornal ou órgão público ali sediado — ou evidência geográfica recorrente no próprio conteúdo, com menção repetida a municípios identificáveis.

A primeira rodada de levantamento buscou por formulações de conteúdo, e o resultado demonstrou que o método é inseguro: a fórmula jornalística "moradores reclamam da rua" é idêntica em todo o país, de modo que a consulta de Pernambuco devolveu emissoras de Santa Catarina e Mato Grosso, e a do Ceará devolveu Joinville. Rotular a partir da consulta introduziria erro na própria variável independente.

### A.3.2 Quatro classes de canal excluídas, e por quê

| Classe | Motivo da exclusão |
|---|---|
| **Itinerante** | Canais de viagem e motovlog citam muitos municípios — sinal que parecia de pertencimento e é de passagem. A fala pode ser de qualquer estado do trajeto |
| **Narração possivelmente sintética** | Introduziria fala não humana em corpus destinado a documentar variação humana. A suspeita basta para excluir |
| **Sem fala** | Passeios em vídeo e montagens com drone satisfazem o critério geográfico sem conter fala |
| **Falante migrante** | O canal está corretamente ancorado no estado, e o autor migrou de outra região |

A quarta é a mais grave, e a razão é direcional: sendo o vetor migratório dominante no Brasil o Nordeste para o Sudeste, um falante nordestino radicado em São Paulo incorporado ao grupo de controle **atenua sistematicamente o contraste que a pesquisa mede**, deslocando o resultado na direção da hipótese nula. O erro produz aparência de ausência de viés.

Dois casos identificados denunciaram-se pelo nome do canal, o que é acidente favorável. **Não há sinal automático para o caso geral, e a defesa efetiva — checagem de coerência dialetal na curadoria — não está implementada.**

### A.3.3 Escopo de plataforma

Adotados: YouTube e podcast por feed aberto. Excluídos: Spotify, por vedação de download nos termos de uso; TikTok e Instagram, porque o reaproveitamento de áudio de terceiros é mecanismo central dessas plataformas, de modo que um vídeo publicado por perfil sediado no estado pode veicular áudio gravado por falante de outra região — **e a dissociação não é detectável por inspeção do perfil**.

**Perda não aleatória a declarar.** Parte do material exige autenticação por restrição etária e não pôde ser baixada. A restrição recai tipicamente sobre matérias de violência, que constituem parcela expressiva do vox-pop de telejornalismo — de modo que a perda remove um tipo de conteúdo, possivelmente em proporção desigual entre estados.

**Período de coleta.** 27 e 28 de agosto de 2026.

**Houve revisão ética por comitê?** `PENDENTE:` não realizada. A situar antes de qualquer publicação, dado que os falantes não consentiram.

## A.4 Pré-processamento e rotulação

**Transcrição** por `faster-whisper`, modelo `large-v3`, com marcação temporal por palavra, filtro de atividade de voz e decodificação determinística. **Diarização** por `pyannote/speaker-diarization-community-1`. Parâmetros exatos em `pipeline_coleta_piloto/config.py`.

**O que foi medido sobre o material processado:** 45.132 palavras transcritas, 4,30 h de fala atribuída a locutor, 211 rótulos de locutor, e 3.503 contextos de palatalização de /t,d/ diante de /i/ — 13,6 por minuto de fala.

**O áudio bruto foi preservado?** Sim, localmente. Não é redistribuído.

**Qualidade da transcrição foi validada?** **Não.** A confiança média do modelo é de 0,944 para fala nordestina contra 0,939 para sudestina, o que não indica penalização de uma variedade — mas **confiança mede certeza do modelo, não acerto**. O cálculo de taxa de erro exige transcrição humana de referência, dimensionada em 20 minutos por estado, e **nenhuma foi produzida**. Enquanto isso não existir, o conjunto não deve ser usado para comparar desempenho de reconhecimento de fala entre variedades.

## A.5 Usos

**Usos pretendidos.** Verificação de ocorrência de marcadores dialetais em fala espontânea contemporânea; estimativa de taxa de palatalização por falante e por variedade; estudo de variação regional em fala pública; avaliação de sistemas de reconhecimento de fala por variedade, **após** a validação descrita em A.4.

**Usos desaconselhados, e esta é a seção que mais importa nesta ficha:**

1. **Classificação de procedência regional de falantes.** Um conjunto de fala rotulada por estado presta-se, sem nenhuma adaptação, a treinar um classificador que infira a origem de uma pessoa a partir da voz ou do texto. A finalidade do conjunto é documentar variação para investigar **preconceito contra** falantes de determinadas variedades; empregá-lo para identificá-los inverte o propósito e cria risco de discriminação em triagem de emprego, atendimento ou crédito. **Este uso é expressamente desaconselhado.**

2. **Afirmações sobre falantes a partir de ausência de marcador.** O conjunto documenta o que ocorreu na fala amostrada. A não ocorrência de um item **não** autoriza afirmar que falantes daquela região não o empregam — os itens do instrumento foram escolhidos sem evidência prévia de frequência, e o volume é pequeno.

3. **Comparação de desempenho de reconhecimento de fala entre variedades**, antes de existir transcrição de referência. Ver A.4.

4. **Generalização para a variedade de um estado.** Cada estado apresenta variação interna — urbano e rural, capital e interior, estratos sociais distintos — que a amostragem por canal público não cobre. O conjunto documenta fala pública de determinados canais, não a variedade de um estado.

5. **Análise que suponha independência entre instâncias.** Trinta e cinco canais fornecem 52 trechos, e o mesmo falante reaparece entre arquivos sem que haja verificação.

**O processamento afeta usos futuros?** Sim. A transcrição automática introduz erro cuja distribuição entre variedades não foi medida, e a detecção de marcadores por correspondência de forma sobre texto normalizado produz três classes de erro documentadas — fronteira de oração suprimida, homonímia verbal e homografia lexical — que inflam contagens de modo desigual entre marcadores.

## A.6 Distribuição

**Como será distribuído?** `PENDENTE, e é a decisão mais consequente em aberto.` A regra fixada no protocolo é publicar **identificadores de vídeo e código de coleta**, nunca o áudio bruto, o que preserva a reprodutibilidade sem redistribuir conteúdo de terceiros.

O que o protocolo **não** decidiu é o estatuto da **transcrição**, que não é áudio nem identificador. Duas condições precedem qualquer publicação dela:

1. A anonimização de nomes próprios exigida pelo protocolo, **não implementada**.
2. Uma decisão informada sobre transcrição como obra derivada do vídeo. A prática da área é publicar transcrições de corpora de fala; a questão não foi examinada por quem tenha competência para respondê-la, e **não deve ser decidida pela equipe técnica sozinha**.

**Sob que licença?** `PENDENTE.` A orientação registrada é licença em duas camadas: CC BY 4.0 para o que é autoria do projeto — metadados, anotações, documentação — e MIT para o código. As transcrições ficam **fora do escopo da licença** até a decisão acima, porque licenciar exige titularidade, e o conteúdo falado é de terceiros.

**Há restrições de terceiros?** Sim. Os termos de uso da plataforma de origem e os direitos sobre o conteúdo dos vídeos.

## A.7 Manutenção

**Quem mantém?** A equipe do projeto. `PENDENTE:` contato a declarar na publicação.

**O conjunto será atualizado?** Sim, enquanto a coleta prosseguir. A meta vigente está em `experimentos/resultados/meta_corpus_autonomo.md`: ao menos vinte falantes distintos por estado, derivados do teto de 5% por falante já fixado.

**Como erros serão comunicados?** `PENDENTE:` canal a definir. O repositório registra defeitos identificados em `docs/pendencias.md`, com uma seção dedicada ao padrão de falha silenciosa.

**Instâncias serão removidas?** Sim, quando um vídeo se tornar indisponível ou quando a curadoria identificar falante migrante, áudio sintético ou incoerência dialetal.

---

# Parte B — Conjunto de pares mínimos

**Estado: não constituído.** Esta parte registra o que está decidido e o que falta, e não descreve um conjunto existente.

## B.1 Motivação

Adaptação para variação regional do português brasileiro do desenho de pares mínimos consolidado por CrowS-Pairs e StereoSet, para os quais não existe adaptação estabelecida em português brasileiro. Cada par contrasta enunciados de conteúdo proposicional idêntico em variedades regionais distintas, permitindo medir se um modelo de linguagem atribui atributos diferentes conforme a variedade.

## B.2 Composição prevista

**Meta fixada em 29/08/2026:** 37 pares por condição de teste e 80 pares no grupo de referência não regional, perfazendo entre 228 e 265 pares. Derivação em `experimentos/resultados/meta_pares_minimos.md`.

**O critério não é arbitrado.** O tamanho responde à pergunta "quantos pares para que a ausência de efeito seja informativa", e o insumo — excluir efeitos de viés acima de 0,08 — é decisão registrada com três razões declaradas.

**Restrição de conteúdo obrigatória.** Os polos de cada eixo medido devem ser **balanceados em extensão de subtokens**. Sem isso, o conjunto reproduz o artefato que produziu, na medição do projeto, viés aparente significativo que se dissolveu ao ser controlado.

**Estado atual:** doze itens rascunhados em três blocos, nenhum validado, um suspenso por pendência bibliográfica. Os quatro blocos testados não produzem resposta detectável no modelo.

## B.3 Processo de construção e validação

Dois filtros independentes e cumulativos, especificados em `docs/pares_minimos_v1.md` §7, **nenhum aplicado**:

- **Filtro 1** — mínimo de cinco juízes falantes nativos por variedade, enunciados embaralhados, três perguntas: escolha forçada de estado, naturalidade em escala de 1 a 5 com reprovação abaixo de mediana 4, e reprovação automática se dois juízes classificarem como caricatura.
- **Filtro 2** — ocorrência do marcador em fala espontânea no corpus da Parte A.

**Vedação de desenho:** transcrições em grafia caricata não integram o conjunto. Representam fenômeno fonético em ortografia deformada, e introduzem simultaneamente raridade de segmentação e caricatura.

## B.4 Usos

**Uso pretendido.** Sondagem de viés regional em modelos de linguagem do português, por pseudo-verossimilhança ou métrica equivalente.

**Usos desaconselhados:**

1. **Tratar o conjunto como inventário de traços da fala nordestina.** Os itens são candidatos selecionados para sondar um modelo, não descrição dialetológica. Vários não têm fonte dialetológica.
2. **Empregar os itens sem controle de frequência lexical e de extensão em subtokens.** O projeto documentou dois casos em que efeitos aparentes eram, na verdade, raridade lexical e assimetria de tokenização.
3. **Tratar a unidade de replicação como a medição.** As medições de um mesmo par compartilham o enunciado e não são independentes; ignorá-lo infla o tamanho amostral por uma ordem de grandeza.
4. **Gerar texto que imite falantes de uma região.** O conjunto contém enunciados construídos para representar variedades; usá-los como molde de imitação produz precisamente a caricatura que o protocolo de validação existe para excluir.

## B.5 Distribuição

**Formato:** `PENDENTE, com proposta.` Formato canônico único, com estrutura por par — identificador, os dois lados, marcador, estado-alvo, extensão em subtokens de cada atributo e anotações de juízes —, acompanhado de script de conversão para o formato tabular dos precedentes, em vez de dois artefatos publicados a manter em sincronia.

**Licença:** `PENDENTE.` Diferentemente das transcrições, os pares mínimos são texto de autoria do projeto e admitem licenciamento permissivo sem a ressalva de titularidade.

---

# Lacunas desta ficha

Registradas aqui para que a preliminaridade do documento não se perca:

| Seção | Lacuna |
|---|---|
| A.1 | Vinculação institucional e financiamento |
| A.3 | Revisão por comitê de ética não realizada |
| A.4 | Taxa de erro de transcrição não medida contra referência humana |
| A.6 | Forma de distribuição, estatuto da transcrição e licença |
| A.7 | Contato de manutenção e canal de comunicação de erros |
| B.5 | Formato e licença |

As decisões de A.6 envolvem questão que a equipe técnica não deve responder sozinha, e estão encaminhadas para consulta externa.
