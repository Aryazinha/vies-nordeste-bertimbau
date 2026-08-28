# Achados: o que pode ser escrito, o que não pode, e sob que condição

**Função deste arquivo.** Separar o que o projeto já pode afirmar em texto submetido do que ainda não pode, e registrar, para cada item em suspenso, a condição precisa que o liberaria. Existe porque a distinção se perde com facilidade: uma medição feita em ambiente controlado, com dezessete arquivos, tem aparência de resultado e não o é — e a diferença só aparece em revisão por pares, quando já é tarde.

**Última revisão:** 27/08/2026

## Convenção de estado

| Estado | Significado |
|---|---|
| **SUSTENTADO** | Pode ser afirmado no artigo, com a qualificação indicada |
| **CONDICIONAL** | Depende de verificação nomeada; não escrever antes dela |
| **VEDADO** | Não pode ser afirmado, nem com ressalva |
| **CADERNO** | Pertence ao repositório e à reprodutibilidade, não ao texto |

---

# 1. SUSTENTADO — pode ser escrito

## 1.1 Assimetria de tokenização no BERTimbau, alinhada ao eixo de prestígio

**Seção do artigo:** Método, e Ameaças à Validade.

As ocupações de alto prestígio testadas — *médico*, *advogado*, *engenheiro*, *professor*, *juiz* — são representadas por token único no vocabulário do BERTimbau. As de baixo prestígio e os adjetivos de traço negativo fragmentam-se: *pedreiro* e *lavrador* em dois subtokens, *faxineiro* em quatro, *grosseira*, *desonesta* e *preguiçosa* em três. Entre os adjetivos de caráter testados, apenas *inteligente* é token único.

A fragmentação acompanha o eixo de prestígio que o experimento pretende medir. A consequência é metodológica e independe do resultado de viés: comparação por probabilidade de máscara única favorece estruturalmente os itens de token único, de modo que o confundidor de frequência descrito por Kaneko e Bollegala (2022) encontra-se materializado no próprio tokenizador. O emprego de AUL deixa de ser recomendação e torna-se condição de possibilidade.

**Procedência:** medição própria, `experimentos/smoke_test_bertimbau.py`, resultado em `experimentos/resultados/smoke_test.md`. Reprodutível por terceiros com o script.

**Qualificação obrigatória:** o conjunto de atributos testado é o do rascunho do instrumento, não um inventário exaustivo do vocabulário. A afirmação deve descrever o padrão observado nesses itens, não generalizar para todo o léxico.

## 1.2 Duas molduras de sondagem degeneram, e substitutas testadas

**Seção do artigo:** Método.

A moldura `Quem falou isso é [MASK]` concentra a massa de probabilidade em pronomes — *você* (0,385), *ele* (0,294), *eu* (0,075) —, não em atribuição de traço. A moldura `Quem falou isso estudou até o [MASK]` colapsa em expressão idiomática: *fim* (0,386), *final*, *momento*, *osso*, *pescoço*.

As substitutas testadas comportam-se adequadamente: `Quem falou isso completou o ensino [MASK]` concentra 97% da massa em *médio* (0,560) e *fundamental* (0,414); `O nível de escolaridade de quem falou isso é [MASK]` produz leitura bipolar entre *alto* (0,265) e *baixo* (0,209); `Quem falou isso parece uma pessoa [MASK]` elimina o vazamento de subtoken observado na formulação original.

**Consequência metodológica citável:** em português, deixar o gênero gramatical livre na lacuna não produz atribuição de traço. O controle de gênero na moldura não é refinamento, é requisito.

**Procedência:** medição própria, `experimentos/resultados/molduras_alternativas.md`.

## 1.3 Ausência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro

**Seção do artigo:** Trabalhos Relacionados, e justificativa da contribuição.

**Procedência:** levantamento bibliográfico, registrado em `docs/fundamentacao_teorica.md`, seção 1.3.1. Localizados precedentes de adaptação para francês e neerlandês, e um conjunto multilíngue sobre grupos migrantes; nenhuma adaptação para o português brasileiro.

## 1.4 O brWaC não documenta estratificação geográfica

**Seção do artigo:** Fundamentação, e Ameaças à Validade.

