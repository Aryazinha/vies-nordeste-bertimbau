# Pendências e Melhorias

**Função deste arquivo.** Registro único do que está aberto no projeto: lacunas conhecidas, decisões não tomadas, melhorias identificadas e verificações devidas. Existe porque o conhecimento acumulado durante uma sessão de trabalho não sobrevive a ela; o que não estiver aqui será redescoberto do zero ou simplesmente perdido — como ocorreu com o rascunho de pares mínimos da revisão v1.3, refeito integralmente meses depois.

**Como usar.** Consultar no início de cada retomada, antes de planejar trabalho novo. Todo item traz o motivo pelo qual importa e o que o encerraria, de modo que possa ser retomado sem o contexto da conversa em que surgiu. Itens resolvidos são marcados como tal, com a data, e não removidos — a lista serve também de histórico do que já foi enfrentado.

**Última revisão:** 31/08/2026

---

## Prioridade

A ordenação abaixo reflete o critério do `docs/roadmap.md`: aproxima-se primeiro o projeto de ter dados montados e validados.

| # | Pendência | Bloqueia | Seção |
|---|---|---|---|
| ~~1~~ | ~~Vox-pop com apenas dois canais em PB, SP e RJ~~ — resolvida em 31/08/2026 pela rodada de igualação | — | 1.2 |
| 1 | Ouvir e preencher `participacao_ouvinte` nos arquivos de canal com o formato; acompanhar o balanço na coleta futura | corpus final | 1.1 |
| 2 | Conferência dos percentuais de Oliveira (2017) | item C1 do instrumento | 3.1 |
| 3 | Correção do instrumento de texto (molduras e atributos) | validação por juízes | 2.1, 2.2 |
| 4 | Ambiente com GPU para o piloto de medição | piloto | 4.1 |
| 5 | ~~Decisão de simetria entre grupos~~ — resolvida em 31/08/2026 pela rodada de reforço de PE e BA (D1) | — | D1 |

---

## 1. Fontes de coleta

### 1.1 Rádio com participação de ouvinte existe em apenas dois estados

Programas em que o ouvinte liga — "Alô Juca" na TV Aratu (BA) e "Super Manhã" na Rádio Jornal (PE) — reúnem as três propriedades desejáveis simultaneamente: falante morador do estado, fala espontânea e áudio limpo. É a melhor fonte identificada em todo o levantamento.

O problema é que só PE e BA dispõem dela. Não se trata de diferença de quantidade, e sim de **tipo de fala**: se o material nordestino contiver fala não monitorada de gente comum e o material do grupo de controle contiver jornalismo de estúdio, a diferença observada entre os grupos passará a incluir registro e situação comunicativa, e não apenas procedência regional. O confundidor incide diretamente sobre a variável de interesse.

**Atualização de 31/08/2026 — a assimetria diminuiu, mas não acabou.** A rodada de igualação acrescentou ao Ceará o canal *Di Calheiros*, programa de rádio de Fortaleza que pede opinião ao ouvinte ("Qual a sua opinião sobre relacionamentos que começam nas redes sociais?"), formato até então restrito a PE e BA. Acrescentou também rádios locais em PB (*98 FM Digital*), PE (*Rádio Cidade 99.7*), BA (*Rádio Salvador FM*) e RJ (*Rádio Roquette-Pinto*), mas **não se verificou** se essas têm quadro de participação do ouvinte — a inspeção olhou ancoragem geográfica e presença de fala, não o formato. **São Paulo continua sem nenhum canal desse tipo identificado.**

### Verificação executada em 31/08/2026, e o resultado muda o entendimento da pendência

**O que foi feito.** Varredura dos 15 títulos mais recentes dos 40 canais de podcast/rádio/TV já aceitos, procurando sinal de programa que dá voz a quem liga ou escreve. E busca dirigida por rádio de participação em São Paulo e no Rio, com seis consultas por estado.

**Resultado da varredura:** quatro canais confirmados — *Radio Jornal* (PE), *TV Aratu* (BA), *Di Calheiros* (CE) e *Rádio Salvador FM* (BA). Nenhum em PB, SP ou RJ.

**Resultado da busca dirigida: negativo, e por um motivo estrutural que vale registrar.** Os programas de participação de ouvinte que aparecem em São Paulo e no Rio pertencem a **redes nacionais** — Jovem Pan, Band FM, BandNews FM. São reais e são de participação, mas os ouvintes que ligam são do país inteiro, de modo que a fala não é atribuível ao estado e a regra de atribuição do projeto os rejeita. O que existe de rádio comunitária genuinamente local nas duas capitais — o caso da Heliópolis 87,5 FM, em São Paulo — quase não publica no YouTube.

A assimetria da seção 1.1, portanto, **não é falha de busca: é fato de estrutura de mídia**. No Nordeste, a rádio regional com participação de ouvinte é publicada no YouTube pela própria emissora regional. No Sudeste, o formato equivalente pertence à rede nacional, que por definição não representa um estado. Buscar mais não resolve.

**Consequência para o desenho.** Como a simetria não é obtenível por busca, ela tem de ser obtida por medida e controle. Foi acrescentado a `fontes.json` o campo `participacao_ouvinte`, com valores `sim` e `nao_verificado`.

Não existe valor `não`, e a razão é metodológica: a varredura de títulos é **limite inferior, não medida**. A prova está no próprio *Alô Juca* da TV Aratu, que tem o formato — registrado desde o levantamento original — e não deixou sinal algum nos quinze títulos mais recentes. Escrever `não` nos 36 canais restantes seria afirmar o que não foi estabelecido.

### Instrumento implementado em 01/09/2026

O campo passou a existir nos dois níveis, e a distinção entre eles é o ponto:

- `canal_tem_participacao_ouvinte`, herdado de `fontes.json` pela mesma via por que `estado_alvo` e `tipo_fonte` já vinham do canal (`selecionar_videos.py`, `collect.py`). Custa nada e serve para indicar quais arquivos vale a pena ouvir.
- `participacao_ouvinte`, fato do arquivo, que só se estabelece ouvindo e nasce `nao_verificado`.

`pipeline_coleta_piloto/balanco_participacao.py` relata o volume por estado e compara os grupos, alertando quando o Nordeste tem proporção sensivelmente maior que o controle. Enquanto ninguém tiver ouvido, o relatório mostra zero — e o texto do próprio relatório diz que zero ali significa **quantidade desconhecida, não nula**.

**Achado da primeira execução, e ele reduz a urgência.** Dos 52 arquivos já coletados, **apenas um** vem de canal com o formato: um trecho de 8,6 min da TV Aratu, na Bahia. O desequilíbrio, portanto, quase não existe no material que está no disco — a ameaça é **prospectiva**, e incide sobre a coleta que ainda será feita, quando as rádios de participação passarem a ser exploradas.

**Encerra a pendência:** ouvir os arquivos de canal com o formato e preencher `participacao_ouvinte`; e, quando a coleta avançar, acompanhar o relatório de balanço para equilibrar ou descontar. Não há mais decisão pendente aqui — só execução.

**Por que isso importa, e é a parte que não pode ser perdida.** Fala de ouvinte ao telefone é o registro menos monitorado de todo o corpus, e os marcadores regionais que o projeto investiga são mais frequentes em fala informal. Se o grupo nordestino tem esse tipo de fala e o grupo de controle não, o contraste entre as regiões fica inflado **na direção que favorece a hipótese do projeto**. É viés que não pode permanecer sem medida.

### Medida executada em 16/09/2026 — RESOLVIDA

Os dois arquivos de canal com o formato, únicos do corpus de 83, foram ouvidos pela equipe (item 9 do plano de fechamento), e o resultado foi gravado por `registrar_participacao.py`:

| Arquivo | UF | Canal | Duração | Fala de ouvinte |
|---|---|---|---|---|
| `kMd1ga7Tz5g` | BA | TV Aratu, *Alô Juca* | 516 s | **43 s** — uma ouvinte ao telefone, 4:40–5:23; apresentador sozinho no restante |
| `Z_ZLH1hratI` | PE | Rádio Jornal, *Super Manhã* | 176 s | **nenhuma** — a segunda voz detectada pela diarização é sobreposição do próprio apresentador |

**Resultado: a assimetria é de 43 segundos.** O corpus tem 0,2% de fala de ouvinte no grupo nordestino (43 s em 296 min) e nada no grupo de controle. A diferença existe, é do sinal previsto — inflaria o contraste regional —, e é pequena demais para afetar qualquer medida do projeto. Conduta adotada: **declarar na ficha do conjunto**, sem descontar, porque descontar 43 segundos de 5 horas de fala nordestina não altera nenhuma comparação. Se a coleta for retomada com rádios de participação, a conduta muda e o relatório volta a ser o instrumento.

**Duas correções de instrumento, feitas antes da medida.** (a) `balanco_participacao.py` contava a duração **inteira** do arquivo marcado com participação, e não os segundos de fala de ouvinte; no arquivo da Bahia isso atribuiria 516 s onde há 43 s, um fator de doze. Passou a somar o novo campo `participacao_ouvinte_s`, mantendo a contagem antiga, e declarando-a, apenas quando o campo faltar. (b) O preenchimento deixou de ser edição manual do JSON e passa por `registrar_participacao.py`, que grava também a nota da escuta e a data.

**Ressalva de leitura do relatório, que permanece.** O alerta de desequilíbrio dispara quando o controle tem zero e o Nordeste tem qualquer coisa, sem consultar a magnitude — de modo que ele está disparando por 43 segundos. Está tecnicamente correto e é praticamente irrelevante neste corpus; quem ler o relatório deve confrontar o alerta com o percentual da tabela, e não tomá-lo como ordem de conduta. Rever o limiar não entra na v1: escopo congelado.

### 1.2 Camada de vox-pop com apenas dois canais — AVANÇADA, e agora é a pendência de fonte mais consequente

O registro original apontava PB, BA, SP e RJ com dois canais nessa camada. **Situação em 31/08/2026:** PE e CE alcançaram a meta de quatro; a Bahia subiu para três, com *azulzinho Itabuna*; **PB, SP e RJ seguem com dois**.

**Por que isto pesa mais do que pesava.** Desde a decisão do item #4 da especificação, que passou a priorizar vox-pop e podcast sobre vlog, o plano de coleta emprega **todos** os canais de vox-pop de **todos** os estados — a tabela de `meta_corpus_autonomo.md` mostra 2/2, 4/4, 4/4, 3/3, 2/2 e 2/2. Não há folga alguma nessa camada. Perder um canal em PB, SP ou RJ significa perder metade do vox-pop do estado, e o piso de 20 falantes deixa de ser alcançável por essa via.

O risco não é hipotético: a seção 4.5 registra que vídeos com restrição etária falham no download, e a restrição recai tipicamente sobre matéria de violência — que é precisamente o conteúdo do telejornalismo policial de onde vem boa parte do vox-pop.

### Rodada de reforço de vox-pop, 31/08/2026 — parcialmente bem-sucedida

Executada pela mesma metodologia das rodadas anteriores, com consultas desenhadas para a camada: entrevista de rua, reportagem de bairro com morador e memória oral. De 164 candidatos, 36 passaram na triagem automática e **11 sobreviveram à revisão — 4 aceitos e 7 `a_confirmar`**.

| UF | Antes | Depois | A confirmar | Situação |
|---|---|---|---|---|
| RJ | 2 | **5** | +4 | Meta atingida |
| PB | 2 | **3** | +2 | Perto; os dois a confirmar bastariam |
| SP | 2 | **2** | +1 | **Sem avanço** |

**São Paulo é um resultado negativo, e a razão é estrutural.** A busca devolveu quase exclusivamente rede nacional — *Jornal da Record*, *g1*, *SBT News*, *Band Jornalismo*, *Hoje em Dia*, *Cidade Alerta*, *Balanço Geral*. Todas foram rejeitadas: um canal nacional não satisfaz a regra de atribuição por estado, porque seu conteúdo vem do país inteiro, e a fala que ele carrega não é atribuível a São Paulo. O paradoxo é que São Paulo concentra a mídia nacional justamente por ser São Paulo, e isso **soterra** o jornalismo de bairro paulista nos resultados de busca. O único candidato genuinamente local e ancorado no estado, *Ponte Jornalismo*, ficou `a_confirmar`.

Uma consequência a considerar: se São Paulo permanecer com dois canais nessa camada enquanto os demais estados chegam a quatro ou cinco, a assimetria se inverte — o grupo de controle é que passa a ser o frágil. Para o experimento importa a simetria, e não o máximo por estado.

### Encerrada em 31/08/2026, e a hipótese sobre São Paulo confirmou-se

A rodada de igualação executou exatamente a estratégia que esta seção previu para São Paulo — partir de emissora regional nomeada e de jornalismo comunitário, em vez de consulta genérica — e o estado saltou de **dois para sete** canais de vox-pop, entre eles a *Agência Mural de Jornalismo das Periferias*, que entrevista moradores de Sapopemba, Paraisópolis e São Mateus. A previsão registrada aqui era, portanto, correta: o problema não era ausência de jornalismo de bairro paulista, era a consulta.

Situação final da camada, por estado: PB 6, PE 6, CE 5, BA 5, SP 7, RJ 6. **Todos acima da meta de quatro.**

E o motivo pelo qual a pendência havia sido promovida a prioridade 1 — a ausência de folga — desapareceu junto: o plano de `meta_corpus_autonomo.md` passou a empregar cinco canais por estado, com margem em quatro deles, em vez de consumir a camada inteira.

### 1.3 ~~Interior da Bahia descoberto~~ — RESOLVIDA em 31/08/2026

O registro original apontava que apenas 3 dos 10 canais baianos tinham marca de interior, agravado pelo fato de o único vlog de interior, `Jairo DroneX`, ser de **Juazeiro-BA**, conurbada com Petrolina-PE — o pior ponto possível da malha num estudo que compara justamente BA e PE. A condição de encerramento era cobrir Feira de Santana, Vitória da Conquista, Itabuna ou Barreiras, distantes da divisa.

**Três das quatro foram cobertas**, entre a inspeção de conteúdo e a rodada de reforço: Vitória da Conquista (*Marcinha De jesus*), Itabuna (*azulzinho Itabuna*, vox-pop) e Barreiras (*Guilherme Barreto*). Somam-se Alagoinhas (*Paty Miranda*), Paulo Afonso (*Motovlog do Marcelo*), Piritiba e Jacobina (*Rosa Oliveira*) e Ilhéus (*NEIZINHO ANDRADE*). Dos 19 canais baianos verificados, **13 têm marca de interior**, contra 3 de 10 no registro original, e nenhum deles depende da conurbação de Juazeiro.

**Feira de Santana foi coberta em 31/08/2026**, na rodada de igualação, pelo *Programa Acorda Cidade* — podcast e noticiário local da cidade. Com isso, as quatro cidades nomeadas na condição de encerramento estão cobertas.

### 1.4 Treze canais em situação `a_confirmar` — RESOLVIDA em 31/08/2026

Eram 11, mais 2 acrescentados na busca de D1 (Samiele Batista, Marcinha De jesus). `selecionar_videos.py` os excluía do planejamento até a inspeção. A equipe ouviu o conteúdo de cada um contra as três perguntas padrão — há fala humana em volume razoável, o falante reside no estado, e não é conteúdo comercial ou institucional disfarçado de vlog — mais a dúvida específica registrada por canal.

**Resultado: 10 aprovados, 3 rejeitados.**

| Canal | UF | Decisão | Motivo |
|---|---|---|---|
| Daniel Alves | PB | Aprovado | Majoritariamente vlog; 3 vídeos antigos de imobiliária excluídos individualmente |
| ESTRELA ALVES | PE | Aprovado | Vlog genuíno, sem ressalva |
| Samiele Batista | PE | **Rejeitado** | Conteúdo é vitrine de preço de feira, não fala espontânea |
| Evelyn Ferreira | CE | Aprovado | Jornalista entrevistando moradores — vox-pop genuíno, não portfólio |
| Band Bahia Oficial | BA | Aprovado | Tem falas espontâneas e entrevistas, não é só apresentador de estúdio |
| João Yurley | BA | Aprovado | Tem falas de verdade; trechos de jogo eletrônico excluídos individualmente |
| Marcinha De jesus | BA | Aprovado | Base real confirmada: Vitória da Conquista |
| Alan City | SP | **Rejeitado** | Narração é roteiro lido, não fala espontânea |
| Kellynha Costa | SP | **Rejeitado** | Canal inativo, último vídeo há 6 anos |
| EXPEDIÇÃO KL | RJ | Aprovado | Capital e Cabo Frio, ambos no RJ |
| Destinos Escolhidos | RJ | Aprovado | Residência confirmada no Rio |
| Mania de carro | RJ | Aprovado | Residência confirmada em Itaboraí |
| Manu Trindade | RJ | Aprovado | Residência confirmada em Ipanema |

Corrigida na mesma revisão uma duplicata encontrada em `fontes.json`: o canal "Vlog com Diogo" (PE) tinha duas entradas com o mesmo `channel_id`, inflando em uma unidade a contagem de vlog do estado.

**Pendência encerrada.** `pipeline_coleta_piloto/fontes.json` já reflete todas as decisões; nenhum canal permanece `a_confirmar`.

### 1.5 ~~Vlogs de Pernambuco são os mais escassos~~ — RESOLVIDA em 31/08/2026

**Encerrada pela rodada de reforço descrita em D1:** Pernambuco passou de 4 para 10 vlogs verificados, contra 8 no Ceará, 11 em São Paulo e 13 no Rio de Janeiro. O registro original segue abaixo, por ser a origem da pendência D1.

Eram quatro canais verificados, contra oito no Ceará e treze em São Paulo. Coincide, sem relação causal, com o fato de Pernambuco ser também o único estado-alvo sem marcador morfossintático próprio no instrumento de texto (seção 2.4). Se as duas fragilidades persistirem, convém declarar PE como caso de cobertura reduzida em vez de forçar paridade artificial.

### 1.6 Rota de coleta por RSS não implementada

A seção 2.3.2 de `docs/fontes_coleta.md` estabelece que podcast distribuído por feed aberto é a fonte de situação jurídica mais clara disponível ao projeto, superior nesse aspecto ao próprio YouTube. O `collect.py`, no entanto, só opera sobre URLs do YouTube. Nenhum feed RSS foi levantado.

