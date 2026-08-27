# Fontes de Coleta do Corpus de Áudio

**Passo 4.1 do roadmap.** Lista semente de canais, por estado e por camada, para alimentar `pipeline_coleta_piloto/`. A versão consumível pelo código está em `pipeline_coleta_piloto/fontes.json`.

**Levantada em:** 27/08/2026. Todos os identificadores de canal foram obtidos por consulta ao YouTube via `yt-dlp`, e não por conhecimento prévio ou memória — cada canal listado existia e estava ativo na data.

---

## 1. Regra de atribuição

O campo `estado_alvo` do esquema da seção 1.4.1 do `CLAUDE.md` é atribuído **pelo canal, nunca pela consulta de busca nem pelo título do vídeo.** Um canal só entra na lista se satisfizer um destes critérios:

- **Vínculo institucional com o estado.** Emissora, rádio, jornal ou órgão público sediado no estado. A atribuição é verificável e estável.
- **Evidência geográfica recorrente no próprio conteúdo.** Para criadores independentes, exige-se menção repetida a municípios identificáveis do estado nos títulos ou descrições recentes.

Canais que não satisfaçam nenhum dos dois são rejeitados, ainda que o conteúdo pareça adequado.

### 1.1 Por que a regra é necessária

A primeira rodada de levantamento buscou por formulações de conteúdo — por exemplo, "moradores reclamam entrevista rua Recife bairro". O resultado demonstrou que o método é inseguro: a fórmula jornalística "moradores reclamam da rua" é idêntica em todo o país, de modo que a consulta de Pernambuco retornou TV Gaspar (Santa Catarina) e TVG Várzea Grande (Mato Grosso); a da Bahia retornou Balanço Geral MG; a de São Paulo retornou SBT MS; a do Ceará retornou Balanço Geral Joinville.

O mesmo vale para vlogs rurais. O canal "Adailton no sertão" apareceu simultaneamente entre os resultados de Paraíba, Pernambuco e Ceará, e seus títulos recentes mencionam apenas "sertão" e "caatinga", sem município identificável — não é atribuível a estado algum.

Rotular `estado_alvo` a partir da consulta introduziria erro de medida exatamente na variável independente do estudo. Um vídeo catarinense rotulado como pernambucano não é ruído aleatório: é contaminação sistemática do contraste que o projeto pretende medir.

### 1.2 Verificação executada

Para cada criador independente candidato, foram extraídos os títulos dos quatro vídeos mais recentes:

| Canal | Evidência | Decisão |
|---|---|---|
| RAÍZES DO REI | "Feira de Pacujá-CE"; "sertão do Ceará" | Aceito — CE |
| COISAS DA PARAÍBA OFICIAL | "Campina Grande-PB"; "Puxinanã" | Aceito — PB, interior |
| Vida no Interior da Bahia | Serrolândia, Conceição do Coité, Jacobina | Aceito — BA, interior |
| ESTRELA ALVES | "Comunidade Sanharó", município do agreste de PE | Aceito com ressalva — PE, confirmar |
| Adailton no sertão | apenas "sertão", "caatinga" | Rejeitado — não atribuível |
| Vlog Maedetrás | nenhum marcador geográfico | Rejeitado — não atribuível |
| Ruth e Família | nenhum marcador geográfico | Rejeitado — não atribuível |

---

## 2. Duas ressalvas que afetam o desenho

### 2.1 A camada âncora tende a capturar a fala mais padronizada

A seção 1.4.3 do `CLAUDE.md` justifica a camada âncora pela qualidade do áudio — menor WER e DER esperados. O levantamento mostra que essa camada carrega um custo não previsto: apresentadores de telejornal e repórteres empregam uma variedade de radiodifusão deliberadamente neutralizada, e boa parte do conteúdo institucional recuperado consiste em sabatinas com políticos, cuja fala pública é profissionalmente treinada. São exatamente os falantes em que os marcadores dialetais estão mais suprimidos.

Segue-se uma qualificação da camada âncora: **o que interessa nela não é o jornalismo de estúdio, e sim os segmentos em que fala gente comum.** Duas subclasses concentram esse valor:

- **Rádio com participação do ouvinte.** Programas como "Alô Juca" (TV Aratu) e "Super Manhã" (Rádio Jornal) reúnem as três propriedades desejáveis ao mesmo tempo: quem fala é morador do estado, a fala é espontânea e o áudio é limpo. É a melhor fonte identificada no levantamento.
- **Vox-pop de reportagem local.** O entrevistado é morador; o repórter frequentemente não é. A diarização não é acessório aqui, é o que separa as duas coisas — e é o que sustenta o rendimento de 35% suposto no cálculo do passo 4.2.

### 2.2 Canais de arquivo não oficiais estão excluídos

O levantamento recuperou canais como "Muito Além do JPB" e "Muito Além do CETV", que republicam material de emissoras. O conteúdo seria adequado, mas a redistribuição por terceiros agrava a exposição de direitos autorais que a seção 1.4.2 do `CLAUDE.md` procura evitar. Sempre que houver canal oficial da emissora, é ele que entra.

---

## 2.3 Plataformas consideradas e decisão de escopo

Avaliadas em 27/08/2026, com verificação do suporte real das ferramentas de coleta.

| Plataforma | Decisão | Fundamento |
|---|---|---|
| YouTube | **Adotada** | Coleta sistemática funcional; conteúdo arquivístico estável; identificadores publicáveis, o que preserva a reprodutibilidade sem redistribuição de áudio |
| Podcast por feed aberto (RSS, Apple Podcasts) | **Adotada** | Ver 2.3.2 |
| Spotify | **Excluída** | Áudio protegido e download vedado pelos termos de uso. O `yt-dlp` não dispõe de nenhum extrator para a plataforma |
| TikTok | **Excluída do corpus principal** | Ver 2.3.1 |
| Instagram | **Excluída do corpus principal** | Mesmos motivos do TikTok, agravados pela exigência de autenticação e pelo extrator `instagram:user` inoperante, o que impede coleta sistemática e compromete a reprodutibilidade |

### 2.3.1 Fundamento da exclusão de TikTok e Instagram

O motivo determinante é a **dissociação entre origem do vídeo e origem da voz**. O reaproveitamento de áudio de terceiros é mecanismo central dessas plataformas: um vídeo publicado por perfil sediado no estado-alvo pode veicular áudio gravado por falante de outra região. Diferentemente da contaminação por consulta de busca descrita no item 1.1, esta não é detectável por inspeção do perfil ou do conteúdo visual. Para um corpus cuja variável independente é a procedência da fala, o defeito é incontornável em escala.

Três fatores adicionais, não determinantes mas onerosos: a alta incidência de encenação de sotaque, com finalidade humorística, que é precisamente a caricatura que a validade de construto exige excluir; a sobreposição de música à fala, prática padrão nessas plataformas, que degrada transcrição e diarização; e a duração típica de 15 a 60 segundos, que eleva o custo de curadoria por hora de fala aproveitável a um patamar incompatível com a meta do passo 4.2.

Registre-se ainda a limitação instrumental: os extratores `tiktok:tag` e `tiktok:sound` — as vias de coleta sistemática — encontram-se inoperantes.

**Reabertura condicionada.** Caso a diversidade de falantes não se complete pelas fontes adotadas, admite-se subcorpus secundário, declarado à parte, sob quatro critérios cumulativos: áudio original do próprio autor; ausência de música de fundo; procedência declarada pelo falante ou verificável no perfil; e ao menos 60 segundos de fala contínua. O subcorpus deve ser aplicado simetricamente aos dois grupos regionais, sob pena de a diferença observada refletir a plataforma e não a região.

### 2.3.2 Fundamento da adoção do podcast por feed aberto

Podcast distribuído por RSS é publicado com a finalidade explícita de ser baixado. A coleta por essa via não incorre na zona cinzenta de termos de uso que motiva a cautela da seção 1.4.2 do `CLAUDE.md`, e constitui **a fonte de situação jurídica mais clara disponível ao projeto**, superior nesse aspecto ao próprio YouTube. O `yt-dlp` dispõe do extrator `ApplePodcasts` e do extrator genérico, que resolve feeds RSS e arquivos diretos.

Não há alteração no esquema de dados: a camada `podcast_radio_tv_regional` já contempla essas fontes. Altera-se apenas a rota de download.

