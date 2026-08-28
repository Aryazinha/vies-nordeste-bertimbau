# Achados: o que pode ser escrito, o que não pode, e sob que condição

**Função deste arquivo.** Separar o que o projeto já pode afirmar em texto submetido do que ainda não pode, e registrar, para cada item em suspenso, a condição precisa que o liberaria. Existe porque a distinção se perde com facilidade: uma medição feita em ambiente controlado, com dezessete arquivos, tem aparência de resultado e não o é — e a diferença só aparece em revisão por pares, quando já é tarde.

**Última revisão:** 28/08/2026

## Convenção de estado

| Estado | Significado |
|---|---|
| **SUSTENTADO** | Pode ser afirmado no artigo, com a qualificação indicada |
| **CONDICIONAL** | Depende de verificação nomeada; não escrever antes dela |
| **VEDADO** | Não pode ser afirmado, nem com ressalva |
| **CADERNO** | Pertence ao repositório e à reprodutibilidade, não ao texto |

---

# 1. SUSTENTADO — pode ser escrito

## 1.1 Assimetria de tokenização no BERTimbau, alinhada ao eixo de prestígio

**Seção do artigo:** Método, e Ameaças à Validade. Constitui contribuição metodológica autônoma.

Sobre trinta e seis ocupações testadas: das dezesseis de alto prestígio, **quinze** são utilizáveis por probabilidade de máscara — token único e produzidas pelo modelo com probabilidade não desprezível. Das vinte de baixo prestígio, **três** — e destas, *motorista* e *mecânico* são ofícios qualificados de prestígio intermediário, restando *empregada* como único representante do extremo inferior.

Os itens propriamente estigmatizados fragmentam-se sem exceção: *pedreiro*, *lavrador*, *faxineiro*, *garçom*, *porteiro*, *cozinheiro*, *agricultor*, *pescador*, *costureira*, *diarista*, *ambulante*, *vigia*, *caseiro*, *servente*, *feirante*, *operário*.

**Formulação forte, e sustentada:** não é possível perguntar ao BERTimbau, por preenchimento de máscara única, se ele associa um falante a ocupação de baixo prestígio — esse léxico não integra seu vocabulário como palavra inteira. Estudo de viés ocupacional em português por *fill-mask* que ignore o fato mede a segmentação do tokenizador e a reporta como viés do modelo.

O confundidor de frequência descrito por Kaneko e Bollegala (2022) encontra-se, portanto, materializado no próprio tokenizador, e alinhado ao eixo que o experimento pretende medir. O emprego de AUL deixa de ser recomendação e torna-se condição de possibilidade.

**Procedência:** medição própria, `experimentos/selecionar_atributos.py`, resultado em `experimentos/resultados/atributos_selecionados.md`. Reprodutível por terceiros.

**Qualificação obrigatória:** o repertório testado é amplo mas não exaustivo, e a seleção de itens de baixo prestígio partiu de ocupações de circulação corrente. A afirmação descreve o padrão nesse repertório.

## 1.1-A Assimetria de tokenização entre gêneros gramaticais

**Seção do artigo:** Método.

O repertório de adjetivos de caráter no feminino fragmenta mais que o masculino — 18 utilizáveis por máscara contra 23 —, e não se trata dos mesmos itens: *culto*, *educado*, *trabalhador*, *nervoso* e *estudioso* passam no masculino e falham no feminino.

Segue-se que molduras de gênero feminino e masculino operam sobre espaços de atributo distintos em tamanho e composição, e **seus resultados não são diretamente comparáveis**. A comparação exige restringi-los à interseção ou empregar AUL em ambos.

O ponto é pertinente a qualquer estudo que compare viés de gênero por *fill-mask* em português, e não apenas a este.

**Procedência:** mesma medição de 1.1.

## 1.2 Duas molduras de sondagem degeneram, e substitutas testadas

**Seção do artigo:** Método.

A moldura `Quem falou isso é [MASK]` concentra a massa de probabilidade em pronomes — *você* (0,385), *ele* (0,294), *eu* (0,075) —, não em atribuição de traço. A moldura `Quem falou isso estudou até o [MASK]` colapsa em expressão idiomática: *fim* (0,386), *final*, *momento*, *osso*, *pescoço*.

