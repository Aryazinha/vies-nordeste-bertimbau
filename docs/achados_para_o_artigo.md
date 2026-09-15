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

**Procedência:** medição própria, `experimentos/selecionar_atributos.py`, resultado em `experimentos/resultados/tabelas/atributos_selecionados.md`. Reprodutível por terceiros.

**Qualificação obrigatória:** o repertório testado é amplo mas não exaustivo, e a seleção de itens de baixo prestígio partiu de ocupações de circulação corrente. A afirmação descreve o padrão nesse repertório.

### Consequência demonstrada, acrescentada em 29/08/2026

O item deixa de ser advertência metodológica e passa a ter **caso documentado**. No passo 5.5, uma medição de viés de valência produziu efeito aparentemente significativo — a condição de menção explícita à macrorregião apresentava viés de +0,1952, com sete de oito pares positivos e p ajustado de 0,0486 contra o grupo de referência de 26 pares — e de **0,0018** contra o grupo ampliado a 86 pares, em 14/09/2026. Restrita a análise aos atributos de **token único**, o efeito caiu para +0,0309, com três de oito pares positivos e p ajustado de 1,0000.

**A restrição aumentou o poder do teste em vez de reduzi-lo:** o controle positivo passou de +0,2352 para +0,4758, e seu p ajustado caiu de 0,0052 para 0,0004 com o grupo de 86 pares (de 0,0556, que não sobrevivia à correção, para 0,0013 com o de 26). Com menos atributos e mais poder, o efeito da condição regional evaporou enquanto o do controle cresceu — o que exclui a leitura de sinal perdido por ruído. A ampliação do grupo de referência torna o caso mais agudo, e não mais brando: o artefato passa a exibir significância forte na versão completa e continua a desaparecer por inteiro na restrita.

O mecanismo é identificável no próprio repertório: entre os atributos multi-token, os desfavoráveis fragmentam-se mais que os favoráveis — *burra* (2), *grosseira* (3), *ignorante* (2), *preguiçosa* (3), média de 2,5 tokens, contra *culta*, *educada*, *honesta* e *trabalhadora*, todos de 2.

**Formulação forte, e é a contribuição:** em português, uma medição de viés por pseudo-verossimilhança pode produzir efeito significativo inteiramente atribuível à assimetria de tokenização entre os atributos comparados. O mascaramento do alvo por inteiro, adotado neste projeto justamente para neutralizar isso, **é correção parcial e não bastou**. O controle exige balanceamento explícito da extensão em subtokens entre os polos do eixo medido, ou o emprego de AUL.

**Procedência:** `experimentos/analise_valencia.py`, relatório em `experimentos/resultados/relatorios/explicito.md`.

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

**Procedência:** medição própria, `experimentos/resultados/relatorios/molduras_alternativas.md`.

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

**Procedência:** inspeção individual de todas as ocorrências em 5,52 h de transcrição, `experimentos/resultados/relatorios/piloto_medicoes.md`.

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

**Procedência:** `experimentos/teste_sensibilidade.py`, resultado em `experimentos/resultados/relatorios/sensibilidade_guise.md`.

**Qualificação obrigatória:** cinco pares por condição, um modelo (BERTimbau Base), uma métrica (PLL sobre alvo mascarado), sem teste de significância. A afirmação deve ser formulada como ausência de efeito detectável nessas condições, e não como impossibilidade.

## 1.14 O efeito do bloco lexical é reproduzido por palavras raras não regionais

**Seção do artigo:** Resultados, e Ameaças à Validade.

Uma condição de controle com palavras raras **não regionais**, pareadas por frequência com os itens do instrumento — *chinfrim* (0,081 por milhão) para *arretado* (0,100), *combalido* (0,071) para *aperreado* (0,000) —, reproduz o efeito do bloco dialetal quase par a par: medianas de 2,80× contra 2,71× o piso. A reprodução impede a leitura dialetal do bloco lexical, e **esta é a parte do item que se sustenta**. Com o grupo de referência de 86 pares, as duas condições seguem indistinguíveis: resíduo de +0,074 no bloco lexical e de +0,070 no controle de raridade, e o bloco lexical não sobrevive à correção de Holm (p ajustado 0,084).

### Revisão de 14/09/2026: a frequência não é o mecanismo

As redações anteriores atribuíam a reprodução à frequência lexical — primeiro como efeito dominante, depois, com 22 pares, como efeito "real, positivo e modesto" (R² = 0,180). **Nenhuma das duas formas deve ser escrita.** Com o grupo de referência ampliado a 86 pares distintos, a inclinação de |Δ PLL| contra log₁₀ da razão de frequência é de 0,0073, com R² = 0,008 e p = 0,41; nos 61 pares acrescentados, isoladamente, é nula (p = 0,74), e a mediana de |Δ| não varia entre razões de 1× e mais de 600×. A inclinação anterior dependia de poucos pares: sem os cinco do controle de raridade, já não era significativa entre os 25 pares antigos (p = 0,13).

