# Protocolo Metodológico

## Investigação de Vieses Sociolinguísticos no BERTimbau: variedades do Nordeste (PB, PE, CE, BA) frente a um grupo de controle do Sudeste (SP, RJ)

**Função deste documento.** Reunir, em arquivo versionado, as partes do protocolo que os demais documentos do repositório citam: o protocolo metodológico e operacional, o esquema de dados e a síntese de ameaças à validade.

**Origem.** Estas seções eram mantidas em `CLAUDE.md`, arquivo de contexto e memória de longo prazo do projeto que permanece fora do versionamento por decisão registrada em agosto de 2026. A consequência era que quem clonasse o repositório encontraria referências a um arquivo ausente, justamente nas partes de método que sustentam a reprodutibilidade. Este documento resolve isso; o `CLAUDE.md` conserva o que é interno — o registro de revisões, o estado corrente do trabalho e as orientações de sessão.

**Correspondência de numeração.** As seções abaixo preservam a numeração original, de modo que uma referência a "seção 1.4.2 do `CLAUDE.md`" corresponde à seção 1.4.2 deste arquivo.

**Documentos irmãos.** A especificação completa e atualizada dos conjuntos de dados está em [`dataset-spec.md`](dataset-spec.md); a fundamentação teórica em [`fundamentacao_teorica.md`](fundamentacao_teorica.md); os parâmetros das ferramentas em [`stack_tecnica.md`](stack_tecnica.md).

---

## 1.4 Protocolo metodológico e operacional

**Decisão registrada em 06/08/2026.** O projeto emprega texto **e** áudio, não apenas literatura dialetológica. O corpus de áudio — coletado pelo pipeline `yt-dlp` → `faster-whisper` → `pyannote.audio` — serve para verificar empiricamente que os marcadores dialetais indicados pela literatura ocorrem em fala espontânea regional contemporânea, antes de serem formalizados como pares mínimos de texto. O experimento final permanece em texto, dado que o BERTimbau é um codificador; o que a coleta acrescenta é que os marcadores não são extraídos apenas de atlas linguísticos, mas confirmados em corpus levantado pelo próprio projeto.

> **Atualização de 29/08/2026.** A função instrumental descrita acima deixou de ser a principal: o corpus de áudio passou a **entregável autônomo**, por decisão registrada em [`dataset-spec.md`](dataset-spec.md) §1.1. O Filtro 2 não desaparece — continua sendo o procedimento pelo qual um marcador se confirma em fala real —, mas deixou de ser a razão de ser da coleta e de dimensioná-la.

### 1.4.1 Informações coletadas por vídeo

| Campo | Descrição |
|---|---|
| `id` | Identificador do vídeo no YouTube, chave primária do registro |
| `canal` | Nome do canal de origem |
| `data_upload` | Data de publicação |
| `duracao_s` | Duração em segundos |
| `transcricao` | Texto transcrito com timestamps em nível de palavra (`faster-whisper`, `word_timestamps=True`) |
| `diarizacao` | Rótulo de locutor por trecho (`pyannote.audio`) |
| `estado_alvo` | PB, PE, CE, BA, SP ou RJ — variedade que o vídeo representa |
| `tipo_fonte` | `entrevista_vox_pop`, `podcast_radio_tv_regional` ou `vlog_amador` (ver 1.4.3) |

Não se coleta dado pessoal sensível. Registra-se apenas o que já está publicamente disponível nos metadados do vídeo.

> **Duas precisões, acrescentadas em 29/08/2026.** O esquema acima descreve o **registro final**, produzido após transcrição e diarização. O **registro de coleta**, gravado antes do processamento, não contém `transcricao` nem `diarizacao`, e acrescenta `arquivo` e `trecho` — este último por exigência de reprodutibilidade, já que um identificador de vídeo sem o recorte utilizado não permite reconstruir o material analisado. Ambos os registros trazem ainda `duracao_coletada_s`, distinto de `duracao_s`: o primeiro é a duração do áudio em disco, o segundo a do vídeo de origem, e eles divergem sempre que apenas um recorte foi baixado. O esquema completo dos dois registros, com tipos e vocabulário controlado, está em [`dataset-spec.md`](dataset-spec.md) §1.2 e §1.3.

