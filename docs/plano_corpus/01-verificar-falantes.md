# Etapa 1 — Quantos falantes distintos há no corpus

**Objetivo.** Apurar quantas **pessoas diferentes** estão nos 52 arquivos já coletados, por estado, e compará-lo ao piso de 20 por estado. É o que decide se a coleta está concluída ou quanto falta.

**Estado:** preparada em 02/09/2026 — ferramenta corrigida e notebook pronto —, aguardando execução no Colab. **Onde roda:** Google Colab, com GPU, mais uma etapa de conferência humana que não exige GPU.

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

## 6. Conferência humana, que é a parte que decide

Para cada par candidato, ouvir os dois trechos e responder: **é a mesma pessoa?**

Ordem sugerida: começar pelos de similaridade mais alta, que devem ser fusões óbvias, e descer até onde os pares deixarem de ser plausíveis. O ponto em que isso ocorre **é a calibração empírica do limiar**, e deve ser registrado — vale mais que o valor default de 0,75.

Atenção ao padrão esperado: o repórter ou apresentador do canal é quem mais reaparece. Pares dentro do **mesmo canal** são os candidatos mais prováveis; entre canais diferentes, muito menos.

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

---

## 8. Ao terminar

1. Atualizar este documento com os números apurados, o limiar calibrado e a data.
2. Atualizar `docs/dataset-spec.md` — a seção "Camada de execução, em números" afirma que a verificação nunca rodou.
3. Atualizar `docs/pendencias.md`, seção 6.4, e o item #5 do registro de pendentes.
4. Se houver déficit, anotá-lo por estado em [`02-completar-coleta.md`](02-completar-coleta.md), que é o insumo daquela etapa.

Uma etapa concluída cujo resultado só existe no histórico da conversa está perdida.
