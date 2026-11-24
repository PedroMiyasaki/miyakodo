---
name: deploy-instagram-autodm
description: >
  Publica o Worker instagram-autodm na Cloudflare depois de mudança de código.
  Use quando pedirem para fazer deploy, subir, publicar ou atualizar o Worker
  de resposta automática de comentários do Instagram, ou quando precisarem do
  passo a passo de app da Meta, D1, segredos, webhook, teste com wrangler tail
  e do dashboard /admin. Não use para criar ou alterar a regra de um post:
  isso é a skill registrar-resposta-automatica e o script build-respostas.
---

# Deploy do instagram-autodm

Este diretório é o Worker que responde comentários de palavra-chave na conta `@pedro.miyasaki.ia`. A fonte das automações são os arquivos `posts/<formato>/<slug>/respostas-comentarios.md`. Você não cadastra regra no dashboard.

O `README.md` é o texto original do projeto upstream. Os comandos de lá usam o nome antigo `manychat-lite-cloudflare` e mandam manter `DRY_RUN` em `"true"`. Aqui o Worker e o banco D1 se chamam `instagram-autodm`. Siga esta skill.

Produção, conferida em 24/11/2026:

- O Worker está no ar em `https://instagram-autodm.pedro-miyasaki.workers.dev`.
- Webhook: `https://instagram-autodm.pedro-miyasaki.workers.dev/webhook`.
- Dashboard: `https://instagram-autodm.pedro-miyasaki.workers.dev/admin`.
- `DRY_RUN` em `wrangler.jsonc` está `"false"`. O Worker envia direct e resposta pública.
- `COMMENT_POLL_ENABLED` está `"true"`.
- A conta Cloudflare do deploy é `ppgazolamiyasaki@gmail.com`, id `746d610009efa1ca1770cb8e0ec41093`.

Um deploy publica o código e as vars do `wrangler.jsonc`. Não altera segredo, token nem regra. Não edite segredo, token, `DRY_RUN` nem `COMMENT_POLL_ENABLED` sem o ok explícito do Pedro. Mudança de regra passa pelas skills `registrar-resposta-automatica` e `responder-comentarios`, com `build-respostas`. Não passa por deploy.

## Deploy depois de mudança de código

Este é o procedimento usado em 24/11/2026. Rode tudo a partir de `tools/instagram-autodm`, com o repositório na branch `main`. `git pull` funciona desse diretório: o git do miyakodo é o da raiz.

Não publique outra branch, árvore suja ou mudança local que o Pedro não pediu para ir ao ar. Se `git status` mostrar alteração fora do que ele acabou de aprovar, pare e avise.

1. Confira a branch e atualize `main`.

```bash
git status
git pull
```

2. Instale o que o lockfile pede.

```bash
npm ci
```

3. Os testes precisam ficar todos verdes. Se algum falhar, pare. Não faça deploy.

```bash
npm test
```

4. `npm run check` roda `tsc --noEmit` e `wrangler deploy --dry-run`. O dry-run não publica. Leia as vars impressas. `DRY_RUN` tem que aparecer `"false"`. `COMMENT_POLL_ENABLED` tem que aparecer `"true"`. `OWNER_IG_USERNAME` tem que aparecer `pedro.miyasaki.ia`. Se alguma var divergir do que está no `wrangler.jsonc` commitado, pare e mostre o diff ao Pedro.

```bash
npm run check
```

5. A conta do Wrangler tem que ser a de produção. Outra conta: pare. Não aplique migration e não faça deploy.

```bash
npx wrangler whoami
```

O resultado precisa mostrar o e-mail `ppgazolamiyasaki@gmail.com` e o account id `746d610009efa1ca1770cb8e0ec41093`.

6. Migration remota só entra se a mudança adicionou arquivo em `migrations/`. Sem arquivo novo, pule este comando.

```bash
npx wrangler d1 migrations apply instagram-autodm --remote
```

7. Publique.

```bash
npm run deploy
```

8. Anote o Version ID que o Wrangler imprimir e leve esse id na resposta ao Pedro.