As substitutas testadas comportam-se adequadamente: `Quem falou isso completou o ensino [MASK]` concentra 97% da massa em *médio* (0,560) e *fundamental* (0,414); `O nível de escolaridade de quem falou isso é [MASK]` produz leitura bipolar entre *alto* (0,265) e *baixo* (0,209); `Quem falou isso parece uma pessoa [MASK]` elimina o vazamento de subtoken observado na formulação original.

**Consequência metodológica citável:** em português, deixar o gênero gramatical livre na lacuna não produz atribuição de traço. O controle de gênero na moldura não é refinamento, é requisito.

**Procedência:** medição própria, `experimentos/resultados/molduras_alternativas.md`.

## 1.3 Ausência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro

**Seção do artigo:** Trabalhos Relacionados, e justificativa da contribuição.

**Procedência:** levantamento bibliográfico, registrado em `docs/fundamentacao_teorica.md`, seção 1.3.1. Localizados precedentes de adaptação para francês e neerlandês, e um conjunto multilíngue sobre grupos migrantes; nenhuma adaptação para o português brasileiro.

## 1.4 O brWaC não documenta estratificação geográfica

**Seção do artigo:** Fundamentação, e Ameaças à Validade.

O artigo do corpus reporta diversidade de domínio temático, não de procedência geográfica ou de variedade. Não há metadado de geolocalização por documento nas versões distribuídas.

**Qualificação obrigatória:** apresentar como ausência de documentação, e a concentração Sul-Sudeste como hipótese de mecanismo apoiada em evidência socioeconômica indireta — jamais como fato quantificado pelos autores do corpus.

## 1.5 Diferenciação frente a Melo e Souza (2026)

**Seção do artigo:** Trabalhos Relacionados.

Sinalização explícita de região contra implícita por dialeto; LLM generativo com estima autoatribuída contra codificador MLM com pseudo-verossimilhança; granularidade regional contra estadual; instanciação automática de estímulos contra validação por juízes e por corpus.

Acresce que a seção de trabalhos futuros daqueles autores propõe expressamente "a incorporação de marcadores sociais implícitos" e "a inclusão de variações linguísticas regionais" — de modo que o presente projeto executa a continuidade que eles nomeiam. O enquadramento converte objeção de sobreposição em demonstração de pertinência.

**Procedência:** leitura integral do PDF, registrada em `docs/fundamentacao_teorica.md`, seção 1.3.4.

## 1.6 Cobertura dialetológica primária dos quatro estados-alvo

**Seção do artigo:** Método, validade de construto.

ALECE (Bessa, 2010) para o Ceará, Atlas Prévio dos Falares Baianos (Rossi, 1963) para a Bahia, ALiPE para Pernambuco, Atlas Linguístico da Paraíba (Aragão e Menezes, 1984) para a Paraíba, além do estudo ALiB de palatalização de /t,d/ cobrindo os nove estados nordestinos.

**Qualificação obrigatória:** há assimetria temporal relevante — o atlas baiano é de 1963 e o paraibano de 1984, contra 2010 do cearense. Marcadores extraídos das fontes mais antigas exigem confirmação em fala contemporânea.

## 1.7 Armadilhas de atribuição na construção de corpus regional a partir de plataforma

**Seção do artigo:** Método, e contribuição metodológica autônoma.

Quatro classes de canal satisfazem critérios geográficos e não servem ao propósito, cada uma por motivo distinto:

1. **Itinerante** — canais de viagem, motovlog e transporte citam muitos municípios do estado, e a menção a muitos municípios era o sinal aparentemente mais forte de pertencimento, quando é a assinatura de quem está de passagem.
2. **Narração possivelmente sintética** — canais de formato enumerativo citam o estado a cada título e são frequentemente narrados por voz artificial, o que introduziria fala não humana em corpus destinado a documentar variação humana.
3. **Sem fala** — passeios em vídeo e montagens com drone percorrem bairros identificáveis sem que ninguém fale.
4. **Falante migrante** — o canal está corretamente ancorado no estado e o autor migrou de outra região.

A quarta merece destaque teórico: sendo o fluxo migratório dominante no Brasil o Nordeste para o Sudeste, o erro **atenua sistematicamente o contraste que a pesquisa mede**, deslocando o resultado na direção da hipótese nula. Produz, portanto, aparência de ausência de viés.