**Formulação sustentada:**

- um controle de palavras raras não regionais reproduz o efeito do bloco lexical, o que impede a leitura dialetal daquele bloco;
- a razão de frequência entre os itens trocados **não prevê** a diferença de escore no grupo de referência ampliado;
- a variação entre pares é dominada por fatores que a razão de frequência não captura, entre os quais a moldura do enunciado: nos pares acrescentados, a mediana de |Δ| por moldura vai de 0,086 a 0,262.

**Hipótese não testada, a declarar como tal:** os cinco itens do controle de raridade combinam raridade com registro marcado, arcaizante ou coloquial, e o efeito que reproduz o do bloco lexical pode ser de marcação de registro, e não de frequência. A hipótese é posterior aos dados.

**A consequência metodológica permanece, com outra justificativa.** O ruído no nível do par segue da ordem do efeito procurado — desvio-padrão de 0,0629 nos resíduos de calibração, contra mediana de 0,1539 —, de modo que *matched-guise probing* com métrica de verossimilhança exige muitos pares, grupo de referência amplo e estatística por conglomerado no nível do par. O que muda é o papel da reta: com inclinação praticamente nula, o resíduo equivale à diferença em relação à média do grupo de referência, e a calibração vale como **verificação** de que a frequência não confunde a comparação, e não como correção dela.

**Procedência:** `experimentos/teste_sensibilidade.py` para a reprodução; `experimentos/teste_explicito.py` para a revisão, com diagnóstico em `docs/pendencias.md` 2.9. As redações de 27 e 28/08/2026 estão no histórico do repositório.

## 1.15 Nenhuma das quatro famílias de sinalização dialetal implícita produz resposta detectável

**Seção do artigo:** Resultados.

Quatro famílias foram testadas contra o mesmo grupo de referência, e nenhuma apresenta resíduo que sobreviva à correção de multiplicidade:

| Família | Pares | Resíduo médio | Pares acima da reta | p | p Holm |
|---|---|---|---|---|---|
| morfossintática — imperativo e negação | 5 | −0,0763 | 0/5 | 0,9997 | 1,0000 |
| lexical — itens regionais | 5 | +0,0739 | 4/5 | 0,0140 | 0,0840 |
| feixe combinado | 5 | +0,0126 | 3/5 | 0,3145 | 0,9435 |
| **construcional** | **10** | **−0,0249** | **3/10** | **0,8885** | **1,0000** |

Valores com o grupo de referência de 86 pares não regionais distintos, de 14/09/2026. A família lexical é a mais próxima do limiar, e seu resíduo é indistinguível do controle de palavras raras não regionais, de +0,0699 — ver 1.14.

A família construcional foi acrescentada em 28/08/2026 para testar a única pista que a explicação por raridade não cobria, e é a mais informativa por dois motivos. Primeiro, seus itens são de frequência atestada — *lhe* de segunda pessoa, *tu* sem flexão, comitativo com *mais*, vocativos *menino* e *rapaz*, avaliativo *massa* —, de modo que a raridade não é explicação disponível. Segundo, a pista original não replicou: o vocativo *menino* contra *cara* apresenta resíduo de +0,0386, mas o vocativo *rapaz* contra o mesmo *cara* apresenta −0,0853, o maior resíduo negativo da condição. Mesma construção, mesmo termo de comparação, sinais opostos.

**O caso mais limpo é a negação pós-verbal.** Os pares *fui não* / *não fui* e *sei não* / *não sei* empregam exatamente as mesmas palavras em ordem diferente, com razão de frequência 1,0 por construção. O confundidor não é atenuado, é eliminado. Ambos apresentam resíduo negativo.

**Duas condições de interpretabilidade estão satisfeitas**, e sem elas o nulo não seria legível:

1. *A medição detecta o que existe.* O controle de conteúdo proposicional apresenta resíduo de +0,3422, com p = 0,0004 após correção de Holm, apesar de razão de frequência baixa (2,3×). É o controle positivo do próprio método de resíduo.
2. *O confundidor de frequência está verificado*, e não apenas declarado: sobre 86 pares não regionais, a razão de frequência não prevê a diferença de escore (1.14, revisão de 14/09/2026).

**Formulação correta:** o BERTimbau Base não exibe, sob pseudo-verossimilhança, resposta detectável à sinalização dialetal implícita, nas quatro famílias testadas. **Formulação incorreta:** o BERTimbau não distingue as variedades, ou não apresenta viés regional.

**Qualificação obrigatória:** um modelo, uma métrica, e cinco pares em três das quatro famílias. A afirmação é sobre ausência de efeito detectável nestas condições.

**Procedência:** `experimentos/teste_construcional.py`, relatório em `experimentos/resultados/relatorios/construcional.md`; valores vigentes em `experimentos/resultados/tabelas/explicito_tabelas.md`, com o grupo de referência de 86 pares.

## 1.16 A unidade de replicação em *matched-guise probing* é o par, não a medição

