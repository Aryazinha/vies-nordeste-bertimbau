# Documento de Referência do Projeto
## Investigação de Vieses Sociolinguísticos no BERTimbau: Variações do Nordeste (PB, PE, CE, BA) vs. Grupo de Controle do Sudeste (SP, RJ)

**Status:** Documento vivo — Contexto oficial e memória de longo prazo do projeto
**Última atualização:** 06/08/2026 (revisão v1.5)
**Mantido por:** Equipe de pesquisa (assistido por Claude, atuando como pesquisador sênior em PLN/IA)

---

## Log de revisões

| Versão | Data | Alterações |
|---|---|---|
| v1.0 | 05/08/2026 | Versão inicial: fundamentação teórica (BERTimbau, brWaC, CrowS-Pairs/StereoSet, Kaneko & Bollegala, Hofmann et al.) + documentação técnica da stack (yt-dlp, faster-whisper, pyannote.audio). |
| v1.1 | 05/08/2026 | Fechamento das 4 pendências de busca da rodada anterior: (1) dados Cetic.br/TIC Domicílios 2024 sobre acesso/produção de conteúdo por região; (2) fontes dialetológicas primárias ALiB (ALiPE, Atlas da Paraíba, estudo de palatalização); (3) referência consolidada de Bagno (1999); (4) confirmação da ausência de adaptação de CrowS-Pairs/StereoSet para PT-BR **e** identificação de trabalho relacionado direto — Melo & Souza (2026), PROPOR — que precisa ser diferenciado explicitamente na seção de trabalhos relacionados do artigo. |
| v1.2 | 06/08/2026 | **Decisão metodológica formal da equipe (nova seção 1.4):** o projeto usará **texto e áudio** (não apenas literatura). Define o protocolo mínimo viável: quais informações são coletadas por vídeo, regras de anonimização, e o corte de região/marcador-alvo inicial (palatalização /t,d/, PB/PE/CE/BA capital+interior vs. SP/RJ). Fecha os 4 pontos que estavam em aberto: informações coletadas, anonimização, texto-e-áudio, corte de coleta. |
| v1.3 | 06/08/2026 | **Marcador primário de TEXTO redefinido:** a palatalização de /t,d/ é fonética e não se manifesta na ortografia — fica reservada para validação via áudio (seção 1.4). Marcador de texto adotado: alternância do imperativo indicativo ("pega/traz/dá") vs. subjuntivo ("pegue/traga/dê") — dados ALiB (Oliveira, 2017): Salvador/BA 28% indicativo, Fortaleza/CE e João Pessoa/PB majoritariamente subjuntivo, vs. Rio de Janeiro >94% indicativo. **Pendência aberta:** Recife/PE tem uso simétrico (sem predominância) — precisa de marcador próprio para PE. Primeiro rascunho de 6 pares mínimos (formato matched-guise) produzido para revisão da equipe antes de validação por juízes/falantes nativos. |
| v1.4 | 06/08/2026 | **Migração para Claude Code:** arquivo renomeado de `contexto_projeto_vies_nordeste_bertimbau.md` para `CLAUDE.md` (memória persistente automática do Claude Code). Parte 2 (documentação técnica detalhada de yt-dlp/faster-whisper/pyannote.audio) movida para `docs/stack_tecnica.md` para reduzir o tamanho do arquivo recarregado a cada sessão (~560 → ~310 linhas). Pipeline piloto (`config.py`, `collect.py`, `transcribe.py`, `diarize.py`, `pipeline.py`) já implementado e versionado junto ao projeto. |
| v1.5 | 06/08/2026 | **Correção de tamanho:** Claude Code acusou CLAUDE.md acima do limite prático de 40.000 caracteres (estava em 45.719). Seções 1.1, 1.2 e 1.3 (fundamentação teórica detalhada: BERTimbau, brWaC, CrowS-Pairs/StereoSet, Kaneko & Bollegala, Hofmann et al., Melo & Souza) movidas para `docs/fundamentacao_teorica.md`, com resumo de 5 linhas mantido no lugar. CLAUDE.md caiu para ~17.000 caracteres. |

