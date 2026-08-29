# Roadmap do Projeto

**Função deste arquivo.** Plano único e canônico do projeto. Toda proposta de trabalho deve ser situada em um dos passos abaixo, e não apresentada como lista nova. A numeração dos passos é estável: passos concluídos permanecem na tabela com a situação atualizada, e nenhum passo é renumerado.

**Última atualização:** 28/08/2026

**Documentos irmãos.** `docs/achados_para_o_artigo.md` separa o que já pode ser afirmado em texto submetido do que não pode, com a condição precisa que liberaria cada item em suspenso — é o filtro a consultar antes de escrever qualquer trecho do artigo. `docs/pendencias.md` registra tudo que está aberto — lacunas, decisões não tomadas, verificações devidas e melhorias identificadas. Este arquivo diz o que fazer em seguida; aquele diz o que não pode ser esquecido. Consultar ambos ao retomar o trabalho.

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

- Duas das cinco molduras estavam inoperantes. `Quem falou isso é [MASK]` colapsa em pronomes; `estudou até o [MASK]` colapsa em expressão idiomática. Substitutas testadas e aprovadas em `experimentos/resultados/molduras_alternativas.md`.
- O vocabulário de estereótipo negativo é majoritariamente multi-token no BERTimbau, ao passo que as ocupações de alto prestígio são todas de token único. O confundidor de frequência está materializado no tokenizador, alinhado ao eixo de interesse. AUL passa de recomendação a condição de possibilidade.
- A sensibilidade ao *guise* concentra-se no léxico. O bloco morfossintático puro apresenta divergência de Jensen-Shannon mediana de 0,0023 bits, contra 0,0144 do bloco lexical e 0,0963 da referência de conteúdo distinto.

### Passo 2 — Pendências de citação e revisão editorial (concluído)

Fechadas as pendências de cobertura dialetológica de Ceará e Bahia; localizada a referência de Oliveira (2017); lido integralmente Melo e Souza (2026); criado `docs/referencias.bib`; todos os documentos convertidos para registro acadêmico formal. Duas correções de conteúdo decorrentes constam do log v1.7 do `CLAUDE.md`.

### Passo 3 — Validação por juízes falantes nativos

Aplicação do Filtro 1 descrito em `docs/pares_minimos_v1.md`, seção 7. Não deve ser iniciado antes da conclusão do passo 3.1, sob pena de consumir a disponibilidade dos juízes com itens que o instrumento descartaria.

**3.1 — Correção do instrumento (bloqueia o passo 3).** Substituir as molduras inoperantes pelas alternativas já testadas; refazer o conjunto de atributos considerando a segmentação em subtokens; decidir quais atributos são lidos por probabilidade de máscara e quais exigem AUL. Trabalho de escrivaninha, da ordem de horas.

**3.1 — Correção do instrumento. Concluído** em 28/08/2026. Molduras inoperantes substituídas pelas testadas; conjunto de atributos reconstruído a partir do vocabulário do modelo, por `experimentos/selecionar_atributos.py`. A correção revelou a assimetria de tokenização por eixo de prestígio, hoje um dos achados sustentados do artigo.

**Por que o passo 3 está suspenso, e não apenas bloqueado.** Convocar juízes exige um conjunto de itens que valha a pena validar, e o passo 5 mostrou que o conjunto atual não produz resposta mensurável no modelo. Validar itens que não medem nada gastaria a disponibilidade dos juízes sem contrapartida.

### Passo 4 — Coleta do corpus de áudio

Execução do pipeline já implementado em `pipeline_coleta_piloto/`. É o passo mais longo em tempo de calendário — coleta, transcrição e verificação manual de WER e DER — e é pré-requisito do Filtro 2 do protocolo de validação, segundo o qual um marcador só integra o experimento se ocorrer em fala espontânea no corpus coletado. Por isso está no caminho crítico, ainda que seja o menos avançado.

**4.1 — Lista de fontes. Concluído** em 27/08/2026. Lista semente de 32 canais verificados, em `docs/fontes_coleta.md` e `pipeline_coleta_piloto/fontes.json`. Estabelecida a regra de atribuição por canal, depois de o levantamento por consulta de busca ter demonstrado contaminação entre estados.

