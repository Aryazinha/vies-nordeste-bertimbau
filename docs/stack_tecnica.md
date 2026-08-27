# Documentação Técnica da Stack de Dados
## Referência de apoio ao projeto — Investigação de Vieses Sociolinguísticos no BERTimbau

> Este arquivo é referenciado pelo `CLAUDE.md` na raiz do projeto (seção 2, transferida para este arquivo em 06/08/2026, a fim de reduzir o tamanho do CLAUDE.md — ver Log de revisões). Não é carregado automaticamente em toda sessão; o Claude Code lê sob demanda quando o trabalho envolve o pipeline `yt-dlp`/`faster-whisper`/`pyannote.audio`.

# PARTE 2 — DOCUMENTAÇÃO TÉCNICA DA STACK DE DADOS

> Contexto de uso: pipeline de coleta de áudio espontâneo/regional (ex. YouTube) → transcrição com timestamps por palavra → diarização de locutores → (etapas futuras: seleção/curadoria de trechos por variedade dialetal para construção do dataset de avaliação).

## 2.1 `yt-dlp` — coleta de áudio e metadados

**Repositório:** https://github.com/yt-dlp/yt-dlp (fork ativamente mantido do `youtube-dl`)
**Dependência recomendada:** `ffmpeg` + `ffprobe` (obrigatórios para extração/conversão de áudio e leitura de metadados técnicos).

### 2.1.1 Instalação
```bash
pip install -U yt-dlp
# Dependências de sistema (Ubuntu/Debian):
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### 2.1.2 Baixar apenas áudio, na melhor qualidade, como WAV 16kHz (linha de comando)

```bash
yt-dlp \
  -x --audio-format wav \
  --postprocessor-args "ffmpeg:-ar 16000 -ac 1" \
  -f "bestaudio/best" \
  --write-info-json \
  -o "dataset_raw/%(id)s.%(ext)s" \
  "URL_DO_VIDEO"
```

**Explicação parâmetro a parâmetro:**
- `-x` (`--extract-audio`): extrai apenas a faixa de áudio, descartando vídeo.
- `--audio-format wav`: força a conversão final para `.wav` (não comprimido — ideal para ASR/diarização, evita artefatos de compressão com perdas como MP3/OPUS).
- `-f "bestaudio/best"`: seleciona o melhor stream de áudio disponível; usa `best` como *fallback* se não houver stream de áudio isolado.
- `--postprocessor-args "ffmpeg:-ar 16000 -ac 1"`: repassa argumentos diretamente ao `ffmpeg` no pós-processamento — `-ar 16000` define a taxa de amostragem em **16 kHz** (padrão exigido tanto pelo Whisper/faster-whisper quanto pelo pyannote.audio) e `-ac 1` força **mono** (1 canal), também padrão dos dois modelos.
- `--write-info-json`: grava um `.info.json` ao lado do áudio, com **todos os metadados brutos** disponíveis (título, descrição, canal, data de upload, duração, contagem de visualizações, tags, categoria, idioma detectado pela plataforma, legendas disponíveis etc.) — essencial para documentação de proveniência do dataset (rastreabilidade/reprodutibilidade).
- `-o "dataset_raw/%(id)s.%(ext)s"`: template de nome de arquivo usando o **ID do vídeo** (mais seguro que título, que pode conter caracteres especiais ou colidir entre vídeos).

### 2.1.3 Extrair *apenas* metadados, sem baixar mídia (útil para triagem prévia em escala)

```python
import yt_dlp

ydl_opts = {"skip_download": True, "quiet": True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("URL_DO_VIDEO", download=False)

# Metadados brutos relevantes para documentação/triagem do dataset
metadata = {
    "id": info.get("id"),
    "title": info.get("title"),
    "uploader": info.get("uploader"),
    "upload_date": info.get("upload_date"),
    "duration_s": info.get("duration"),
    "view_count": info.get("view_count"),
    "description": info.get("description"),
    "tags": info.get("tags"),
    "categories": info.get("categories"),
    "language": info.get("language"),
    "automatic_captions_available": bool(info.get("automatic_captions")),
}
print(metadata)
```

### 2.1.4 Download + extração de áudio via API Python (equivalente ao comando CLI acima)

```python
import yt_dlp

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "dataset_raw/%(id)s.%(ext)s",
    "writeinfojson": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
    }],
    "postprocessor_args": {
        "ffmpeg": ["-ar", "16000", "-ac", "1"],
    },
    "ignoreerrors": True,        # não interrompe lote inteiro por 1 vídeo com erro
    "download_archive": "dataset_raw/archive.txt",  # evita redownload em execuções futuras
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(["URL_DO_VIDEO"])
```

**Vantagens / Desvantagens (`yt-dlp`):**
- *Vantagem.* Gratuito, open source, ativamente mantido (fork robusto do `youtube-dl`), suporta >1000 sites além do YouTube.
- *Vantagem.* `download_archive` é essencial em pipelines de pesquisa incrementais (evita reprocessar e reintroduzir vídeos já anotados/excluídos por QA).
- *Ressalva.* Sujeito a mudanças frequentes no *player* do YouTube que podem quebrar extração — convém monitorar a versão instalada (`pip install -U yt-dlp` regularmente) e o *issue tracker* oficial em caso de falha súbita.
- *Ressalva.* **Aspecto ético/legal a documentar no artigo:** verificar Termos de Serviço da plataforma de origem e, quando aplicável, licença de uso do conteúdo (Creative Commons vs. todos os direitos reservados) antes de redistribuir qualquer trecho de áudio/transcrição como parte do dataset publicado. Para publicação científica, o padrão mais seguro é **disponibilizar os IDs dos vídeos e o código de coleta**, não o áudio bruto redistribuído, salvo licença explícita que permita.

---

## 2.2 `faster-whisper` — transcrição com timestamps a nível de palavra

**Repositório oficial:** https://github.com/SYSTRAN/faster-whisper
**Motor de inferência:** CTranslate2 (reimplementação otimizada do Whisper da OpenAI) — até 4x mais rápido que `openai/whisper` com a mesma acurácia, com suporte a quantização INT8 tanto em CPU quanto GPU.

### 2.2.1 Instalação (com suporte a GPU/CUDA)
```bash
pip install faster-whisper
# Requer CUDA + cuDNN compatíveis com a versão do CTranslate2 instalada.
# Verificar compatibilidade exata na documentação do CTranslate2 antes de instalar.
```

### 2.2.2 Configuração recomendada para o modelo `large-v3` em GPU

```python
from faster_whisper import WhisperModel

