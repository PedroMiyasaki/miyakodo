# Resposta automática no Instagram

Este diretório é o Worker que responde comentários de palavra-chave na conta `@pedro.miyasaki.ia`. A fonte das automações são os arquivos `posts/<formato>/<slug>/respostas-comentarios.md`. Você não cadastra regra no dashboard.

O `README.md` é o texto original do projeto. Os comandos de lá usam o nome antigo `manychat-lite-cloudflare`. Aqui o Worker e o banco D1 se chamam `instagram-autodm`. Siga este arquivo.

Nada aqui foi publicado na Cloudflare nem chamado na API da Meta. `DRY_RUN` está `"true"`: nesse modo o Worker não envia direct nem resposta pública.

## O que acontece num comentário

1. A pessoa comenta uma única palavra, igual à palavra-chave daquele post. Maiúsculas não importam. Espaço e pontuação nas pontas também não. `EVALS!` dispara. `quero evals` não. A palavra de um post não dispara em outro.
2. O Worker manda um private reply com o botão "Quero o material". O texto desse primeiro direct é fixo: "Toque no botão para receber o material." O link ainda não vai.
3. Quando a pessoa toca o botão, a API já pode dizer se ela segue a conta. Se segue, o Worker manda o texto exato de `## Mensagem no direct` e, só depois disso, a resposta de `## Resposta no comentário`.
4. Se não segue, manda o texto exato de `## Pedido para seguir` com o botão "Já segui". Esse botão repete a checagem.
5. Se a primeira checagem diz que a pessoa não segue, o Worker espera 4 segundos e checa de novo antes de negar. O atraso da API logo depois do follow é comum. Se a checagem falha, ele não trata a pessoa como quem não segue: pede para tocar de novo.
6. A mesma pessoa não recebe o material duas vezes no mesmo post. Comentário seu (`pedro.miyasaki.ia`) é ignorado. Comentário genérico também.

Os textos do material, da resposta pública e do pedido para seguir saem do markdown, sem reescrita.

## Ordem do que você faz

Faça nesta ordem. Tudo a partir de `tools/instagram-autodm`, salvo o app da Meta.

### 1. Criar o app na Meta

A conta do Instagram precisa ser de criador ou empresa, e pública enquanto o app estiver em desenvolvimento.