### 1.4.2 Anonimização

- Nomes próprios de terceiros mencionados nas transcrições — não o autor do vídeo — são mascarados antes de qualquer publicação do conjunto de dados.
- O áudio bruto não é redistribuído. Publicam-se os identificadores de vídeo e o código de coleta, o que preserva a reprodutibilidade sem violar direitos autorais ou os termos de uso da plataforma.
- O nome do canal é mantido, por tratar-se de conteúdo público publicado voluntariamente.
- Não se coleta geolocalização precisa; registra-se apenas o estado-alvo, já conhecido pela origem ou temática do canal.

> **Duas condições ainda não satisfeitas**, registradas em [`ficha_conjunto.md`](ficha_conjunto.md) A.6. O mascaramento de nomes próprios **não está implementado**, de modo que as transcrições existentes não podem ser publicadas como estão. E o estatuto da transcrição — que não é áudio bruto nem identificador — não foi decidido por este protocolo, permanecendo em consulta.

### 1.4.3 Escopo de coleta e camadas de fonte

**Escopo geográfico.** PB, PE, CE e BA, capital e interior, comparados ao grupo de controle formado por SP e RJ.

**Marcadores-alvo.** A distinção entre marcador de áudio e marcador de texto é constitutiva do desenho e não deve ser reduzida a um marcador único:

- *No áudio:* palatalização de /t,d/ diante de /i/, o traço mais robusto disponível, documentado nos nove estados nordestinos com metodologia de amostragem transparente. Por ser fenômeno fonético, valida-se exclusivamente em áudio.
- *No texto:* feixe de marcadores morfossintáticos e lexicais especificado em [`pares_minimos_v1.md`](pares_minimos_v1.md) — alternância do imperativo, negação pós-verbal e léxico regional. Nenhum marcador de texto é empregado isoladamente, e nenhum integra o experimento sem aprovação nos dois filtros de validação daquele documento.

**Camadas de fonte de áudio**, seguindo a lógica de diversidade diafásica do C-ORAL-BRASIL:

- *Camada âncora*, de 60% a 70% do volume: entrevistas de rua, podcasts e rádio ou televisão local. Áudio mais limpo, com WER e DER esperados mais baixos.
- *Camada espontânea*, de 30% a 40% do volume: vlogs e criadores de conteúdo regionais. Fala mais informal, exigindo verificação manual mais criteriosa.

---

## Parte 3 — Ameaças à validade

