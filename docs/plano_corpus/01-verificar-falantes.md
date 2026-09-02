# Etapa 1 — Quantos falantes distintos há no corpus

**Objetivo.** Apurar quantas **pessoas diferentes** estão nos 52 arquivos já coletados, por estado, e compará-lo ao piso de 20 por estado. É o que decide se a coleta está concluída ou quanto falta.

**Estado:** não iniciada. **Onde roda:** Google Colab, com GPU, mais uma etapa de conferência humana que não exige GPU.

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

---

## 3. Advertência que trava a execução se ignorada

O script lê os registros de `FINAL_DIR`, isto é, `pipeline_coleta_piloto/dataset_raw/registros_finais/` — **e essa pasta está vazia**.

Os registros com diarização existem em dois lugares:

- `pipeline_coleta_piloto/dataset_raw/registros_anonimizados/` — 52 arquivos, já anonimizados
- `piloto_resultados (2).zip`, na raiz do projeto — 52 arquivos, **não anonimizados**

**Recomendação:** usar os **anonimizados**. Têm o mesmo campo `diarizacao` e o mesmo `arquivo`, e manipular material já anonimizado é preferível sempre que o resultado não dependa dos nomes — e aqui não depende: a comparação é de voz, não de texto.

Duas saídas, à escolha de quem executar:

1. Copiar os anonimizados para `registros_finais/` antes de rodar; ou
2. Acrescentar ao script um parâmetro `--registros`, que hoje não existe — ele só aceita `--estado` e `--audio-dir`.

A segunda é preferível se a etapa 2 for necessária, porque o problema voltaria a cada nova rodada.

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

```bash
python verificar_reincidencia.py --estado PB
# repetir para PE, CE, BA, SP, RJ
```

Saída: `dataset_raw/diarizacao/reincidencia_{estado}.json`, com os pares candidatos ordenados por similaridade decrescente, cada um trazendo os dois arquivos, os dois rótulos e o valor da similaridade.

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