**Seção do artigo:** Método. Contribuição metodológica autônoma.

Um instrumento de *matched-guise* multiplica pares por molduras por atributos, e o número de medições cresce depressa: 28 medições por par neste desenho. As medições de um mesmo par compartilham o enunciado e não são independentes, de modo que tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza e produz significância espúria.

A consequência é verificável neste conjunto: com o piso e as medianas calculados sobre medições individuais, a condição de controle neutro aparece como 1,25× de si mesma quando confrontada com medianas de par. Ambos os números descrevem os mesmos dados.

Adotou-se, por isso, estatística por conglomerado — reamostragem de pares para o intervalo, permutação de rótulos de par para o valor-p, e correção de Holm para a família de condições confrontadas com a mesma calibração.

**Procedência:** medição própria. O ponto vale para qualquer trabalho do gênero, e a literatura consultada não o explicita.

## 1.17 O modelo responde à menção explícita de região; sem especificidade para o Nordeste acima de 0,08 na autoidentificação, com sinal pequeno e exploratório na menção em terceira pessoa

**Seção do artigo:** Resultados. Forma par com 1.15.

Três condições de menção explícita produzem resíduo acima do grupo de referência de 86 pares não regionais e **sobrevivem à correção de Holm** para as nove condições confrontadas com a mesma calibração. Valores com 20 frases por condição, de 15/09/2026:

| Condição | Pares | Razão med. | Resíduo médio | Acima da reta | p Holm |
|---|---|---|---|---|---|
| gentílico de estado — *pernambucano*, *baiana*, *cearense* | 20 | 3,4× | +0,1631 | 20/20 | **0,0004** |
| macrorregião — *Nordeste*, *nordestino* | 20 | 1,8× | +0,0871 | 16/20 | **0,0007** |
| menção em terceira pessoa — *O cliente é do Nordeste* | 20 | 5,3× | +0,0796 | 16/20 | **0,0007** |
| topônimo — *Ceará*, *Caruaru*, *Recife* | 20 | 4,0× | +0,0303 | 13/20 | 0,1328 |

### Controle de moldura, com regras de decisão registradas antes da medição

Os enunciados de gentílico e de macrorregião são quase todos de autoidentificação — *Sou baiano*, *Meu marido é nordestino* —, forma ausente do grupo de referência. Cada par recebeu um gêmeo com a mesma frase e o mesmo lado de comparação, trocado apenas o rótulo nordestino por rótulo equivalente do Sul. Para cada frase, D é a diferença de |Δ| entre o par de teste e o gêmeo. Com oito frases por condição, em 14/09/2026, a predição de especificidade não se confirmou; a medida foi estendida a 20 frases em 15/09/2026, com três regras registradas antes: especificidade detectada se p Holm < 0,05; efeito acima de 0,08 excluído se não detectada e o limite superior do IC 95% ficar abaixo de 0,08; inconclusivo nos demais casos.

| Condição | Frases | D médio | IC 95% | D > 0 | p Holm | Leitura |
|---|---|---|---|---|---|---|
| macrorregião | 20 | −0,0210 | −0,0704 a +0,0188 | 11/20 | 0,7922 | exclui D > 0,08 |
| gentílico de estado | 20 | +0,0147 | −0,0537 a +0,0852 | 11/20 | 0,6861 | inconclusivo |
| topônimo | 20 | +0,0108 | −0,0163 a +0,0383 | 12/20 | 0,6790 | exclui D > 0,08 |
| menção em terceira pessoa | 20 | +0,0262 | +0,0052 a +0,0446 | 18/20 | 0,0409 | especificidade detectada |

As três primeiras leituras coincidem com a expectativa registrada. Os gêmeos, que não mencionam o Nordeste, produzem |Δ| acima do grupo de referência em macrorregião (mediana 0,2087), gentílico (0,3181) e terceira pessoa (0,2053), contra 0,1539: a resposta a rótulo regional é, em larga medida, resposta à troca de rótulo, qualquer que seja a região.

**Formulação sustentada:** o BERTimbau Base responde à menção explícita de região acima de pares não regionais. Em enunciados de autoidentificação, não há resposta específica ao Nordeste acima de 0,08 em macrorregião e em topônimo, e o gentílico permanece sem resolução. Em menção em terceira pessoa, detecta-se resposta específica ao Nordeste **pequena** — D médio de +0,026, com limite superior de +0,045 —, a registrar como **exploratória**. O modelo não responde à sinalização dialetal implícita (1.15).

**Por que a especificidade em terceira pessoa é exploratória, e não resultado:** (a) a hipótese nasceu dos cinco pares originais daquela condição, e assim foi registrada antes da medição; (b) restrita às quinze frases acrescentadas em 15/09/2026, que não participaram de decisão anterior, a condição não sobrevive à correção (D +0,0217, 13/15 positivos, p Holm 0,2046); (c) o efeito fica inteiramente abaixo do limiar de 0,08 adotado como relevante.

**Formulações vedadas:**