1. Abra [Meta for Developers](https://developers.facebook.com/apps/) e crie um app.
2. No caso de uso, escolha **Manage messaging and content on Instagram**.
3. Entre no app e abra **Use cases, Manage messaging and content on Instagram, Customize**. Isso leva à tela **API setup with Instagram login**.
4. Não use token de Página do Facebook nem `graph.facebook.com`. Este Worker chama `https://graph.instagram.com/v25.0`.

Permissões usadas:

- `instagram_business_basic`
- `instagram_business_manage_comments`
- `instagram_business_manage_messages`

### 2. Te adicionar como Instagram Tester

No modo de desenvolvimento a Meta só autentica papéis do app.

1. No app, abra **App roles** ou **Roles**.
2. **Add people**, papel **Instagram Tester**.
3. Usuário `pedro.miyasaki.ia`, sem `@`.
4. No Instagram, com essa conta: **Settings, Website permissions, Apps and websites, Tester invitations**. Aceite o convite.
5. Volte ao painel da Meta e confira que o tester não está mais pendente.

### 3. Gerar o token, o ID e o segredo

1. Em **API setup with Instagram login**, adicione a conta e aprove as permissões.
2. **Generate token**. Esse valor é `INSTAGRAM_ACCESS_TOKEN`. Não cole em arquivo commitado.
3. Se o painel mostrar o Instagram user ID, esse é o `IG_USER_ID`. Se não mostrar:

```bash
curl -G "https://graph.instagram.com/v25.0/me" \
  --data-urlencode "fields=user_id,username" \
  --data-urlencode "access_token=COLE_O_TOKEN"
```

Use o `user_id` da resposta, não o `id` do app.

4. Em **App settings, Basic, App secret**, copie o segredo. Esse valor é `INSTAGRAM_APP_SECRET`.

### 4. Criar o D1 e aplicar as migrations

```bash
npx wrangler login
npx wrangler d1 create instagram-autodm
```

Copie o `database_id` para `wrangler.jsonc`, no lugar de `REPLACE_WITH_D1_DATABASE_ID`.

```bash
npx wrangler d1 migrations apply instagram-autodm --remote
```

### 5. Segredos

```bash
npx wrangler secret put WEBHOOK_VERIFY_TOKEN
npx wrangler secret put INSTAGRAM_APP_SECRET
npx wrangler secret put INSTAGRAM_ACCESS_TOKEN
npx wrangler secret put IG_USER_ID
npx wrangler secret put ADMIN_TOKEN
```

`WEBHOOK_VERIFY_TOKEN` e `ADMIN_TOKEN` são senhas que você inventa. A do webhook precisa ser a mesma que você cola na Meta. `ADMIN_TOKEN` entra no dashboard em `/admin`.

`OWNER_IG_USERNAME` já está em `wrangler.jsonc` como `pedro.miyasaki.ia`. Não precisa de secret.

Para teste local, copie `.dev.vars.example` para `.dev.vars`. Esse arquivo está no `.gitignore`.

### 6. Gravar as regras que já existem

Os dois markdowns atuais (`evals` e `especialista`) entram assim:

```bash
node scripts/build-respostas.mjs --dry-run --remote
node scripts/build-respostas.mjs --remote
```

O primeiro só mostra o diff. O segundo cria, atualiza e pausa. Regra que sumiu dos markdowns fica pausada, não é apagada. Palavra-chave repetida entre posts ativos faz o comando falhar, sem gravar. Direct acima de 1000 bytes também.

Sem `--remote`, o comando só valida e escreve `data/automations.json`, que não vai para o git.

### 7. Deploy em modo de teste

Confira que `DRY_RUN` em `wrangler.jsonc` continua `"true"`.

```bash
npm run check
npm run deploy
```

A URL fica neste formato:

```text
https://instagram-autodm.<sua-subdomain>.workers.dev/webhook
https://instagram-autodm.<sua-subdomain>.workers.dev/admin
```

### 8. Webhook

No app da Meta, em **API setup with Instagram login**, configure o webhook:

- Callback: `https://instagram-autodm.<sua-subdomain>.workers.dev/webhook`
- Verify token: o mesmo `WEBHOOK_VERIFY_TOKEN`
- Campos: `comments`, `messages`, `messaging_postbacks`

O campo `messaging_postbacks` é o toque no botão. Sem ele, o material não sai.

Assine a conta. Troque os dois valores:

```bash
curl -X POST "https://graph.instagram.com/v25.0/COLE_IG_USER_ID/subscribed_apps" \
  --data-urlencode "subscribed_fields=comments,messages,messaging_postbacks" \
  --data-urlencode "access_token=COLE_O_TOKEN"
```

### 9. Testar sem enviar

```bash
npx wrangler tail
```

De outra conta, comente `evals` no Reel `DeU8X1fhF6a`, ou `especialista` no Reel `DehPW4yCR7W`. No log, o comentário certo aparece como `dry_run_private_reply`. `quero evals` não dispara. Nesse modo nada é enviado.

A primeira vez, o Worker pode ler a lista de posts para ligar o código (`DeU8X1fhF6a`) ao id numérico da Meta. É só leitura. Enquanto `DRY_RUN` for `"true"`, ele não manda mensagem. Se um post antigo não aparecer nessa lista, acrescente no markdown uma linha `- ID da mídia: 123` com o id numérico e rode o `build-respostas` de novo.

### 10. Ligar o envio

Quando o teste acima bater com o comentário certo:

1. Em `wrangler.jsonc`, mude `DRY_RUN` para `"false"`.
2. `npm run deploy` de novo.
3. Comente de novo, com uma conta que ainda não recebeu aquele material. O direct deve trazer o botão, não o link.
4. Toque o botão. Seguindo a conta, o material chega e a resposta pública aparece no comentário. Sem seguir, chega o pedido para seguir.

Abra `/admin` com o `ADMIN_TOKEN` para ver a atividade. As regras dos markdowns também aparecem lá. Se você editar uma nesse dashboard, o próximo `build-respostas --remote` cobre com o texto do arquivo.

### 11. Post novo

1. Crie ou atualize `respostas-comentarios.md` na pasta da peça. A skill `registrar-resposta-automatica` faz isso.
2. Rode `node scripts/build-respostas.mjs --remote`.

Não há GitHub Action. A pasta `posts/` está no `.gitignore`, então um workflow no GitHub não veria esses markdowns. O sync fica na sua máquina.

## Polling de reserva

A Meta não é clara sobre webhook de comentário sem App Review. O cron `*/5 * * * *` já está no Worker, mas não lê comentários enquanto `COMMENT_POLL_ENABLED` for `"false"`.

Se no teste o webhook não chegar, mude essa variável para `"true"`, faça deploy e comente de novo. A cada poucos minutos o Worker lê `GET /<media-id>/comments` dos posts ativos e passa pelo mesmo filtro e pela mesma deduplicação. Comentário com mais de 7 dias fica de fora: a Meta não aceita private reply depois disso.

Deixe o polling desligado no primeiro teste. Ligado, ele chama a API de leitura mesmo com `DRY_RUN` `"true"`. O envio continua bloqueado pelo `DRY_RUN`.

## O que só o teste real confirma

- Se o webhook de `comments` chega nesta conta sem App Review e sem Advanced Access. No modo de desenvolvimento, a Meta às vezes só entrega eventos de quem tem papel no app.
- Se o private reply desta conta aceita o botão de postback. O código manda o mesmo formato de button template que a API documenta. A conta precisa aceitar.
- Se `is_user_follow_business` responde certo depois do toque no botão, inclusive o atraso logo depois que a pessoa segue.

## Renovação do token

O token da Instagram Login dura cerca de 60 dias. Com `DRY_RUN` em `"false"`, o cron das 06:00 UTC renova o token e guarda a versão nova criptografada no D1. Depois do primeiro deploy com token de verdade, entre em `/admin`, abra a conexão do Instagram e rode a checagem. Isso confirma que o token é da conta do `IG_USER_ID`.

Enquanto `DRY_RUN` for `"true"`, essa checagem e a renovação ficam desligadas.
