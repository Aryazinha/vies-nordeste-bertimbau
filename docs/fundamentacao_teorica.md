# Fundamentação Teórica

**Projeto:** Investigação de vieses sociolinguísticos no BERTimbau — variedades do Nordeste (PB, PE, CE, BA) frente a um grupo de controle do Sudeste (SP, RJ)

**Natureza do documento:** revisão de literatura e justificativa metodológica. Serve de base para as seções de fundamentação teórica e de trabalhos relacionados do artigo. As referências completas encontram-se em `docs/referencias.bib`; as decisões operacionais derivadas destas seções estão registradas em `CLAUDE.md` (protocolo) e em `docs/pares_minimos_v1.md` (instrumento de sondagem).

**Convenção de verificação.** Cada afirmação de terceiros neste documento recebe uma marca de procedência: *fonte verificada* indica que o texto integral foi consultado; *fonte secundária* indica que o dado provém de citação em outro trabalho ou de resumo publicado, não do texto original. Nenhum dado marcado como secundário deve ser levado ao artigo sem conferência prévia contra a fonte primária.

| Revisão | Data | Alterações |
|---|---|---|
| v1.0 | 05/08/2026 | Redação inicial das seções 1.1 a 1.3. |
| v1.1 | 05/08/2026 | Inclusão das subseções 1.2.1 (dados Cetic.br), 1.2.2 (Bagno), 1.2.3 (fontes ALiB) e 1.3.4 (trabalho relacionado). |
| v1.2 | 27/08/2026 | Conversão para registro acadêmico formal. Fechamento da pendência de cobertura dialetológica de Ceará e Bahia (subseção 1.2.3). Nova subseção 1.2.4, sobre marcadores morfossintáticos com manifestação ortográfica, com dados verificados sobre imperativo e negação. Ampliação da subseção 1.3.4 a partir da leitura integral de Melo e Souza (2026). Criação de `docs/referencias.bib`. |

---

# PARTE 1 — FUNDAMENTAÇÃO TEÓRICA

## 1.1 BERTimbau: origem, arquitetura e treinamento

