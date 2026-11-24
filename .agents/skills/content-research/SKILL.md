---
name: content-research
description: >
  Use quando o usuário ou a rotina diária pedir content research, radar do
  dia ou pesquisa de ideias sobre IA para donos de empresa. Dispara uma
  estratégia por subagente, grava ideias incipientes no banco Ideas e não
  publica nem altera ideias que já existem.
---

# Pesquisa diária de ideias

Encha o banco `Ideas` de ideias incipientes para a Miyakodo. Quem recebe o pedido é o orquestrador. Ele não pesquisa no lugar das estratégias e não escreve a peça. Cada estratégia roda num subagente só dela. O orquestrador junta, tira duplicata entre elas e fecha com um resumo curto.

A rodada das 6h no horário de Brasília chega por uma rotina externa, que manda a mensagem abaixo para este Project. A mesma rodada vale quando o Pedro pedir a pesquisa do dia em outras palavras. Não peça confirmação para começar. Não crie agendamento. Não publique em rede nenhuma.

Mensagem da rotina, verbatim:

```text
Rode a skill content-research. Rodada diária, 6h no horário de Brasília. Janela das últimas 24 horas. Teto de 4 ideias por estratégia. Dispare todas as estratégias em paralelo. Não publique nada. Não altere ideias que já existem. Feche com o resumo: quantas ideias por estratégia, título e link de cada página criada.
```

## Leitura por papel

O orquestrador lê este arquivo, [themes.md](references/themes.md) e [contrato.md](references/contrato.md). Não carregue os arquivos de estratégia no próprio contexto. Passe o caminho absoluto no despacho.

Cada subagente lê só o arquivo da estratégia dele, a lente e o contrato. `sources.md` entra apenas quando a estratégia mandar.

## Estratégias

| ID | Arquivo | O que procura |
|---|---|---|
| fontes-de-referencia | [fontes-de-referencia.md](references/estrategias/fontes-de-referencia.md) | Fontes primárias confiáveis e o que nelas vira conteúdo |
| viral | [viral.md](references/estrategias/viral.md) | O que está circulando agora e por que circulou |
| conceitos-quentes | [conceitos-quentes.md](references/estrategias/conceitos-quentes.md) | Termo quente de IA traduzido para o dono |
| dores-da-audiencia | [dores-da-audiencia.md](references/estrategias/dores-da-audiencia.md) | Dor e pergunta repetida em fórum e comentário |
| casos-no-exterior | [casos-no-exterior.md](references/estrategias/casos-no-exterior.md) | Operação real de empresa de fora |
| ementa-do-webinar | [ementa-do-webinar.md](references/estrategias/ementa-do-webinar.md) | Cena nova para um tema da ementa |

Por padrão as seis rodam. Se a mensagem nomear uma ou algumas, rode só essas. Sobreposição é esperada. Ela se resolve na deduplicação, não com mais agentes.

## Teto e janela

Capture `AGORA` uma vez, no horário de Brasília. Relógio da máquina em UTC não é Brasília. Timestamp com `Z` ou com offset é o fuso que ele declara: converta antes de comparar.

`INICIO = AGORA - 24 horas`, salvo se a mensagem pedir outra janela.

`TETO = 4` por estratégia, salvo se a mensagem pedir 3 ou 5. Recuse pedido acima de 5 e use 5, dizendo isso no resumo. O teto da estratégia, quando o arquivo dela for menor, prevalece. Teto é teto, não cota. Zero ideias numa estratégia é resultado válido.

