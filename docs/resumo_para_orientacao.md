# Resumo do estado da pesquisa

**Data:** 31/08/2026. **Destinatário:** orientação. **Atualização de 15/09/2026:** todas as seções revistas — resultados com 20 frases por condição de menção explícita, validação dos pares sem juízes, corpus concluído na coleta, anonimização executada e enquadramento decidido.

Documento de leitura rápida. As questões que dependem de decisão da orientação estão reunidas em [`questoes_para_orientacao.md`](questoes_para_orientacao.md); este arquivo apenas relata o estado. Cada número indica a fonte de onde foi extraído.

---

## 1. Contexto e objetivo

A pesquisa investiga viés sociolinguístico regional no BERTimbau, contrastando variedades da Paraíba, Pernambuco, Ceará e Bahia com um grupo de controle de São Paulo e Rio de Janeiro.

O desenho adota o *matched-guise probing* de Hofmann et al. (2024): pares de enunciados com conteúdo proposicional idêntico, apresentados ao modelo em variedades distintas, medindo-se a diferença de escore atribuída a cada atributo. A lacuna que motiva o trabalho é a inexistência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro.

**O projeto produz dois conjuntos de dados.** Um corpus de fala regional coletado de plataformas públicas, e um conjunto de pares mínimos de texto. O corpus servia originalmente para confirmar, em fala espontânea contemporânea, que os marcadores dialetais indicados pela literatura de fato ocorrem — função que os resultados alteraram, como se registra adiante.

Método e ameaças à validade estão em [`protocolo.md`](protocolo.md); a especificação dos conjuntos, em [`dataset-spec.md`](dataset-spec.md).

---

## 2. O que já está concluído

### 2.1 O modelo não responde à sinalização dialetal implícita

Quatro famílias de marcadores foram testadas, e nenhuma produz efeito acima do grupo de referência de pares não regionais que sobreviva à correção de multiplicidade:

| Família | Pares | Resíduo médio | p ajustado |
|---|---|---|---|
| Morfossintática — imperativo e negação | 5 | −0,0763 | 1,0000 |
| Lexical — itens regionais | 5 | +0,0739 | 0,0700 |
| Feixe combinado | 5 | +0,0126 | 0,9435 |
| Construcional | 10 | −0,0249 | 1,0000 |

*Fonte: `experimentos/resultados/tabelas/explicito_tabelas.md`. A família lexical, a mais próxima do limiar, é indistinguível de um controle de palavras raras não regionais (+0,0699).*

O caso mais informativo é a negação pós-verbal — "fui não" contra "não fui" —, cujos dois lados empregam **as mesmas palavras em ordem diferente**. A explicação por raridade lexical está aí excluída por construção, e o resultado é nulo.

O nulo é legível porque duas condições de interpretabilidade foram satisfeitas. O controle positivo, que contrasta proposições distintas, produz resíduo de +0,3422 com p ajustado de 0,0004 — a medição detecta o que existe. E o confundidor de frequência está verificado, e não apenas declarado: sobre 86 pares não regionais, a razão de frequência não prevê a diferença de escore.

### 2.2 O modelo responde à menção explícita de região, sem especificidade relevante para o Nordeste quando a pessoa fala de si

Três condições, com 20 frases cada, produzem resíduo acima do grupo de referência não regional **e sobrevivem à correção de Holm**:

| Condição | Pares | Resíduo | Acima da reta | p ajustado |
|---|---|---|---|---|
| Gentílico de estado — *pernambucano*, *baiana* | 20 | +0,1631 | 20/20 | **0,0004** |
| Macrorregião — *Nordeste*, *nordestino* | 20 | +0,0871 | 16/20 | **0,0007** |
| Terceira pessoa — *O cliente é do Nordeste* | 20 | +0,0796 | 16/20 | **0,0007** |
| Topônimo — *Ceará*, *Caruaru*, *Recife* | 20 | +0,0303 | 13/20 | 0,1328 |

*Fonte: `experimentos/resultados/tabelas/explicito_tabelas.md`.*

**O efeito não é de raridade lexical.** A razão de frequência não prevê a diferença de escore no grupo de referência.

**Controle de moldura, com regras de decisão registradas antes da medição.** Cada frase recebeu um gêmeo com rótulo do Sul no lugar do nordestino — *Meu vizinho é catarinense* ao lado de *Meu vizinho é cearense*. Três regras foram fixadas antes: especificidade detectada, efeito acima de 0,08 excluído, ou inconclusivo.