---

## Como usar este documento

Este arquivo é o `CLAUDE.md` do projeto — lido automaticamente pelo Claude Code no início de toda sessão. Consolida o protocolo metodológico fechado (seção 1.4) e as ameaças à validade (Parte 3). A fundamentação teórica completa está em `docs/fundamentacao_teorica.md`, e a documentação técnica da stack de coleta em `docs/stack_tecnica.md` — ambos consultados sob demanda, não recarregados automaticamente. Este arquivo deve ser tratado como **artefato versionado** (sugestão: Git, com commits por revisão) e citado nas próximas decisões metodológicas, para garantir rastreabilidade e reprodutibilidade — requisitos centrais para submissão em periódico/conferência (ex.: BRACIS, PROPOR, STIL, LREC, ACL/EMNLP tracks de fairness).

---
# PARTE 1 — FUNDAMENTAÇÃO TEÓRICA

**[MOVIDO em 06/08/2026 — v1.5]** A fundamentação teórica completa (BERTimbau, brWaC, metodologias de avaliação de viés, CrowS-Pairs/StereoSet, Kaneko & Bollegala, Hofmann et al., trabalho relacionado de Melo & Souza) foi movida para `docs/fundamentacao_teorica.md` — CLAUDE.md ultrapassou o limite prático de 40k caracteres do Claude Code. Consulte esse arquivo quando precisar justificar uma escolha metodológica ou escrever a fundamentação do artigo; ele não é recarregado automaticamente a cada sessão.

**Resumo do que está lá, pra referência rápida sem abrir o arquivo:**
- 1.1 BERTimbau: treinado só com brWaC, MLM+WWM, Base/Large.
- 1.2 brWaC: 2,7B tokens, sem estratificação geográfica documentada — viés Sul-Sudeste é hipótese apoiada em dados Cetic.br/NIC.br (1.2.1), Bagno (1.2.2) e fontes ALiB/ALiPE/Atlas da Paraíba (1.2.3).
- 1.3 Metodologias: CrowS-Pairs/StereoSet (PLL), crítica de Kaneko & Bollegala (usar AUL/AULA também), Hofmann et al. 2024 = precedente central (matched-guise probing), Melo & Souza (2026, PROPOR) = trabalho relacionado a diferenciar explicitamente (sinalização explícita/LLM/estima vs. nosso implícito/MLM/PLL).

---

## 1.4 [NOVO — v1.2] Protocolo metodológico e operacional definido pela equipe

**Decisão registrada em 06/08/2026:** o projeto usará **texto e áudio**, não apenas literatura dialetológica. O corpus de áudio (pipeline `yt-dlp` → `faster-whisper` → `pyannote.audio`, Parte 2) serve para validar empiricamente que os marcadores dialetais citados na seção 1.2.3 realmente ocorrem em fala espontânea regional atual, antes de serem formalizados como pares mínimos de texto para o *fill-mask* do BERTimbau. O experimento final continua sendo em texto (BERTimbau é um encoder), mas os marcadores não serão extraídos *apenas* de atlas linguísticos — serão confirmados em corpus coletado pelo projeto.

Isso fecha os quatro pontos que estavam em aberto na fase de planejamento:

### 1.4.1 Informações coletadas por vídeo/áudio

| Campo | Descrição |
|---|---|
| `id` | ID do vídeo no YouTube (identificador primário, evita colisão de nomes) |
| `canal` | Nome do canal de origem |
| `data_upload` | Data de publicação do vídeo |
| `duracao_s` | Duração em segundos |
| `transcricao` | Texto transcrito, com timestamps a nível de palavra (`faster-whisper`, `word_timestamps=True`) |
| `diarizacao` | Rótulo de locutor por trecho (`pyannote.audio`) |
| `estado_alvo` | PB / PE / CE / BA / SP / RJ — variedade que o vídeo representa |
| `tipo_fonte` | `entrevista_vox_pop` / `podcast_radio_tv_regional` / `vlog_amador` (ver camadas da seção 1.4.3) |

