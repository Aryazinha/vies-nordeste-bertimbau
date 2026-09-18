# Etapa 3 — Validar o corpus

**Objetivo.** Produzir as três medidas que sustentam as afirmações que o artigo fará sobre o corpus. Sem elas, o conjunto existe mas não é defensável.

**Estado:** não iniciada. **Pré-requisito: satisfeito em 14/09/2026** — o corpus está estável, com 83 arquivos, 7,96 h e 216 falantes distintos, e as etapas 1 e 2 estão encerradas. As amostras desta etapa são extraídas do corpus final; extraí-las antes obrigaria a refazê-las.

---

## Situação em 14/09/2026, por frente

A equipe optou, nessa data, por trabalhar primeiro no conjunto de pares mínimos, que corre em paralelo e não depende do áudio. Esta seção registra o que fica pendente aqui, para que a etapa possa ser retomada sem o histórico da conversa em que foi levantada.

| Frente | O que existe | O que falta | Trabalho humano |
|---|---|---|---|
| 3.1 WER estratificado | ferramenta pronta; **amostra refeita em blocos em 17/09/2026** | transcrever à mão | 8 a 16 h |
| 3.2 Coerência dialetal | **concluída em 17/09/2026** | — | feito |

### Amostras geradas em 15/09/2026

Ambas na máquina local, sobre os 83 registros anonimizados, e gravadas em `pipeline_coleta_piloto/dataset_raw/`, fora do versionamento, por conterem transcrição ou apontarem para ela. Nos 31 registros cujo original está disponível localmente, os tempos, a diarização e o texto de todos os segmentos sem máscara coincidem com o original (1.665 segmentos comparados, nenhuma divergência).

**Amostra do WER** (`amostra_wer.json`, gerada por `preparar_amostra_wer.py`). Reproduz a lógica da seção 6.4 do notebook — trechos de pelo menos 5 s, semente 20260827, acumulação até 20 minutos por estado —, com uma diferença decidida pela equipe: **trechos com nome mascarado ficam fora do sorteio**, porque a transcrição manual registra o nome pronunciado e o cálculo contaria a máscara como erro do reconhecedor. Cada trecho recebe código estável (`PB-001`…).

| UF | Trechos | Minutos | Arquivos | Vox-pop | Rádio/TV/podcast | Vlog | Excluídos com máscara |
|---|---|---|---|---|---|---|---|
| PB | 143 | 20,1 | 13 | 8,3 | 6,9 | 4,8 | 20 (3,1 min) |
| PE | 154 | 20,0 | 11 | 11,3 | 6,2 | 2,5 | 28 (4,6 min) |
| CE | 166 | 20,0 | 14 | 13,5 | 4,1 | 2,4 | 34 (5,4 min) |
| BA | 163 | 20,2 | 11 | 6,5 | 11,2 | 2,4 | 27 (3,8 min) |
| SP | 152 | 20,2 | 13 | 5,7 | 10,3 | 4,2 | 17 (2,0 min) |
| RJ | 122 | 20,1 | 17 | 4,5 | 7,0 | 8,5 | 18 (2,5 min) |

Total: 900 trechos, 120,6 min, 79 dos 83 arquivos. **Esta amostra foi substituída em 17/09/2026** pela amostra em blocos descrita adiante; o quadro fica como registro. **A composição por camada difere entre estados**, porque o sorteio, tal como na seção 6.4, não é estratificado por camada; o efeito sobre a comparação entre estados está registrado em `docs/pendencias.md` 4.11.

**Amostra de coerência dialetal** (`diarizacao/coerencia_{UF}.json`, gerada por `preparar_amostra_coerencia.py`). O script foi revisto antes da execução em dois pontos: passou a ler os registros anonimizados, pois a pasta de registros originais contém apenas 31 dos 83 arquivos na máquina local; e passou a sortear **pessoas**, fundindo os rótulos de diarização confirmados como mesma pessoa na conferência de reincidência (`vereditos_reincidencia.json`), pela mesma função de `verificar_teto_falante.py`. Sem a fusão, a amostra poderia conter a mesma pessoa duas vezes. Cada pessoa recebe código estável (`COE-PB-01`…).