Duas ressalvas de conteúdo. A diversidade de falantes por hora é baixa, tipicamente dois por episódio, de modo que a camada serve como base de áudio limpo e não como solução para o problema de diversidade. E o apresentador costuma ser profissional de mídia, com fala mais padronizada que a do convidado — em entrevistas, o turno do convidado tende a ter maior valor dialetal, o que reforça a necessidade da diarização.

---

## 2.4 Ampliação da camada de vlogs e os limites da triagem automática

Executada em 27/08/2026 para corrigir a deficiência de diversidade de falantes descrita no item 4: a camada `vlog_amador` contava com um único canal por estado nordestino e nenhum nos estados de controle. Como um canal de vlog corresponde, na prática, a um falante, mais de um terço do volume previsto para a camada espontânea repousava sobre uma única pessoa por estado.

Foram levantados 101 canais candidatos por consultas nomeando municípios de cada estado. O resultado quantifica a precisão da triagem automatizada:

| Etapa | Canais |
|---|---|
| Candidatos levantados | 101 |
| Aprovados pela triagem automática (`verificar_fontes.py`) | 34 |
| Sobreviventes à revisão humana | 13 |

**A precisão da triagem automática foi de aproximadamente 38%.** A causa é precisa: a regra verificava *geografia*, e geografia não implica residência, nem fala humana, nem fala alguma. Três classes de canal passavam pela verificação sem satisfazer o propósito da coleta.

### 2.4.1 Canais itinerantes

Canais de viagem, motovlog, caminhoneiro e entusiasta de transporte percorrem o estado e o citam abundantemente — e, no critério original, a menção a *muitos* municípios era o sinal mais forte de pertencimento, quando é justamente a assinatura de quem está de passagem. O caso exemplar é um canal aprovado por citar João Pessoa, Campina Grande, Guarabira e Sapé, cujo conteúdo consiste em trajetos rodoviários que atravessam também Rio Grande do Norte e Pernambuco. Nada garante a procedência do locutor, e a fala registrada pode ser de qualquer estado do trajeto.

### 2.4.2 Narração possivelmente sintética

Canais de formato enumerativo — "as 15 piores cidades de Pernambuco", "o código secreto de Pernambuco", "a história proibida do frevo" — citam o estado a cada título e são frequentemente narrados por voz sintética. Trata-se de risco de natureza distinta dos demais: introduziria **fala não humana** num corpus cuja finalidade é documentar variação dialetal humana. Nenhum áudio sintético pode entrar no corpus, e a suspeita basta para excluir.

### 2.4.3 Canais sem fala

Canais de passeio em vídeo — rotulados `walk`, `4K`, `POV` — e montagens com drone percorrem bairros identificáveis e satisfazem plenamente o critério geográfico, mas costumam não conter fala, ou conter apenas música. São inúteis para um corpus de fala, ainda que perfeitamente atribuíveis a um estado.

### 2.4.4 Tratamento adotado

`verificar_fontes.py` passou a computar a incidência dessas três classes de sinal nos títulos recentes. Quando a incidência atinge um terço dos títulos examinados, o veredito é rebaixado de aceito para **revisar**, e não para rejeitado — deliberadamente. O motivo é que o sinal também produz falso positivo: um canal de Belford Roxo cujos títulos dizem "viajando de carro em Belford Roxo, indo trabalhar" descreve deslocamento diário, não viagem, e é fonte legítima. Distinguir morador de viajante é julgamento que a heurística não substitui.

A triagem automática permanece, portanto, como redutora de esforço e como registro auditável da evidência — não como decisão final. Nenhum canal entra em `fontes.json` sem revisão humana.

### 2.4.5 Consequência para o desenho

A camada de vlogs revelou-se de baixo rendimento: cerca de oito candidatos levantados para cada canal aproveitável. Os estados de controle são os mais afetados, e São Paulo permanece com um único vlog — criadores urbanos raramente nomeiam o município, que é exatamente o critério de atribuição.

Recomenda-se, em consequência, **reconsiderar a composição entre camadas** fixada na seção 1.4.3 do `CLAUDE.md`. As proporções ali (60% a 70% para a camada âncora, 30% a 40% para a espontânea) foram estipuladas antes de se conhecer o rendimento real de cada fonte. O rádio com participação de ouvinte fornece, por hora coletada, muito mais falantes distintos que o vlog, com atribuição de estado mais segura, situação jurídica mais clara e áudio melhor. Deslocar volume da camada de vlogs para essa subclasse melhoraria simultaneamente diversidade, atribuição e qualidade — ao custo de alguma formalidade de registro, já que quem liga para um programa de rádio monitora a própria fala mais do que quem grava em casa.