O artigo do corpus reporta diversidade de domínio temático, não de procedência geográfica ou de variedade. Não há metadado de geolocalização por documento nas versões distribuídas.

**Qualificação obrigatória:** apresentar como ausência de documentação, e a concentração Sul-Sudeste como hipótese de mecanismo apoiada em evidência socioeconômica indireta — jamais como fato quantificado pelos autores do corpus.

## 1.5 Diferenciação frente a Melo e Souza (2026)

**Seção do artigo:** Trabalhos Relacionados.

Sinalização explícita de região contra implícita por dialeto; LLM generativo com estima autoatribuída contra codificador MLM com pseudo-verossimilhança; granularidade regional contra estadual; instanciação automática de estímulos contra validação por juízes e por corpus.

Acresce que a seção de trabalhos futuros daqueles autores propõe expressamente "a incorporação de marcadores sociais implícitos" e "a inclusão de variações linguísticas regionais" — de modo que o presente projeto executa a continuidade que eles nomeiam. O enquadramento converte objeção de sobreposição em demonstração de pertinência.

**Procedência:** leitura integral do PDF, registrada em `docs/fundamentacao_teorica.md`, seção 1.3.4.

## 1.6 Cobertura dialetológica primária dos quatro estados-alvo

**Seção do artigo:** Método, validade de construto.

ALECE (Bessa, 2010) para o Ceará, Atlas Prévio dos Falares Baianos (Rossi, 1963) para a Bahia, ALiPE para Pernambuco, Atlas Linguístico da Paraíba (Aragão e Menezes, 1984) para a Paraíba, além do estudo ALiB de palatalização de /t,d/ cobrindo os nove estados nordestinos.

**Qualificação obrigatória:** há assimetria temporal relevante — o atlas baiano é de 1963 e o paraibano de 1984, contra 2010 do cearense. Marcadores extraídos das fontes mais antigas exigem confirmação em fala contemporânea.

## 1.7 Armadilhas de atribuição na construção de corpus regional a partir de plataforma

**Seção do artigo:** Método, e contribuição metodológica autônoma.

Quatro classes de canal satisfazem critérios geográficos e não servem ao propósito, cada uma por motivo distinto:

1. **Itinerante** — canais de viagem, motovlog e transporte citam muitos municípios do estado, e a menção a muitos municípios era o sinal aparentemente mais forte de pertencimento, quando é a assinatura de quem está de passagem.
2. **Narração possivelmente sintética** — canais de formato enumerativo citam o estado a cada título e são frequentemente narrados por voz artificial, o que introduziria fala não humana em corpus destinado a documentar variação humana.
3. **Sem fala** — passeios em vídeo e montagens com drone percorrem bairros identificáveis sem que ninguém fale.
4. **Falante migrante** — o canal está corretamente ancorado no estado e o autor migrou de outra região.

A quarta merece destaque teórico: sendo o fluxo migratório dominante no Brasil o Nordeste para o Sudeste, o erro **atenua sistematicamente o contraste que a pesquisa mede**, deslocando o resultado na direção da hipótese nula. Produz, portanto, aparência de ausência de viés.

**Procedência:** levantamento próprio de 390 canais candidatos, com registro em `docs/fontes_coleta.md`, seções 2.4 e 2.5. Casos concretos documentados, incluindo dois canais autoidentificados como migrantes e um canal de falante moçambicano residente em Salvador.

## 1.8 Dimensionamento de corpus a partir do requisito de detecção de variante rara

**Seção do artigo:** Método.

O volume de fala necessário por variedade foi derivado da condição estatística que torna a **ausência** de uma variante informativa, e não arbitrado. Tomando a produtividade máxima da negação pós-verbal reportada por Santos e Vitório (2025), 5,6%, e as premissas de fala declaradas, chega-se a cerca de 4,1 h de fala do locutor-alvo por variedade para que zero ocorrências constituam evidência, e não insuficiência amostral.

**Procedência:** `experimentos/meta_volume_corpus.py`, com premissas declaradas no próprio script.

**Qualificação obrigatória:** as premissas de fala — palavras por minuto, palavras por oração, proporção de orações negadas — são estimativas declaradas, não medições.

---

# 2. CONDICIONAL — depende de verificação nomeada

## 2.1 A transcrição automática não penaliza a fala nordestina

