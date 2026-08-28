# Roadmap do Projeto

**Função deste arquivo.** Plano único e canônico do projeto. Toda proposta de trabalho deve ser situada em um dos passos abaixo, e não apresentada como lista nova. A numeração dos passos é estável: passos concluídos permanecem na tabela com a situação atualizada, e nenhum passo é renumerado.

**Última atualização:** 27/08/2026

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
| **3** | Validação dos itens por juízes falantes nativos | Não iniciado, **bloqueado** | Passo 3.1 |
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
