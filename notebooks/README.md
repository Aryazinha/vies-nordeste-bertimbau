# Execução do piloto no Google Colab

Instruções operacionais para `piloto_colab.ipynb`. O notebook executa o passo 4 do `docs/roadmap.md` — coleta, transcrição e diarização — e produz as medições que hoje são suposições no cálculo da meta de volume.

**Link direto:** https://colab.research.google.com/github/Aryazinha/vies-nordeste-bertimbau/blob/main/notebooks/piloto_colab.ipynb

---

## 1. Preparação da credencial do Hugging Face

A diarização usa `pyannote/speaker-diarization-community-1`, modelo de acesso condicionado. São três etapas, e a segunda é a mais esquecida:

1. Criar conta em https://huggingface.co
2. Acessar https://huggingface.co/pyannote/speaker-diarization-community-1 e aceitar os termos, no botão **Agree and access repository**. Sem esta etapa o token é válido mas o download do modelo é recusado, com erro que não menciona a causa.
3. Gerar token de leitura em https://huggingface.co/settings/tokens

## 2. Configuração do ambiente no Colab

**GPU.** Menu *Ambiente de execução* → *Alterar o tipo de ambiente* → **T4 GPU** → Salvar. Sem GPU a transcrição opera abaixo do tempo real e o piloto torna-se inviável.

**Token.** Ícone de chave na barra lateral esquerda → *Adicionar novo segredo* → nome `HF_TOKEN`, valor o token gerado, com o acesso ao notebook habilitado. O token não deve ser colado em célula: o notebook é versionado e a célula preserva o conteúdo.

## 3. Execução

As células rodam em ordem, de cima para baixo.

**A primeira célula acusará falhas na primeira passagem.** É o comportamento previsto: ela verifica o ambiente antes da instalação. Execute a célula 2, de instalação, e retorne à célula 1 — todos os itens devem então indicar `OK`.

A verificação antecede qualquer download por decisão de projeto. No teste local de 27/08/2026, duas condições — versão do `yt-dlp` e disponibilidade de runtime de JavaScript — falhavam de modo silencioso: a leitura de metadados seguia correta e apenas o download era afetado, de forma que o erro se apresentava como sucesso. Ver `docs/pendencias.md`, seção 4.6.

## 4. O que esperar

| Etapa | Ordem de grandeza |
|---|---|
| Instalação | 2 a 3 minutos |
| Plano de coleta | 1 a 2 minutos, por consultar cada canal |
| Coleta | proporcional ao volume planejado |
| Transcrição | etapa dominante; em GPU opera acima do tempo real |
| Diarização | inferior à transcrição |

## 5. Resultados

Ao final o notebook baixa dois arquivos:

- `piloto_resultados.zip` — registros no esquema da seção 1.4.1 do `CLAUDE.md`, com transcrição, timestamps por palavra e locutor atribuído.
- `amostra_wer.json` — trechos totalizando 20 minutos por estado, com o campo `referencia_manual` em branco.

O áudio bruto **não** é baixado, conforme a seção 1.4.2 do `CLAUDE.md`, e a coleta completa chega a cerca de 6 GB.

## 6. Sobre a medição de erro de transcrição

O notebook **não calcula WER**. O cálculo exige transcrição humana de referência, sem atalho automático.

O que ele calcula é a confiança média por palavra, agregada por estado — indicador fraco, que mede a certeza do modelo e não o seu acerto. Presta-se a uma única pergunta: existe diferença sistemática entre variedades que justifique o custo da transcrição manual? Diferença observada nesse indicador é resultado a investigar, jamais a reportar como WER.

O WER propriamente dito exige preencher o campo `referencia_manual` de `amostra_wer.json` e comparar com `jiwer`. A ameaça à validade correspondente está registrada na Parte 3 do `CLAUDE.md`: erro de transcrição maior para fala nordestina seria viés de ferramenta apresentando-se como resultado sobre o modelo — e, medido corretamente, constitui resultado publicável por si só.