**Procedência:** levantamento próprio de 390 canais candidatos, com registro em `docs/fontes_coleta.md`, seções 2.4 e 2.5. Casos concretos documentados, incluindo dois canais autoidentificados como migrantes e um canal de falante moçambicano residente em Salvador.

## 1.8 Dimensionamento de corpus a partir do requisito de detecção de variante rara

**Seção do artigo:** Método.

O volume de fala necessário por variedade foi derivado da condição estatística que torna a **ausência** de uma variante informativa, e não arbitrado. Tomando a produtividade máxima da negação pós-verbal reportada por Santos e Vitório (2025), 5,6%, e as premissas de fala declaradas, chega-se a cerca de 4,1 h de fala do locutor-alvo por variedade para que zero ocorrências constituam evidência, e não insuficiência amostral.

**Procedência:** `experimentos/meta_volume_corpus.py`, com premissas declaradas no próprio script.

**Confirmação empírica.** Com 0,25 h de fala por estado no primeiro lote, o cálculo previa menos de uma ocorrência de negação pós-verbal por estado, e observaram-se zero — situação que o próprio cálculo descreve como não informativa. O dimensionamento, portanto, descreveu corretamente o regime em que a ausência não distingue "não ocorre" de "não foi amostrado".

**Qualificação obrigatória:** as premissas de fala — palavras por minuto, palavras por oração, proporção de orações negadas — são estimativas declaradas, não medições.

---

## 1.9 Detecção de marcadores dialetais por correspondência de forma é inadequada

**Seção do artigo:** Método, e contribuição metodológica.

A busca por expressão regular sobre transcrição normalizada produz três classes de erro, todas verificadas neste corpus:

1. **Fronteira de oração suprimida.** "foi. Não ia dar certo" é contabilizado como negação pós-verbal "foi não". Os três únicos candidatos encontrados no primeiro lote eram desse tipo.
2. **Homonímia de forma verbal.** "ele vai" é contabilizado como imperativo no indicativo, quando é presente do indicativo.
3. **Homografia lexical.** *visse*, imperfeito do subjuntivo de *ver*, é contabilizado como o marcador discursivo recifense; *da hora*, na acepção literal — "os pacotinhos da hora e da roça" —, é contabilizado como gíria paulistana.

Os três erros inflam a contagem, e o fazem **de modo desigual entre marcadores e entre grupos**, o que enviesa a comparação e não apenas sua magnitude. A detecção precisa operar sobre texto com pontuação preservada e com análise morfossintática.

O ponto vale para qualquer trabalho que pretenda confirmar marcadores dialetais em corpus por meio de listas de formas.

**Procedência:** inspeção individual de todas as ocorrências em 5,52 h de transcrição, `experimentos/resultados/piloto_medicoes.md`.

## 1.10 Critérios de escopo de plataforma para corpus de fala regional

**Seção do artigo:** Método.

TikTok e Instagram foram excluídos do corpus principal por razão que não é de conveniência: o reaproveitamento de áudio de terceiros é mecanismo central dessas plataformas, de modo que um vídeo publicado por perfil sediado no estado-alvo pode veicular áudio gravado por falante de outra região. **A dissociação entre origem do vídeo e origem da voz não é detectável por inspeção do perfil ou do conteúdo visual** — diferentemente da contaminação por consulta de busca, que o é.

Registram-se ainda três fatores onerosos: alta incidência de encenação de sotaque com finalidade humorística, que é a caricatura que a validade de construto exige excluir; sobreposição de música à fala; e duração típica que eleva o custo de curadoria por hora aproveitável.

Em contrapartida, podcast distribuído por feed aberto é publicado com a finalidade explícita de ser baixado, e constitui a fonte de situação jurídica mais clara disponível — superior, nesse aspecto, ao próprio YouTube.

**Procedência:** `docs/fontes_coleta.md`, seção 2.3.

## 1.11 Confundidor de escolaridade no marcador do imperativo

**Seção do artigo:** Método, validade de construto.

