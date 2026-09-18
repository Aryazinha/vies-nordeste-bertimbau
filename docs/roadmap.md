# Roadmap do Projeto

**Função deste arquivo.** Plano único e canônico do projeto. Toda proposta de trabalho deve ser situada em um dos passos abaixo, e não apresentada como lista nova. A numeração dos passos é estável: passos concluídos permanecem na tabela com a situação atualizada, e nenhum passo é renumerado.

**Última atualização:** 28/08/2026

**Documentos irmãos.** `docs/protocolo.md` reúne o método — protocolo, esquema de dados e ameaças à validade —, e é o arquivo a citar em lugar do `CLAUDE.md`, que permanece fora do versionamento. `docs/resumo_para_orientacao.md` relata o estado do projeto em duas páginas. `docs/achados_para_o_artigo.md` separa o que já pode ser afirmado em texto submetido do que não pode, com a condição precisa que liberaria cada item em suspenso — é o filtro a consultar antes de escrever qualquer trecho do artigo. `docs/pendencias.md` registra tudo que está aberto — lacunas, decisões não tomadas, verificações devidas e melhorias identificadas. Este arquivo diz o que fazer em seguida; aquele diz o que não pode ser esquecido. Consultar ambos ao retomar o trabalho.

---

## Princípio de ordenação

A contribuição publicável do projeto é o **dataset**. A lacuna identificada na literatura é a inexistência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro, e os precedentes diretos — CrowS-Pairs, French CrowS-Pairs — são artigos de dataset, nos quais o achado sobre o modelo é demonstração de uso, não a contribuição central.

Segue-se o critério de priorização: **trabalho que aproxima o projeto de ter os dados montados e validados tem precedência sobre refinamento do instrumento de medição.** Sondagem do modelo só se justifica quando altera quais itens entram no conjunto de dados.

---

## Os quatro passos

| # | Passo | Situação | Depende de |
|---|---|---|---|
| **1** | Teste de fumaça do instrumento | **Concluído** em 27/08/2026 | — |
| **2** | Fechamento das pendências de citação e revisão editorial | **Concluído** em 27/08/2026 | — |
| **3** | Validação dos itens por juízes falantes nativos | Não iniciado, **suspenso** | ver passo 5 |
| **4** | Coleta do corpus de áudio | **Piloto executado** em 27/08/2026: 17 trechos, 1,55 h, esteira validada de ponta a ponta. Coleta em escala não iniciada | — |

### Passo 1 — Teste de fumaça do instrumento (concluído)

Verificou a viabilidade do instrumento antes de investir em volume. Resultados em `experimentos/resultados/`. Três achados alteram o desenho:

- Duas das cinco molduras estavam inoperantes. `Quem falou isso é [MASK]` colapsa em pronomes; `estudou até o [MASK]` colapsa em expressão idiomática. Substitutas testadas e aprovadas em `experimentos/resultados/relatorios/molduras_alternativas.md`.
- O vocabulário de estereótipo negativo é majoritariamente multi-token no BERTimbau, ao passo que as ocupações de alto prestígio são todas de token único. O confundidor de frequência está materializado no tokenizador, alinhado ao eixo de interesse. AUL passa de recomendação a condição de possibilidade.
- A sensibilidade ao *guise* concentra-se no léxico. O bloco morfossintático puro apresenta divergência de Jensen-Shannon mediana de 0,0023 bits, contra 0,0144 do bloco lexical e 0,0963 da referência de conteúdo distinto.

### Passo 2 — Pendências de citação e revisão editorial (concluído)

Fechadas as pendências de cobertura dialetológica de Ceará e Bahia; localizada a referência de Oliveira (2017); lido integralmente Melo e Souza (2026); criado `docs/referencias.bib`; todos os documentos convertidos para registro acadêmico formal. Duas correções de conteúdo decorrentes constam do log v1.7 do `CLAUDE.md`.

### Passo 3 — Validação por juízes falantes nativos

Aplicação do Filtro 1 descrito em `docs/pares_minimos_v1.md`, seção 7. Não deve ser iniciado antes da conclusão do passo 3.1, sob pena de consumir a disponibilidade dos juízes com itens que o instrumento descartaria.

**3.1 — Correção do instrumento (bloqueia o passo 3).** Substituir as molduras inoperantes pelas alternativas já testadas; refazer o conjunto de atributos considerando a segmentação em subtokens; decidir quais atributos são lidos por probabilidade de máscara e quais exigem AUL. Trabalho de escrivaninha, da ordem de horas.