**Encerra a pendência:** levantar feeds de podcasts regionais por estado e estender o `collect.py`, que já pode usar o extrator genérico do `yt-dlp`.

---

## 2. Instrumento de texto

### 2.1 Molduras inoperantes ainda não substituídas no documento

O teste de fumaça (passo 1) mostrou que duas das cinco molduras não funcionam: `Quem falou isso é [MASK]` colapsa em pronomes (*você* 0,385; *ele* 0,294) e `estudou até o [MASK]` colapsa em expressão idiomática (*fim* 0,386). As substitutas foram testadas e aprovadas — `completou o ensino [MASK]` concentra 97% da massa em *médio* e *fundamental*; `parece uma pessoa [MASK]` elimina o vazamento de subtoken — e constam de `experimentos/resultados/relatorios/molduras_alternativas.md`, mas **não foram incorporadas** a `docs/pares_minimos_v1.md`.

### 2.2 Conjunto de atributos precisa ser refeito

O vocabulário de estereótipo negativo é majoritariamente multi-token no BERTimbau (*grosseira*, *desonesta*, *preguiçosa* em três subtokens), enquanto as ocupações de alto prestígio são todas de token único. A assimetria acompanha o eixo de prestígio que o estudo mede, o que torna AUL condição de possibilidade e não recomendação.

**Encerra a pendência:** refazer os conjuntos pareados verificando segmentação item a item, e definir explicitamente quais atributos são lidos por probabilidade de máscara e quais exigem AUL.

### 2.3 Item C1 suspenso

O item que representa o Ceará depende da direção do marcador do imperativo em Fortaleza, hoje em disputa entre fontes secundárias (ver 3.1).

### 2.4 Pernambuco sem marcador morfossintático próprio

Recife apresenta uso simétrico do imperativo, de modo que M1 não distingue PE do grupo de controle. A proposta em avaliação apoia-se em negação pós-verbal, no marcador discursivo *visse?* e em léxico regional — mas *visse?* não tem fonte dialetológica citável.

### 2.5 Balanceamento de frequência lexical não realizado

Terceira crítica de Kaneko e Bollegala (2022): efeito de frequência confunde-se com efeito de viés. Itens como *arretado* e *da hora* não têm frequência comparável, e nada foi medido.

**Encerra a pendência:** medir a frequência de cada item em corpus de referência e descartar ou compensar os pares muito descompensados.

### 2.6 Volume do conjunto

Doze itens constituem piloto. O CrowS-Pairs tem 1.508 pares. A meta do conjunto final só pode ser definida depois de conhecida a taxa de aprovação dos juízes.

### 2.7 A sensibilidade concentra-se no léxico

Achado do passo 1: a divergência entre condições é de 0,0144 bits no bloco lexical contra 0,0023 no morfossintático, tendo 0,0963 como referência de conteúdo distinto. Se o efeito final vier do léxico, um revisor poderá alegar que se mediu frequência lexical, e não dialeto. Três encaminhamentos possíveis: aceitar e reposicionar o artigo; ampliar o volume de itens e testar se a morfossintaxe produz efeito agregado; ou avaliar o BERTimbau Large antes de decidir. **Decisão em aberto.**

### 2.8 Grupo de referência: dependência entre pares, duplicata e chave de medição posicional — ABERTA e ENCERRADA em 14/09/2026

Revisão dos 54 pares propostos por `experimentos/propor_calibracao.py` (`experimentos/resultados/dados/calibracao_proposta.json`), antes de qualquer incorporação. Três constatações.

**(a) Duplicata no conjunto canônico.** `controle_frequencia-05` e `controle_neutro-03` são o mesmo par com os lados invertidos, e ambos entram no ajuste da reta. O grupo de referência tem 25 pares distintos, e não 26; o par duplicado recebe peso dobrado na calibração.

**(b) A proposta não produz 54 unidades independentes.** O gerador forma todas as combinações de itens dentro de seis molduras, de modo que a mesma frase se repete entre pares: *Guardei o coador no armário da cozinha* e *O menino levou o transferidor para a escola* comparecem em cinco pares cada, e dez frases propostas já constam do conjunto canônico. Ligando pares que compartilham frase, os 80 pares resultantes formam apenas 20 grupos, o maior com 18 pares. Pares que compartilham um lado compartilham o termo de pseudo-verossimilhança daquele lado e não são independentes — a mesma objeção de `docs/achados_para_o_artigo.md` §1.16, deslocada da medição para o par. O teto de detecção de `experimentos/resultados/tabelas/meta_pares_minimos.md` supõe pares independentes e ficaria superestimado.

**(c) Concentração de moldura.** Com a incorporação, *Comprei X na feira hoje* passaria a 18 pares, e três molduras somariam 38 dos 80. O próprio gerador declara que a reta ajustada sobre variantes de uma construção descreve aquela construção.

Registre-se ainda que a checagem de carga regional dos itens no corpus de áudio foi executada e **não é informativa**: a maioria dos itens tem zero ocorrências nos dois grupos, em cerca de 63 mil palavras. A dúvida sobre *sombrinha*, cujo emprego como designação genérica de guarda-chuva pode ter distribuição regional, permanece sem fonte.

**(d) Remover par do código desalinha as medições em silêncio.** `empacotar_pares.py` associa cada medição ao par pela chave `(condicao, índice na lista)`, e o identificador publicado deriva do mesmo índice. Apagar `controle_frequencia-05` de `CONTROLE_FREQUENCIA` deslocaria os seis pares seguintes, que passariam a receber a medição do vizinho e a trocar de identificador, e `--verificar` não o detectaria, porque compara o arquivo com o código e não o código com a medição. Remover `controle_neutro-03` tem custo adicional: o piso é a mediana daquela condição. A exclusão deve ser feita por marcação, sem apagar a entrada da lista, ou acompanhada de chave de medição que não dependa de posição.

**Decisões de 14/09/2026.**

1. **A duplicata sai da calibração por marcação, sem apagar a entrada da lista.** Mantém-se `controle_neutro-03`, que define o piso, e exclui-se `controle_frequencia-05`. A meta de pares novos passa de 54 a 55.
2. **O gerador foi reescrito** sob a regra de uma frase por par (`experimentos/propor_calibracao.py`, revisão de 14/09/2026). Produziu 55 pares em vinte molduras novas, com no máximo três pares cada, sem frase repetida entre pares nem coincidente com o conjunto canônico, e com dez pares em cada faixa de razão, exceto a superior (acima de 100×), que tem cinco. Nada foi medido no modelo; a proposta aguarda revisão humana.
3. **Os 25 pares distintos restantes do grupo permanecem**, ainda que alguns compartilhem frase entre si (os quatro de `calibracao_extra` repetem *Comprei fermento na feira hoje*). Removê-los reduziria o grupo e exigiria mais pares novos; a dependência residual deve ser declarada na análise.

**Revisão humana de 14/09/2026.** Dos 55 pares propostos, 45 foram aprovados e 10 rejeitados, e dez itens foram vetados em todas as molduras — *globo*, *ação*, *violeta*, *quinta*, *quarta* e *sexta* por segundo sentido corrente que inflaria a razão de frequência; *chaveiro* e *carregador* por designarem ocupação; *bateria* por polissemia; *pote* por possível carga regional. Decisões e motivos em `experimentos/resultados/dados/calibracao_revisao.json`. O gerador passou a travar os aprovados e a completar apenas as vagas, e propôs dez substitutos. Na segunda rodada, nove foram aprovados e `filme-4` rejeitado, com veto a *terror* (valência negativa sem equivalente no outro lado, e sentido corrente fora do cinema) e a *drama* (sentido corrente fora do cinema). O substituto proposto, `presente-4` (*relógio* / *anel*), está pendente de revisão; com ele aprovado, a lista de 55 fica completa.

**Faixa superior sub-representada.** Após a revisão, a faixa de razão acima de 100× tem três pares, contra dez ou onze nas demais: três dos pares rejeitados estavam nela, e as molduras com vaga não oferecem outra combinação admissível nessa faixa. Somados os dois pares do grupo atual nessa faixa, o grupo de 80 teria cinco. A inclinação da reta depende de pontos nos extremos; se isso for julgado insuficiente, a correção é acrescentar itens raros às molduras com vaga (*viagem*, *zoologico*, *presente*, *chuva*), declarando a mudança, e não afrouxar as regras.

**Reforço executado em 14/09/2026.** Aprovado `presente-4`, os 55 pares ficaram fechados. A equipe decidiu reforçar a faixa superior **acrescentando** seis pares, e não substituindo aprovados, o que preserva a revisão ao custo de cerca de 11% a mais de medição: a proposta passa a 61 pares, e o grupo de referência a 86. Os itens foram escolhidos por sondagem prévia de frequência e segmentação — o par admissível nessa faixa combina item comum de um subtoken com item raro de dois —, e produziram as molduras novas `gaveta` e `sala` e o item *guerra* em `filme`. Uma moldura `quarto` foi testada e descartada, por fragmentação dos itens raros. Um par do reforço, `zoologico-3`, foi rejeitado antes de ir à equipe, com veto a *leão* (signo e metonímia da Receita Federal). A faixa acima de 100× passa a nove pares, contra dez ou onze nas demais. Os seis pares novos foram aprovados na quinta rodada, e a lista fechou em 61.

**Incorporação ao código, 14/09/2026 — medição pendente.** Os 61 pares entraram como condição `calibracao_v2` em `experimentos/teste_explicito.py`, acrescentada ao final para não deslocar a posição de nenhum par medido, e a condição passou a integrar a reta (`CALIBRACAO`) e o grupo de referência de `analise_valencia.py` (`REFERENCIA`). A duplicata foi marcada em `EXCLUIDOS_DA_CALIBRACAO`, sem remoção da lista, e as duas análises passaram a respeitá-la. `empacotar_pares.py` ganhou o campo `excluido_da_calibracao` e a versão 1.1 do esquema. Conferência executada sem o modelo: a lista no código é idêntica, e na mesma ordem, à aprovada em `calibracao_revisao.json`; nenhuma frase repete a de outra condição; e o grupo de referência efetivo é de 86 pares.

**Estado intermediário, e deliberado.** O código está à frente da medição. Os 61 pares não têm medição, e por isso `pares_minimos.json`, `explicito_tabelas.md` e `valencia_tabelas.md` não foram regerados, e `empacotar_pares.py --verificar` falha até que sejam. Os valores publicados continuam os de 26 pares, com a duplicata. A branch não deve ser integrada à `main` nesse estado. O que falta, em ordem: (1) notebook de medição no Colab — `notebooks/piloto_colab.ipynb` é de áudio e não serve —, que execute `teste_explicito.py`, o qual mede apenas a condição ausente de `explicito_bruto.json` e reanalisa; (2) `analise_valencia.py`; (3) `meta_pares_minimos.py`, cujo desvio-padrão de ruído vem do grupo de referência; (4) `empacotar_pares.py` e `--verificar`; (5) atualização dos valores citados nos documentos, listados no parágrafo sobre o impacto da exclusão. A análise do passo 5.1 (`teste_construcional.py`) fica como registro histórico, com a calibração da época, e não recebe os pares novos.

**Notebook de medição e custo real, 14/09/2026.** Criado `notebooks/medir_calibracao_colab.ipynb`, que antes de medir remede os cinco pares de `controle_neutro` e compara com os valores guardados, recusando-se a prosseguir se a diferença exceder 10⁻³ — as medições guardadas foram feitas em processador, e o Colab mede em GPU. A mesma conferência, executada na máquina local, reproduziu as 140 medições com diferença **nula**, em 44 segundos. Por extrapolação, as 1.708 medições dos pares novos levam cerca de nove minutos na máquina local. A estimativa anterior de que a medição exigiria o Colab superestimava o custo: a execução local é viável e dispensa a mistura de ambientes que a conferência existe para detectar. O notebook permanece como alternativa.

**Medição executada em 14/09/2026, no Colab (Tesla T4).** 1.708 medições novas; as 2.380 anteriores intactas; conferência de reprodutibilidade com maior diferença de 1,9·10⁻⁵ em 140 medições, contra tolerância de 10⁻³ (`experimentos/resultados/dados/ambiente_calibracao_v2.json`). `pares_minimos.json` foi regerado e passa em `--verificar`, com 146 pares e nenhum sem medição. Os valores citados nos documentos foram atualizados em 14/09/2026, na rodada da reescrita do item 1.14 (2.9).

**Meta recalculada.** Com `DP_RUIDO` = 0,1217 e 86 pares de referência em `meta_pares_minimos.py`, o teto de detecção sob correção de Holm cai de 0,078 para **0,044** — objetivo da ampliação, atingido. O mesmo critério de excluir efeitos acima de 0,08 passa a exigir **40 pares por condição, e não 37**, porque o desvio-padrão do ruído subiu levemente e o efeito-alvo passou de d = 0,68 a d = 0,66. A meta de 37 registrada em `docs/dataset-spec.md` (§2.2.1 e registro de pendentes), `docs/ficha_conjunto.md`, `docs/questoes_para_orientacao.md` e `docs/resumo_para_orientacao.md` deve ser atualizada, e o volume total implicado passa a 4 × 40 + 86 = 246 ou 5 × 40 + 86 = 286 pares.

**Encerra a pendência:** ~~aplicar a exclusão pelo mecanismo descrito em (d), junto com a incorporação dos pares novos; reformular o gerador para que cada frase compareça em um único par, com molduras em número maior e distintas das já presentes; e, caso se admita reúso, declarar a estatística de conglomerado correspondente e recalcular o teto de detecção~~ — **encerrada em 14/09/2026**: exclusão aplicada por marcação na reanálise, gerador reformulado sem reúso de frase, e teto recalculado em 0,044. Permanece, como risco residual, a chave de medição posicional de (d), mitigada pela regra de não reordenar nem apagar entradas, declarada no código.

### 2.9 A reta da frequência não se sustenta com o grupo de referência ampliado — ABERTA em 14/09/2026

**Constatação.** Com os 86 pares distintos, a inclinação da reta de |Δ PLL| contra log₁₀ da razão de frequência cai de 0,0308 (R² = 0,159, p = 0,044, 26 pares) para 0,0073 (R² = 0,008, p = 0,41). Nos 61 pares novos, isoladamente, a inclinação é nula: −0,0037, R² = 0,002, p = 0,74, e a mediana de |Δ| não varia entre as faixas de razão, de 1× a mais de 100×.

**A inclinação anterior era frágil antes da ampliação.** Sem a duplicata, os 25 pares antigos dão p = 0,055; sem também os cinco de `controle_raridade`, p = 0,13. Esses cinco pares — *chinfrim*, *combalido*, *afoito*, *arre*, *moço* — combinam raridade com registro marcado, arcaizante ou coloquial, e têm |Δ| elevado. É compatível com a hipótese de que o efeito atribuído à frequência fosse, ao menos em parte, efeito de marcação de registro; a hipótese é posterior aos dados e não foi testada.

**A variação dominante é a moldura.** Nos 61 pares novos, a mediana de |Δ| por moldura vai de 0,086 (`louca`) a 0,262 (`aula`), amplitude muito superior à atribuível à razão de frequência. Com três pares por moldura, a estimativa por moldura é imprecisa, mas a heterogeneidade é visível.

**O que muda, e o que não muda.**

- **Não muda:** a menção explícita segue acima do grupo de referência — gentílico de estado a p ajustado de 0,0004 e macrorregião a 0,0045 —, com a separação entre rótulo de pessoa e de lugar mais nítida (lugar passa de p = 0,048 a 0,107; diferença entre os agrupamentos, p = 0,0004). No eixo de caráter restrito a token único, nenhuma condição sobrevive à correção, e o viés aparente de macrorregião permanece desfeito (+0,0309, p ajustado 1,0). O controle positivo passa a sobreviver à correção de Holm no eixo de caráter completo (0,0556 → 0,0052), o que indica o ganho de poder pretendido.
- **Muda:** o item 1.14 de `docs/achados_para_o_artigo.md`, que descreve o efeito da frequência como "real, positivo e modesto", deixa de ter sustentação. Como a inclinação é praticamente nula, a leitura do resíduo reduz-se, na prática, à comparação com a média do grupo de referência, e o argumento de que a condição lexical seria "explicada pela frequência" perde o mecanismo — ainda que `dialeto_B` (+0,074) continue indistinguível de `controle_raridade` (+0,070) e não sobreviva à correção (p ajustado 0,084).
- **Atenção no eixo de caráter completo:** o viés de macrorregião de +0,1952 passa de p ajustado 0,0486 a 0,0018. Continua sendo o artefato de tokenização desfeito pela restrição a token único, e continua vedada a sua citação como resultado; o aumento de significância é o aumento de poder aplicado ao mesmo artefato.

**Decisões pendentes da equipe.** (1) ~~Como reescrever o item 1.14 e as passagens que dele dependem~~ — **decidida em 14/09/2026**: o item 1.14 foi reescrito, mantendo a reprodução do bloco lexical pelo controle de raridade e retirando a frequência como mecanismo, com a hipótese de marcação de registro declarada como não testada. Atualizados na mesma rodada 1.1, 1.15, 1.17, 1.17-A, 1.19, 3.1 e 3.5 dos achados, `CLAUDE.md` (log v2.1), `README.md`, `docs/resumo_para_orientacao.md`, `docs/questoes_para_orientacao.md`, `docs/dataset-spec.md` e `docs/ficha_conjunto.md`; `docs/roadmap.md` e os relatórios `explicito.md` e `construcional.md` receberam aviso de revisão, preservando o registro das execuções. (2) ~~Se o desenho da calibração deve passar a modelar a moldura~~ — **decidido em 14/09/2026: será feito**, antes do crescimento das condições de teste, porque o desenho escolhido condiciona como aqueles pares são montados. A razão é de proteção do resultado 1.17: os pares de menção explícita são quase todos enunciados de autoidentificação (*Sou baiano*, *Meu pai é carioca*), forma ausente do grupo de referência, e a objeção de que esse tipo de enunciado produz |Δ| elevado qualquer que seja o rótulo não tem, hoje, resposta. Trabalho na branch `controle-moldura`; desenho em 2.10. (3) Se a hipótese de marcação de registro merece teste próprio, com pares raros de registro neutro contra raros de registro marcado — **adiada em 14/09/2026 para outra oportunidade**, por decisão da equipe. Não altera nenhuma das três conclusões principais e exigiria critério validado do que é registro marcado, idealmente por juízes. Registrada como candidata a trabalho futuro no artigo; quando retomada, o ponto de partida é o contraste entre os cinco itens de `controle_raridade` e itens de raridade equivalente e registro neutro.