A forma subjuntiva do imperativo é a prescrita pela tradição gramatical, e seu uso correlaciona-se com escolaridade mais alta **dentro da própria comunidade nordestina**. Figuereido (2025) reporta, para Feira de Santana, estimativa negativa para o nível superior (−2,23) frente ao intercepto: falantes mais escolarizados empregam menos a forma indicativa — 40% contra 53% dos menos escolarizados. Em Campinas a variável não é significativa.

Segue-se que um *guise* nordestino construído sobre a forma subjuntiva fica parcialmente sobreposto à condição "falante mais escolarizado", e o efeito medido pode ter sinal invertido em relação ao viés pretendido. Registre-se que Sampaio (2001), para Salvador, encontra direção oposta do efeito.

**Procedência:** fonte verificada, leitura integral. O mesmo trabalho fornece o contraste interregional disponível: Campinas-SP 81% de morfologia indicativa contra Feira de Santana-BA 47%.

## 1.12 Perda não aleatória por restrição etária

**Seção do artigo:** Método, e Ameaças à Validade.

Parte do material exige autenticação por restrição etária, e o download é abortado. A perda não é aleatória: a restrição recai tipicamente sobre matérias de violência e crime, que constituem parcela expressiva do vox-pop de telejornalismo policial — justamente o conteúdo em que moradores são entrevistados na rua. A exclusão silenciosa removeria um tipo de conteúdo, possivelmente em proporção desigual entre estados.

A contabilização de perdas por estado e camada é, portanto, requisito de método, e não zelo administrativo.

**Procedência:** `docs/pendencias.md`, seção 4.5.

# 2. CONDICIONAL — depende de verificação nomeada

## 2.1 A transcrição automática não penaliza a fala nordestina

**Estado:** indício consistente em dois lotes; falta o WER.
**Medido, 52 arquivos e 45 mil palavras:** Nordeste 0,944, Sudeste 0,939, diferença de +0,006 em favor do Nordeste. Por estado, entre 0,929 (RJ) e 0,948 (PE e SP).
**Estabilidade:** no primeiro lote, com 17 arquivos, a dispersão entre estados ia de 0,898 a 0,975; com o triplo do material reduziu-se a 0,929–0,948. A variação anterior era ruído de amostra pequena, e a convergência reforça a leitura em vez de enfraquecê-la.
**Libera a afirmação:** WER contra transcrição humana de referência. Confiança mede certeza do modelo, não acerto, e nenhuma quantidade de confiança substitui a comparação com referência.
**Se confirmado:** remove confundidor previsto na Parte 3 do `CLAUDE.md`, e constitui resultado secundário publicável.
**Se não confirmado:** torna-se limitação central.
**Ressalva de balanceamento:** o material nordestino tem o dobro de palavras do sudestino (30 mil contra 15 mil), o que não invalida a comparação de médias mas deve ser declarado.

## 2.2 Rendimento por camada e revisão da meta de volume

**Estado:** medido em dois lotes, com estabilidade entre eles.
**Medido, 52 arquivos:** 91,8% de fala em vox-pop contra 35% supostos; 87,3% em podcast contra 60%; 85,1% em vlog contra 70%. No primeiro lote, 92,3%, 89,2% e 81,0% — variação pequena com o triplo do material.
**Descontado o locutor dominante:** cerca de 47% de fala-alvo em vox-pop, e a suposição de 70% para vlog foi a única correta.
**Recálculo:** cerca de 6,4 h de áudio bruto por estado, e 38 h no total, contra 8,3 h e 50 h supostas.
**Libera a afirmação:** verificação de 2.3, da qual a leitura do vox-pop depende.

## 2.3 A diarização separa o morador entrevistado do repórter

**Estado:** sustentado quanto à separação; não verificado quanto à identidade.
**Medido, 52 arquivos:** a média de locutores por arquivo mantém a ordenação entre camadas observada no primeiro lote, com o dominante ocupando 51% do tempo em vox-pop, 73% em podcast e 83% em vlog — coerente com a natureza de cada camada.
**Não verificado:** que o locutor dominante da camada de vox-pop seja o repórter, e não um entrevistado loquaz. Da suposição depende toda a estimativa de fala aproveitável.
**Libera a afirmação:** verificar se o mesmo perfil de voz reaparece em vídeos distintos do mesmo canal.

## 2.4 Assimetria de ocorrência entre os itens lexicais dos dois grupos