A decisão é da equipe e deve ser registrada como revisão do protocolo, não adotada tacitamente.

---

## 2.5 O falante migrante: a armadilha de atribuição mais perigosa

Identificada em 27/08/2026, durante a ampliação da camada de vlogs para São Paulo e Rio de Janeiro. É qualitativamente distinta das três descritas em 2.4 e exige tratamento próprio.

**O problema.** Um canal pode estar corretamente ancorado no estado-alvo — o autor mora ali, filma as ruas de lá, cita bairros identificáveis, satisfaz integralmente a regra de atribuição do item 1 — e ainda assim veicular fala de outra variedade, porque **o autor migrou**. A localização do canal é verdadeira; a procedência da fala é outra.

Dois casos apareceram nomeando-se a si mesmos: um canal intitulado "Carioca em SP", cujo autor é carioca radicado em São Paulo, e outro intitulado "Viviane Baiana", de autora baiana radicada no Rio. Ambos foram aprovados pela triagem automática, com evidência geográfica correta.

**Por que é mais grave que as demais.** Um vídeo catarinense rotulado como pernambucano é erro grosseiro, detectável por inspeção. O falante migrante é erro fino: tudo confere, exceto a única propriedade que o estudo mede. E o vetor migratório dominante no Brasil é justamente Nordeste para Sudeste, que é o eixo desta pesquisa. Um falante nordestino radicado em São Paulo, incorporado ao grupo de controle, não introduz ruído aleatório: **atenua sistematicamente o contraste que a pesquisa pretende detectar**, deslocando o resultado na direção da hipótese nula. O erro produz, portanto, a aparência de ausência de viés.

O inverso também ocorre e é igualmente danoso: um paulista radicado em Recife incorporado ao grupo nordestino.

**Por que a automação não resolve.** Os dois casos encontrados se denunciaram pelo nome do canal, o que é acidente favorável. Não há sinal textual confiável para o caso geral: quem migrou não anuncia isso em cada título. Migração de longa data, ademais, produz repertório híbrido, e nesse caso não há resposta binária correta — a literatura sobre falares nordestinos migrantes no Sudeste documenta precisamente essa hibridização.

**Tratamento adotado.**

1. Nenhum canal cujo nome, descrição ou conteúdo indique migração entra no corpus, em qualquer dos dois grupos.
2. A verificação de fala, na etapa de curadoria manual das transcrições, passa a incluir uma checagem de coerência: se um falante do grupo de controle apresentar marcadores nordestinos, ou o inverso, o trecho é excluído e o canal reexaminado. Esta é a defesa efetiva, já que opera sobre a fala e não sobre metadados.
3. A limitação é declarada no artigo. Um corpus de fala pública coletado de plataformas não permite verificar a biografia linguística dos falantes, e nenhuma amostragem por procedência de canal elimina inteiramente o risco. É limitação de método, não defeito corrigível por esforço adicional de triagem.

---

## 3. Lista de fontes por estado

Gerada a partir de `pipeline_coleta_piloto/fontes.json`, que é a fonte de verdade. Situação `verificado` indica canal aprovado na triagem automática e confirmado em revisão humana; `a_confirmar` indica canal aceito com ressalva, pendente de inspeção de conteúdo.