**Impacto medido da exclusão, e por que ela não é aplicada agora.** A reanálise sem o par duplicado, executada fora do repositório sobre `explicito_pares.json`, altera pouco o passo 5.4 e não muda nenhuma conclusão: a reta passa de 0,1296 + 0,0308·log₁₀(razão), R² = 0,159, a 0,1323 + 0,0298·log₁₀(razão), R² = 0,151; o gentílico de estado passa de p ajustado 0,0012 a 0,0004, a macrorregião de 0,0038 a 0,0045, e o controle positivo de 0,0009 a 0,0004. Nenhuma condição cruza o limiar de 0,05. A exclusão, contudo, alcança três análises — a reta do passo 5.1 (`teste_construcional.py`, `CALIBRACAO`), a do passo 5.4 (`teste_explicito.py`) e o grupo de referência do passo 5.5 (`analise_valencia.py`, `REFERENCIA`), de que sai o desvio-padrão de 0,1182 empregado em `meta_pares_minimos.py` — e cerca de dez documentos que citam seus valores, entre eles `CLAUDE.md`, `docs/achados_para_o_artigo.md` e `docs/resumo_para_orientacao.md`. Como a incorporação dos 55 pares medidos reabre as mesmas análises e altera os mesmos valores, **a exclusão será aplicada na mesma rodada**, para que os números publicados mudem uma única vez. Até lá, os valores vigentes são os que incluem o par duplicado.

### 2.10 Controle de moldura para a menção explícita — APROVADA e EXECUTADA em 14/09/2026; reformulação de 1.17 pendente

Desenho da decisão (2) de 2.9, aprovado pela equipe em 14/09/2026. Predições versionadas em `e852c5a` e análise em `f7b1cdc`, ambas antes da medição; resultado ao final desta seção.

**Pergunta.** A resposta do modelo à menção explícita (1.17) é específica do rótulo nordestino, ou é o que qualquer troca de rótulo regional produz num enunciado de autoidentificação? O PLL é calculado sobre o atributo mascarado, com o enunciado como contexto; um enunciado que descreve a pessoa (*Sou baiano*) tem razão para deslocar a probabilidade de atributos de pessoa mais que um enunciado sobre objeto (*Quebrei o prato*), e o grupo de referência não contém enunciados do primeiro tipo.

**Escopo.** Os 29 pares de menção explícita: `explicito_regiao`, `explicito_gentilico`, `explicito_toponimo` e `controle_explicito`. As famílias implícitas ficam fora desta rodada, por serem nulas e a objeção incidir sobre o resultado positivo.

**Construção.** Para cada par de teste, um par-controle com **a mesma frase e o mesmo lado de comparação**, trocado apenas o rótulo nordestino por rótulo equivalente de outra região que não o Sudeste, na mesma categoria — macrorregião por macrorregião, gentílico de estado por gentílico de estado, estado por estado, capital por capital. Exemplo: *Sou baiano, e minha família também* / *Sou fluminense, e minha família também* recebe o controle *Sou gaúcho, e minha família também* / *Sou fluminense, e minha família também*.

**Região do rótulo-controle: Sul, por sondagem.** Os rótulos do Sul pareiam com os nordestinos em frequência e segmentação — *gaúcho* (11,5 por milhão, 1 subtoken), *paranaense* (6,3; 1), *catarinense* (6,8; 1) contra *baiano* (9,6; 1) e *cearense* (7,1; 2); *sulista* (2,2; 2) contra *nordestino* (4,3; 2); *Paraná*, *Curitiba* e *Florianópolis*, todos de 1 subtoken, contra *Ceará*, *Recife* e *Fortaleza*. Os do Norte são raros e fragmentados (*nortista*, 0,32; *amazonense*, 3 subtokens) e compartilham estigma regional com o Nordeste, o que confundiria a pergunta. **Duas exceções:** nos pares em que o lado de comparação já é do Sul (*Sou nordestino, nascido e criado* / *Sou sulista…*; *Todo nordestino sabe disso* / *Todo gaúcho…*), o rótulo-controle vem do Centro-Oeste (*goiano*).

**Análise.** Pareada por frase: para cada frase k, D_k = |Δ|teste − |Δ|controle. Teste unilateral de D médio > 0 por permutação de sinais no nível da frase, por condição, com correção de Holm sobre as quatro condições. O reagrupamento pessoa/lugar permanece exploratório: os pares de teste são os mesmos que sugeriram a hipótese.

**Predições, registradas antes da medição.**

- Se a resposta for específica do Nordeste: D > 0 em `explicito_gentilico` e `explicito_regiao`, as duas condições que sobreviveram à correção; D próximo de zero em `explicito_toponimo`.
- Se D for próximo de zero nas duas: o modelo responde a rótulo regional em enunciado de autoidentificação, e não ao Nordeste em particular. O item 1.17 teria de ser reformulado nessa direção, o que continua sendo resultado, mas outro.

**Custo.** 29 pares novos, 812 medições; cerca de quatro minutos na máquina local, pela conferência de 14/09/2026, ou o notebook de medição.

**Consequência para as condições de teste.** Se aprovado, o desenho pareado passa a ser o padrão: cada par de teste novo nasce com seu controle na mesma frase. O pareamento remove a variância de moldura, o que tende a reduzir o número de pares necessário por condição; a meta de 40 será recalculada sobre o desvio-padrão de D depois desta medição.

**Resultado, 14/09/2026.** Medição local em processador: 812 medições em 29 pares-gêmeos, as 4.088 anteriores intactas. Tabela em `experimentos/resultados/tabelas/moldura_tabelas.md`.

| Condição de teste | Frases | D médio | IC 95% | D > 0 | p exato | p Holm |
|---|---|---|---|---|---|---|
| macrorregião | 8 | +0,0279 | −0,0138 a +0,0692 | 6/8 | 0,1211 | 0,3633 |
| gentílico de estado | 8 | +0,0158 | −0,0994 a +0,1219 | 5/8 | 0,3984 | 0,7969 |
| topônimo | 8 | −0,0010 | −0,0490 a +0,0494 | 4/8 | 0,5117 | 0,7969 |
| conjunto explícito original | 5 | +0,0398 | +0,0117 a +0,0775 | 5/5 | 0,0312 | 0,1250 |

**A predição de especificidade não se confirmou.** Nas duas condições que sustentam 1.17, o rótulo nordestino não produz resposta detectavelmente maior que o rótulo do Sul, ou do Centro-Oeste, na mesma frase. Vale, pelo registro prévio, o desfecho alternativo: o modelo responde a **rótulo regional em enunciado de autoidentificação**, e não se detecta resposta específica ao Nordeste.

**Três elementos que o qualificam.**

1. *A premissa da objeção se confirma por via independente.* Os gêmeos, que não mencionam o Nordeste, já produzem |Δ| acima do grupo de referência: mediana de 0,2492 nos de gentílico, p = 0,0005, e de 0,2036 nos de macrorregião, p = 0,019, contra 0,1539 do grupo. Análise secundária, não registrada.
2. *O nulo tem poder limitado.* Oito frases por condição; os intervalos admitem efeito específico de até +0,07 na macrorregião e +0,12 no gentílico, e a dispersão de D no gentílico é grande, de −0,29 a +0,21. O que se estabelece é ausência de especificidade **detectável**, e não sua ausência.
3. *O reagrupamento pessoa/lugar não sobrevive ao controle.* Sobre D, rótulo de pessoa rende +0,0145 e de lugar +0,0139. A diferença entre pessoa e lugar de 1.17-A é compatível com efeito de moldura — frases que descrevem a pessoa deslocam atributos de pessoa, qualquer que seja a região — e não sustenta a leitura de que *nordestino* carrega representação social que *Recife* não carrega.

**Registre-se, sem estatuto confirmatório,** que o conjunto explícito original tem os cinco pares com D positivo (p exato 0,031), condição que não podia sobreviver à correção por construção, e que é a única cujos enunciados não são de autoidentificação.

**Decisões pendentes da equipe.** (a) ~~Como reformular 1.17 e 1.17-A e as passagens que deles dependem~~ — **decidida em 14/09/2026**: 1.17 passa a afirmar resposta a rótulo regional em enunciado sobre a pessoa, sem especificidade detectável para o Nordeste, com vedação expressa às duas leituras extremas; 1.17-A é rebaixado a exemplo de método, com a leitura substantiva vedada. Atualizados na mesma rodada 1.18, 2.8, 3.1 e 3.7 dos achados, `CLAUDE.md` (log v2.2), `README.md`, `docs/resumo_para_orientacao.md`, `docs/questoes_para_orientacao.md`, `docs/dataset-spec.md` e o bloco de revisão de `docs/roadmap.md`; o relatório `explicito.md` recebeu aviso.

### 2.11 Controle intrarregional e meta do desenho pareado — ABERTA e DECIDIDA em 14/09/2026; crescimento das condições por executar

Decisões (b) e (c) de 2.10, aprovadas pela equipe em 14/09/2026. Branch `controle-intrarregional-e-meta`. **Esta seção é versionada antes da medição do controle intrarregional**, com o código dos pares e da análise.

#### Parte (c) — controle intrarregional

**Pergunta.** O controle de moldura mostrou que o rótulo nordestino não produz mais resposta que um rótulo do Sul na mesma frase. Resta saber se o modelo responde a **diferença de região** entre os dois lados do par, ou a **qualquer troca de rótulo geográfico** num enunciado sobre a pessoa. Os gêmeos de 2.10 sempre contrastam regiões distintas e não separam as duas leituras.

**Construção.** Para cada um dos 29 pares de menção explícita, um segundo gêmeo com a mesma frase e o mesmo lado de comparação, trocado o rótulo nordestino por rótulo **da mesma região do lado de comparação**: *Sou baiano, e minha família também* / *Sou fluminense…* recebe *Sou mineiro, e minha família também* / *Sou fluminense…*. Pares em `teste_explicito.CONTROLE_INTRARREGIONAL`, com o índice como pareamento e conferência automática.

**Desvios de construção, declarados.**

- Nos pares de macrorregião de lugar (`explicito_regiao` 0 a 3 e `controle_explicito` 1), não existe macrorregião dentro do Sudeste: o gêmeo usa *Minas*, estado, contra *Sudeste*, macrorregião que o contém, com mudança de preposição (*do* → *de*, *no* → *em*).
- Nos dois pares cujo lado de comparação é do Sul (`explicito_regiao` 4 e 6, *sulista* e *gaúcho*), o gêmeo intrarregional é do Sul (*catarinense*, *paranaense*).
- Mudanças de artigo ou preposição em `explicito_toponimo` 2 e `controle_explicito` 2; nomes de duas palavras (*Minas Gerais*, *Espírito Santo*, *Belo Horizonte*). Frequência não pareada, por não prever a diferença de escore (1.14).

**Medida primária, registrada.** Para cada frase k: E_k = |Δ| do gêmeo inter-regional de 2.10 − |Δ| do gêmeo intrarregional. Teste unilateral de média de E > 0 por permutação exata de sinais no nível da frase, por condição, com correção de Holm sobre as quatro condições.

**Predições, registradas antes da medição.**

- Se o modelo responde a diferença de região: E > 0 em `explicito_gentilico` e `explicito_regiao` — a troca dentro da mesma região produz menos resposta que a troca entre regiões.
- Se o modelo responde a qualquer troca de rótulo geográfico em enunciado sobre a pessoa: E próximo de zero nas duas.

**Medidas secundárias, registradas como secundárias.** D₂ = |Δ| do par de teste − |Δ| do gêmeo intrarregional, com o mesmo teste e correção; e |Δ| dos gêmeos intrarregionais contra o grupo de referência, descritivo.

**Limites declarados.** Oito frases por condição; `controle_explicito`, com cinco, não pode sobreviver à correção. Os desvios de construção concentram-se em `explicito_regiao`, uma das duas condições das predições.

**Análise:** `experimentos/analise_intrarregional.py`; tabela em `experimentos/resultados/tabelas/intrarregional_tabelas.md`.

#### Parte (b) — desenho pareado no crescimento das condições

**Regra adotada.** Todo par de menção explícita acrescentado ao conjunto nasce com seus gêmeos de moldura — inter-regional e, se (c) se mostrar informativo, intrarregional —, na mesma frase e com o mesmo lado de comparação. Registrada em `docs/dataset-spec.md` §2.4.

**A meta muda de estatística.** A de 40 pares por condição foi dimensionada para a análise de direção, sobre escore de viés com duas amostras independentes. A pergunta que decide a interpretação da menção explícita é agora a de especificidade, sobre D pareado. `experimentos/meta_pareada.py` calcula, a partir da dispersão de D nos 29 gêmeos já medidos, quantas frases por condição exclui cada efeito específico. **O efeito-alvo é decisão da equipe**, como foi o 0,08 da meta anterior, e a tabela é produzida para subsidiá-la.

**As condições implícitas ficam fora da regra, e em aberto.** Um gêmeo de moldura para sinalização dialetal implícita exigiria marcador equivalente de outra variedade (do Sul, por exemplo), o que é desenho de instrumento, e não troca de rótulo. Decisão pendente da equipe.

#### Resultado da parte (c), 14/09/2026

Medição local: 812 medições em 29 gêmeos intrarregionais; as 4.900 anteriores intactas. Tabela em `experimentos/resultados/tabelas/intrarregional_tabelas.md`.

| Condição de teste | Frases | E médio | IC 95% | E > 0 | p exato | p Holm |
|---|---|---|---|---|---|---|
| macrorregião | 8 | −0,0251 | −0,1301 a +0,0790 | 4/8 | 0,6562 | 1,0000 |
| gentílico de estado | 8 | +0,0534 | −0,0200 a +0,1247 | 5/8 | 0,1094 | 0,4375 |
| topônimo | 8 | −0,0288 | −0,1598 a +0,0628 | 5/8 | 0,5742 | 1,0000 |
| conjunto explícito original | 5 | −0,0652 | −0,1917 a +0,0353 | 2/5 | 0,7812 | 1,0000 |

**A predição de resposta a diferença de região não se confirmou**, e o desfecho não é o nulo limpo que a predição alternativa descreve: é **inconclusivo**, porque os desvios de construção declarados antes da medição dominam a variação.

- *Os gêmeos de macrorregião de lugar produzem as maiores respostas da condição.* *Eu sou de Minas* e *Minha família é toda de Minas*, contra *…do Sudeste*, rendem |Δ| de 0,367 e 0,398 — estado contra a macrorregião que o contém, com mudança de preposição. Nesses quatro pares E é fortemente negativo (média −0,169); nos quatro pares de rótulo de pessoa da mesma condição, construídos sem desvio, E é positivo nos quatro (média +0,119). A separação é posterior aos dados, e com quatro pares o menor p exato possível é 0,0625: não tem estatuto de resultado.
- *Conteúdo lexical do rótulo produz resposta própria.* *Eu sou do Espírito Santo* contra *Eu sou do Rio* rende |Δ| de 0,614, o maior valor de todas as medições de menção explícita. É plausível que o conteúdo religioso do nome desloque atributos de caráter; não foi testado.
- *Os gêmeos intrarregionais também ficam acima do grupo de referência*, nas quatro condições (p descritivo de 0,002 a 0,047). Qualquer troca de rótulo geográfico em enunciado sobre a pessoa, inclusive dentro de uma mesma região, produz |Δ| acima de pares não regionais.
- *Secundária registrada:* D₂ = |Δ| teste − |Δ| intrarregional não é significativa em condição alguma (gentílico, +0,069, p Holm 0,375).

**Consequência para 1.17.** A formulação vigente não muda: resposta a rótulo regional em enunciado sobre a pessoa, sem especificidade detectável para o Nordeste. A qualificação de que não se separou resposta a qualquer gentílico de resposta a região distinta permanece verdadeira, agora com a tentativa registrada e inconclusiva. Acrescenta-se evidência de método: a resposta é sensível ao conteúdo lexical particular do rótulo, a ponto de a construção do controle decidir o resultado.

#### Resultado da parte (b), 14/09/2026

Tabela em `experimentos/resultados/tabelas/meta_pareada.md`. Desvio-padrão de D nos 29 gêmeos inter-regionais: 0,106 combinado, heterogêneo entre condições (0,044 a 0,171, o maior no gentílico). Com as oito frases atuais e correção de Holm, o menor efeito específico detectável é de 0,140 pelo desvio combinado. Frases necessárias por condição, com Holm e desvio combinado: 20 para excluir 0,08; 14 para 0,10; 46 para 0,05. Pelo desvio do gentílico, 46, 31 e 113.

**Decisões da equipe, 14/09/2026.**

1. **Efeito específico a excluir: 0,08, com 20 frases por condição de menção explícita**, pelo desvio-padrão combinado e com correção de Holm. Coerente com o 0,08 da meta de direção e com a ordem dos efeitos já observados. **Declarado:** o gentílico, de maior dispersão, fica com menos poder que as demais condições — exigiria 46 frases para a mesma cobertura.
2. **O gêmeo intrarregional não integra a regra.** Sua construção mostrou-se frágil nos rótulos de lugar e de macrorregião, o resultado foi inconclusivo, e o custo por frase aumentaria em 50%. Cada frase nova nasce apenas com o gêmeo inter-regional. Os 29 gêmeos intrarregionais medidos permanecem no conjunto, como registro.
3. **As condições de sinalização implícita ficam fora do crescimento por ora.** Um gêmeo para elas exigiria marcadores equivalentes de outra variedade, o que é desenho de instrumento novo.

**Consequência declarada para a análise de direção.** A meta de 40 pares por condição foi dimensionada para a análise de direção, sobre escore de viés, e não é atingida com 20 frases. Pela tabela de `meta_pares_minimos.md`, com 20 pares por condição e o grupo de referência de 86, o menor viés de valência excluível sob correção de Holm fica em torno de 0,10, e não de 0,08. A equipe optou por dimensionar pela pergunta de especificidade, que é a que decide a interpretação de 1.17; a análise de direção segue com a cobertura menor, a declarar no artigo.