O banco é **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`.

## 1. Preparar

Sem ferramenta de subagente, pare e diga que a rodada não pode separar as estratégias. Não junte as seis num agente só.

Leia as linhas do banco, paginando até o fim, em todos os `Status`, inclusive `Processed` e `Discarded`. De cada linha guarde título, `Date`, `Notes`, URLs e o id. Ler só o schema não é ler as ideias. Monte um digest compacto (data, título, URLs, uma linha de `Notes`) para os despachos.

Essa leitura pode acontecer enquanto você prepara os despachos. Não escreva nada no banco nesta etapa.

## 2. Disparar a pesquisa

Um subagente por estratégia, em paralelo, contexto limpo, o mesmo modelo da sessão. Não crie agente por fonte, por rede ou por segunda passada. O subagente não cria outros agentes, não edita arquivo e não escreve no Notion nesta fase.

Modelo de despacho:

```text
Pesquise só a estratégia {ID}, na janela de {INICIO} até {AGORA} (horário de Brasília), com teto {TETO}.
O repositório está em {caminho absoluto da raiz}. Caminhos como webinar/ partem dessa raiz.
Leia {caminho absoluto da estratégia} e siga só esse arquivo.
A lente está em {caminho absoluto de themes.md}.
O contrato de retorno e de registro está em {caminho absoluto de contrato.md}.
Ideias já existentes, para não repetir: {digest}.
Devolva o YAML do contrato, com no máximo {TETO} candidatos. Não escreva no Notion, não edite arquivo e não crie agente.
Se faltar uma URL específica, peça essa URL e o dado. Não declare a estratégia encerrada por falta de uma página.
```

Se o subagente não tiver como pesquisar, ele pede a consulta. Você busca só o que ele apontou e devolve ao mesmo subagente. Não transforme a falta de acesso em "nada encontrado".

Se um subagente não responder, a estratégia fica em aberto. Siga com as que voltaram.

## 3. Deduplicar

Confira teto, URL e encaixe na janela. Hora em que a página foi aberta não prova novidade.

Junte os candidatos pelo núcleo: o mesmo fato, a mesma decisão ou a mesma dor. Um anúncio visto em três estratégias vira uma ideia. Repost, tradução e comentário do mesmo fato não criam outra.

Quando duas estratégias disputam o mesmo núcleo, fique com uma. Prefira o ângulo em que o dono decide alguma coisa, e a fonte primária quando os ângulos forem o mesmo. Se os ângulos produziriam peças diferentes (uma crença que circulou, e um desenho de operação que não é essa crença), mantenha as duas e marque no resumo que estão relacionadas.

Compare com o digest do banco. URL igual, sem parâmetro de rastreamento (`utm`, `fbclid`, `igshid`, `si` e equivalentes), é duplicata. Parâmetro que identifica o conteúdo fica. Domínio ou empresa em comum não bastam. Se o núcleo já está no banco, em qualquer status, descarte. Desdobramento só entra quando a novidade está explícita na fonte. Na dúvida, releia a linha original.

Estratégia sem candidato aprovado não volta para a fase de registro.

## 4. Registrar

Cada subagente grava só as ideias que você devolveu para a estratégia dele, na ordem, seguindo o contrato. Mensagem:

```text
Deduplicação fechada. Crie somente estas ideias, seguindo {caminho de contrato.md}:
{lista aprovada: título, contexto, fonte, formato sugerido, fase ACP}
Antes de cada criação, confira de novo o banco. Se já existir, pule e não altere a página. Não mude Status de ideia existente. Não preencha Format. Não publique. Devolva o que criou (título e URL da página) e o que pulou.
```

A fase de pesquisa não autoriza criar. Só esta lista autoriza.

Se o subagente não tiver o conector do Notion, grave você essas páginas, com a mesma checagem, e diga no resumo que o orquestrador gravou aquela estratégia. Não faça isso se o conector estiver disponível para ele.

Depois de cada criação confirmada, some a ideia ao conjunto já visto. Se o retorno for incerto, leia o banco antes de tentar de novo. Não crie a segunda cópia.

Conector sem aprovação: não grave em arquivo local para "não perder". Liste no resumo as ideias não gravadas, com título e fonte. Não finja que entraram no banco.

## 5. Resumir

Responda curto, em português, sem travessão e sem emoji:

```text
Janela: DD/MM/AAAA HH:MM até DD/MM/AAAA HH:MM, horário de Brasília.
Fontes de referência: N
- Título: URL da página no Notion
Viral: N
Conceitos quentes: N
Dores da audiência: N
Casos no exterior: N
Ementa do webinar: N
Total: N
Não gravadas: ...
Lacunas: ...
```

Estratégia que não rodou não entra como zero. Diga que ficou em aberto e por quê. `Nenhuma ideia nova registrada.` só quando todas as estratégias rodaram e nada passou, ou tudo era duplicata.

## Git

A rodada grava ideias no Notion. Não abre pull request, não cria branch e não commita rascunho de pesquisa. Arquivo temporário, se for inevitável, fica só em `.agents/skills/content-research/runs/`, coberto pelo `.gitignore`.

Mudar esta skill é infraestrutura e segue por pull request. A rodada diária não é essa mudança.