**3.1 — Correção do instrumento. Concluído** em 28/08/2026. Molduras inoperantes substituídas pelas testadas; conjunto de atributos reconstruído a partir do vocabulário do modelo, por `experimentos/selecionar_atributos.py`. A correção revelou a assimetria de tokenização por eixo de prestígio, hoje um dos achados sustentados do artigo.

**Por que o passo 3 está suspenso, e não apenas bloqueado.** Convocar juízes exige um conjunto de itens que valha a pena validar, e o passo 5 mostrou que o conjunto atual não produz resposta mensurável no modelo. Validar itens que não medem nada gastaria a disponibilidade dos juízes sem contrapartida.

**Substituído em 15/09/2026.** A equipe registrou não dispor de contatos nos estados-alvo, o que inviabiliza o recrutamento. O passo passa a ser executado **sem juízes**, e só onde é exigível: os 25 pares de sinalização implícita são validados por fonte dialetológica documentada e por ocorrência no corpus de áudio próprio; menção explícita e calibração ficam fora, com justificativa declarada. Com 7,96 h de corpus, a ocorrência confirma um traço mas não reprova traço raro por ausência. A ausência de juízes vai como limitação, e o acesso a juízes pela rede da orientação fica como reforço eventual (`docs/pendencias.md` 2.14).

### Passo 4 — Coleta do corpus de áudio

Execução do pipeline já implementado em `pipeline_coleta_piloto/`. É o passo mais longo em tempo de calendário — coleta, transcrição e verificação manual de WER e DER — e é pré-requisito do Filtro 2 do protocolo de validação, segundo o qual um marcador só integra o experimento se ocorrer em fala espontânea no corpus coletado. Por isso está no caminho crítico, ainda que seja o menos avançado.

**4.1 — Lista de fontes. Concluído** em 27/08/2026. Lista semente de 32 canais verificados, em `docs/fontes_coleta.md` e `pipeline_coleta_piloto/fontes.json`. Estabelecida a regra de atribuição por canal, depois de o levantamento por consulta de busca ter demonstrado contaminação entre estados.

**4.2 — Meta de volume. Concluído** em 27/08/2026. Derivada do requisito estatístico do Filtro 2 em `experimentos/meta_volume_corpus.py`, com resultado em `experimentos/resultados/historico/meta_volume.md`: 4,1 h de fala do locutor-alvo por estado, equivalentes a 8,3 h de áudio bruto, totalizando cerca de 50 h no conjunto dos seis estados.

**4.3 — Piloto executado** em 27/08/2026. Dezessete trechos, 1,55 h, seis estados e três camadas. A esteira funciona de ponta a ponta; as medições estão em `experimentos/resultados/relatorios/piloto_medicoes.md`. Três resultados alteram o planejamento: o rendimento por camada é bem superior ao suposto, o que reduziria a meta de 50 h para cerca de 38 h; não há indício de que a transcrição penalize a fala nordestina, o que removeria um confundidor; e a primeira aplicação do Filtro 2 não registrou nenhuma ocorrência do léxico regional em que o Bloco B do instrumento se apoia.

**Restrição prática.** A transcrição com `large-v3` em CPU opera a uma fração do tempo real. Para escala, o processamento vai para ambiente com GPU, e essa conta de tempo deve entrar no planejamento antes da coleta, não depois.

---

## Situação dos dois conjuntos de dados

Atualizada em 15/09/2026. A versão de 28/08/2026 está no histórico do repositório.

| Conjunto | Situação |
|---|---|
| **Corpus de áudio** | **Coleta concluída, validação por fazer.** Entregável autônomo desde 29/08/2026. 83 arquivos, 7,96 h, 65 canais, 216 falantes distintos; todos os estados acima do piso de 20 pessoas úteis sob o teto de 5% por falante. Transcrições anonimizadas. Restam erro de transcrição por variedade, coerência dialetal e participação de ouvinte (itens 5, 6, 9, 10 e 11 do plano de fechamento, ao final deste arquivo). |
| **Pares mínimos** | **Concluídos para a v1.** 306 pares medidos, esquema 1.3, licença CC BY 4.0: 86 de referência não regional, 80 de menção explícita com 80 gêmeos de moldura, 25 de sinalização implícita e 35 de controle. Os 25 implícitos validados por fonte e corpus, sem juízes: 7 confirmados, 5 com ressalva, 13 não confirmados. Falta a ficha (item 7). |

### Por que a assimetria importa — histórico, superado

> **Superado em 15/09/2026.** O raciocínio abaixo descreve a situação de 28/08/2026, antes de o passo 5.3 ser adotado e de os pares serem concluídos. Conservado como registro.


