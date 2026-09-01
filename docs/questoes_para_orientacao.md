# Questões para a orientação

**Preparado em:** 29/08/2026.
**Função.** Reunir, em forma de pergunta fechada, tudo que o projeto não pode decidir sozinho. Cada item traz o contexto mínimo para ser respondido sem consultar os demais documentos, e indica o que depende da resposta.

**Como ler.** Os blocos estão em ordem de consequência, e não de assunto. O Bloco 1 determina o que os outros significam; os Blocos 2 e 3 travam a publicação; os demais são resolvíveis em qualquer ordem.

**Estado do projeto, em três frases.** O modelo não responde à sinalização dialetal implícita, em quatro famílias de marcadores testadas. Responde à menção explícita da região, acima do que a frequência lexical prevê, e o efeito concentra-se em rótulos de pessoa e não de lugar. Essa resposta, porém, não é depreciativa de forma detectável — o único viés candidato revelou-se artefato de tokenização.

---

# Bloco 1 — Enquadramento do artigo

Este bloco determina o que fazer com todo o resto. Enquanto não for respondido, não há critério para decidir o volume do dataset nem o esforço a investir em medição adicional.

## 1.1 O contraste entre sinalização implícita e explícita basta como resultado principal de um artigo?

**Contexto.** Não há viés medido. O que há é um contraste obtido com a mesma régua, a mesma calibração e a mesma estatística: quatro famílias de marcadores dialetais implícitos não produzem resposta no modelo, e a menção explícita da região produz, sobrevivendo à correção para múltiplas comparações. A leitura proposta é que o modelo associa conteúdo à **categoria regional nomeada** e não à **variedade linguística que a indicia**.

**Do que depende a resposta.** Se sim, o artigo é sobre representação e o dataset se dimensiona para sustentar um nulo bem-posto. Se não, é preciso ou trocar de modelo, ou reposicionar o trabalho como artigo de recurso e método.

## 1.2 Para qual veículo devemos escrever?

**Contexto.** As opções consideradas são BRACIS, PROPOR, STIL, LREC e trilhas de *fairness* em ACL ou EMNLP. A moldura muda bastante entre elas, e um resultado negativo é recebido de modo diferente em cada uma — LREC valoriza recurso, as trilhas de *fairness* tendem a esperar efeito medido.

**Do que depende a resposta.** O tamanho exigido do conjunto de pares, a proporção entre método e resultado no texto, e se a coleta de áudio prossegue.

## 1.3 Um resultado negativo bem controlado é publicável no veículo escolhido, ou precisamos de efeito positivo?

**Contexto.** O projeto tem um resultado que a literatura raramente reporta: um viés aparentemente significativo, a p = 0,049, foi identificado como artefato de tokenização e desfeito. Isso é contribuição de método, mas é contribuição negativa.

## 1.4 Vale testar o BERTimbau Large antes de fechar o enquadramento?

**Contexto.** Todas as medições foram feitas no BERTimbau Base. Se o Large responder à sinalização implícita, o artigo volta a ser sobre viés dialetal e o enquadramento muda por completo. O custo é de algumas horas de máquina, sem coleta nova.

**Do que depende a resposta.** Se sim, isso precede tudo. Se não, o enquadramento pode ser fechado agora.

## 1.5 Oito pares por condição é defensável na submissão, ou precisamos escalar antes?

**Contexto.** Os resultados atuais repousam sobre oito pares por condição, com estatística por conglomerado no nível do par e correção de Holm. Calculamos que excluir efeitos de viés acima de 0,08 exigiria 37 pares por condição e 80 no grupo de referência — cerca de 250 pares no total, contra os 1.508 do CrowS-Pairs.

---

# Bloco 2 — Questões jurídicas e éticas

Estas travam a publicação do dataset e **não devem ser respondidas pela equipe técnica**. Se a orientação também não for a instância adequada, a pergunta é a quem encaminhar.

## 2.1 Podemos publicar as transcrições dos vídeos, ou apenas os identificadores? — RESOLVIDA em 31/08/2026, pela equipe

**Decisão:** sim, pode publicar, condicionado à anonimização dos nomes próprios de terceiros já exigida pelo protocolo (`docs/protocolo.md` §1.4.2). A pergunta original registrava que essa decisão não deveria ser tomada pela equipe técnica sozinha; foi, ainda assim, e fica registrado aqui por transparência. Dois pontos permanecem abertos, mais estreitos que a pergunta original: a anonimização em si não está implementada, e a licença específica sob a qual a transcrição será distribuída não foi fixada (ver 2.2).

