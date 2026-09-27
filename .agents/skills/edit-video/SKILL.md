---
name: edit-video
description: >
  Use ao editar um talking head ou Reel deste projeto, inclusive pedidos como
  "edita esse vídeo" e "edita no modo news". Aplica as preferências editoriais
  de modos, cortes, notas de gravação, legendas, capa e entregas.
---

# Edição de Reels — preferências do projeto

Este guia define o resultado editorial desejado. A execução fica a cargo dos
recursos de edição disponíveis na sessão do Codex, com preferência pelos
recursos nativos quando houver. Verifique a disponibilidade antes de prometer
um efeito ou exportação. Se faltar uma capacidade necessária, explique a
limitação concreta e proponha uma alternativa.

Não há dependência da skill legada video-use, de um fornecedor de transcrição
ou de scripts próprios de renderização. Não carregue o setup antigo como
pré-requisito deste projeto.

## Material e modo

Use o vídeo indicado pelo usuário; sem indicação, o mais recente em
video/inputs/. Preserve os originais. Reaproveite o slug do roteiro em
posts/script/<slug>/; se não houver roteiro, derive o slug do título em
minúsculas, sem acentos e com hífens.

Leia o material completo para identificar retomadas e notas de editor antes
de montar o corte. Use o modo pedido. Sem modo explícito, notícia concreta
pede news; nos demais casos, baseline. Authority é a opção para uma edição
pedagógica com ênfases visuais, quando solicitada.

Leia [Modos e efeitos](references/modos.md) para aplicar o modo escolhido.
Explique brevemente as escolhas e avance com o pedido já autorizado. Pergunte
apenas quando faltar uma decisão editorial que o material não resolve.

## Preferências comuns

- Preserve proporção, enquadramento, resolução e fluidez da gravação; não
  force 9:16. Um zoom de ênfase é temporário e volta ao enquadramento original.
  Cards e diagramas nunca encolhem nem recortam o apresentador para caber.
- Corte tempo morto, tropeços e takes abandonados. Preserve pausas
  intencionais, respiros naturais e palavras inteiras.
- Mantenha a voz clara e o volume consistente, sem distorção, estalos nas
  emendas ou efeitos sonoros cobrindo a fala.
- Legendas ficam ligadas por padrão. Leia
  [Legendas, caption e capa](references/legendas-e-entregas.md) para o estilo
  e as entregas. "Sem legenda" desliga a legenda do vídeo. O mesmo arquivo
  cobre a label "Aperte aqui para 2X": borda direita, não o canto, mesma
  fonte das legendas, ~1 cm acima do meio da tela.
- Preserve a cor natural do talking head, salvo efeito pontual. Capas e
  diagramas próprios seguem design/identity.md; imagens de fontes externas
  preservam seu conteúdo.
- No fecho e no pedido de follow, deixe o rosto livre de cards e diagramas.

## Notas faladas ao editor

Reconheça pela intenção qualquer fala dirigida a quem edita: não há palavra
ou marcador obrigatório. "Corta, vou falar de novo" e "nessa imitação, vai para
preto e branco" são instruções de edição, não conteúdo para o público.

Aplique a instrução ao trecho a que ela se refere e retire a nota inteira do
áudio, da imagem e das legendas. Retire também o take abandonado quando a
nota pedir uma retomada. "Corta todo esse final sobre X" alcança o assunto
inteiro, mesmo que tenha começado vários takes antes.

A nota ganha do padrão do modo e pode pedir algo além dos efeitos descritos
aqui. Informe o que foi dito, como interpretou o alcance e o que fez.
Se uma fala parecer nota e o limite continuar ambíguo, deixe-a fora do
preview e sinalize a dúvida. Uma nota que não pôde ser aplicada deve ser
relatada, nunca descartada em silêncio.

## Revisão e entrega

Mostre o preview para revisar corte, ritmo, imagens e efeitos. Os previews
de corte podem ficar sem legendas; não é preciso impor essa restrição quando
a ferramenta permitir revisá-las sem atrito. A versão final deve ter as
legendas conferidas, salvo pedido para removê-las.

Antes de apresentar a saída, confira emendas, sincronismo, notas removidas,
legibilidade e o espaço entre rosto, cards e legendas. Informe qualquer
checagem que a sessão não consiga realizar.

No "pronto", entregue juntos em posts/script/<slug>/:

- reels.mp4 — vídeo final;
- caption.md — legenda do post;
- cover.png — capa.

Use edit/<slug>/ para o material de edição e sketch/ para intermediários da
capa, quando necessários. Mantenha final.md e sketch/v<N>.md do roteiro.
Edição de vídeo não altera o fechamento da ideia no Notion, que pertence
à produção do roteiro.