### Paraíba (PB)

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| TH+ SBT TAMBAÚ | `UCdFKGMlvchusRx1u3mBUwrQ` | vox-pop | verificado | Programa Tambaú da Gente |
| TV ARAPUAN | `UCFWkgzJ360DGEJMU4XsQzSA` | vox-pop | verificado | Programa Cidade em Ação |
| CBN Paraíba | `UCOJfaGzIcQIPBaiRyCjLtyQ` | podcast/rádio/TV | verificado | CBN Cotidiano |
| Sistema 83 Podcast | `UCelNb6fi8eQQcB-74NokR0A` | podcast/rádio/TV | verificado | Entrevistas longas |
| TV Correio | `UCJ4uxK_mo6gNoqk9cyvgWkw` | podcast/rádio/TV | verificado | Emissora estadual; sabatinas e agenda política, registro formal |
| Canal Oxente Paraíba | `UCKCaPZH4rEZGIvDn3Mkv4ig` | vlog | verificado | Zona rural de Campina Grande e Lagoa Seca |
| Canal Reality do Casal | `UCpthj4pmjNspHRN6MLDK43A` | vlog | verificado | João Pessoa e Pombal; vlog familiar |
| COISAS DA PARAÍBA OFICIAL | `UCCRbfYz7GEMu4B3Hf-lgdYw` | vlog | verificado | Interior; Campina Grande e Puxinanã |
| Coisas de Cajazeiras | `UCq33E7-YdVXpRucBRVkNCdw` | vlog | verificado | Cajazeiras; cultura local e forró |
| Daniel Alves | `UCEiUJdzUOkOsj8SK6nscZBg` | vlog | a_confirmar | João Pessoa e Cabedelo; confirmar se não é conteúdo imobiliário |
| Tia Noza | `UCz187zucLvWxdIPI8135g0g` | vlog | verificado | São José de Piranhas; sertão paraibano |
| VLOG DO PARAÍBA | `UCt4oCmo4R0zaJZUifjnRavQ` | vlog | verificado | Campina Grande, Lagoa Seca; comércio e bairros |

### Pernambuco (PE)

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| Folha de Pernambuco | `UCFs1-aEBwg7d_n9a0gwUAZw` | vox-pop | verificado | Série Cotidiano |
| TV Guararapes Oficial | `UCOFMoDHG-vKXs-f5vcG7JaQ` | vox-pop | verificado | Recife e Caruaru; reportagem policial com moradores |
| TVTribunaPE | `UCCbJ6DzrYeuzKb3lljEOQNw` | vox-pop | verificado | Programa Ronda Geral |
| CANAPÉ PODCAST | `UCcjRt_xpaI-eAMZRjBXVB3Q` | podcast/rádio/TV | verificado | Convidados locais |
| Radio Jornal | `UCJmUR7pEaYgWquW6YwEXw6A` | podcast/rádio/TV | verificado | Super Manhã, com participação de ouvintes |
| Recife Podcast | `UCR15jJ_w5J7yLU52Nlz9u0g` | podcast/rádio/TV | verificado | — |
| TV Jornal Interior | `UCQD_Fq8NZXbHz9LI8Fa1Q9A` | podcast/rádio/TV | verificado | Cobertura de interior |
| TV Jornal SBT | `UCe1XGNDeEwAx5xaLGcNPEbQ` | podcast/rádio/TV | verificado | Sistema Jornal do Commercio, Recife |
| 38313067 | `UCjFHDmE_dwrI3jr5psQCkEg` | vlog | verificado | Serra Talhada; verificar proporção de fala |
| candido leal | `UCEHW6Hz3b8RLeYdS7srQ1mQ` | vlog | verificado | Surubim; sítio e cotidiano rural |
| ESTRELA ALVES | `UChpNJfaiccqD5FjbPhZ0AfA` | vlog | a_confirmar | Comunidade Sanharó, agreste de PE |
| Vlog com Diogo | `UCccloBzO8YHKF0GqcunbHfQ` | vlog | verificado | Caruaru; feira e cotidiano do agreste |