model_size = "large-v3"

# GPU com FP16 (recomendado quando há VRAM suficiente e prioridade é qualidade)
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Alternativa com menor uso de VRAM (qualidade quase equivalente):
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")

# Fallback CPU (sem GPU disponível):
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
```

| `compute_type` | Uso de VRAM | Quando usar |
|---|---|---|
| `float16` | Alto | GPU com VRAM ampla (≥10 GB); prioridade em qualidade máxima |
| `int8_float16` | Médio | GPU com VRAM limitada; leve perda de precisão numérica, impacto mínimo em WER |
| `int8` (CPU) | N/A (RAM) | Sem GPU disponível; bom para prototipagem, lento para lotes grandes |

### 2.2.3 Transcrição com timestamps a nível de palavra (parâmetros exatos)

```python
segments, info = model.transcribe(
    "audio.wav",
    language="pt",              # força português — evita erros de auto-detecção em áudio ruidoso/dialetal
    beam_size=5,                 # busca em feixe; 5 é o padrão recomendado (trade-off qualidade/velocidade)
    word_timestamps=True,        # ATIVA timestamps a nível de PALAVRA (essencial para o projeto)
    vad_filter=True,             # usa VAD (Silero) embutido para remover silêncios/ruído antes da transcrição
    vad_parameters=dict(min_silence_duration_ms=500),
    condition_on_previous_text=False,  # evita "alucinação"/loop de repetição em áudios longos
    temperature=0.0,             # decodificação determinística (reprodutibilidade — importante p/ ciência!)
)

print(f"Idioma detectado: {info.language} (confiança: {info.language_probability:.2f})")

resultado = []
for segment in segments:
    seg_dict = {"start": segment.start, "end": segment.end, "text": segment.text, "words": []}
    if segment.words:
        for word in segment.words:
            seg_dict["words"].append({
                "word": word.word,
                "start": word.start,
                "end": word.end,
                "probability": word.probability,  # confiança da predição — útil para QA/filtragem
            })
    resultado.append(seg_dict)

