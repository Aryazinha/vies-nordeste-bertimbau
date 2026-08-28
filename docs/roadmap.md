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

| Conjunto | Situação |
|---|---|
| Corpus de áudio | Um vídeo, baixado como teste avulso, sem `estado_alvo` nem `tipo_fonte` registrados. Nenhuma transcrição. |
| Pares mínimos | Doze itens rascunhados, nenhum validado, um suspenso por pendência bibliográfica, conjunto de atributos por refazer. |

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
| **5.4** Menção explícita em volume | baixo | se o modelo responde ao rótulo regional, ainda que não à variedade | Aberto, e novo |

Os quatro não se excluem. O 5.1 era o mais barato e determinava se os demais eram necessários; a resposta dele é que sim.

### 5.1 — Marcadores construcionais (concluído, resposta negativa)

Relatório em `experimentos/resultados/construcional.md`; tabelas regeráveis em `construcional_tabelas.md`.

**Desenho.** Como o pareamento perfeito de frequência é inalcançável para marcadores construcionais — os melhores candidatos apresentam razão de 5 a 11 vezes —, abandonou-se a comparação de medianas e adotou-se a **calibração da lei de frequência**: ajusta-se |Δ| contra log₁₀ da razão de frequência sobre 22 pares não regionais, e mede-se o **resíduo** de cada par dialetal contra essa reta. Toda estatística passa a operar no nível do par.

**Resultado.** A condição construcional apresenta resíduo médio de −0,0141, com três de dez pares acima da reta e p = 0,71. A pista que motivou o passo — o vocativo *menino* — não replica: seu irmão, o vocativo *rapaz*, apresenta o maior resíduo negativo da condição.

Somam-se agora **quatro famílias testadas sem efeito**: morfossintática, lexical, feixe e construcional. O caso mais limpo é a negação pós-verbal, cujos pares empregam as mesmas palavras em ordem diferente — razão de frequência 1,0 por construção — e cujo resíduo é negativo.

**Dois subprodutos que valem por si.** O controle de conteúdo funciona como controle positivo do método de resíduo (p = 0,0003 após Holm), o que torna o nulo legível. E a calibração revelou que a frequência explica bem menos do que o relatório anterior afirmava — R² = 0,180 —, o que **exigiu revisão do item 1.14** de `docs/achados_para_o_artigo.md`.

### 5.4 — Menção explícita em volume (aberto)

Não estava previsto. Surgiu porque a condição de menção explícita é a **única** com resíduo consistente entre as regionais: cinco pares em cinco acima da reta, p = 0,026 bruto, 0,13 após Holm. E tem estrutura interna interpretável — os resíduos grandes são os que nomeiam a região como categoria; os que nomeiam estados ficam próximos de zero.

Exige um conjunto de pares de menção explícita em volume comparável ao dos demais blocos, com a distinção entre rótulo de região e nome de estado como variável de desenho. Detalhamento no item 2.8 de `docs/achados_para_o_artigo.md`.

**Relação com o restante.** É barato e usa a esteira já construída. Se confirmar, produz o contraste que sustentaria o artigo pretendido em nova chave — o modelo responde à categoria regional nomeada e não à variedade que a indicia. Se não confirmar, o 5.3 passa a ser o único caminho disponível.

**Sai do "fora de escopo".** A comparação com o BERTimbau Large fora afastada por ser refinamento de medição, e não construção de dataset. Com o dataset existindo e o desenho em questão, a comparação passa a responder à pergunta que bloqueia o projeto, e volta a ser pertinente.