Nenhum dado pessoal sensível (CPF, endereço, contato) é coletado — apenas o que já está publicamente disponível no vídeo (conforme metadados do `yt-dlp`, seção 2.1.3).

### 1.4.2 Anonimização

- Nomes próprios de terceiros mencionados nas transcrições (não o autor do vídeo) são mascarados antes de qualquer publicação do dataset.
- O áudio bruto **não** é redistribuído publicamente — segue a prática já recomendada na seção 2.1: publicar apenas IDs de vídeo + código de coleta, permitindo reprodutibilidade sem violar direitos autorais/ToS do YouTube.
- O nome do canal/criador de conteúdo é mantido, por se tratar de conteúdo público postado voluntariamente (não é dado pessoal de terceiro vulnerável).
- Nenhum dado de geolocalização precisa (endereço, coordenadas) é coletado — apenas o estado-alvo já conhecido pela origem/temática do canal.

### 1.4.3 Corte de coleta / região e camadas de fonte

- **Escopo geográfico:** PB, PE, CE, BA — capital **e** interior (conforme já definido), comparados ao grupo de controle SP, RJ.
- **Marcador-alvo inicial:** palatalização de /t,d/ diante de /i/ (seção 1.2.3, item 1) — escolhido por ser o traço mais robusto, documentado nos 9 estados nordestinos, com metodologia de amostragem transparente.
- **Camadas de fonte de áudio** (mesma lógica de diversidade diafásica do C-ORAL-BRASIL — contextos públicos e mais controlados vs. mais espontâneos):
  - Camada "âncora" (~60–70% do volume): entrevistas de rua/vox-pop regionais, podcasts e rádio/TV local no YouTube — áudio mais limpo, menor WER/DER esperado.
  - Camada "espontânea" (~30–40% do volume): vlogs amadores e criadores de conteúdo regionais — fala mais genuinamente informal, exige QA manual mais criterioso.

**Próximo passo operacional:** com o protocolo fechado, os dois entregáveis concretos que dependem dele podem começar em paralelo — (1) rascunho dos primeiros pares mínimos de texto a partir do marcador de palatalização, e (2) script piloto de coleta seguindo os campos da seção 1.4.1.

---

# PARTE 2 — DOCUMENTAÇÃO TÉCNICA DA STACK DE DADOS

**[MOVIDO em 06/08/2026 — v1.4]** A documentação detalhada de `yt-dlp`, `faster-whisper` e `pyannote.audio` (parâmetros, código, vantagens/desvantagens de cada ferramenta) foi movida para `docs/stack_tecnica.md`, para manter este arquivo enxuto — ele é recarregado a cada mensagem de sessão no Claude Code, então só o que precisa moldar decisões em toda sessão fica aqui. O pipeline implementado (`config.py`, `collect.py`, `transcribe.py`, `diarize.py`, `pipeline.py`) já reflete essas decisões em código executável — consulte `docs/stack_tecnica.md` só quando precisar entender o *porquê* de um parâmetro específico.

---

# PARTE 3 — SÍNTESE DE AMEAÇAS À VALIDADE (a expandir ao longo do projeto)