- que o modelo responda especificamente ao Nordeste, ou à categoria *nordestino*, sem a distinção entre autoidentificação e terceira pessoa e sem as qualificações acima;
- que o modelo **não** distinga o Nordeste de outras regiões — o gentílico está sem resolução, e a terceira pessoa tem sinal;
- que o modelo apresente viés contra falantes nordestinos — a medida é de magnitude, e não de direção (1.19, 3.7).

**O contraste com 1.15 muda de natureza.** Deixa de ser "variedade indiciada contra categoria regional nomeada" e passa a ser "sinalização linguística, sem resposta, contra rótulo geográfico explícito, com resposta" — resposta que, na autoidentificação, não distingue o Nordeste de outra região acima de 0,08.

**Qualificação obrigatória:** 20 frases por condição, um modelo, uma métrica, e um único tipo de rótulo alternativo (Sul). O controle com rótulo da mesma região do lado de comparação foi tentado e resultou inconclusivo (`docs/pendencias.md` 2.11), de modo que não se separou resposta a qualquer rótulo de resposta a região distinta do Sudeste. O gentílico exigiria cerca de 42 frases pela sua dispersão, resolução adiada para fase posterior ao dataset v1. Em topônimo, parte das cidades é do interior e menos frequente que as capitais. O contraste de gentílico não é simétrico, pela inexistência de *sudestino* (1.18).

**Procedência:** `experimentos/teste_explicito.py` e `experimentos/analise_moldura.py`; tabelas em `experimentos/resultados/tabelas/explicito_tabelas.md` e `moldura_tabelas.md`. Registros prévios em `e852c5a` e `f7b1cdc` (oito frases) e `03d8571` (vinte frases); medição em `c145966`; detalhamento em `docs/pendencias.md` 2.10 e 2.12. Redações anteriores deste item estão no histórico do repositório.

## 1.17-A Rótulo de pessoa contra rótulo de lugar — exploratório, e não sustentado pelo controle de moldura

**Seção do artigo:** não deve ir a Resultados. Pode ir a Método, como exemplo de diferença aparente produzida pela moldura.

A predição registrada antes da medição de 5.4 era ordinal por granularidade do rótulo, e não se confirmou. A inspeção posterior sugeriu um corte entre enunciados que nomeiam **pessoa** e os que nomeiam **lugar**: sobre o resíduo, rótulo de pessoa +0,1490, doze de doze acima da reta, contra +0,0249 de lugar, com p = 0,0004 para a diferença.

**O controle de moldura desfaz a leitura.** Sobre D — a diferença entre o par nordestino e o gêmeo do Sul na mesma frase —, rótulo de pessoa rende +0,0145 e rótulo de lugar +0,0139. A diferença entre os agrupamentos desaparece quando a frase é mantida constante. É compatível com efeito de moldura: frases que descrevem a pessoa deslocam a probabilidade de atributos de pessoa, qualquer que seja a região nomeada.

**Não deve ser escrita** a leitura substantiva antes registrada aqui — de que *nordestino* carrega representação social e *Recife* não. **Pode ser escrito**, em Método e com a declaração de que a hipótese foi posterior aos dados, que uma diferença entre categorias de rótulo aparentemente forte (p = 0,0004) se mostrou atribuível à forma dos enunciados quando controlada por pareamento.

## 1.18 O português não dispõe de gentílico corrente para o Sudeste

**Seção do artigo:** Método, e Ameaças à Validade.

*Sudestino* apresenta frequência de 0,015 por milhão contra 4,27 de *nordestino* — razão de 285 vezes. O contraste simétrico de gentílico de macrorregião é, por isso, impossível de construir, e os controles empregados foram gentílicos de outra macrorregião (*sulista*) ou de estados do Sudeste (*mineiro*, *carioca*, *paulista*, *paulistano*, *fluminense*).

O fato é dado, e não apenas obstáculo de desenho: a categoria "nordestino" existe na língua como rótulo de pessoa de um modo que "sudestino" não existe. Deve ser reportado como limitação. A leitura que o tomava também como evidência de que a primeira funciona como categoria social e a segunda como coordenada geográfica apoiava-se em 1.17-A, que o controle de moldura desfez em 14/09/2026, e não deve ser escrita.

**Procedência:** medição própria com `wordfreq`, registrada em `experimentos/teste_explicito.py`.

**Qualificação obrigatória:** a fonte de frequência não estratifica por variedade nem separa português brasileiro de europeu.

## 1.19 A resposta do modelo à menção explícita não é depreciativa de forma que sobreviva ao controle de tokenização — com sinal exploratório em rótulos de pessoa

**Seção do artigo:** Resultados. Fecha o par com 1.17 e é a terceira parte da conclusão.

O item 1.17 estabelece que o modelo responde à menção explícita da região. A medida ali é de **magnitude**, em valor absoluto, e não diz se a resposta é desfavorável. A medida com sinal é executada sobre as mesmas medições, em dois eixos separados; os valores abaixo são de 15/09/2026, com 20 frases por condição.