**Estado:** indício favorável, insuficiente.
**Medido:** confiança média por palavra — Nordeste 0,935, Sudeste 0,925, diferença de +0,010 em favor do Nordeste. A dispersão entre estados (0,077, de PE 0,975 a RJ 0,898) supera em muito a diferença entre grupos.
**Libera a afirmação:** WER calculado contra transcrição humana de referência, sobre a amostra estratificada já exportada. Confiança mede certeza do modelo, não acerto.
**Se confirmado:** remove um confundidor previsto na Parte 3 do `CLAUDE.md` e constitui resultado secundário publicável por si só.
**Se não confirmado:** torna-se limitação central, pois erro de transcrição desigual entre variedades se apresentaria como resultado sobre o modelo.

## 2.2 Rendimento por camada e revisão da meta de volume

**Estado:** medido em amostra insuficiente.
**Medido:** 92,3% de fala em vox-pop contra 35% supostos; 89,2% em podcast contra 60%; 81,0% em vlog contra 70%. Descontado o locutor dominante, cerca de 47% de fala-alvo em vox-pop e 68% em vlog. O recálculo indicaria cerca de 38 h no total, contra as 50 h previstas.
**Libera a afirmação:** piloto de maior volume. A amostra atual é de 6, 6 e 5 arquivos por camada.
**Depende ainda de 2.3.**

## 2.3 A diarização separa o morador entrevistado do repórter

**Estado:** sustentado quanto à separação; não verificado quanto à identidade.
**Medido:** 4,2 locutores por arquivo em vox-pop, 3,0 em podcast, 2,2 em vlog — coerente com a natureza de cada camada.
**Não verificado:** que o locutor dominante da camada de vox-pop seja o repórter, e não um entrevistado loquaz. Da suposição depende toda a estimativa de fala aproveitável.
**Libera a afirmação:** verificar se o mesmo perfil de voz reaparece em vídeos distintos do mesmo canal.

## 2.4 Os marcadores lexicais não ocorrem em fala espontânea

**Estado:** indício forte, volume insuficiente.
**Medido:** nenhuma ocorrência de *oxe*, *oxente*, *arretado*, *aperreado* ou *avexado* em 1,55 h de fala regional. A única ocorrência aparente é homógrafo — "se você **visse** as imagens" é o imperfeito do subjuntivo de *ver*, não o marcador discursivo recifense.
**Libera a afirmação:** volume compatível com a frequência esperada dos itens. Com 0,25 h por estado, ausência não distingue "não ocorre" de "não foi amostrado" — que é precisamente o que o dimensionamento do item 1.8 formaliza.
**Se confirmado:** o Bloco B do instrumento perde sustentação e a limitação deve ser declarada.
**Observação citável desde já:** a homografia de *visse* é armadilha real para detecção automática, e recai sobre o único marcador proposto para Pernambuco.

## 2.5 A sensibilidade do modelo concentra-se no léxico

**Estado:** medido em conjunto pequeno, sem teste estatístico.
**Medido:** divergência de Jensen-Shannon mediana de 0,0144 bits no bloco lexical contra 0,0023 no morfossintático, tendo 0,0963 como referência de conteúdo proposicional distinto.
**Libera a afirmação:** conjunto de itens em volume adequado e teste estatístico. Doze itens não sustentam inferência.
**Se confirmado:** exige reposicionamento do artigo, pois um efeito de origem lexical é atacável como efeito de frequência, e não de dialeto. É a objeção mais previsível em revisão.

## 2.6 A marcação explícita de região não revela o viés

**Estado:** leitura própria de tabela publicada, não confirmada contra o texto integral.
**Observado:** na Tabela 7 de Melo e Souza (2026), o marcador "nordeste" recebe estima **superior** à do marcador "sudeste" em três dos quatro modelos avaliados. O texto do artigo afirma que a menor pontuação da categoria é a do sujeito "nordeste", o que é compatível com a tabela apenas na leitura de que 2,150 é o menor valor absoluto.
**Libera a afirmação:** conferência contra o texto integral e, idealmente, comunicação com os autores.
**Se confirmado:** argumento forte para a introdução — a sinalização explícita não produziu o rebaixamento esperado, o que é o padrão de Hofmann et al. (2024), em que o alinhamento suprime o preconceito manifesto e preserva o encoberto. Motiva diretamente a abordagem implícita.