**Referência primária.** Souza, Nogueira e Lotufo (2020), *BERTimbau: Pretrained BERT Models for Brazilian Portuguese*, BRACIS 2020, LNCS 12319, Springer, p. 403–417. DOI: [10.1007/978-3-030-61377-8_28](https://doi.org/10.1007/978-3-030-61377-8_28). Repositório oficial: https://github.com/neuralmind-ai/portuguese-bert

O trabalho apresenta modelos BERT (Devlin et al., 2019) treinados especificamente para o português brasileiro, em duas variantes: *Base* (110 milhões de parâmetros, 12 camadas) e *Large* (335 milhões de parâmetros, 24 camadas), ambas na configuração *cased*. O objetivo de treinamento é o *Masked Language Modeling* (MLM) com *whole-word masking*: quando um subtoken de uma palavra é mascarado, todos os subtokens da mesma palavra também o são, o que elimina atalhos triviais de predição e força representações semânticas mais robustas. O treinamento estendeu-se por um milhão de passos, e a avaliação cobriu três tarefas — similaridade textual semântica e inferência textual (ASSIN2) e reconhecimento de entidades nomeadas (MiniHAREM) —, com desempenho superior ao do BERT multilíngue em todas.

O ponto de maior consequência para este projeto é a composição do corpus de pré-treinamento: **o brWaC é a única fonte** (seção 1.2). Parte da literatura posterior descreve o BERTimbau como treinado sobre uma combinação de brWaC, Wikipédia e corpus jornalístico; tanto o artigo original quanto o repositório oficial contradizem essa descrição.

**Implicação metodológica.** Não havendo outro corpus que dilua a distribuição do brWaC, qualquer viés geográfico ou sociolinguístico presente em sua composição é herdado pelo modelo de forma quase direta. Esse é o encadeamento causal que sustenta a hipótese central do estudo, e deve ser explicitado tanto na fundamentação quanto na seção de ameaças à validade do artigo.

---

## 1.2 O corpus brWaC: composição e questão geográfica

**Referência primária.** Wagner Filho, Wilkens, Idiart e Villavicencio (2018), *The brWaC Corpus: A New Open Resource for Brazilian Portuguese*, LREC 2018. https://aclanthology.org/L18-1686/

**Ficha técnica.** O corpus reúne entre 2,68 e 2,7 bilhões de tokens, distribuídos em 3,53 milhões de documentos, com 5,79 milhões de *types*. Foi construído pela metodologia WaCky (Baroni et al., 2009), em quatro etapas: identificação de URLs semente; rastreamento e limpeza pós-coleta; remoção de conteúdo duplicado; e anotação linguística com etiquetagem morfossintática e análise sintática pelo *parser* Palavras. Mais de 60 milhões de páginas foram rastreadas, das quais 3,5 milhões foram retidas — regras estritas de filtragem preservaram cerca de 5,6% das sementes originais. Cento e vinte mil sítios distintos contribuíram conteúdo, número que os autores empregam como argumento de diversidade de domínio. O trabalho é conduzido pela UFRGS, com colaboração da UCLouvain e da University of Essex. A licença restringe o uso a fins acadêmicos e de pesquisa, o que é pertinente à seção de ética do artigo.

**Ausência de estratificação geográfica documentada.** O artigo original não publica quebra estatística por região ou estado de origem dos sítios coletados. A diversidade reportada é de domínio temático — notícias, blogues, fóruns, sítios institucionais —, não de procedência geográfica ou de variedade dialetal. Essa ausência é, em si, relevante para o argumento do projeto: é precisamente a lacuna que a sondagem comportamental do modelo torna investigável.

Tendo o corpus sido coletado por rastreamento de domínios `.br` sem estratificação regional, dois mecanismos indiretos, ambos documentados na literatura, explicam por que a distribuição textual resultante tende a favorecer o eixo Sul-Sudeste:

1. **Desigualdade regional de acesso à internet e de produção de conteúdo digital**, historicamente concentrada no Sul e no Sudeste. Trata-se de fator socioeconômico e de infraestrutura, não linguístico, mas com efeito direto sobre quais variedades do português chegam a ser textualizadas na web. Os dados quantitativos constam da seção 1.2.1.
2. **Estigmatização do falar nordestino em contextos formais e escritos.** Falantes nordestinos tendem a produzir texto escrito formal — o gênero majoritariamente capturado pelo rastreamento de sítios institucionais e jornalísticos — em variedades mais próximas da norma padrão, o que apaga superficialmente os traços dialetais salientes. O fenômeno é discutido, entre outros, em *Português nordestino: para além das capitais* (2021), que trata da estigmatização do falar nordestino migrante no Sudeste e da hibridização dialetal decorrente do movimento de retorno (https://www.researchgate.net/publication/361462317). O enquadramento clássico brasileiro do fenômeno é o de Bagno (1999), tratado na seção 1.2.2.

**Recomendação de enquadramento.** A concentração Sul-Sudeste do brWaC deve ser apresentada no artigo como **hipótese de mecanismo, plausível por inferência**, sustentada por três apoios — a ausência de estratificação geográfica no desenho do corpus, os dados demográficos de acesso à internet por região e a literatura sociolinguística sobre estigma dialetal — e nunca como fato quantificado pelos autores do corpus. Essa formulação é mais defensável em revisão por pares do que a alegação de um viés "documentado" que o artigo original não sustenta.

**Limitação epistemológica a declarar.** O brWaC não expõe publicamente metadados de geolocalização por documento, ao menos nas versões amplamente distribuídas (`UFRGS/brwac` e `dominguesm/brwac` no Hugging Face). Não é possível, portanto, auditar diretamente a proporção de conteúdo por variedade regional na fonte de treinamento. A única via disponível é comportamental e indireta — a sondagem do modelo já treinado —, e o artigo deve declarar explicitamente que infere viés a partir do comportamento do modelo, não da auditoria do corpus.

### 1.2.1 Acesso e produção de conteúdo digital por região

**Fonte.** TIC Domicílios 2024, Cetic.br/NIC.br, divulgada em 31/10/2024, vigésima edição da série histórica. https://cetic.br/pt/pesquisa/domicilios/ — *fonte secundária* (dados obtidos de divulgação da pesquisa, não do microdado).

Dos 29 milhões de brasileiros que não usam internet, 21 milhões concentram-se no Sudeste (12 milhões) e no Nordeste (8 milhões); por serem as duas regiões mais populosas, os números absolutos exigem essa ressalva de leitura.

O dado mais forte para o argumento do projeto não é o de presença, mas o de **qualidade** de acesso. O indicador de conectividade significativa do Cetic.br — que pondera custo, velocidade, presença de banda larga fixa e acesso por múltiplos dispositivos — aponta que apenas 22% dos brasileiros com dez anos ou mais dispõem de condições satisfatórias de conectividade. A desagregação regional é acentuada: 33% no Sul contra 11% no Nordeste.

Quanto à **produção** de conteúdo, que é o proxy mais próximo da composição de um corpus como o brWaC, a proporção de usuários que publicaram conteúdo próprio passou de 31% em 2021 para 43% em 2022; historicamente, porém, o compartilhamento de conteúdo de terceiros supera a criação própria por ampla margem — em 2017, 73% contra 37%. Um indicador indireto de precariedade de acesso, o compartilhamento de conexão com vizinhos, é mais frequente no Norte (21%) e no Nordeste (22%) que nas demais regiões.

**Ressalva.** São dados de acesso e uso de internet em geral, não auditoria da composição do brWaC. Devem sustentar a hipótese de mecanismo causal, jamais serem apresentados como estatísticas do corpus.

### 1.2.2 Preconceito linguístico: o enquadramento brasileiro

**Referência.** Bagno, M. (1999), *Preconceito Linguístico: o que é, como se faz*, São Paulo, Edições Loyola.

Marcos Bagno, professor da Universidade de Brasília e doutor em Filologia e Língua Portuguesa pela USP, dedica-se à educação linguística e ao impacto da sociolinguística sobre o ensino de português no Brasil. A obra é referência fundacional da divulgação científica sobre preconceito linguístico no país.

O primeiro capítulo, "A mitologia do preconceito linguístico", desconstrói dois mitos diretamente pertinentes ao projeto: o da homogeneidade do português brasileiro — cuja negação da heterogeneidade dialetal constitui a base ideológica do preconceito linguístico — e o de que "o brasileiro não sabe português", contraposto ao português europeu, quando toda língua viva é heterogênea, inclusive a de Portugal.

**Uso no artigo.** Bagno (1999) fornece o enquadramento sociológico e ideológico brasileiro do fenômeno; Hofmann et al. (2024), tratado na seção 1.3.3, fornece o paradigma experimental computacional. As duas referências são complementares, não substitutas.

### 1.2.3 Fontes dialetológicas primárias

O Projeto Atlas Linguístico do Brasil (ALiB), sediado na UFBA desde 1996, orienta-se pela Dialetologia Pluridimensional, contemplando variação diatópica, diastrática, diagenérica e diageracional. Dele e de sua tradição derivam as fontes primárias adotadas pelo projeto.

**a) Realização de /t,d/ diante de /i/ no Nordeste brasileiro.** Estudo vinculado ao ALiB, sediado na UEFS/UFBA, sobre a palatalização de /t,d/ diante de /i/ — a alternância entre africada [tʃ, dʒ] e dental [t, d] em itens como *tia* e *dia*. O corpus abrange 78 localidades nordestinas e 348 informantes (72 nas nove capitais, 276 no interior), estratificados por sexo, duas faixas etárias (18 a 30 e 50 a 65 anos) e, nas capitais, dois níveis de escolaridade. Disponível em http://www.mel.uefs.br/modules/conteudo/conteudo.php?conteudo=67 — *fonte secundária*; o sítio responde apenas por HTTP e não pôde ser recuperado na verificação de 27/08/2026.

Trata-se do traço fonético mais robusto disponível para o recorte do projeto: é isoglossa documentada, com metodologia de amostragem transparente e réplica em múltiplos pontos do Nordeste. Por ser fenômeno fonético, **não se manifesta na ortografia** e, portanto, é usado exclusivamente na validação por áudio, nunca no instrumento de texto (ver seção 1.2.4 e `docs/pares_minimos_v1.md`).

**b) Atlas Linguístico de Pernambuco (ALiPE).** Sá, E. J. de. Tese de doutorado em Letras, Universidade Federal da Paraíba. https://alib.ufba.br/atlas-linguistico-de-pernambuco-alipe — 20 pontos de inquérito, 84 informantes segundo os critérios de Cardoso (2010), 105 cartas linguísticas, sendo 50 fonéticas, 47 semântico-lexicais e 8 morfossintáticas.

