# Piloto de coleta — medições

**Executado em:** 27/08/2026
**Material:** 17 trechos, 1,55 h de áudio, 6 estados × 3 camadas, um trecho por combinação
**Ambiente:** coleta local, transcrição e diarização em GPU (Colab), conforme `notebooks/README.md`

O piloto não produz dados de pesquisa. Produz as medidas que até aqui eram suposições declaradas, e submete os marcadores do instrumento de texto ao Filtro 2 pela primeira vez.

**Advertência de escala.** São 6, 6 e 5 arquivos por camada, e cerca de 0,25 h de fala por estado. Nada aqui autoriza revisão definitiva de parâmetro; o que se pode fazer é distinguir suposições que se sustentam daquelas que não se sustentam, e identificar defeitos de método antes de escalar.

---

## 1. Rendimento por camada

| Camada | Fala / duração | Suposto | Locutor dominante |
|---|---|---|---|
| `entrevista_vox_pop` | 92,3% | 35% | 49,4% |
| `podcast_radio_tv_regional` | 89,2% | 60% | 82,8% |
| `vlog_amador` | 81,0% | 70% | 84,4% |

As suposições eram pessimistas. Elas pressupunham vídeos com proporção considerável de vinheta, música e imagem sem fala; o material efetivamente coletado é denso em fala, sobretudo a reportagem curta de telejornal.

**A primeira coluna não é, porém, a medida que interessa.** Fala não equivale a fala aproveitável: na camada de vox-pop, o turno do repórter não integra a variedade-alvo. A coluna do locutor dominante permite uma leitura por camada:

- **Vox-pop, dominante em 49,4%.** Uma voz ocupa cerca de metade do tempo. Sob a hipótese de que seja a do repórter, o aproveitamento situa-se em torno de **47%** — ainda acima dos 35% supostos.
- **Vlog, dominante em 84,4%.** Aqui o locutor dominante **é** o alvo. Aproveitamento em torno de **68%**, praticamente coincidente com os 70% supostos. Foi a única suposição correta.
- **Podcast, dominante em 82,8%.** Presumivelmente o apresentador. Em emissora regional, o apresentador também é falante do estado, de modo que o turno conta; o aproveitamento aproxima-se dos 89% medidos.

**Recálculo da meta de volume, a título indicativo:**

| | Suposto | Medido |
|---|---|---|
| Áudio bruto por estado | 8,3 h | ~6,4 h |
| Total, seis estados | 50 h | ~38 h |

**Hipótese não testada.** A leitura do vox-pop depende de supor que o locutor dominante seja o repórter, e não um entrevistado loquaz. A verificação possível é observar se o mesmo perfil de voz reaparece em vídeos distintos do mesmo canal.

**Defeito corrigido durante a execução.** A primeira versão da medida usava como denominador o fim do último segmento de fala, e não a duração do arquivo. Como o Whisper suprime silêncio antes de emitir segmentos, o resultado tendia a 100% por construção — a fala era medida contra si mesma. Os valores acima já empregam a duração real, obtida de `metadados.json`.

## 2. Diarização

| Camada | Locutores por arquivo |
|---|---|
| `entrevista_vox_pop` | 4,2 |
| `podcast_radio_tv_regional` | 3,0 |
| `vlog_amador` | 2,2 |

A distribuição é coerente com a natureza de cada camada, e o pressuposto da camada de vox-pop — que a diarização separe o morador entrevistado do repórter — sustenta-se. O vídeo institucional de escola municipal em São Paulo e o programa de debate do Rio de Janeiro registraram oito locutores cada.

Dois arquivos apresentaram locutor único, ambos em `podcast_radio_tv_regional` (CE e PE): locução de notícia sem entrevistado. Não constituem erro de diarização, mas não servem ao propósito da coleta.

## 3. Indicador de dificuldade de transcrição

Confiança média por palavra. **Não é WER** — mede a certeza do modelo, não o acerto.

| Estado | Palavras | Confiança |
|---|---|---|
| PE | 782 | 0,975 |
| CE | 1.347 | 0,961 |
| SP | 2.397 | 0,953 |
| PB | 2.405 | 0,941 |
| BA | 2.543 | 0,904 |
| RJ | 2.467 | 0,898 |

**Nordeste 0,935; Sudeste 0,925; diferença +0,010.**

O grupo nordestino apresentou confiança ligeiramente **superior**, e o menor valor individual é o do Rio de Janeiro. A dispersão entre estados (0,077, de PE a RJ) supera em muito a diferença entre grupos (0,010), o que sugere que a variação não é explicada pelo agrupamento regional — mais provavelmente por qualidade de áudio e tipo de conteúdo.

