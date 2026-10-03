# Contrato entre pesquisador e coordenador

Lido pelos dois papéis. Os campos textuais são em português. O coordenador fornece evidências sociais; o pesquisador devolve candidatos e cobertura, sem precisar acessar a sessão autenticada.

## Entrada - pacote social do coordenador

Um pacote por tema, enviado no despacho. Pode conter zero itens, acompanhado do motivo. É material da rodada, não uma nova lista de fontes fixas.

```yaml
theme_id: ID do tema
coverage:
  status: complete | partial | unavailable
  consulted: [] # URLs que o coordenador efetivamente abriu
  gaps: [] # redes bloqueadas, consultas sem acesso e limites materiais
items:
  - url: link direto da publicação ou vídeo
    platform: Reddit | X | YouTube | Instagram | outro
    author: criador ou organização, ou null
    content: resumo fiel e trechos essenciais do conteúdo acessado
    read_as: text | caption | description | transcript | image
    published_at: data original com precisão e fuso conhecidos, ou null
    published_label: rótulo mostrado pela interface, ou null
    observed_at: timestamp UTC real da coleta
    discovery: consulta, fonte inicial e filtros efetivamente aplicados
    metrics: {} # contadores com nome e valor observado; ausente é null, não zero
    limitations: [] # partes não acessadas, alegações não verificadas, dúvida de recência
```

`content` descreve somente o que foi lido. `read_as` identifica a base principal; detalhe bases complementares no texto quando necessário. `metrics` conserva a precisão exibida (por exemplo, `views: "10 mil"`). Fontes complementares entram como itens próprios, sem misturar autores, datas ou contadores. Uma mesma URL pode constar em pacotes de temas diferentes.

O pacote não pré-aprova candidatos. O pesquisador avalia a suficiência do conteúdo, a recência e a relevância. Para pesquisa aberta feita pelo coordenador a pedido do pesquisador, envie os mesmos dados pertinentes, identificando a origem como pesquisa, não coleta social.

## Saída - seleção do pesquisador

O pesquisador entrega um objeto YAML por tema. O coordenador usa-o para conferir cobertura, evidência, deduplicação e registro, sem carregar as instruções de análise.

```yaml
theme_id: ID recebido no despacho
coverage:
  research:
    status: complete | partial | unavailable
    consulted: [] # URLs abertas diretamente pelo pesquisador nesta passada
    provided: [] # URLs cujo conteúdo fornecido pelo coordenador foi analisado
    gaps: [] # limitações e tentativas sem acesso, com canal/URL quando conhecido
  social:
    status: complete | partial | unavailable
    consulted: []
    provided: []
    gaps: []
candidates:
  - rank: 1
    title: título factual em português, até 10 palavras
    explanation: explicação autocontida do fato, aplicação ou ideia central
    context: consequências, limitações e relevância brasileira quando fundamentada
    found_in: [research, social] # apenas as passadas em que foi encontrado
    entry_basis: new_fact | recent_traction
    published_at: data original com precisão/fuso conhecidos, ou null
    recent_evidence:
      date_or_period: data ou intervalo verificável que qualifica o item na janela
      description: o que aconteceu ou qual sinal recente de interesse foi observado
      url: link que sustenta essa evidência temporal
    attention_evidence: sinal observado e contexto; ou tração não demonstrada
    observed_at: timestamp real da observação de métricas, ou null
    sources:
      - url: URL direta efetivamente consultada
        role: primary | discovery | creator
        author: nome do criador/organização quando identificável, ou null
        access: direct | coordinator_packet
```

## Como interpretar

- `complete`: a passada foi feita com evidência suficiente para julgar os achados; pode resultar em zero candidatos. Não significa que todos os sites da internet foram acessados.
- `partial`: houve trabalho útil, mas ficou uma lacuna material. `unavailable`: a passada não pôde ser executada. Analisar evidência suficiente do pacote pode completar a passada social sem navegação do pesquisador. Preserve lacunas materiais reportadas pelo coordenador; pacote bloqueado/vazio não autoriza alegar pesquisa concluída sem outra coleta suficiente.
- `consulted` e `provided` distinguem leitura direta de conteúdo recebido. Não conte uma URL citada sem conteúdo acessível como leitura. `sources.access` preserva essa mesma distinção por fonte; o coordenador pode conferir o pacote original.
- `candidates` contém de zero a `N` itens, ranks consecutivos a partir de 1, após combinar e deduplicar as duas passadas. Nenhuma passada tem cota própria.
- `explanation` explica o assunto, inclusive mecanismo ou passos essenciais quando forem necessários. `context` distingue consequências comprovadas de hipóteses; não sugere formato, hook ou roteiro.
- `entry_basis` determina o que precisa estar dentro de `WINDOW_START` → `NOW`. Em `new_fact`, `recent_evidence` sustenta a novidade; em `recent_traction`, sustenta o interesse recente, mesmo com publicação original antiga.
- Datas de publicação, do sinal recente e da consulta têm papéis distintos. Campos desconhecidos recebem `null`; não use o timestamp da rodada para preencher lacunas. Se a precisão da evidência temporal não permitir verificar a janela, o candidato não está pronto para registro.
- `attention_evidence` descreve métricas com suas datas, posição em lista temporal, discussão recente ou destaque editorial. Conteúdo novo com contadores pode qualificar por `new_fact`, sem alegar crescimento medido. Em `recent_traction`, declarar apenas tração não demonstrada, views acumuladas ou presença no Explorar é insuficiente.
- `sources` identifica as referências usadas, incluindo autor e link dos criadores que inspiraram a descoberta. Quando uma fonte exercer mais de um papel, escolha o mais informativo e esclareça o restante em `explanation` ou `context`.

O coordenador pode reunir referências de vários temas num único registro. Preserve a autoria dos criadores e a distinção entre declaração de uma empresa, relato pessoal e evidência independente.