| Ameaça | Descrição | Mitigação |
|---|---|---|
| **Validade de construto dos marcadores dialetais** | Emprego de estereótipo de circulação popular no lugar de traço dialetal documentado | Fundamentação em fontes dialetológicas primárias (seção 1.2.3 da fundamentação) e validação por juízes falantes nativos de cada variedade |
| **Confundidor de prestígio e escolaridade no marcador do imperativo** | A forma subjuntiva é a prescrita pela norma culta e, dentro da própria comunidade nordestina, correlaciona-se com escolaridade mais alta (Figuereido, 2025). Um *guise* nordestino apoiado nessa forma pode medir escolaridade em vez de região, com possível inversão do sinal | Nunca empregar o marcador isoladamente no bloco combinado; medir a magnitude do confundidor pela comparação entre os blocos do instrumento; registrar a divergência de Sampaio (2001) para Salvador |
| **Baixa produtividade da negação pós-verbal** | A variante alcança no máximo 5,6% de ocorrência nas localidades estudadas (Santos e Vitório, 2025); a dupla negação, mais frequente, é compartilhada com o Rio de Janeiro | Calibrar o volume de fala necessário para que a ausência de ocorrências seja informativa; não interpretar ausência em corpus pequeno como refutação |
| **Confusão entre viés de frequência lexical e viés social** | Itens de frequência desigual no corpus de treinamento distorcem o escore de PLL (Kaneko e Bollegala, 2022) | Balancear frequência lexical entre condições; reportar AUL/AULA ao lado do PLL; decompor o instrumento em blocos morfossintático, lexical e combinado |
| **Atribuição causal ao brWaC não auditável** | O corpus não expõe metadados geográficos por documento | Tratar como hipótese de mecanismo apoiada em evidência socioeconômica indireta, declarando explicitamente a limitação |
| **Qualidade da transcrição automática** | Erros de ASR podem introduzir ruído sistemático, sobretudo se o WER for maior para fala nordestina que para fala do eixo Sul-Sudeste — o que seria viés de ferramenta, não do modelo-alvo | Verificação manual amostral por variedade; reportar WER estratificado por grupo, e não apenas agregado. O WER estratificado é resultado publicável por si só |
| **Erros de diarização** | Confusão de locutores em trechos sobrepostos ou ruidosos | Amostragem de verificação manual com cálculo de DER |
| **Representatividade dentro de cada estado** | Cada estado apresenta variação interna: urbano e rural, capital e interior, estratos sociais distintos | Documentar os critérios de seleção de canais e discutir como limitação de generalização |
| **Balanceamento do conjunto final** | Desbalanceamento entre grupos enviesa métricas agregadas | Igualar ou normalizar estatisticamente o volume de áudio e de tokens por grupo regional |
| **Falante migrante** | Canal corretamente ancorado no estado pode ter autor migrado de outra região. Como o vetor migratório dominante é Nordeste para Sudeste, o erro atenua sistematicamente o contraste medido e produz aparência de ausência de viés | Exclusão de canais com indício de migração; checagem de coerência dialetal na curadoria das transcrições, que opera sobre a fala e não sobre metadados; declaração explícita da limitação, incontornável em corpus de fala pública (ver [`fontes_coleta.md`](fontes_coleta.md), 2.5) |
| **Procedência da voz em plataformas de áudio reaproveitado** | TikTok e Instagram permitem publicar vídeo com áudio gravado por terceiro, possivelmente de outra região, sem que a substituição seja detectável por inspeção do perfil | Excluídas do corpus principal; reabertura apenas como subcorpus declarado e simétrico entre grupos, sob os critérios da seção 2.3.1 de [`fontes_coleta.md`](fontes_coleta.md) |
| **Ética e direitos autorais** | O conteúdo tem termos de uso próprios e os falantes não consentiram para fins de pesquisa | Publicar identificadores e código, não o áudio bruto; anonimizar nomes próprios nas transcrições publicadas |
| **Sobreposição percebida com trabalho relacionado** | Melo e Souza (2026) investigaram viés de região em modelos de linguagem em português | Diferenciar explicitamente na introdução e em trabalhos relacionados, enquadrando o projeto como execução da continuidade que aqueles autores propõem em sua seção de trabalhos futuros |
| **Propagação de dado não verificado** | Índices citados a partir de fontes secundárias podem não corresponder à fonte primária, como no caso do índice de 94% atribuído ao Rio de Janeiro na revisão v1.3 | Convenção de procedência obrigatória em todos os documentos; nenhum dado secundário vai ao artigo sem conferência |

> **Duas ameaças acrescentadas pelas medições de 28 e 29/08/2026**, e documentadas em [`achados_para_o_artigo.md`](achados_para_o_artigo.md), itens 1.1 e 1.16.
>
> **Assimetria de tokenização alinhada ao eixo medido.** O léxico de baixo prestígio fragmenta-se em subtokens no BERTimbau, ao passo que o de alto prestígio é de token único, de modo que uma medição de viés pode produzir efeito significativo inteiramente atribuível à segmentação. Ocorreu neste projeto e foi desfeito. O mascaramento do alvo por inteiro é correção parcial e não basta; o controle exige balancear a extensão em subtokens entre os polos do eixo, ou empregar AUL.
>
> **Unidade de replicação.** As medições de um mesmo par compartilham o enunciado e não são independentes. Tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza. Toda estatística deve operar no nível do par.

---

## Convenção de procedência

Toda afirmação de terceiros nos documentos do projeto recebe uma marca: *fonte verificada* indica consulta ao texto integral; *fonte secundária* indica dado obtido por citação em outro trabalho ou por resumo publicado. Nenhum dado marcado como secundário vai ao artigo sem conferência prévia contra a fonte primária.