**Volume implicado.** Condições `explicito_regiao`, `explicito_gentilico` e `explicito_toponimo` de 8 para 20 frases, e `controle_explicito` de 5 para 20: 51 frases novas, cada uma com par de teste e gêmeo inter-regional, perfazendo 102 pares e cerca de 2.900 medições. (b) ~~Se o crescimento das condições de teste deve seguir o desenho pareado~~ — **decidida em 14/09/2026: sim**; regra e recálculo da meta em 2.11. (c) ~~Se cabe um segundo controle, com troca de rótulo dentro da mesma região do lado de comparação~~ — **decidida em 14/09/2026: sim**; desenho e predições em 2.11.

### 2.16 AUL para o eixo ocupacional — ABERTA em 15/09/2026, para depois da v1

Decisão da equipe de 15/09/2026: o eixo de prestígio ocupacional, declarado limitação do dataset v1 (decisão 16 do plano de fechamento), será **retomado ao final, caso haja tempo antes da submissão**, para entregar o conjunto mais completo. Não começa antes da marca `dataset-v1.0`. Item 18 do plano em `docs/roadmap.md`.

**Por que importa.** É a única limitação da v1 que decorre de impossibilidade de medição, e não de volume ou de validação: o PLL não compara ocupações de baixo prestígio, fragmentadas em subtokens, com as de alto prestígio, inteiras (achados 1.1 e 1.20). O AUL, de Kaneko e Bollegala (2022), é a via proposta na literatura para esse caso.

**Plano completo** em `docs/plano_aul_eixo_ocupacional.md`: o que já existe no código, as quatro variantes candidatas, a escolha da variante sem olhar as condições de teste (controle positivo, sanidade e independência do comprimento do atributo), registro prévio, análise, e critério de abandono — se nenhuma variante se validar, a limitação permanece e a tentativa é registrada como resultado de método.

**Encerra a pendência:** execução do plano até A5, ou abandono registrado em A6.

### 2.15 Dispersão e defasagem da documentação — ABERTA em 15/09/2026

Levantamento de 15/09/2026, só de leitura. **A estrutura do repositório está organizada**: código, dados e documentos separados; resultados divididos em `dados/`, `tabelas/`, `relatorios/` e `historico/`; áudio fora do versionamento; licenças, `README.md` e `pyproject.toml` na raiz. **A documentação, não.** São cerca de 100 mil palavras em 29 arquivos de texto, com cinco problemas:

1. **O mesmo resultado é repetido em muitos arquivos.** As três conclusões do projeto e seus valores aparecem em `CLAUDE.md`, `README.md`, `docs/achados_para_o_artigo.md`, `docs/resumo_para_orientacao.md`, `docs/questoes_para_orientacao.md`, `docs/roadmap.md` e `docs/dataset-spec.md`. Cada revisão de 14 e 15/09/2026 exigiu editar cerca de dez arquivos, e cada cópia é um ponto em que a versão antiga pode sobreviver.
2. **Documentos defasados sem aviso.** O quadro de abertura de `docs/dataset-spec.md` (ver 2.13); `docs/pares_minimos_v1.md`, de 31/08, que desconhece o desenho pareado e a calibração ampliada; `docs/resumo_para_orientacao.md`, datado de 31/08 e só parcialmente revisto; `AUDITORIA.md`, de 29/08, com etapas C a F sem situação conhecida; a tabela "Prioridade" do topo deste arquivo, de 31/08, cujos itens 3 e 4 estão resolvidos; e o cabeçalho "Estado atual" do `CLAUDE.md`, que ainda diz 29/08.
3. **Este arquivo cresceu além da função.** Com cerca de 19 mil palavras, mistura o que está aberto com o histórico do que foi resolvido, e deixou de ser consultável como "registro do que está aberto".
4. **As listas de pares estão espalhadas em três módulos** (`teste_sensibilidade.py`, `teste_construcional.py`, `teste_explicito.py`), com a medição associada ao par pela posição. A condição `controle_explicito` vive em um módulo e é medida por outro.
5. **`CLAUDE.md`, a memória oficial do projeto, está fora do versionamento** (`.gitignore`), apesar do precedente de perda de material que motivou este arquivo. `docs/protocolo.md` existe e é citado, mas não consta do índice do `CLAUDE.md`.

**Conduta proposta, a decidir.** Não reorganizar agora, para não reabrir o escopo da v1. Os itens 1 a 3 e 5 são consolidação de documentos, sem risco para dados ou medições, e cabem no fechamento da v1: um único documento de resultados, com os demais remetendo a ele em vez de repetir valores; histórico de pendências resolvidas movido para arquivo próprio; aviso de "histórico" nos documentos superados; e decisão sobre versionar o `CLAUDE.md`. O item 4 é refatoração de código com risco de deslocar medições, e fica para a v2.

**Decisão de 15/09/2026.** Os itens 1, 2, 3 e 5 entram no plano de fechamento da v1 como **item 17**, na fase final, depois da atualização de documentos do item 2. O item 4 fica para a v2.

### 2.14 Filtro 1 inviável na forma prevista — ABERTA em 15/09/2026

O protocolo de validação (`docs/pares_minimos_v1.md` §7; `docs/dataset-spec.md` §2.3) prevê cinco juízes falantes nativos por variedade. Em 15/09/2026 a equipe registrou não dispor de contatos nos estados-alvo, o que inviabiliza o recrutamento tanto na forma original (30 juízes) quanto na reduzida discutida na mesma data (cerca de dez juízes, só para as condições implícitas, em nível de macrorregião).

**Por que importa.** Os pares de menção explícita e de calibração dispensam juízes com justificativa declarável: a região está escrita no enunciado, ou o enunciado é neutro. As condições de sinalização implícita não: seu resultado é nulo, e sem validação de que os enunciados soam nordestinos, naturais e não caricatos, o nulo admite a leitura de que o instrumento, e não o modelo, falhou.

**Alternativas identificadas, a decidir.** (a) Substituir o Filtro 1 pela combinação de fonte dialetológica documentada e ocorrência no corpus de áudio próprio (Filtro 2), declarando a ausência de juízes como limitação; (b) consultar a orientação sobre acesso a juízes pela rede do programa; (c) painel pago de respondentes; (d) retirar a validação sem substituto, declarando a limitação. Julgamento por modelo de linguagem foi considerado e não é recomendado como substituto, por circularidade: seria um modelo validando o instrumento com que se mede viés em outro modelo.

**Decisão de 15/09/2026: alternativa (a).** Os 25 pares de sinalização implícita são validados por fonte dialetológica documentada e por ocorrência no corpus de áudio próprio; a ausência de juízes é declarada como limitação, e a consulta (b) à orientação corre em paralelo, como reforço eventual. Menção explícita e calibração ficam fora da validação, com justificativa declarada.

**Assimetria do filtro, a declarar.** O corpus tem 7,96 h. A meta original de 50 h foi derivada precisamente para que a **ausência** de uma variante rara — a negação pós-verbal, com produtividade máxima de 5,6% — fosse informativa (`docs/dataset-spec.md` §1.5). Com o volume atual, o Filtro 2 pode **confirmar** um traço, quando ele ocorre, mas não pode **reprovar** traço raro por ausência. Item sem ocorrência é classificado como "não confirmado no corpus", e não como reprovado. A coleta não é ampliada por esse motivo: a meta do corpus foi redefinida em cobertura de falantes (item 7 do `dataset-spec`) e está cumprida, e ampliar a coleta para servir ao filtro reabriria a função instrumental abandonada em 29/08/2026.

**Execução, 15/09/2026 — busca no corpus, antes da conferência humana.** `experimentos/validar_implicitos.py` associa os 25 pares a 13 traços, registra a situação de fonte de cada um e busca candidatos nas transcrições anonimizadas dos 83 arquivos (39.851 palavras do Nordeste, 23.218 do Sudeste). Tabela de contagens em `experimentos/resultados/tabelas/filtro2_implicitos.md`; trechos para conferência em `pipeline_coleta_piloto/dataset_raw/validacao_filtro2/trechos_para_conferir.md`, fora do versionamento. Duas correções de busca na mesma data: o imperativo, restrito aos cinco verbos do instrumento, rendia um candidato e passou a verbos comuns em início de oração, com a forma de indicativo como referência de proporção; a negação pós-verbal rendia sobretudo falsos positivos de resposta e de advérbio (*Eu disse, não*; *Ainda não*) e passou a excluí-los.

- **Não confirmados no corpus — nenhum candidato no Nordeste: 12 pares.** Léxico regional (`dialeto_B-00` a `B-03`, e os feixes `dialeto_C-00`, `C-01`, `C-02`, que dependem dele), comitativo com *mais* (`D-02`), *massa* avaliativo (`D-05`), *que foi que* (`D-07`), *tá com* durativo (`D-08`) e *toda vida* (`D-09`). Pela regra de assimetria, não são reprovados.
- **A conferir: 13 pares.** Imperativo (`A-00` a `A-02`; `C-03` e `C-04` dependem também de outros traços), negação pós-verbal (`A-03`, `A-04`), vocativo *menino* (`B-04`, `D-03`), vocativo *rapaz* (`D-04`), *lhe* de segunda pessoa (`D-00`, `D-01`) e *tu* sem flexão (`D-06`).
- **Três cautelas para a conferência.** (a) Os candidatos de imperativo com forma de subjuntivo no Nordeste são dominados por *veja*, de uso formal de apresentadores e de político — o confundidor de escolaridade e registro já documentado para o traço; a proporção provisória (16% no Nordeste contra 3% no Sudeste) vai na direção da fonte, mas não separa região de registro. (b) *Tu* sem flexão concentra-se em três arquivos no Nordeste, oito candidatos num só, e aparece num arquivo de São Paulo. (c) *Lhe* e *visse* têm candidatos num único arquivo cada. Candidatos de repórter ou apresentador podem não ser da variedade do estado.

**Encerra a execução:** conferência humana dos trechos (item 8 do plano) e classificação final por par — um par de feixe só é confirmado se todos os seus traços o forem.

**Conferência humana e classificação final, 15/09/2026 — execução encerrada.** A equipe conferiu 46 trechos em sete traços, com leitura comparada do assistente; duas divergências foram resolvidas pela equipe (um *rapaz* que abre resposta a pergunta, mantido; uma negação em frase cortada, sem verbo antes, excluída). Critério adotado no imperativo: *veja bem* e *veja só* são marcadores de conversa, e não ordem, e foram excluídos. Pelo mesmo critério, parte de *olha* seria marcador, e a referência de indicativo não foi conferida — **a proporção entre as duas formas não é usada**. Registro em `experimentos/resultados/dados/filtro2_conferencia.json`, sem reprodução de transcrição.

| Situação | Pares | Traços |
|---|---|---|
| **confirmado** (7) | `A-00`, `A-01`, `A-02`, `A-03`, `A-04`, `C-04`, `D-04` | imperativo (fonte verificada; 7 ocorrências em 5 arquivos), negação pós-verbal (fonte verificada; 3 em 3), *rapaz* (6 em 5) |
| **confirmado com ressalva** (5) | `B-04`, `D-03`, `D-00`, `D-01`, `D-06` | *menino*: uma ocorrência, na forma *menina*; *lhe*: duas do mesmo falante; *tu* sem flexão: também em São Paulo, não exclusivo |
| **não confirmado no corpus** (13) | `B-00` a `B-03`, `C-00` a `C-03`, `D-02`, `D-05`, `D-07`, `D-08`, `D-09` | léxico regional, *visse*, comitativo com *mais*, *massa*, *que foi que*, *tá com*, *toda vida* |

**Consequência para o dataset.** A situação de validação passa a constar de cada par em `pares_minimos.json` (esquema 1.3). Pares não confirmados permanecem no conjunto, marcados, porque o resultado nulo das famílias implícitas depende deles e a regra de assimetria impede lê-los como reprovados. **Limitações a declarar:** ausência de juízes; corpus de 7,96 h, incapaz de reprovar traço raro; conferência feita pela própria equipe; candidatos de apresentador e repórter, que podem não ser da variedade do estado.

**Questão ética associada, independente da alternativa:** a dispensa de comitê de ética registrada no item 9 do `dataset-spec` foi decidida para o corpus de áudio, e não se estende automaticamente a participantes humanos respondendo a questionário. A confirmar com a orientação caso (b) ou (c) sejam adotadas.

### 2.13 `docs/dataset-spec.md` desatualizado no quadro de abertura — ABERTA e ENCERRADA em 15/09/2026

O quadro "Estado por camada — leia primeiro", que é a primeira coisa que o leitor encontra, descreve a situação de 28/08/2026: a camada de definição dos pares mínimos como "aberta", sem objeto de execução, e o corpus de áudio a "11% da meta vigente". Os dois pontos estão superados — os pares têm tamanho, formato, desenho pareado e 204 pares medidos, e a coleta do corpus está encerrada com 83 arquivos e 216 falantes distintos. O parágrafo introdutório ("nenhuma definição de entrega") e a seção "A circularidade que a tabela não mostra" repousam sobre a mesma premissa superada. Há ainda contradição interna: §2.2.3 marca a licença como `PENDENTE`, e o item 8 do registro a dá como decidida em 31/08/2026 (CC BY 4.0).

**Encerra a pendência:** reescrever o quadro por camada e o parágrafo introdutório com o estado vigente, marcar como histórica a seção da circularidade, e alinhar §2.2.3 ao item 8 — na rodada de atualização de documentos posterior à medição de 2.12, para que os números mudem uma única vez.

**Encerrada em 15/09/2026**, no item 2 do plano de fechamento: quadro por camada e parágrafo introdutório reescritos; seções 2.1 e "A circularidade que a tabela não mostra" marcadas como histórico; §2.2.3 alinhada ao item 8 (CC BY 4.0); §2.3 e §2.5 atualizadas com a validação e o conteúdo de 306 pares. Na mesma rodada, `CLAUDE.md` (v2.4), `README.md`, `docs/resumo_para_orientacao.md`, `docs/questoes_para_orientacao.md`, `docs/roadmap.md` e os itens 1.1, 1.14, 1.15, 3.1, 3.3 e 3.7 dos achados; o plano de fechamento passou a constar de `docs/roadmap.md`.

### 2.12 Crescimento das condições de menção explícita a 20 frases pareadas — REGISTRO PRÉVIO em 15/09/2026

Execução das decisões de 2.11. Branch `crescimento-explicitos`. **Esta seção é versionada antes da medição**, junto com os pares e a análise.

**Construção e revisão.** 51 frases novas — 12 em cada uma de `explicito_regiao`, `explicito_gentilico` e `explicito_toponimo`, e 15 em `controle_explicito` —, cada uma com par de teste (rótulo nordestino contra rótulo do Sudeste) e gêmeo inter-regional (rótulo do Sul na mesma frase). Proposta em `experimentos/propor_explicitos.py`, com cinco conferências automáticas: ineditismo, ausência de palavra de atributo, rótulo como única diferença, diferença de subtokens e, em topônimo, reconhecimento pela frequência (≥ 2 por milhão, razão ≤ 2 entre Nordeste e Sul), além de igualdade de artigo e preposição entre teste e gêmeo. Revisão da equipe em três rodadas: seis duplas de topônimo substituídas por reconhecimento; `explicito_toponimo-13` substituído por diferença de preposição (*do Crato* / *de Lages* → *de Olinda* / *de Londrina*); *curitibano(a)* revertido a *paranaense* e *catarinense*, por raridade, ao custo de diferença de subtokens contra *paraibano(a)*. **Limitação declarada:** as cidades do interior, mesmo acima do limiar, são menos frequentes que as capitais, e o topônimo é a condição com menos informação para o modelo.

**Correção de medição feita junto.** `teste_explicito.py` media apenas condições ausentes do arquivo bruto; pares acrescentados a condição já medida teriam ficado sem medição, sem aviso. Passa a medir par a par o que falta e a falhar se os faltantes não forem o final da lista. O controle intrarregional não acompanha o crescimento, e a análise correspondente passa a ler só as frases que têm esse gêmeo.

**Análise primária — a de 2.10, estendida a 20 frases.** D = |Δ| do par de teste − |Δ| do gêmeo; teste unilateral de média de D > 0 por permutação exata de sinais no nível da frase, por condição; correção de Holm sobre as quatro condições. `experimentos/analise_moldura.py`.

**Regras de decisão, por condição, registradas antes da medição.**

1. p Holm < 0,05: **especificidade do Nordeste detectada** naquela condição; 1.17 é revisto.
2. p Holm ≥ 0,05 e limite superior do IC 95% de D abaixo de 0,08: **efeito específico acima de 0,08 excluído** naquela condição — o objetivo do dimensionamento.
3. Nos demais casos: **inconclusivo** na resolução pretendida.

**Expectativa registrada.** Pelos valores de 2.10 com oito frases (D médio de +0,028 na macrorregião, +0,016 no gentílico, −0,001 no topônimo) e pela dispersão de D, espera-se a regra 2 em macrorregião e topônimo e a regra 3 no gentílico, cuja dispersão (0,17) exigiria 46 frases (`meta_pareada.md`). Para `controle_explicito`, cujos cinco pares originais tinham D positivo, a indicação de 2.10 é testada pela primeira vez com poder: resultado pela regra 1 sustentaria que a especificidade aparece em menção de terceira pessoa e não em autoidentificação — leitura a registrar como exploratória, porque a hipótese nasceu dos cinco pares.

**Secundária registrada.** A mesma análise restrita às frases novas, como replicação com frases que não participaram de nenhuma decisão anterior. Não entra nas regras de decisão.

#### Resultado, 15/09/2026

Medição local: 2.856 medições em 102 pares, em 901 s; as anteriores intactas. Análise primária em `experimentos/resultados/tabelas/moldura_tabelas.md`. A primeira execução de `analise_moldura.py` não terminou: o reagrupamento exploratório pessoa/lugar passou a 30 frases, e a permutação exata de 2^30 atribuições foi interrompida; a função passou a sortear 200 mil atribuições acima de 20 frases (`79d62d3`). A análise primária, com 20 frases por condição, seguiu exata.