**4.2 — Meta de volume. Concluído** em 27/08/2026. Derivada do requisito estatístico do Filtro 2 em `experimentos/meta_volume_corpus.py`, com resultado em `experimentos/resultados/meta_volume.md`: 4,1 h de fala do locutor-alvo por estado, equivalentes a 8,3 h de áudio bruto, totalizando cerca de 50 h no conjunto dos seis estados.

**4.3 — Piloto executado** em 27/08/2026. Dezessete trechos, 1,55 h, seis estados e três camadas. A esteira funciona de ponta a ponta; as medições estão em `experimentos/resultados/piloto_medicoes.md`. Três resultados alteram o planejamento: o rendimento por camada é bem superior ao suposto, o que reduziria a meta de 50 h para cerca de 38 h; não há indício de que a transcrição penalize a fala nordestina, o que removeria um confundidor; e a primeira aplicação do Filtro 2 não registrou nenhuma ocorrência do léxico regional em que o Bloco B do instrumento se apoia.

**Restrição prática.** A transcrição com `large-v3` em CPU opera a uma fração do tempo real. Para escala, o processamento vai para ambiente com GPU, e essa conta de tempo deve entrar no planejamento antes da coleta, não depois.

---

## Situação dos dois conjuntos de dados

Atualizada em 28/08/2026. A redação anterior descrevia o estado de 26/08 — um vídeo avulso, sem transcrição — e permaneceu no arquivo depois do piloto e da coleta, o que é defeito de manutenção do próprio plano canônico.

| Conjunto | Situação |
|---|---|
| **Corpus de áudio** | **Especificação fechada, execução em curso.** Esquema de oito campos definido em `CLAUDE.md`, seção 1.4.1, e implementado. Regra de atribuição por canal estabelecida e verificada contra contaminação. Meta de volume derivada de requisito estatístico, e não arbitrada. Coletados 52 trechos, 5,52 h, cerca de 0,92 h por estado, contra meta revista de cerca de 6,4 h por estado. Esteira validada de ponta a ponta, com 88 canais verificados disponíveis. |
| **Pares mínimos** | **Especificação aberta, e o conteúdo perdeu sustentação.** Doze itens rascunhados, nenhum validado por juízes. Os quatro blocos testados — morfossintático, lexical, feixe e construcional — não produzem resposta no modelo, de modo que o conjunto atual não serve como instrumento de medição de viés. Faltam, além do conteúdo, quatro definições formais: tamanho-alvo, formato de publicação, licença e ficha de conjunto de dados. |

### Por que a assimetria importa

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

Resultado em `experimentos/resultados/sensibilidade_guise.md`. Com controles que estabelecem piso e teto de sensibilidade: o instrumento detecta diferença de conteúdo a 6,32× o piso, mas os marcadores morfossintáticos ficam em 1,00×, e o efeito dos lexicais é reproduzido por um controle com palavras raras não regionais.

**Decisão de rumo, e é ela que destrava o resto:**

| Caminho | Custo | O que responde | Situação |
|---|---|---|---|
| **5.1** Marcadores construcionais pareados em frequência | baixo | se ainda existe instrumento possível neste modelo | **Concluído** em 28/08/2026 — resposta negativa |
| **5.2** BERTimbau Large, ou métrica baseada em representação | médio | se o limite é do modelo ou da métrica | Não iniciado |
| **5.3** Reposicionar como artigo de método e recurso | — | encerra a dependência de um resultado de viés | Não iniciado, e hoje o mais amparado |
| **5.4** Menção explícita em volume | baixo | se o modelo responde ao rótulo regional, ainda que não à variedade | **Concluído** em 29/08/2026 — resposta afirmativa |
| **5.5** Direção do efeito, e não sua magnitude | baixo | se a resposta é preconceituosa, e não apenas diferente | **Concluído** em 29/08/2026 — nenhum viés de valência sobrevive |
| **5.6** Eixo ocupacional por AUL | baixo | o único eixo que o PLL não consegue medir neste modelo | Aberto, e é a última medição pendente |

Os quatro não se excluem. O 5.1 era o mais barato e determinava se os demais eram necessários; a resposta dele é que sim.

### 5.1 — Marcadores construcionais (concluído, resposta negativa)

Relatório em `experimentos/resultados/construcional.md`; tabelas regeráveis em `construcional_tabelas.md`.

