---
id: loudnorm
phase: render
---

# Feature · Loudnorm

## O que faz
Normaliza o áudio do Reel para **-14 LUFS / -1 dBTP / LRA 11** (dois passes), o
padrão de publicação.

## Como rodar
Rode o renderer desta skill **sem** `--no-loudnorm`:

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/final.mp4"
```

Preview rápido (ainda com loudnorm, qualidade de encode mais baixa):

```bash
PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project "$HOME/.claude/skills/video-use" \
  python .claude/skills/edit-video/assets/render_vertical.py \
  "<edit>/edl.json" -o "<edit>/preview.mp4" --preview
```

Só use `--no-loudnorm` se o usuário pedir explicitamente um render sem
normalização (debug). Nas rodadas de produção desta skill, o loudnorm é
obrigatório sempre que esta feature estiver no modo.
