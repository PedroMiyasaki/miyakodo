---
name: registrar-resposta-automatica
description: >
  Registra ou atualiza a orientação de respostas a comentários na pasta local
  de um Reel ou carrossel, a partir do post do Instagram informado pelo usuário.
  Use com pedidos como "registra a resposta automática desse post" ou
  "quando comentarem essa palavra, envie esse material".
---

# Registrar resposta automática

Recebe um post do Instagram e salva `respostas-comentarios.md` na pasta da peça. Esse arquivo é a fonte das automações do Worker em `tools/instagram-autodm`. A skill [responder-comentarios](../responder-comentarios/SKILL.md) não envia mais mensagens pelo navegador. Registrar uma orientação não envia mensagens nem executa atendimentos.

## Entrada

O parâmetro principal é o link de um **Reel ou carrossel**. A palavra-chave, o material e as mensagens podem vir no mesmo pedido, na conversa ou no conteúdo local do post. Uma referência como "esse Reel aberto" também vale quando identificar a publicação sem dúvida. Se não houver um post identificável, peça o link.

Exemplo de chamada:

```text
$registrar-resposta-automatica <link-do-post> palavra <palavra-chave>, envie <link-do-material>
```

## 1. Localizar a pasta da publicação

Procure a URL ou o código do post em `posts/`, inclusive em orientações já existentes. URLs `/p/<codigo>/` e `/reel/<codigo>/` podem identificar a mesma publicação. Compare o código preservando maiúsculas e minúsculas; parâmetros de compartilhamento não identificam outro post.

Se ainda não houver vínculo local, use o navegador do Codex para ler a publicação informada e comparar legenda, CTA e conteúdo com as peças locais. Confira que o post pertence a `@pedro.miyasaki.ia`; se o link for de outro perfil, peça a publicação correta. Reels costumam estar em `posts/script/`; carrosséis, em `posts/carousel/` ou em `posts/thread/` quando derivados de threads. Procure também nas outras pastas de `posts/` se necessário, sem mover a peça para adequá-la a essa convenção.

Use a pasta indicada pelo usuário ou uma correspondência inequívoca com o conteúdo da publicação. Sem correspondência ou com mais de uma candidata, peça a pasta ou o slug correto. Não crie uma pasta nova só para acomodar o link nem escolha pela semelhança do tema. Se a publicação estiver inacessível e não houver informação suficiente no pedido ou nos arquivos, peça a identificação que faltar.

## 2. Determinar a orientação

Leia o registro existente, quando houver, e o conteúdo pertinente da pasta: legenda, versão final e contexto da entrega. A instrução atual do usuário prevalece sobre o registro anterior. Aproveite o que já estiver definido, sem pedir de novo.

Defina:

- **Publicação:** URL, código, conta e tipo, Reel ou carrossel. Não deduza o tipo somente pelo caminho `/p/` ou `/reel/`.
- **Palavra-chave:** a palavra que dispara a entrega. Aproveite a palavra do CTA se estiver explícita. A skill de atendimento aceita comentários de uma única palavra; se o pedido definir uma expressão de várias palavras, peça uma palavra compatível. Mais de uma palavra-chave só entra quando solicitada, com a mesma entrega ou com mensagens claramente associadas a cada uma.
- **Mensagem no direct:** texto completo e o link ou material que deve ser entregue. Use o material indicado pelo usuário ou claramente definido como a entrega do post. Uma fonte citada no roteiro não é automaticamente o material prometido.
- **Resposta no comentário:** texto a publicar depois da confirmação da DM. Se o usuário não ditar a mensagem, redija uma resposta curta e natural, como `Enviei no direct.`.
- **Pedido para seguir:** use o texto indicado ou `Me segue por aqui para eu te enviar o material.`.

Se houver informação suficiente, redija as mensagens e salve sem pedir aprovação adicional. Preserve textos ditados pelo usuário; ao redigir, siga a voz do `AGENTS.md`. Se faltar a palavra-chave, o destino da entrega ou outra informação indispensável, pergunte apenas o que faltar antes de gravar. Não salve mensagens de envio com links inventados, campos vazios ou placeholders.

O atendimento continua restrito a seguidores. O pedido para seguir não entrega o material. Quem envia é o Worker, depois que você roda `node scripts/build-respostas.mjs --remote` em `tools/instagram-autodm`. Não copie a lógica de envio para o markdown.

## 3. Gravar no padrão

Para um registro novo, crie `respostas-comentarios.md` **na raiz da pasta da peça**, ao lado dos arquivos finais, usando este padrão e substituindo todos os campos:

```markdown
# Respostas para comentários

- Post do Instagram: <URL da publicação>
- Código do post: <código preservando maiúsculas e minúsculas>
- Conta: @pedro.miyasaki.ia
- Tipo: <Reel ou Carrossel>
- Palavra-chave: <palavra configurada>
- Somente seguidores: sim

## Mensagem no direct

<texto completo da mensagem, com o link da entrega quando houver>

## Resposta no comentário

<texto completo da resposta pública>

## Pedido para seguir

<texto completo do pedido para seguir>
```

Se o arquivo já existir, edite somente o que o pedido altera e preserve as demais palavras-chave, mensagens, metadados e orientações. Não reformate o registro inteiro para encaixá-lo no template. Se a pasta já tiver a orientação em outro Markdown, mantenha um único registro: atualize-o ou use o nome padrão quando isso não afetar outras referências, sem deixar duas instruções concorrentes.

## 4. Conferir e entregar

Releia o arquivo salvo e confira a associação com a publicação, a palavra-chave e o destino da entrega. Verifique que o texto está completo e que uma atualização preservou tudo que não foi solicitado.

Informe o caminho clicável do arquivo e resuma a palavra-chave e as mensagens registradas. Não altere o estado de `responder-comentarios`, o status da ideia no Notion nem a publicação no Instagram. Criar ou revisar esta skill também não registra uma orientação para um post por conta própria.
