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

## 1.13 O BERTimbau não responde a marcadores dialetais morfossintáticos

**Seção do artigo:** Resultados — é o primeiro item que pertence a essa seção.

Em teste com condições de controle que estabelecem piso e teto de sensibilidade, a alternância do imperativo e o deslocamento da negação produzem diferença de escore igual à do piso: 1,00× a mediana da condição neutra, com os cinco pares entre 0,70× e 1,27×, dentro da faixa da própria condição neutra (0,41× a 1,55×).

**A afirmação é sustentada porque a medição foi calibrada nos dois extremos.** O controle de conteúdo proposicional produz 6,32× o piso, o que demonstra capacidade de detecção; e a condição dialetal morfossintática é pareada em frequência — *feche* e *fecha* são ambas correntes —, o que exclui a explicação por raridade. Nulo com instrumento demonstradamente capaz é resultado, não ausência de resultado.

**Procedência:** `experimentos/teste_sensibilidade.py`, resultado em `experimentos/resultados/sensibilidade_guise.md`.

**Qualificação obrigatória:** cinco pares por condição, um modelo (BERTimbau Base), uma métrica (PLL sobre alvo mascarado), sem teste de significância. A afirmação deve ser formulada como ausência de efeito detectável nessas condições, e não como impossibilidade.

## 1.14 O efeito do bloco lexical é atribuível à raridade das palavras

**Seção do artigo:** Resultados, e Ameaças à Validade.

Uma condição de controle com palavras raras **não regionais**, pareadas por frequência com os itens do instrumento — *chinfrim* (0,081 por milhão) para *arretado* (0,100), *combalido* (0,071) para *aperreado* (0,000) —, reproduz o efeito do bloco dialetal quase par a par: medianas de 2,80× contra 2,71× o piso, com correspondência item a item.

**Procedência:** mesma execução.

### Revisão de 28/08/2026, obrigatória

A redação original deste item prosseguia afirmando que "nesta métrica, a diferença de escore entre dois contextos é **dominada** pela frequência das palavras que os distinguem", e lia a menção explícita à região como indistinguível do controle de raridade. Com conjunto de calibração três vezes maior — 22 pares não regionais, com razões de frequência de 1,0× a 2.883× —, a forma forte não se sustenta e **não deve ser escrita**.

O que a calibração mostra é que a razão de frequência responde por R² = 0,180 da variação entre pares, com p = 0,0493 para a inclinação. O efeito é real, positivo e modesto. Entre pares de razão de frequência praticamente idêntica, |Δ| varia por um fator de sete.

**Formulação sustentada:**

- a frequência lexical tem efeito positivo e mensurável sobre a diferença de escore;
- um controle de raridade não regional reproduz o efeito do bloco lexical, o que continua a impedir a leitura dialetal daquele bloco — esta é a parte central do item, e permanece intacta;
- **a maior parte da variação entre pares é idiossincrática**, determinada por quais palavras foram trocadas e não pela frequência delas.

**A consequência metodológica muda de forma junto com o diagnóstico, e ganha alcance.** O que inviabiliza a comparação ingênua entre guises não é apenas o desbalanceamento de frequência, corrigível por pareamento: é que o **ruído no nível do par é da ordem do efeito procurado** — desvio-padrão de 0,0618 nos resíduos de calibração, contra mediana de 0,1360. Segue-se que *matched-guise probing* com métrica de verossimilhança exige muitos pares, calibração explícita da resposta à frequência e estatística por conglomerado no nível do par. Delineamentos que comparem duas condições por uma diferença de médias sobre medições individuais tratam como replicação o que é a mesma frase medida várias vezes.

**Procedência da revisão:** `experimentos/teste_construcional.py`, relatório em `experimentos/resultados/construcional.md`, seção 5.

## 1.15 Nenhuma das quatro famílias de sinalização dialetal implícita produz resposta detectável

**Seção do artigo:** Resultados.

