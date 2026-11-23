# narrar-roteiro

Narração local da voz do Pedro para o modo `sem-gravacao` do `produzir-video`.

O modelo é o `Qwen/Qwen3-TTS-12Hz-1.7B-Base`, pacote `qwen-tts` 0.1.1, licença Apache 2.0. O português é um dos idiomas oficiais. A amostra de referência em português do Brasil puxa o sotaque: sem uma amostra brasileira, o modelo tende ao português europeu.

Roda na máquina do Pedro. O alvo é uma GPU NVIDIA com 8 GB de VRAM ou mais, no Windows. Sem placa, o comando usa a CPU.

O código desta pasta é o mesmo visto por `.cursor/skills/narrar-roteiro` e `.claude/skills/narrar-roteiro`, porque esses caminhos são links para `.agents/skills`.

## 1. Ambiente no Windows

Python 3.12, `uv` e `ffmpeg` no PATH. O `ffmpeg` pode vir de `winget install Gyan.FFmpeg`. O SoX também precisa existir, porque o `qwen-tts` depende dele (`choco install sox` ou o instalador do SoX).

Crie um ambiente só para a voz. Não instale isto no `.venv` dos scripts de conteúdo: o `qwen-tts` fixa `transformers==4.57.3`.

```powershell
cd C:\caminho\miyakodo
uv venv --python 3.12 .venv-tts
.venv-tts\Scripts\activate
uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
uv pip install -r .agents\skills\narrar-roteiro\requirements.txt
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

O índice `cu124` é o wheel oficial de CUDA 12.4 para Windows. Se o driver for mais antigo, use o índice que o site do PyTorch indicar para a sua versão, sempre antes do `requirements.txt`. Instalar o `qwen-tts` primeiro puxa o torch da CPU e a GPU fica ociosa.

Sem `uv`:

```powershell
py -3.12 -m venv .venv-tts
.venv-tts\Scripts\activate
python -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
python -m pip install -r .agents\skills\narrar-roteiro\requirements.txt
```

Confira a placa:

```powershell
nvidia-smi
```

O peso do 1.7B em `bfloat16` cabe em 8 GB se a placa estiver livre. Ampere (série 30) e mais novas usam `bfloat16`. Turing (série 20) cai para `float16`. Os dois são escolhidos com `--dtype auto`.

`flash-attn` é opcional e raramente compila no Windows nativo. Sem ele, a skill usa `sdpa`, que é o caminho esperado nessa máquina. No WSL, se quiser instalar: `pip install -U flash-attn --no-build-isolation`, e só com `float16` ou `bfloat16`.

O primeiro `narrar` baixa o modelo (cerca de 4 GB) para o cache do Hugging Face. Dá para apontar o cache para um disco grande:

```powershell
$env:HF_HOME = "D:\hf-cache"
```

Não commite esse cache. `video/models/` já está no `.gitignore` se você guardar o modelo ali e passar o caminho local no lugar do id `Qwen/Qwen3-TTS-12Hz-1.7B-Base`.

## 2. Amostra de voz

Dez a trinta segundos de fala limpa, uma pessoa só, sem música. O lugar é `video/inputs/voice-ref/`, fora do git.

Para tirar o trecho de um vídeo já publicado, por exemplo o `headless-software.MP4` do release `footage-headless-software`:

```powershell
mkdir video\inputs\headless-software
mkdir video\inputs\voice-ref
gh release download footage-headless-software --repo PedroMiyasaki/miyakodo -p headless-software.MP4 -D video\inputs\headless-software
python .agents\skills\narrar-roteiro\cli.py extrair-referencia video\inputs\headless-software\headless-software.MP4 --out video\inputs\voice-ref\pedro.wav --transcribe --transcript-out video\inputs\voice-ref\pedro.txt
```

O comando corta um trecho contínuo de fala perto de 18 segundos, tira o silêncio das pontas, aplica highpass e normaliza o volume. `--start 12 --duration 18` fixa a janela quando você já sabe o ponto.

A transcrição tem que ser o que a amostra diz, palavra por palavra. Esse texto liga o modo ICL do Qwen (`ref_text`). Sem ele, a skill avisa e usa só o embedding (`x_vector_only_mode`), que clona pior.

O Whisper dessa transcrição usa `--language pt` e um modelo sem sufixo `.en`. `small.en` traduz o português e é recusado.

## 3. Narrar um roteiro

Roteiro híbrido do `write-script` (`posts/script/<slug>/final.md`): só blocos `literal` são falados. Tópicos, inserts, títulos e a nota depois de `---` ficam de fora. `[pause]` vira pausa, não palavra.

```powershell
python .agents\skills\narrar-roteiro\cli.py texto posts\script\<slug>\final.md --mode auto
python .agents\skills\narrar-roteiro\cli.py narrar posts\script\<slug>\final.md --ref video\inputs\voice-ref\pedro.wav --ref-text video\inputs\voice-ref\pedro.txt
```

Markdown corrido, sem cabeçalho de bloco, é narrado por inteiro no `--mode auto`. `--mode all` força a leitura também dos tópicos. `--mode literal` num arquivo sem blocos continua lendo a prosa.

Saída, em `video/outputs/narracao/<slug>/`:

| Arquivo | Uso |
|---|---|
| `voice.wav` | Faixa mono, 48 kHz, -16 LUFS, teto de -1 dBTP |
| `words.json` | `[{text, start, end}]` no relógio do WAV |
| `produzir-video.snippet.json` | `voice` e `words` para colar no roteiro do `produzir-video` |

Os chunks têm no máximo 240 caracteres e quebram em frase. A pausa entre frases é 0,28 s, entre parágrafos 0,52 s, e o `[pause]` do teleprompter 0,75 s. `--crossfade-ms 15` faz a borda de cada chunk descer até o zero, encostada na pausa, para não estalar.

O prompt de voz é criado uma vez e reutilizado. Antes do Whisper, o modelo de TTS sai da memória da GPU.

Para encaixar no Reel, copie `voice` e `words` do snippet para o JSON do `produzir-video` e escreva os beats. O `voice.src` já vem relativo à raiz do repo quando a saída está dentro dele.

## 4. Testes

Na raiz, sem GPU e sem baixar modelo:

```powershell
python -m unittest discover -s .agents\skills\narrar-roteiro\tests -v
```

O backend `mock` cobre o CLI. Ele não é a voz do Pedro.

## 5. Quando a GPU não entra

- `torch.cuda.is_available()` falso: o torch instalado é o da CPU, ou o driver não enxerga a placa. Reinstale o torch pelo índice CUDA antes do `qwen-tts`.
- Erro de memória: feche o que estiver na GPU. A skill processa um chunk por vez. `--dtype float16` e `--attn sdpa` são o caminho de 8 GB.
- Flash attention com NaN: use `--attn sdpa`.
- Whisper ausente: `uv pip install faster-whisper`. Não use modelo `.en`.