| UF | Pessoas elegíveis (turno ≥ 8 s) | Amostradas | Arquivos | Canais | Duração média do segmento indicado | Escuta total |
|---|---|---|---|---|---|---|
| PB | 29 | 10 | 9 | 5 | 33,9 s | 5,7 min |
| PE | 30 | 10 | 9 | 7 | 28,6 s | 4,8 min |
| CE | 32 | 10 | 10 | 8 | 37,0 s | 6,2 min |
| BA | 27 | 10 | 7 | 6 | 30,7 s | 5,1 min |
| SP | 38 | 10 | 7 | 6 | 32,9 s | 5,5 min |
| RJ | 37 | 10 | 8 | 7 | 24,4 s | 4,1 min |

A escuta dos segmentos indicados soma cerca de 31 minutos, abaixo da estimativa de 1 h, que permanece como margem para ouvir além do segmento quando o trecho for insuficiente.
| 3.3 Participação de ouvinte | **concluída em 16/09/2026** | — | feito |

### 3.1 — a amostra precisa ser regerada

`amostra_wer.json` foi sorteado quando o corpus tinha 52 arquivos. O corpus tem 83, e os 31 acrescentados não podem ficar fora do sorteio: a amostra existe para medir o erro de transcrição **do corpus**, e uma amostra que ignora 37% dele mede outra coisa.

A seção 6.4 do notebook `notebooks/piloto_colab.ipynb` foi corrigida em 14/09/2026 justamente para isto — ela lia apenas o lote processado na sessão, e passou a ler o corpus inteiro do Drive. Regerar é rodar aquela seção; o custo é de minutos, e não exige GPU.

**Só depois vem o trabalho longo**, que é humano e indivisível por arquivo: ouvir e digitar. É também o item de maior valor isolado da etapa — WER estratificado por variedade é resultado publicável, e não controle de qualidade.

### 3.2 — pronta para executar, e agora roda na máquina local

`preparar_amostra_coerencia.py` exige o áudio, que no piloto só existia no ambiente de processamento. **Isso mudou:** o áudio dos 83 arquivos está na máquina local, de modo que a amostra pode ser gerada sem Colab, um estado por vez:

```bash
python preparar_amostra_coerencia.py --estado PE --n 10
```

O dimensionamento da seção 3.2 supunha 20 locutores por estado; hoje há entre 31 e 45, o que **melhora** o poder da amostra de 10, não o piora.

### 3.3 — duas escutas, e é a frente mais barata

O relatório rodou em 14/09/2026 sobre os 83 arquivos, com este resultado:

| UF | Arquivos | Fala de ouvinte medida | Arquivos de canal com o formato |
|---|---|---|---|
| PB | 13 | desconhecida | 0 |
| PE | 12 | desconhecida | 1 |
| CE | 15 | desconhecida | 0 |
| BA | 12 | desconhecida | 1 |
| SP | 14 | desconhecida | 0 |
| RJ | 17 | desconhecida | 0 |

**Os zeros de volume significam desconhecido, e não nulo** — nenhum arquivo foi verificado por escuta, e o campo `participacao_ouvinte` nasce `nao_verificado`. São **dois arquivos** a ouvir, um em PE e um na BA, e com isso a frente fica medida em vez de suposta.

### Resultado da escuta, 16/09/2026 — frente 3.3 concluída

Os dois arquivos foram ouvidos pela equipe, e o resultado gravado por `registrar_participacao.py`: na TV Aratu (BA, *Alô Juca*, 516 s), **43 s** de uma ouvinte ao telefone, entre 4:40 e 5:23, com o apresentador sozinho no restante; na Rádio Jornal (PE, *Super Manhã*, 176 s), **nenhuma** — a segunda voz que a diarização registrou é sobreposição do próprio apresentador.

O corpus tem, portanto, **43 segundos de fala de ouvinte no grupo nordestino (0,2% de 296 min) e nada no grupo de controle**. A assimetria é do sinal previsto, e é pequena demais para afetar qualquer comparação; a conduta adotada é declará-la na ficha do conjunto, sem descontar. O relatório dispara alerta de desequilíbrio porque o controle tem zero, sem consultar a magnitude — o alerta deve ser lido junto com o percentual da tabela (`docs/pendencias.md` 1.1). Antes da medida, `balanco_participacao.py` foi corrigido: contava a duração inteira do arquivo em vez dos segundos de fala de ouvinte, o que atribuiria 516 s à Bahia.

A assimetria permanece estrutural e conhecida: não há canais do formato em SP e RJ que satisfaçam a regra de atribuição, porque nas duas capitais os programas de participação pertencem a redes nacionais. Por isso a conduta é medir e descontar, não buscar equivalentes.

---

## Por que esta etapa não é formalidade