9. Confira o que subiu, nesta ordem:

- `npx wrangler tail` e acompanhe o próximo evento.
- Abra `https://instagram-autodm.pedro-miyasaki.workers.dev/admin` com o `ADMIN_TOKEN`. O cabeçalho precisa indicar modo ao vivo.
- Um comentário real, de uma conta que ainda não recebeu o material daquele post. A conta `pedro.miyasaki.ia` não serve: comentário dela é ignorado. Com `DRY_RUN` em `"false"`, esse comentário envia direct de verdade. Não trate o log `dry_run_private_reply` como sucesso de produção. Esse log só aparece se `DRY_RUN` estiver `"true"`.

Não rode `npx wrangler secret put`. Não cole token em arquivo, em comando commitado nem na resposta.

## O que acontece num comentário

1. A pessoa comenta uma única palavra, igual à palavra-chave daquele post. Maiúsculas não importam. Espaço e pontuação nas pontas também não. `EVALS!` dispara. `quero evals` não. A palavra de um post não dispara em outro.
2. Comentário de `pedro.miyasaki.ia` é ignorado. Comentário genérico também. A mesma pessoa não recebe o material duas vezes no mesmo post.
3. Quando o Worker tem o id numérico de quem comentou, consulta se a pessoa segue. Se a primeira consulta diz que não segue, espera 4 segundos (`FOLLOWER_RECHECK_MS` em `wrangler.jsonc`) e consulta de novo antes de negar. Falha de consulta não conta como "não segue".
4. Quem já segue recebe o texto exato de `## Mensagem no direct`. O link, quando o markdown tem um, vai nesse texto.
5. Quem não segue recebe o texto exato de `## Pedido para seguir` e o botão "Já segui". Se a seção estiver vazia, o texto padrão é "Me segue por aqui para eu te enviar o material." Esse botão repete a consulta.
6. Se a consulta não confirma (sem id numérico, ou a segunda consulta não responde), o primeiro direct traz o texto fixo "Toque no botão para receber o material." e o botão "Quero o material".
7. A resposta de `## Resposta no comentário`, quando a regra tem uma, sai junto com esse primeiro direct. O clique no botão entrega o material e não publica outra resposta no mesmo comentário. Se a resposta pública falhou na primeira tentativa, o clique pode repetir só essa resposta.
8. No clique, a consulta roda de novo. Seguindo, sai o texto de `## Mensagem no direct`. Sem seguir, sai o pedido para seguir com "Já segui". Se a consulta falha no clique, o direct diz: "Não consegui confirmar se você segue a conta. Toque em Já segui para eu verificar de novo."

Os textos do material, da resposta pública e do pedido para seguir saem do markdown, sem reescrita.

A primeira vez, o Worker pode ler a lista de posts para ligar o código curto (por exemplo `DeU8X1fhF6a`) ao id numérico da Meta. É leitura. Se um post antigo não aparecer nessa lista, acrescente no markdown uma linha `- ID da mídia: 123` com o id numérico e rode o `build-respostas` de novo.

Os dois posts que serviram de prova no começo: `evals` no Reel `DeU8X1fhF6a`, `especialista` no Reel `DehPW4yCR7W`. A regra vigente é a dos markdowns atuais, não essa dupla.

## App da Meta

O app, o tester, o D1, os segredos e o webhook já existem. As seções abaixo guardam o procedimento. Não recrie nada disso num deploy comum.

A conta do Instagram precisa ser de criador ou empresa, e pública enquanto o app estiver em desenvolvimento.