Quatro famílias foram testadas contra a mesma calibração, e nenhuma apresenta resíduo acima do que a frequência lexical prevê:

| Família | Pares | Resíduo médio | Pares acima da reta | p | p Holm |
|---|---|---|---|---|---|
| morfossintática — imperativo e negação | 5 | −0,0608 | 0/5 | 0,9900 | 1,0000 |
| lexical — itens regionais | 5 | +0,0447 | 4/5 | 0,1266 | 0,5064 |
| feixe combinado | 5 | −0,0063 | 3/5 | 0,5671 | 1,0000 |
| **construcional** | **10** | **−0,0141** | **3/10** | **0,7129** | **1,0000** |

A família construcional foi acrescentada em 28/08/2026 para testar a única pista que a explicação por raridade não cobria, e é a mais informativa por dois motivos. Primeiro, seus itens são de frequência atestada — *lhe* de segunda pessoa, *tu* sem flexão, comitativo com *mais*, vocativos *menino* e *rapaz*, avaliativo *massa* —, de modo que a raridade não é explicação disponível. Segundo, a pista original não replicou: o vocativo *menino* contra *cara* apresenta resíduo de +0,0443, mas o vocativo *rapaz* contra o mesmo *cara* apresenta −0,0846, o maior resíduo negativo da condição. Mesma construção, mesmo termo de comparação, sinais opostos.

**O caso mais limpo é a negação pós-verbal.** Os pares *fui não* / *não fui* e *sei não* / *não sei* empregam exatamente as mesmas palavras em ordem diferente, com razão de frequência 1,0 por construção. O confundidor não é atenuado, é eliminado. Ambos apresentam resíduo negativo.

**Duas condições de interpretabilidade estão satisfeitas**, e sem elas o nulo não seria legível:

1. *A medição detecta o que existe.* O controle de conteúdo proposicional apresenta resíduo de +0,3597, com p = 0,0003 após correção de Holm, apesar de razão de frequência baixa (2,3×). É o controle positivo do próprio método de resíduo.
2. *O confundidor de frequência está descontado*, e não apenas declarado, pela reta ajustada sobre 22 pares não regionais.

**Formulação correta:** o BERTimbau Base não exibe, sob pseudo-verossimilhança, resposta detectável à sinalização dialetal implícita, nas quatro famílias testadas. **Formulação incorreta:** o BERTimbau não distingue as variedades, ou não apresenta viés regional.

**Qualificação obrigatória:** um modelo, uma métrica, e cinco pares em três das quatro famílias. A afirmação é sobre ausência de efeito detectável nestas condições.

**Procedência:** `experimentos/teste_construcional.py`, relatório em `experimentos/resultados/construcional.md`.

## 1.16 A unidade de replicação em *matched-guise probing* é o par, não a medição

**Seção do artigo:** Método. Contribuição metodológica autônoma.

Um instrumento de *matched-guise* multiplica pares por molduras por atributos, e o número de medições cresce depressa: 28 medições por par neste desenho. As medições de um mesmo par compartilham o enunciado e não são independentes, de modo que tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza e produz significância espúria.

A consequência é verificável neste conjunto: com o piso e as medianas calculados sobre medições individuais, a condição de controle neutro aparece como 1,25× de si mesma quando confrontada com medianas de par. Ambos os números descrevem os mesmos dados.

Adotou-se, por isso, estatística por conglomerado — reamostragem de pares para o intervalo, permutação de rótulos de par para o valor-p, e correção de Holm para a família de condições confrontadas com a mesma calibração.

**Procedência:** medição própria. O ponto vale para qualquer trabalho do gênero, e a literatura consultada não o explicita.

## 1.17 O modelo responde à menção explícita da região, e o efeito concentra-se em rótulos de pessoa

**Seção do artigo:** Resultados. É o primeiro resultado positivo do projeto, e forma par com 1.15.

Duas condições de menção explícita produzem resíduo acima da reta da frequência e **sobrevivem à correção de Holm** para as nove condições confrontadas com a mesma calibração:

| Condição | Pares | Razão med. | Resíduo médio | Acima da reta | p Holm |
|---|---|---|---|---|---|
| gentílico de estado — *pernambucano*, *baiano*, *cearense* | 8 | 3,8× | +0,1567 | 8/8 | **0,0012** |
| macrorregião — *Nordeste*, *nordestino* | 8 | 1,8× | +0,1072 | 7/8 | **0,0038** |
| topônimo — *Ceará*, *Recife*, *Salvador* | 8 | 4,9× | +0,0326 | 6/8 | 0,4177 |

**Não é efeito de raridade,** e a comparação com 1.14 é o que o estabelece: as duas condições significativas têm as razões de frequência **mais baixas** de todo o conjunto, e o par mais bem pareado — *pernambucano* contra *paulistano*, a 1,1× — apresenta resíduo de +0,0895, uma vez e meia o desvio-padrão do ruído de calibração.

**O contraste com 1.15 é a contribuição.** Mesmo modelo, mesma métrica, mesma reta de calibração, mesma estatística por conglomerado: quatro famílias de sinalização implícita entre −0,061 e +0,050, nenhuma significativa; menção explícita a +0,107 e +0,157, ambas sobreviventes à correção.

**Formulação sustentada:** o BERTimbau Base responde à menção explícita da região acima do que a frequência lexical prevê, e não responde à sinalização dialetal implícita. **Formulação vedada:** que o modelo apresente viés contra falantes nordestinos — a medida é de magnitude, em valor absoluto, e nada diz sobre direção. Ver 3.7.

**Procedência:** `experimentos/teste_explicito.py`, relatório em `experimentos/resultados/explicito.md`.

**Qualificação obrigatória:** oito pares por condição, um modelo, uma métrica. O contraste de gentílico não é simétrico, pela inexistência de *sudestino* — ver 1.18.

## 1.17-A Rótulo de pessoa contra rótulo de lugar — exploratório

**Seção do artigo:** Resultados, e **apenas com a declaração de estatuto abaixo**.

A predição registrada antes da medição era ordinal por granularidade do rótulo, e não se confirmou: o gentílico de estado supera a macrorregião. A inspeção por par mostra que o corte é outro — entre enunciados que nomeiam uma **pessoa** e os que nomeiam um **lugar** —, e que ele atravessa a condição de macrorregião, cujos quatro pares com *Nordeste* rendem +0,043 contra +0,172 dos quatro com *nordestino*.

Reagrupados os 24 pares explícitos por essa distinção: rótulo de pessoa, 12 pares, +0,1618, **doze de doze acima da reta**; rótulo de lugar, 12 pares, +0,0359, nove de doze. Diferença entre os agrupamentos, p = 0,0003.

**Declaração de estatuto, obrigatória em qualquer menção:** a hipótese foi formulada **depois** de ver os dados. O valor-p não tem o estatuto dos de 1.17 e vale como magnitude de efeito a testar em conjunto novo. O que permanece confirmatório é 1.17: as duas condições que contêm rótulos de pessoa sobrevivem a Holm, e a que contém apenas topônimos não sobrevive.

**Leitura substantiva, se confirmado:** o modelo associa conteúdo a categorias de pessoa e trata nomes de lugar como topônimos quaisquer. *Nordestino* carrega representação social; *Recife* não.

## 1.18 O português não dispõe de gentílico corrente para o Sudeste

**Seção do artigo:** Método, e Ameaças à Validade.

*Sudestino* apresenta frequência de 0,015 por milhão contra 4,27 de *nordestino* — razão de 285 vezes. O contraste simétrico de gentílico de macrorregião é, por isso, impossível de construir, e os controles empregados foram gentílicos de outra macrorregião (*sulista*) ou de estados do Sudeste (*mineiro*, *carioca*, *paulista*, *paulistano*, *fluminense*).