O achado é preliminar e não substitui o WER. Se confirmado em amostra maior, remove um confundidor relevante: a ameaça registrada na Parte 3 do `CLAUDE.md` prevê que erro de transcrição maior para fala nordestina se apresentaria como resultado sobre o modelo quando é viés de ferramenta.

Não foi detectada alucinação do reconhecedor (segmentos idênticos repetidos), verificação feita sobre todos os 17 arquivos.

## 4. Primeira aplicação do Filtro 2

Busca dos marcadores do instrumento de texto nas transcrições. **Todas as ocorrências foram inspecionadas individualmente**, e o exame altera radicalmente a leitura dos números brutos.

### 4.1 Negação pós-verbal: nenhuma ocorrência real

A busca automática retornou três candidatos. Os três são artefato de fronteira de oração, pois a normalização suprime a pontuação:

| Detectado | Enunciado real |
|---|---|
| "foi nao ia dar certo" | "foi. Não ia dar certo" |
| "que esta nao podem ficar" | "que está, não podem ficar" |
| "ali nao ta nao vai atrapalhar" | "ali, não tá. Não vai atrapalhar" |

**O resultado, entretanto, confirma o dimensionamento em vez de contrariá-lo.** O cálculo do passo 4.2 prevê cerca de 2,4 ocorrências por hora de fala-alvo; com 0,25 h por estado, o valor esperado é inferior a uma ocorrência por estado. Zero está dentro do previsto, e é precisamente a situação que o cálculo descreve como não informativa: com esse volume, a ausência não distingue "não ocorre" de "não foi amostrado".

A meta de 4,1 h de fala-alvo por estado ganha, assim, apoio empírico.

### 4.2 Léxico regional: ausente, com armadilha de homografia

Nenhuma ocorrência de `oxe`, `oxente`, `arretado`, `aperreado`, `avexado` em 1,55 h de fala regional.

A única ocorrência aparente, no Ceará, é falsa:

> "se você **visse** as imagens"

Trata-se do imperfeito do subjuntivo de *ver*, não do marcador discursivo recifense. São a mesma sequência gráfica.

**Duas consequências, ambas graves.**

A primeira atinge Pernambuco especificamente: *visse?* era a proposta de marcador para o estado que já se encontrava sem marcador morfossintático próprio (`docs/pares_minimos_v1.md`, seção 6). Um detector que não distinga o homógrafo registrará o marcador em qualquer variedade, inclusive no grupo de controle.

A segunda é mais ampla: o Bloco B do instrumento, e parte do Bloco C, apoiam-se em itens lexicais que não compareceram. O volume examinado é pequeno demais para reprovar os itens, mas é suficiente para estabelecer que a frequência é baixa o bastante para que a confirmação exija volume consideravelmente maior que o previsto para os marcadores morfossintáticos.

No grupo de controle registrou-se uma ocorrência legítima de *maneiro*, no Rio de Janeiro.

### 4.3 Consequência metodológica

**A detecção por expressão regular não é adequada ao Filtro 2.** Contabiliza "que não" como negação pós-verbal, "ele vai" como imperativo e o subjuntivo de *ver* como marcador do Recife. Todos os três erros inflam a contagem, e o fazem de modo assimétrico entre marcadores.

A detecção precisa operar sobre texto com pontuação preservada e com análise morfossintática que distinga imperativo de presente do indicativo e identifique a fronteira de oração.

## 5. Observação operacional

Um vídeo do plano tornou-se indisponível entre o planejamento e a coleta — 17 de 18 obtidos. Não é bloqueio nem defeito de configuração, mas rotatividade ordinária da plataforma. Em coleta de dezenas de horas o fenômeno será recorrente, e reforça a necessidade de contabilizar perdas por estado e camada, conforme `docs/pendencias.md`, seção 4.5.

---

## Síntese

| Suposição | Situação |
|---|---|
| Rendimento de 35% em vox-pop | Subestimada; medido 92,3% de fala, ~47% de fala-alvo |
| Rendimento de 60% em podcast | Subestimada; medido 89,2% |
| Rendimento de 70% em vlog | **Confirmada**; medido 81,0%, ~68% de fala-alvo |
| Diarização separa morador e repórter | **Sustentada**; 4,2 locutores por arquivo em vox-pop |
| Transcrição penaliza fala nordestina | **Não corroborada**; diferença de +0,010 a favor do Nordeste |
| Negação pós-verbal exige volume alto | **Confirmada**; zero ocorrências em volume abaixo do dimensionado |
| Léxico regional ocorre em fala espontânea | **Não corroborada**; nenhuma ocorrência em 1,55 h |


---

# Adendo — segundo lote, 28/08/2026

