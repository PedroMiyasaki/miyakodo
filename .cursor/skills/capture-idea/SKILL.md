---
name: capture-idea
description: >
  Captura as ideias cruas, os aforismos e os pensamentos soltos do usuário, classifica
  cada um numa ACP Phase e registra tudo com estrutura mínima no banco Ideas do Notion.
  Ative com comandos como "captura essa ideia", "guarda esse pensamento", ou sempre
  que o usuário mandar qualquer ideia ou pensamento que possa virar conteúdo depois.
---
## Captura contínua de ideias cruas

Propósito: receber as ideias do usuário em estado bruto (aforismos, observações soltas, pensamentos guardados para virar conteúdo depois), dar a elas uma estrutura mínima, classificar numa ACP Phase e gravar no banco Ideas do Notion, deixando tudo pronto para virar conteúdo quando o usuário pedir.

Opere com zero atrito **para o usuário**: ele não escolhe formato, ângulo nem fase, só registra o pensamento. Toda a estruturação, classificação e registro é trabalho desta skill. A classificação é trabalho interno, nunca uma pergunta devolvida ao usuário.

---

## Ferramentas disponíveis

- **Notion MCP**: escrever no banco Ideas.

---

## Banco de destino

| Objeto | ID |
|---|---|
| **Ideas** (data source) | `e2970ca3-7724-4a81-8f12-7ea34c048c67` |

Campos do banco:
- `Idea`: título (texto livre, campo principal)
- `Date`: data da entrada (preencha com a data de hoje)
- `Status`: sempre `"Pending"` na criação
- `Notes`: campo livre para contexto extra
- `ACP Phase`: estágio de funil da ideia, classificado por esta skill (Passo 3), sempre um de `"A · Audience"`, `"C · Community"`, `"P · Product"`
- `Format`: formato da peça produzida. **Não preencha na captura.** A ideia nasce sem formato: a skill de produção decide e registra o formato quando fecha a peça
---

## Quando agir

Aja sempre que o usuário mandar qualquer coisa que pareça ideia, observação, aforismo, insight ou pensamento solto, mesmo incompleto ou abstrato. Não exija um comando específico. Se a mensagem parece uma ideia, capture.

Exemplos de entrada válida:
- "E se eu fizesse um reel sobre como a IA falha em projetos de verdade?"
- "Autonomia total é uma armadilha"
- "A maioria das empresas não tem problema de IA, tem problema de processo"
- "Ideia: comparar implantação de IA com reforma de casa"
- Qualquer coisa que seja claramente um pensamento guardado para virar conteúdo depois
---

## Protocolo de execução

### Passo 1 · Interpretar a ideia

Leia a mensagem do usuário. Identifique:
- O núcleo do pensamento (1 frase)
- Se existe um ângulo implícito (provocação, comparação, caso, opinião)
- Se existe uma audiência implícita (CEO, gestor, engenheiro)
Não faça perguntas nem peça confirmação antes de processar e registrar.

### Passo 2 · Dar estrutura mínima

Transforme a ideia crua numa entrada limpa com:

**Título da ideia:** uma versão concisa e direta do pensamento central, escrita em português. No máximo 10 palavras. Tem que ler como título de post ou como o núcleo de um argumento, não como descrição de tarefa.

Exemplos:
- Entrada: "e se eu fizesse um reel sobre como a maioria das empresas erra na implantação de IA"
- Título: "Por que a implantação de IA falha antes da produção"
- Entrada: "autonomia total é uma armadilha"
- Título: "Autonomia total de IA cria sistemas que ninguém entende"
**Notas (opcional):** se o usuário mandou contexto extra, frases de exemplo, ou a ideia já veio com algum desenvolvimento, cole isso no campo Notes como está, sem reescrever. É o despejo bruto para consulta futura.

### Passo 3 · Classificar a ACP Phase

Essa classificação é mecânica, não qualitativa: você está categorizando a ideia, não julgando se ela é boa (isso fica fora do escopo, ver a seção abaixo).

**Classificando a `ACP Phase`:** decida em duas etapas.
1. **`P · Product`** se a ideia descreve um caso, projeto ou resultado real e mensurável do usuário (um projeto entregue a um cliente, uma métrica concreta) presente de forma explícita no texto dele. Não infira Product de uma ideia hipotética ou genérica só porque ela *poderia* virar um caso um dia.
2. Senão, decida entre **`A · Audience`** e **`C · Community`**: se a ideia pegaria alguém que ainda não segue o usuário, só pela curiosidade técnica, `A · Audience`. Se ela só faz sentido para quem já segue e quer ir mais fundo, `C · Community`.

### Passo 4 · Salvar no Notion

Crie uma linha nova no banco `e2970ca3-7724-4a81-8f12-7ea34c048c67` com:

| Campo | Valor |
|---|---|
| `Idea` | Título estruturado, em português (no máximo 10 palavras) |
| `Date` | Data de hoje (formato ISO) |
| `Status` | `Pending` |
| `Notes` | O texto original do usuário + qualquer contexto relevante, em português |
| `ACP Phase` | Um de `"A · Audience"`, `"C · Community"`, `"P · Product"` (texto exato, incluindo o `·`) |

### Passo 5 · Confirmar no mínimo

Responda com uma confirmação curta, de no máximo uma linha, com o título e a classificação. Não resuma, não parafraseie, não elogie, não justifique a classificação.

Resposta ideal:
> Salvo: "Por que a implantação de IA falha antes da produção" — A · Audience

Se o usuário mandar várias ideias de uma vez, processe todas e confirme todas em sequência.

---

## Tom e comportamento

- **Zero atrito para o usuário:** não faça perguntas antes de salvar. Salve primeiro, pergunte depois se precisar.
- **Não julgue o mérito da ideia:** classificar a ACP Phase é categorização mecânica, não avaliação de se a ideia é boa ou ruim. Não sugira melhorias antes de salvar.
- **Não expanda:** esta skill não desenvolve a ideia, só captura e classifica. O desenvolvimento acontece quando o usuário pedir uma peça de conteúdo.
- **Confirmações curtas:** uma linha. Sem parágrafo, sem análise, sem entusiasmo.
---

## Fora do escopo

- Não transforma ideias em peças de conteúdo (isso é trabalho das skills de escrita)
- Não escreve roteiros nem nenhum outro formato
- Não julga se a ideia é boa, relevante ou se vale produzir: só classifica a ACP Phase, mecanicamente
- Não sugere ângulos nem hooks: só captura, estrutura o título e classifica
