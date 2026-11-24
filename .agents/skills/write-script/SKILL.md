---
name: write-script
description: >
  Lê uma ideia do banco Ideas e produz um roteiro de Reel completo, na voz do
  usuário e no formato híbrido do teleprompter. A ideia costuma chegar como
  análise; o roteiro deve sair como história. O trabalho não é resumir, mas
  transformar a matéria-prima em storytelling autoritativo, interessante e
  valioso para quem assiste. Ative com pedidos como "escreve o roteiro da
  última ideia", "roteiro da ideia X" ou "escreve o roteiro".
---

# Roteiro de Reel

## Git

Peça desta skill entra por commit direto na `main`. Não abra pull request e não crie branch para o conteúdo. Rascunho e versão final são conteúdo. Saída intermediária ou que dá para gerar de novo fica de fora do git, no caminho coberto pelo `.gitignore`.

## Quando ativar

Use esta skill quando o usuário pedir para transformar uma ideia em roteiro de Reel.

## Fonte

O banco canônico é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`. Leia a ideia no começo e, no fechamento, atualize somente `Status` e `Format`.

## Formato: literal e tópicos

O usuário não lê o roteiro inteiro palavra por palavra. Use dois modos:

- **Literal:** texto falado exatamente como está escrito. Funciona especialmente bem onde a escolha das palavras sustenta a retenção.
- **Tópicos:** pistas curtas, em ordem, para o usuário explicar com naturalidade.

Todo bloco declara o modo no cabeçalho, como `[HOOK] · literal` ou `[CONTEXTO] · tópicos`, e usa apenas um modo. Os nomes e a quantidade dos blocos dependem da história.

## Protocolo de execução

### Passo 1 · Identificar a ideia

Se o usuário indicou uma ideia, encontre essa linha em **Ideas** e use-a. Caso contrário, selecione a ideia `Pending` mais recente, usando `Date` e depois `createdTime` como desempate, mostre o título e confirme antes de seguir.

### Passo 2 · Ler a ideia

Leia tudo que estiver disponível na linha: título, notas, exemplos, links, data e status. Entenda a ideia e defina também a fase ACP.

### Passo 3 · Calibrar pelo histórico

Liste os slugs mais recentes em `posts/script/` e leia a última versão de até cinco roteiros: `final.md` quando existir ou o `sketch/v<N>.md` de maior número.

Use esses textos como few-shot, não como checklist. Observe vocabulário, registro, construção das frases, ritmo, densidade técnica, maneira de explicar conceitos, uso de primeira pessoa, opinião, humor, aberturas, encerramentos, tamanho e equilíbrio entre literal e tópicos. Imite os padrões recorrentes sem copiar frases e dê mais peso aos exemplos recentes.

Se houver menos de cinco, use o que existir. Se não houver nenhum, siga sem calibração.

### Passo 4 · Planejar o storytelling

Assuma o papel de um copywriter experiente em Reels. Escolha a estrutura que melhor serve à ideia e transforme o material em uma história clara, envolvente e natural.

Priorize um gancho forte, porque ele decide se o vídeo será assistido. Depois, conduza a atenção com boa progressão, tensão, viradas e uma recompensa que cumpra a promessa inicial. Busque potencial de compartilhamento e retenção sem forçar uma fórmula ou distorcer a ideia.

Faça esse planejamento nas suas notas de trabalho. Não apresente uma etapa separada ao usuário.

### Passo 5 · Escrever o roteiro

Escreva o roteiro seguindo o formato híbrido de literal e tópicos. Escolha livremente os blocos, a duração e a estrutura narrativa adequados à ideia.

### Passo 7 · Apresentar, salvar e iterar

Derive o slug do título da ideia: minúsculas, sem acento e com hífens no lugar de espaços e pontuação.

Ao apresentar a primeira versão, salve-a em:

```text
posts/script/<slug>/sketch/v1.md
```

Apresente o roteiro, informe o caminho e pergunte se está pronto ou se precisa de correções.

Cada rodada de feedback cria `sketch/v<N+1>.md`. Leia a versão anterior, preserve verbatim tudo que não precisa mudar e aplique somente o necessário. Repita até o usuário dizer explicitamente "pronto".

### Passo 8 · Fechar

Quando o usuário disser "pronto", copie a versão de maior número verbatim para:

```text
posts/script/<slug>/final.md
```

Mantenha o histórico em `sketch/`. Depois atualize a ideia de origem em **Ideas** para `Status` = `Processed` e `Format` = `Reel`. Essa é a única escrita no Notion.

### Passo 9 · Confirmar

Informe que o roteiro está pronto, indique o caminho de `final.md` e aponte a gravação do Reel como próximo passo.
