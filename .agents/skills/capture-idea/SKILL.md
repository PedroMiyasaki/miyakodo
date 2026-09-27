---
name: capture-idea
description: >
  Captura as ideias cruas, os aforismos e os pensamentos soltos do usuário, classifica
  cada um numa ACP Phase e registra tudo com estrutura mínima no banco Ideas do Notion.
  Ative com comandos como "captura essa ideia", "guarda esse pensamento", ou sempre
  que o usuário mandar qualquer ideia ou pensamento que possa virar conteúdo depois.
  Também se aplica quando o usuário envia apenas um link de Reel do Instagram para
  guardar como referência de conteúdo.
---
## Captura contínua de ideias cruas

Propósito: receber as ideias do usuário em estado bruto (aforismos, observações soltas, pensamentos guardados para virar conteúdo depois), dar a elas uma estrutura mínima, classificar numa ACP Phase e gravar no banco Ideas do Notion, deixando tudo pronto para virar conteúdo quando o usuário pedir.

Opere com zero atrito **para o usuário**: ele não precisa escolher formato, ângulo nem fase. Toda a estruturação, classificação e registro é trabalho desta skill. A classificação é trabalho interno, nunca uma pergunta devolvida ao usuário. Links de Reels já definem o destino padrão: Instagram, formato Reel.

---

## Ferramentas disponíveis

- **Notion MCP**: escrever no banco Ideas.
- **Navegador interno do Codex (`iab`)**: abrir e analisar Reels; também permite registrar no Notion pela interface quando o MCP não estiver disponível.

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
- `Format`: normalmente vazio na captura; a skill de produção decide e registra o formato quando fecha a peça. **Exceção: link de Reel do Instagram entra com `Reel`**, salvo orientação diferente do usuário. Isso não muda o `Status`: a ideia continua `Pending`.
- Canal: para links de Reels, registre `Instagram` na propriedade de canal se ela existir no schema consultado. Se não existir, inclua `Canal: Instagram` em `Notes`. Não crie nem altere o schema para isso.
---

## Quando agir

Aja sempre que o usuário mandar qualquer coisa que pareça ideia, observação, aforismo, insight ou pensamento solto, mesmo incompleto ou abstrato. Não exija um comando específico. Se a mensagem parece uma ideia, capture.

Exemplos de entrada válida:
- "E se eu fizesse um reel sobre como a IA falha em projetos de verdade?"
- "Autonomia total é uma armadilha"
- "A maioria das empresas não tem problema de IA, tem problema de processo"
- "Ideia: comparar implantação de IA com reforma de casa"
- Um link `instagram.com/reel/...` ou `instagram.com/reels/...`, mesmo sem texto adicional
- Qualquer coisa que seja claramente um pensamento guardado para virar conteúdo depois

Se o link vier com um pedido explícito diferente de captura, siga esse pedido. O envio isolado de um Reel é suficiente para acionar o fluxo abaixo.
---

## Protocolo de execução

### Passo 1 · Interpretar a ideia

**Se a entrada for um Reel do Instagram, execute primeiro o fluxo “Reels como referência” abaixo.**

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
**Notas (opcional para ideias em texto; obrigatórias para Reels):** se o usuário mandou contexto extra, frases de exemplo, ou a ideia já veio com algum desenvolvimento, cole isso no campo Notes como está, sem reescrever. É o despejo bruto para consulta futura. Para Reels, acrescente o registro estruturado da referência conforme o fluxo abaixo.

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
| `Format` | `Reel` para links de Reels do Instagram; vazio nas demais capturas |
| Canal, se houver propriedade no schema | `Instagram` para links de Reels; sem propriedade, registrar em `Notes` |

Para Reels, `Notes` recebe a ideia e a análise da referência descritas abaixo, além de qualquer comentário original do usuário. Depois de salvar, confira se título, notas, fase, formato e canal foram persistidos antes de confirmar o registro.

### Passo 5 · Confirmar no mínimo

Responda com uma confirmação curta, de no máximo uma linha, com o título e a classificação. Não resuma, não parafraseie, não elogie, não justifique a classificação.

Resposta ideal:
> Salvo: "Por que a implantação de IA falha antes da produção" — A · Audience

Para Reels, inclua o link da entrada salva e `Instagram · Reel` na confirmação curta.

Se o usuário mandar várias ideias de uma vez, processe todas e confirme todas em sequência.

---

## Reels como referência

