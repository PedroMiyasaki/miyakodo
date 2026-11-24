---
name: deploy-instagram-autodm
description: >
  Publica o Worker instagram-autodm na Cloudflare depois de mudança de código.
  Use quando pedirem para fazer deploy, subir, publicar ou atualizar o Worker
  de resposta automática de comentários do Instagram. A skill canônica está em
  tools/instagram-autodm. Não use para criar ou alterar a regra de um post:
  isso é registrar-resposta-automatica e o script build-respostas.
---

# Deploy do instagram-autodm

A skill canônica está em `tools/instagram-autodm/.agents/skills/deploy-instagram-autodm/SKILL.md`. Leia esse arquivo e siga só ele. Este ponteiro existe para o agente na raiz do repositório encontrar o procedimento quando ainda não está mexendo em arquivos de `tools/instagram-autodm`.

Não duplique os passos aqui. Não edite segredo, token, `DRY_RUN` nem `COMMENT_POLL_ENABLED`. Não faça deploy a partir deste texto.
