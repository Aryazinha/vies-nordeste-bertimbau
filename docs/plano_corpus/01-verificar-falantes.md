# Etapa 1 — Quantos falantes distintos há no corpus

**Objetivo.** Apurar quantas **pessoas diferentes** estão nos 52 arquivos já coletados, por estado, e compará-lo ao piso de 20 por estado. É o que decide se a coleta está concluída ou quanto falta.

**Estado:** comparação e conferência humana concluídas em 10/09/2026. **O piso de 20 falantes distintos está atingido em todos os estados.** O teto de 5% por falante, de que o piso deriva, **não** é satisfeito pelo material tal como coletado — ver a seção 7.1, que registra a medição e a decisão, tomada na mesma data, de tratar o teto como condição de conclusão. Por esse critério a coleta não está concluída, e a etapa 2 é necessária. **Onde roda:** Google Colab, com GPU, mais uma etapa de conferência humana que não exige GPU.

**Leia antes:** [`README.md`](README.md) desta pasta, para saber por que esta etapa vem antes de coletar mais.

---

## 1. O problema que a etapa resolve

A diarização atribui rótulos de locutor **dentro** de cada arquivo — `SPEAKER_00`, `SPEAKER_01`. Esses rótulos não têm relação alguma entre arquivos distintos: o repórter que aparece em cinco episódios do mesmo canal recebe cinco rótulos diferentes e é contado como cinco pessoas.

O teto de 5% por falante, fixado em `docs/fontes_coleta.md` (2.4.5), exige por aritmética **20 falantes distintos por estado**. Sem saber quantos há de fato, não é possível afirmar que o piso foi atingido — apenas que o volume de áudio provavelmente basta.

---

## 2. A ferramenta

`pipeline_coleta_piloto/verificar_reincidencia.py`, já escrito e nunca executado.

**Método.** Extrai um *embedding* de locutor — vetor que resume as características de uma voz — para cada rótulo com fala suficiente, usando `pyannote/embedding`. Compara todos os pares de vozes do mesmo estado por similaridade de cosseno. Pares acima do limiar são **candidatos** a mesma pessoa.

**O que ele não faz, e a razão.** Não decide. Devolve uma lista para revisão humana, porque os dois erros possíveis são graves e assimétricos: fundir dois rótulos por engano **apaga uma pessoa real** do corpus; deixar de fundir dois rótulos da mesma pessoa **viola o teto** sem que ninguém perceba. Nenhum dos dois pode ocorrer em silêncio.

**Parâmetros a calibrar:**

- `LIMIAR_SIMILARIDADE = 0.75` — ponto de partida conservador, **não validado**. Deve ser calibrado contra uma amostra conferida à mão antes de se confiar na lista.
- `DURACAO_MINIMA_S = 8.0` — abaixo disso a voz não dá sinal confiável. Rótulos com menos fala ficam **fora da comparação**, e devem aparecer no relatório como "sem embedding", nunca como "diferente de todos".
- `DURACAO_ALVO_S = 30.0` — acrescentado em 02/09/2026. O mínimo acima é critério de admissão, não de qualidade: um rótulo com cem segundos de fala não tem por que ser resumido em oito. A mediana de áudio por rótulo passou de 8,6 s para 33,6 s, sem alteração alguma na contagem de rótulos admitidos.
- `LIMIAR_REGISTRO = 0.50` — acrescentado em 02/09/2026. Piso abaixo do qual um par nem sequer é gravado. Não é limiar de decisão: pares entre 0,50 e o limiar são gravados marcados como abaixo dele, para que a calibração descrita na seção 6 possa ser feita sobre a mesma execução, sem nova passagem de GPU.

---

## 3. A pasta vazia — resolvido em 02/09/2026

O script lia os registros de `FINAL_DIR`, isto é, `pipeline_coleta_piloto/dataset_raw/registros_finais/`, **que está vazia**. Os registros com diarização existem em dois outros lugares:

- `pipeline_coleta_piloto/dataset_raw/registros_anonimizados/` — 52 arquivos, já anonimizados
- `piloto_resultados (2).zip`, na raiz do projeto — 52 arquivos, **não anonimizados**

**Adotada a segunda das duas saídas previstas:** o script ganhou o parâmetro `--registros`. Copiar os arquivos para `registros_finais/` resolveria a rodada corrente e reapresentaria o problema a cada nova rodada da etapa 2; o parâmetro o resolve de uma vez. Se a pasta indicada não contiver nenhum JSON, o script agora interrompe com mensagem que nomeia a pasta correta, em vez de comparar zero arquivos e relatar zero pares — que era a falha silenciosa possível.