**c) Atlas Linguístico da Paraíba.** Aragão, M. do S.; Menezes, C. P. B. de (1984), Brasília, UFPB/CNPq.

**d) Atlas Linguístico do Estado do Ceará (ALECE).** Coordenação geral de José Rogério Fontenele Bessa. Fortaleza, Edições UFC, 2010, dois volumes. Iniciado em 1978 e publicado em 2010. O primeiro volume cobre antecedentes históricos, orientação teórica e metodologia; o segundo apresenta 256 cartogramas com dados lexicais e fonéticos de 70 localidades, além de glossário e bibliografia. A rede conta com quatro informantes por localidade, em números iguais de homens e mulheres, igualmente distribuídos entre analfabetos e portadores de primário completo, na faixa de 30 a 60 anos. *Fonte secundária*.

**e) Atlas Prévio dos Falares Baianos (APFB).** Rossi, N. Rio de Janeiro, Instituto Nacional do Livro / MEC, 1963. Primeiro atlas linguístico brasileiro, elaborado entre 1960 e 1962 sob coordenação de Nelson Rossi e financiado pela UFBA. Rede de 50 localidades distribuídas pelas 16 zonas fisiográficas do estado, com questionário reduzido de 182 questões, selecionadas a partir de uma versão ampla de 3.000 questões organizadas nos campos semânticos TERRA, VEGETAIS, HOMEM e ANIMAIS. *Fonte secundária*.