O fato é dado, e não apenas obstáculo de desenho: a categoria "nordestino" existe na língua como rótulo de pessoa de um modo que "sudestino" não existe. É consistente com a leitura de que a primeira funciona como categoria social e a segunda como coordenada geográfica, e deve ser reportada como limitação **e** como evidência.

**Procedência:** medição própria com `wordfreq`, registrada em `experimentos/teste_explicito.py`.

**Qualificação obrigatória:** a fonte de frequência não estratifica por variedade nem separa português brasileiro de europeu.

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

## 2.8 O modelo responde à menção explícita da região, e não à variedade que a indicia

**Estado:** único resíduo consistente entre as condições regionais; não sobrevive à correção de multiplicidade.
**Medido:** a condição de menção explícita apresenta resíduo médio de +0,0711 acima da reta da frequência, com **os cinco pares acima da reta** e p = 0,026 por permutação. Cinco positivos em cinco têm probabilidade 1/32 sob sinal aleatório.
**Estrutura interna, e é ela que torna o achado interessante:** os dois maiores resíduos são os pares que nomeiam a região como categoria — "do Nordeste" contra "do Sudeste" (+0,1820) e "um nordestino" contra "um paulista" (+0,1123). Os três que nomeiam estados ficam próximos de zero: Paraíba (+0,0322), Ceará (+0,0235), Pernambuco (+0,0052). É o padrão de um modelo que associa conteúdo ao rótulo regional e trata topônimos estaduais como topônimos quaisquer.
**Revisa leitura anterior.** O relatório de sensibilidade registrara esta condição como indistinguível do controle de raridade. Era leitura correta enquanto a comparação era de medianas brutas, e deixa de sê-la quando a frequência é descontada — precisamente porque os pares desta condição são os que mais dela sofriam.
**Libera a afirmação:** volume. Com correção de Holm para as seis condições, p sobe a 0,13, e são cinco pares. É necessário um conjunto de pares de menção explícita em volume comparável ao dos demais blocos, com a distinção entre rótulo de região e nome de estado como variável de desenho.
**Se confirmado:** produz o contraste central do artigo — o modelo responde à categoria regional nomeada e não à variedade linguística que a indicia. É o recorte de Hofmann et al. (2024) com os termos invertidos, e o contraste direto com Melo e Souza (2026), que mediram exatamente a sinalização explícita.
**Se não confirmado:** o projeto fica sem qualquer resposta do modelo a estímulo regional, e o caminho 5.3 do roadmap torna-se o único disponível.

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

## 3.1 Afirmação sobre viés do BERTimbau contra fala nordestina

**Requalificado em 28/08/2026.** Deixa de ser "não foi medido" e passa a ser "mediu-se a condição de possibilidade, e ela não se verificou para a morfossintaxe".

**Continua vedado** afirmar que o BERTimbau enviesa, ou que não enviesa, contra fala nordestina. O que se estabeleceu é que os marcadores morfossintáticos do instrumento não produzem resposta detectável, e que o efeito dos marcadores lexicais é atribuível à raridade. Não havendo resposta ao guise, não há viés a medir por esse caminho — o que é afirmação sobre o método, e não sobre a existência do preconceito.

**Formulação correta:** não foi possível detectar, com este desenho, resposta do modelo à sinalização dialetal. **Formulação incorreta:** o BERTimbau não apresenta viés regional.

**Atualização de 28/08/2026, segunda requalificação.** O teste construcional acrescentou a quarta família de marcadores, descontou o confundidor de frequência por calibração explícita e executou os primeiros testes de significância do projeto. O que era "não foi possível detectar resposta" passa a ser afirmação com controle positivo e valor-p, registrada em 1.15.

**Segue vedado:** afirmar que o BERTimbau enviesa, ou que não enviesa, contra fala nordestina. Não havendo resposta ao guise, não há viés a medir por esse caminho, e a afirmação é sobre o método e o modelo, não sobre a existência do preconceito.