Usam-se os **anonimizados**: têm o mesmo campo `diarizacao` e o mesmo `arquivo`, e manipular material já anonimizado é preferível sempre que o resultado não dependa dos nomes — e aqui não depende, porque a comparação é de voz, não de texto.

### 3.1 Segunda correção, encontrada na preparação

O script acumulava turnos até somar `DURACAO_MINIMA_S`, mas calculava o embedding **apenas sobre o turno mais longo** daquele rótulo. Conferido contra os 52 registros: dos 154 rótulos que alcançam 8 s de fala, **16 só os alcançam somando turnos**, e nesses o turno isolado mais longo é menor que o mínimo declarado. O embedding sairia de menos áudio do que o próprio critério exige, sem que nada no relatório o indicasse — e rótulo de fala fragmentada é justamente o do entrevistado de rua, não o do repórter, de modo que o erro recairia sobre o grupo que mais importa contar.

O script passa a concatenar os turnos escolhidos numa única forma de onda antes de extrair o embedding.

---

## 4. Preparação do ambiente

**O que subir ao Drive:**

| O quê | Onde está | Tamanho |
|---|---|---|
| 52 arquivos `.wav` | `dataset_raw/audio/` | 607 MB |
| 52 registros com diarização | `dataset_raw/registros_anonimizados/` | pequeno |

**Credencial.** `pyannote/embedding` é modelo de acesso condicionado. São três passos, e o segundo é o mais esquecido:

1. Criar conta em `huggingface.co`
2. Acessar a página do modelo e **aceitar os termos**, no botão *Agree and access repository*. Sem isso o token é válido mas o download é recusado, com erro que não menciona a causa
3. Gerar token de leitura e cadastrá-lo no Colab como segredo `HF_TOKEN` — nunca colado em célula, porque o notebook é versionado

**GPU.** Ativar antes de executar qualquer célula: *Ambiente de execução* → *Alterar o tipo de ambiente* → **T4 GPU**. A troca reinicia o ambiente.

**Restrição de versão.** O notebook do projeto fixa `numpy<2.3`, e o motivo é sutil: sem a restrição, a instalação traz `numpy` mais novo do que o `numba` aceita, e o `numba` entra por baixo do `pyannote`, via `librosa`. O conflito se manifesta **apenas na diarização** — isto é, depois de todo o resto já ter rodado. Ver `notebooks/README.md`.

---

## 5. Execução

O caminho recomendado é o notebook `notebooks/verificar_falantes_colab.ipynb`, criado em 02/09/2026 para esta etapa. Ele executa as seções 4 a 7 deste documento, e a sua seção 7 instrumenta a conferência humana, tocando os dois trechos de cada par candidato — sem isso, o revisor teria de localizar os tempos à mão em 607 MB de áudio.

Pela linha de comando, o equivalente é:

```bash
python verificar_reincidencia.py --estado todos \
    --registros dataset_raw/registros_anonimizados
```

`--estado` aceita agora `todos`, o que carrega o modelo uma única vez para os seis estados. A comparação continua interna a cada estado: um falante do Recife e outro de São Paulo não disputam o mesmo teto.

Saída: `dataset_raw/diarizacao/reincidencia_{estado}.json`, mais um `reincidencia_resumo.json` agregado. Cada relatório traz o resumo do estado, a lista de rótulos com o áudio efetivamente usado, **a lista dos rótulos sem embedding** — exigida pela seção 7 — e os pares ordenados por similaridade decrescente, cada um com os dois arquivos, os dois rótulos, os canais, os tempos dos trechos comparados e um campo `veredito_humano` a preencher.

---

## 5.1 Comparação executada — 02/09/2026

Executada no Colab, sobre os 52 registros anonimizados, com limiar de 0,75 e piso de registro de 0,50.

| UF | Arquivos | Rótulos com embedding | Sem embedding | Pares acima de 0,75 | Margem sobre o piso |
|---|---|---|---|---|---|
| PB | 10 | 30 | 2 | 5 | +10 |
| PE | 9 | 28 | 1 | 1 | +8 |
| CE | 10 | 23 | 4 | 1 | +3 |
| BA | 7 | 22 | 3 | 0 | +2 |
| SP | 7 | 21 | 2 | 0 | +1 |
| RJ | 9 | 30 | 5 | 0 | +10 |
| **Total** | **52** | **154** | **17** | **7** | — |