**Contexto original.** O protocolo do projeto fixou publicar identificadores de vídeo e código, nunca o áudio bruto. Nunca decidiu sobre a **transcrição**, que não é nem uma coisa nem outra. Corpora de fala publicam transcrições rotineiramente, mas uma transcrição é obra derivada do vídeo, e o conteúdo é de terceiros.

## 2.2 Sob que licença podemos publicar, e o que exatamente ela cobre?

**Contexto.** A orientação técnica é licença em duas camadas — CC BY 4.0 para o que é autoria do projeto e MIT para o código —, decidida em 31/08/2026 (`LICENSE`, `LICENSE-DATA.md`). A transcrição está agora autorizada a ser publicada (ver 2.1), mas segue fora do escopo do CC BY: licenciar exigiria titularidade que o projeto não tem sobre a fala de terceiros. Não sabemos se essa cautela é necessária ou excessiva frente à prática da área, nem que licença (se alguma) se aplicaria à transcrição especificamente.

## 2.3 O projeto precisa de aprovação de comitê de ética em pesquisa? — RESOLVIDA em 31/08/2026, pela equipe

**Decisão:** não é necessária, por determinação da equipe (`docs/ficha_conjunto.md`, A.3). A ausência de consentimento dos falantes permanece registrada como limitação do método, independentemente da dispensa.

**Contexto original.** Os falantes não consentiram para fins de pesquisa: falaram publicamente, para outra finalidade. Não se coleta dado sensível nem geolocalização precisa, e os nomes próprios de terceiros serão mascarados. Ainda assim, trata-se de fala humana identificável associada a rótulo de procedência regional.

## 2.4 A ficha do conjunto precisa de aprovação institucional antes de publicada?

**Contexto.** Rascunhamos uma ficha no formato consolidado por Gebru et al., em `docs/ficha_conjunto.md`, com seção de **usos desaconselhados**. O primeiro item adverte que o conjunto se presta, sem adaptação, a treinar classificador de procedência de falante — o que inverteria o propósito da pesquisa e criaria risco de discriminação.

---

# Bloco 3 — Validação metodológica

Perguntas sobre se o que fizemos se sustenta em revisão por pares.

## 3.1 O delineamento de calibrar a resposta à frequência e ler o resíduo é defensável?

**Contexto.** Comparar guises por diferença de escore mede raridade lexical quando os guises não são pareados em frequência, e o pareamento perfeito é inalcançável para marcadores dialetais. Adotamos, em lugar dele, ajustar uma reta de |Δ| contra o logaritmo da razão de frequência **sobre pares não regionais**, e medir o resíduo de cada par dialetal contra essa reta. Não encontramos precedente dessa solução na literatura consultada.

**Do que depende a resposta.** É a peça de método sobre a qual todos os resultados repousam. Se não se sustentar, os resultados caem junto.

## 3.2 Como apresentar um reagrupamento que foi formulado depois de ver os dados?

**Contexto.** Registramos antes da medição a previsão de que o efeito decresceria com a granularidade do rótulo — macrorregião, gentílico de estado, topônimo. Não foi o que ocorreu: o corte real é entre **rótulo de pessoa** e **rótulo de lugar**, e atravessa uma das condições. O reagrupamento é forte, com doze pares em doze acima da reta, mas é posterior aos dados.

**Do que depende a resposta.** Se deve ir ao texto como achado exploratório declarado, ficar de fora, ou motivar uma replicação em conjunto novo antes da submissão.

## 3.3 A unidade de replicação em *matched-guise probing* é o par, e não a medição — isso é ponto conhecido ou contribuição?

**Contexto.** Um instrumento desses multiplica pares por molduras por atributos, e as medições de um mesmo par compartilham o enunciado. Tratá-las como replicações independentes infla o tamanho amostral por uma ordem de grandeza. Adotamos estatística por conglomerado no nível do par. Não encontramos a exigência explicitada na literatura consultada, mas pode ser conhecimento tácito da área.

## 3.4 A classificação de valência dos atributos precisa passar por juízes?

**Contexto.** A medida de viés é inteiramente definida por uma partição dos atributos entre favoráveis e desfavoráveis, feita pelo projeto por circulação corrente e declarada em código. Itens ambíguos foram excluídos em vez de arbitrados. Não foi validada externamente.

## 3.5 O achado sobre tokenização é publicável separadamente?

**Contexto.** Medimos que, das dezesseis ocupações de alto prestígio testadas, quinze são palavra inteira no vocabulário do BERTimbau, enquanto os itens de baixo prestígio se fragmentam sem exceção — *pedreiro*, *faxineiro*, *lavrador*, *costureira*. Segue-se que estudo de viés ocupacional em português por preenchimento de máscara mede a segmentação do tokenizador e a reporta como viés do modelo. Demonstramos a consequência num caso concreto.