| Condição | Diferença média (Nordeste − Sul) | Leitura |
|---|---|---|
| Macrorregião | −0,021 | exclui efeito acima de 0,08 |
| Topônimo | +0,011 | exclui efeito acima de 0,08 |
| Gentílico | +0,015 | inconclusivo (dispersão alta; exigiria cerca de 42 frases) |
| Terceira pessoa | +0,026 (p ajustado 0,041) | especificidade detectada — pequena, exploratória e não replicada nas frases novas isoladamente |

*Fonte: `experimentos/resultados/tabelas/moldura_tabelas.md`.* Os gêmeos, sem Nordeste, já ficam acima do grupo de referência.

O contraste entre 2.1 e 2.2 é obtido com o mesmo modelo, a mesma métrica, o mesmo grupo de referência e a mesma estatística. **O modelo responde a rótulo geográfico explícito, e não à variedade linguística; quando a pessoa fala de si, o Nordeste não se destaca de outra região acima de 0,08, e em frases sobre terceiros há sinal pequeno a confirmar.** A resolução do gentílico e do sinal em terceira pessoa ficou para fase posterior ao dataset.

### 2.3 Nenhum viés depreciativo sobrevive ao controle de tokenização — com um sinal exploratório

As medições anteriores empregam a diferença de escore em valor absoluto, o que responde se o modelo distingue, e não se ele deprecia. A medida com sinal foi executada em separado, sobre as mesmas medições, com 20 frases por condição.

Na análise completa, macrorregião (+0,2119) e terceira pessoa (+0,1571) aparecem como depreciativas, com p ajustados de 0,0004 e 0,0020. **Os dois efeitos não sobrevivem ao controle do artefato de tokenização:** restrita a análise a atributos de token único, nenhuma condição sobrevive à correção — macrorregião +0,0945, p ajustado 0,40 —, enquanto o controle positivo sobrevive a 0,0004.

**Há, porém, um sinal a declarar.** A estimativa restrita da macrorregião subiu de +0,031, com oito frases, para +0,095, com vinte; e, num reagrupamento exploratório, rótulos de pessoa (*nordestino*, *baiano*) rendem +0,12 com p = 0,006. O reagrupamento é posterior aos dados e não tem estatuto de resultado, mas é o primeiro sinal de direção na versão controlada. Com 20 frases, a análise de direção só exclui vieses a partir de cerca de 0,10, e a confirmação ficou para fase posterior ao dataset.

*Fonte: `experimentos/resultados/tabelas/valencia_tabelas.md`, com o grupo de referência de 86 pares.*

O mecanismo está identificado: entre os atributos de mais de um token, os desfavoráveis fragmentam-se mais que os favoráveis, com média de 2,5 subtokens contra 2,0.

### 2.4 Contribuições de método

Quatro achados independem de haver ou não viés a medir, e constituem contribuição autônoma:

- **Assimetria de tokenização alinhada ao eixo de prestígio.** Das dezesseis ocupações de alto prestígio testadas, quinze são palavra inteira no vocabulário do modelo; os itens de baixo prestígio fragmentam-se sem exceção. Segue-se que estudo de viés ocupacional em português por preenchimento de máscara mede a segmentação do tokenizador. O item 2.3 acima é a demonstração da consequência em caso concreto.
- **Grupo de referência amplo, e não calibração da frequência.** Com 86 pares não regionais, a razão de frequência entre os itens trocados não prevê a diferença de escore (R² = 0,008), o que revogou a leitura anterior de efeito real e modesto. O ruído no nível do par é da ordem do efeito procurado, e o que ele exige é grupo de referência amplo e estatística por conglomerado; a variação dominante entre pares vem da moldura do enunciado.
- **Unidade de replicação.** As medições de um mesmo par compartilham o enunciado e não são independentes. Tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza.
- **Armadilhas de atribuição em corpus construído a partir de plataforma.** Quatro classes de canal satisfazem critérios geográficos sem servir ao propósito, sendo a mais grave o falante migrante — erro que, por seguir o vetor migratório dominante, atenua sistematicamente o contraste medido e produz aparência de ausência de viés.

*Fonte: `docs/achados_para_o_artigo.md`, itens 1.1, 1.7, 1.14 e 1.16.*

### 2.5 Corpus de fala coletado

**Coleta concluída em 14/09/2026:** 83 arquivos, 7,96 h de áudio, de 65 canais, com **216 falantes distintos** apurados por comparação de vozes e conferência humana. Todos os estados superam o piso de 20 pessoas úteis sob o teto de 5% por falante: PB 23, PE 21, CE 27, BA 22, SP 21 e RJ 23. As transcrições foram anonimizadas em 02/09/2026.

*Fontes: `docs/dataset-spec.md`, "Camada de execução, em números"; `docs/anonimizacao.md`.*

No piloto, sobre 45.132 palavras transcritas, mediram-se 13,6 contextos de palatalização de /t,d/ diante de /i/ por minuto de fala.