O princípio de ordenação deste arquivo estabelece que a contribuição publicável do projeto é o dataset, e os precedentes adotados — CrowS-Pairs e French CrowS-Pairs — são artigos de conjunto de dados. Ocorre que o conjunto que sustentaria essa contribuição é o de **pares mínimos**, e é justamente o que não está definido. O corpus de áudio, bem especificado, tem no desenho original função **instrumental**: serve ao Filtro 2, isto é, a confirmar que os marcadores ocorrem em fala espontânea.

Duas consequências, registradas para a decisão do passo 5:

1. Enquanto o passo 5 não se resolver, não há critério para decidir **quais** pares mínimos construir, e escalar a coleta de áudio produz material cuja função de validação está suspensa junto com os marcadores que ela validaria.
2. Se o rumo adotado for o 5.3, o corpus de áudio deixa de ser instrumento e passa a ser **entregável autônomo** — corpus de fala regional documentado, com WER estratificado por variedade. Isso alteraria o que precisa ser definido a seu respeito: formato de distribuição, licença e ficha passariam a ser exigíveis também para ele.

---

## Fora de escopo por ora

- **Comparação com o BERTimbau Large.** Refinamento do instrumento de medição, não construção de dataset. Retomar apenas se e quando o conjunto estiver montado e o efeito medido no modelo Base se mostrar insuficiente para sustentar o artigo.

---

## Passo 5 — Viabilidade do desenho *matched-guise*

**Concluído** em 28/08/2026, e não previsto no plano original. Foi inserido porque investir em juízes e em dezenas de horas de coleta sem saber se o modelo responde ao guise seria apostar sem olhar a carta.

Resultado em `experimentos/resultados/relatorios/sensibilidade_guise.md`. Com controles que estabelecem piso e teto de sensibilidade: o instrumento detecta diferença de conteúdo a 6,32× o piso, mas os marcadores morfossintáticos ficam em 1,00×, e o efeito dos lexicais é reproduzido por um controle com palavras raras não regionais.

**Decisão de rumo, e é ela que destrava o resto:**

| Caminho | Custo | O que responde | Situação |
|---|---|---|---|
| **5.1** Marcadores construcionais pareados em frequência | baixo | se ainda existe instrumento possível neste modelo | **Concluído** em 28/08/2026 — resposta negativa |
| **5.2** BERTimbau Large, ou métrica baseada em representação | médio | se o limite é do modelo ou da métrica | Não iniciado |
| **5.3** Reposicionar como artigo de método e recurso | — | encerra a dependência de um resultado de viés | **Adotado em 15/09/2026** como primeiro artigo — ver "Situação do artigo" |
| **5.4** Menção explícita em volume | baixo | se o modelo responde ao rótulo regional, ainda que não à variedade | **Concluído** em 29/08/2026 — resposta afirmativa |
| **5.5** Direção do efeito, e não sua magnitude | baixo | se a resposta é preconceituosa, e não apenas diferente | **Concluído** em 29/08/2026 — nenhum viés de valência sobrevive |
| **5.6** Eixo ocupacional por AUL | baixo | o único eixo que o PLL não consegue medir neste modelo | **Adiado** em 15/09/2026 para logo após a conclusão da v1; declarado limitação na v1 |

Os quatro não se excluem. O 5.1 era o mais barato e determinava se os demais eram necessários; a resposta dele é que sim.

### 5.1 — Marcadores construcionais (concluído, resposta negativa)

Relatório em `experimentos/resultados/relatorios/construcional.md`; tabelas regeráveis em `tabelas/construcional_tabelas.md`.

**Desenho.** Como o pareamento perfeito de frequência é inalcançável para marcadores construcionais — os melhores candidatos apresentam razão de 5 a 11 vezes —, abandonou-se a comparação de medianas e adotou-se a **calibração da lei de frequência**: ajusta-se |Δ| contra log₁₀ da razão de frequência sobre 22 pares não regionais, e mede-se o **resíduo** de cada par dialetal contra essa reta. Toda estatística passa a operar no nível do par.

**Resultado.** A condição construcional apresenta resíduo médio de −0,0141, com três de dez pares acima da reta e p = 0,71. A pista que motivou o passo — o vocativo *menino* — não replica: seu irmão, o vocativo *rapaz*, apresenta o maior resíduo negativo da condição.

Somam-se agora **quatro famílias testadas sem efeito**: morfossintática, lexical, feixe e construcional. O caso mais limpo é a negação pós-verbal, cujos pares empregam as mesmas palavras em ordem diferente — razão de frequência 1,0 por construção — e cujo resíduo é negativo.