| Ameaça | Descrição | Mitigação proposta |
|---|---|---|
| **Validade de construto dos marcadores dialetais** | Risco de usar estereótipos populares em vez de traços dialetais reais | Basear-se em fontes dialetológicas (ALiB, ALiPE, Atlas da Paraíba — seção 1.2.3) + validação por juízes/falantes nativos de cada variedade |
| **Confusão entre viés de frequência lexical e viés social** | Itens mais/menos frequentes no corpus de treino podem distorcer o escore de PLL | Balancear frequência lexical entre condições; reportar métricas complementares (AUL/AULA) |
| **Atribuição causal ao brWaC não auditável diretamente** | O brWaC não expõe metadados geográficos por documento | Tratar como hipótese de mecanismo, apoiada em dados socioeconômicos indiretos (Cetic.br/NIC.br, seção 1.2.1), não fato comprovado; declarar explicitamente como limitação |
| **Qualidade/ruído da transcrição automática (ASR)** | Erros de transcrição podem introduzir ruído sistemático, especialmente se o WER for maior para fala nordestina do que para fala do eixo Sul-Sudeste (viés de ferramenta, não só do modelo-alvo) | QA manual amostral por variedade regional; reportar WER estratificado por grupo, não só agregado — isso é, aliás, um resultado interessante por si só |
| **Erros de diarização em áudio de baixa qualidade** | Pode confundir locutores em trechos sobrepostos/ruidosos | Amostragem de QA manual com cálculo de DER |
| **Representatividade da amostra dentro de cada estado** | PB/PE/CE/BA e SP/RJ têm variação interna (urbano/rural, capital/interior, classe social) | Documentar explicitamente critérios de seleção de fontes/canais e discutir como limitação de generalização |
| **Balanceamento do dataset final** | Desbalanceamento entre grupos pode enviesar métricas agregadas | Igualar (ou normalizar estatisticamente) volume de áudio/tokens por grupo regional |
| **Ética/direitos autorais do material coletado** | Conteúdo do YouTube tem termos de uso próprios; falantes podem não ter consentido para pesquisa | Preferir publicar IDs de vídeo + código de coleta, não o áudio bruto; considerar anonimização de nomes próprios nas transcrições publicadas |
| **[NOVO — v1.1] Sobreposição percebida com trabalho relacionado recente** | Melo & Souza (2026, PROPOR) já investigou viés de região em LLMs em português, o que um revisor pode confundir com o escopo deste projeto | Diferenciar explicitamente na introdução/trabalhos relacionados: sinalização implícita (dialeto) vs. explícita (menção à região), MLM/PLL vs. LLM generativo/estima, granularidade estadual vs. regional (ver seção 1.3.4) |

---

# PARTE 4 — REFERÊNCIAS CONSOLIDADAS (formato para BibTeX / gerenciador de referências)