O projeto compara fala nordestina e fala do Sudeste. Cada uma das três medições abaixo existe para excluir uma explicação alternativa que, se não for excluída, derruba o resultado:

| Medição | A explicação alternativa que ela exclui |
|---|---|
| WER estratificado | "A diferença observada é erro do transcritor, não do modelo estudado" |
| Coerência dialetal | "Parte dos falantes ditos nordestinos migrou do Sudeste" |
| Participação de ouvinte | "O Nordeste foi gravado em situação mais informal que o controle" |

As três compartilham um traço: **o erro que produzem empurra o resultado na direção que favorece a hipótese do projeto.** É a pior direção para um viés passar despercebido, e a razão de nenhuma delas poder ser dispensada.

---

## 3.1 WER estratificado por variedade

**Adiado deliberadamente pela equipe em 31/08/2026.** Segue pendente por decisão, não por esquecimento.

**O que mede.** A taxa de erro da transcrição automática, **por estado**. Nunca só a média geral: o que importa é se o `faster-whisper` erra mais na fala nordestina que na sudestina. Se errar, a diferença medida entre as regiões seria viés de ferramenta apresentando-se como resultado sobre o modelo-alvo.

Medido corretamente, o WER estratificado é **resultado publicável por si só**, e não apenas controle de qualidade.

**O que existe.** O notebook gera `amostra_wer.json`, com até 20 minutos de trechos por estado, cada um trazendo `hipotese_asr` — o que o modelo transcreveu — e `referencia_manual` em branco. `pipeline_coleta_piloto/medir_wer.py` fecha a conta com a biblioteca `jiwer`, e informa quantos trechos ainda faltam preencher em vez de tratá-los como acerto.

**O que falta.** Trabalho humano: ouvir cada bloco e digitar o que foi dito, segundo as convenções fixadas em 17/09/2026 e reproduzidas abaixo.

### Teste de calibração, 17/09/2026, e o que ele corrigiu

Antes de iniciar as 8 a 16 horas de transcrição, dez trechos de seis estados foram transcritos por um membro da equipe e comparados com a saída do reconhecedor. O teste custou quinze minutos e alterou quatro pontos do procedimento. **Nenhum número dele é resultado:** sete blocos medidos não estimam WER de nada, e os valores não devem ser citados.

1. **Acentuação, maiúsculas e pontuação passam a ser ignoradas nos dois lados.** O `jiwer` não normaliza coisa alguma por conta própria — "Ele disse que sim." contra "ele disse que sim" divergia em 50%. Num bloco do teste, ignorar acento reduziu o erro medido de 0,27 para 0,07, diferença que era apenas acentuação não digitada por quem transcreve.
2. **A amostra foi refeita em blocos de cerca de 30 segundos.** As marcas de tempo por palavra do `faster-whisper` são aproximadas, e o recorte por segmento cortava a primeira e a última palavra ao meio: quem transcreve ouvia "crian", "soci", "priva", enquanto a hipótese trazia a palavra inteira. Em trechos de 17 palavras medianas, o artefato respondia por cerca de 12% de erro espúrio. Restringir a amostra a segmentos cercados de silêncio foi descartado com dado — apenas 6% dos segmentos elegíveis têm pausa de 0,4 s dos dois lados. A amostra vigente tem **241 blocos, 121,9 min, cerca de 40 blocos por estado**, sorteados com a semente 20260917, com 0,4 s de folga de cada lado no recorte do áudio.
3. **O resultado será reportado com e sem equivalências de fala reduzida** (decisão da equipe em 17/09/2026). O reconhecedor regulariza a ortografia — escreve *para* onde se disse *pra*, *está* onde se disse *tá* —, o que não é falha de compreensão; como as formas reduzidas podem ser mais frequentes numa variedade, contá-las como erro recairia sobre ela na direção que favorece a hipótese do projeto. A lista é curta e está declarada em `pipeline_coleta_piloto/normalizar_wer.py`; o teste mostrou que expansões ambiciosas pioram a medida.
4. **Blocos com trecho inaudível saem do cálculo principal**, e a frequência dessas marcas por estado é reportada à parte: ela mede o que o ouvinte humano não entendeu, não o que a máquina errou, e contá-la como erro puniria a máquina mais onde o áudio é pior.

### Convenções da transcrição manual, versão de 17/09/2026

