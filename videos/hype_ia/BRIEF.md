---
workflow: talking-head-recut
flow: automation
storyboard: no
message: "O hype de IA pode atrapalhar a adoção que gera resultado para a empresa."
destination: Instagram Reels
aspect: "9:16"
language: pt-BR
audience: empresários e interessados em IA
---

## Pedido

Editar o vídeo de `video/inputs/hype_ia/IMUL3615.MP4`. As únicas intervenções são legenda, aviso de 2x, identificação do perfil e um print da fonte oficial quando a fala aborda a aposentadoria dos custom GPTs.

## Padrões

- `perfil-pb`: `@pedro.miyasaki.ia`, canto superior esquerdo, presente durante todo o vídeo.
- `legenda-evals`: Inter variável 650, caixa preta e borda branca, grupo inteiro visível e destaque por palavra.
- `aviso-2x`: `SEGURE PARA 2X`, posição de referência do catálogo, abaixo da legenda. Entrada em 0,409 s, duração de 3,091 s após aceleração de 10%.
- Catálogo visual: `.agents/skills/editar-video/video-patterns.md`.

## Fonte e insert

Print real de https://learn.chatgpt.com/docs/build-plugins, capturado no navegador em 12/10/2026. O recorte preserva o título “Custom GPTs are moving to plugins” e a frase “Custom GPTs in ChatGPT Enterprise are being retired.” O print completo permanece em `assets/openai-source-full.jpg`.

Mostrar `assets/openai-custom-gpts.jpg` de 53,955 s a 61,818 s, durante a explicação da aposentadoria no ChatGPT Enterprise e transição para plugins. O recorte fica abaixo do rosto e acima da legenda, com atribuição à OpenAI e ao domínio oficial. A gravação já especifica o escopo Enterprise.

## Preservação

Manter a sequência completa, o enquadramento e as cores da gravação. A pedido do usuário, acelerar todo o vídeo em 10%, para 1,1x, preservando o tom da voz. Duração final: 140,166667 s. Retimar todos os overlays na mesma proporção. Sem cortes, zooms, trilha, efeitos sonoros, cartões extras ou alterações do roteiro.

## Decisões de exportação

Canvas vertical 1080 × 1920, 60 fps. Fonte HEVC HDR HLG de 1440 × 2560; preservar corretamente a aparência e documentar o formato de cor da entrega após a validação.

Entrega: `hype_ia_editado_1-1x.mp4`, 1080 × 1920, 60 fps, HEVC Main10, HLG e BT.2020. Duração verificada: 140,166 s. A composição do Studio também reflete 1,1x.

Os gráficos são renderizados pelo HyperFrames 0.8.150 como ProRes 4444 com alpha, em `renders/overlays.mov`. `compose_export.py` combina essa camada com o vídeo original e aplica `setpts=(PTS-STARTPTS)/1.1` e `atempo=1.1`, com codificação HEVC na GPU. As cores da gravação não recebem tonemap; a camada gráfica recebe a conversão de sRGB para HLG com branco de referência de aproximadamente 203 nits.

A exportação HDR direta do HyperFrames apresentou várias legendas sobrepostas, embora a prévia estivesse correta. Ela foi descartada. Cada legenda agora também controla a opacidade de seu conteúdo. O perfil permanente usa um recorte com alpha do próprio gráfico renderizado, para evitar seu desaparecimento na segunda faixa de captura paralela.

Para refazer a entrega: executar `build_composition.py`, renderizar `renders/overlays.html` em MOV com alpha a 60 fps e dois workers, executar `compose_export.py` e depois `verify_export.py`.

## Legendas

550 palavras em 105 grupos, extraídas da gravação com Whisper local. Grafia de IA e anos normalizada. Timestamps de duração zero foram distribuídos no intervalo disponível, mantendo a ordem. A segunda transcrição foi utilizada para conferir o conteúdo. Sem substituir a fala pelo roteiro.

## Validação

Verificar timestamps e grafia das legendas, destaque por palavra, convivência do aviso 2x com a legenda, perfil sobre a fala e sobre o insert, legibilidade do print, áudio e duração da exportação.

Arquivo final conferido em frames do início, do print e do encerramento. Perfil presente até o fim, legendas legíveis e sem sobreposição nesses pontos. Comparação do áudio com a gravação acelerada em 1,1x: correlação acima de 0,9997 e atraso de 0 ms nos trechos de 5, 55 e 125 s. Evidência em `export-validation.json`.
