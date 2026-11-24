---
name: responder-comentarios
description: >
  A resposta automática de comentários do Instagram roda no Worker em
  tools/instagram-autodm. A automação de navegador está aposentada. Use quando
  o usuário perguntar como os comentários são atendidos ou for publicar a
  resposta de um post. Não abra o Instagram no navegador para responder.
---

# Responder comentários

O atendimento de palavra-chave saiu do navegador. O Worker em `tools/instagram-autodm` recebe o comentário pela API oficial da Meta, manda um botão no direct e só entrega o material para quem segue `@pedro.miyasaki.ia`.

Não use automação de navegador para responder comentários. Essa rotina está aposentada. O checkpoint do Instagram em 2026-10-18 encerrou esse caminho.

## Publicar ou atualizar uma resposta

1. A orientação continua em `posts/<formato>/<slug>/respostas-comentarios.md`. Quem cria esse arquivo é a skill `registrar-resposta-automatica`.
2. No diretório `tools/instagram-autodm`, rode `node scripts/build-respostas.mjs --dry-run --remote` para ver o diff e `node scripts/build-respostas.mjs --remote` para gravar no D1.
3. O passo a passo de app da Meta, Cloudflare, segredos, deploy e teste está em `tools/instagram-autodm/SETUP-PEDRO.md`.

O comentário dispara só quando é uma única palavra igual à palavra-chave daquele post. `EVALS!` dispara. `quero evals` não. A palavra não vale em outro post.

O primeiro direct sai no comentário. Quem já segue recebe o texto de `## Mensagem no direct`. Quem não segue recebe o texto de `## Pedido para seguir` e o botão "Já segui". Quando a checagem não confirma, o direct traz o botão "Quero o material". A resposta pública, quando a regra tem uma, sai junto com esse primeiro direct. O clique no botão entrega o material e não publica outra resposta no mesmo comentário.

## Estado antigo

`estado.md` é o histórico da varredura feita pelo navegador até 2026-10-18. Não retome esses atendimentos pelo navegador.

`@ayrtonsilvapmp`, `@cdreina`, `@joelvictor__` e `@rodrigociabatari` receberam o pedido para seguir e não tinham seguido até a última checagem. Os comentários deles têm mais de sete dias. A API não aceita private reply nesse prazo, então não vale migrar a lista. Se comentarem a palavra de novo, o Worker atende.