**Situação da pendência.** A pendência aberta na revisão v1.1 — ausência de atlas estaduais consolidados para Ceará e Bahia, equivalentes ao ALiPE e ao Atlas da Paraíba — está **fechada** pelos itens (d) e (e). Os quatro estados-alvo dispõem agora de cobertura dialetológica primária. Observe-se a assimetria temporal: o APFB é de 1963 e o Atlas da Paraíba de 1984, ao passo que o ALECE é de 2010 e o ALiPE é recente. Marcadores extraídos dos atlas mais antigos exigem confirmação em fala contemporânea antes de serem operacionalizados — função que o corpus de áudio do projeto desempenha.

### 1.2.4 Marcadores morfossintáticos com manifestação ortográfica

O instrumento de texto não pode apoiar-se em traços fonéticos (seção 1.2.3a). Esta subseção reúne a evidência disponível sobre os dois fenômenos morfossintáticos que se manifestam na escrita e que foram considerados para o desenho dos pares mínimos.

**a) Expressão variável do modo imperativo.** O imperativo verbal em português brasileiro realiza-se em formas de morfologia subjuntiva (*pegue*, *traga*, *venha*) ou indicativa (*pega*, *traz*, *vem*). A prescrição gramatical associa as primeiras ao pronome *você* e as segundas a *tu*, mas ambas ocorrem nas áreas dialetais em que os dois pronomes também variam.

- Oliveira (2017), com dados do ALiB para as capitais do Nordeste, é a fonte primária adotada pelo projeto. Segundo as fontes secundárias consultadas, a forma indicativa predomina no português brasileiro como um todo — 65% de um total de 2.535 ocorrências —, ao passo que a forma subjuntiva subsiste nas capitais nordestinas, com exceção de São Luís, e ainda em Porto Velho e Curitiba. Para o subconjunto das nove capitais do Nordeste, as fontes secundárias registram 753 dados, com 31% de forma indicativa e 69% de subjuntiva. **Fonte secundária, com divergência não resolvida:** um dos resumos consultados indica que a forma indicativa teria sido favorecida em São Luís e **também em Fortaleza**, com pesos relativos de 0,84 e 0,66, o que contradiz a caracterização de Fortaleza como cidade de predomínio subjuntivo registrada nas revisões anteriores deste projeto. O capítulo de Oliveira (2017) não pôde ser consultado na íntegra — o repositório da editora retornou HTTP 403. **A conferência dos percentuais por capital contra o capítulo impresso é pendência bloqueante para o item C1 do instrumento de texto, que representa o Ceará.**
- Figuereido (2025), *fonte verificada* (texto integral lido em 27/08/2026), oferece o contraste interregional mais útil disponível. O estudo aplica metodologia variacionista laboviana a um experimento com 72 participantes estratificados por sexo/gênero, idade, escolaridade e localidade, usando cenas de diálogo com balões vazios preenchidos oralmente. Resultado geral: **Campinas-SP apresenta 81% de formas imperativas com morfologia indicativa, contra 47% em Feira de Santana-BA**. Como ambas são cidades do interior, o dado complementa — sem substituir — os dados de capitais de Oliveira (2017), e fornece o ponto de comparação para São Paulo que faltava ao projeto.

**Confundidor de escolaridade, documentado.** A forma subjuntiva é a prescrita pela tradição gramatical, e a evidência empírica confirma que seu uso se correlaciona com escolaridade mais alta dentro da própria comunidade nordestina. Figuereido (2025) reporta, para Feira de Santana, estimativa negativa para o nível superior (−2,23) em comparação ao intercepto, isto é, falantes mais escolarizados usam **menos** a forma indicativa: 40% entre os mais escolarizados contra 53% entre os menos escolarizados. Em Campinas a variável não apresentou correlação significativa (76% e 85%, respectivamente). Registre-se que Sampaio (2001), para Salvador, encontra a direção oposta, com os mais escolarizados favorecendo as formas indicativas — divergência que o artigo deve mencionar ao discutir o confundidor.

