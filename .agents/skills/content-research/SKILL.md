---
name: content-research
description: Use quando o usuário pedir content research, radar diário ou pesquisa de notícias, tendências, workflows e ideias sobre IA, tecnologia, negócios e legaltech.
---

# Content research

Encontre ideias relevantes e variadas para o banco `Ideas`: novidades, aplicações úteis, conteúdos com tração e descobertas técnicas. O **coordenador coleta nas redes autenticadas**; **um pesquisador por tema** combina esse material com pesquisa aberta e entrega até `N` candidatos (três, por padrão).

As ideias são explicadas em português e nascem sem formato. As categorias organizam a coleta; não são pilares nem novas propriedades do Notion.

## Leitura por papel

O coordenador lê este arquivo e [result-contract.md](references/result-contract.md). Para coletar nas redes, carrega [social-collection.md](references/social-collection.md) e as fontes sociais de [sources.md](references/sources.md).

Os arquivos abaixo são instruções dos pesquisadores; o coordenador passa seus caminhos absolutos no despacho, sem carregá-los nem copiar seu conteúdo para o próprio contexto:

- [researcher.md](references/researcher.md): pesquisa aberta, análise do material social e seleção.
- [themes.md](references/themes.md): escopo e régua editorial de cada tema.

`sources.md` é compartilhado: o pesquisador lê as fontes de seu tema; o coordenador usa os pontos de partida sociais. O guia de navegação fica somente com quem opera o navegador.

## Temas da rodada

| ID | Tema |
|---|---|
| news | Notícias quentes e lançamentos |
| workflows | Skills e workflows populares |
| business | Negócios de IA |
| startups | Startups, investimentos e aquisições |
| policy | Política, regulação e geopolítica |
| engineering | Engenharia e bastidores técnicos |
| benchmarks | Comparações e benchmarks |
| opportunities | Oportunidades emergentes |
| legaltech | Legaltech e IA no mercado jurídico |

Por padrão, todos os nove temas participam. Sobreposição é esperada e será resolvida na consolidação. Fontes adicionais ampliam a cobertura do pesquisador, sem criar agentes extras.

## 1. Preparar a rodada

Capture `NOW` em UTC uma vez e fixe `WINDOW_START = NOW - 24 horas`. Se o usuário pedir outra janela, use-a explicitamente. `N = 3` por tema, salvo outro limite pedido pelo usuário; é teto combinado das duas passadas, nunca cota. Não há limite global rígido nem proporções entre categorias.

Use as ferramentas de pesquisa, subagentes e Notion realmente disponíveis na sessão. Sem ferramenta de subagentes, informe a limitação antes de executar uma arquitetura diferente.

Carregue as linhas do data source `Ideas`, ID `e2970ca3-7724-4a81-8f12-7ea34c048c67`, com `Idea`, `Notes`, URLs e IDs. Percorra a paginação e considere todos os Status, inclusive `Processed` e `Discarded`. Ler apenas o schema do data source não é ler suas ideias. Essa leitura pode ocorrer enquanto os pesquisadores trabalham.

## 2. Coletar nas redes autenticadas

Siga [social-collection.md](references/social-collection.md) no navegador integrado do coordenador. Confira o acesso na execução atual: login anterior não garante sessão válida hoje. Não dependa de os subagentes enxergarem suas abas ou herdarem autenticação.

Explore os temas selecionados para a rodada, usando as fontes cadastradas e buscas livres. Inclua criadores em inglês; não se limite a contas oficiais nem privilegie complexidade técnica. Agrupe consultas sobrepostas e reutilize evidências entre temas.

Prepare um pacote social por tema segundo o contrato, com conteúdo realmente lido, autoria, URLs, datas, métricas e limites da coleta. Encaminhe somente o recorte pertinente, não o histórico inteiro do navegador. Se uma rede estiver bloqueada, registre a lacuna e continue nas acessíveis; não invente um pacote completo.

## 3. Despachar os pesquisadores

Use a ferramenta de subagentes da sessão, com contexto limpo (`fork_turns: none`, quando disponível), herdando o modelo configurado. Não crie tarefas independentes na sidebar.

Despache um pesquisador por tema selecionado na rodada (todos os nove por padrão), em ondas conforme os slots livres; o coordenador também ocupa um slot. Não crie um agente por fonte, plataforma ou segunda passada. O pesquisador combina pesquisa aberta e análise social, sem delegar novamente. Pode começar assim que o pacote de seu tema estiver disponível, enquanto o coordenador coleta os demais.

Inclua no despacho:

```text
Pesquise o tema {ID e nome}, na janela {WINDOW_START} → {NOW}, com N={N}.
Leia {caminho absoluto de researcher.md} e siga suas instruções.
Seu escopo está na seção {ID} de {caminho absoluto de themes.md}.
As fontes iniciais estão em {caminho absoluto de sources.md}.
Retorne segundo {caminho absoluto de result-contract.md}.
Analise este pacote social coletado pelo coordenador: {pacote do tema}.
Você não precisa acessar a sessão autenticada. Para uma lacuna essencial,
peça ao coordenador uma consulta ou URL específica e o dado necessário.
Sua responsabilidade é pesquisa somente leitura. Não escreva no Notion,
não edite arquivos e não crie outros agentes.
```

Sem ferramentas de pesquisa aberta no subagente, ele solicita consultas dirigidas; o coordenador coleta o necessário e reenvia ao mesmo pesquisador. Não trate falta de acesso como pesquisa concluída. Use mensagens/continuação do mesmo agente, sem criar uma nova tarefa.

## 4. Conferir os retornos

Receba o retorno de cada tema e confira as duas coberturas, o teto combinado `N`, as URLs e a evidência temporal de cada candidato. Uma publicação nova e um conteúdo antigo com tração recente são caminhos válidos, conforme o contrato. O horário em que um agente abriu uma página não prova novidade nem tração recente.

Se faltar informação necessária, peça uma complementação dirigida ao mesmo pesquisador. Quando depender de navegador autenticado, faça a leitura no coordenador e devolva a evidência. Distinga fontes abertas diretamente pelo pesquisador de material fornecido no pacote. Registre falhas de acesso como cobertura parcial; elas não significam ausência de novidades. Se um agente não responder, reporte o tema não concluído e prossiga com os retornos válidos.

## 5. Consolidar e deduplicar

Agrupe candidatos pelo acontecimento, aplicação ou ideia central, reunindo evidências e atribuições. Um anúncio da Harvey encontrado em três temas rende uma única ideia. Reposts, traduções e reações ao mesmo fato não criam novidades independentes.

Compare os grupos com `Idea` e `Notes` de todas as linhas existentes. Normalize URLs de artigos/posts removendo rastreamento; preserve parâmetros que identificam conteúdo. URL igual é um sinal de duplicata, mas páginas atualizadas podem conter um desdobramento material novo. Domínio, empresa ou página inicial em comum não bastam para deduplicar.

Se o núcleo já estiver registrado, descarte. Aceite um desdobramento apenas quando a novidade estiver explícita e comprovada. Em dúvida, confira a linha original antes de decidir. Registre todos os candidatos distintos que passarem na régua do seu tema; profundidade técnica não é um bônus universal.

## 6. Preparar e registrar

`Idea`: título factual e claro, em português, com até 10 palavras. `Notes`: explicação autocontida, suficiente para decidir depois se vale produzir uma peça:

```markdown
O que aconteceu: <fato, aplicação ou ideia central, incluindo como funciona quando útil>
Por que está em alta: <sinal observado e suas datas; declare quando tração não foi demonstrada>
Contexto: <consequências, limitações e relevância para o Brasil quando fundamentada>
Fontes: <URLs consolidadas, identificando fontes primárias e criadores originais>
```

Explique o assunto em palavras próprias. Preserve autoria e links de conteúdos de inspiração. Não traduza peças inteiras nem acrescente hook, CTA, opinião atribuída ao usuário, formato sugerido ou recomendação de canal. Os temas não viram propriedades adicionais no banco.

**SUB-SKILL OBRIGATÓRIA:** leia e use `capture-idea` no próprio coordenador para classificar ACP e registrar cada título e Notes já preparados. Preserve o título factual e as notas; a captura não deve reenquadrá-los como um argumento. `Date` é a data de registro, `Status` é `Pending` e `Format` é omitido.

Nesta composição, `capture-idea` cuida da classificação e criação. Seu “zero atrito” não dispensa autorização do conector, e sua confirmação curta não substitui o relatório agregado desta skill.

Antes de escrever, confira novamente o banco para incorporar entradas criadas durante a pesquisa. Sem leitura suficiente para deduplicar, apresente os candidatos como não registrados. Respeite a autorização exigida pelo conector; em execução agendada sem aprovação disponível, reporte a pendência.

Após cada criação confirmada, incorpore a ideia ao conjunto já registrado. Se uma criação retornar resultado incerto, confira o banco antes de repetir. Em falha parcial, diferencie registros confirmados de candidatos pendentes.

## 7. Reportar

Informe a janela, os temas concluídos, a cobertura efetiva das redes, lacunas em cada passada e a quantidade de ideias registradas. Liste os títulos com os links das ideias criadas. Se nada novo passou, diga `Nenhuma ideia nova registrada.`; se a coleta ou o registro ficou bloqueado, explique a limitação em vez de declarar uma rodada vazia bem-sucedida.

Esta skill pode ser chamada por uma automação diária; sua execução não cria nem altera agendamentos.