**Material:** 52 registros, 5,52 h, cerca de 0,92 h por estado. Distribuição: CE 10, PB 10, PE 9, RJ 9, BA 7, SP 7. Triplica o volume do primeiro lote e permite distinguir raridade de ausência.

## A.1 Rendimento — estável

| Camada | n | Fala / duração | Primeiro lote | Suposto | Dominante |
|---|---|---|---|---|---|
| `entrevista_vox_pop` | 21 | 91,8% | 92,3% | 35% | 51,0% |
| `podcast_radio_tv_regional` | 20 | 87,3% | 89,2% | 60% | 73,0% |
| `vlog_amador` | 11 | 85,1% | 81,0% | 70% | 83,0% |

As medidas mantêm-se com o triplo do material, o que eleva a confiança na revisão da meta de volume. As suposições permanecem pessimistas por larga margem, exceto a do vlog.

## A.2 Confiança de transcrição — a diferença entre grupos desaparece

| Estado | Palavras | Confiança | Primeiro lote |
|---|---|---|---|
| PB | 9.069 | 0,947 | 0,941 |
| PE | 5.681 | 0,948 | 0,975 |
| CE | 7.192 | 0,944 | 0,961 |
| BA | 8.205 | 0,940 | 0,904 |
| SP | 7.554 | 0,948 | 0,953 |
| RJ | 7.431 | 0,929 | 0,898 |

**Nordeste 0,944; Sudeste 0,939; diferença +0,006.**

A dispersão entre estados, que no primeiro lote ia de 0,898 a 0,975, reduziu-se a 0,929–0,948. A variação anterior era ruído de amostra pequena; com 45 mil palavras os estados convergem, e o Rio de Janeiro permanece como o menor valor.

Reforça-se a leitura preliminar: **não há indício de que o reconhecimento penalize a fala nordestina.** Segue valendo que confiança não é WER, e que a verificação definitiva exige transcrição humana de referência.

## A.3 Léxico regional — assimetria entre grupos, e ela é decisiva

Todas as ocorrências foram inspecionadas individualmente. Dois homógrafos foram excluídos da contagem:

- ***visse*** — "se você **visse** as imagens" é o imperfeito do subjuntivo de *ver*, não o marcador discursivo recifense.
- ***da hora*** — "os pacotinhos **da hora** e da roça", no Ceará, é a expressão literal, não a gíria paulistana.

Contagem após inspeção:

| Grupo | Ocorrências | Palavras | Taxa |
|---|---|---|---|
| Nordeste | **0** | 29.999 | 0,00 por 10 mil |
| Sudeste | 5 | 14.934 | 3,35 por 10 mil |

As ocorrências sudestinas são *mano* (3, em vlog de São Paulo), *maneiro* (1, em rádio e TV do Rio) e *caraca* (1, em vox-pop do Rio).

**O resultado não se explica por composição de camadas.** As ocorrências sudestinas distribuem-se pelas três camadas, e não se concentram no vlog. Na camada de vlog isoladamente, o Nordeste dispõe de **mais** material — 7.917 palavras contra 5.338 — e registra zero ocorrências, contra três do Sudeste.

Sob a hipótese de taxas iguais, esperar-se-iam cerca de 10 ocorrências no material nordestino. A probabilidade de observar zero é da ordem de 4×10⁻⁵.

### O que isso autoriza e o que não autoriza afirmar

**Autoriza:** neste corpus, os itens lexicais nordestinos do instrumento não ocorrem, ao passo que os itens sudestinos ocorrem, e a diferença de taxa é improvável sob a hipótese de igualdade.

**Não autoriza:** afirmar que falantes nordestinos não empregam léxico regional. Os itens foram escolhidos sem evidência de frequência, e as duas listas não são equivalentes em natureza — a sudestina reúne gíria urbana corrente, a nordestina reúne itens possivelmente restritos a registros ou faixas etárias que o corpus não amostra. **O achado é sobre os itens do instrumento, não sobre os falantes.**

### Consequência para o Bloco B

A conduta (a) da seção 8 de `docs/pares_minimos_v1.md` — manter o bloco declarando a fragilidade — **deixa de ser sustentável**. O problema não é o bloco ser fraco, e sim ser **assimétrico**: contrastaria itens sudestinos que ocorrem em fala real contra itens nordestinos que não ocorrem. Isso não é *matched-guise* — é opor fala atestada a fala construída, e no eixo exato que o estudo mede.

Um efeito medido nessas condições seria indistinguível do artefato de um lado do contraste ser artificial.

Restam as condutas (b), substituir os itens por outros de frequência atestada, e (c), reduzir o peso do bloco e reposicionar o instrumento sobre a morfossintaxe.