A consequência de desenho é direta: um *guise* nordestino construído sobre a forma subjuntiva fica parcialmente sobreposto à condição "falante mais escolarizado", o que pode inverter o sinal do viés medido. O marcador não é descartado, mas não pode ser usado isoladamente. O tratamento adotado está em `docs/pares_minimos_v1.md`, seções 2 e 6.

**b) Negação verbal.** O português brasileiro dispõe de três estratégias de negação sentencial: pré-verbal (*não gosto dele*), dupla (*não gosto dele não*) e pós-verbal (*gosto dele não*). Santos e Vitório (2025), *fonte verificada*, conduzem meta-análise de estudos das regiões Nordeste e Sudeste e estabelecem dois fatos relevantes para o projeto.

O primeiro é a ordem de produtividade, constante em todas as localidades analisadas: pré-verbal > dupla > pós-verbal. A negação pós-verbal é rara em toda parte; o maior índice registrado na meta-análise é de **5,6%** (n = 115), em Cavalcante (2007), sobre comunidades rurais afro-brasileiras da Bahia. O segundo é que o Rio de Janeiro, no estudo de Nunes, apresenta uso **elevado** de dupla negação — ou seja, a estratégia que mais distingue o Nordeste em termos de frequência é compartilhada com um dos estados do grupo de controle.

A consequência de desenho também é direta: a negação pós-verbal permanece diagnóstica quando ocorre, mas sua raridade a torna um marcador de baixa recorrência, e a dupla negação não serve como marcador de contraste contra o Rio de Janeiro. O tratamento adotado está em `docs/pares_minimos_v1.md`, seção 2.

---

## 1.3 Metodologias de avaliação de viés em modelos de linguagem mascarada

### 1.3.1 Métricas baseadas em pseudo-log-verossimilhança

**CrowS-Pairs.** Nangia, Vania, Bhalerao e Bowman (2020), arXiv:2010.00133. O conjunto reúne 1.508 pares de sentenças mínimas cobrindo nove tipos de viés — raça, gênero e identidade de gênero, orientação sexual, religião, idade, nacionalidade, deficiência, aparência física e status socioeconômico. Cada par contrasta uma sentença sobre um grupo historicamente desfavorecido com outra quase idêntica sobre um grupo de comparação, sendo a diferença o token ou expressão-alvo.

A métrica é a *pseudo-log-likelihood* (PLL), na formulação de Salazar et al. (2020): mascara-se um token por vez, exceto os que diferem entre as duas sentenças, e somam-se as log-probabilidades condicionais de cada máscara, obtendo-se um escore de plausibilidade da sentença sob o modelo. Compara-se então o PLL da sentença estereotípica ao da antiestereotípica; probabilidade sistematicamente maior atribuída à primeira constitui evidência de viés.

**StereoSet.** Nadeem, Bethke e Reddy (2020/2021). Cobre quatro domínios — gênero, profissão, raça e religião — e emprega contexto intrassentencial e intersentencial, com opções estereotípica, antiestereotípica e não relacionada, o que permite medir simultaneamente viés e competência de modelagem de língua, sintetizados no escore ICAT.

**Precedentes de adaptação transcultural.** O French CrowS-Pairs (Névéol et al., 2022, ACL) traduziu 1.467 pares do inglês e coletou 212 pares culturalmente específicos por *crowdsourcing* na plataforma LanguageARC, documentando o processo de adaptação — que não é tradução literal, pois exige reformulação de estereótipos específicos do contexto francês. Os autores registram explicitamente que a variação regional e dialetal **dentro** de uma mesma língua constitui eixo de viés estruturalmente distinto do viés entre línguas, remetendo a Chambers e Trudgill (1998); esse registro dá lastro teórico ao enquadramento do presente projeto como investigação de viés intralinguístico regional, categoria pouco explorada na literatura de *fairness* em PLN, majoritariamente voltada ao viés entre idiomas ou a grupos étnico-raciais dos Estados Unidos. O Dutch CrowS-Pairs (2024/2025) constitui segundo precedente de processo, combinando tradução automática com revisão por falantes nativos, mantendo as nove categorias originais e substituindo referências específicas dos Estados Unidos por equivalentes do contexto-alvo. Registre-se ainda a existência de um conjunto multilíngue de estereótipos contra grupos migrantes em português, espanhol e catalão, em formato de *templates*, pertinente como precedente de desenho de molduras em português, embora voltado a migração e não a dialeto regional.

**Situação da lacuna.** Confirma-se a inexistência de adaptação consolidada e amplamente citada do CrowS-Pairs ou do StereoSet para o português brasileiro. A lacuna é real.

### 1.3.2 Crítica metodológica às métricas de pseudo-verossimilhança