**Escore de viés por par:** média de Δ PLL nos atributos desfavoráveis menos média nos favoráveis, positiva quando o guise nordestino torna os desfavoráveis relativamente mais prováveis. É a definição operacional do CrowS-Pairs.

**Resultado, eixo de caráter, com controle do artefato de segmentação:**

| Condição | Viés (7+7 atributos) | Viés (3+3, token único) |
|---|---|---|
| menção explícita — macrorregião | +0,2119 (p Holm 0,0004) | +0,0945 (p 0,058; Holm 0,4049) |
| menção explícita — terceira pessoa | +0,1571 (p Holm 0,0020) | +0,0684 (Holm 0,7977) |
| menção explícita — gentílico de estado | +0,0562 (Holm 0,5292) | +0,0600 (Holm 0,7977) |
| menção explícita — topônimo | +0,0591 (Holm 0,3591) | +0,0187 (Holm 1,0000) |
| **controle de conteúdo — positivo** | +0,2352 (p Holm 0,0045) | **+0,4758 (p Holm 0,0004)** |

**Os valores significativos da versão completa não são resultado.** A versão completa mistura atributos de extensões diferentes, e os desfavoráveis fragmentam-se mais que os favoráveis — o artefato de 1.1. Com mais frases, o artefato ganha mais significância, e continua a não sobreviver à versão restrita.

**Três condições de interpretabilidade estão satisfeitas**, e sem elas o nulo não seria legível:

1. *O grupo de referência é adequado.* São 86 pares não regionais distintos, com viés médio de +0,0072 no eixo de caráter, e não os cinco do controle neutro empregados na primeira versão da análise — erro de desenho corrigido, cujo sintoma foi o controle positivo não sobreviver à correção apesar das maiores magnitudes brutas.
2. *A verificação de sanidade passa.* O controle neutro, testado contra o grupo do qual faz parte, resulta não significativo em todos os eixos (p de 0,32 no caráter, 0,50 no restrito, 0,32 na ocupação).
3. *O teste tem poder, e o tem mais na versão restrita.* O controle positivo sobrevive à correção de Holm nas duas versões, a 0,0045 e a 0,0004.

**Formulação sustentada:** nas condições testadas, nenhuma condição de menção explícita apresenta viés de valência no eixo de caráter que sobreviva à correção de multiplicidade na versão controlada da tokenização. Os efeitos significativos da versão completa são atribuíveis à assimetria de tokenização (1.1).

### Sinal a declarar, sem estatuto confirmatório

Duas observações acompanham obrigatoriamente a formulação acima, porque apontam na direção oposta à de um nulo limpo:

- **As estimativas subiram com o volume.** Na versão restrita, a macrorregião passou de +0,0309, com oito frases, a +0,0945, com vinte, e fica a p bruto 0,058. Com 20 frases por condição, a análise de direção só exclui vieses a partir de cerca de 0,10 (`docs/pendencias.md` 2.11), e o valor observado está dentro dessa margem.
- **Há sinal em rótulos de pessoa.** No reagrupamento exploratório pessoa/lugar, restrito a token único, rótulos de pessoa (*nordestino*, *baiano*, *cearense*) rendem +0,1226, com p = 0,0057, contra −0,0071 de rótulos de lugar. O reagrupamento é posterior aos dados, e o mesmo corte desapareceu na medida de magnitude com o controle de moldura (1.17-A); não há, portanto, base para lê-lo como resultado. É, contudo, o primeiro sinal de direção a aparecer na versão controlada da tokenização.

A confirmação desse sinal exige mais frases na análise de direção e foi adiada para fase posterior ao dataset v1 (`docs/pendencias.md` 2.12).

**Formulações vedadas:**

- que o modelo não apresente viés regional, ou que a resposta não seja depreciativa — um instrumento que não detecta não demonstra ausência, a análise de direção tem resolução de cerca de 0,10, e há sinal exploratório declarado acima;
- que o modelo seja depreciativo com rótulos de pessoa nordestinos — o sinal é exploratório;
- citar qualquer valor significativo da versão completa como resultado;
- citar qualquer valor do eixo de prestígio ocupacional, que permanece sem medição válida (1.20, 3.7).

**Qualificação obrigatória:** 20 frases por condição, seis atributos na versão restrita, um modelo, uma métrica. A classificação de valência é do projeto e não foi validada por juízes.

**Procedência:** `experimentos/analise_valencia.py`; tabela em `experimentos/resultados/tabelas/valencia_tabelas.md`; medição em `c145966`. A redação anterior, com oito frases por condição, está no histórico do repositório.

## 1.20 O eixo de prestígio ocupacional não é mensurável por PLL neste modelo

**Seção do artigo:** Método, e Ameaças à Validade. Decorre de 1.1 e é sua consequência mais dura.

A verificação do artefato de segmentação, executável no eixo de caráter, **não é executável no de ocupação**:

| Prestígio | Atributos | Tokens |
|---|---|---|
| alto | *advogado*, *juiz*, *médico*, *professor* | 1, 1, 1, 1 |
| baixo | *empregada* / *lavrador*, *pedreiro* / *faxineiro* | 1 / 2, 2 / 4 |

Restringir a análise a atributos de token único deixaria quatro ocupações de alto prestígio contra **uma** de baixo, e essa uma — *empregada* — é também a única do feminino, o que substituiria o confundidor de segmentação pelo de gênero.

A impossibilidade não é acidente deste conjunto de itens: é o item 1.1 operando. O léxico ocupacional de baixo prestígio não integra o vocabulário do BERTimbau como palavra inteira, e não há do que restringir.

**Consequência prática, e citável:** medir viés de prestígio ocupacional em português por pseudo-verossimilhança sobre este modelo exige AUL, e não PLL. Não se trata de preferência entre métricas, e sim de condição de possibilidade — o que confirma, por via independente, a conclusão já registrada em 1.1.

**Estado no projeto:** o eixo permanece sem medição válida. O valor de −0,2706 observado na condição de gentílico, que significaria ocupações de alto prestígio tornando-se mais prováveis sob o guise nordestino, **não deve ser citado em nenhuma direção**.

# 2. CONDICIONAL — depende de verificação nomeada

## 2.1 A transcrição automática não penaliza a fala nordestina

**Estado:** indício consistente em dois lotes; falta o WER.
**Medido, 52 arquivos e 45 mil palavras:** Nordeste 0,944, Sudeste 0,939, diferença de +0,006 em favor do Nordeste. Por estado, entre 0,929 (RJ) e 0,948 (PE e SP).
**Estabilidade:** no primeiro lote, com 17 arquivos, a dispersão entre estados ia de 0,898 a 0,975; com o triplo do material reduziu-se a 0,929–0,948. A variação anterior era ruído de amostra pequena, e a convergência reforça a leitura em vez de enfraquecê-la.
**Libera a afirmação:** WER contra transcrição humana de referência. Confiança mede certeza do modelo, não acerto, e nenhuma quantidade de confiança substitui a comparação com referência.
**Se confirmado:** remove confundidor previsto na Parte 3 de `docs/protocolo.md`, e constitui resultado secundário publicável.
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

## 2.5 A sensibilidade do modelo concentra-se no léxico — SUPERADO

**Superado em 28/08/2026 por 1.14 e 1.15, e não deve ser citado.** A medição por divergência de Jensen-Shannon, sobre doze itens e sem controle de frequência, foi substituída por |Δ PLL| com calibração explícita da resposta à frequência e estatística no nível do par. A conclusão mudou de forma: o efeito do bloco lexical não é sensibilidade ao dialeto, e sim à raridade das palavras.

**Estado original, conservado como histórico:** medido em conjunto pequeno, sem teste estatístico.
**Medido:** divergência de Jensen-Shannon mediana de 0,0144 bits no bloco lexical contra 0,0023 no morfossintático, tendo 0,0963 como referência de conteúdo proposicional distinto.
**Libera a afirmação:** conjunto de itens em volume adequado e teste estatístico. Doze itens não sustentam inferência.
**Se confirmado:** exige reposicionamento do artigo, pois um efeito de origem lexical é atacável como efeito de frequência, e não de dialeto. É a objeção mais previsível em revisão.

## 2.8 O modelo responde à menção explícita da região — ENCERRADO, promovido a 1.17

**Encerrado em 29/08/2026.** Este item era condicional a volume, e o volume foi produzido pelo passo 5.4 do roadmap: vinte e quatro pares novos, em três níveis de granularidade do rótulo. A condição liberadora foi cumprida e o achado passa a **SUSTENTADO**, no item 1.17.

**Uma parte da leitura original não sobreviveu, e o registro importa.** O item afirmava que a estrutura interna era de granularidade — região como categoria acima, nomes de estado próximos de zero. Com oito pares por nível, o corte revelou-se outro: entre **rótulo de pessoa** e **rótulo de lugar**, distinção que atravessa a condição de macrorregião e que os cinco pares originais não permitiam ver. Ver 1.17-A, e a declaração de estatuto que o acompanha. Em 14/09/2026, esse segundo corte também não sobreviveu ao controle de moldura.

**Conservado como histórico**, e não removido, porque a previsão registrada antes da medição é parte do que torna 1.17 confirmatório e 1.17-A exploratório.

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

**Continua vedado** afirmar que o BERTimbau enviesa, ou que não enviesa, contra fala nordestina. O que se estabeleceu é que os marcadores morfossintáticos do instrumento não produzem resposta detectável, e que o efeito dos marcadores lexicais é reproduzido por palavras raras não regionais (1.14). Não havendo resposta ao guise, não há viés a medir por esse caminho — o que é afirmação sobre o método, e não sobre a existência do preconceito.

**Formulação correta:** não foi possível detectar, com este desenho, resposta do modelo à sinalização dialetal. **Formulação incorreta:** o BERTimbau não apresenta viés regional.