**Dois subprodutos que valem por si.** O controle de conteúdo funciona como controle positivo do método de resíduo (p = 0,0003 após Holm), o que torna o nulo legível. E a calibração revelou que a frequência explica bem menos do que o relatório anterior afirmava — R² = 0,180 —, o que **exigiu revisão do item 1.14** de `docs/achados_para_o_artigo.md`.

### 5.4 — Menção explícita em volume (concluído, resposta afirmativa)

Não estava previsto. Surgiu porque a condição de menção explícita é a **única** com resíduo consistente entre as regionais: cinco pares em cinco acima da reta, p = 0,026 bruto, 0,13 após Holm. E tem estrutura interna interpretável — os resíduos grandes são os que nomeiam a região como categoria; os que nomeiam estados ficam próximos de zero.

Exige um conjunto de pares de menção explícita em volume comparável ao dos demais blocos, com a distinção entre rótulo de região e nome de estado como variável de desenho. Detalhamento no item 2.8 de `docs/achados_para_o_artigo.md`.

**Relação com o restante.** É barato e usa a esteira já construída. Se confirmar, produz o contraste que sustentaria o artigo pretendido em nova chave — o modelo responde à categoria regional nomeada e não à variedade que a indicia. Se não confirmar, o 5.3 passa a ser o único caminho disponível.

**Resultado**, em `experimentos/resultados/relatorios/explicito.md`. Vinte e quatro pares novos, em três níveis de granularidade do rótulo, todos de autoidentificação. Duas condições produzem resíduo acima da reta da frequência **e sobrevivem à correção de Holm**: gentílico de estado, com p ajustado de 0,0012 e oito de oito pares acima da reta, e macrorregião, com 0,0038 e sete de oito. Topônimo não sobrevive. Não é efeito de raridade: as duas condições significativas têm as razões de frequência mais baixas do conjunto, e o par mais bem pareado — *pernambucano* contra *paulistano*, 1,1× — está entre os de maior efeito.

**É o primeiro resultado positivo do projeto**, e produz o contraste que sustenta o artigo: mesma régua, mesma calibração, mesma estatística, e quatro famílias implícitas sem efeito contra menção explícita com efeito.

**A predição registrada era ordinal e não se confirmou como escrita.** Previa-se macrorregião acima de gentílico; observou-se o inverso. A inspeção por par mostra que o corte não é de granularidade, e sim entre **rótulo de pessoa** e **rótulo de lugar** — distinção que atravessa a condição de macrorregião, cujos pares com *Nordeste* rendem +0,043 e os com *nordestino*, +0,172. Reagrupados, os rótulos de pessoa somam +0,162 com doze de doze pares acima da reta, contra +0,036 dos de lugar. O reagrupamento é posterior aos dados e está declarado como tal.

### 5.5 — Direção do efeito (concluído, sem viés detectável)

Aberto em 29/08/2026, pelo resultado do 5.4. Toda a medição do projeto até aqui emprega |Δ| em **valor absoluto**, o que responde a "o modelo responde ao guise?" e não a "o modelo responde com preconceito?" — um modelo que assinalasse ao guise nordestino atributos mais favoráveis produziria o mesmo número.

`experimentos/analise_valencia.py` implementa a medida com sinal, sobre as medições já existentes, em dois eixos separados: traço de caráter e prestígio ocupacional. O resultado é **inconclusivo, e por razão demonstrável**: o controle positivo não sobrevive à correção de Holm em nenhum dos dois eixos, ainda que apresente as maiores magnitudes brutas das duas tabelas. Com cinco pares no grupo de referência, a permutação não tem resolução. Pela lógica de interpretabilidade adotada desde o passo 5, quando o controle positivo não passa, nenhum nulo é legível.

**O que o passo exige:** conjunto maior de pares por condição, ampliação do grupo de referência para além dos cinco pares do controle neutro, e descarte do artefato de segmentação no eixo de ocupação — onde o gentílico de estado apresenta viés de −0,271, isto é, ocupações de alto prestígio tornando-se mais prováveis sob o guise nordestino, o que pode ser efeito da assimetria de tokenização registrada no item 1.1 de `docs/achados_para_o_artigo.md`.

**Por que é o caminho crítico.** Sem ele, o artigo pode afirmar que o modelo **distingue**, e não pode afirmar que **deprecia**. É a diferença entre um resultado sobre representação e um resultado sobre viés.

**Resultado, em 29/08/2026, em duas etapas.**