## 2.7 Direção do marcador do imperativo em Fortaleza

**Estado:** fontes secundárias em conflito.
**Conflito:** uma indica predomínio subjuntivo em Fortaleza; outra indica indicativo favorecido, com peso relativo 0,66. O capítulo de Oliveira (2017) não pôde ser consultado.
**Libera a afirmação:** consulta ao capítulo impresso.
**Consequência atual:** o item que representa o Ceará no instrumento está suspenso.

---

# 3. VEDADO — não pode ser escrito

## 3.1 Qualquer afirmação sobre viés do BERTimbau contra fala nordestina

**Não foi medido.** Nenhuma vez. O instrumento não está validado, o conjunto de itens não está fechado, nenhum juiz foi consultado e nenhum escore de viés foi calculado. Não há resultado — nem positivo, nem negativo, nem nulo.

Nada no material atual autoriza sequer a formulação "resultados preliminares sugerem".

## 3.2 O índice de 94% de imperativo indicativo no Rio de Janeiro

Registrado em revisão anterior do projeto e **não confirmado por nenhuma fonte** consultada. Não deve ser citado enquanto a origem não for localizada. O único contraste verificado entre variedades é o de Figuereido (2025), entre cidades do interior: Campinas-SP 81% contra Feira de Santana-BA 47%.

## 3.3 Que os marcadores dialetais do instrumento estejam validados

Nenhum item passou pelo Filtro 1, de juízes falantes nativos, nem pelo Filtro 2 em volume suficiente. Os itens são candidatos, e o texto deve tratá-los como tais.

## 3.4 Balanceamento de frequência lexical entre condições

Não foi medido. A terceira crítica de Kaneko e Bollegala é reconhecida no desenho, e não endereçada empiricamente.

## 3.5 Qualquer afirmação de significância estatística

Nenhum teste foi executado sobre nenhuma medida.

## 3.6 Que a composição do brWaC explique o viés observado

Não há viés observado, e a composição do corpus não é auditável. A relação permanece hipótese de mecanismo.

---

# 4. CADERNO — pertence ao repositório, não ao texto

Defeitos identificados e corrigidos durante o desenvolvimento: falha silenciosa que reportava download bem-sucedido sem arquivo em disco; aceitação de URL de canal onde se esperava vídeo; caminhos de dados relativos ao diretório de trabalho; incompatibilidade com a API nova do `pyannote`; dependência de versão do `yt-dlp` e de runtime de JavaScript.

Pertencem à documentação de reprodutibilidade. Uma exceção possível: o bloqueio de downloads originados de datacenter, que afeta qualquer tentativa de replicação em ambiente de nuvem e justifica nota em apêndice de reprodutibilidade.

---

# 5. Situação do artigo

Em termos de estrutura de texto submetido:

| Seção | Situação |
|---|---|
| Introdução e motivação | sustentada |
| Trabalhos relacionados | sustentada |
| Fundamentação | sustentada |
| Método | sustentada, e com contribuições próprias (itens 1.1, 1.2, 1.7, 1.8) |
| **Resultados** | **vazio** |
| Ameaças à validade | madura, e mais desenvolvida que o usual |
| Conclusão | inexistente, por depender de Resultados |

**Dois caminhos possíveis, não excludentes.**

O primeiro é o artigo pretendido: medição de viés dialetal implícito no BERTimbau. Exige instrumento corrigido e validado, corpus em volume suficiente para o Filtro 2, e a medição propriamente dita. É o de maior alcance e o mais distante.

O segundo é um **artigo de recurso e método**: o conjunto de pares mínimos para variação regional do português brasileiro, o protocolo de validação em dois filtros, o dimensionamento por requisito de detecção, e os achados sobre tokenização e sobre construção de corpus a partir de plataforma. Os precedentes que o projeto adota — CrowS-Pairs e French CrowS-Pairs — são exatamente dessa natureza, com a medição no modelo servindo de demonstração de uso. É alcançável com o que já existe, mais a validação por juízes, e constrói o terreno do primeiro.

A escolha é da equipe. Registre-se apenas que, no estado atual, o segundo caminho está muito mais próximo do que o primeiro.