**Atualização de 28/08/2026, segunda requalificação.** O teste construcional acrescentou a quarta família de marcadores, descontou o confundidor de frequência por calibração explícita e executou os primeiros testes de significância do projeto. O que era "não foi possível detectar resposta" passa a ser afirmação com controle positivo e valor-p, registrada em 1.15.

**Atualização de 29/08/2026, terceira requalificação, e ela altera a premissa das duas anteriores.**

As requalificações acima repousavam sobre "não havendo resposta ao guise, não há viés a medir". A premissa deixou de valer: o passo 5.4 estabeleceu que **existe** resposta à menção explícita da região, sobrevivente à correção de multiplicidade (item 1.17). O que não existe é resposta à sinalização **implícita**.

A vedação, portanto, muda de fundamento — e deixa de ser sobre ausência de resposta para ser sobre ausência de **direção medida**.

**Segue vedado, agora por outra razão:** afirmar que o BERTimbau deprecia falantes nordestinos, ou que não os deprecia. Toda a medição do projeto emprega |Δ| em valor absoluto, e a análise com sinal é inconclusiva por subdimensionamento. O detalhamento está em 3.7, que é hoje a vedação operante sobre este ponto.

**Formulação correta, em três partes que não devem ser separadas:**
1. O BERTimbau Base **não** exibe resposta detectável à sinalização dialetal implícita, nas quatro famílias testadas (1.15).
2. O BERTimbau Base **exibe** resposta à menção explícita de região em enunciados sobre a pessoa, acima do grupo de referência não regional, sem especificidade detectável para o Nordeste (1.17).
3. **Não se sabe** se essa resposta é depreciativa: a medida é de magnitude, e a de direção não tem poder estatístico (3.7).

**Formulação incorreta, e a mais tentadora:** que o modelo apresente, ou deixe de apresentar, viés regional. Distinguir não é depreciar.

O instrumento continua não validado por juízes, e o conjunto de itens continua aberto. O que o material autoriza é uma seção de Resultados sobre **a viabilidade do desenho e sobre o contraste entre sinalização implícita e explícita**, e não sobre a magnitude de um viés.

## 3.2 O índice de 94% de imperativo indicativo no Rio de Janeiro

Registrado em revisão anterior do projeto e **não confirmado por nenhuma fonte** consultada. Não deve ser citado enquanto a origem não for localizada. O único contraste verificado entre variedades é o de Figuereido (2025), entre cidades do interior: Campinas-SP 81% contra Feira de Santana-BA 47%.

## 3.3 Que os marcadores dialetais do instrumento estejam validados

Nenhum item passou pelo Filtro 1, de juízes falantes nativos, nem pelo Filtro 2 em volume suficiente. Os itens são candidatos, e o texto deve tratá-los como tais.

## 3.4 Balanceamento de frequência lexical entre condições — parcialmente endereçado

**Deixa de ser inteiramente vedado.** A frequência dos itens lexicais foi medida em 28/08/2026, com resultado registrado em `experimentos/resultados/relatorios/piloto_medicoes.md`, adendo B.

**Pode ser afirmado:** as listas do Bloco B não eram comparáveis em frequência — de uma a três ordens de grandeza de distância, com dois itens nordestinos ausentes da fonte —, e o desequilíbrio é de dupla natureza: itens nordestinos de circulação restrita contra itens sudestinos de circulação nacional. Declarar como limitação identificada e corrigida, não como controle que o desenho sempre teve.

**Continua vedado:** afirmar que o instrumento final está balanceado, o que depende da reformulação do bloco.

**Qualificação obrigatória:** a fonte de frequência não estratifica por variedade nem separa português brasileiro de europeu. Item regionalmente restrito tem frequência nacional baixa por construção, de modo que a medida compara itens entre si e não caracteriza uso regional.

## 3.7 Que a resposta do modelo à região seja preconceituosa — requalificado

**Aberto em 29/08/2026 e requalificado no mesmo dia, depois de o passo 5.5 responder à pergunta.** A redação original vedava qualquer leitura de direção por subdimensionamento da análise. O subdimensionamento era erro de desenho — grupo de referência de cinco pares em vez de vinte e seis — e foi corrigido.

**Deixa de ser vedado:** afirmar que, nas condições testadas e no eixo de caráter, a resposta do modelo à menção explícita **não se organiza por valência**. É o item 1.19, com controle positivo sobrevivente à correção e artefato de segmentação controlado.

**Continua vedado, e sem atenuação:**

- Afirmar que o BERTimbau **não apresenta viés regional**. Um instrumento que não detecta não demonstra ausência. O que se mostrou é que este instrumento, neste modelo, nesta métrica e neste repertório de atributos, não detecta.
- Citar qualquer valor do eixo de **prestígio ocupacional**, em qualquer direção, inclusive o −0,2706 da condição de gentílico. Aquele eixo não tem medição válida por impossibilidade instrumental — ver 1.20.
- Citar o viés de +0,1952 da condição de macrorregião como resultado. Ele não sobrevive ao controle de tokenização, e sua história pertence a 1.1, não a Resultados.