**Desenho.** Como o pareamento perfeito de frequência é inalcançável para marcadores construcionais — os melhores candidatos apresentam razão de 5 a 11 vezes —, abandonou-se a comparação de medianas e adotou-se a **calibração da lei de frequência**: ajusta-se |Δ| contra log₁₀ da razão de frequência sobre 22 pares não regionais, e mede-se o **resíduo** de cada par dialetal contra essa reta. Toda estatística passa a operar no nível do par.

**Resultado.** A condição construcional apresenta resíduo médio de −0,0141, com três de dez pares acima da reta e p = 0,71. A pista que motivou o passo — o vocativo *menino* — não replica: seu irmão, o vocativo *rapaz*, apresenta o maior resíduo negativo da condição.

Somam-se agora **quatro famílias testadas sem efeito**: morfossintática, lexical, feixe e construcional. O caso mais limpo é a negação pós-verbal, cujos pares empregam as mesmas palavras em ordem diferente — razão de frequência 1,0 por construção — e cujo resíduo é negativo.

**Dois subprodutos que valem por si.** O controle de conteúdo funciona como controle positivo do método de resíduo (p = 0,0003 após Holm), o que torna o nulo legível. E a calibração revelou que a frequência explica bem menos do que o relatório anterior afirmava — R² = 0,180 —, o que **exigiu revisão do item 1.14** de `docs/achados_para_o_artigo.md`.

### 5.4 — Menção explícita em volume (concluído, resposta afirmativa)

Não estava previsto. Surgiu porque a condição de menção explícita é a **única** com resíduo consistente entre as regionais: cinco pares em cinco acima da reta, p = 0,026 bruto, 0,13 após Holm. E tem estrutura interna interpretável — os resíduos grandes são os que nomeiam a região como categoria; os que nomeiam estados ficam próximos de zero.

Exige um conjunto de pares de menção explícita em volume comparável ao dos demais blocos, com a distinção entre rótulo de região e nome de estado como variável de desenho. Detalhamento no item 2.8 de `docs/achados_para_o_artigo.md`.

**Relação com o restante.** É barato e usa a esteira já construída. Se confirmar, produz o contraste que sustentaria o artigo pretendido em nova chave — o modelo responde à categoria regional nomeada e não à variedade que a indicia. Se não confirmar, o 5.3 passa a ser o único caminho disponível.

**Resultado**, em `experimentos/resultados/explicito.md`. Vinte e quatro pares novos, em três níveis de granularidade do rótulo, todos de autoidentificação. Duas condições produzem resíduo acima da reta da frequência **e sobrevivem à correção de Holm**: gentílico de estado, com p ajustado de 0,0012 e oito de oito pares acima da reta, e macrorregião, com 0,0038 e sete de oito. Topônimo não sobrevive. Não é efeito de raridade: as duas condições significativas têm as razões de frequência mais baixas do conjunto, e o par mais bem pareado — *pernambucano* contra *paulistano*, 1,1× — está entre os de maior efeito.

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

**Consequência para o artigo.** O trabalho não é sobre viés medido, e sim sobre o que o modelo distingue e o que não distingue, em três resultados que se sustentam mutuamente — e ganha uma contribuição de método que não existiria sem o resultado negativo: a demonstração, em caso concreto, de que uma medição de viés por pseudo-verossimilhança em português pode produzir efeito significativo inteiramente atribuível à tokenização. Detalhamento na seção 5 de `docs/achados_para_o_artigo.md`.

### 5.6 — Eixo ocupacional por AUL (aberto)

Aberto em 29/08/2026 pelo resultado do 5.5. É a última medição pendente para fechar a seção de Resultados, e a única que exige nova passagem pelo modelo: os escores de AUL não foram gravados, porque as medições dos passos 5.1 e 5.4 empregaram o atalho de PLL apenas, por economia de tempo de máquina.

A necessidade não é preferência entre métricas. É condição de possibilidade, pelo item 1.20 de `docs/achados_para_o_artigo.md`: o léxico ocupacional de baixo prestígio não integra o vocabulário do BERTimbau como palavra inteira, e nenhuma restrição de itens contorna isso.

Custo: uma execução sobre os 73 pares do conjunto acumulado, com as três métricas em vez de uma. Não depende de decisão da equipe.

**Sai do "fora de escopo".** A comparação com o BERTimbau Large fora afastada por ser refinamento de medição, e não construção de dataset. Com o dataset existindo e o desenho em questão, a comparação passa a responder à pergunta que bloqueia o projeto, e volta a ser pertinente.