- Escrever o que foi dito, sem corrigir gramática: *nós vai*, *os menino*.
- Preservar a forma falada na grafia: *tá*, *pra*, *cê*, *né*.
- Registrar repetição e gaguejo: *o o cara foi*.
- Não registrar ruído de hesitação sem forma de palavra ("ãh", "hum").
- Números por extenso, como falados; algarismos na hipótese são convertidos na normalização.
- Acento, maiúscula e pontuação são dispensáveis.
- Palavra incompreensível: `[?]`; bloco incompreensível: `[inaudível]`.
- **Transcrever tudo o que for falado no bloco, por qualquer voz.** A medida é da transcrição do áudio, e não de um falante: a hipótese do reconhecedor cobre o trecho inteiro, de modo que transcrever apenas o falante principal produziria omissões que seriam contadas como erro da máquina. A regra contrária, herdada da escuta de coerência dialetal, vigorou por engano no primeiro lote de 17/09/2026 e foi corrigida no mesmo dia.
- **Grafia padrão para a mesma palavra; forma gramatical como foi dita.** Pronúncia regional não se escreve foneticamente: quem ouve *nu combati* escreve *no combate*, quem ouve *homi* escreve *homem*, quem ouve *combustivis* escreve *combustíveis*. Já a variação de forma permanece: *nós vai*, *os menino*, *tá*, *pra*, *cê*. A razão é de validade: a fala nordestina apresenta mais fenômenos de pronúncia sem correspondência ortográfica, e respelá-los criaria erro artificial concentrado num dos grupos, **na direção que favorece a hipótese do projeto**. Erro de digitação da referência tem o mesmo efeito, e por isso cada lote passa por conferência de grafia antes de entrar no cálculo.
- Fragmento de palavra solto no começo ou no fim do áudio, vindo da folga de recorte, deve ser ignorado.

**Custo estimado:** 2 h de áudio ao todo; transcrição manual cuidadosa de fala espontânea com ruído leva de 4 a 8 vezes o tempo do áudio, o que dá **8 a 16 horas**. Divisível entre pessoas, porque os seis estados são arquivos independentes.

**Ressalva de dimensionamento:** os 20 minutos por estado são recomendação de bom senso registrada em `experimentos/meta_volume_corpus.py`, e **não** cálculo de poder como os que o projeto usa para os pares mínimos.

```bash
pip install jiwer
python medir_wer.py --entrada amostra_wer.json
```

---

## 3.2 Coerência dialetal — falante migrante

**O que mede.** Se os falantes atribuídos a um estado de fato falam a variedade daquele estado.

**Por que não é automatizável, e isso foi testado.** Duas vias foram consideradas e descartadas com base em achados do próprio projeto:

1. **Densidade de marcadores lexicais.** O item 2.4 de `docs/achados_para_o_artigo.md` mediu **zero** ocorrências desses itens em 30 mil palavras de fala nordestina genuína. Um detector assim marcaria como suspeito quase todo falante nordestino verdadeiro.
2. **Densidade de contextos de palatalização.** `densidade_palatalizacao.py` conta contextos **ortográficos**, não a realização fonética. Os mesmos contextos existem em qualquer fala do português.

A defesa efetiva é **curadoria manual, ouvindo**. `pipeline_coleta_piloto/preparar_amostra_coerencia.py` torna isso executável: amostra 10 locutores por estado, recorta o segmento mais longo de cada um e gera uma planilha com veredito em aberto — `coerente`, `suspeito` ou `inconclusivo`.

**Dimensionamento:** com 20 locutores por estado e amostra de 10, uma taxa real de migração de 15% teria cerca de 80% de chance de produzir ao menos uma detecção. É poder adequado para primeiro descarte, **não** para medir a taxa.

**A ameaça é direcional, e o documento precisa dizê-lo.** O vetor migratório dominante é Nordeste → Sudeste. Um falante migrado atenua o contraste medido e produz **aparência de ausência de viés** — ou seja, empurra na direção do resultado que o projeto encontrou.

```bash
python preparar_amostra_coerencia.py --estado PE --n 10
```

Requer o áudio, portanto o mesmo ambiente da etapa 1.

### Resultado da escuta, 17/09/2026 — frente 3.2 concluída

As 60 pessoas da amostra foram ouvidas por um membro da equipe, em seis blocos conduzidos em sessão, com os clipes recortados por `preparar_clipes_coerencia.py` e o veredito de cada pessoa gravado por `registrar_coerencia.py`.

| UF | Coerente | Suspeito | Inconclusivo |
|---|---|---|---|
| PB | 10 | 0 | 0 |
| PE | 10 | 0 | 0 |
| CE | 8 | 1 | 1 |
| BA | 9 | 0 | 1 |
| SP | 10 | 0 | 0 |
| RJ | 9 | 0 | 1 |
| **Total** | **56** | **1** | **3** |