**Formulação correta, em três partes que não devem ser separadas:** o modelo não responde à sinalização dialetal implícita (1.15); responde à menção explícita de região em enunciados sobre a pessoa, sem especificidade detectável para o Nordeste (1.17); e essa resposta não é depreciativa de forma detectável no eixo de caráter (1.19), permanecendo o eixo ocupacional sem medição (1.20).

**Libera afirmação mais forte:** medição do eixo ocupacional por AUL, e validação da classificação de valência por juízes.

## 3.5 Qualquer afirmação de significância estatística — parcialmente endereçado

**Deixa de ser inteiramente vedado em 28/08/2026.** Os testes de `experimentos/teste_construcional.py` são os primeiros do projeto: permutação de rótulos de par, intervalo por reamostragem de conglomerado, correção de Holm sobre a família de seis condições, e teste t para a inclinação da reta de frequência.

**Pode ser afirmado**, com os valores tais como o relatório os traz, para as condições ali medidas — o que abrange os itens 1.13, 1.14, 1.15, 1.16, 1.17 e 1.18. O passo 5.4, de 29/08/2026, estendeu a mesma maquinaria ao conjunto de menção explícita, com a calibração passando a 26 pares. Em 14/09/2026 o grupo de referência foi ampliado a 86 pares distintos e todos os valores foram regerados; os vigentes são os de `experimentos/resultados/tabelas/explicito_tabelas.md` e `valencia_tabelas.md`.

**A análise de direção é abrangida, com a ressalva de 1.1.** A redação anterior deste parágrafo a excluía por falta de poder. O controle positivo passou a sobreviver à correção no eixo de caráter restrito a token único em 29/08/2026, e também no completo com o grupo de 86 pares. Um valor significativo na versão completa do eixo de caráter não sustenta afirmação sem a verificação por token único, que é o que desfaz o da macrorregião. O eixo ocupacional segue fora. Ver 1.19 e 3.7.

**Continua vedado** para todo o restante. Nenhum teste foi executado sobre as medidas do corpus de áudio — rendimento por camada, confiança de transcrição, taxa de ocorrência de marcadores —, e as comparações entre Nordeste e Sudeste registradas na seção 2 permanecem descritivas.

**Qualificação obrigatória, a declarar junto de cada valor-p:** os pares que definem a reta de calibração — 22 no passo 5.1, 26 no 5.4, 86 desde 14/09/2026 — têm resíduo de média zero por construção, o que estreita a distribuição nula da permutação e torna o teste ligeiramente anticonservador. Um conjunto de validação separado do de ajuste seria preferível, e não foi constituído.

## 3.6 Que a composição do brWaC explique o viés observado

Não há viés observado, e a composição do corpus não é auditável. A relação permanece hipótese de mecanismo.

---

# 4. CADERNO — pertence ao repositório, não ao texto

Defeitos identificados e corrigidos durante o desenvolvimento: falha silenciosa que reportava download bem-sucedido sem arquivo em disco; aceitação de URL de canal onde se esperava vídeo; caminhos de dados relativos ao diretório de trabalho; incompatibilidade com a API nova do `pyannote`; dependência de versão do `yt-dlp` e de runtime de JavaScript; consulta de frequência sobre forma sem diacrítico; piso e medianas calculados sobre unidades de replicação diferentes; script de medição gravando tabela no caminho do relatório interpretado.

Acrescente-se, de 29/08/2026, o campo `duracao_s`, que registrava a duração do vídeo de origem e não a do áudio coletado, de modo que somá-lo devolvia 11,43 h contra as 5,52 h reais do corpus. Corrigido pelo campo `duracao_coletada_s`. **Este merece nota em apêndice, e não apenas no caderno:** o conjunto de dados será publicado, e um consumidor que somasse o campo antigo obteria o dobro do corpus sem receber erro. A distinção entre duração de origem e duração coletada é requisito de qualquer corpus construído por recorte de material mais longo.

Pertencem à documentação de reprodutibilidade. Uma exceção possível: o bloqueio de downloads originados de datacenter, que afeta qualquer tentativa de replicação em ambiente de nuvem e justifica nota em apêndice de reprodutibilidade.

---

# 5. Situação do artigo — transferida para o roadmap

**Movida em 29/08/2026 para `docs/roadmap.md`.** Esta seção fazia planejamento — estado de cada seção do texto submetido e escolha entre caminhos possíveis —, que é função do plano canônico e não do filtro editorial. Manter as duas coisas no mesmo arquivo produzia contradição sempre que uma delas era atualizada sozinha.

**Este documento faz uma coisa só:** dizer o que pode e o que não pode ser escrito, e sob que condição. O que fazer em seguida está no roadmap; o que não pode ser esquecido, em `docs/pendencias.md`.