**Estado:** medido em 5,52 h; forte, e com consequência decidida sobre o instrumento.
**Medido:** nenhuma ocorrência dos itens nordestinos do instrumento em 29.999 palavras de fala nordestina; cinco ocorrências dos itens sudestinos em 14.934 palavras de fala sudestina — *mano* (3), *maneiro* (1) e *caraca* (1) —, distribuídas pelas três camadas. Na camada de vlog isoladamente, o grupo nordestino dispõe de mais material (7.917 palavras contra 5.338) e registra zero. Sob taxas iguais, esperar-se-iam cerca de dez ocorrências no material nordestino; a probabilidade de observar zero é da ordem de 4×10⁻⁵.
**Homógrafos excluídos após inspeção individual:** *visse* como imperfeito do subjuntivo de *ver*, e *da hora* na acepção literal, ocorrida no Ceará.

**O que autoriza afirmar:** neste corpus, os itens lexicais nordestinos do instrumento não ocorrem, os sudestinos ocorrem, e a diferença de taxa é improvável sob hipótese de igualdade.

**O que não autoriza afirmar:** que falantes nordestinos não empreguem léxico regional. Os itens foram escolhidos sem evidência de frequência, e as duas listas não são equivalentes em natureza — a sudestina reúne gíria urbana corrente; a nordestina, itens possivelmente restritos a registros, faixas etárias ou contextos que este corpus não amostra. **O achado é sobre os itens do instrumento, não sobre os falantes.** Escrever o contrário seria erro grave, e do tipo que confirma o próprio preconceito que o artigo investiga.

**Consequência já decidida:** o bloco lexical do instrumento é assimétrico, e não apenas frágil. Contrastaria itens sudestinos atestados em fala real contra itens nordestinos não atestados, o que não constitui *matched-guise*. Efeito medido nessas condições é indistinguível de artefato.

**Libera afirmação mais forte:** levantamento de frequência dos itens em corpus de fala de referência, que permitiria distinguir "itens raros" de "itens mal escolhidos".

## 2.5 A sensibilidade do modelo concentra-se no léxico

**Estado:** medido em conjunto pequeno, sem teste estatístico.
**Medido:** divergência de Jensen-Shannon mediana de 0,0144 bits no bloco lexical contra 0,0023 no morfossintático, tendo 0,0963 como referência de conteúdo proposicional distinto.
**Libera a afirmação:** conjunto de itens em volume adequado e teste estatístico. Doze itens não sustentam inferência.
**Se confirmado:** exige reposicionamento do artigo, pois um efeito de origem lexical é atacável como efeito de frequência, e não de dialeto. É a objeção mais previsível em revisão.

## 2.6 A marcação explícita de região não revela o viés

**Estado:** leitura própria de tabela publicada, não confirmada contra o texto integral.
**Observado:** na Tabela 7 de Melo e Souza (2026), o marcador "nordeste" recebe estima **superior** à do marcador "sudeste" em três dos quatro modelos avaliados. O texto do artigo afirma que a menor pontuação da categoria é a do sujeito "nordeste", o que é compatível com a tabela apenas na leitura de que 2,150 é o menor valor absoluto.
**Libera a afirmação:** conferência contra o texto integral e, idealmente, comunicação com os autores.
**Se confirmado:** argumento forte para a introdução — a sinalização explícita não produziu o rebaixamento esperado, o que é o padrão de Hofmann et al. (2024), em que o alinhamento suprime o preconceito manifesto e preserva o encoberto. Motiva diretamente a abordagem implícita.

## 2.7 Direção do marcador do imperativo em Fortaleza

**Estado:** fontes secundárias em conflito.
**Conflito:** uma indica predomínio subjuntivo em Fortaleza; outra indica indicativo favorecido, com peso relativo 0,66. O capítulo de Oliveira (2017) não pôde ser consultado.
**Libera a afirmação:** consulta ao capítulo impresso.
**Consequência atual:** o item que representa o Ceará no instrumento está suspenso.

---

# 3. VEDADO — não pode ser escrito

## 3.1 Qualquer afirmação sobre viés do BERTimbau contra fala nordestina

**Não foi medido.** Nenhuma vez. O instrumento não está validado, o conjunto de itens não está fechado, nenhum juiz foi consultado e nenhum escore de viés foi calculado. Não há resultado — nem positivo, nem negativo, nem nulo.