*Fonte: `experimentos/resultados/tabelas/densidade_palatalizacao.md`.*

---

## 3. O que está em andamento

**O fechamento do conjunto de dados v1**, com escopo congelado e plano de dezessete itens em `docs/roadmap.md`.

- **Pares mínimos: concluídos.** 306 pares medidos — 86 de referência não regional, 80 de menção explícita com 80 gêmeos de moldura, 25 de sinalização implícita e 35 de controle. Metas atingidas: 80 no grupo de referência e 20 frases com gêmeo por condição de menção explícita. Os 25 implícitos foram validados (seção 4.2).
- **Corpus de áudio: coleta concluída, validação por fazer.** Restam três frentes de trabalho humano: erro de transcrição por variedade (cerca de 2 h de transcrição manual, de 8 a 16 h de trabalho), coerência dialetal (escuta de 60 falantes) e participação de ouvinte (escuta de 2 arquivos).

*Fontes: `experimentos/resultados/dados/pares_minimos.json`; `docs/plano_corpus/03-validar.md`.*

---

## 4. O que permanece em aberto

### 4.1 Medição

O **eixo de prestígio ocupacional** não é mensurável pela métrica empregada neste modelo: das quatro ocupações de baixo prestígio, apenas uma é de token único, e é também a única do feminino, de modo que restringir a análise trocaria um confundidor por outro. Exige AUL em lugar de pseudo-verossimilhança. No artigo de recurso deixou de ser pré-requisito, e a equipe decidirá entre medi-lo e declará-lo como limitação.

### 4.2 Validação

**Pares mínimos: validados sem juízes.** A equipe não dispõe de contatos nos estados-alvo, o que inviabilizou os juízes falantes nativos previstos no protocolo. Os 25 pares de sinalização implícita foram validados, em substituição, por fonte dialetológica documentada e por ocorrência no corpus próprio, com conferência humana dos trechos: **7 confirmados, 5 confirmados com ressalva e 13 não confirmados no corpus**. "Não confirmado" não equivale a reprovado, porque o corpus, de 7,96 h, não permite reprovar traço raro. Os demais pares dispensam essa validação — a região está escrita no enunciado, ou o enunciado é neutro.

**Corpus: validação por fazer.** Não há ainda transcrição humana de referência, de modo que a taxa de erro do reconhecimento automático não foi medida por variedade.

### 4.3 Publicação dos dados

As condições para publicar o corpus estão satisfeitas: os nomes próprios de terceiros foram mascarados em 02/09/2026, a transcrição pode ser publicada mediante essa anonimização, e as licenças estão definidas — CC BY 4.0 para dados e documentação, MIT para código, e declaração de uso em pesquisa para as transcrições. **Pergunta à orientação:** se questionário ou consulta a pessoas, caso a rede do programa permita juízes como reforço, exige comitê de ética, dado que a dispensa registrada se referia ao corpus de conteúdo público.

### 4.4 Enquadramento do artigo

**Decidido em 15/09/2026: dois artigos.** O primeiro é de recurso e método — os dois conjuntos de dados, com as medições no BERTimbau como demonstração de uso. O segundo, de análise de sentimento com PLN, será construído sobre o conjunto publicado.

---

## Advertências de leitura, obrigatórias

Registradas em `docs/achados_para_o_artigo.md` e reproduzidas aqui por serem o ponto em que o texto do artigo mais facilmente erraria:

1. **Não afirmar que o BERTimbau não apresenta viés regional.** O que se estabeleceu é que este instrumento, neste modelo, nesta métrica e neste repertório de atributos não detecta viés. Não detectar não é demonstrar ausência.
2. **Não citar como resultado os vieses significativos da análise completa** (+0,2119 na macrorregião; +0,1952 com oito frases). Pertencem à discussão sobre assimetria de tokenização, e não à seção de resultados.
3. **Não citar valor algum do eixo ocupacional**, em direção alguma, enquanto não houver medição válida.
4. **Não escrever como achado** o reagrupamento entre rótulo de pessoa e rótulo de lugar. Além de posterior aos dados, desapareceu no controle de moldura de 14/09/2026.
5. **Não afirmar que o modelo responde especificamente ao Nordeste**, nem que está demonstrado que não responde. O que se estabeleceu é a ausência de especificidade acima de 0,08 na autoidentificação em macrorregião e topônimo, o gentílico sem resolução e um sinal pequeno e exploratório em terceira pessoa.
6. **Não afirmar que a resposta não é depreciativa, nem que é.** Nenhum viés sobrevive ao controle de tokenização, mas há sinal exploratório em rótulos de pessoa.
7. **Não afirmar que os pares foram validados por juízes.** Foram validados por fonte e corpus.