*5.5a — o subdimensionamento era erro de desenho, não falta de dados.* O grupo de referência da permutação era o `controle_neutro`, de cinco pares, quando a referência correta são os 26 pares não regionais já medidos — a mesma escolha feita para calibrar a reta da frequência. Corrigido, o controle positivo passa a sobreviver à correção de Holm no eixo de ocupação, a p de 0,0022, e a ficar a um passo do limiar no de caráter, a 0,0556 com p bruto de 0,0069. A verificação de sanidade passa: o controle neutro, testado contra o grupo do qual faz parte, resulta não significativo.

Com a correção, um efeito apareceu: a condição de macrorregião, no eixo de caráter, com viés de +0,1952, sete de oito pares positivos e p ajustado de 0,0486.

*5.5b — o efeito era artefato de tokenização.* Restrita a análise aos atributos de **token único**, o viés de macrorregião cai de +0,1952 para +0,0309, e de sete pares positivos para três. **A restrição aumentou o poder do teste em vez de reduzi-lo**: o controle positivo mais que dobra, de +0,2352 para +0,4758, com p ajustado passando de 0,0556 para 0,0013. Com menos atributos e mais poder, o efeito regional evaporou enquanto o do controle cresceu — o que exclui a leitura de sinal perdido por ruído.

O mecanismo está identificado: entre os atributos multi-token, os desfavoráveis fragmentam-se mais que os favoráveis, com média de 2,5 tokens contra 2,0. O mascaramento do alvo por inteiro, adotado justamente para neutralizar a assimetria de tokenização, **é correção parcial e não bastou**.

**Conclusão do passo.** Não há viés de valência detectável no eixo de caráter. O de prestígio ocupacional **não é mensurável por PLL neste modelo**, e a impossibilidade não é de volume: das quatro ocupações de baixo prestígio apenas *empregada* é de token único, e é também a única do feminino, de modo que restringir trocaria um confundidor por outro.

**Consequência para o artigo.** O trabalho não é sobre viés medido, e sim sobre o que o modelo distingue e o que não distingue, em três resultados que se sustentam mutuamente — e ganha uma contribuição de método que não existiria sem o resultado negativo: a demonstração, em caso concreto, de que uma medição de viés por pseudo-verossimilhança em português pode produzir efeito significativo inteiramente atribuível à tokenização. Detalhamento na seção "Situação do artigo", ao final deste arquivo.

### Revisão de 14/09/2026 — grupo de referência ampliado

Os passos 5.4 e 5.5 foram reanalisados com 86 pares não regionais distintos, em lugar de 26 (`docs/pendencias.md` 2.8 e 2.9). **As conclusões dos dois passos se mantêm:** gentílico de estado e macrorregião seguem sobrevivendo à correção de Holm, a 0,0004 e 0,0045, e o viés de macrorregião no eixo de caráter segue desfeito pela restrição a token único. Os valores citados acima são os da execução de 29/08/2026 e ficam como registro; os vigentes estão em `experimentos/resultados/tabelas/`.

**Uma premissa, porém, caiu.** Com o grupo ampliado, a razão de frequência não prevê a diferença de escore, e o item 1.14 de `docs/achados_para_o_artigo.md` foi reescrito. A "reta da frequência" dos passos 5.1 e 5.4 passa a valer como verificação de que a frequência não confunde a comparação, e não como correção dela.

**Controle de moldura, 14/09/2026 — o resultado de 5.4 muda de alcance.** Com predição e análise versionadas antes da medição, cada par de menção explícita recebeu um gêmeo com a mesma frase e rótulo do Sul no lugar do nordestino (`docs/pendencias.md` 2.10). A resposta ao rótulo nordestino não é detectavelmente maior que a ao rótulo do Sul — p ajustados de 0,36 na macrorregião e 0,80 no gentílico —, e a distinção pessoa/lugar desaparece. O "primeiro resultado positivo" de 5.4 subsiste como resposta a rótulo regional em enunciado sobre a pessoa, sem especificidade detectável para o Nordeste; o item 1.17 dos achados foi reformulado nessa direção.

### Revisão de 15/09/2026 — menção explícita a 20 frases pareadas

Com regras de decisão registradas antes da medição (`docs/pendencias.md` 2.12): sem especificidade para o Nordeste acima de 0,08 em macrorregião e topônimo; gentílico inconclusivo; especificidade pequena e exploratória na menção em terceira pessoa. Na direção, nenhum viés sobrevive na versão controlada da tokenização, mas as estimativas subiram e há sinal exploratório em rótulos de pessoa. Itens 1.17 e 1.19 dos achados reescritos; resolução do gentílico e do sinal de direção adiada para fase posterior ao dataset.