**Segue vedado igualmente:** apresentar como resultado de viés o resíduo da menção explícita (item 2.8). Ele é direção a investigar, com cinco pares e sem sobreviver à correção de multiplicidade.

**Formulação correta:** o BERTimbau Base não exibe, sob pseudo-verossimilhança, resposta detectável à sinalização dialetal implícita, nas quatro famílias testadas. **Formulação incorreta:** o BERTimbau não apresenta viés regional.

O instrumento continua não validado por juízes, e o conjunto de itens continua aberto. O que o material autoriza é uma seção de Resultados sobre **a viabilidade do desenho**, e não sobre a magnitude de um viés.

## 3.2 O índice de 94% de imperativo indicativo no Rio de Janeiro

Registrado em revisão anterior do projeto e **não confirmado por nenhuma fonte** consultada. Não deve ser citado enquanto a origem não for localizada. O único contraste verificado entre variedades é o de Figuereido (2025), entre cidades do interior: Campinas-SP 81% contra Feira de Santana-BA 47%.

## 3.3 Que os marcadores dialetais do instrumento estejam validados

Nenhum item passou pelo Filtro 1, de juízes falantes nativos, nem pelo Filtro 2 em volume suficiente. Os itens são candidatos, e o texto deve tratá-los como tais.

## 3.4 Balanceamento de frequência lexical entre condições — parcialmente endereçado

**Deixa de ser inteiramente vedado.** A frequência dos itens lexicais foi medida em 28/08/2026, com resultado registrado em `experimentos/resultados/piloto_medicoes.md`, adendo B.

**Pode ser afirmado:** as listas do Bloco B não eram comparáveis em frequência — de uma a três ordens de grandeza de distância, com dois itens nordestinos ausentes da fonte —, e o desequilíbrio é de dupla natureza: itens nordestinos de circulação restrita contra itens sudestinos de circulação nacional. Declarar como limitação identificada e corrigida, não como controle que o desenho sempre teve.

**Continua vedado:** afirmar que o instrumento final está balanceado, o que depende da reformulação do bloco.

**Qualificação obrigatória:** a fonte de frequência não estratifica por variedade nem separa português brasileiro de europeu. Item regionalmente restrito tem frequência nacional baixa por construção, de modo que a medida compara itens entre si e não caracteriza uso regional.

## 3.7 Que a resposta do modelo à região seja preconceituosa

**Aberto em 29/08/2026, e é hoje a vedação mais importante do documento.**

Toda a medição do projeto emprega |Δ PLL| em **valor absoluto**. Isso responde a "o modelo responde ao guise?" e não responde a "o modelo responde com preconceito?" — um modelo que assinalasse ao guise nordestino atributos *mais favoráveis* produziria exatamente o mesmo número.

A medida com sinal foi implementada em `experimentos/analise_valencia.py`, em dois eixos separados, e o resultado é **inconclusivo por subdimensionamento**: o controle positivo não sobrevive à correção de Holm em nenhum dos dois eixos, ainda que apresente as maiores magnitudes brutas de ambas as tabelas. Com cinco pares no grupo de referência, a permutação não tem resolução. Pela lógica de interpretabilidade que o projeto aplica desde o passo 5, quando o controle positivo não passa, nenhum nulo é legível.

**Vedado, portanto:** afirmar que o modelo deprecia falantes nordestinos; afirmar que **não** os deprecia; e citar qualquer valor da tabela de valência como resultado, inclusive o viés de caráter de +0,195 da condição de macrorregião, com sete de oito pares positivos, que é o mais sugestivo do conjunto.

**Vedado com ênfase particular:** ler o viés de ocupação de −0,271 da condição de gentílico — ocupações de alto prestígio tornando-se mais prováveis sob o guise nordestino — como ausência de estigma ocupacional. A explicação alternativa mais provável é o artefato de segmentação registrado em 1.1, e não foi descartada.