O padrão é **abrir, assistir, entender a ideia, dissecar a apresentação e registrar no Ideas**, sem pedir ao usuário que descreva um vídeo acessível. Cada Reel gera uma entrada com sua fonte.

### Acessar e assistir

1. Selecione explicitamente o navegador interno do Codex (`iab`); não deixe a seleção automática escolher o navegador pessoal. Reutilize a aba do Reel se já estiver aberta. Verifique a sessão existente antes de pedir login. Mantenha o navegador em segundo plano, exceto quando o usuário quiser acompanhar ou conferir a execução.
2. Reproduza e examine o vídeo inteiro: fala, textos na tela, imagens, demonstrações e encerramento. Leia também a legenda do post para complementar o contexto. Capa, descrição e primeiros segundos não substituem o vídeo completo.
3. Use os recursos disponíveis para compreender o conteúdo, inclusive transcrição e quadros do vídeo quando necessários. Se só conseguir ler legendas completas e quadros, declare esse alcance; não alegue ter ouvido o áudio nem infira entonação, música ou cortes que não observou. Se faltar conteúdo para entender a ideia ou o encerramento, informe a limitação e peça o vídeo ou a transcrição, sem inventar uma análise completa.
4. Se o navegador interno estiver indisponível ou não permitir acesso, avise antes de recorrer ao navegador pessoal. Não presuma que ele precisa ser usado por causa de login.

### Registrar a ideia e a construção do vídeo

Escreva `Notes` em português, com detalhe proporcional ao conteúdo. Separe o que o criador disse da sua análise de como ele apresentou a ideia:

- **Fonte:** URL do Reel e autor/@handle observado; inclua fontes citadas ou exibidas quando identificáveis.
- **Canal e formato:** `Instagram` e `Reel`, já definidos para esta captura, salvo pedido diferente do usuário.
- **Ideia original:** tese, argumentos, exemplos e conclusão, preservando o sentido e as ressalvas. Atribua previsões, números e resultados ao criador; não os transforme em fatos verificados nem em experiências do usuário. “As-is” significa fidelidade à ideia, sem criar outro ângulo, ampliar a tese ou escrever um roteiro novo.
- **Gancho:** o que abre o vídeo e como procura despertar interesse (por exemplo, pergunta, promessa, contraste ou demonstração). Diferencie uma citação curta literal de uma paráfrase.
- **Desenvolvimento e entrega:** ordem dos argumentos, progressão até a conclusão, exemplos e provas; recursos visuais, texto na tela, ritmo e edição quando observados e relevantes. Descreva os mecanismos usados sem afirmar que causaram engajamento.
- **CTA e reaproveitamento:** descreva a chamada original como parte da referência, sua função e o que depende do contexto daquele criador. Não copie para o usuário chamadas para perfil, produto, comunidade, link na bio ou material de terceiros. Exemplo: “Comente X que eu envio meu e-book” vira a observação “CTA de comentário com palavra-chave para receber material do criador; depende de uma entrega própria e não deve ser reutilizado literalmente”. Se não houver CTA, registre isso. Preserve mecanismos pertinentes sem inventar ofertas, materiais, automações ou promessas para o usuário.

Essa análise registra a construção existente para consulta futura; a adaptação para a voz e os recursos do usuário acontece na produção. Classifique a ACP Phase normalmente: um case do criador não é um case do usuário e não justifica `P · Product` por si só. Salve com `Status = Pending`, `Format = Reel` e canal `Instagram`, seguindo o mapeamento do banco acima.

---

## Tom e comportamento

- **Zero atrito para o usuário:** não faça perguntas antes de salvar. Salve primeiro, pergunte depois se precisar.
- **Não julgue o mérito da ideia:** classificar a ACP Phase é categorização mecânica, não avaliação de se a ideia é boa ou ruim. Não sugira melhorias antes de salvar.
- **Não expanda:** esta skill não desenvolve uma ideia nova. Em Reels, captura a tese e analisa a construção do conteúdo existente; o desenvolvimento de uma peça própria acontece quando o usuário pedir.
- **Confirmações curtas:** uma linha. Sem parágrafo, sem análise, sem entusiasmo.
---

## Fora do escopo

- Não transforma ideias em peças de conteúdo (isso é trabalho das skills de escrita)
- Não escreve roteiros nem nenhum outro formato
- Não julga se a ideia é boa, relevante ou se vale produzir: só classifica a ACP Phase, mecanicamente
- Não sugere ângulos nem hooks novos; pode identificar e analisar os que já existem no Reel de referência
