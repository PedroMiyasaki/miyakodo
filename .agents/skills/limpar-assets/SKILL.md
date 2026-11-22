---
name: limpar-assets
description: >
  Limpa vídeos de input e arquivos intermediários de edição, preservando as
  entregas finais. Use quando o usuário pedir para limpar assets, liberar
  espaço em disco, apagar MP4 de input, snippets, cortes, renders
  intermediários, cache de transcode ou pedaços usados na montagem de um vídeo.
---

# Limpar assets de vídeo

Apaga vídeo de input e vídeo intermediário da montagem. A entrega final permanece no disco.

Quem apaga é `classificar.py`. O relatório sem `--apply` não remove nada. Depois do sim do usuário, `--apply` apaga só o que o próprio script listou como `excluir`.

## Papéis

| Papel | Onde está | Destino |
|---|---|---|
| Entrega | `posts/`, `video/outputs/`, e na raiz de `videos/<slug>/` um arquivo com `editado`, `reels` ou `video` no nome | manter |
| Biblioteca de ganchos | `video/hooks/`, inclusive `originais/` | manter |
| Input | `video/inputs/` | excluir se a peça já tem entrega; senão, rever |
| Intermediário | `assets/`, `.media/`, `renders/`, `.transcode-cache/` dentro de `video/projects/<slug>/` ou `videos/<slug>/`; `input-video` em `public/` | excluir se a peça já tem entrega; senão, rever |
| Export numerado | `output-<número>` na raiz de `videos/<slug>/` | rever |
| Qualquer outro vídeo | caminho que não entra nas linhas acima | rever |

A peça "já tem entrega" quando o slug da pasta, ou o nome do arquivo em `video/inputs/`, aparece no caminho de um vídeo mantido fora de `video/hooks/`. `tier_list` casa com `tier-list-de-casos-de-uso-de-ia`. Sem esse elo, o arquivo fica em `rever`.

Duplicata de entrega também fica. Esta skill não compara arquivos para deduplicar.

Áudio, imagem, legenda, HTML e a pasta do projeto HyperFrames ficam. A limpeza é só destes vídeos: `.mp4`, `.mov`, `.m4v`, `.webm`, `.mkv`.

## Exemplos

- `video/inputs/peca.MP4` com `posts/script/peca/reels.mp4` presente: excluir o input, manter o `reels.mp4`.
- `video/projects/peca/renders/rascunho.mp4` com `video/outputs/peca.mp4` presente: excluir o render, manter a saída.
- `video/hooks/cafe_cortado.mp4`: manter. O modo Lista com gancho sorteia de novo a partir daqui.
- `video/projects/rascunho/assets/corte.mp4` sem vídeo correspondente em `posts/` nem em `video/outputs/`: rever.

## Procedimento

1. Na raiz do repositório, gere o relatório. Sem `--apply`.

```bash
python .agents/skills/limpar-assets/classificar.py
```

2. Mostre as três listas (`manter`, `excluir`, `rever`) com o tamanho de cada arquivo e o total de `excluir`.
3. Pare. A exclusão espera um sim explícito nesta conversa, depois desse relatório.
4. Com o sim, rode o mesmo comando com `--apply`.
5. Se o sim incluir caminhos de `rever`, repita o `--apply` com um `--incluir` por caminho, exatamente como o relatório mostrou:

```bash
python .agents/skills/limpar-assets/classificar.py --apply --incluir video/projects/exemplo/renders/rascunho.mp4
```

`--incluir` só aceita caminho que esteja em `rever`. Entrega, gancho e qualquer caminho fora de `rever` fazem o script encerrar sem apagar nada. Nesse caso, relate a recusa e pare.

6. Depois do `--apply`, rode o relatório de novo e confirme que `excluir` ficou vazio e que as entregas continuam na lista `manter`.
