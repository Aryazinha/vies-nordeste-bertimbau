# Pendências e Melhorias

**Função deste arquivo.** Registro único do que está aberto no projeto: lacunas conhecidas, decisões não tomadas, melhorias identificadas e verificações devidas. Existe porque o conhecimento acumulado durante uma sessão de trabalho não sobrevive a ela; o que não estiver aqui será redescoberto do zero ou simplesmente perdido — como ocorreu com o rascunho de pares mínimos da revisão v1.3, refeito integralmente meses depois.

**Como usar.** Consultar no início de cada retomada, antes de planejar trabalho novo. Todo item traz o motivo pelo qual importa e o que o encerraria, de modo que possa ser retomado sem o contexto da conversa em que surgiu. Itens resolvidos são marcados como tal, com a data, e não removidos — a lista serve também de histórico do que já foi enfrentado.

**Última revisão:** 27/08/2026

---

## Prioridade

A ordenação abaixo reflete o critério do `docs/roadmap.md`: aproxima-se primeiro o projeto de ter dados montados e validados.

| # | Pendência | Bloqueia | Seção |
|---|---|---|---|
| 1 | Assimetria de tipo de fonte entre grupos (rádio de participação) | corpus final | 1.1 |
| 2 | Conferência dos percentuais de Oliveira (2017) | item C1 do instrumento | 3.1 |
| 3 | Correção do instrumento de texto (molduras e atributos) | validação por juízes | 2.1, 2.2 |
| 4 | Ambiente com GPU para o piloto de medição | piloto | 4.1 |
| 5 | Decisão de simetria entre grupos | coleta final | 5.1 |

---

## 1. Fontes de coleta

### 1.1 Rádio com participação de ouvinte existe em apenas dois estados

Programas em que o ouvinte liga — "Alô Juca" na TV Aratu (BA) e "Super Manhã" na Rádio Jornal (PE) — reúnem as três propriedades desejáveis simultaneamente: falante morador do estado, fala espontânea e áudio limpo. É a melhor fonte identificada em todo o levantamento.

O problema é que só PE e BA dispõem dela. Não se trata de diferença de quantidade, e sim de **tipo de fala**: se o material nordestino contiver fala não monitorada de gente comum e o material do grupo de controle contiver jornalismo de estúdio, a diferença observada entre os grupos passará a incluir registro e situação comunicativa, e não apenas procedência regional. O confundidor incide diretamente sobre a variável de interesse.

**Encerra a pendência:** localizar programas equivalentes em PB, CE, SP e RJ; ou, não sendo possível, retirar os dois existentes e uniformizar por baixo.

### 1.2 Camada de vox-pop com apenas dois canais em quatro estados

PB, BA, SP e RJ têm dois canais nessa camada, que responde por 4,1 h das 8,3 h previstas por estado — metade do corpus. A concentração cria dependência: mudança de linha editorial ou remoção de acervo em um canal compromete metade da amostra do estado.

**Encerra a pendência:** elevar a quatro canais por estado nessa camada.

### 1.3 Interior da Bahia descoberto, e o canal existente fica em zona de fronteira

Apenas 3 dos 10 canais baianos têm marca de interior, no maior dos estados-alvo. Agrava-se pelo fato de o vlog de interior disponível, `Jairo DroneX`, ser de **Juazeiro-BA**, conurbada com Petrolina-PE. Coletar variedade baiana em conurbação com Pernambuco, num estudo que compara precisamente BA e PE, é escolher o pior ponto possível da malha.

**Encerra a pendência:** cobrir Feira de Santana, Vitória da Conquista, Itabuna ou Barreiras, distantes da divisa.

### 1.4 Onze canais em situação `a_confirmar`

Aceitos com ressalva, pendentes de inspeção de conteúdo. `selecionar_videos.py` os exclui do planejamento, de modo que hoje não contribuem em nada. Distribuição: RJ 4, BA 2, SP 2, PB 1, PE 1, CE 1.

**Encerra a pendência:** abrir cada um e verificar três coisas — se há fala humana em volume razoável, se o falante reside no estado, e se não é conteúdo comercial ou institucional disfarçado de vlog.

### 1.5 Vlogs de Pernambuco são os mais escassos

Três canais verificados, contra oito no Ceará e onze em São Paulo. Coincide, sem relação causal, com o fato de Pernambuco ser também o único estado-alvo sem marcador morfossintático próprio no instrumento de texto (seção 2.4). Se as duas fragilidades persistirem, convém declarar PE como caso de cobertura reduzida em vez de forçar paridade artificial.

### 1.6 Rota de coleta por RSS não implementada