1. Abra [Meta for Developers](https://developers.facebook.com/apps/) e crie um app.
2. No caso de uso, escolha **Manage messaging and content on Instagram**.
3. Entre no app e abra **Use cases, Manage messaging and content on Instagram, Customize**. Isso leva à tela **API setup with Instagram login**.
4. Não use token de Página do Facebook nem `graph.facebook.com`. Este Worker chama `https://graph.instagram.com/v25.0` (`GRAPH_API_BASE` no `wrangler.jsonc`).

Permissões usadas:

- `instagram_business_basic`
- `instagram_business_manage_comments`
- `instagram_business_manage_messages`

### Instagram Tester

No modo de desenvolvimento a Meta só autentica papéis do app.

1. No app, abra **App roles** ou **Roles**.
2. **Add people**, papel **Instagram Tester**.
3. Usuário `pedro.miyasaki.ia`, sem `@`.
4. No Instagram, com essa conta: **Settings, Website permissions, Apps and websites, Tester invitations**. Aceite o convite.
5. Volte ao painel da Meta e confira que o tester não está mais pendente.

### Token, ID e segredo

1. Em **API setup with Instagram login**, adicione a conta e aprove as permissões.
2. **Generate token**. Esse valor é o segredo `INSTAGRAM_ACCESS_TOKEN`. Não cole em arquivo commitado.
3. Se o painel mostrar o Instagram user ID, esse é o `IG_USER_ID`. Se não mostrar:

```bash
curl -G "https://graph.instagram.com/v25.0/me" \
  --data-urlencode "fields=user_id,username" \
  --data-urlencode "access_token=COLE_O_TOKEN"
```

Use o `user_id` da resposta, não o `id` do app.

4. Em **App settings, Basic, App secret**, copie o segredo. Esse valor é `INSTAGRAM_APP_SECRET`.

## D1

O banco `instagram-autodm` já existe. O `database_id` está no `wrangler.jsonc`: `0bb7752f-b57f-4e2b-b6ae-4b2acc9e6c45`. Não rode `d1 create` de novo.

O procedimento que criou o banco, para o caso de reconstruir do zero com o ok do Pedro:

```bash
npx wrangler login
npx wrangler d1 create instagram-autodm
```

O `database_id` impresso entra em `wrangler.jsonc`, no binding `DB`.

As migrations já aplicadas estão em `migrations/` (`0001` a `0009` na data desta skill). Num deploy comum, aplique de novo no remoto só se a mudança adicionou arquivo novo:

```bash
npx wrangler d1 migrations apply instagram-autodm --remote
```

## Segredos

Nomes, sem valores. Já estão na Cloudflare. Um deploy não mexe neles. Não rode `wrangler secret put` sem o Pedro passar o valor na hora e pedir a troca.

```bash
npx wrangler secret put WEBHOOK_VERIFY_TOKEN
npx wrangler secret put INSTAGRAM_APP_SECRET
npx wrangler secret put INSTAGRAM_ACCESS_TOKEN
npx wrangler secret put IG_USER_ID
npx wrangler secret put ADMIN_TOKEN
```

`WEBHOOK_VERIFY_TOKEN` e `ADMIN_TOKEN` são senhas inventadas. A do webhook é a mesma colada na Meta. `ADMIN_TOKEN` entra no dashboard em `/admin`.

`OWNER_IG_USERNAME` já está em `wrangler.jsonc` como `pedro.miyasaki.ia`. Não é segredo.

Para teste local, copie `.dev.vars.example` para `.dev.vars`. Esse arquivo está no `.gitignore`. O exemplo local deixa `DRY_RUN=true` e `COMMENT_POLL_ENABLED=false`. Isso vale só na máquina. Não copie esses dois para o `wrangler.jsonc`.

## Regras

Regra nova ou editada não pede deploy.

1. A skill `registrar-resposta-automatica` grava `posts/<formato>/<slug>/respostas-comentarios.md`.
2. No diretório `tools/instagram-autodm`:

```bash
node scripts/build-respostas.mjs --dry-run --remote
node scripts/build-respostas.mjs --remote
```

O primeiro só mostra o diff. O segundo cria, atualiza e pausa. Regra que sumiu dos markdowns fica pausada, não é apagada. Palavra-chave repetida entre posts ativos faz o comando falhar, sem gravar. Direct acima de 1000 bytes também.

Sem `--remote`, o comando só valida e escreve `data/automations.json`, que não vai para o git.

Não há GitHub Action. A pasta `posts/` está no `.gitignore`, então um workflow no GitHub não veria esses markdowns. O sync fica na máquina do Pedro.

## Webhook

Já aponta para `https://instagram-autodm.pedro-miyasaki.workers.dev/webhook`. Não reconfigure num deploy comum.

No app da Meta, em **API setup with Instagram login**, os campos são:

- Callback: `https://instagram-autodm.pedro-miyasaki.workers.dev/webhook`
- Verify token: o mesmo `WEBHOOK_VERIFY_TOKEN`
- Campos: `comments`, `messages`, `messaging_postbacks`

O campo `messaging_postbacks` é o toque no botão. Sem ele, o material não sai no clique.

A assinatura da conta, se precisar refazer, troca os dois placeholders. Não cole o token de verdade no comando que for parar no histórico:

```bash
curl -X POST "https://graph.instagram.com/v25.0/COLE_IG_USER_ID/subscribed_apps" \
  --data-urlencode "subscribed_fields=comments,messages,messaging_postbacks" \
  --data-urlencode "access_token=COLE_O_TOKEN"
```

## Envio

O envio já está ligado. `DRY_RUN` é `"false"` e o Worker responde de verdade.

O que esse valor faz: com `"true"`, o Worker registra o match e não manda direct nem resposta pública. O log fica `dry_run_private_reply`. Com `"false"`, o direct sai. Quem segue recebe o material. Quem não segue recebe o pedido para seguir. A resposta pública, quando existe, sai com o primeiro direct.

Não volte `DRY_RUN` para `"true"` e não troque para outro valor sem o ok explícito do Pedro. A troca pede deploy de novo.

Abra `/admin` com o `ADMIN_TOKEN` para ver a atividade. As regras dos markdowns também aparecem lá. Se você editar uma nesse dashboard, o próximo `build-respostas --remote` cobre com o texto do arquivo.

## Post novo

1. Crie ou atualize `respostas-comentarios.md` na pasta da peça. A skill `registrar-resposta-automatica` faz isso.
2. Rode `node scripts/build-respostas.mjs --dry-run --remote` e, se o diff estiver certo, `node scripts/build-respostas.mjs --remote`.

Não faça deploy por causa de texto de regra.

## Polling de reserva

A Meta não é clara sobre webhook de comentário sem App Review. O cron `*/5 * * * *` já está no Worker. Ele lê comentários quando `COMMENT_POLL_ENABLED` é `"true"`. Em produção essa var está `"true"`. Não desligue sem o ok do Pedro.

Ligado, a cada poucos minutos o Worker lê `GET /<media-id>/comments` dos posts ativos e passa pelo mesmo filtro e pela mesma deduplicação. Comentário com mais de 7 dias fica de fora: a Meta não aceita private reply depois disso.

O polling chama a API de leitura mesmo se `DRY_RUN` fosse `"true"`. O envio continua bloqueado pelo `DRY_RUN`. Hoje o envio está liberado, então comentário lido pelo polling também pode gerar direct.

## O que só o teste real confirma

O Worker já envia em produção. Estes pontos continuam dependendo da Meta. Código e dry-run não fecham sozinhos:

- Se o webhook de `comments` chega nesta conta sem App Review e sem Advanced Access. No modo de desenvolvimento, a Meta às vezes só entrega eventos de quem tem papel no app. O polling está ligado por causa dessa incerteza.
- Se o private reply desta conta aceita o botão de postback. O código manda o button template que a API documenta. A conta precisa aceitar.
- Se `is_user_follow_business` responde certo depois do toque no botão, inclusive o atraso logo depois que a pessoa segue. Por isso a segunda consulta espera 4 segundos.

## Renovação do token

O token da Instagram Login dura cerca de 60 dias. Com `DRY_RUN` em `"false"`, o cron das 06:00 UTC renova o token e guarda a versão nova criptografada no D1. A produção está nesse modo, então a renovação roda. Enquanto `DRY_RUN` for `"true"`, a checagem e a renovação ficam desligadas.

Para confirmar que o token é da conta do `IG_USER_ID`, entre em `/admin`, abra a conexão do Instagram e rode a checagem. Não troque o token à mão sem o Pedro pedir.