| Condição | Frases | D médio | IC 95% | D > 0 | p Holm | Regra | Expectativa registrada |
|---|---|---|---|---|---|---|---|
| macrorregião | 20 | −0,0210 | −0,0704 a +0,0188 | 11/20 | 0,7922 | 2 — exclui D > 0,08 | confirmada |
| gentílico de estado | 20 | +0,0147 | −0,0537 a +0,0852 | 11/20 | 0,6861 | 3 — inconclusivo | confirmada |
| topônimo | 20 | +0,0108 | −0,0163 a +0,0383 | 12/20 | 0,6790 | 2 — exclui D > 0,08 | confirmada |
| conjunto explícito original | 20 | +0,0262 | +0,0052 a +0,0446 | 18/20 | 0,0409 | 1 — especificidade detectada | leitura exploratória, como registrado |

**Leitura.** Nos enunciados de autoidentificação não há resposta específica ao Nordeste acima de 0,08 em macrorregião e topônimo, e o gentílico permanece sem resolução, como previsto pela sua dispersão. Na menção em terceira pessoa, a especificidade é detectada, com três qualificações que acompanham o registro prévio: (a) a hipótese nasceu dos cinco pares originais, e a leitura é exploratória; (b) o efeito é pequeno — o limite superior do intervalo, +0,045, fica abaixo do próprio limiar de 0,08; (c) restrita às quinze frases novas, que não participaram de decisão anterior, a condição não sobrevive à correção (D +0,0217, 13/15, p Holm 0,2046). Os gêmeos sem Nordeste seguem acima do grupo de referência em macrorregião, gentílico e conjunto original, confirmando o efeito de moldura; o reagrupamento pessoa/lugar sobre D segue nulo (−0,009 contra +0,013).

**Consequência:** a regra 1 exige revisão de 1.17, que passa a registrar especificidade pequena, exploratória e não replicada isoladamente na menção em terceira pessoa, mantendo a ausência de especificidade acima de 0,08 na autoidentificação. Texto a propor à equipe no item 2 do plano de fechamento.

**Reanálise de direção (1.19), com 20 frases por condição — e um sinal novo a declarar.** Tabela em `experimentos/resultados/tabelas/valencia_tabelas.md`.

- *Eixo de caráter completo:* macrorregião +0,2119 (p Holm 0,0004) e conjunto explícito original +0,1571 (0,0020); gentílico e topônimo não sobrevivem.
- *Eixo de caráter restrito a token único, que é o controle do artefato de 1.1:* **nenhuma condição sobrevive à correção** — macrorregião +0,0945 (p bruto 0,058, Holm 0,405), conjunto original +0,0684 (Holm 0,798) —, com o controle positivo a +0,4758 (Holm 0,0004). A formulação de 1.19 segue sustentada pela análise registrada.
- **Mas as estimativas subiram, e há sinal exploratório.** Com oito frases, a macrorregião restrita valia +0,0309; com vinte, +0,0945. No reagrupamento exploratório pessoa/lugar restrito a token único, rótulo de pessoa rende +0,1226 com p = 0,0057, contra −0,0071 de lugar. É análise posterior aos dados, sobre agrupamento que o controle de moldura desfez em |Δ|, e não tem estatuto confirmatório — mas é a primeira vez que um sinal de direção aparece na versão controlada da tokenização, e **não pode ser omitido** ao se escrever 1.19. Com 20 frases, a análise de direção exclui vieses a partir de cerca de 0,10 (2.11), e +0,09 está dentro dessa margem.
- *Eixo de ocupação:* sem medição válida; valores não citáveis (1.20).

**Meta pareada recalculada.** Desvio-padrão combinado de D: 0,1034 com 80 frases (era 0,106 com 29). Para excluir 0,08 sob Holm, 19 frases por condição — as 20 adotadas bastam pelo desvio combinado. Pelo desvio do gentílico (0,161), seriam 42, o que confirma a leitura inconclusiva daquela condição.

**Decisão de 15/09/2026 — duas questões vão para fase posterior ao dataset v1.** (a) A resolução do gentílico de estado, que exigiria cerca de 42 frases pelo seu desvio-padrão de D; (b) a confirmação do sinal exploratório de direção em rótulos de pessoa, que exigiria mais frases na análise de direção. Nenhuma invalida o conjunto de dados — alteram o que o artigo pode afirmar, e ficam declaradas como limitação. Não entram no critério de conclusão da v1.

**Consequência adicional:** o item 1.19 também é revisto no item 2 do plano — mantendo a ausência de viés sobrevivente à correção na versão controlada, e declarando o aumento das estimativas e o sinal exploratório em rótulos de pessoa.

**Reanálises decorrentes, sem estatuto confirmatório novo.** `teste_explicito.py` (resíduo contra o grupo de referência, 1.17) e `analise_valencia.py` (direção, 1.19) serão regerados com 20 frases por condição; seus valores entram nos documentos na rodada de atualização, e a meta pareada é recalculada sobre a dispersão de D observada.

---

## 3. Bibliografia e verificação de fontes

### 3.1 Percentuais de Oliveira (2017) — bloqueante

Fontes secundárias divergem quanto a Fortaleza: uma indica predomínio subjuntivo, outra indica indicativo favorecido com peso relativo 0,66. O capítulo não pôde ser consultado (repositório da editora devolveu HTTP 403). Referência: *O imperativo gramatical nas capitais do Nordeste*, em Lopes, Oliveira e Parcero (orgs.), *Estudos sobre o português do Nordeste*, Blucher, 2017, p. 27–44.

### 3.2 Índice de 94% atribuído ao Rio de Janeiro

Registrado na revisão v1.3 do `CLAUDE.md` e **não confirmado por nenhuma fonte** consultada. Não deve ser citado enquanto a origem não for localizada.

### 3.3 Dados de imperativo para as capitais de SP e RJ

Só existe, em fonte verificada, o contraste entre cidades do interior — Campinas-SP 81% contra Feira de Santana-BA 47% (Figuereido, 2025). Faltam dados de capital em fonte primária.

### 3.4 Cavalcante (2007)

Citado por Santos e Vitório (2025) como o estudo de maior índice de negação pós-verbal (5,6%), em comunidades rurais afro-brasileiras da Bahia. Recuperar para avaliar se o contexto restringe a generalização do marcador.

### 3.5 Referências apoiadas em fonte secundária

ALECE (Bessa, 2010) e Atlas Prévio dos Falares Baianos (Rossi, 1963) foram obtidos por resumo, não por consulta ao impresso. O ano de defesa do ALiPE segue por confirmar. O sítio do estudo de palatalização do ALiB responde apenas por HTTP e não pôde ser recuperado.

### 3.6 Fonte para os marcadores lexicais

Nenhum item de M3 — *arretado*, *aperreado*, *avexado*, *oxe*, *visse* — tem fonte dialetológica citável. Ou se localiza fonte, ou entram na validação declarados como candidatos sem respaldo.

---

## 4. Pipeline e execução

### 4.1 O piloto de medição exige GPU

As três medições que justificam o piloto — rendimento por camada, WER estratificado por variedade e DER — dependem de transcrição e diarização. Na máquina local, o modelo `large-v3` opera abaixo do tempo real e o `pyannote.audio` não está instalado. Executar a esteira completa em ambiente com GPU é mais econômico que baixar localmente e transferir centenas de megabytes depois.

**Encerra a pendência:** montar notebook que receba o plano de coleta e o `HF_TOKEN` e execute coleta, transcrição e diarização no mesmo ambiente.

### 4.2 Suposições de fala não calibradas

O cálculo da meta de volume assume 130 palavras por minuto, 9 palavras por oração e 5% de orações negadas. São estimativas declaradas, não medições. As primeiras horas transcritas devem substituí-las.

### 4.3 Rendimento por camada não medido

Supôs-se que sobra 35% da duração em vox-pop, 60% em rádio e TV e 70% em vlog, depois de descontar vinheta, música, silêncio e turnos de locutor de outra variedade. Se o rendimento real de vox-pop for metade do suposto, a meta de 50 h dobra.

### 4.4 Heurísticas do planejador não calibradas

`selecionar_videos.py` usa teto de 35% por canal, recorte de 10 minutos, descarte dos 120 segundos iniciais e mínimo de um vídeo por canal. São escolhas razoáveis e não medidas. O descarte inicial, em particular, foi fixado para pular vinheta e escalada, sem verificação de que 120 segundos bastam.

### 4.5 Vídeos com restrição etária falham, e a falha não é aleatória

Constatado em 27/08/2026: parte dos vídeos dos canais listados exige autenticação — o `yt-dlp` responde com "Sign in to confirm your age" e o download é abortado. Como `ignoreerrors` está ativo e `coletar_lote` trata exceções por vídeo, um lote não é interrompido; o vídeo simplesmente não entra.

O problema é que a perda **não é aleatória**. A restrição etária recai tipicamente sobre matérias de violência e crime, que constituem parcela expressiva do vox-pop de telejornalismo policial — justamente o conteúdo em que moradores são entrevistados na rua. A exclusão silenciosa removeria um tipo de conteúdo, e possivelmente em proporção desigual entre canais e estados, produzindo viés de amostragem sem deixar rastro no conjunto final.

**Encerra a pendência:** contabilizar e reportar as falhas por canal e por estado, em vez de descartá-las em silêncio; avaliar se a proporção de perda difere entre grupos regionais; e decidir se o caso justifica autenticação por cookies, o que traz suas próprias implicações de termos de uso.

### 4.6 Dependência de versão do yt-dlp e de runtime de JavaScript

Constatado no teste mecânico de 27/08/2026. A coleta exige duas condições que não são evidentes e que falham de modo assimétrico:

- **Versão recente do `yt-dlp`.** A versão 2026.07.04, instalada até então, devolvia HTTP 403 em todos os downloads. A atualização para 2026.08.19 restabeleceu o funcionamento sem nenhuma outra alteração. O piso foi elevado em `requirements.txt`.
- **Runtime de JavaScript disponível.** O YouTube passou a exigir execução de JS para liberar as URLs de mídia. O `yt-dlp` habilita apenas `deno` por padrão; nesta máquina existe `node`, que precisa ser declarado explicitamente. Na API Python o parâmetro é `js_runtimes` e espera **dicionário**, não lista — uma lista levanta `ValueError`.

O modo de falha é o que torna isto perigoso: **a extração de metadados continua funcionando sem o runtime**, e apenas o download falha. A triagem registra sucesso, o vídeo parece válido, e a ausência só aparece no disco.

**Encerra a pendência:** garantir que o ambiente do Colab também disponha de runtime de JavaScript e de versão recente do `yt-dlp`, verificando ambos no início do notebook em vez de descobrir a falha no meio da coleta.

### 4.8 O YouTube bloqueia download originado de datacenter

Constatado em 27/08/2026, na primeira execução do notebook no Google Colab: **0 de 51 vídeos coletados**, todos com a mesma resposta — *"Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies for the authentication"*.

A causa é o endereço de origem. Os endereços do Colab pertencem a datacenter e são reconhecidos como tal; conexão residencial não sofre o bloqueio. O mesmo plano de coleta que falhou integralmente no Colab executa sem incidente na máquina local, como demonstrado no teste mecânico do mesmo dia.

Isso **inverteu a arquitetura prevista**. A suposição anterior era de que valia coletar e processar no mesmo ambiente com GPU, evitando transferir áudio. A restrição real é outra, e reparte a esteira:

| Etapa | Ambiente | Motivo |
|---|---|---|
| Coleta | máquina local | conexão residencial não é bloqueada |
| Transcrição e diarização | Colab | exigem GPU |

A transferência passa pelo Google Drive. Para o piloto são algumas centenas de megabytes; para as 50 h do corpus final, cerca de 6 GB, o que exige planejamento em lotes.

**Alternativa descartada por ora:** autenticar o `yt-dlp` com cookies da conta do usuário contornaria o bloqueio, mas implica submeter credencial de sessão a ambiente de terceiros e opera contra a intenção explícita da plataforma. Fica registrada, não adotada.

### 4.9 Verificação manual de referência

O cálculo de WER e DER exige transcrição manual de referência: 20 minutos por estado, estratificados entre camadas, cerca de 2 h ao todo. Não iniciada.

**Atualização de 31/08/2026.** A ferramenta que fecha a conta passou a existir: `pipeline_coleta_piloto/medir_wer.py` lê o `amostra_wer.json` preenchido, calcula o WER **por estado** — nunca só o agregado, porque é a diferença entre variedades que constitui a ameaça — e informa quantos trechos ainda estão sem referência, em vez de tratá-los como acerto. Registre-se também que o dimensionamento de 20 minutos por estado é recomendação de bom senso em `experimentos/meta_volume_corpus.py`, e não cálculo de poder como os que o projeto usa para os pares mínimos.

**Decisão da equipe, 31/08/2026: o trabalho de transcrição manual fica adiado deliberadamente**, para execução posterior. Até lá, o WER permanece declarado como não medido na ficha do conjunto, e o corpus não deve ser usado para comparar desempenho de reconhecimento de fala entre variedades.

**Atualização de 15/09/2026.** A medida entrou na v1 (decisão 13 do plano de fechamento), e a amostra foi regerada sobre os 83 arquivos, na máquina local, por `pipeline_coleta_piloto/preparar_amostra_wer.py`: 900 trechos, 120,6 min, cerca de 20 min por estado (`docs/plano_corpus/03-validar.md`, "Amostras geradas em 15/09/2026"). Duas ressalvas: (a) por decisão da equipe, **os trechos com nome mascarado foram excluídos do sorteio** — de 2,0 a 5,4 min elegíveis por estado —, o que deve constar como limitação da medida; (b) a amostra **não é estratificada por camada**, ao contrário do que o primeiro parágrafo deste item previa (4.11). Resta a transcrição manual, item 11 do plano.

### 4.11 A amostra do WER não é estratificada por camada — ABERTA em 15/09/2026

**O problema.** O sorteio da amostra do WER, que reproduz a seção 6.4 do notebook, acumula trechos por estado sem controlar a camada de fonte. A composição resultante difere bastante entre estados: a camada de vox-pop responde por 13,5 dos 20 minutos do Ceará e por 4,5 dos 20 do Rio de Janeiro; a de vlog, por 8,5 minutos no Rio de Janeiro e 2,4 no Ceará e na Bahia.

**Por que importa.** O erro do reconhecedor depende das condições de gravação, e a entrevista de rua, com ruído de ambiente, tende a produzir WER mais alto. Uma diferença de WER entre estados pode, portanto, refletir a composição de camadas da amostra, e não a variedade — e, dado que a camada de vox-pop pesa mais em três dos estados nordestinos, a confusão iria na direção de atribuir ao sotaque nordestino um erro que é da condição de gravação.

**O que encerraria.** Não exige refazer a amostra nem acrescentar transcrição. Basta que o relatório do WER, depois do item 11, apresente o valor também por estado e camada, ou uma média por estado ponderada por uma composição comum de camadas, e que a comparação entre Nordeste e Sudeste seja lida sob essa ressalva. Por estar contido na leitura da condição C6, e não ampliar o escopo, é tratado como parte do item 11; a extensão de `medir_wer.py` para o recorte por camada é pequena e será feita quando houver referências a medir.

### 4.10 Anonimização das transcrições — RESOLVIDA em 02/09/2026

A seção 1.4.2 do protocolo exige mascarar nomes próprios de terceiros — não o do autor do vídeo — antes de qualquer publicação. Com a decisão de 31/08/2026 que autorizou publicar as transcrições, a anonimização deixou de ser cláusula de protocolo e passou a ser pré-condição técnica de entrega.

`pipeline_coleta_piloto/anonimizar_transcricao.py`, escrito na mesma data, opera em duas fases: a primeira detecta nomes de pessoa e monta uma planilha de revisão, com contexto de cada ocorrência e uma sugestão de mascarar ou manter; a segunda **recusa-se a executar** enquanto houver item não confirmado por uma pessoa, e grava cópias mascaradas sem tocar no material original. A máscara alcança tanto o texto do segmento quanto a lista de palavras com marcação temporal, e uma verificação final falha ruidosamente se algum nome sobreviver.

A automação é deliberadamente parcial, pelas mesmas razões que motivaram a curadoria manual em 6.2 e 6.4: os reconhecedores de entidade disponíveis para português são treinados em texto jornalístico formal e degradam em fala espontânea transcrita por ASR, perdendo sobretudo apelido e forma de tratamento — que é justamente o que a fala de rua usa.

**Atualização de 01/09/2026.** A ferramenta foi executada em fase de proposta e a classificação foi construída; a revisão humana não começou, e a etapa foi interrompida por decisão da equipe, para ser retomada em sessão dedicada. **O estado completo, com a política de decisão, os números e os erros conhecidos, está em `docs/anonimizacao.md`** — é por ali que a retomada deve começar.

**Resolvida em 02/09/2026.** Os 307 itens foram revistos e a fase de aplicação foi executada: 52 arquivos anonimizados, 176 nomes mascarados, e a conferência posterior da saída não encontrou nome que devesse sair e tenha sobrevivido, nem nome que devesse permanecer e tenha desaparecido. **O registro completo está em `docs/anonimizacao.md`.**

Dois resultados da revisão merecem registro por valerem para além desta coleta:

1. **A varredura automática erra sobretudo por excesso, e o excesso custa corpus.** Oitenta e um dos 307 itens tiveram a classificação corrigida, e 62 dessas correções foram falsos positivos de pessoa — palavra comum capitalizada em início de frase (`Mané`, `Poxa`, `Calma`, `Parabéns`), topônimo, marca, doença, título de obra e erro de transcrição. São exatamente o material linguístico que o projeto estuda. Na direção contrária houve **um** erro: o autor de um canal classificado como terceiro.
2. **A conferência por amostragem foi implementada e usada**, nas fases `amostra` e `aceitar-bloco` do script, que gravam no próprio arquivo como cada item foi confirmado. Duas amostras sucessivas reprovaram e obrigaram à passagem item a item; a terceira, depois das correções, passou.

**Conferência humana concluída em 02/09/2026.** A equipe percorreu os nomes de pessoa que a revisão decidiu manter e fixou dois critérios que valem para as coletas seguintes:

1. **Equipe de canal não se mascara.** Repórter, apresentador, cinegrafista, correspondente e dono de canal ficam com o nome no texto, por estarem no papel profissional deles. A equipe chegou a mandar mascarar treze desses nomes e reverteu ao constatar que eram todos dessa natureza.
2. **Convidado não é figura pública.** Quem é chamado a dar entrevista ou a comentar um assunto — o médico convidado ao programa de saúde, o advogado convidado ao podcast — é terceiro e se mascara, ainda que aceite o convite de bom grado. Aceitar aparecer na TV não é aceitar entrar num banco de dados de pesquisa. Foi por esse critério que o advogado convidado a um podcast passou a mascarado, e o caso revelou uma incoerência: o script o classificara como figura pública porque a palavra "vereador" aparece no contexto, quando ela nomeia o assunto que ele comenta, não o cargo dele.

**Uma ressalva que a conclusão não elimina, e precisa ir para a limitação do conjunto:** o critério sobre equipe de canal é da equipe, mas *quem é equipe* foi classificação do assistente, não conferida trecho a trecho. Se alguém classificado como repórter for na verdade um entrevistado, o nome vai publicado.

**Custo da anonimização em coleta futura, medido em 02/09/2026.** A etapa é **por arquivo e não se transfere**: cada arquivo novo traz nomes novos, e nenhum trabalho já feito os cobre. A proporção observada é de **cerca de seis nomes por arquivo** (307 em 52), de modo que trinta arquivos novos implicariam cerca de cento e oitenta itens.

O que **melhora** com o tempo é a taxa de falso positivo, e ela foi medida. Dos 63 falsos positivos que a revisão de 02/09/2026 teve de corrigir a mão, **33 (52%) a lista `NAO_SAO_PESSOAS` já resolveria sozinha** numa execução seguinte, porque foram incorporados a ela. Os 30 restantes voltariam a exigir juízo, e por dois motivos distintos:

- **Não são listáveis de antemão:** títulos de obra, nomes de instituição, topônimos e erros de transcrição são novos a cada coleta.
- **Foram deliberadamente deixados de fora**, por serem também antropônimo plausível — incluí-los faria o script preservar em silêncio o nome de alguém real (ver seção 6 de `docs/anonimizacao.md`).

**Automatizar a distinção "é palavra comum ou é nome" foi testado e reprovado.** Duas regras foram avaliadas contra os dados de 02/09/2026: (a) *o token aparece em minúscula em outro ponto do corpus* pegou apenas 13% dos falsos positivos; (b) *a forma minúscula é palavra conhecida do léxico do spaCy e não é analisada como nome próprio* pegou 35%, **mas preservaria por engano 14 nomes de pessoa real**, entre eles os de duas pessoas em matéria sensível. A segunda erra na direção que expõe gente e por isso não pode decidir. Serve, quando muito, para **ordenar a fila de revisão**, pondo à frente os itens com maior chance de serem falso positivo — o que reduz o tempo sem transferir a decisão à máquina.

**O que reduz custo de verdade, em ordem de efeito:**

1. **Alimentar `NAO_SAO_PESSOAS` a cada rodada.** É exato, permanente e cumulativo: hoje tem 70 entradas e resolve metade dos falsos positivos observados.
2. **Codificar os dois critérios fixados em 02/09/2026** — equipe de canal não se mascara; convidado não é figura pública. O segundo corrigiria um defeito real de precisão: o script toma qualquer qualificador próximo do nome como sendo o papel *daquela* pessoa, e foi assim que um advogado convidado a comentar eleições virou "figura pública" porque a palavra "vereador" aparecia no trecho.
3. **Ordenar a revisão pelo sinal de triagem** descrito acima, sem deixá-lo decidir.

**A parte irredutível.** Nomes de pessoa novos exigem juízo humano a cada coleta, e o volume cresce linearmente com os arquivos. A sessão de 02/09/2026 foi longa porque construiu as fases de amostragem, descobriu os critérios e encontrou os modos de falha; esse custo é de uma vez só. A revisão em si, com os critérios já fixados e a lista já alimentada, deve ficar na ordem de uma hora para cada trinta arquivos novos.

**Aberto, e encontrado em 02/09/2026: o título do vídeo desfaz parte da máscara.** Os planos de coleta (`plano_piloto.json`, `plano_resto.json`, `plano_fatia.json`) guardam o título público de cada vídeo, e alguns títulos nomeiam pessoas cujo nome foi mascarado na transcrição. Dois casos mostram o alcance do problema:

- Um vídeo cujo título anuncia a doença rara e grave de uma pessoa nomeada. O nome está mascarado na transcrição pela regra de matéria sensível, e o título o devolve junto com a informação de saúde.
- Um vídeo cujo título nomeia a pessoa perfilada e a descreve como fundadora de uma instituição. A revisão a tratou como terceiro citado, quando o título indica que ela é o próprio objeto da reportagem — o que a aproxima de "pessoa conhecida perfilada pelo trabalho", que a seção 5 manda manter.

**Não é descuido, e não se resolve apagando o título.** O protocolo publica identificadores de vídeo justamente para permitir reprodução (§1.4.2), e quem tem o identificador assiste ao vídeo e ouve todos os nomes. A máscara nunca prometeu tornar as pessoas inencontráveis; ela evita que o conjunto de dados, por si, seja um índice de nomes pesquisável. O título, porém, fica **dentro** do conjunto e é pesquisável — está numa posição intermediária que o desenho não previu.

**Encerra a pendência:** decidir entre três saídas — manter o título e declarar a limitação na ficha; guardar só o identificador e recuperar o título sob demanda, o que preserva a reprodução e tira o nome do arquivo; ou mascarar no título os mesmos nomes mascarados na transcrição, o que é coerente mas dificulta conferir a que vídeo o registro corresponde. A segunda parece a mais equilibrada e não foi decidida.

**Fica aberto, e não bloqueia:** curar, por canal, o nome real do autor a preservar — hoje `fontes.json` guarda apenas o nome do canal, e o script deriva dele um palpite explicitamente marcado como tal. Na execução de 02/09/2026 essa lacuna produziu um erro real, corrigido a mão.

---

## 4-A. Achados do piloto de 27/08/2026

Medições completas em `experimentos/resultados/relatorios/piloto_medicoes.md`.

### 4A.1 Detecção de marcadores por expressão regular é inadequada

A busca automática contabilizou "que não" como negação pós-verbal, "ele vai" como imperativo e o subjuntivo de *ver* como o marcador recifense *visse?*. Os três erros inflam a contagem, e de modo desigual entre marcadores — o que enviesaria a comparação entre grupos, não apenas a sua magnitude.

**Encerra a pendência:** detector que opere sobre texto com pontuação preservada e com análise morfossintática capaz de distinguir imperativo de presente do indicativo e de identificar fronteira de oração. Sem isso, o Filtro 2 não pode ser aplicado em escala.

### 4A.2 Hipótese do locutor dominante em vox-pop não verificada

O recálculo do rendimento supõe que o locutor dominante da camada de vox-pop seja o repórter, e não um entrevistado loquaz. Da suposição depende a estimativa de fala aproveitável e, por consequência, a meta de volume.

**Encerra a pendência:** verificar se o mesmo perfil de voz reaparece em vídeos distintos do mesmo canal, o que caracterizaria o repórter.

### 4A.3 Revisão da meta de volume, pendente de piloto maior

As medições indicam cerca de 6,4 h de áudio bruto por estado, contra as 8,3 h supostas, e cerca de 38 h no total contra 50 h. A amostra é de 6, 6 e 5 arquivos por camada, insuficiente para revisar o parâmetro. A revisão fica condicionada a piloto de maior volume.

### 4A.4 O léxico regional pode ser o caso dimensionante, e não a negação

O cálculo do passo 4.2 tomou a negação pós-verbal como marcador mais raro, e dela derivou a meta. O piloto não registrou nenhuma ocorrência de léxico regional em 1,55 h, o que levanta a possibilidade de que o léxico seja ainda mais raro. Sendo esse o caso, é ele que deve dimensionar a coleta.

**Encerra a pendência:** estimar a frequência dos itens lexicais em corpus de fala já existente, ou no próprio corpus do projeto quando alcançar volume suficiente.

---

## 5. Decisões pendentes da equipe

**Convenção de numeração, adotada em 29/08/2026.** Os itens desta seção usam o prefixo `D`, e não `5.x`. O motivo é concreto: o passo 5 de `docs/roadmap.md` também emprega subitens `5.1` a `5.6`, para **etapas de trabalho**, de modo que "5.4" designava duas coisas distintas em dois documentos — "menção explícita em volume" no roadmap e "subcorpus de TikTok" aqui. A ambiguidade já produziu erro: o item D5 permaneceu desatualizado por descrever o mesmo rumo que o roadmap descrevia, sem que a atualização de um alcançasse o outro.

Referências a estes itens devem ser escritas como `docs/pendencias.md`, D4 — e as referências ao roadmap, como passo 5.4.


### D1 Simetria entre os grupos — AVANÇADA em 31/08/2026, revisão de conteúdo FECHADA em 31/08/2026

O grupo de controle tem 9 a 11 vlogs verificados por estado; Pernambuco tinha 3. Como um canal de vlog corresponde na prática a um falante, a composição dos grupos difere. **Decisão de 31/08/2026:** reforçar PE e BA em vez de limitar por baixo.

**Busca real executada na mesma data**, por `yt-dlp`, mesma regra de atribuição do projeto (§1, geografia recorrente nos títulos recentes, não na consulta). Seis candidatos inspecionados, títulos recentes conferidos um a um:

| Canal | UF | Situação | Evidência |
|---|---|---|---|
| Vlog com Diogo | PE | **Aceito** | 6 de 6 títulos recentes mencionam Caruaru; conteúdo de vida cotidiana |
| Samiele Batista | PE | **Rejeitado em 31/08/2026** | Ancoragem forte em Caruaru confirmada, mas conteúdo é vitrine de preço de feira, não fala espontânea |
| Marcinha De jesus | BA | **Aceito em 31/08/2026** | Base real confirmada por revisão humana: Vitória da Conquista |
| Taise Walber | BA | Rejeitado | Nenhum dos 6 títulos recentes menciona Feira de Santana; achado original era vídeo avulso |
| Esterfany Silva | BA | Rejeitado | Mesmo padrão — sem menção recorrente a Feira de Santana |
| Rebeca Luiza | PE | Rejeitado | Ancoragem em Caruaru não confirmada; um título recente aponta para Catende |

Os três primeiros foram acrescentados a `pipeline_coleta_piloto/fontes.json`. É busca **parcial**, não a metodologia de três rodadas empregada no levantamento original (390 candidatos) — rendeu 2 aceitos e 1 rejeitado em 6 testados, taxa compatível com o histórico do projeto (~1 aproveitável a cada 8).

**Achado que muda o peso desta pendência.** A revisão de D2 (abaixo), que prioriza vox-pop e podcast sobre vlog, faz PE e BA atingirem o piso de 20 falantes **sem depender de vlog algum** (26,6 e 22,4 falantes projetados, respectivamente — ver `experimentos/resultados/tabelas/meta_corpus_autonomo.md`). A fragilidade de vlog em PE deixa de ser bloqueio para o piso mínimo; permanece relevante apenas para diversidade de fonte e margem acima do piso.

### Segunda rodada, 31/08/2026 — a pendência D1 é encerrada

A pedido da equipe, a busca foi retomada e executada em escala, pela metodologia do próprio projeto: vinte consultas ancoradas em municípios de PE e BA, triagem automática por `verificar_fontes.py` e revisão de conteúdo canal a canal.

| Etapa | PE | BA | Total |
|---|---|---|---|
| Candidatos distintos levantados | 84 | 94 | 178 |
| Aprovados na triagem automática | 31 | 31 | 62 |
| Aceitos após revisão de conteúdo | 7 | 6 | 13 |
| Marcados `a_confirmar` | 4 | 7 | 11 |

**Efeito sobre a assimetria.** A camada de vlog de Pernambuco passou de 4 para 10 canais verificados, e a da Bahia de 7 para 12 — contra 11 em São Paulo e 13 no Rio de Janeiro. O desequilíbrio que originou esta pendência deixa de existir. Dois canais aceitos são de vox-pop, camada que era a mais frágil dos dois estados: *SERTÃO MAMOEIRO OFICIAL*, com entrevistas de moradores rurais no sertão pernambucano, e *azulzinho Itabuna*, reportagem policial de bairro.

**As rejeições confirmam os critérios documentados.** Concentraram-se nos quatro perfis que o projeto já previa — canal de viagem, imagem sem fala, vitrine de preço e narração de ranking —, e não em casos idiossincráticos. Dois achados merecem registro:

- **Um falante migrante foi identificado e rejeitado.** O canal *Marcela Sevla* satisfaz todos os critérios geográficos de Barreiras-BA, e declara no próprio acervo a mudança de São Paulo para a Bahia. É a ameaça da Parte 3 do protocolo materializada, detectada pela leitura do conteúdo e não pelos metadados — o que reforça a conclusão da seção 6.2: contra falante migrante, o que funciona é curadoria, não automação.
- **Um caso que a ficha do conjunto não cobre.** O canal *Pietra teles*, de Jacobina, é vlog estudantil cuja autora aparenta ser menor de idade. Ficou marcado `a_confirmar`, e a decisão sobre incluir criador menor cabe à equipe antes de qualquer coleta. A ficha trata da ausência de consentimento em geral, mas não deste caso em particular.

**Questão derivada, e menor.** Com PE e BA reforçados, o piso do grupo nordestino passa a ser a **Paraíba, com 7 vlogs**. Se a equipe quiser simetria estrita com o controle, é a PB que precisa de reforço — não mais PE ou BA.

**Pendência encerrada.** Resta apenas, como trabalho opcional, a inspeção de conteúdo dos 11 canais `a_confirmar` produzidos por esta rodada, que ampliaria a margem acima do piso sem ser necessária para atingi-lo.

### D2


### D2 Composição entre camadas — IMPLEMENTADA em 31/08/2026