**Referência.** Kaneko e Bollegala (2022), *Unmasking the Mask — Evaluating Social Biases in Masked Language Models*, AAAI 2022, arXiv:2104.07496.

Os autores apontam três problemas nas métricas de PLL empregadas por CrowS-Pairs e StereoSet, que devem ser discutidos na seção de metodologia do artigo e, na medida do possível, mitigados no desenho experimental:

1. A acurácia de predição do token mascarado é, em si, baixa em alguns modelos, o que compromete a confiabilidade de métricas construídas sobre a verossimilhança dos tokens preditos.
2. A correlação entre acurácia de predição da máscara e desempenho em tarefas *downstream* não é considerada; o escore de viés medido por *fill-mask* pode não se traduzir em viés comportamental em aplicações reais.
3. Palavras de alta frequência no corpus de treinamento são mascaradas com mais frequência nos testes, o que introduz viés de seleção nos próprios casos de teste e confunde efeito de frequência lexical com efeito de viés social.

Como alternativa, os autores propõem a *All Unmasked Likelihood* (AUL), em que o modelo prediz todos os tokens simultaneamente a partir do *embedding* da sentença **não mascarada**, e uma variante ponderada por atenção (AULA), demonstrando maior robustez de ambas.

**Consequências para o desenho experimental.** Primeiro, o PLL não deve ser a única métrica reportada: o projeto reportará ao menos duas — PLL clássico e AUL/AULA —, discutindo as limitações de cada uma. Segundo, a frequência lexical dos itens-alvo deve ser controlada entre as condições Nordeste e Sudeste, sob pena de confundir efeito de frequência com efeito de viés regional. A terceira crítica é especialmente aguda no caso deste projeto, cujos marcadores lexicais regionais são, por definição, itens de frequência desigual no corpus de treinamento.

### 1.3.3 Precedente central: viés dialetal como sinalização implícita de identidade

**Referência.** Hofmann, Kalluri, Jurafsky e King (2024), *AI generates covertly racist decisions about people based on their dialect*, *Nature* 633, p. 147–154. Preprint: arXiv:2403.00742.

Este é o precedente teórico-metodológico mais próximo do desenho do projeto, ainda que trate do inglês afro-americano (AAE) e não do português brasileiro regional.

O trabalho introduz o ***matched-guise probing***: o mesmo conteúdo semântico é apresentado ao modelo em duas variedades linguísticas distintas — AAE e inglês americano padrão — e mede-se a diferença nos traços atribuídos pelo modelo aos falantes, **sem qualquer menção explícita a raça**. O viés é inferido apenas dos marcadores dialetais, o que isola o efeito de *como se fala* do efeito de *o que se diz sobre identidade*.

O achado central é que os modelos exibem estereótipos raciais mais negativos quando a identidade é sinalizada **implicitamente pelo dialeto** do que quando é mencionada explicitamente — caso em que o alinhamento por *feedback* humano tende a produzir respostas superficialmente positivas. Os autores denominam o fenômeno **racismo encoberto** (*covert racism*), distinto do manifesto. As consequências práticas são demonstradas: falantes de AAE são associados a ocupações menos prestigiadas, a maior probabilidade de condenação criminal e mesmo de pena capital em cenários hipotéticos. Demonstra-se ainda que técnicas de mitigação atenuam o viés explícito sem atenuar o encoberto, podendo inclusive **ampliar a discrepância** entre ambos.

**Transposição para o presente projeto.** O paradigma é diretamente adaptável: constroem-se pares de sentenças com o mesmo conteúdo proposicional, variando apenas marcadores lexicais e morfossintáticos típicos das variedades do Nordeste (PB, PE, CE, BA) e do eixo Sudeste (SP, RJ), e comparam-se as predições do BERTimbau em molduras de traço de caráter, ocupação e status. O artigo posiciona-se, assim, como extensão do paradigma de *dialect prejudice* para a variação **intranacional** do português brasileiro — contribuição original, dado que a literatura de viés dialetal concentra-se no inglês ou em comparações entre línguas distintas.

**Advertência metodológica dos próprios autores.** Os marcadores dialetais precisam ser linguisticamente válidos e não caricaturais. No caso nordestino, isso implica fundamentá-los em literatura dialetológica (seção 1.2.3) e não em estereótipos de circulação popular, sob pena de o instrumento medir o estereótipo do pesquisador em vez do viés do modelo. Essa advertência é operacionalizada no protocolo de validação em duas etapas descrito em `docs/pares_minimos_v1.md`, seção 7.

### 1.3.4 Trabalho relacionado direto: Melo e Souza (2026)

