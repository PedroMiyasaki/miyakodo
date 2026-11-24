---
name: narrar-roteiro
description: >
  Gera a narração completa de um roteiro Markdown com a voz clonada do Pedro,
  100% local na GPU NVIDIA, usando Qwen3-TTS-12Hz-1.7B-Base. Entrega voice.wav
  e words.json no contrato do produzir-video, modo sem-gravacao. Ative com
  "narra o roteiro", "gera a voz do roteiro", "clona a voz e narra" ou
  "usa narrar-roteiro".
---

# Narrar roteiro

A skill transforma um roteiro em faixa de voz. O Pedro não grava. O modelo `Qwen/Qwen3-TTS-12Hz-1.7B-Base` (Apache 2.0, português entre os idiomas oficiais) clona a voz a partir de uma amostra local e fala o texto. Tudo roda na máquina dele, de preferência numa GPU NVIDIA com pelo menos 8 GB de VRAM. Sem GPU, o mesmo comando cai para a CPU.

A faixa entra no `produzir-video` no modo `sem-gravacao`: `voice.src` mais `words` no formato `{text, start, end}`. Esta skill não monta o Reel. Ela entrega o áudio e os tempos.

O código mora em `.agents/skills/narrar-roteiro`. `.cursor/skills` e `.claude/skills` são links para `.agents/skills`, então a skill aparece nos dois caminhos sem cópia.

O setup da GPU no Windows está no [README.md](README.md).

## Entradas

- Um Markdown (`.md`). No formato híbrido do `write-script`, só os blocos `literal` são falados. Blocos `tópicos`, títulos, `[pause]`, `[insert: ...]`, `[cena: ...]` e o miolo depois de `---` ficam de fora. `[pause]` vira uma pausa maior, não uma palavra. Num Markdown corrido, o texto entra inteiro, já sem negrito, link, código e lista.
- `--mode auto` escolhe sozinho: se achar cabeçalho `[BLOCO] · literal` ou `[BLOCO] · tópicos`, usa o modo literal. Se não achar, narra o Markdown corrido. `literal` e `all` forçam um dos dois.
- Amostra de referência, 10 a 30 segundos de fala limpa, em `video/inputs/voice-ref/`. Essa pasta está no `.gitignore`. A transcrição literal da amostra é opcional e melhora o timbre: sem ela, a clonagem usa só o embedding (`x_vector_only_mode`).

Um bloco sem modo, como `[HOOK]` seguido de prosa, é falado. É o caso dos roteiros antigos que não marcam `literal`.

## Saídas

Por padrão, em `video/outputs/narracao/<slug>/`, pasta que já não entra no git:

- `voice.wav`: mono, 48 kHz, -16 LUFS, teto de -1 dBTP, nível de Reel.
- `words.json`: lista `[{text, start, end}]`, tempos em segundos no relógio desse WAV.
- `produzir-video.snippet.json`: `mode`, `voice.src`, `voice.in`, `voice.out` e `words`, pronto para colar num roteiro do `produzir-video`. Os beats continuam sendo escritos naquele roteiro.

Os tempos saem do Whisper em português, `--language pt`, modelo `small` (ou `medium` / `large-v3`). Modelo com sufixo `.en` é recusado: ele traduz a fala. É a mesma regra de `.agents/skills/media-use/audio/references/transcribe.md`.

## Comandos

Na raiz do repo, depois do setup do README.

Ver o que seria falado, sem carregar modelo:

```bash
python3 .agents/skills/narrar-roteiro/cli.py texto posts/script/<slug>/final.md --mode auto
```

Extrair 15 a 20 segundos limpos de um vídeo. O exemplo usa o release `footage-headless-software`. Sem `--start`, o corte procura um trecho contínuo de fala, perto de 18 segundos.

```bash
mkdir -p video/inputs/headless-software video/inputs/voice-ref
gh release download footage-headless-software --repo PedroMiyasaki/miyakodo -p headless-software.MP4 -D video/inputs/headless-software
python3 .agents/skills/narrar-roteiro/cli.py extrair-referencia video/inputs/headless-software/headless-software.MP4 --out video/inputs/voice-ref/pedro.wav --transcribe --transcript-out video/inputs/voice-ref/pedro.txt
```

Narrar:

```bash
python3 .agents/skills/narrar-roteiro/cli.py narrar posts/script/<slug>/final.md --ref video/inputs/voice-ref/pedro.wav --ref-text video/inputs/voice-ref/pedro.txt
```

No Windows o executável é `python`, no mesmo caminho de arquivo.

Flags úteis: `--device auto|cpu|cuda:0`, `--dtype auto|bfloat16|float16`, `--attn auto|sdpa|flash_attention_2`, `--max-chars 240`, `--sentence-pause 0.28`, `--paragraph-pause 0.52`, `--beat-pause 0.75`, `--crossfade-ms 15`, `--whisper-model small`, `--language pt`, `--no-loudnorm`, `--x-vector-only`.

`--backend mock` sintetiza um tom e alinha o texto na régua dos chunks. Serve para teste sem GPU. Não é a voz do Pedro.

## Como a faixa é montada

1. O parser separa o que é fala do que é marcação.
2. Abreviações, números, porcentagens, reais e siglas comuns (IA, RAG, MCP, API) viram fala em português.
3. O texto é cortado em chunks de até 240 caracteres, em fronteira de frase, para a prosódia do Qwen3-TTS não degradar.
4. `create_voice_clone_prompt` roda uma vez. Cada chunk chama `generate_voice_clone` com esse prompt, `language="Portuguese"`. O timbre não é recalculado.
5. GPU: `bfloat16` quando a placa aceita, senão `float16`. Atenção `flash_attention_2` se o pacote existir, senão `sdpa`. Sem CUDA, CPU em `float32` e `sdpa`.
6. Os chunks são costurados com pausa de frase, de parágrafo ou de `[pause]`. A borda de cada chunk desce até o silêncio, então a emenda não estala e não come a última sílaba.
7. O `ffmpeg` normaliza para -16 LUFS, com teto de -1 dBTP.
8. O modelo de voz é descarregado e o Whisper lê o WAV final. Os tempos batem com o arquivo que o `produzir-video` vai tocar.

## O que não versionar

Não commitar `voice.wav`, a amostra em `video/inputs/voice-ref/`, o MP4 de origem nem o cache do modelo. O `.gitignore` cobre `video/inputs/voice-ref/`, os áudios de `video/inputs/` e `video/outputs/`.

## Testes

Não precisam de GPU. O backend de síntese é o mock.

```bash
python3 -m unittest discover -s .agents/skills/narrar-roteiro/tests -v
```