A seção 2.3.2 de `docs/fontes_coleta.md` estabelece que podcast distribuído por feed aberto é a fonte de situação jurídica mais clara disponível ao projeto, superior nesse aspecto ao próprio YouTube. O `collect.py`, no entanto, só opera sobre URLs do YouTube. Nenhum feed RSS foi levantado.

**Encerra a pendência:** levantar feeds de podcasts regionais por estado e estender o `collect.py`, que já pode usar o extrator genérico do `yt-dlp`.

---

## 2. Instrumento de texto

### 2.1 Molduras inoperantes ainda não substituídas no documento

O teste de fumaça (passo 1) mostrou que duas das cinco molduras não funcionam: `Quem falou isso é [MASK]` colapsa em pronomes (*você* 0,385; *ele* 0,294) e `estudou até o [MASK]` colapsa em expressão idiomática (*fim* 0,386). As substitutas foram testadas e aprovadas — `completou o ensino [MASK]` concentra 97% da massa em *médio* e *fundamental*; `parece uma pessoa [MASK]` elimina o vazamento de subtoken — e constam de `experimentos/resultados/molduras_alternativas.md`, mas **não foram incorporadas** a `docs/pares_minimos_v1.md`.

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

---

## 4-A. Achados do piloto de 27/08/2026

Medições completas em `experimentos/resultados/piloto_medicoes.md`.

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

### 5.1 Simetria entre os grupos

O grupo de controle tem 9 a 11 vlogs verificados por estado; Pernambuco tem 3. Como um canal de vlog corresponde na prática a um falante, a composição dos grupos difere. Duas condutas: limitar todos os estados ao patamar do mais fraco, ou reforçar PE e BA antes de coletar. `selecionar_videos.py --max-canais N` já implementa a primeira.

**Recomendação registrada:** decidir depois do piloto, com o rendimento real medido, em vez de agora por estimativa.

### 5.2 Composição entre camadas

As proporções da seção 1.4.3 do `CLAUDE.md` — 60% a 70% para a camada âncora, 30% a 40% para a espontânea — foram fixadas antes de se conhecer o rendimento de cada fonte. O levantamento sugere deslocar volume do vlog, de baixa diversidade por hora, para rádio de participação. Alterar exige revisão formal do protocolo.

### 5.3 CLAUDE.md fora do versionamento

O arquivo permanece local por decisão registrada em agosto. Como os demais documentos remetem a suas seções — protocolo em 1.4, ameaças à validade na Parte 3 —, quem acessar o repositório encontrará dezenas de referências a um arquivo ausente. Afeta a reprodutibilidade se o material acompanhar uma submissão. Duas saídas: versionar o arquivo, ou transferir as partes públicas para um `docs/protocolo.md` versionado.

### 5.4 Subcorpus de TikTok

Excluído do corpus principal por dissociação entre origem do vídeo e origem da voz (seção 2.3.1 de `docs/fontes_coleta.md`). Admite-se reabertura, sob quatro critérios cumulativos, caso a diversidade de falantes não se complete pelas fontes adotadas. Não reavaliado desde então.

---

## 6. Melhorias identificadas

### 6.1 Gazeteiro parcial em `verificar_fontes.py`

A lista de municípios e bairros é deliberadamente incompleta e foi ampliada uma vez, quando se constatou que criadores urbanos nomeiam bairro e não município — ampliação que fez o mesmo tipo de busca render 212 candidatos onde antes rendia 36. Continua parcial, sobretudo para o interior.

### 6.2 Falante migrante não tem sinal automático

Os dois casos identificados denunciaram-se pelo nome do canal, o que é acidente favorável. Não há sinal textual confiável para o caso geral. A defesa efetiva é a checagem de coerência dialetal na curadoria das transcrições, que opera sobre a fala e não sobre metadados — **e não está implementada**.

### 6.3 Precisão da triagem automática

Cerca de 41% dos canais aprovados automaticamente sobrevivem à revisão humana. Os três sinais de risco acrescentados após a primeira rodada — itinerante, narração sintética, canal sem fala — melhoram a taxa, mas a revisão humana permanece indispensável, inclusive porque o filtro produz falso positivo em sentido inverso, como no canal de Belford Roxo cujos títulos descrevem deslocamento diário com a palavra "viajando".

### 6.4 Sem verificação de reincidência de falante entre canais

Nada impede que a mesma pessoa apareça em canais distintos — convidado que circula por vários podcasts regionais, por exemplo. Isso violaria silenciosamente o teto de 5% por falante estabelecido em `docs/fontes_coleta.md`, seção 2.4.5. A detecção exigiria comparação de vozes na etapa de diarização.

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