A contagem de rótulos reproduz exatamente a tabela do `README.md` desta pasta, o que confirma que a comparação leu todo o corpus.

**Leitura preliminar, e ela é condicional.** Sete pares candidatos em 154 rótulos. Ainda que todos os sete se confirmem na conferência, e ainda que nenhum deles seja transitivo, nenhum estado cai abaixo do piso: o pior caso é PB com 25 e CE com 22. **Isso não encerra a etapa**, por dois motivos que a conferência precisa resolver:

1. **O limiar de 0,75 não está calibrado**, e o erro que importa aqui é o falso negativo. Um limiar alto demais deixa fusões reais fora da lista, e o efeito seria subestimar a reincidência exatamente onde não há folga para absorvê-la.
2. **A margem é muito desigual entre estados.** SP suporta **uma** fusão antes de cair abaixo de 20, BA duas e CE três; PB, PE e RJ não mudam de conclusão. A escuta deve, portanto, descer bem abaixo do limiar em SP, BA e CE, e pode parar cedo nos outros três — a mesma varredura não serve para os seis.

### 5.2 Distribuição por faixa de similaridade, e correção da leitura acima

Pares por faixa, em contagem cumulativa — a coluna ">0,70" inclui os pares de ">0,75":

| UF | Margem | >0,90 | >0,85 | >0,80 | >0,75 | >0,70 | >0,65 | >0,60 | >0,55 | >0,50 |
|---|---|---|---|---|---|---|---|---|---|---|
| PB | +10 | 2 | 3 | 4 | 5 | 5 | 5 | 5 | 5 | 6 |
| PE | +8 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| CE | +3 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| BA | +2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SP | +1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| RJ | +10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**A distribuição é bimodal, e isso responde à preocupação com o limiar.** Os pares estão acima de 0,80 ou abaixo de 0,50; entre 0,55 e 0,75 não há um único par em estado algum. Nessa faixa vazia, qualquer limiar escolhido produz a mesma lista, de modo que a calibração deixa de ser decisiva para o resultado. A conferência humana reduz-se a **oito pares no total**, todos os pares registrados.

**Correção de uma leitura desta mesma data.** Na seção 5.1 afirmou-se, numa primeira redação, que a ausência de candidatos em SP, BA e RJ indicaria limiar alto demais, por serem "os estados com menos arquivos por canal, onde a reincidência deveria aparecer". O raciocínio estava invertido: menos arquivos por canal significa **menos** oportunidade de o mesmo apresentador reaparecer, e não mais. A contagem por canal o confirma:

| UF | Arquivos | Canais | Canais com dois ou mais arquivos |
|---|---|---|---|
| PB | 10 | 6 | 3 |
| PE | 9 | 5 | 4 |
| CE | 10 | 6 | 3 |
| BA | 7 | 6 | 1 |
| SP | 7 | 6 | 1 |
| RJ | 9 | 6 | 3 |

BA e SP têm, cada um, um único canal com mais de um arquivo, e zero candidato é o esperado. E a hipótese de limiar alto fica refutada pela tabela de faixas: mesmo a 0,50, nenhum par aparece nesses estados.

**O que a tabela não descarta.** Ela afasta o limiar como causa da ausência, mas não o outro modo de falha do método: uma mesma voz, em condições de gravação muito diferentes, pode ficar abaixo de 0,50 e escapar por inteiro. O caso mais exposto é RJ, que tem três canais com mais de um arquivo e nenhum par. A verificação correspondente é ouvir, em cada canal com mais de um arquivo, o rótulo de maior fala de cada arquivo contra o do outro — comparação que independe do limiar, e por isso alcança o que ele não alcança. Implementada na seção 7.2 do notebook, em 12/09/2026.

Ela **não se restringe a BA, SP e RJ**: o rótulo de maior fala de um arquivo nem sempre é o que a comparação automática pareou, e por isso há pares de mesmo canal não conferidos também nos demais estados. São dezenove ao todo — PB 5, CE 5, PE 4, RJ 3, BA 1, SP 1 —, e **os de PB decidem mais que os outros**: o estado está exatamente no piso, de modo que uma única fusão confirmada ali o retira da condição de único estado sem déficit. Nos estados que já têm déficit, cada fusão confirmada apenas o aumenta em uma pessoa.

