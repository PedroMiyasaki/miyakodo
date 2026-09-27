# Legendas, caption e capa

## Legendas do vídeo

- Ligadas por padrão e incorporadas ao vídeo final, para não depender da
  legenda automática do Instagram. O usuário pode desligá-las.
- Português do Brasil, fiel à fala mantida no corte, com nomes e termos
  técnicos revisados. Notas ao editor e takes descartados não aparecem.
- Maiúsculas apenas onde a língua pede: início de frase, nomes e siglas.
- Trechos curtos que se substituem, sem acumular: até quatro palavras e
  duas linhas por vez, acompanhando a fala depois dos cortes.
- Bricolage Grotesque ExtraBold, branca, com sombra e sem contorno por
  padrão. Aumente a sombra se o fundo claro prejudicar a leitura.
- Posição inferior com margem segura. Cards nunca cobrem o texto; rosto e
  legendas precisam continuar legíveis juntos.

## Label 2X

Todo Reel leva o texto "Aperte aqui para 2X" o tempo inteiro, na mesma
fonte das legendas (Bricolage Grotesque ExtraBold, 32px). Fica na borda
direita, nunca no canto superior. O centro da label fica ~1 cm acima do
meio da tela do celular (`y=(H-h)/2-182` num canvas de 2560 px; `x=W-w-24`).

Gere o PNG com [assets/make_tap2x.py](../assets/make_tap2x.py). Num vídeo
já renderizado sem a label, grave por cima com
[assets/apply_tap2x.py](../assets/apply_tap2x.py). Se a label antiga já
estiver queimada no canto, re-renderize o corte; overlay por cima deixa as
duas.

As fontes de referência estão em
[assets/fonts/](../assets/fonts/). A identidade canônica é design/identity.md.

## Caption do Instagram

Leia docs/voice/base.md antes de escrever. caption.md tem duas linhas:

~~~
<uma frase curta que conversa com quem acabou de assistir>
siga @pedro.miyasaki.ia
~~~

A primeira frase reage ao assunto, confirma a surpresa ou abre os
comentários. Não resume o Reel, não repete o hook e não ensina algo novo.
A segunda linha é sempre exatamente "siga @pedro.miyasaki.ia".

Mostre o texto no chat para revisão. Correções atualizam caption.md.

## Capa

Capa composta, seguindo design/identity.md e o arquétipo 01 COVER de
design/templates/slides.html. Use o hook de abertura do Reel, encurtado
para caber, sem inventar uma afirmação nova.

- Preto e branco, composição invertida, marca e tipografia do Alvinegro.
- Texto de apoio e desenho geométrico são opcionais.
- Tela vertical 1080 × 1920, com o conteúdo essencial no miolo de
  1080 × 1350 para sobreviver ao recorte do feed. A proporção da capa
  não obriga a recortar o vídeo.
- Mostre a capa e confira a leitura em miniatura. Salve como cover.png.
  Eventual composição de trabalho fica em sketch/cover.html.

O vídeo, a caption e a capa são entregues juntos na pasta do roteiro,
posts/script/<slug>/, com os nomes reels.mp4, caption.md e cover.png.