### 5.6 — Eixo ocupacional por AUL (aberto)

Aberto em 29/08/2026 pelo resultado do 5.5. É a última medição pendente para fechar a seção de Resultados, e a única que exige nova passagem pelo modelo: os escores de AUL não foram gravados, porque as medições dos passos 5.1 e 5.4 empregaram o atalho de PLL apenas, por economia de tempo de máquina.

A necessidade não é preferência entre métricas. É condição de possibilidade, pelo item 1.20 de `docs/achados_para_o_artigo.md`: o léxico ocupacional de baixo prestígio não integra o vocabulário do BERTimbau como palavra inteira, e nenhuma restrição de itens contorna isso.

Custo: uma execução sobre os 73 pares do conjunto acumulado, com as três métricas em vez de uma. Não depende de decisão da equipe.

**Sai do "fora de escopo".** A comparação com o BERTimbau Large fora afastada por ser refinamento de medição, e não construção de dataset. Com o dataset existindo e o desenho em questão, a comparação passa a responder à pergunta que bloqueia o projeto, e volta a ser pertinente.

---

## Situação do artigo

Em termos de estrutura de texto submetido:

| Seção | Situação |
|---|---|
| Introdução e motivação | sustentada |
| Trabalhos relacionados | sustentada |
| Fundamentação | sustentada |
| Método | sustentada, e com contribuições próprias (itens 1.1, 1.2, 1.7, 1.8, 1.16) |
| **Resultados** | **Completa** em 29/08/2026, em três partes: nulo sobre a sinalização implícita (1.13, 1.14, 1.15); resposta à menção explícita (1.17, 1.18); e ausência de organização por valência nessa resposta (1.19). O eixo ocupacional permanece sem medição válida (1.20) |
| Ameaças à validade | madura, e mais desenvolvida que o usual |
| Conclusão | escrevível na chave do terceiro caminho abaixo, que passou a existir em 29/08/2026 |

**Dois caminhos possíveis, não excludentes.**

O primeiro é o artigo pretendido: medição de viés dialetal implícito no BERTimbau. Exige instrumento corrigido e validado, corpus em volume suficiente para o Filtro 2, e a medição propriamente dita. É o de maior alcance e o mais distante.

O segundo é um **artigo de recurso e método**: o conjunto de pares mínimos para variação regional do português brasileiro, o protocolo de validação em dois filtros, o dimensionamento por requisito de detecção, e os achados sobre tokenização e sobre construção de corpus a partir de plataforma. Os precedentes que o projeto adota — CrowS-Pairs e French CrowS-Pairs — são exatamente dessa natureza, com a medição no modelo servindo de demonstração de uso. É alcançável com o que já existe, mais a validação por juízes, e constrói o terreno do primeiro.

A escolha é da equipe. Registre-se apenas que, no estado atual, o segundo caminho está muito mais próximo do que o primeiro.

**Atualização de 28/08/2026.** O teste construcional altera a relação entre os dois caminhos, e não apenas a distância a cada um.

O primeiro caminho deixa de estar apenas distante e passa a ter uma condição declarada: exige que alguma sinalização dialetal produza resposta no modelo, e quatro famílias já foram testadas sem que nenhuma produzisse. Prossegui-lo significa trocar de modelo ou de métrica — os caminhos 5.2 do roadmap —, e não acrescentar itens ao instrumento atual.

O segundo caminho, em contrapartida, ganhou material que não tinha. A seção de Resultados deixa de estar vazia: o nulo sobre quatro famílias, com controle positivo, confundidor de frequência descontado por calibração e teste de significância, é resultado publicável na chave de um artigo de método. Acrescentam-se as duas contribuições metodológicas novas — a calibração da resposta à frequência (1.14, revisado) e a unidade de replicação por par (1.16).

Há ainda uma terceira possibilidade, que não existia antes e que combina os dois: um artigo cuja pergunta seja **por que a sinalização implícita não produz resposta onde a explícita produz** (item 2.8). Depende inteiramente da confirmação de 2.8 em volume, e é a única linha em que o resultado sobre o modelo voltaria a ser a contribuição central.

**Atualização de 29/08/2026 — o terceiro caminho deixou de ser possibilidade.** O item 2.8 foi confirmado em volume e promovido a 1.17: duas condições de menção explícita sobrevivem à correção de Holm, com razões de frequência mais baixas que as de qualquer condição dialetal. O contraste que aquele parágrafo tratava como hipotético está medido.