**Os 17 rótulos sem embedding** ficam fora da conferência e continuam desconhecidos, nem verificados nem descartados. Sua distribuição é desigual — RJ tem 5 e CE 4, contra 1 em PE —, e o número limita o que se pode afirmar sobre a contagem final de cada estado.

---

## 6. Conferência humana, que é a parte que decide

Para cada par candidato, ouvir os dois trechos e responder: **é a mesma pessoa?**

Ordem sugerida: começar pelos de similaridade mais alta, que devem ser fusões óbvias, e descer até onde os pares deixarem de ser plausíveis. O ponto em que isso ocorre **é a calibração empírica do limiar**, e deve ser registrado — vale mais que o valor default de 0,75.

Atenção ao padrão esperado: o repórter ou apresentador do canal é quem mais reaparece. Pares dentro do **mesmo canal** são os candidatos mais prováveis; entre canais diferentes, muito menos.

### 6.1 Regra para o par duvidoso

**Na dúvida, registra-se como mesma pessoa, com a nota `incerto`** — `marcar(uf, i, True, "incerto")`.

A regra é conservadora nas duas verificações que a contagem sustenta, e na mesma direção. Para o **piso de 20 por estado**, fundir reduz a contagem, de modo que um estado que permaneça acima do piso com as fusões duvidosas permanece acima dele qualquer que seja a verdade. Para o **teto de 5% por falante**, fundir soma a fala dos dois rótulos numa só pessoa, o que torna a verificação do teto mais exigente, e não menos. Registrar como pessoas distintas, ao contrário, poderia deixar passar em silêncio precisamente a violação que esta etapa existe para detectar.

O custo da regra é o erro oposto — apagar da contagem uma pessoa que existe —, e ele é aceitável aqui porque é visível: a nota `incerto` permite reportar quantas fusões foram duvidosas e recalcular a contagem sem elas, apresentando o intervalo em vez de um número único.

No corpus de 02/09/2026 a regra não altera a conclusão sobre o piso: os oito pares estão em PB, PE e CE, e mesmo a fusão de todos deixa os três estados acima de 20.

---

## 7. Apuração e critério de conclusão

Feita a conferência, o número de falantes distintos por estado é:

```
rótulos com fala ≥ 8s  −  fusões confirmadas
```

**Com uma ressalva de aritmética**, incorporada à seção 8 do notebook: a subtração só vale enquanto cada fusão confirmada envolver rótulos ainda não fundidos. Se os rótulos A e B são a mesma pessoa, e B e C também, os três pares que a conferência pode confirmar descrevem **uma** pessoa, e subtrair três apagaria duas pessoas que existem. O notebook agrupa os rótulos em componentes conexos, o que dá a contagem correta qualquer que seja o número de pares confirmados sobre a mesma voz — e o caso é esperado, não hipotético: é exatamente o do apresentador que reaparece em vários episódios do canal.

Comparar ao piso de 20. O teto de partida está no `README.md` desta pasta: PB 30, RJ 30, PE 28, CE 23, BA 22, SP 21.

| Resultado | Encaminhamento |
|---|---|
| Todos os estados ≥ 20 | Coleta concluída. Ir para a etapa 3 |
| Algum estado < 20 | Ir para a etapa 2, com o déficit por estado apurado |

**Registrar também os rótulos excluídos por terem menos de 8 segundos de fala.** Eles não são falantes verificados nem descartados: são desconhecidos, e o número deles limita o que se pode afirmar.

### 7.1 Resultado — 10/09/2026

**Conferência humana.** Oito pares conferidos — todos os registrados acima do piso de 0,50 —, com seis fusões efetivas, apuradas por componentes conexos.

| UF | Rótulos comparáveis | Fusões | Falantes distintos | Piso | Situação | Sem embedding |
|---|---|---|---|---|---|---|
| PB | 30 | 4 | 26 | 20 | atingido | 2 |
| PE | 28 | 1 | 27 | 20 | atingido | 1 |
| CE | 23 | 1 | 22 | 20 | atingido | 4 |
| BA | 22 | 0 | 22 | 20 | atingido | 3 |
| SP | 21 | 0 | 21 | 20 | atingido | 2 |
| RJ | 30 | 0 | 30 | 20 | atingido | 5 |
| **Total** | **154** | **6** | **148** | **120** | — | **17** |

