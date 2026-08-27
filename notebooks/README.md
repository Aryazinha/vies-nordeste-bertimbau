# Execução do piloto

O piloto executa o passo 4 do `docs/roadmap.md` e produz as medições que hoje são suposições no cálculo da meta de volume.

## A esteira é dividida entre dois ambientes

Não por conveniência, mas por restrição de cada um:

| Etapa | Ambiente | Motivo |
|---|---|---|
| Coleta | máquina local | o YouTube recusa downloads originados de datacenter |
| Transcrição e diarização | Google Colab | exigem GPU |

A primeira execução no Colab, em 27/08/2026, coletou **0 de 51 vídeos**, todos recusados com *"Sign in to confirm you're not a bot"*. O mesmo plano executa normalmente numa conexão residencial. O registro completo está em `docs/pendencias.md`, seção 4.8.

---

## Parte 1 — Coleta, na máquina local

```
cd pipeline_coleta_piloto
python selecionar_videos.py --piloto --max-canais 2 --saida plano_piloto.json
python coletar_local.py plano_piloto.json
```

O primeiro comando consulta os canais de `fontes.json` e monta o plano; o segundo baixa o áudio e grava `dataset_raw/metadados.json`, que carrega estado, camada e canal de cada arquivo. Sem esse arquivo, o ambiente de processamento receberia áudio sem procedência regional — e procedência é a variável do estudo.

Ao final, envie a pasta `dataset_raw` inteira para o Google Drive, na raiz do drive.

**Se houver falhas de coleta**, verifique se elas se concentram em algum estado ou camada. Perda desigual entre grupos é viés de amostragem, não ruído — a restrição etária, por exemplo, recai sobre matérias de violência, que são parte expressiva do vox-pop policial (ver `docs/pendencias.md`, seção 4.5).

---

## Parte 2 — Processamento, no Colab

**Link direto:** https://colab.research.google.com/github/Aryazinha/vies-nordeste-bertimbau/blob/main/notebooks/piloto_colab.ipynb

### Credencial do Hugging Face

A diarização usa `pyannote/speaker-diarization-community-1`, modelo de acesso condicionado. Três etapas, sendo a segunda a mais esquecida:

1. Criar conta em https://huggingface.co
2. Acessar https://huggingface.co/pyannote/speaker-diarization-community-1 e aceitar os termos, no botão **Agree and access repository**. Sem esta etapa o token é válido mas o download do modelo é recusado, com erro que não menciona a causa.
3. Gerar token de leitura em https://huggingface.co/settings/tokens

### Configuração

**GPU.** *Ambiente de execução* → *Alterar o tipo de ambiente* → **T4 GPU** → Salvar. Faça isso antes de executar qualquer célula: a troca reinicia o ambiente.

**Token.** Ícone de chave na barra lateral → *Adicionar novo segredo* → nome `HF_TOKEN`, com o acesso ao notebook habilitado. O token não deve ser colado em célula: o notebook é versionado e a célula preserva o conteúdo.

**Pasta do Drive.** A célula 4 usa `/content/drive/MyDrive/dataset_raw`. Ajuste se você enviou para outro lugar.

### Execução

Células em ordem. A de instalação pede reinício da sessão — o limite de versão do `numpy` só passa a valer depois disso.

O limite é deliberado: a instalação sem restrição traz `numpy` mais novo do que o `numba` aceita, e o `numba` entra por baixo do `pyannote`, via `librosa`. O conflito se manifestaria apenas na diarização, isto é, **depois** de a transcrição inteira já ter rodado.

A célula de transcrição baixa cerca de 3 GB de modelo na primeira execução e permanece vários minutos sem imprimir nada.

---

## Resultados

| Arquivo | Conteúdo |
|---|---|
| `piloto_resultados.zip` | registros no esquema da seção 1.4.1 do `CLAUDE.md`, com transcrição, timestamps por palavra e locutor atribuído |
| `amostra_wer.json` | trechos totalizando 20 minutos por estado, com `referencia_manual` em branco |

Os registros são gravados também no Drive, de modo a sobreviverem ao encerramento da sessão.

O áudio bruto não é redistribuído, conforme a seção 1.4.2 do `CLAUDE.md`.

---

## Sobre a medição de erro de transcrição

O notebook **não calcula WER**, que exige transcrição humana de referência e não admite atalho automático.

O que calcula é a confiança média por palavra, agregada por estado — indicador fraco, que mede a certeza do modelo e não o seu acerto. Presta-se a uma única pergunta: existe diferença sistemática entre variedades que justifique o custo da transcrição manual? Diferença observada nesse indicador é resultado a investigar, jamais a reportar como WER.

O WER propriamente dito exige preencher `referencia_manual` em `amostra_wer.json` e comparar com `jiwer`. A ameaça correspondente está na Parte 3 do `CLAUDE.md`: erro de transcrição maior para fala nordestina seria viés de ferramenta apresentando-se como resultado sobre o modelo — e, medido corretamente, constitui resultado publicável por si só.
