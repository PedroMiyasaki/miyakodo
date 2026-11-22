---
slug: tier-list-de-casos-de-uso-de-ia
entrada: video/hooks/trabalho_cortado.mp4
versao: v2
status: aprovado
duracao_original: 5.0
duracao_prevista: 25.0
---

## Pedido do usuário
(observações literais, sem reinterpretação)

> Eu quero que você localize o vídeo que eu fiz sobre tier list de casos de uso de IA, e aí eu quero que você utilize a skill de edição de vídeo no modo Lista com gancho. Transformando aquele roteiro ali no modo que a lista com gancho pede. No caso, sinta-se à vontade para estruturar o gancho de chamada, e cada um dos itens da tier list vai ser uma Das imagens, desse modo, em cada uma das imagens , você pode meio que escrever uma nota de zero a dez ao invés do tier. A chamada final... da imagem de CTA é a mesma do script original.

## Revisão v2, pedido do usuário

> Sei que o vídeo ja foi feito mas vamos mudar algumas coisas, se atente a esses 4 pontos, mude, e renderize o video novamente, não precisa apresentar pré-plano, só faz essas mudanças e re-gera o vídeo
>
> 1 - Escreva "Minha opinião sobre use cases de AI comuns da indústria
> 2 - Na legenda coloque dois "*"
> - Muito profissional ruim fazendo
> - Dificil fazer bem
> - Não compensa para muitas empresas
> 3 - Na legenda coloca
> - Ainda precisa de bom profissional no loop
> - Sem cuidado, tudo fica com a mesma cara
> 4 - No de CTA, embaixo da frase "especialista" deixa a legenda assim:
> que eu mando um artigo detalhando o ultimo padrão

## Fonte

- Peça localizada: `posts/script/tier-list-de-casos-de-uso-de-ia/`. O roteiro é `final.md`. O `reels.mp4` publicado em 2026-10-15 é só referência.
- Lista: os cinco blocos de tier do roteiro, na ordem dele (D, C, C, B, S). Nenhum item foi acrescentado, removido ou fundido.
- Gancho: sorteado com `secrets.choice` entre os seis `.mp4` da raiz de `video/hooks/`. Resultado: `trabalho_cortado.mp4`, 5 s, 2160 × 3840, 60 fps, sem fala (média de -50 dB, pico de -29,7 dB). Será escalado para 1080 × 1920.

## Comportamentos padrão

- Legenda `legenda-evals`: não se aplica, o gancho não tem fala. As legendas do modo são overlays próprios.
- Espaço morto: não se aplica, o gancho não tem fala. Entra inteiro, sem cortes.
- Modo: Lista com gancho. Opcionais: `perfil-pb` e `aviso-2x` desligados.
- Exceções: CTA em fundo preto, sem imagem, em três linhas, conforme o modo.

## Decisões e intenção

- Gancho v2: "Minha opinião sobre use cases de AI comuns da indústria".
- Categoria das legendas dos banners: área da empresa afetada. Cada legenda nomeia a área e acrescenta o ângulo do item.
- Notas: D = 3, C = 5, B = 7, S = 10, escritas na imagem no lugar da letra do tier. Os dois C ficam iguais, como no roteiro. Sugestão, a confirmar.
- Ordem: a do roteiro, para o 10 fechar a sequência.
- Duração: 5 s de gancho, 3 s por banner (ponto de partida do modo), 5 s de CTA. Total: 25 s.
- CTA v2: frase de entrega substituída diretamente pelo usuário. Mantém a palavra-chave "especialista" e o CTA em três linhas.

## Textos

- Take 1, gancho: "Minha opinião sobre use cases de AI comuns da indústria".
- Take 2, Bot de atendimento no WhatsApp (tier D), nota 3/10: cabeçalho literal `*Atendimento*`; três tópicos: "Muito profissional ruim fazendo", "Difícil fazer bem", "Não compensa para muitas empresas".
- Take 3, IA para produzir conteúdo para redes sociais (tier C), nota 5/10: dois tópicos: "Ainda precisa de bom profissional no loop", "Sem cuidado, tudo fica com a mesma cara".
- Take 4, IA para analisar ligações e reuniões de vendas (tier C), nota 5/10: "Comercial: funciona, mas o retorno não é tão alto."
- Take 5, RAG Enterprise para conversar com documentos (tier B), nota 7/10: "Conhecimento interno: pra maioria, Gemini ou Copilot já resolvem."
- Take 6, Copiloto de IA para especialistas (tier S), nota 10/10: "Operação: o especialista produz muito mais."
- Take final, CTA, sem imagem:
  - linha 1: `comenta:`
  - linha 2: `"especialista"`
  - linha 3: "que eu mando um artigo detalhando o último padrão"

## Linha do tempo (tempos da edição)

| # | Início | Fim | Tipo | Conteúdo | Motivo |
|---|--------|-----|------|----------|--------|
| 1 | 00:00.0 | 00:05.0 | gancho | `trabalho_cortado.mp4` com a legenda de impacto | modo |
| 2 | 00:05.0 | 00:08.0 | banner | Bot de atendimento no WhatsApp, nota 3/10 | modo |
| 3 | 00:08.0 | 00:11.0 | banner | IA para produzir conteúdo para redes sociais, nota 5/10 | modo |
| 4 | 00:11.0 | 00:14.0 | banner | IA para analisar ligações e reuniões de vendas, nota 5/10 | modo |
| 5 | 00:14.0 | 00:17.0 | banner | RAG Enterprise para conversar com documentos, nota 7/10 | modo |
| 6 | 00:17.0 | 00:20.0 | banner | Copiloto de IA para especialistas, nota 10/10 | modo |
| 7 | 00:20.0 | 00:25.0 | CTA | comenta, palavra-chave e frase de entrega, fundo preto | modo |

## Cortes propostos

- Nenhum. O gancho entra inteiro, porque não tem fala.

## Pendências e dúvidas

- Palavra-chave do CTA: `especialista`, como você escolheu no chat. Ela já está na orientação do Reel publicado (`posts/script/tier-list-de-casos-de-uso-de-ia/respostas-comentarios.md`). A skill `responder-comentarios` associa cada comentário ao post, então não há colisão técnica. A regra do modo pede palavra inédita, e esta escolha fica registrada como exceção.
- Frase do CTA: atualizada conforme o pedido v2, sem novo pré-plano.
- Aprovação da estrutura: versão original aprovada; revisão v2 solicitada pelo usuário sem pré-plano.
- Pasta da peça e resposta automática: criada em `posts/script/tier-list-de-casos-de-uso-de-ia-v2/`, porque a pasta atual pertence ao Reel publicado. A resposta automática só é registrada depois da publicação, com o link do post do Instagram.
- Marca `@pedro.miyasaki.ia`: a identidade pede a marca em todo slide, mas o modo mantém `perfil-pb` desligado. Esta versão não tem a marca. Decisão minha, seguindo o modo. Se o usuário quiser a marca nos banners, basta pedir.
- Render final: só depois do "pronto" do usuário.

## Histórico

- v1: estrutura original aprovada e renderizada.
- v2: gancho atualizado; legendas dos takes 2 e 3 substituídas por tópicos; frase do CTA atualizada para `que eu mando um artigo detalhando o último padrão`. Renderização pedida diretamente pelo usuário, sem novo pré-plano. Render final refeito após validação. Movida para `posts/script/tier-list-de-casos-de-uso-de-ia-v2/reels.mp4`, pasta separada do Reel publicado.