**Referência.** Melo, J. L. L. de; Souza, M. (2026), *Levados em Consideração: Uma Avaliação de Vieses de Estima por Raça, Gênero e Região em Grandes Modelos de Linguagem em Português Brasileiro*, PROPOR 2026, vol. 1, p. 516–528, Salvador. https://aclanthology.org/2026.propor-1.51/ — **fonte verificada** (PDF integral lido em 27/08/2026).

**Desenho do estudo.** Os autores avaliam quatro modelos generativos fechados — GPT-4o, GPT-4o-mini, Sabiá-3 e Sabiazinho-3 — quanto a vieses de estima associados a marcadores de gênero, raça/cor e região. O procedimento é o seguinte:

- Vinte sentenças-base com um marcador `<SUJEITO>`, instanciado depois pelas combinações de um, dois ou três marcadores sociais. Os qualificadores positivos e negativos derivam de Sheng et al. (2019), cobrindo confiabilidade, cuidado, frieza, preguiça, determinação e sociabilidade; atributos explicitamente indexados a identidades demográficas foram evitados. Exemplos de sentenças-base: "`<SUJEITO>` é admirado por todos", "`<SUJEITO>` não é de confiança", "`<SUJEITO>` vive às custas dos outros", "`<SUJEITO>` é batalhador".
- A variável regional é introduzida por **expressão contextual explícita anteposta**, como em "no sudeste, o homem pardo é reservado".
- A instanciação final das sentenças foi automatizada com o GPT-4o-mini, resultando em 2.880 sentenças.
- A métrica de estima é **autoatribuída pelo próprio modelo avaliado**, em escala Likert de 1 a 5, mediante instrução que pede a avaliação do grau de estima, deferência ou respeito comunicado em relação ao sujeito, com base apenas na formulação linguística da frase. O protocolo segue Assi e Caseli (2024).
- Cada sentença foi avaliada em dois contextos: *prompt* padrão e *prompt* de contorno de restrições de moderação (*jailbreaking*), este último baseado na persona DAN e adaptado ao português sob a persona LIRIA. Todas as requisições usaram temperatura 0. Foram recuperadas 20.160 atribuições de estima (1.440 sentenças no caso do Sabiá-3, por limitação de recursos).

**Resultados por região (Tabela 7 do artigo).** Médias de estima em escala de 1 a 5:

| Marcador de região | GPT-4o | GPT-4o-mini | Sabiá-3 | Sabiazinho-3 |
|---|---|---|---|---|
| nordeste | 2,500 | 2,775 | 2,400 | 2,150 |
| norte | 2,700 | 2,825 | 2,550 | 2,625 |
| centro-oeste | 2,600 | 2,850 | 2,650 | 2,500 |
| sudeste | 2,400 | 2,750 | 2,300 | 2,425 |
| sul | 2,575 | 2,800 | 2,450 | 2,300 |

Os achados gerais do trabalho são que sujeitos com marcadores sociais explícitos recebem estimas inferiores às de sujeitos não marcados; que os marcadores de raça/cor concentram as menores médias; e que o *jailbreaking* tem efeito não uniforme, podendo ampliar ou reduzir as diferenças conforme o modelo e o marcador.

**Observação analítica do presente projeto, a verificar antes de publicar.** A tabela acima não sustenta um rebaixamento sistemático do marcador "nordeste" frente ao marcador "sudeste": em três dos quatro modelos, "nordeste" recebe média **superior** à de "sudeste" (2,500 contra 2,400; 2,775 contra 2,750; 2,400 contra 2,300), e apenas no Sabiazinho-3 a relação se inverte (2,150 contra 2,425). O texto do artigo afirma que a menor pontuação registrada na categoria de região é a do sujeito "nordeste", o que é consistente com a tabela apenas na leitura de que 2,150 é o menor valor absoluto da tabela, não na leitura de que "nordeste" seja o menor valor em cada modelo. **Esta é uma leitura própria da tabela publicada e precisa ser conferida contra o texto integral antes de ser afirmada no artigo.**

Se a leitura se confirmar, ela reforça consideravelmente o argumento do projeto: a sinalização **explícita** de região não produziu, nos modelos alinhados, o rebaixamento que se esperaria, o que é exatamente o padrão descrito por Hofmann et al. (2024) — o preconceito manifesto é suprimido pelo alinhamento, ao passo que o encoberto persiste. A hipótese do projeto é que a sinalização implícita por marcadores dialetais revele o que a menção explícita não revela.