Nada no material atual autoriza sequer a formulação "resultados preliminares sugerem".

## 3.2 O índice de 94% de imperativo indicativo no Rio de Janeiro

Registrado em revisão anterior do projeto e **não confirmado por nenhuma fonte** consultada. Não deve ser citado enquanto a origem não for localizada. O único contraste verificado entre variedades é o de Figuereido (2025), entre cidades do interior: Campinas-SP 81% contra Feira de Santana-BA 47%.

## 3.3 Que os marcadores dialetais do instrumento estejam validados

Nenhum item passou pelo Filtro 1, de juízes falantes nativos, nem pelo Filtro 2 em volume suficiente. Os itens são candidatos, e o texto deve tratá-los como tais.

## 3.4 Balanceamento de frequência lexical entre condições — parcialmente endereçado

**Deixa de ser inteiramente vedado.** A frequência dos itens lexicais foi medida em 28/08/2026, com resultado registrado em `experimentos/resultados/piloto_medicoes.md`, adendo B.

**Pode ser afirmado:** as listas do Bloco B não eram comparáveis em frequência — de uma a três ordens de grandeza de distância, com dois itens nordestinos ausentes da fonte —, e o desequilíbrio é de dupla natureza: itens nordestinos de circulação restrita contra itens sudestinos de circulação nacional. Declarar como limitação identificada e corrigida, não como controle que o desenho sempre teve.

**Continua vedado:** afirmar que o instrumento final está balanceado, o que depende da reformulação do bloco.

**Qualificação obrigatória:** a fonte de frequência não estratifica por variedade nem separa português brasileiro de europeu. Item regionalmente restrito tem frequência nacional baixa por construção, de modo que a medida compara itens entre si e não caracteriza uso regional.

## 3.5 Qualquer afirmação de significância estatística

Nenhum teste foi executado sobre nenhuma medida.

## 3.6 Que a composição do brWaC explique o viés observado

Não há viés observado, e a composição do corpus não é auditável. A relação permanece hipótese de mecanismo.

---

# 4. CADERNO — pertence ao repositório, não ao texto

Defeitos identificados e corrigidos durante o desenvolvimento: falha silenciosa que reportava download bem-sucedido sem arquivo em disco; aceitação de URL de canal onde se esperava vídeo; caminhos de dados relativos ao diretório de trabalho; incompatibilidade com a API nova do `pyannote`; dependência de versão do `yt-dlp` e de runtime de JavaScript.

Pertencem à documentação de reprodutibilidade. Uma exceção possível: o bloqueio de downloads originados de datacenter, que afeta qualquer tentativa de replicação em ambiente de nuvem e justifica nota em apêndice de reprodutibilidade.

---

# 5. Situação do artigo

Em termos de estrutura de texto submetido:

| Seção | Situação |
|---|---|
| Introdução e motivação | sustentada |
| Trabalhos relacionados | sustentada |
| Fundamentação | sustentada |
| Método | sustentada, e com contribuições próprias (itens 1.1, 1.2, 1.7, 1.8) |
| **Resultados** | **vazio** |
| Ameaças à validade | madura, e mais desenvolvida que o usual |
| Conclusão | inexistente, por depender de Resultados |

**Dois caminhos possíveis, não excludentes.**

O primeiro é o artigo pretendido: medição de viés dialetal implícito no BERTimbau. Exige instrumento corrigido e validado, corpus em volume suficiente para o Filtro 2, e a medição propriamente dita. É o de maior alcance e o mais distante.

O segundo é um **artigo de recurso e método**: o conjunto de pares mínimos para variação regional do português brasileiro, o protocolo de validação em dois filtros, o dimensionamento por requisito de detecção, e os achados sobre tokenização e sobre construção de corpus a partir de plataforma. Os precedentes que o projeto adota — CrowS-Pairs e French CrowS-Pairs — são exatamente dessa natureza, com a medição no modelo servindo de demonstração de uso. É alcançável com o que já existe, mais a validação por juízes, e constrói o terreno do primeiro.

A escolha é da equipe. Registre-se apenas que, no estado atual, o segundo caminho está muito mais próximo do que o primeiro.