### Ceará (CE)

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| Acervo Mucuripe | `UC-SFNxh2EGCqhOF0yqfIMQg` | vox-pop | verificado | Memória oral do Mucuripe, Fortaleza; depoimentos de moradores antigos e pescadores |
| Cidade Alerta Ceará | `UCFG0PpSEK6YUUvyA9-AH2WA` | vox-pop | verificado | Juazeiro do Norte; reportagem com moradores. Encerra a dependência de fonte única no vox-pop do estado |
| Diário do Nordeste | `UCMf_wuiFqxdhZI1GVx02mmw` | vox-pop | verificado | Reportagem e entrevista |
| Evelyn Ferreira | `UCKloHJ0XbUJYAoL2JBAYDdQ` | vox-pop | a_confirmar | Fortaleza e Canindé; séries documentais, confirmar se é portfólio jornalístico |
| Câmara de Fortaleza | `UCaa7wRZqVT8rrv69BZB079g` | podcast/rádio/TV | verificado | Podcast Nossa Voz |
| Fortaleza Ordinária | `UCykKsnCll1OJgbgWq-jY82A` | podcast/rádio/TV | verificado | Convidados cearenses |
| O POVO | `UCj-RTZE-V3Q6jleatRR9k2A` | podcast/rádio/TV | verificado | Entrevistas ao vivo |
| TV Jangadeiro SBT | `UCEjtlZD61V7Aj-zVCi3QaUQ` | podcast/rádio/TV | verificado | Programa Barra |
| Aglais Rodrigues | `UC_AoEPCamv0OKurXEVPoGdQ` | vlog | verificado | Sobral; Mercado Central e comércio local |
| Erneston Gonçalves | `UCA1dhE6CRnUn7abJDDrQhEg` | vlog | verificado | Aquiraz e estradas do interior; cotidiano e mecânica |
| Hallyson Motovlog | `UCBknbM0sfC13DB5UQfXKo4Q` | vlog | verificado | Fortaleza; motovlog com fala corrida |
| Jenniffer Emmanuellen | `UC3TwhBS7790aFijWDZc-pww` | vlog | verificado | Iguatu; vaquejada e cotidiano do interior |
| Luchano Malik | `UC5ThrxE79tj30lsj-LK5v2w` | vlog | verificado | Cariri; vlog estudantil, Juazeiro e Crato |
| PELAS VIAS DO CARIRI | `UClG0yi8VeV2fTyM5Qr-KfaQ` | vlog | verificado | Juazeiro do Norte; bairros e comércio |
| RAÍZES DO REI | `UCNvSpGz7kXMxpkG23uWA2wA` | vlog | verificado | Interior; sertão do Ceará, Pacujá |
| Sara Emilly | `UChz6i3wDPo7HVgb_6klP0Sw` | vlog | verificado | Sobral; rotina doméstica |

### Bahia (BA)

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| Jornal Correio | `UCSbUDnouVlBoCFAA7OUrcqg` | vox-pop | verificado | Reportagem com moradores |
| Tv Baianidade Oficial | `UCmGDamP2EG1qD89d6SyJ01w` | vox-pop | verificado | Reportagem de bairro em Salvador |
| Bahia Notícias | `UCelevrrg2g7NdlrJMPrunhw` | podcast/rádio/TV | verificado | Voz Própria Podcast |
| Band Bahia Oficial | `UClXz2Nus3ASfscB60dC5gxQ` | podcast/rádio/TV | a_confirmar | Emissora regional; conteúdo esportivo de estúdio |
| Portal Metro1 - Rádio Metropole | `UCKbuLR06szTjZRNSPB0Aeuw` | podcast/rádio/TV | verificado | Jornal da Bahia no Ar |
| TV Aratu | `UCX_Nxpcz-9EXhRIlaoo2c-w` | podcast/rádio/TV | verificado | Alô Juca, com participação de ouvintes; fonte de maior valor identificada |
| Isabela Libório | `UCqAjNsKDiVvs0sXSa1wTLNA` | vlog | verificado | Salvador; cotidiano e eventos locais |
| Izabella Silva | `UCBy-xcN8gGMoGdBehIwe78g` | vlog | verificado | Ilhéus; vlog semanal de rotina |
| Jairo DroneX | `UC9LbJbLsdiRIkyQu04KiOTQ` | vlog | verificado | Juazeiro-BA; ATENÇÃO: divisa com Petrolina-PE, risco de mistura de variedades |
| João Yurley | `UClf8--I7S_LWx7exp4afLWw` | vlog | a_confirmar | Ilhéus; parte do acervo é jogo eletrônico |
| Sabor com Dri | `UCvc_34czo-Ol4nGB6VOXr8A` | vlog | verificado | Salvador; cotidiano doméstico e culinária |
| Vida no Interior da Bahia | `UCJgIwzY6ZAOvSRDusRM5JwA` | vlog | verificado | Interior; Serrolândia, Conceição do Coité, Jacobina |