As proporções da seção 1.4.3 de `docs/protocolo.md` — 60% a 70% para a camada âncora, 30% a 40% para a espontânea — haviam sido fixadas antes de se conhecer o rendimento de cada fonte, e eram medidas em **horas**, herdadas da função instrumental que o corpus não tem mais (ver item #3 do registro de `docs/dataset-spec.md`).

**Decisão de 31/08/2026:** priorizar vox-pop e podcast sobre vlog, por rendimento marginal de falantes por arquivo — vlog rende exatamente 1 pessoa por canal, não importa quantos vídeos; vox-pop e podcast rendem gente nova a cada episódio adicional do mesmo canal (3,2 e 2,0 falantes novos por arquivo, respectivamente, contra 0 do vlog).

**Implementado em `experimentos/meta_corpus_autonomo.py`.** Um canal de vox-pop ou podcast agora pode contribuir com mais de um arquivo, até um teto por canal — reaproveitado de `TETO_POR_CANAL = 0.35` já usado em `selecionar_videos.py`, aqui aplicado ao piso de 20 falantes (≈ 7 falantes por canal). Vlog deixa de ser somado por padrão e só entra se vox-pop e podcast, mesmo explorados ao máximo, não bastarem.

**Resultado, com as fontes hoje verificadas:** todos os seis estados atingem o piso de 20 falantes usando **apenas** vox-pop e podcast — nenhum canal de vlog é necessário. O plano de coleta cai de 8,3 h/estado para cerca de 0,7 a 1,0 h/estado (relatório completo em `experimentos/resultados/tabelas/meta_corpus_autonomo.md`).

**Encerrada.**

### D3 CLAUDE.md fora do versionamento — PARCIALMENTE RESOLVIDA em 31/08/2026

As partes públicas do arquivo — protocolo metodológico e operacional (§1.4), esquema de dados (§1.4.1), regras de anonimização (§1.4.2), escopo e camadas de coleta (§1.4.3) e a síntese de ameaças à validade (Parte 3) — passaram a `docs/protocolo.md`, com a numeração original preservada, de modo que uma referência a "seção 1.4.2 do `CLAUDE.md`" corresponde à seção 1.4.2 daquele arquivo. Vinte linhas de referência em seis documentos foram redirecionadas.

**O que permanece.** O `CLAUDE.md` segue fora do versionamento, conservando o que é interno: o log de revisões, o estado corrente do trabalho e as orientações de sessão. Restam referências a ele em documentos e em código, e são de duas naturezas:

- **Ao log de revisões** — "revisão v1.3", "log v1.7". São menções históricas, e a decisão de versionar ou não o histórico é distinta da de versionar o método.
- **Em código e nos READMEs de subpasta** — `collect.py`, `config.py`, `meta_volume_corpus.py`, `densidade_palatalizacao.py`, `notebooks/README.md` e `pipeline_coleta_piloto/README.md`. Não foram alteradas na mesma rodada por estarem fora do escopo autorizado, e devem apontar para `docs/protocolo.md` na próxima passagem por esses arquivos.

**Encerra a pendência:** redirecionar as referências restantes em código e READMEs, e decidir se o log de revisões também deve ser versionado.

### D4 Subcorpus de TikTok, Instagram e Spotify — DECIDIDO em 31/08/2026

**Decisão: nenhuma das três plataformas será incorporada**, nem como subcorpus secundário. TikTok e Instagram permanecem excluídos pela dissociação entre origem do vídeo e origem da voz (seção 2.3.1 de `docs/fontes_coleta.md`) — risco que a checagem de reincidência de falante (D-6.4) e a checagem de falante migrante (D-6.2) já não dão conta de cobrir, e que a reabertura condicionada nunca chegou a ser justificada pela diversidade de falantes, que hoje está resolvida por vox-pop e podcast (ver D2). Spotify segue fora por vedação de download nos termos de uso (`docs/dataset-spec.md` §1.4.4).

**Encerrada.**

### D7 O conjunto de pares mínimos não tem especificação de entrega

**Aberta em 28/08/2026.** O projeto declara o dataset como sua contribuição publicável e adota CrowS-Pairs e French CrowS-Pairs como precedentes, que são artigos de conjunto de dados. O conjunto que sustentaria essa contribuição é o de pares mínimos, e dele estão definidos o desenho conceitual — princípios da seção 2 de `docs/pares_minimos_v1.md`, decomposição em blocos, protocolo de validação em dois filtros — mas **nenhuma das definições de entrega**. Faltam quatro, e as quatro são exigidas em submissão a veículo que aceite artigo de recurso:

1. **Tamanho-alvo.** O documento observa que doze itens são insuficientes e cita os 1.508 pares do CrowS-Pairs, sem fixar meta. Diferentemente do corpus de áudio, cuja meta foi derivada de requisito estatístico em `experimentos/meta_volume_corpus.py`, aqui não há número nem critério que o produza.
2. **Formato de publicação.** Não há esquema de registro definido — campos, tipos, codificação, unidade de linha. O CrowS-Pairs distribui pares com identificador, os dois lados, tipo de viés e anotações de juízes; nada equivalente foi especificado.
3. **Licença.** Não decidida. A questão é distinta da do áudio, cuja conduta está registrada em `docs/stack_tecnica.md` — publicar identificadores e código, não mídia. Os pares mínimos são texto de autoria do projeto e podem ser licenciados de modo permissivo, mas a decisão não foi tomada nem registrada.
4. **Ficha de conjunto de dados.** Não existe. É prática consolidada em publicação de recurso, e descreve motivação, composição, processo de coleta, usos pretendidos e usos desaconselhados. Este último item é particularmente pertinente aqui: um conjunto de enunciados dialetais rotulados por região presta-se a uso indevido como classificador de procedência de falantes.

**O que encerra.** Um documento de especificação de entrega, a escrever depois da decisão do passo 5 — antes dela não há critério para fixar o tamanho-alvo nem para definir o que o conjunto contém.

**Ressalva de sequenciamento.** Se o rumo adotado for o 5.3, o corpus de áudio deixa de ser instrumento do Filtro 2 e passa a entregável autônomo, e as quatro definições acima passam a ser exigíveis também para ele.

### D8 Dimensionamento da análise de direção — ENCERRADA em 29/08/2026

O diagnóstico registrado abaixo estava **parcialmente errado**, e o registro do erro importa mais que o item. Atribuía-se a inconclusividade a falta de volume; era erro de desenho. O grupo de referência da permutação empregava cinco pares quando havia vinte e seis pares não regionais já medidos e adequados ao papel. Corrigido, o controle positivo passou a sobreviver à correção, e a análise ganhou resolução **sem nenhuma medição nova**.

A providência 3 abaixo — descartar o artefato de segmentação — foi executada no eixo de caráter e **não é executável** no de ocupação, pelas razões do item 1.20 de `docs/achados_para_o_artigo.md`. Substituída pelo passo 5.6 do roadmap, que exige AUL.

**Lição de método, e é a que sobrevive ao item:** antes de atribuir um resultado inconclusivo a falta de dados, conferir se o grupo de comparação é o correto. O sintoma que denunciou o erro foi o controle positivo apresentar a maior magnitude bruta da tabela e ainda assim não passar — padrão que aponta para referência inadequada, e não para efeito ausente.

**Registro original, conservado:**

### D8-A Diagnóstico original (superado)

**Aberta em 29/08/2026.** A medida com sinal — se a resposta do modelo é preconceituosa, e não apenas diferente — está implementada em `experimentos/analise_valencia.py` e é inconclusiva por falta de resolução estatística, e não por ausência de efeito. O diagnóstico é o próprio controle positivo, que não sobrevive à correção de Holm em nenhum dos dois eixos apesar de apresentar as maiores magnitudes brutas.

**Três providências, todas de custo baixo:**

1. **Ampliar o grupo de referência.** O controle neutro tem cinco pares, e é contra ele que toda permutação é feita. Com cinco pares no grupo de referência a distribuição nula é grossa demais para que qualquer condição atinja significância após correção.
2. **Ampliar os pares por condição**, hoje entre cinco e dez.
3. **Descartar o artefato de segmentação no eixo de ocupação.** O gentílico de estado apresenta viés de −0,271, com apenas um de oito pares positivo, o que significaria ocupações de alto prestígio tornando-se mais prováveis sob o guise nordestino. Antes de qualquer leitura substantiva é preciso descartar a assimetria de tokenização registrada no item 1.1 de `docs/achados_para_o_artigo.md`, segundo a qual as ocupações de baixo prestígio são majoritariamente multi-token. O mascaramento do alvo por inteiro foi adotado para neutralizar isso e pode não bastar.

**Por que importa mais que as demais pendências.** Sem ela, o artigo afirma que o modelo distingue e não pode afirmar que deprecia — a diferença entre um resultado sobre representação e um resultado sobre viés, que é o objeto declarado da pesquisa.

### D9 Classificação de valência dos atributos não validada

A partição dos atributos entre favoráveis e desfavoráveis, e entre alto e baixo prestígio ocupacional, foi feita pelo projeto por circulação corrente e está declarada em código, em `analise_valencia.py`, para ser auditável e contestável. Atributos ambíguos — *simples*, *normal*, *séria*, *fria*, *vendedor*, *motorista* — foram excluídos em vez de arbitrados.

Não foi submetida a juízes. Como a medida de viés é inteiramente definida por essa partição, ela deve integrar o Filtro 1 quando este for aplicado, sob pena de o escore de viés depender de julgamento não validado de uma única fonte.

### D10 Proposta de linha de análise por sentimento, discutida com a orientação em 31/08/2026 — DECIDIDA em 15/09/2026: segundo artigo

**Aberta em 31/08/2026.** Três ideias trazidas de conversa com a orientação, ainda não integradas ao roadmap nem confrontadas com o desenho vigente. Registradas aqui como surgiram, em linguagem próxima do original, para não se perderem antes de decididas:

1. **Validar o Whisper por divergência de sentimento.** Sobre amostra aleatória com transcrição manual, comparar a transcrição manual e a do Whisper por análise de sentimento, perguntando se a diferença é significativa — em vez de, ou além de, computar WER diretamente.
2. **Aplicar análise de sentimento aos pares mínimos.** Selecionar frases, inserir marcadores regionais, e verificar por análise de sentimento se há divergência entre as duas condições — uma métrica nova sobre o mesmo desenho de pares que hoje usa PLL.
3. **Regressão de sentimento sobre o corpus real coletado.** "Pegar os pares dos vídeos", extrair sentimento do conteúdo dos vídeos coletados (não dos pares sintéticos), e regredir sobre Tema, Tempo, Região e outras covariáveis, com sentimento como variável a prever.

**Tensões identificadas, a resolver antes de qualquer execução:**

- **As três ideias pertencem a objetos diferentes do projeto**, e cada uma herda um estatuto distinto: (1) é validação de ferramenta (o mesmo objeto da pendência de WER, seção 2.1 dos achados); (2) é metodologicamente paralela ao desenho de *matched-guise* já em uso — troca a métrica (PLL por sentimento) mantendo pares sintéticos; (3) muda o objeto de medição para o **corpus real coletado**, o que deixa de ser uma pergunta sobre viés do BERTimbau e passa a ser sobre o conteúdo do corpus em si.
- **A ideia 3 colide com a ficha do conjunto.** `docs/ficha_conjunto.md`, seção de usos desaconselhados, item 1, adverte contra inferir características de falantes a partir do rótulo regional — e regredir sentimento sobre Região no corpus real é, estruturalmente, esse mesmo movimento, ainda que a intenção declarada seja outra. A moldura da análise (testar viés de um classificador de sentimento, ou caracterizar o corpus) precisa ser explicitada antes de rodar.
- **Um classificador de sentimento em português introduz o mesmo risco que a tokenização introduziu no BERTimbau**: pode carregar viés próprio, não medido, que se confundiria com o efeito procurado. A ideia 1, se usar divergência de sentimento como proxy de WER, herda esse risco em vez de evitá-lo — WER direto (já planejado, 2h de transcrição manual dimensionadas) é medida mais direta e sem esse confundidor.
- **Nenhuma das três está posicionada no roadmap.** Se aprovadas, precisam de numeração própria (candidata: passo 5.7, ou frente separada do passo 5) e de dimensionamento pelo mesmo padrão do resto do projeto — critério de decisão explícito antes de qualquer coleta ou medição nova.

**Encerra a pendência:** decisão da equipe sobre cada uma das três, com a moldura de interpretação da ideia 3 explicitada por escrito antes de proceder.

**Atualização de 31/08/2026.** A equipe decidiu que o esquema de campos do dataset final somará os campos já existentes (`docs/dataset-spec.md` §1.3) a três campos novos, discutidos com a orientação: **descrição ou transcrição do texto**, **features textuais** (TF-IDF citado como exemplo) e **features de áudio**. Dois pontos permanecem abertos antes de o esquema poder ser escrito em `dataset-spec.md`:

- **"Descrição" e "transcrição" não são a mesma coisa**, e a escolha entre elas reabre ou fecha a pendência #2 daquele documento. Transcrição literal exige a decisão jurídica sobre obra derivada e a anonimização ainda não implementada (Bloco 2 de `docs/questoes_para_orientacao.md`); uma descrição gerada — resumo, não verbatim — teria posição legal muito mais leve e poderia dispensar parte daquela consulta.
- **"Features de áudio" não tem conteúdo especificado.** Nenhum candidato foi indicado (MFCC, estatísticas de F0, *embeddings* de um modelo de fala, ou outro), e a escolha importa em particular para este projeto, cujo marcador de áudio é fonético — a palatalização de /t,d/ diante de /i/.

**Segunda atualização, 31/08/2026.** As duas perguntas acima foram respondidas em parte:

- **Confirmado: transcrição, não descrição.** O campo será a transcrição literal do texto. **Isto é decisão de esquema, não autorização de publicação** — continua valendo a advertência: publicar a transcrição depende da decisão jurídica sobre obra derivada (pergunta 2.1 de `docs/questoes_para_orientacao.md`) e do mascaramento de nomes próprios, que segue **não implementado**. Enquanto essas duas condições não forem satisfeitas, a transcrição integra o esquema do dado interno, mas não pode ser publicada como está.
- **Features de áudio:** confirmadas como **marcadores regionais** — não features acústicas genéricas (MFCC, F0), e sim indicadores derivados dos próprios marcadores dialetais do projeto (por exemplo, densidade de contextos de palatalização, já medida em `experimentos/resultados/tabelas/densidade_palatalizacao.md`). Lista declarada como **aberta**, a ser estendida.
- **Features de texto:** confirmado TF-IDF como primeiro item. Lista igualmente **aberta**, a ser estendida.

**Por que o esquema formal em `docs/dataset-spec.md` ainda não foi atualizado.** As duas listas de *features* são declaradas incompletas pela própria equipe ("entre outros que posteriormente vou falar pra atualizar"). O esquema daquele documento é escrito com tipo, vocabulário controlado e obrigatoriedade fechados para cada campo — entrar com uma lista aberta ali quebraria o padrão de precisão que os demais campos seguem, e obrigaria a reescrever a entrada a cada extensão. A atualização formal fica para quando as listas estiverem fechadas, ou para quando a equipe decidir registrá-las como "vocabulário aberto" deliberadamente, o que também é uma opção válida — a decidir.

**Terceira atualização, 31/08/2026 — onde a análise de sentimento entra.** A pergunta não tem resposta única: o lugar da análise de sentimento depende de qual das três ideias originais (início desta pendência) está em jogo. As três não são posições alternativas de um mesmo componente — são três papéis estruturalmente diferentes:

| Ideia | Onde entra | É campo do esquema? |
|---|---|---|
| 1 — validar o Whisper | Computada uma vez, sobre a amostra de verificação manual (as 2h de transcrição de referência já dimensionadas). É medição de controle de qualidade | **Não.** Não persiste no dado; é resultado de uma checagem pontual |
| 2 — métrica sobre os pares mínimos | Aplicada aos enunciados sintéticos em `experimentos/`, como métrica alternativa ao PLL — mesmo papel que `metricas.py` já ocupa | **Não.** É medição de experimento, não dado do corpus; não pertence a `dataset-spec.md`, e sim a um novo script de medição |
| 3 — regressão sobre o corpus real | Precisaria de um escore de sentimento **por vídeo ou trecho**, calculado a partir da transcrição. É o único dos três casos em que a análise de sentimento se tornaria dado persistido | **Sim, seria.** Entraria como item dentro de **features textuais**, ao lado do TF-IDF — é o mesmo tipo de objeto: um escore derivado do texto transcrito |

Só a ideia 3 faz da análise de sentimento um campo do dataset. Nas ideias 1 e 2 ela é ferramenta de análise, não dado armazenado — a diferença entre "está no banco de dados" e "roda sobre o banco de dados", que já foi discutida nesta mesma conversa a propósito da natureza do corpus.

**Segue pendente:** qual das três ideias a equipe pretende de fato executar. Enquanto isso não for decidido, não é possível saber se "análise de sentimento" deve ou não entrar como um dos itens declarados em aberto de *features textuais*.

**Decisão de 15/09/2026 — o sentimento vai para um segundo artigo.** A equipe dividiu o trabalho em duas publicações. A **primeira** é o artigo do conjunto de dados — corpus de áudio e pares mínimos, com as medições que os caracterizam —, e nenhuma das três ideias entra nela. A **segunda** é um artigo de análise de sentimento com PLN, construído sobre o conjunto publicado. Consequências:

- As três ideias ficam registradas como insumo do segundo artigo, sem prazo, e **fora do critério de conclusão do dataset v1**.
- A ideia 1 perde a função que tinha: a validação da transcrição na primeira fase é o WER direto, já planejado.
- As listas de *features* de texto e de áudio, que só se tornam campos do esquema se a ideia 3 for executada, também saem da v1.
- As tensões registradas acima continuam válidas e são o ponto de partida do segundo artigo: o viés próprio do classificador de sentimento, que se confundiria com diferença regional, e o conflito da ideia 3 com o item 1 dos usos desaconselhados de `docs/ficha_conjunto.md`, cuja moldura de interpretação precisa ser explicitada antes de qualquer execução.

**Quarta atualização, 31/08/2026 — três decisões de método, respondendo perguntas da equipe.**

**Sobre manter `diarizacao` no registro publicado (decisão: manter).** A pergunta era se o rótulo de locutor por trecho é necessário. É, e por um motivo que não é acessório: em vox-pop, o repórter frequentemente não é do estado, e é a diarização que separa a fala dele da do entrevistado — sem ela, o corpus incorporaria fala de fora da variedade sob o rótulo do estado errado, contaminando exatamente a variável que o projeto mede. É também o que sustenta a contagem de 211 falantes de que D1 e D2 dependem. Removê-la desfaria o próprio teto de 5% (item #5): sem separar quem fala, não há como saber quantos falantes distintos existem. Registro final escolhido como artefato a publicar (item #2 do registro de `docs/dataset-spec.md`), com `diarizacao` mantida.

**Sobre o teto de 5% por falante (decisão: manter).** A pergunta era se é crucial. É: sem ele, nada impede que 80% da fala de um estado venha de uma só pessoa loquaz, e nesse caso o corpus não representaria "a variedade de Pernambuco" — representaria o idioleto de um indivíduo. É a condição mínima para a alegação de representatividade que sustenta o corpus como entregável autônomo (item #3 de `docs/dataset-spec.md`). Continua sem verificação de identidade entre arquivos implementada (D-6.4), que é o que falta para *confirmar* que o teto é respeitado, não o teto em si.

**Sobre o falante migrante (decisão: manter como limitação declarada, não como algo a remover).** A pergunta era se impacta negativamente e como validar. Impacta, e na direção mais perigosa possível: como o fluxo migratório dominante no Brasil é Nordeste → Sudeste, um nordestino incorporado por engano ao grupo de controle **atenua** o contraste medido, empurrando o resultado para "não há diferença" — que é justamente o achado central do projeto (item 1.15 de `docs/achados_para_o_artigo.md`, sinalização implícita nula). Não é risco simétrico: ele empurra na direção que o projeto já encontrou. Não há como "validar" e descartar o risco por completo — a defesa é a checagem de coerência dialetal na curadoria manual das transcrições (D-6.2), que opera ouvindo a fala e não lendo metadados, e **não está implementada**. Continua registrada como limitação a declarar no artigo, por ser incontornável em corpus de fala pública coletado de plataforma — não é um item que se "retira".

### D5 Rumo do projeto — remetido ao roadmap

**Reduzido a ponteiro em 29/08/2026.** Este item descrevia os rumos disponíveis depois do passo 5.1, duplicando o que o passo 5 de `docs/roadmap.md` já descrevia. A duplicação teve o custo previsível: permaneceu registrando "restam três rumos: 5.2, 5.3 e 5.4" depois de 5.4 e 5.5 terem sido concluídos e de 5.6 ter sido aberto.

**O rumo do projeto vive no passo 5 do `docs/roadmap.md`, e só lá.** Situação em 29/08/2026: 5.1 concluído com resposta negativa, 5.4 concluído com resposta afirmativa, 5.5 concluído sem viés detectável, 5.6 aberto e é a última medição pendente; 5.2 e 5.3 não iniciados.

O que permanece **aqui**, por ser decisão e não etapa: a escolha entre prosseguir a medição no modelo e reposicionar o artigo. A recomendação registrada em `docs/achados_para_o_artigo.md`, seção 5, é o terceiro caminho — o contraste entre sinalização implícita e explícita.

### D6 Validação dos marcadores construcionais, caso o 5.4 confirme

Os dez marcadores de `dialeto_D` foram formulados para testar a **existência de sinal**, e não como itens de instrumento. Três deles — *lhe* de segunda pessoa, *tu* sem flexão, comitativo com *mais* — têm respaldo na literatura dialetológica cuja conferência em fonte primária permanece pendente. Os demais são candidatos derivados do corpus próprio (*menino*, *rapaz*, *massa*) ou sem fonte alguma (clivagem *que foi que*, durativo *tá com*, *toda vida*).

Dado o resultado negativo, não há razão para submetê-los ao Filtro 1 agora. A pendência fica registrada para o caso de o passo 5.2 mostrar que o limite era da métrica, e não do fenômeno — situação em que o conjunto voltaria a ter uso e a validação passaria a ser exigível.

Registre-se ainda uma ressalva de construto identificada durante a formulação: *tu* com verbo não flexionado ocorre também no Rio de Janeiro, que integra o grupo de controle. O item não serve para separar os grupos deste desenho, ainda que a construção seja legítima.

---

## 5-A. Padrão recorrente: falha silenciosa

Cinco defeitos distintos identificados em 27/08/2026 pertencem à mesma classe — o programa prossegue e relata sucesso em situação de erro:

1. URL de canal aceita onde se esperava vídeo, produzindo registro com identificador de canal e duração vazia.
2. Download dado por bem-sucedido sem arquivo em disco, por efeito de `ignoreerrors`.
3. Caminho de dados relativo ao diretório de trabalho, criando pasta paralela vazia.
4. Metadados sobrescritos entre lotes, deixando áudio sem procedência regional.
5. Detecção de marcadores por expressão regular contabilizando "que não" como negação pós-verbal.

Nenhum emitiu erro. Todos foram descobertos por conferência posterior, e três deles apenas porque a coleta foi efetivamente executada — não por leitura do código.

**Encaminhamento.** A regra adotada é que toda etapa que produza artefato verifique o artefato, e não apenas o retorno da chamada. Aplicada em (1) a (4). Falta aplicá-la sistematicamente ao restante da esteira, e ao Filtro 2 em particular, cujo modo de falha inflaria a contagem de marcadores de modo desigual entre grupos — isto é, produziria resultado, e não erro.

**Três casos acrescentados em 28/08/2026**, todos da mesma classe, e nenhum deles emitindo erro:

6. Consulta de frequência sobre forma sem diacrítico, devolvendo o valor de outra palavra. Detalhamento em 6.5.
6-A. Campo `duracao_s` registrando a duração do vídeo de origem, e não a do áudio coletado, sem que nome ou documentação o declarassem. Somar o campo sobre os 52 registros devolvia 11,43 h contra 5,52 h reais. **Encerrado em 29/08/2026** pelo campo `duracao_coletada_s`, acrescentado ao registro de coleta e ao registro final e preenchido retroativamente com verificação de que nenhum outro campo se alterou. O campo antigo foi preservado com seu significado original, e não redefinido, porque os produtos de transcrição já gerados foram escritos sob a semântica antiga.
7. Piso da comparação calculado sobre medições individuais enquanto as medianas passaram a ser calculadas sobre medianas de par, o que fazia a condição de controle neutro aparecer como 1,25× de si mesma. Numerador e denominador precisam compartilhar a unidade de replicação.
8. Script de medição gravando a tabela no mesmo caminho do relatório interpretado escrito à mão. Reexecutar o script apagaria a interpretação sem aviso — inclusive as correções nela registradas. Corrigido pela separação entre `*_tabelas.md`, regerável, e o relatório, que o script não toca.

O sétimo caso merece nota: não era defeito de programa, e sim de **coerência entre a estatística e a unidade de replicação**. Pertence à mesma classe porque produz número plausível em vez de erro, e porque só apareceu na conferência de uma tabela contra a anterior.

## 6. Melhorias identificadas

### 6.0 O casador de municípios confunde sobrenome com cidade

Constatado em 31/08/2026, na rodada de vox-pop: o canal *Memória IBGE* foi aprovado na triagem automática com a evidência "Santos", que não vinha da cidade de Santos — vinha do sobrenome de um entrevistado, *Geraldo dos Santos*. O canal é de história oral do IBGE, com depoentes de MS, RN e PA, e nada tem de paulista.

O mecanismo de `AMBIGUOS` em `verificar_fontes.py` trata a ambiguidade **entre estados** (Penha existe em SP e no RJ), mas não a colisão entre topônimo e palavra comum ou sobrenome. São vulneráveis pelo menos *Santos*, *Franca*, *Lapa*, *Areia* e *Campo Grande*.

Não produziu erro no conjunto, porque a revisão humana pegou. Mas é falha silenciosa no sentido da seção 5-A: a triagem entrega um veredito ACEITO com evidência que parece sólida.

**Encerra a pendência:** exigir, para esse subconjunto de nomes, um segundo marcador no mesmo acervo — a sigla do estado ou outro município — do mesmo modo como já se faz com os ambíguos entre estados.

### 6.1 Gazeteiro parcial em `verificar_fontes.py`

A lista de municípios e bairros é deliberadamente incompleta e foi ampliada uma vez, quando se constatou que criadores urbanos nomeiam bairro e não município — ampliação que fez o mesmo tipo de busca render 212 candidatos onde antes rendia 36. Continua parcial, sobretudo para o interior.

### 6.2 Falante migrante não tem sinal automático

Os dois casos identificados denunciaram-se pelo nome do canal, o que é acidente favorável. Não há sinal textual confiável para o caso geral. A defesa efetiva é a checagem de coerência dialetal na curadoria das transcrições, que opera sobre a fala e não sobre metadados — **e não está implementada**.

**Investigado em 31/08/2026: as duas vias automáticas óbvias não funcionam, e por motivos já documentados no projeto.** Densidade de marcadores lexicais regionais é sinal fraco demais — o item 2.4 de `docs/achados_para_o_artigo.md` mediu zero ocorrências desses itens em 30 mil palavras de fala nordestina genuína, então um detector assim marcaria quase todo falante verdadeiro como suspeito. Densidade de contextos de palatalização mede apenas contexto ortográfico, não realização fonética, e os mesmos contextos existem em qualquer fala do português — não separa quem palataliza de quem não palataliza sem análise acústica do áudio, que o projeto não tem.

**Encaminhamento adotado: protocolo de curadoria manual, operacionalizado em vez de deixado como frase.** `pipeline_coleta_piloto/preparar_amostra_coerencia.py` amostra locutores por estado (10 de 20, dimensionado para poder de detecção adequado a um primeiro descarte) e recorta o segmento mais longo de cada um, gerando uma planilha para veredito humano — coerente, suspeito ou inconclusivo. Não decide nada sozinho; prepara o material para quem vai ouvir. Requer ambiente com áudio; não foi executado.

**Atualização de 15/09/2026: amostra gerada**, item 6 do plano de fechamento, na máquina local: 10 pessoas por estado, 60 ao todo, entre 27 e 38 elegíveis por estado. O script foi revisto antes da execução para ler os registros anonimizados — a pasta de originais tem 31 dos 83 arquivos localmente — e para sortear pessoas em vez de rótulos de diarização, com a fusão confirmada na conferência de reincidência (6.4). Planilhas em `dataset_raw/diarizacao/coerencia_{UF}.json`, fora do versionamento. Resta a escuta, item 10 do plano, que encerra a condição C5.

### 6.3 Precisão da triagem automática

Cerca de 41% dos canais aprovados automaticamente sobrevivem à revisão humana. Os três sinais de risco acrescentados após a primeira rodada — itinerante, narração sintética, canal sem fala — melhoram a taxa, mas a revisão humana permanece indispensável, inclusive porque o filtro produz falso positivo em sentido inverso, como no canal de Belford Roxo cujos títulos descrevem deslocamento diário com a palavra "viajando".

### 6.4 Sem verificação de reincidência de falante entre canais — CONDIÇÃO SATISFEITA EM 14/09/2026

> **Encerrada.** A verificação foi implementada, corrigida, executada duas vezes e conferida por escuta humana: 15 vereditos, 7 fusões confirmadas, 207 falantes distintos em 77 arquivos. O teto de 5% — a regra de que a pendência deriva — está satisfeito nos seis estados pelo critério adotado em 12/09/2026. Detalhamento em `docs/plano_corpus/01-verificar-falantes.md`, seções 7.1 e 7.2.
>
> **Duas ressalvas sobrevivem à conclusão.** Primeira: PB e RJ atingem o piso exatamente, sem margem, de modo que a exclusão de um único falante na etapa 3 reabre a coleta — encaminhamento sugerido em `docs/plano_corpus/02-completar-coleta.md`. Segunda: 22 rótulos ficaram sem embedding, por terem menos de 8 s de fala; não são falantes verificados nem descartados, e o número limita o que se pode afirmar.
>
> O texto abaixo é o registro histórico da pendência, preservado.

**Deixa de ser melhoria desejável em 29/08/2026, e passa a condição para declarar o corpus completo.** A decisão de tratar o corpus como entregável autônomo mudou a meta de horas para cobertura de falantes, e a meta inteira deriva do teto de 5% por falante. Sem verificar que os locutores são pessoas distintas, não é possível afirmar que o teto é respeitado — e os 211 rótulos de locutor do corpus atual são limite superior, possivelmente muito acima do número real de pessoas, já que repórteres e apresentadores reaparecem entre arquivos do mesmo canal.

Detalhamento em `experimentos/resultados/tabelas/meta_corpus_autonomo.md`, seção final.

Nada impede que a mesma pessoa apareça em canais distintos — convidado que circula por vários podcasts regionais, por exemplo. Isso violaria silenciosamente o teto de 5% por falante estabelecido em `docs/fontes_coleta.md`, seção 2.4.5. A detecção exigiria comparação de vozes na etapa de diarização.

**Método proposto e implementado em 31/08/2026, execução pendente.** `pipeline_coleta_piloto/verificar_reincidencia.py` compara *embeddings* de locutor (via `pyannote/embedding`, mesma dependência já usada na diarização) entre todos os arquivos de um estado, sinalizando pares acima de um limiar de similaridade para revisão humana — não decide sozinho, só reduz o volume a conferir. Requer ambiente com `pyannote.audio` e o áudio bruto, isto é, o ambiente de processamento (Colab), não esta máquina; não foi executado.

**Ferramenta preparada para execução em 02/09/2026, sob a etapa 1 de `docs/plano_corpus/`.** Três defeitos foram corrigidos antes de a primeira execução ocorrer, dois deles capazes de falhar em silêncio:

1. O script lia de `registros_finais/`, que está vazia, e teria comparado zero arquivos relatando zero pares. Ganhou o parâmetro `--registros`, e interrompe com mensagem explícita quando a pasta não tem registro algum.
2. O embedding era extraído do turno mais longo do rótulo, embora a admissão do rótulo se desse pela **soma** dos turnos. Dos 154 rótulos que alcançam 8 s de fala, 16 só os alcançam somando, e neles o embedding sairia de menos áudio do que o critério exige. O script passa a concatenar os turnos escolhidos. O viés era direcionado: fala fragmentada é a do entrevistado de rua, não a do repórter.
3. A saída trazia apenas os pares já acima do limiar, o que impediria calibrá-lo sem repetir a passagem de GPU — que é justamente o que a etapa 1 prevê fazer. Passa a registrar os pares a partir de 0,50, marcados quanto ao limiar, com os tempos dos trechos e os canais de cada lado.

O notebook `notebooks/verificar_falantes_colab.ipynb` executa a comparação e instrumenta a conferência humana, tocando os dois trechos de cada par.

**Comparação executada em 02/09/2026; conferência pendente.** Oito pares acima de 0,50 em todo o corpus — seis em PB, um em PE, um em CE, nenhum em BA, SP e RJ —, com distribuição bimodal: nenhum par entre 0,55 e 0,75, o que torna a escolha do limiar indiferente para o resultado. Detalhamento em `docs/plano_corpus/01-verificar-falantes.md`, seções 5.1 e 5.2.

**Ressalva que a comparação não resolve.** A ausência de pares em BA, SP e RJ não se deve ao limiar, mas pode dever-se ao outro modo de falha do método: a mesma voz, em condições de gravação distintas, cair abaixo de 0,50. RJ é o caso mais exposto, com três canais de mais de um arquivo e nenhum par. Encerraria a ressalva ouvir, em cada canal com mais de um arquivo, o rótulo de maior fala de um arquivo contra o do outro. São cinco comparações nesses três estados e **dezenove no corpus inteiro**, listadas e tocadas pela seção 7.2 do notebook: PB 5, CE 5, PE 4, RJ 3, BA 1 e SP 1. A extensão aos seis estados não é zelo excessivo — o rótulo de maior fala de cada arquivo nem sempre é o que a comparação automática pareou, de modo que também em PB, PE e CE há pares de mesmo canal ainda não conferidos. **PB era o caso decisivo**, por estar exatamente no piso: uma única fusão confirmada ali o derrubaria. **Conferido em 12/09/2026: os cinco pares de PB são pessoas distintas, e nada mudou** — as fusões continuam seis, PB segue com 20 pessoas úteis e o déficit com 27 pessoas. Restam catorze pares (PE 4, CE 5, RJ 3, BA 1, SP 1), que não alteram a conclusão de estado algum e apenas aumentariam em uma pessoa, cada um, o déficit já existente.

**Conferência humana concluída em 10/09/2026, e o piso está atingido.** Oito pares conferidos, seis fusões — quatro em PB, uma em PE, uma em CE. Falantes distintos: PB 26, PE 27, CE 22, BA 22, SP 21, RJ 30, todos acima do piso de 20. A pergunta desta seção — quantas pessoas distintas há — está respondida, ressalvada a checagem dos canais repetidos descrita acima.

**Pendência nova, aberta na mesma data: o teto de 5% por falante, de que o piso deriva, não é satisfeito pelo material tal como coletado.** Ter 20 pessoas é condição necessária para o teto, e não suficiente: ele depende também de como a fala se distribui entre elas, e em telejornal e podcast apresentador e repórter falam muito mais que o entrevistado. Medido sem as fusões — que só agravariam o quadro —, entre 5 e 9 rótulos por estado excedem 5% da fala do estado, o maior chegando a 20,5% em BA, e esses rótulos concentram de 46,6% a 71,5% da fala. Aplicar o teto por recorte reduz as 4,6 h de fala a 1,8 h, e SP a 6,6 minutos, com no máximo 0,3 minuto por pessoa — abaixo do segundo piso de 0,7 minuto de fala por falante fixado em `experimentos/resultados/tabelas/meta_corpus_autonomo.md`. Medição reproduzível por `pipeline_coleta_piloto/verificar_teto_falante.py`; detalhamento em `docs/plano_corpus/01-verificar-falantes.md`, seção 7.1.

**Decidido em 10/09/2026: o teto é condição de conclusão.** O critério da etapa 1 passa a ser 20 pessoas por estado que conservem o segundo piso de fala depois do recorte pelo teto. A coleta não está concluída, e a etapa 2 torna-se necessária: **faltam 27 pessoas novas** — PE 3, CE 5, BA 5, SP 8, RJ 6, PB nenhuma —, apurado em 12/09/2026 com as seis fusões da conferência aplicadas (`verificar_teto_falante.py --vereditos`). PB ficou exatamente no piso, com 20 pessoas úteis e margem nula. Detalhamento em `docs/plano_corpus/02-completar-coleta.md`.

**Pendência aberta em 10/09/2026 e decidida em 12/09/2026: o teto permanece em 5%, agora como convenção declarada do projeto**, a ser apresentada como tal no artigo e na ficha do conjunto, acompanhada da tabela de sensibilidade abaixo. A origem de registro passa a ser `docs/dataset-spec.md` §1.4.5, e não mais a remissão falsa a `docs/fontes_coleta.md` §2.4.5. O registro do problema fica abaixo, porque a decisão só se sustenta declarada junto com ele.

**O problema que a decisão resolve por declaração, e não por fundamentação: o valor de 5% não tinha fundamento documentado.** O projeto justifica a existência de um teto — sem ele, uma pessoa loquaz responderia pela maior parte da fala de um estado, e o corpus representaria um idioleto (decisão de 31/08/2026, abaixo) —, mas não o seu valor. A origem citada em `docs/dataset-spec.md` §1.4.5, na etapa 1 do plano do corpus e em `meta_corpus_autonomo.md` é `docs/fontes_coleta.md` §2.4.5, que não contém o teto: trata do rendimento da camada de vlogs. A frase que o enuncia, noutra seção do mesmo documento, entrou na revisão v1.7 remetendo a esse item. **Por que importa:** o piso de pessoas é o inverso do teto — 20 a 5%, 10 a 10%, 34 a 3% —, e o déficit da etapa 2 muda com ele. **O que encerraria:** fundamentar o valor em literatura de construção de corpus de fala, ou declará-lo como convenção do projeto, com a sensibilidade do déficit ao valor reportada ao lado; e, em qualquer caso, corrigir a remissão a §2.4.5.

**Sensibilidade do déficit ao valor** (`verificar_teto_falante.py --teto --vereditos`, com as fusões, em 12/09/2026): a 10%, o piso cai a 10 pessoas úteis e **nenhum estado tem déficit**; a 5%, faltam 27 pessoas; a 3%, o piso sobe a 34 e faltam 111. O valor decide, portanto, entre coleta concluída, coleta moderada e coleta mais de quatro vezes maior que esta — e precisa ser fechado **antes** da etapa 2, e não depois dela, pela decisão registrada em `CLAUDE.md` de fechar a camada de definição do dataset antes de qualquer execução de coleta.


### 6.5 Consulta de frequência sensível a diacrítico

A fonte de frequência lexical trata forma acentuada e não acentuada como palavras distintas, e devolve valor para ambas sem sinalizar a diferença. Em 28/08/2026 constatou-se que a frequência atribuída a *moço* no relatório de sensibilidade — 0,158 por milhão — fora obtida sobre *moco*; o valor correto é 4,90, cerca de trinta vezes maior. A consulta não falha: devolve o número de outra palavra.

Pertence à classe descrita na seção 5-A. O encaminhamento é o mesmo: toda consulta de frequência deve partir da forma tal como ocorre no enunciado medido, e não de transcrição manual do item, e valores destinados ao artigo devem ser regerados por código a partir dos próprios enunciados. Implementado em `experimentos/teste_construcional.py`, cuja função `razao_frequencia` extrai as palavras diretamente dos dois lados do par. Falta reconferir os valores do adendo B de `experimentos/resultados/relatorios/piloto_medicoes.md`, que foram digitados a partir de consulta avulsa.

---

## 7. Encerradas

| Data | Pendência | Como foi encerrada |
|---|---|---|
| 27/08/2026 | Atlas dialetológicos de CE e BA, aberta na v1.1 | ALECE (Bessa, 2010) e Atlas Prévio dos Falares Baianos (Rossi, 1963) |
| 27/08/2026 | Referência completa de Oliveira (2017) | Localizada; leitura do capítulo segue pendente (3.1) |
| 27/08/2026 | Leitura integral de Melo e Souza (2026) | Realizada; metodologia e resultados registrados na fundamentação, seção 1.3.4 |
| 27/08/2026 | Ausência de lista de fontes de coleta | 88 canais verificados, com regra de atribuição documentada |
| 27/08/2026 | Ausência de meta de volume | Derivada do requisito estatístico do Filtro 2 |
| 27/08/2026 | SP e RJ sem vlogs atribuíveis | De 1 e 2 para 11 e 9 canais verificados |
| 27/08/2026 | Etapa entre lista de canais e coleta | `selecionar_videos.py` |
| 27/08/2026 | Falha silenciosa com URL de canal no `collect.py` | Verificação de forma da URL antes de qualquer chamada de rede |
