# Contrato da ideia incipiente

O orquestrador e o subagente leem este arquivo. A pesquisa devolve candidatos. Só a lista aprovada pelo orquestrador pode ser gravada.

## O que volta da pesquisa

Um YAML por estratégia. Texto em português. No máximo o teto recebido. Zero candidatos é válido.

```yaml
estrategia: ID recebido
cobertura:
  status: completa | parcial | vazia
  consultadas: [] # URLs efetivamente abertas
  lacunas: [] # o que não deu para abrir, com o motivo
candidatos:
  - titulo: até 10 palavras, factual, em português
    contexto: uma a três frases. O fato, a consequência para o dono e o limite. Sem roteiro.
    fonte: URL direta da fonte que sustenta a ideia
    formato_sugerido: Reel | IG Carousel | Thread | LinkedIn Post | Substack
    acp: "A · Audience" # ou "C · Community". Nunca "P · Product".
    nucleo: meia dúzia de palavras para achar duplicata
    publicado_em: data do fato ou do sinal, com o fuso conhecido, ou null
    por_que_entrou: uma frase para o orquestrador. Não vai para o Notion.
```

`completa`: deu para julgar. Pode terminar em zero. `parcial`: houve trabalho e ficou lacuna material. `vazia`: a estratégia rodou e nada passou na lente. Não use `vazia` para esconder página que não abriu. Isso é `parcial`.

`por_que_entrou` carrega o critério da estratégia (decisão, mecanismo da circulação, termo, padrão da dor, desenho da operação, tema da ementa). Não vira nota.

`acp` nunca é `P · Product`. Pesquisa não registra caso medido do próprio Pedro.

- `A · Audience`: o dono que não acompanha o Pedro reconhece o problema ou a decisão no título.
- `C · Community`: o título só fecha para quem já usa o vocabulário da escola (evals, harness, MCP, engenharia de contexto) e a tradução ainda depende desse termo.

Prefira `A · Audience` quando o título consegue dispensar o jargão. Copie o valor com o ponto médio, como está no banco.

## O que entra no Notion

Banco **Ideas**, data source `e2970ca3-7724-4a81-8f12-7ea34c048c67`. Crie uma página nova. Não atualize página existente. Não mude `Status` de quem já está no banco. Não publique.

| Campo | Valor |
|---|---|
| `Idea` | O `titulo`, até 10 palavras |
| `Date` | Data de hoje no horário de Brasília, ISO (`AAAA-MM-DD`) |
| `Status` | `Pending` |
| `ACP Phase` | O `acp` aprovado |
| `Format` | Vazio. O palpite fica nas notas |
| `Notes` | O bloco abaixo, e nada mais |

```text
Contexto: <uma a três frases>
Fonte: <url>
Estratégia: <nome da estratégia>
Formato sugerido: <valor de formato_sugerido>
```

Nomes das estratégias nas notas: Fontes de referência, Viral, Conceitos quentes, Dores da audiência, Casos no exterior, Ementa do webinar.

Não crie propriedade nova. Não cole a peça original. Não acrescente hook, CTA nem recomendação de canal além do formato sugerido.

## Duplicata, na hora de gravar

Antes de cada criação, busque de novo no banco. A busca da preparação não basta: outra estratégia, ou o Pedro, pode ter gravado no meio da rodada.

Considere duplicata:

- a mesma URL, depois de tirar rastreamento (`utm`, `fbclid`, `igshid`, `si` e equivalentes), mantendo parâmetro que identifica o conteúdo
- o mesmo núcleo já coberto por `Idea` ou `Notes`, em qualquer status

Não são duplicata: o mesmo domínio, a mesma empresa, o mesmo termo genérico. Página atualizada só é ideia nova quando o desdobramento está na fonte.

Se for duplicata, pule. Não edite a linha antiga. Não "complete" a nota dela. Se a criação voltar incerta, leia o banco antes de repetir.

## O que não fazer

Não preencha cota. Não grave candidato que o orquestrador não devolveu. Não altere arquivo da skill, da ementa ou de `posts/`. Não abra pull request.