**Composição dos vereditos — 12/09/2026.** Dos oito pares, **sete foram confirmados como mesma pessoa e um foi rejeitado**; nenhum recebeu a nota `incerto`. Os sete confirmados são todos do **mesmo canal**, com similaridade de 0,7713 a 0,9259; o rejeitado tem 0,5081 e é de canais distintos. As cinco confirmações de PB produziram quatro fusões, porque uma delas incidia sobre voz já fundida — o caso transitivo que a apuração por componentes conexos prevê.

**O limiar não pôde ser calibrado por baixo, e a razão está na própria distribuição.** A fronteira empírica se encontra entre 0,5081, rejeitado, e 0,7713, confirmado, e nesse intervalo não existe um único par no corpus, como já mostrava a tabela de faixas da seção 5.2. O valor de 0,75 é, portanto, **compatível** com a conferência, e não validado por ela: qualquer limiar entre 0,52 e 0,77 teria produzido a mesma lista e as mesmas seis fusões. O que a conferência estabelece é mais estreito, e mais útil para as próximas rodadas: **acima de 0,77, sete de sete pares eram a mesma pessoa, e todos os sete eram do mesmo canal** — o sinal de canal acompanhou integralmente o sinal de voz.

Pelo critério da seção 7, a coleta estaria concluída. **Esse critério, contudo, é incompleto**, e a incompletude só se tornou visível com a contagem em mãos.

#### O teto que o piso não garante

O piso de 20 deriva do teto de 5% por aritmética: com menos de 20 pessoas, alguma responde necessariamente por mais de 5% da fala do estado. **A recíproca não vale.** Vinte pessoas satisfazem o teto somente se a fala se distribuir entre elas de modo suficientemente uniforme — e nos formatos que compõem o corpus ela não se distribui, porque apresentador e repórter falam muito mais que o entrevistado.

Medição por `pipeline_coleta_piloto/verificar_teto_falante.py`, **sem aplicar as fusões**. Cada rótulo conta como uma pessoa, inclusive os de menos de 8 s, o que torna os números **limite inferior da violação**: fundir rótulos da mesma pessoa só aumenta a participação dela.

| UF | Pessoas | Acima do teto | Maior participação | Fala bruta | Com o teto aplicado | Conservado | Fatia máxima por pessoa | Pessoas com ≥ 0,7 min após o recorte |
|---|---|---|---|---|---|---|---|---|
| PB | 32 | 7 | 12,8% | 57,8 min | 34,2 min | 59% | 1,71 min | 21 |
| PE | 29 | 5 | 15,0% | 35,6 min | 22,6 min | 64% | 1,13 min | 18 |
| CE | 27 | 9 | 14,6% | 44,7 min | 13,2 min | 30% | 0,66 min | 0 |
| BA | 25 | 6 | 20,5% | 47,3 min | 11,9 min | 25% | 0,60 min | 0 |
| SP | 23 | 5 | 17,0% | 47,7 min | 6,6 min | 14% | 0,33 min | 0 |
| RJ | 35 | 5 | 19,6% | 43,8 min | 19,2 min | 44% | 0,96 min | 14 |
| **Total** | **171** | **37** | — | **4,61 h** | **1,80 h** | **39%** | — | — |

"Com o teto aplicado" é o maior volume que o estado conserva quando cada pessoa é recortada a 5% desse mesmo volume. A última coluna combina o teto com o segundo piso de `experimentos/resultados/tabelas/meta_corpus_autonomo.md` — 0,7 minuto de fala por falante, o necessário para dez contextos de palatalização — e conta as pessoas que ainda o alcançam depois do recorte. É uma construção desta seção, e não um critério previamente fixado; mas é o número que precisaria chegar a 20 para que o corpus recortado sirva ao marcador de áudio para o qual o segundo piso foi definido.

**Leitura.**

1. **A violação é geral, e não marginal.** Todos os estados têm entre 5 e 9 pessoas acima do teto, e elas concentram de 46,6% a 71,5% da fala. É consequência estrutural do formato — telejornal, rádio, podcast —, e não acidente de algum arquivo.
2. **Com o teto aplicado por recorte, apenas PB conserva 20 pessoas com fala suficiente**, e por margem de uma. PE e RJ ficam perto; CE, BA e SP ficam em zero, porque a fatia máxima por pessoa cai abaixo de 0,7 minuto. O zero de CE é, contudo, sensível ao parâmetro: sua fatia é de 0,66 minuto, e um segundo piso ligeiramente menor o mudaria por inteiro.
3. **As fusões agravam o quadro**, como se previa — ver a tabela final logo abaixo, que as aplica e substitui os números deste bloco.
4. **O recorte é uma interpretação operacional do teto, e não a única.** A regra fixa o limite, mas não diz se ele se cumpre descartando fala excedente ou coletando mais pessoas. As duas vias apontam, porém, para a mesma falta: pessoas distintas com fala equilibrada, e não horas.