Segue-se uma recomendação, e não apenas o registro de uma opção. **O artigo a escrever é o do terceiro caminho**, cuja pergunta é o contraste entre sinalização implícita e explícita, pelas seguintes razões:

- É a única chave em que os dois blocos de resultado se sustentam mutuamente. O nulo sobre quatro famílias implícitas, isolado, é um resultado fraco e atacável como falha de instrumento; ao lado de um positivo obtido com **a mesma régua, a mesma calibração e a mesma estatística**, torna-se demonstração de que o instrumento funciona e de que a diferença está no fenômeno.
- Incorpora integralmente as contribuições de método do segundo caminho — tokenização (1.1), molduras (1.2), armadilhas de corpus (1.7), dimensionamento (1.8), unidade de replicação (1.16), calibração da frequência (1.14) —, que passam de contribuição central a fundamentação do resultado.
- Reposiciona a literatura de forma favorável: Hofmann et al. (2024) encontram, em modelos alinhados, preconceito encoberto preservado sob manifesto suprimido; o BERTimbau Base, não alinhado, apresenta o padrão inverso. E o contraste com Melo e Souza (2026) deixa de ser diferenciação defensiva e passa a ser complementaridade — eles mediram o eixo explícito, que é justamente o que aqui responde.
- Reconduz à hipótese de mecanismo sobre o brWaC com evidência nova: a associação com o **rótulo** existe, e a associação com a **forma linguística** não. Um corpus sem estratificação geográfica explicaria exatamente esse padrão. *Qualificação de 14/09/2026:* a associação com o rótulo não se mostrou específica do Nordeste — rótulos do Sul, na mesma frase, produzem resposta equivalente —, o que enfraquece a leitura de mecanismo centrada na sub-representação nordestina.

**Atualização de 29/08/2026 — a condição que faltava foi cumprida, e a resposta muda o título.** O passo 5.5 mediu a direção do efeito. Não há viés de valência detectável: o único candidato dissolveu-se ao se controlar o artefato de tokenização, justamente quando o poder do teste aumentou.

O artigo, portanto, **não é sobre viés medido**. É sobre o que o modelo distingue e o que não distingue, com três resultados que se sustentam mutuamente:

1. Não responde à sinalização dialetal implícita, em quatro famílias (1.15).
2. Responde à menção explícita de região; sem especificidade para o Nordeste acima de 0,08 na autoidentificação, com sinal pequeno e exploratório em terceira pessoa (1.17, reescrito em 15/09/2026).
3. Essa resposta não se organiza por valência dos atributos de caráter (1.19).

**E ganha uma contribuição metodológica que não existiria sem o resultado negativo:** a demonstração, em caso concreto, de que uma medição de viés por pseudo-verossimilhança em português pode produzir efeito significativo inteiramente atribuível à assimetria de tokenização (1.1, consequência demonstrada, e 1.20). O projeto encontrou um viés aparente a p = 0,049 e o desfez. Isso é resultado de método com valor próprio, e é o tipo de coisa que a literatura de *bias probing* raramente reporta.

**A ressalva que preserva a honestidade do texto:** não detectar não é demonstrar ausência. O eixo ocupacional segue sem medição válida, a classificação de valência não passou por juízes, e, desde 15/09/2026, são 20 frases por condição de menção explícita, com sinal exploratório de direção em rótulos de pessoa declarado em 1.19.

**Decisão de 15/09/2026 — dois artigos, e o primeiro é o do conjunto de dados.** A equipe dividiu a produção em duas publicações:

1. **Primeiro artigo: recurso e método** — o segundo caminho acima, que é o passo 5.3. A contribuição central são os dois conjuntos de dados — o corpus de fala regional e os pares mínimos com desenho pareado —, com protocolo de construção e validação. As medições no BERTimbau (1.15, 1.17, 1.19) entram como **demonstração de uso** e caracterização do recurso, no papel que ocupam no CrowS-Pairs, e as contribuições de método (1.1, 1.14, 1.16, e o controle de moldura de 1.17-A) entram como achados de construção.
2. **Segundo artigo: análise de sentimento com PLN**, construída sobre o conjunto publicado (`docs/pendencias.md` D10).

**Isto substitui a recomendação de 29/08/2026 pelo terceiro caminho.** Duas razões tornam a mudança coerente com o estado do projeto, e não apenas preferência. Primeiro, o contraste que sustentava aquele caminho enfraqueceu: desde o controle de moldura, a resposta à menção explícita não se mostrou específica do Nordeste (1.17), e um artigo centrado no modelo perderia seu resultado positivo mais forte. Segundo, o artigo de recurso não depende de haver viés detectado, e acomoda sem perda o nulo, o positivo qualificado e a ausência de direção.