# ATENÇÃO: `segments` é um generator — a transcrição só roda de fato ao iterar (como acima) ou com list(segments).
```

**Explicação dos parâmetros críticos para o projeto:**
- `word_timestamps=True`: ativa o alinhamento a nível de palavra via atenção cruzada do modelo (não é *forced alignment* fonético como no WhisperX — é uma estimativa baseada nos pesos de atenção do próprio Whisper). Para alinhamento fonético mais preciso (ex. se o projeto evoluir para análise prosódica fina), considerar complementar com **WhisperX** (usa `wav2vec2` para *forced alignment*).
- `temperature=0.0`: fixa decodificação determinística — **crítico para reprodutibilidade científica**; com `temperature > 0` o mesmo áudio pode gerar transcrições ligeiramente diferentes entre execuções.
- `condition_on_previous_text=False`: reduz risco de "alucinação em cadeia" (o modelo repetir ou inventar texto influenciado por erros do segmento anterior), problema documentado em áudios longos ou com trechos de silêncio/ruído — relevante para material coletado de fontes espontâneas como YouTube.
- `vad_filter=True`: reduz processamento de silêncio e mitiga um problema conhecido do Whisper de "alucinar" texto em trechos sem fala.

**Vantagens / Desvantagens:**
- *Vantagem.* Muito mais rápido e leve em memória que o Whisper original, mantendo acurácia equivalente.
- *Vantagem.* Suporte nativo a quantização (INT8) viabiliza rodar em GPUs com VRAM limitada ou até CPU.
- *Ressalva.* `word_timestamps` do faster-whisper é uma estimativa baseada em atenção, **não é *forced alignment* fonético** — para timestamps de palavra de altíssima precisão (ex. se o projeto precisar de análise prosódica/fonética fina), o padrão da literatura é usar **WhisperX**, que faz alinhamento fonético pós-hoc com `wav2vec2`.
- *Ressalva.* Modelos `large-v3` têm custo computacional significativo — para triagem em larga escala antes da curadoria manual, pode-se considerar `distil-large-v3` (mais rápido, leve perda de WER, principalmente calibrado para inglês — validar WER em PT-BR antes de adotar para a versão final do dataset).

---

## 2.3 `pyannote.audio` — diarização de locutores

**Repositório:** https://github.com/pyannote/pyannote-audio
**Modelos no Hugging Face Hub:** requer criação de token de acesso em https://hf.co/settings/tokens e aceite dos termos de uso do(s) modelo(s) escolhido(s).

### 2.3.1 Instalação
```bash
pip install pyannote.audio
# ffmpeg é necessário (usado pelo torchcodec para decodificação de áudio)
```

### 2.3.2 Pipeline recomendado — `speaker-diarization-community-1` (estado da arte open-source atual)

> **Nota de atualização:** o pipeline `pyannote/speaker-diarization-3.1` (que corrige um problema de dependência em `onnxruntime` presente na versão 3.0, rodando segmentação e *embedding* em PyTorch puro) foi, por um tempo, a recomendação padrão. A documentação oficial mais recente indica o pipeline **`pyannote/speaker-diarization-community-1`** como sucessor com desempenho superior — sugiro validar empiricamente qual versão está disponível/estável no momento da execução do projeto, pois esse ecossistema evolui rápido.

```python
import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

# Carrega o pipeline pré-treinado (requer token do Hugging Face com termos aceitos)
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token="SEU_TOKEN_HUGGINGFACE",
)

# Envia o pipeline para GPU, se disponível
pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# Executa a diarização (com barra de progresso opcional)
with ProgressHook() as hook:
    output = pipeline("audio.wav", hook=hook)

# Itera sobre os turnos de fala identificados
for turn, speaker in output.speaker_diarization:
    print(f"{speaker}: {turn.start:.2f}s -> {turn.end:.2f}s")
```

### 2.3.3 Controlando o número de locutores (útil quando já se sabe, ex. entrevista 1-para-1)

```python
# Quando o número exato de locutores é conhecido:
output = pipeline("audio.wav", num_speakers=2)

# Quando se sabe apenas um intervalo plausível:
output = pipeline("audio.wav", min_speakers=1, max_speakers=4)
```

### 2.3.4 Exportando para o formato padrão RTTM (interoperável com outras ferramentas de avaliação de diarização)

```python
with open("audio.rttm", "w") as rttm:
    output.speaker_diarization.write_rttm(rttm) if hasattr(output, "speaker_diarization") else output.write_rttm(rttm)
```

### 2.3.5 Integração conceitual com o `faster-whisper` (alinhar diarização + transcrição por palavra)

```python
def atribuir_locutor(word_start, word_end, diarization_output):
    """Atribui o locutor dominante a uma palavra, por sobreposição temporal."""
    melhor_speaker, melhor_overlap = None, 0.0
    for turn, _, speaker in diarization_output.itertracks(yield_label=True):
        overlap = max(0.0, min(word_end, turn.end) - max(word_start, turn.start))
        if overlap > melhor_overlap:
            melhor_overlap, melhor_speaker = overlap, speaker
    return melhor_speaker

# Uso: para cada `word` retornada pelo faster-whisper (word.start, word.end),
# chamar atribuir_locutor(word.start, word.end, output) para rotular o locutor.
```

**Requisitos técnicos do modelo:**
- Ingere áudio **mono, 16 kHz** — se a entrada tiver outro formato, o `pyannote.audio` faz *downmix* e *resample* automaticamente, mas é mais eficiente já entregar áudio nesse formato (coerente com a configuração do `yt-dlp` recomendada na seção 2.1).

**Vantagens / Desvantagens:**
- *Vantagem.* Pipeline pronto, *state of the art* em benchmarks acadêmicos abertos (AMI, VoxConverse, DIHARD, etc.), integração nativa com Hugging Face Hub.
- *Vantagem.* Suporta cenários com número de locutores desconhecido (clustering automático) ou conhecido (`num_speakers`).
- *Ressalva.* Requer aceite de termos de uso + token do Hugging Face por modelo (fricção operacional a documentar no protocolo de coleta).
- *Ressalva.* Desempenho de diarização pode degradar em áudio de baixa qualidade/ruído de fundo típico de gravações amadoras do YouTube — recomenda-se etapa de QA manual amostral (ex. checar DER — *Diarization Error Rate* — em uma subamostra anotada manualmente) antes de tomar a diarização automática como confiável para curadoria do dataset final.
- *Ressalva.* Licenciamento: verificar a licença específica do checkpoint usado (`community-1` é CC-BY-4.0; versões anteriores podem ter termos distintos) antes de redistribuir artefatos derivados.

---