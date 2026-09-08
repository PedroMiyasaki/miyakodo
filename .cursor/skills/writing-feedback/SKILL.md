---
name: writing-feedback
description: >
  Use quando o usuário pedir explicitamente para consolidar o feedback de escrita
  acumulado numa sessão de conteúdo dentro do guia de voz. Gatilhos: "consolida o
  feedback de escrita dessa sessão", "transforma as correções dessa conversa em
  regras", "atualiza o guia de voz". Vale para sessões de conteúdo (roteiro,
  carrossel, thread, LinkedIn) depois de várias correções de tom, vocabulário,
  ritmo ou registro. NÃO invoque numa correção isolada no meio da sessão: roda
  uma vez, sob demanda, sobre todas as correções do chat.
---

# Writing Feedback · Consolidação do guia de voz

## Propósito

Função: consolidar, num lote só, as correções de escrita que o usuário fez ao longo de uma sessão de produção em regras permanentes no guia de voz. Objetivo: impedir que o mesmo erro volte nas sessões seguintes.

Restrição central: rode esta skill **uma vez, sob demanda, no fim da conversa**, varrendo a sessão inteira. Não reaja a correções individuais durante a produção.

## Quando usar

Condição de ativação: o usuário invoca explicitamente, no fim de uma sessão de produção de conteúdo (roteiro, carrossel, thread, LinkedIn, legenda do post) em que corrigiu tom, vocabulário, ritmo, registro ou estrutura mais de uma vez. Gatilhos: "consolida o feedback de escrita dessa sessão", "transforma as correções dessa conversa em regras", "atualiza o guia de voz".

**Quando NÃO usar:**

- Não rode durante a sessão, a cada correção. A correção individual já é aplicada na hora, dentro da skill de produção. Esta skill só entra quando o usuário pede a consolidação.
- Não rode sobre correções de código, análise ou documentos internos. Só conteúdo publicável.

## Protocolo

### Passo 1 · Varrer a conversa

Releia a conversa inteira. Colete todo momento em que o usuário corrigiu, rejeitou ou redirecionou *como* algo foi escrito: tom, escolha de palavra, vocabulário, ritmo, registro, estrutura de frase, pontuação, formato.

Para cada correção, registre:

- **✗ rejeitado**: o que o modelo tinha escrito.
- **✓ aceito**: o que o usuário pediu no lugar, ou a reescrita que ele aprovou.
- **motivo**: a razão que ele deu, se deu.

A conversa guarda os pares ✗/✓ reais que alimentam o Passo 4. Não invente exemplo no Passo 4 quando o par real está registrado aqui.

Se a varredura encontrar zero correções de escrita, diga isso e pare. Se encontrar só uma, siga mesmo assim.

### Passo 2 · Avaliar a generalização

Uma correção só vira regra se for **generalizável**: se a mesma escolha estaria errada numa peça futura, sobre outro assunto. Classifique cada uma:

- **Generalizável**: aponta para um padrão ("você sempre faz X", "para de usar Y"). A mesma palavra ou estrutura estaria errada em qualquer peça.
- **Pontual**: presa ao assunto desta peça, a um fato, ou a uma escolha que só vale aqui. Ou o usuário disse "só aqui".
- **Limítrofe**: na dúvida, marque assim e deixe a decisão para o usuário no Passo 5.

Não descarte correções pontuais em silêncio. Inclua na proposta do Passo 5 com o motivo, para o usuário poder promover qualquer uma delas.

### Passo 3 · Deduplicar e reconciliar com o guia

A voz mora em `docs/voice/`. Leia o arquivo-alvo: `docs/voice/base.md` por padrão, ou a layer em `docs/voice/layers/` se o usuário nomeou uma. Ainda não existe nenhuma layer, então hoje o alvo é sempre a base. Depois rode duas passadas:

**(a) Deduplicar entre si.** Se o usuário corrigiu o mesmo padrão em pontos diferentes da conversa, trate como uma regra, não várias. Junte as ocorrências e guarde os exemplos.