**Consequências para o plano.** O critério de conclusão do conjunto passa a ser o critério de conclusão do primeiro artigo, e deve ser escrito como lista fechada (a registrar em documento próprio). A validação por juízes do Passo 3 foi substituída em 15/09/2026 por fonte dialetológica e ocorrência no corpus (`docs/pendencias.md` 2.14). O passo 5.6, eixo ocupacional por AUL, deixa de ser pré-requisito automático: num artigo de recurso ele pode ser declarado como limitação, e a decisão entra no critério de conclusão.

---

## Plano de fechamento do dataset v1

Aprovado pela equipe em 15/09/2026. **Numeração estável:** os itens não são renumerados; item novo recebe o número seguinte. Escopo congelado — o que surgir depois vai para fase posterior, salvo se invalidar a v1, e quem decide é a equipe. Visualização em página própria, fora do repositório; este quadro é a fonte.

| # | Fase | Item | Responsável | Situação | Depende de |
|---|---|---|---|---|---|
| 1 | 1 — rodada atual | Analisar a medição dos 102 pares contra as regras registradas | assistente | **concluído** 15/09 | — |
| 2 | 1 — rodada atual | Atualizar documentos e integrar à `main` | assistente | **concluído** 15/09 | 1 |
| 3 | 2 — congelar escopo | Escrever o "Critério de conclusão do dataset v1", com as decisões 13, 15 e 16 (`docs/criterio_conclusao_v1.md`) | assistente | **concluído** 15/09 (aprovado sem alterações) | 2 |
| 4 | 3 — validar pares | Validar os 25 pares implícitos por fonte e corpus | assistente | **concluído** 15/09 | — |
| 5 | 3 — validar corpus | Regerar a amostra do WER sobre os 83 arquivos | assistente | **concluído** 15/09 (900 trechos, 120,6 min; trechos com nome mascarado excluídos) | — |
| 6 | 3 — validar corpus | Gerar a amostra de coerência dialetal, 10 falantes por estado | assistente | **concluído** 15/09 (60 pessoas, com fusão de rótulos da mesma pessoa) | — |
| 7 | 4 — fechar | Fechar a ficha do conjunto | assistente | a fazer | 4, 8, 9, 10, 11 |
| 8 | 3 — validar pares | Conferir os trechos encontrados na busca | equipe | **concluído** 15/09 | 4 |
| 9 | 3 — validar corpus | Ouvir 2 arquivos: participação de ouvinte (15 min) | equipe | **concluído** 16/09 (43 s na BA; nenhuma em PE) | — |
| 10 | 3 — validar corpus | Ouvir os 60 falantes da coerência dialetal (cerca de 1 h) | equipe | **concluído** 17/09 (56 coerentes, 1 suspeito, 3 inconclusivos) | 6 |
| 11 | 3 — validar corpus | Transcrever 2 h de áudio para o WER (8 a 16 h) | equipe | **em andamento** desde 17/09: 5 de 241 blocos, instrumento calibrado | 5, 13 |
| 12 | 3 — orientação | Consulta à orientação: juízes como reforço e comitê de ética | equipe | a fazer | — |
| 13 | 2 — decisão | O WER entra na v1? | equipe | **decidida** 15/09: entra | — |
| 14 | 2 — decisão | Análise de sentimento e listas de *features* | equipe | **decidida** 15/09: segundo artigo | — |
| 15 | 2 — decisão | Integrar a branch `etapa3-situacao` | equipe | **decidida e executada** 15/09 | — |
| 16 | 2 — decisão | Eixo ocupacional por AUL: medir ou declarar limitação | equipe | **decidida** 15/09: limitação na v1, medição em fase posterior | — |
| 17 | 4 — fechar | Consolidar a documentação (`docs/pendencias.md` 2.15) | assistente | a fazer | 2 |
| 18 | depois da v1 | AUL para o eixo de prestígio ocupacional, **se houver tempo** antes da submissão (`docs/plano_aul_eixo_ocupacional.md`) | sessão própria | a fazer, após a v1 | v1 concluída |

**Retomada por sessão nova:** `docs/retomada_fechamento_v1.md`.

**Fora da v1, de propósito:** análise de sentimento (segundo artigo), crescimento das condições implícitas, resolução do gentílico, confirmação do sinal de direção, hipótese de marcação de registro, controle intrarregional, coleta de mais áudio, juízes como filtro obrigatório, e juntar as listas de pares num só módulo.