### São Paulo (SP) — grupo de controle

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| EducaPrefSP SME | `UC5A8Zp0SzXnsyjGt_LmS2yQ` | vox-pop | verificado | Escolas municipais em Paraisópolis e Perus; alunos e professores. Amplia o vox-pop paulista, que dependia de fonte única |
| TV Band Paulista | `UCnMfPFJ5B7pQdEl7hVwTCFQ` | vox-pop | verificado | Band Cidade, Brasil Urgente Regional |
| Jornal da Gazeta | `UCNl_i-ggJbZNyOLlhE7yyhw` | podcast/rádio/TV | verificado | Jornalismo local |
| Record Paulista | `UCdd1PhFKkX96UUr8KmK1DhA` | podcast/rádio/TV | verificado | Emissora regional; Bauru, Sorocaba, Marília |
| TH+ SBT Interior | `UCfgLINec5p8KFyWVnogp1BA` | podcast/rádio/TV | verificado | Emissora do interior paulista; Presidente Prudente e Araçatuba |
| TV Câmara São Paulo | `UCP8XlGjPSGj8JkuZ8hgDAJw` | podcast/rádio/TV | verificado | Séries sobre periferias |
| Alan City | `UCOu8tmZzHxFdpui4q6n73DQ` | vlog | a_confirmar | História urbana da capital; verificar se é narração roteirizada |
| Beatriz Salustiano | `UCYN8VWQ_WckW8_X2DpTq4Fg` | vlog | verificado | Presidente Prudente; rotina doméstica e maternidade |
| Bielzau | `UCnoSIjynxXS5SE7CqeRH9gA` | vlog | verificado | Vlog pessoal na capital |
| Bruno Reis | `UC2ftSjkx9TcPtqaa5X37b9g` | vlog | verificado | Ribeirão Preto; daily vlog |
| Cavani Original | `UC9Xkj2idxMFBgzO9rJrILww` | vlog | verificado | Penha, Cangaíba, Mauá; percurso por bairros da capital |
| Fernando Alves | `UC-cMolhazk6A3WszU22EvRg` | vlog | verificado | Tatuapé, capital; morar sozinho em São Paulo |
| Filosofia 2 Rodas | `UCPSo2AAdJxJNIRMJ-GDAWiQ` | vlog | verificado | Motovlog; capital, Mauá e Santo André |
| Kaio D'Elaqua | `UCSp9JYcUHrU7WOAMOVI-vsw` | vlog | verificado | Mooca e cena urbana da capital; documentário de bairro |
| Kellynha Costa | `UCDMuhTKfP5PxCgXFC0Sb7jg` | vlog | a_confirmar | Campinas e Limeira; acervo majoritariamente de 2019 |
| Luki MotoVlog | `UCHx0b7B1rdKZW5vsZBh31Tg` | vlog | verificado | Motovlog urbano; Zona Sul, Marginal Pinheiros |
| Mais um na pista | `UCCAtY4pLHaGsSsFrZJcMc1A` | vlog | verificado | Motorista de aplicativo; capital e Jundiaí |
| Marco Santos 012 | `UC1u0koYujXv4n7SXS8rUmhw` | vlog | verificado | Entregador de aplicativo; região de São José dos Campos |
| Will Vlogs | `UCIiwZH_bTfGsEhPoeLpJUXQ` | vlog | verificado | Parelheiros e Bororé; cotidiano da Zona Sul |

### Rio de Janeiro (RJ) — grupo de controle