**(b) Reconciliar com o guia.** Para cada regra que sobrou, aplique a tabela abaixo:

| Situação | Ação |
|---|---|
| Já coberta por uma regra existente, nada novo | Descarte. Não duplique. |
| Coberta por uma regra existente, mas a sessão produziu um exemplo mais afiado ou um padrão mais amplo | Proponha **afiar a regra existente**: reescreva para absorver o exemplo melhor. |
| Contradiz uma regra existente | **Não sobrescreva.** Aponte a contradição na proposta e deixe a decisão para o usuário. |
| Nova, não coberta | Vira regra nova na seção do guia que melhor encaixa. |

### Passo 4 · Escrever as regras com exemplos afiados

Para cada regra nova e cada entrada a afiar, escreva o item no estilo das regras do guia:

- **Negrito** na abertura, nomeando o padrão a evitar ou a calibração.
- Uma frase de diagnóstico: por que soa errado, ou por que a calibração importa.
- Um exemplo concreto, de preferência o contraste ✗/✓ tirado da sessão real: a frase que o modelo escreveu e a que o usuário aceitou. Exemplo genérico ("evite palavras formais") é exatamente o que a regra deveria eliminar.
- Atemporal: sem data, sem "nesta sessão", sem referência ao episódio.

Coloque cada regra na seção do arquivo-alvo que melhor encaixa. `docs/voice/base.md` está organizado em: **Estrutura**, **Inflação de importância e linguagem promocional**, **Vocabulário**, **Tiques de gramática**, **Ritmo e estilo**, **Hedge, enchimento e atribuição vaga**, **Tecido conectivo**, **Voz e textura**. Se um grupo de regras não encaixa em nenhuma, proponha uma seção nova, com título.

### Passo 5 · Propor o lote ao usuário

Antes de tocar no arquivo, apresente a proposta inteira numa mensagem só:

- **Regras novas**: cada uma como o item markdown literal que vai ser inserido, com a subseção de destino.
- **Entradas a afiar**: o item atual e o proposto, lado a lado.
- **Pontuais**: listadas, cada uma com uma linha dizendo "tratando como pontual porque X".
- **Conflitos**: "a correção Z contradiz a regra N do guia; escolha qual das duas vale, a skill não decide sozinha."

O usuário pode aprovar tudo, aprovar um subconjunto, editar o texto, ou promover e rebaixar itens. Não escreva nada sem aprovação explícita.

### Passo 6 · Aplicar em lote

Depois da aprovação, aplique todas as mudanças aprovadas de uma vez, no arquivo-alvo identificado no Passo 3: `docs/voice/base.md` por padrão, ou a layer nomeada em `docs/voice/layers/`.

Preserve a estrutura existente do arquivo-alvo. Insira cada regra dentro da seção a que ela pertence, na voz que o arquivo já usa. Não acrescente um bloco de "correções da sessão" no fim e não reestruture o documento para acomodar uma regra.

Depois confirme ao usuário o que foi inserido, e onde.

A skill não recorrige as saídas da sessão. As correções já foram aplicadas na hora, durante a produção.

## O que esta skill não faz

- Não roda sozinha durante a sessão. Só quando o usuário pede, uma vez, no fim.
- Não resolve sozinha uma contradição entre uma correção nova e uma regra existente: aponta e deixa a decisão para o usuário.
- Não inventa exemplos. Usa os pares ✗/✓ reais da conversa.
- Não recorrige as saídas da sessão.
- Não promove uma correção a regra sem a aprovação do usuário.
- Não registra feedback sobre código, análise ou documentos internos.

## Régua de qualidade da regra

Uma regra está boa o bastante quando:

- Um engenheiro de IA sênior consegue aplicar sem ambiguidade.
- Ela impede o erro específico que foi corrigido, sem proibir o que nunca foi problema.
- O exemplo é real (da sessão) e afiado (um contraste ✗/✓, não uma ilustração genérica).

Se a regra sair vaga ("não use palavras formais"), refine até dar para aplicar mecanicamente.