**O suspeito não é o caso previsto.** `COE-CE-04`, em canal do Ceará, é falante estrangeiro: o próprio conteúdo declara restaurante na Itália e pizzaria em Acqui Terme, com trabalho em Fortaleza. A ameaça documentada é o migrante de outra região do Brasil, e no grupo de controle — onde um nordestino migrado atenuaria o contraste entre as regiões — **nenhum caso foi identificado** em 20 pessoas. As 20 pessoas de São Paulo e do Rio de Janeiro foram reconferidas na mesma sessão, com a pergunta dirigida e única — *esta pessoa soa nordestina?* —, e a resposta foi negativa em todas. A reconferência é reafirmação pelo mesmo ouvinte, e não escuta cega independente: não constitui medida de concordância (`docs/pendencias.md` 6.6).

**Os três inconclusivos têm duas causas, e nenhuma é sotaque.** `COE-BA-10` tem ruído de ambiente em toda a fala da pessoa, sem trecho mais limpo no arquivo. `COE-CE-06` e `COE-RJ-09` são defeitos de diarização — fusão de dois locutores num rótulo, no primeiro, e rótulo espúrio sobre passagem musical, no segundo —, registrados em `docs/pendencias.md` 4.12, com a consequência que têm sobre a contagem de pessoas distintas.

**O que o resultado autoriza dizer, e o que não autoriza.** Autoriza: numa amostra de dez pessoas por estado, uma pessoa foi julgada incoerente com a variedade do estado, nenhuma delas no grupo de controle. Não autoriza afirmar que o corpus está livre de falante migrante: a amostra foi dimensionada para detectar uma taxa real de 15% com cerca de 80% de chance, de modo que taxas menores passam despercebidas com facilidade. O julgamento é de um único ouvinte, sem medida de concordância entre juízes (`docs/pendencias.md` 6.6).

---

## 3.3 Participação de ouvinte

**O que mede.** Quanto do material, por estado, é fala de ouvinte participando de programa de rádio — o registro menos monitorado do corpus.

**Por que importa.** Os marcadores regionais que o projeto investiga são mais frequentes em fala informal. Se o grupo nordestino tiver esse tipo de fala e o controle não, o contraste entre as regiões fica inflado.

**O que já se sabe.** O formato foi confirmado em quatro canais — PE, CE e dois na BA — e em nenhum de PB, SP ou RJ. A busca dirigida por equivalentes em SP e RJ **falhou por razão estrutural**, não por falta de esforço: nas duas capitais, os programas de participação pertencem a redes nacionais, cujos ouvintes ligam do país inteiro e que por isso não satisfazem a regra de atribuição por estado.

**Consequência de método:** a simetria não é obtenível por busca, e por isso tem de ser obtida por **medida e desconto**.

**O que existe.** Dois campos, e a distinção entre eles é o ponto:

- `canal_tem_participacao_ouvinte`, herdado de `fontes.json`, que diz quais arquivos vale a pena ouvir;
- `participacao_ouvinte`, fato do arquivo, que só se estabelece ouvindo e nasce `nao_verificado`.

`pipeline_coleta_piloto/balanco_participacao.py` relata o volume por estado e compara os grupos.

**O trabalho é pequeno hoje.** Dos 52 arquivos coletados, **apenas um** vem de canal com o formato — 8,6 min da TV Aratu, na Bahia. A ameaça é **prospectiva**: incide sobre a coleta futura, se as rádios de participação passarem a ser exploradas.

```bash
python balanco_participacao.py                  # relatório
python balanco_participacao.py --marcar-canal   # repropaga a marca herdada do canal
```

---

## Ao terminar

1. Registrar as três medidas neste documento, com data.
2. Atualizar `docs/ficha_conjunto.md` — A.4 traz o WER como não medido.
3. Atualizar `docs/dataset-spec.md`, camada de validação, e `docs/pendencias.md` (4.9, 6.2, 1.1).
4. Levar o WER estratificado a `docs/achados_para_o_artigo.md`: é resultado, e não apenas controle.

**Advertência de escrita, que vale para as três.** Nenhuma dessas medições autoriza afirmar que o corpus é representativo da fala de um estado. Ele documenta fala pública de determinados canais. A distinção está em `docs/ficha_conjunto.md`, entre os usos desaconselhados, e não deve ser afrouxada porque as medições saíram favoráveis.