| Canal | ID | Camada | Situação | Observação |
|---|---|---|---|---|
| Jornal O São Gonçalo | `UCLRZOdi6KtqcRtncWO5sUog` | vox-pop | verificado | Região metropolitana |
| Record Rio | `UC-5q6GpZ1my8fV7VGT6LsWg` | vox-pop | verificado | Reportagem com moradores |
| Jeitinho Carioca | `UC002CUgSIkHJG496r6PBnqw` | podcast/rádio/TV | verificado | Papo de Carioca |
| TV Band Rio | `UCzQxHUiLa5prpJoyOxS0GSA` | podcast/rádio/TV | verificado | Jornal do Rio |
| Anjodoasfalto13 | `UCGVqO-7zPAEq-T8X2LML1FQ` | vlog | verificado | Motovlog; capital e Baixada |
| AS AVENTURAS DE ADRIANO RJ | `UCqm7wMBkh8dv9MIjbcVkZ9w` | vlog | verificado | Transporte público carioca; BRT, cartão Jaé, Penha, Madureira |
| Caty Senna | `UCgfaioA9LZdwfmX8nP4-DVA` | vlog | verificado | Duque de Caxias; rotina doméstica, feira local |
| Destinos Escolhidos | `UCAbkS1NK68lgqWiaAzVgT5Q` | vlog | a_confirmar | Feiras e comida de rua no Rio; confirmar residência |
| Dgw Raiz | `UC1b9HVkWnKrpLcrs9vrAxHA` | vlog | verificado | Feiras cariocas; Marechal Hermes, Praça XV, Bangu |
| EXPEDIÇÃO KL | `UCl-wjMCg6kwdR_3mao3TTBQ` | vlog | a_confirmar | Mudança da capital para Cabo Frio; ambos no RJ |
| Madrugada RJ | `UCTim5T0iUZwfHsmyWdJ8Xjg` | vlog | verificado | Baixada Fluminense; Belford Roxo, Nova Iguaçu, Tinguá |
| Mania de carro | `UCxFBGY68PJqq0pSFcCodh5w` | vlog | a_confirmar | Itaboraí e Nova Iguaçu; tema automotivo com fala espontânea |
| Manu Trindade | `UCbgme8gXDhZ6f-j-kKZAonA` | vlog | a_confirmar | Ipanema; confirmar residência |
| Me leva para conhecer | `UC5iDCiLTrOebInoqyHG008A` | vlog | verificado | Vila da Penha, Bonsucesso, Tijuca; subúrbio carioca |
| Personal Daniel Santos | `UCj5L5g7CaL0lSyuGjVqrZlw` | vlog | verificado | Motovlog; Copacabana e zona sul |
| Rodrigo Santos | `UCk-z5pXwPzy7NFr3QSil__w` | vlog | verificado | Belford Roxo; deslocamento diário e vida de CLT |
| Thay Magalhães | `UCm-A8ismf7K6YjsXUSAzemA` | vlog | verificado | Vlog doméstico; rotina na capital |

---

## 4. Situação da lista

Levantamento consolidado em 27/08/2026, após três rodadas de busca e três passagens de revisão humana.

| UF | vox-pop | podcast/rádio/TV | vlog | total | vozes distintas no vlog |
|---|---|---|---|---|---|
| PB | 2 | 3 | 7 | 12 | 7 |
| PE | 3 | 5 | 4 | 12 | 4 |
| CE | 4 | 4 | 8 | 16 | 8 |
| BA | 2 | 4 | 6 | 12 | 6 |
| SP | 2 | 4 | 13 | 19 | 13 |
| RJ | 2 | 2 | 13 | 17 | 13 |
| **Total** | **15** | **22** | **51** | **88** | — |

Rendimento agregado das três rodadas: 390 candidatos levantados, 114 aprovados na triagem automática, 47 confirmados em revisão humana — precisão de cerca de 41% para a etapa automatizada.

**Lacunas encerradas.** Ceará e São Paulo dependiam de um único canal na camada de vox-pop, que é a maior em volume e a de maior diversidade de falantes; ambos passaram a dispor de fontes adicionais. São Paulo e Rio de Janeiro não tinham nenhum vlog atribuível; passaram a treze cada.

**Assimetria remanescente, e é agora o ponto crítico.** O grupo de controle dispõe de treze vozes por estado na camada de vlog, contra quatro a oito nos estados nordestinos, sendo Pernambuco o mais frágil. A assimetria inverteu-se em relação ao diagnóstico inicial, mas continua sendo assimetria: para o experimento importa a **simetria de composição** entre os grupos, não o máximo disponível em cada um. Duas condutas são admissíveis, e a escolha cabe à equipe:

1. **Limitar por baixo.** Empregar, em cada estado, no máximo o número de vozes do estado mais fraco — hoje quatro, de Pernambuco. Descarta material disponível, mas garante composição idêntica entre grupos sem trabalho adicional.
2. **Reforçar Pernambuco e Bahia** até o patamar dos demais, e então aplicar teto comum. Preserva volume, ao custo de nova rodada de busca com o rendimento observado de cerca de um canal aproveitável a cada oito candidatos.

Em qualquer das duas, mantém-se o teto por falante estabelecido no item 2.4.5: nenhum indivíduo responde por mais de 5% da fala de um estado.

**Pendências.** Onze canais estão marcados como `a_confirmar` e exigem inspeção de conteúdo antes da coleta. A camada `vlog_amador` de Pernambuco continua sendo a mais frágil do conjunto — coincidência incômoda, já que Pernambuco é também o único estado-alvo sem marcador morfossintático próprio no instrumento de texto, conforme `docs/pares_minimos_v1.md`, seção 6.