1. Souza, F., Nogueira, R., Lotufo, R. (2020). BERTimbau: Pretrained BERT Models for Brazilian Portuguese. *BRACIS 2020*, LNCS 12319, Springer. https://doi.org/10.1007/978-3-030-61377-8_28
2. Wagner Filho, J. A., Wilkens, R., Idiart, M., Villavicencio, A. (2018). The brWaC Corpus: A New Open Resource for Brazilian Portuguese. *LREC 2018*. https://aclanthology.org/L18-1686/
3. Nangia, N., Vania, C., Bhalerao, R., Bowman, S. R. (2020). CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models. arXiv:2010.00133.
4. Nadeem, M., Bethke, A., Reddy, S. (2020). StereoSet: Measuring stereotypical bias in pretrained language models.
5. Kaneko, M., Bollegala, D. (2022). Unmasking the Mask — Evaluating Social Biases in Masked Language Models. *AAAI 2022*. arXiv:2104.07496.
6. Névéol, A., Dupont, Y., Bezançon, J., Fort, K. (2022). French CrowS-Pairs: Extending a challenge dataset for measuring social bias in masked language models to a language other than English. *ACL 2022*. https://aclanthology.org/2022.acl-long.583/
7. Hofmann, V., Kalluri, P. R., Jurafsky, D., King, S. (2024). Dialect prejudice predicts AI decisions about people's character, employability, and criminality. arXiv:2403.00742. Publicado como: AI generates covertly racist decisions about people based on their dialect. *Nature*, 633, 147–154. https://www.nature.com/articles/s41586-024-07856-5
8. Salazar, J., Liang, D., Nguyen, T. Q., Kirchhoff, K. (2020). Masked Language Model Scoring. (metodologia base de PLL usada em CrowS-Pairs).
9. Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. (arquitetura base do BERTimbau).
10. Documentação técnica: `yt-dlp` (https://github.com/yt-dlp/yt-dlp), `faster-whisper` (https://github.com/SYSTRAN/faster-whisper), `pyannote.audio` (https://github.com/pyannote/pyannote-audio).
11. **[NOVO — v1.1]** Cetic.br/NIC.br (2024). Pesquisa sobre o uso das tecnologias de informação e comunicação nos domicílios brasileiros: TIC Domicílios 2024. https://cetic.br/pt/pesquisa/domicilios/
12. **[NOVO — v1.1]** Bagno, M. (1999). Preconceito Linguístico: o que é, como se faz. São Paulo: Edições Loyola.
13. **[NOVO — v1.1]** Projeto Atlas Linguístico do Brasil (ALiB). Estudo sobre a realização de /t,d/ diante de /i/ no Nordeste brasileiro. UEFS/UFBA. http://www.mel.uefs.br/modules/conteudo/conteudo.php?conteudo=67
14. **[NOVO — v1.1]** Sá, E. J. de. Atlas Linguístico de Pernambuco (ALiPE). Tese (Doutorado em Letras) — Universidade Federal da Paraíba. https://alib.ufba.br/atlas-linguistico-de-pernambuco-alipe
15. **[NOVO — v1.1]** Aragão, M. do S.; Menezes, C. P. B. de. (1984). Atlas Linguístico da Paraíba. Brasília: UFPB/CNPq.
16. **[NOVO — v1.1]** Melo, J. L. L. de; Souza, M. (2026). Levados em Consideração: Uma Avaliação de Vieses de Estima por Raça, Gênero e Região em Grandes Modelos de Linguagem em Português Brasileiro. *PROPOR 2026*, pp. 516–528, Salvador, Brasil. https://aclanthology.org/2026.propor-1.51/

**Pendências de busca para a próxima rodada** (atualizado v1.1):
- ~~Dados quantitativos atualizados de acesso à internet/produção de conteúdo digital por região do Brasil (Cetic.br, IBGE/PNAD-TIC)~~ — **RESOLVIDO, ver seção 1.2.1.**
- ~~Literatura dialetológica primária sobre os traços fonético-lexicais-sintáticos específicos de PB, PE, CE, BA (ex. Atlas Linguístico do Brasil — ALiB)~~ — **PARCIALMENTE RESOLVIDO, ver seção 1.2.3.** Pendência remanescente: atlas estaduais específicos e consolidados para **Ceará** e **Bahia** (equivalentes ao ALiPE e ao Atlas da Paraíba já localizados).
- ~~Bagno, M. — obras sobre preconceito linguístico no Brasil~~ — **RESOLVIDO, ver seção 1.2.2.**
- ~~Eventuais adaptações de CrowS-Pairs/StereoSet especificamente para português brasileiro~~ — **CONFIRMADO: não há adaptação consolidada e amplamente citada.** Lacuna real. Porém, **identificado trabalho relacionado direto que precisa ser diferenciado no artigo: Melo & Souza (2026), PROPOR — ver seção 1.3.4.**
- **[NOVO]** Buscar "Atlas Linguístico do Ceará" e "Atlas Linguístico da Bahia" (ou equivalentes de mesorregião/atlas de pequeno domínio) para fechar a cobertura dialetológica primária dos 4 estados-alvo.
- **[NOVO]** Ler o PDF completo de Melo & Souza (2026) (não apenas o abstract) para avaliar se o desenho metodológico deles (prompt templates, definição operacional de "estima") oferece algum insumo reaproveitável para o desenho dos pares mínimos do projeto, além da diferenciação já registrada na seção 1.3.4.