#### Números finais, com as seis fusões aplicadas — 12/09/2026

`verificar_teto_falante.py --registros dataset_raw/registros_anonimizados --vereditos dataset_raw/diarizacao/vereditos_reincidencia.json`. **É esta a tabela a citar**; a anterior, sem fusões, fica como limite inferior.

| UF | Pessoas | Fusões | Acima do teto | Com o teto aplicado | Fatia máxima por pessoa | Pessoas úteis | Faltam |
|---|---|---|---|---|---|---|---|
| PB | 28 | 4 | 9 | 29,3 min | 1,46 min | 20 | 0 |
| PE | 28 | 1 | 6 | 19,8 min | 0,99 min | 17 | 3 |
| CE | 26 | 1 | 10 | 11,1 min | 0,56 min | 0 | 5 |
| BA | 25 | 0 | 6 | 11,9 min | 0,60 min | 0 | 5 |
| SP | 23 | 0 | 5 | 6,6 min | 0,33 min | 0 | 8 |
| RJ | 35 | 0 | 5 | 19,2 min | 0,96 min | 14 | 6 |
| **Total** | **165** | **6** | **41** | **97,9 min** | — | — | **27** |

As fusões produziram o efeito antecipado: **PB perdeu uma pessoa útil e ficou exatamente no piso, com 20 e margem nula**, e PE passou de duas pessoas novas a três. O déficit total sobe de 26 para 27, e a fala admissível sob o teto cai de 1,80 h para 1,63 h.

**Sensibilidade ao valor do teto**, na mesma medição: a 10% o piso cai a 10 pessoas e nenhum estado tem déficit; a 5%, faltam 27; a 3%, o piso sobe a 34 e faltam 111. A escolha do valor decide, sozinha, entre corpus concluído e coleta quatro vezes maior que a prevista — razão pela qual a ressalva sobre a origem do número, registrada adiante, precisa ser resolvida antes da etapa 2, e não depois.

**Decisão tomada em 10/09/2026: o teto é condição de conclusão.** Das duas leituras possíveis — manter o critério da seção 7, que conta apenas falantes distintos, ou exigir o teto —, adotou-se a segunda, que é a coerente com `meta_corpus_autonomo.md`, onde o teto figura como "a única regra de que a meta inteira deriva". O critério da seção 7 fica substituído, para esta e para as próximas rodadas, por: **20 pessoas por estado que conservem o segundo piso de fala depois do recorte pelo teto.** A etapa 2 torna-se necessária, com o déficit registrado em [`02-completar-coleta.md`](02-completar-coleta.md).

**Ressalva sobre o valor do teto, registrada na mesma data.** A decisão adota o teto de 5% tal como fixado, mas **o valor não tem justificativa escrita no projeto**. A razão para haver um teto está documentada — sem ele, uma pessoa loquaz poderia responder pela maior parte da fala de um estado, e o corpus representaria um idioleto, e não uma variedade (`docs/pendencias.md`, decisão de 31/08/2026) —, mas nada fundamenta 5% contra 3% ou 10%. A origem citada em toda a documentação, `docs/fontes_coleta.md` §2.4.5, não contém o teto: trata do rendimento da camada de vlogs. A frase que o enuncia, introduzida na revisão v1.7, remete a um item que não o estabelece. E o valor não é detalhe: o piso de pessoas é o seu inverso — 20 a 5%, 10 a 10%, 34 a 3% —, de modo que ele determina diretamente quanto falta coletar.

---

## 8. Ao terminar

1. Atualizar este documento com os números apurados, o limiar calibrado e a data.
2. Atualizar `docs/dataset-spec.md` — a seção "Camada de execução, em números" afirma que a verificação nunca rodou.
3. Atualizar `docs/pendencias.md`, seção 6.4, e o item #5 do registro de pendentes.
4. Se houver déficit, anotá-lo por estado em [`02-completar-coleta.md`](02-completar-coleta.md), que é o insumo daquela etapa.

Uma etapa concluída cujo resultado só existe no histórico da conversa está perdida.