**Formulação correta:** o modelo **distingue**; se **deprecia**, não se sabe. **Libera a afirmação:** o passo 5.5 do roadmap.

## 3.5 Qualquer afirmação de significância estatística — parcialmente endereçado

**Deixa de ser inteiramente vedado em 28/08/2026.** Os testes de `experimentos/teste_construcional.py` são os primeiros do projeto: permutação de rótulos de par, intervalo por reamostragem de conglomerado, correção de Holm sobre a família de seis condições, e teste t para a inclinação da reta de frequência.

**Pode ser afirmado**, com os valores tais como o relatório os traz, para as condições ali medidas — o que abrange os itens 1.13, 1.14, 1.15, 1.16 e 2.8.

**Continua vedado** para todo o restante. Nenhum teste foi executado sobre as medidas do corpus de áudio — rendimento por camada, confiança de transcrição, taxa de ocorrência de marcadores —, e as comparações entre Nordeste e Sudeste registradas na seção 2 permanecem descritivas.

**Qualificação obrigatória, a declarar junto de cada valor-p:** os 22 pares que definem a reta de calibração têm resíduo de média zero por construção, o que estreita a distribuição nula da permutação e torna o teste ligeiramente anticonservador. Um conjunto de validação separado do de ajuste seria preferível, e não foi constituído.

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
| Método | sustentada, e com contribuições próprias (itens 1.1, 1.2, 1.7, 1.8, 1.16) |
| **Resultados** | **deixa de estar vazia** em 28/08/2026, com os itens 1.13, 1.14 e 1.15 — um nulo com controle positivo, confundidor descontado e teste de significância |
| Ameaças à validade | madura, e mais desenvolvida que o usual |
| Conclusão | escrevível na chave do segundo caminho abaixo; não na do primeiro |

**Dois caminhos possíveis, não excludentes.**

O primeiro é o artigo pretendido: medição de viés dialetal implícito no BERTimbau. Exige instrumento corrigido e validado, corpus em volume suficiente para o Filtro 2, e a medição propriamente dita. É o de maior alcance e o mais distante.

O segundo é um **artigo de recurso e método**: o conjunto de pares mínimos para variação regional do português brasileiro, o protocolo de validação em dois filtros, o dimensionamento por requisito de detecção, e os achados sobre tokenização e sobre construção de corpus a partir de plataforma. Os precedentes que o projeto adota — CrowS-Pairs e French CrowS-Pairs — são exatamente dessa natureza, com a medição no modelo servindo de demonstração de uso. É alcançável com o que já existe, mais a validação por juízes, e constrói o terreno do primeiro.

A escolha é da equipe. Registre-se apenas que, no estado atual, o segundo caminho está muito mais próximo do que o primeiro.

**Atualização de 28/08/2026.** O teste construcional altera a relação entre os dois caminhos, e não apenas a distância a cada um.

O primeiro caminho deixa de estar apenas distante e passa a ter uma condição declarada: exige que alguma sinalização dialetal produza resposta no modelo, e quatro famílias já foram testadas sem que nenhuma produzisse. Prossegui-lo significa trocar de modelo ou de métrica — os caminhos 5.2 do roadmap —, e não acrescentar itens ao instrumento atual.

O segundo caminho, em contrapartida, ganhou material que não tinha. A seção de Resultados deixa de estar vazia: o nulo sobre quatro famílias, com controle positivo, confundidor de frequência descontado por calibração e teste de significância, é resultado publicável na chave de um artigo de método. Acrescentam-se as duas contribuições metodológicas novas — a calibração da resposta à frequência (1.14, revisado) e a unidade de replicação por par (1.16).

Há ainda uma terceira possibilidade, que não existia antes e que combina os dois: um artigo cuja pergunta seja **por que a sinalização implícita não produz resposta onde a explícita produz** (item 2.8). Depende inteiramente da confirmação de 2.8 em volume, e é a única linha em que o resultado sobre o modelo voltaria a ser a contribuição central.
