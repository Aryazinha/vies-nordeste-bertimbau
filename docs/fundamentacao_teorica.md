# Fundamentação Teórica Completa
## Referência de apoio ao projeto — Investigação de Vieses Sociolinguísticos no BERTimbau

> Movido do CLAUDE.md em 06/08/2026 (v1.5) por limite de tamanho. Contém as seções 1.1, 1.2 e 1.3 na íntegra.

---

# PARTE 1 — FUNDAMENTAÇÃO TEÓRICA

## 1.1 BERTimbau: origem, arquitetura e treinamento

**Referência primária:**
> Souza, F., Nogueira, R., Lotufo, R. (2020). *BERTimbau: Pretrained BERT Models for Brazilian Portuguese*. In: Cerri, R., Prati, R.C. (eds) *Intelligent Systems* (BRACIS 2020), LNCS vol. 12319, Springer, Cham, pp. 403–417. DOI: [10.1007/978-3-030-61377-8_28](https://doi.org/10.1007/978-3-030-61377-8_28)
> Repositório oficial: https://github.com/neuralmind-ai/portuguese-bert

**O que o artigo estabelece:**
- Os autores treinam modelos **BERT** (arquitetura original de Devlin et al., 2019) especificamente para o português brasileiro, apelidados **BERTimbau**, disponibilizados em duas variantes: **Base** (110M parâmetros, 12 camadas) e **Large** (335M parâmetros, 24 camadas), seguindo a configuração *cased* do BERT original.
- O treinamento foi feito com o objetivo de **Masked Language Modeling (MLM)** com *whole-word masking* (WWM) — isto é, quando um subtoken de uma palavra é mascarado, todos os subtokens da mesma palavra também são mascarados, o que reduz "atalhos" triviais de predição e força o modelo a aprender representações semânticas mais robustas.
- O corpus de pré-treino foi **exclusivamente o brWaC** (ver seção 1.2) — ao contrário de outros modelos citados na literatura correlata que combinam brWaC + Wikipédia + corpus jornalístico (essa combinação aparece em alguns trabalhos posteriores que descrevem o BERTimbau de forma imprecisa; o texto original e o repositório oficial confirmam **brWaC como única fonte de pré-treino**).
- Treinamento por **1.000.000 de passos (steps)**.
- Avaliação em três tarefas *downstream*: similaridade textual semântica (STS/ASSIN2), inferência textual (RTE/ASSIN2) e reconhecimento de entidades nomeadas (NER/MiniHAREM), superando o mBERT (BERT multilíngue) em todas.

**Implicação direta para o projeto:** como o BERTimbau foi treinado **apenas** com o brWaC, qualquer viés geográfico/sociolinguístico presente na composição do brWaC é herdado quase diretamente pelo modelo — não há outro corpus "diluindo" essa distribuição. Isso reforça a hipótese central do estudo (comparação Nordeste vs. Sudeste) e deve ser citado explicitamente na seção de "ameaças à validade" do artigo, como confundidor causal a ser discutido.

**Fontes de apoio (contextualização, não citações centrais):**
- Repositório oficial (BibTeX oficial de citação): https://github.com/neuralmind-ai/portuguese-bert
- Verbete Springer (abstract oficial): https://link.springer.com/chapter/10.1007/978-3-030-61377-8_28
- Contextualização por trabalhos posteriores (ex.: *PeLLE: Encoder-based language models for Brazilian Portuguese*, arXiv:2402.19204) confirmando "BrWaC dataset... 2.68B tokens" como corpus de treino do BERTimbau.

---

## 1.2 Corpus brWaC (Brazilian Web as Corpus): composição e viés geográfico

**Referência primária:**
> Wagner Filho, J. A., Wilkens, R., Idiart, M., Villavicencio, A. (2018). *The brWaC Corpus: A New Open Resource for Brazilian Portuguese*. In: Proceedings of LREC 2018, Miyazaki, Japan. ELRA. ACL Anthology: https://aclanthology.org/L18-1686/

**Ficha técnica do corpus (dados que constam nos textos indexados):**
- **2,68–2,7 bilhões de tokens**; **3,53 milhões de documentos**; **5,79 milhões de types**.
- Construído via metodologia **WaCky** (*Web as Corpus*, Baroni et al. 2009), com pipeline de 4 etapas: (1) identificação de seed URLs, (2) *crawling* e limpeza pós-coleta, (3) remoção de conteúdo duplicado, (4) anotação linguística (PoS tagging e parsing com o parser Palavras).
- Mais de **60 milhões de páginas rastreadas**, das quais apenas **3,5 milhões foram selecionadas** (regras estritas de filtragem mantiveram só ~5,6% das sementes originais).
- **120.000 sites diferentes** contribuíram conteúdo — usado pelos autores como argumento de "diversidade de domínio".
- Instituições responsáveis: **UFRGS** (Instituto de Informática e Instituto de Física), com colaboração da **UCLouvain** (Bélgica) e **University of Essex** (Reino Unido).
- Licenciamento: uso **exclusivamente acadêmico/pesquisa**, proibida aplicação comercial (relevante para a seção de direitos autorais/ética do projeto).

**⚠️ Ponto crítico para o projeto — viés geográfico não documentado explicitamente pelos autores:**

Nas buscas realizadas, **o artigo original do brWaC (Wagner Filho et al., 2018) não publica uma quebra estatística explícita por região/estado de origem dos sites coletados**. O que os autores reportam é diversidade de **domínio temático** (notícias, blogs, fóruns, sites institucionais, etc.), não diversidade **geográfica/dialetal**. Isso é, em si, um achado metodológico relevante para o artigo de vocês: a ausência de estratificação geográfica documentada na ficha técnica do corpus é justamente a lacuna que a pesquisa de vocês torna operacionalizável empiricamente (via os testes de MLM).

Como o brWaC foi coletado por *web crawling* de domínios `.br` de forma não estratificada por região, a literatura de ciência da computação e sociolinguística brasileira aponta um mecanismo indireto, mas bem estabelecido, para explicar por que a distribuição textual resultante tende a favorecer o eixo Sul-Sudeste:

1. **Desigualdade de acesso à internet e de produção de conteúdo digital por região** — historicamente concentrada nas regiões Sul e Sudeste do Brasil (dado socioeconômico e de infraestrutura, não linguístico per se, mas com efeito causal direto sobre *quais* variedades de português acabam representadas em texto *web*). **Ver seção 1.2.1, abaixo, para os dados quantitativos atualizados que sustentam este ponto (pendência da rodada anterior, agora fechada).**
2. **Estigmatização do falar nordestino em contextos formais/escritos** — mesmo falantes nordestinos tendem a produzir texto escrito formal (que é o tipo de texto majoritariamente capturado por *web crawling* de sites institucionais/jornalísticos) em variedades mais próximas da norma padrão, "apagando" superficialmente os traços dialetais salientes. Isso é discutido em trabalhos de dialetologia/sociolinguística, por exemplo:
   > "Português nordestino: para além das capitais" (2021) — discute como o falar nordestino migrante é estigmatizado no Sudeste, e como o movimento de retorno gera hibridização dialetal (citando Oushiro, 2016, sobre altura vocálica). Disponível em: https://www.researchgate.net/publication/361462317

   **Referência clássica complementar (pendência da rodada anterior, agora fechada — ver seção 1.2.2):** Bagno, M. (1999). *Preconceito Linguístico: o que é, como se faz*. São Paulo: Loyola.

**Recomendação metodológica:** no capítulo de fundamentação do artigo, tratem a "concentração Sul-Sudeste do brWaC" como uma **hipótese testável e plausível por inferência**, apoiada em (a) ausência de estratificação geográfica no desenho do corpus, (b) dados demográficos de acesso à internet por região (ver seção 1.2.1), e (c) literatura sociolinguística sobre estigma do dialeto nordestino — e não como um fato explicitamente quantificado pelos autores do brWaC. Isso é *mais defensável* perante revisores do que alegar um viés "documentado" que não está no paper original. Uma real contribuição do artigo de vocês pode ser justamente **quantificar empiricamente**, pela primeira vez, esse viés geográfico via comportamento do modelo (já que o corpus não fornece metadados de geolocalização por documento que permitiriam auditá-lo diretamente).

**Ameaça à validade a registrar desde já:** o brWaC não expõe metadados de geolocalização de documentos publicamente (pelo menos não nas versões amplamente distribuídas, ex. Hugging Face `UFRGS/brwac`, `dominguesm/brwac`). Isso significa que **não é possível auditar diretamente a proporção de conteúdo por variedade regional na fonte de treino** — a única via de investigação é comportamental/indireta (via *probing* do modelo já treinado, que é exatamente o desenho do projeto). Isso deve ser declarado explicitamente como limitação epistemológica no artigo: "inferimos viés a partir do comportamento do modelo, não da auditoria direta do corpus."

### 1.2.1 [NOVO — v1.1] Dados quantitativos de acesso e produção de conteúdo digital por região (Cetic.br/NIC.br — TIC Domicílios 2024)

Pendência fechada nesta rodada. Fonte: pesquisa **TIC Domicílios 2024**, realizada por Cetic.br/NIC.br (Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação), divulgada em 31/10/2024, 20ª edição da série histórica.

**Achados relevantes para sustentar a hipótese de concentração Sul-Sudeste na origem do brWaC (usar como inferência socioeconômica, não como prova direta sobre o corpus):**

- Do total de 29 milhões de brasileiros que não usam internet, 21 milhões estão concentrados nas regiões Sudeste (12 milhões) e Nordeste (8 milhões) — as regiões mais populosas, portanto números absolutos precisam ser lidos com essa ressalva.
- O dado mais forte para o argumento do projeto é o de **qualidade** de acesso, não apenas presença: o indicador de "conectividade significativa" do Cetic.br — que pondera custo, velocidade, presença de banda larga fixa e acesso por múltiplos dispositivos — mostra que apenas 22% dos brasileiros com 10 anos ou mais têm condições satisfatórias de conectividade. Por região, esse indicador chega a 33% no Sul, mas apenas 11% no Nordeste.
- Sobre **produção** de conteúdo (proxy mais direto para composição de um corpus como o brWaC do que consumo): a proporção de usuários que postaram conteúdo próprio (textos, imagens, vídeos) subiu de 31% em 2021 para 43% em 2022, mas o compartilhamento de conteúdo de terceiros historicamente supera a criação própria por larga margem — em 2017, a proporção de compartilhamento (73%) era o dobro da de postagem de conteúdo próprio (37%).
- Um proxy indireto de precariedade de acesso — o compartilhamento de conexão de internet com vizinhos — é mais comum no Norte (21%) e Nordeste (22%) do que no Sul, Sudeste ou Centro-Oeste.

**Referência para BibTeX:**
> Cetic.br/NIC.br (2024). *Pesquisa sobre o uso das tecnologias de informação e comunicação nos domicílios brasileiros: TIC Domicílios 2024*. Disponível em: https://cetic.br/pt/pesquisa/domicilios/

**Nota metodológica:** estes são dados de acesso/uso de internet em geral, não uma auditoria da composição do brWaC especificamente. Usar apenas como evidência socioeconômica de apoio à hipótese de mecanismo causal (conforme já recomendado na seção 1.2), nunca como se fossem estatísticas do próprio corpus.

### 1.2.2 [NOVO — v1.1] Marcos Bagno — referência clássica de sociolinguística brasileira (pendência fechada)

> Bagno, M. (1999). *Preconceito Linguístico: o que é, como se faz*. São Paulo: Edições Loyola.

Marcos Bagno é professor da Universidade de Brasília (UnB), doutor em Filologia e Língua Portuguesa pela USP, com pesquisa focada em educação linguística e no impacto da sociolinguística sobre o ensino de português no Brasil. A obra é considerada referência fundacional da divulgação científica sobre preconceito linguístico no país.

**O que o Capítulo 1 ("A mitologia do preconceito linguístico") estabelece e é diretamente citável para o projeto:**
- Desconstrói o mito da homogeneidade do português brasileiro, argumentando que a negação da heterogeneidade dialetal é a base ideológica do preconceito linguístico.
- Desconstrói o mito de que "o brasileiro não sabe português" (em oposição ao português europeu), mostrando que toda língua viva é heterogênea, incluindo o português de Portugal.

**Uso recomendado no artigo:** citar Bagno (1999) como fundamentação teórica geral do conceito de preconceito linguístico no Brasil, em complemento (não substituição) às referências de dialetologia variacionista (Oushiro) e ao precedente internacional de *dialect prejudice* (Hofmann et al., 2024, seção 1.3.3) — Bagno fornece o enquadramento sociológico/ideológico brasileiro; Hofmann et al. fornecem o paradigma experimental computacional.

### 1.2.3 [NOVO — v1.1] Fontes dialetológicas primárias — Projeto ALiB (pendência fechada, parcialmente)

Localizadas fontes primárias do **Projeto Atlas Linguístico do Brasil (ALiB)**, sediado na UFBA desde 1996, baseado em Dialetologia Pluridimensional (variação diatópica, diastrática, diagenérica, diageracional).

**Fontes com cobertura direta de PE e PB (dois dos quatro estados-alvo do projeto):**

1. **Fenômeno fonético operacionalizável e citável — realização de /t,d/ diante de /i/ no Nordeste:**
   > Estudo vinculado ao ALiB, sediado na UEFS/UFBA, investigando a palatalização de /t,d/ diante de /i/ (ex. "tia"/"dia" pronunciados com africada [tʃ,dʒ] vs. dental [t,d]) nos nove estados nordestinos. Corpus: 78 localidades nordestinas, 348 informantes (72 nas 9 capitais, 276 no interior), estratificados por sexo, duas faixas etárias (18–30 e 50–65 anos) e, nas capitais, dois níveis de escolaridade. Disponível em: http://www.mel.uefs.br/modules/conteudo/conteudo.php?conteudo=67

   Este é o traço fonético mais robusto e diretamente operacionalizável como marcador dialetal para os pares mínimos do projeto: é uma isoglossa documentada, com metodologia de amostragem transparente e réplica em múltiplos pontos do Nordeste.

2. **Atlas Linguístico de Pernambuco (ALiPE):**
   > Sá, E. J. de. *Atlas Linguístico de Pernambuco*. Tese (Doutorado em Letras) — Universidade Federal da Paraíba. Disponível em: https://alib.ufba.br/atlas-linguistico-de-pernambuco-alipe
   Metodologia: 20 pontos de inquérito, 84 informantes (critérios de Cardoso, 2010: faixas etárias 18–30 e 50–65, escolaridade), 105 cartas linguísticas (50 fonéticas, 47 semântico-lexicais, 8 morfossintáticas).

3. **Atlas Linguístico da Paraíba:**
   > Aragão, M. do S.; Menezes, C. P. B. de. (1984). *Atlas Linguístico da Paraíba*. Brasília: UFPB/CNPq.

4. **Trabalhos complementares de Maria do Socorro Aragão (UFPB/UFC)** sobre variantes fonéticas nordestinas e variantes de natureza palatal no português brasileiro — publicados na série *Documentos* do Projeto ALiB (UFBA).

**⚠️ Pendência remanescente para a próxima rodada:** não foram localizados nesta busca atlas estaduais específicos e consolidados para **Ceará** e **Bahia** equivalentes ao ALiPE (PE) e ao Atlas da Paraíba (PB) — apenas menções de que atlas para outros estados nordestinos estão "em fase iniciada ou avançada de execução". Buscar especificamente "Atlas Linguístico do Ceará" e "Atlas Linguístico da Bahia" (ou equivalentes de mesorregião) na próxima rodada, dado que Bahia sedia o próprio Projeto ALiB (UFBA) e provavelmente tem produção associada não capturada nesta busca.

**Uso recomendado:** citar diretamente o estudo de palatalização /t,d/ (item 1) como referência primária para validação de marcadores fonéticos de PE, PB, CE e BA (já que o corpus cobre os nove estados nordestinos); citar ALiPE e Atlas da Paraíba para marcadores lexicais/morfossintáticos específicos de PE e PB.

---

## 1.3 Metodologias de avaliação de viés em PLN (foco em MLM / fill-mask)

### 1.3.1 Linha fundacional: métricas baseadas em pseudo-log-likelihood

**CrowS-Pairs**
> Nangia, N., Vania, C., Bhalerao, R., Bowman, S. R. (2020). *CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models*. arXiv:2010.00133. https://ar5iv.labs.arxiv.org/html/2010.00133

- Dataset de **1.508 pares de sentenças mínimas** ("minimal pairs"), cobrindo **9 tipos de viés** (raça, gênero/identidade de gênero, orientação sexual, religião, idade, nacionalidade, deficiência, aparência física, status socioeconômico).
- Cada par contrasta uma sentença sobre um grupo historicamente desfavorecido com uma sentença quase idêntica sobre um grupo de comparação (a diferença é o token/expressão-alvo).
- **Métrica:** *pseudo-log-likelihood* (PLL) — mascara-se um token por vez (exceto os tokens que diferem entre as duas sentenças), soma-se a log-probabilidade condicional de cada máscara, chegando a um escore de plausibilidade da sentença inteira sob o MLM (metodologia original de Salazar et al., 2020). Compara-se o PLL da sentença estereotípica vs. a antiestereotípica: se o modelo atribui probabilidade sistematicamente maior à sentença estereotípica, isso é evidência de viés.
- **Adaptável ao design do projeto de vocês:** este é o desenho mais direto de se adaptar para PT-BR/variação dialetal — vocês podem construir pares mínimos do tipo "um nordestino que fala assim... / um paulista que fala assim..." e comparar o PLL atribuído pelo BERTimbau.

**StereoSet**
> Nadeem, M., Bethke, A., Reddy, S. (2020/2021). *StereoSet: Measuring stereotypical bias in pretrained language models*.
- Cobre 4 domínios (gênero, profissão, raça, religião); usa contexto intra-sentença (*intrasentence*) e inter-sentença (*intersentence*), com opções estereotípica, antiestereotípica e não relacionada (*unrelated*), permitindo medir viés e "sensatez linguística" (*language modeling score*) simultaneamente — métrica combinada chamada **ICAT score**.

**Adaptações multilíngues relevantes (metodologia de tradução/adaptação cultural):**
- **French CrowS-Pairs** (Névéol et al., 2022, ACL) — traduziram 1.467 pares do inglês e coletaram 212 novos pares culturalmente específicos via *crowdsourcing* na plataforma LanguageARC, documentando explicitamente o processo de adaptação cultural (não é tradução literal — exige reformulação de estereótipos específicos do contexto francês). https://aclanthology.org/2022.acl-long.583/
  - **Achado citável para vocês:** os autores relatam explicitamente que **variação regional/dialetal dentro de uma mesma língua** é um eixo de viés estruturalmente diferente de viés entre línguas distintas, citando Chambers & Trudgill (1998) sobre dialetos regionais/sociais — isso dá lastro teórico direto para o enquadramento "viés intralinguístico regional" do projeto de vocês (nordeste vs. sudeste dentro do PT-BR), que é uma categoria pouco explorada na literatura de bias em PLN (majoritariamente focada em viés *entre* idiomas ou grupos étnico-raciais nos EUA).
- Existe também um dataset multilíngue de estereótipos contra **grupos migrantes em Português, Espanhol e Catalão** (formato *sentence templates*), referenciado na literatura de *fairness datasets* — relevante como precedente metodológico de *template design* em português, embora focado em migração e não em dialeto regional.
- **[NOVO — v1.1] Precedente de processo de adaptação (Dutch CrowS-Pairs):** Chen et al./autores do Dutch CrowS-Pairs (2024/2025) adaptaram o dataset original combinando tradução automática (avaliada como competitiva na literatura) com revisão por falantes nativos, retendo as 9 categorias originais e substituindo referências específicas dos EUA por equivalentes do contexto-alvo (ex. grupos migrantes locais no lugar de grupos étnicos americanos). Útil como segundo precedente de *processo* de adaptação transcultural, ao lado do French CrowS-Pairs, para documentar metodologicamente como o projeto adaptará os pares para o eixo dialetal Nordeste/Sudeste.

### 1.3.2 Crítica metodológica às métricas de pseudo-likelihood (leitura obrigatória antes de escolher a métrica)

> Kaneko, M., Bollegala, D. (2021/2022). *Unmasking the Mask — Evaluating Social Biases in Masked Language Models*. AAAI 2022. arXiv:2104.07496. https://arxiv.org/abs/2104.07496

Os autores apontam **três problemas metodológicos sérios** nas métricas de PLL usadas por CrowS-Pairs/StereoSet, que vocês **devem** discutir na seção de metodologia do artigo (e idealmente mitigar no desenho experimental):

1. A **acurácia de predição do token mascarado em si já é baixa** em alguns MLMs, o que compromete a confiabilidade de métricas baseadas na (pseudo)verossimilhança dos tokens preditos.
2. A **correlação entre acurácia de predição da máscara e desempenho em tarefas *downstream* reais não é considerada** — ou seja, o escore de viés medido via *fill-mask* pode não se traduzir em viés comportamental em aplicações reais.
3. **Palavras de alta frequência no corpus de treino são mascaradas com mais frequência** nos testes, introduzindo um viés de seleção nos próprios casos de teste (efeito de frequência lexical se confunde com efeito de viés social).

**Proposta alternativa dos autores:** *All Unmasked Likelihood* (**AUL**) — em vez de mascarar um token por vez, o modelo prediz todos os tokens simultaneamente a partir do *embedding* MLM da sentença **não mascarada**, e uma variante com pesos de atenção (**AULA**). Os autores mostram que essas métricas são mais robustas.

**Recomendação para o desenho experimental do projeto:**
- Não usem PLL "puro" como única métrica. Reportem **ao menos duas métricas** (ex.: PLL clássico do CrowS-Pairs *e* AUL/AULA, ou PLL + análise direta de probabilidade top-k no *fill-mask*), e discutam explicitamente as limitações de cada uma — isso fortalece a defesa metodológica em revisão por pares.
- Controlem a **frequência lexical** dos itens-alvo entre as condições Nordeste/Sudeste nos seus pares mínimos (ex.: usando frequência no próprio brWaC ou em corpora de referência), para não confundir "efeito de frequência" com "efeito de viés regional".

### 1.3.3 Precedente direto e mais próximo do desenho do projeto: viés de dialeto como proxy de identidade social

> Hofmann, V., Kalluri, P. R., Jurafsky, D., King, S. (2024). *Dialect prejudice predicts AI decisions about people's character, employability, and criminality*. arXiv:2403.00742 — publicado como *AI generates covertly racist decisions about people based on their dialect*, **Nature** 633, 147–154 (2024). https://www.nature.com/articles/s41586-024-07856-5

Este é, na minha avaliação como pesquisador, **o precedente teórico-metodológico mais importante para o desenho de vocês**, mesmo sendo sobre inglês afro-americano (AAE) e não sobre PT-BR regional. Pontos centrais:

- Introduz a técnica de ***matched-guise probing***: o mesmo conteúdo semântico é apresentado ao modelo em duas variedades linguísticas distintas (AAE vs. Standard American English), e mede-se a diferença nos traços/associações atribuídos pelo modelo aos falantes — **sem nunca mencionar raça explicitamente**. O viés é inferido *apenas* a partir de marcadores dialetais (léxico, sintaxe), isolando o efeito do "como se fala" do efeito do "o que se diz sobre identidade explícita".
- Achado central: modelos exibem **estereótipos raciais mais negativos quando a identidade é sinalizada implicitamente via dialeto** do que quando é mencionada explicitamente (onde o *alignment*/RLHF tende a produzir respostas superficialmente positivas) — os autores chamam isso de **"racismo encoberto" (covert racism)**, distinto do racismo manifesto.
- Demonstram consequências práticas: modelos tendem a associar falantes de AAE a empregos menos prestigiados, maior probabilidade de condenação criminal e até de pena de morte em cenários hipotéticos — evidência de que o viés dialetal *não é inócuo*, tem efeito em decisões automatizadas simuladas.
- Mostram que técnicas de mitigação de viés (RLHF/*human feedback*) **atenuam o viés explícito mas não o encoberto**, e podem até **aumentar a discrepância** entre os dois (o modelo "aprende a esconder" o viés, mas mantém a associação internamente).

**Transposição direta para o projeto de vocês:**
- O design "matched-guise probing" é diretamente adaptável: construir pares de sentenças com o **mesmo conteúdo proposicional**, mas com marcadores lexicais/sintáticos típicos do falar nordestino (PB/PE/CE/BA) vs. do falar do eixo Sudeste (SP/RJ), e comparar as predições de *fill-mask* do BERTimbau para completar lacunas relacionadas a traços de personalidade, profissão, status socioeconômico etc.
- Vocês podem (e acredito que **devem**) posicionar o artigo explicitamente como uma extensão do paradigma de "*dialect prejudice*" de Hofmann et al. para o contexto de variação **intranacional** do português brasileiro — isso é uma contribuição original clara e citável, pois a maior parte da literatura de *dialect bias* trata de inglês (AAE) ou de comparações entre línguas distintas, não de variação dialetal regional dentro do português.
- **Cuidado ético/metodológico:** os autores do estudo original alertam que os marcadores dialetais precisam ser **linguisticamente válidos e não caricaturais** — para o Nordeste, isso significa basear os marcadores lexicais/sintáticos em literatura dialetológica séria (ver seção 1.2.3 — Atlas Linguístico do Brasil, ALiPE, Atlas da Paraíba, trabalhos de Aragão — e Oushiro, Bagno), e não em estereótipos populares ("forró", "cangaço" etc.), sob risco de o instrumento medir estereótipo do pesquisador em vez de viés do modelo.

### 1.3.4 [NOVO — v1.1] Trabalho relacionado direto identificado: Melo & Souza (2026), PROPOR

**⚠️ Achado importante da rodada de busca — deve ser citado explicitamente na seção de trabalhos relacionados do artigo.**

> Melo, J. L. L. de; Souza, M. (2026). *Levados em Consideração: Uma Avaliação de Vieses de Estima por Raça, Gênero e Região em Grandes Modelos de Linguagem em Português Brasileiro*. In: Proceedings of the 17th International Conference on Computational Processing of Portuguese (PROPOR 2026), Vol. 1, pp. 516–528, Salvador, Brasil. ACL Anthology: https://aclanthology.org/2026.propor-1.51/

**O que o artigo estabelece:**
- Avalia vieses sociais em português nos modelos GPT-4o, GPT-4o-mini, Sabiá-3 e Sabiázinho-3, usando uma métrica de "estima" para medir o nível de respeito/deferência do modelo sobre diferentes grupos demográficos.
- Cobre sujeitos com marcadores sociais **explícitos** de gênero, raça e região brasileira, com e sem uso de técnica de jailbreaking (contorno de restrições de moderação).
- Achado central: os modelos reproduzem padrões sistemáticos de valoração diferenciada entre grupos sociais; sujeitos com marcadores de raça enfatizados recebem estimas mais baixas; jailbreaking tem impacto não-uniforme (pode ampliar ou reduzir as diferenças).

**Por que este NÃO é o mesmo estudo que o de vocês (diferenciação obrigatória no artigo):**

| Dimensão | Melo & Souza (2026) | Este projeto |
|---|---|---|
| Modelos avaliados | LLMs generativos (GPT-4o, Sabiá-3, etc.) | BERTimbau (encoder MLM) |
| Sinalização de identidade regional | **Explícita** (menção direta à região) | **Implícita** — via marcadores dialetais léxico-sintáticos (*matched-guise*, paradigma Hofmann et al. 2024), sem menção explícita à região |
| Paradigma de medição | Métrica de "estima"/deferência sobre resposta gerada | *Fill-mask* / pseudo-log-likelihood (PLL) / AUL-AULA sobre predição mascarada |
| Granularidade geográfica | Região como categoria ampla (ex. "Nordeste" vs. outras regiões) | Estado/variedade específica (PB, PE, CE, BA vs. SP, RJ) |
| Venue/ano | PROPOR 2026 | Alvo: BRACIS/PROPOR/STIL (a definir) |

**Uso recomendado:** citar como o precedente mais recente e mais próximo em português sobre viés regional em modelos de linguagem, na seção de trabalhos relacionados, argumentando explicitamente que a contribuição original do projeto está na combinação (a) sinalização **implícita** via dialeto (não menção explícita a região/identidade), (b) paradigma de **encoder MLM** com métricas de pseudo-verossimilhança (não LLM generativo com métrica de estima), e (c) granularidade **estadual/dialetal** (não regional ampla). Esse contraste fortalece — não enfraquece — a posição do artigo de vocês, pois demonstra que o tema está ativo na comunidade (relevância) sem que a lacuna específica já tenha sido preenchida (originalidade).

### 1.3.5 Síntese metodológica recomendada para a Parte Experimental

| Componente | Recomendação | Justificativa |
|---|---|---|
| Paradigma central | *Matched-guise probing* (Hofmann et al., 2024) adaptado para PT-BR regional | Precedente direto mais robusto para viés dialetal implícito; diferencia o projeto de Melo & Souza (2026), que usa sinalização explícita |
| Métrica de viés | Reportar PLL (CrowS-Pairs) **+** AUL/AULA (Kaneko & Bollegala, 2022) | Mitiga críticas conhecidas ao PLL puro |
| Estrutura dos itens | Pares mínimos por template (nomes de traço/profissão/atributo mascarados) | Compatível com MLM do BERTimbau; replica desenho CrowS-Pairs/StereoSet |
| Controle de confundidores | Balancear frequência lexical dos itens-alvo entre grupos; usar mesma estrutura sintática | Evita confundir efeito de frequência com efeito de viés regional |
| Validação dos marcadores dialetais | Basear-se em fontes dialetológicas (ALiB, ALiPE, Atlas da Paraíba, Aragão — seção 1.2.3) + validação por falantes nativos/juízes | Evita caricaturização e reforça validade de construto |
| Discussão da fonte do viés | Enquadrar o brWaC como hipótese de mecanismo causal plausível (não fato quantificado), apoiada em dados Cetic.br/NIC.br (seção 1.2.1) | Coerente com o que o paper do brWaC realmente documenta |
| Posicionamento em trabalhos relacionados | Diferenciar explicitamente de Melo & Souza (2026) — ver tabela na seção 1.3.4 | Demonstra relevância do tema e originalidade da lacuna preenchida |

---