---

# Bloco 4 — Acesso bibliográfico

Pendências que dependem de acesso físico ou de contato com autores.

## 4.1 É possível conseguir o capítulo de Oliveira (2017)?

**Referência.** *O imperativo gramatical nas capitais do Nordeste*, em Lopes, Oliveira e Parcero (orgs.), *Estudos sobre o português do Nordeste: língua, lugar e sociedade*, Blucher, 2017, p. 27–44.

**Por que importa.** Duas fontes secundárias divergem sobre a direção do marcador do imperativo em Fortaleza — uma indica predomínio subjuntivo, outra indica indicativo favorecido. O item do instrumento que representa o Ceará está **suspenso** por causa disso.

## 4.2 Devemos escrever aos autores de Melo e Souza (2026)?

**Contexto.** Na Tabela 7 daquele trabalho, o marcador "nordeste" recebe estima **superior** à do marcador "sudeste" em três dos quatro modelos avaliados, o que parece divergir do que o texto afirma. É leitura nossa da tabela publicada, não confirmada. O ponto é relevante porque o trabalho é o mais próximo do nosso e a diferenciação depende dele.

## 4.3 Como localizar Cavalcante (2007)?

**Contexto.** Citado por Santos e Vitório (2025) como o estudo com maior índice de negação pós-verbal. Interessa avaliar se o contexto restringe a generalização do marcador. Não bloqueia nada.

---

# Bloco 5 — Operacional

## 5.1 Como recrutar os juízes falantes nativos?

**Contexto.** O protocolo de validação exige mínimo de cinco juízes por variedade, em seis variedades — trinta pessoas. Cada juiz avalia enunciados embaralhados, respondendo a três perguntas: de qual estado é quem falou, se soa natural, e se soa como imitação.

**Do que depende a resposta.** O protocolo está pronto e nunca foi aplicado. É o passo que valida o instrumento, e sem ele nenhum item do conjunto pode ser declarado validado.

## 5.2 Devemos reforçar a cobertura de Pernambuco e Bahia, ou trabalhar com o que há?

**Contexto.** Na camada de vlogs, o grupo de controle tem treze vozes por estado, contra quatro em Pernambuco e seis na Bahia. Uma análise sobre subamostra balanceada ficaria limitada pelo estado mais fraco — quatro falantes por estado. Reforçar exige nova rodada de busca, com rendimento observado de cerca de um canal aproveitável a cada oito candidatos.

## 5.3 Qual é a vinculação institucional e o financiamento a declarar? — RESOLVIDA em 31/08/2026, pela equipe

**Decisão:** sem vínculo institucional a declarar (`docs/ficha_conjunto.md`, A.1). O contato de manutenção e o canal de erros também foram confirmados (A.7): repositório em `github.com/Aryazinha/vies-nordeste-bertimbau`, com *issues* do GitHub.

## 5.4 O protocolo metodológico deve ser versionado no repositório público?

**Contexto.** O documento que contém o protocolo, as ameaças à validade e o esquema de dados está deliberadamente fora do versionamento, por decisão de agosto. Como os demais documentos remetem às suas seções, quem acessar o repositório encontra dezenas de referências a um arquivo ausente — o que afeta a reprodutibilidade se o material acompanhar uma submissão.

---

# Ordem sugerida, se o tempo for curto

Se houver tempo para poucas perguntas, esta é a ordem de retorno:

1. **1.1 e 1.2** — enquadramento e veículo, porque determinam o significado de tudo o mais.
2. **1.4** — o BERTimbau Large, porque precede o fechamento do enquadramento e é barato.
3. **2.2** — a licença específica da transcrição, porque trava a publicação e tem prazo próprio (2.1 e 2.3 já foram decididas pela equipe, ver acima).
4. **3.1** — o delineamento de calibração, porque é a peça sobre a qual os resultados repousam.

O restante pode ser resolvido por escrito depois.

---

# Documentos de apoio

Se a orientação quiser examinar o material:

| Para | Ler |
|---|---|
| Estado geral e plano | `docs/roadmap.md` |
| O que pode e o que não pode ser escrito | `docs/achados_para_o_artigo.md` |
| O resultado central | `experimentos/resultados/relatorios/explicito.md` |
| Especificação do dataset | `docs/dataset-spec.md` |
| Ficha dos conjuntos | `docs/ficha_conjunto.md` |