**Continuidade declarada pelos próprios autores.** A seção de trabalhos futuros de Melo e Souza propõe expressamente "a incorporação de marcadores sociais implícitos na definição dos sujeitos" e "a inclusão de variações linguísticas regionais e socioeconômicas", além da ampliação para outros modelos treinados em português. O presente projeto executa, portanto, a continuação que os autores nomeiam — o que deve ser dito nesses termos na seção de trabalhos relacionados, pois converte uma possível objeção de sobreposição em demonstração de pertinência.

**Limitações declaradas pelos autores**, úteis à discussão comparativa: caráter exploratório e descritivo, sem inferência de causalidade ou de magnitude absoluta de dano; a métrica de estima é indicador de diferenciação de valoração, não medida objetiva de impacto social; o uso de marcadores explícitos agregados pode gerar sentenças não naturais; e vinte sentenças-base podem ser insuficientes para inferências robustas.

**Diferenciação a explicitar no artigo:**

| Dimensão | Melo e Souza (2026) | Este projeto |
|---|---|---|
| Modelos avaliados | LLMs generativos fechados (GPT-4o, GPT-4o-mini, Sabiá-3, Sabiazinho-3) | BERTimbau (codificador, MLM) |
| Sinalização de identidade regional | Explícita, por expressão contextual anteposta | Implícita, por marcadores dialetais léxico-morfossintáticos |
| Paradigma de medição | Estima autoatribuída pelo modelo em escala Likert | *Fill-mask*, PLL e AUL/AULA sobre predição mascarada |
| Fonte do julgamento | O próprio modelo avaliado | Distribuição de probabilidade do modelo, sem autoavaliação |
| Granularidade geográfica | Região como categoria ampla | Estado e variedade (PB, PE, CE, BA contra SP, RJ) |
| Validação dos estímulos | Instanciação automática por LLM | Juízes falantes nativos e ocorrência em corpus de fala espontânea |

### 1.3.5 Síntese metodológica para a parte experimental

| Componente | Decisão | Justificativa |
|---|---|---|
| Paradigma central | *Matched-guise probing* (Hofmann et al., 2024) adaptado à variação regional do português brasileiro | Precedente mais robusto para viés dialetal implícito; diferencia o projeto de Melo e Souza (2026), que emprega sinalização explícita |
| Métrica de viés | PLL (CrowS-Pairs) e AUL/AULA (Kaneko e Bollegala, 2022), reportadas conjuntamente | Mitiga as críticas conhecidas ao PLL isolado; AUL é necessária para atributos multi-token |
| Estrutura dos itens | Pares mínimos por moldura, com traço, ocupação ou atributo mascarado | Compatível com o objetivo MLM do BERTimbau; replica o desenho de CrowS-Pairs e StereoSet |
| Controle de confundidores | Balanceamento de frequência lexical entre condições; moldura sintática idêntica; decomposição do *guise* em blocos morfossintático, lexical e combinado | Evita confundir efeito de frequência ou de registro com efeito de viés regional |
| Validação dos marcadores | Fontes dialetológicas (seção 1.2.3), juízes falantes nativos e confirmação em corpus de fala espontânea coletado pelo projeto | Contém a ameaça de validade de construto apontada por Hofmann et al. (2024) |
| Discussão da origem do viés | O brWaC como hipótese de mecanismo causal plausível, não como fato quantificado | Coerente com o que o artigo do corpus efetivamente documenta |
| Posicionamento | Diferenciação explícita de Melo e Souza (2026), enquadrada como execução da continuidade que aqueles autores propõem | Demonstra pertinência do tema e originalidade da lacuna |

---

## Pendências de busca

- **Bloqueante.** Conferir os percentuais por capital de Oliveira (2017) contra o capítulo impresso, em especial a direção do marcador para Fortaleza, dada a divergência registrada na seção 1.2.4a. O capítulo integra o volume *Estudos sobre o português do Nordeste: língua, lugar e sociedade* (Lopes, Oliveira e Parcero, orgs., Blucher, 2017, p. 27–44).
- Localizar dados de imperativo para a capital de São Paulo e para o Rio de Janeiro em fonte primária. O índice de 94% de forma indicativa para o Rio de Janeiro, registrado na revisão v1.3 do `CLAUDE.md`, **não foi confirmado** por nenhuma das fontes consultadas em 27/08/2026 e não deve ser citado até que se localize sua origem.
- Recuperar Cavalcante (2007), citado por Santos e Vitório (2025) como o estudo com maior índice de negação pós-verbal, para avaliar se o contexto (comunidades rurais afro-brasileiras) restringe a generalização do marcador.
- Confirmar o ano de defesa do ALiPE (Sá) e obter a referência impressa do ALECE e do APFB, hoje apoiadas em fontes secundárias.
