# Craft de carrossel

Engenharia reversa de cinco carrosséis virais em `examples/carousels/` (dois idiomas, cinco
nichos): toda regra abaixo é prática observada nos cinco. Os princípios são um sistema só — um
template travado não salva copy que enterra a conclusão, e boa headline não sobrevive a slide
poluído.

**Leia antes de escrever copy e antes de escrever HTML.** Em divergência com a skill, este arquivo
ganha.

## Os cinco princípios

**P1 · A capa vende uma unidade contável, não um tema.** A capa diz a forma do que vem (hábitos,
achados de um dataset, um binário resolvido) e sugere quantos são — um contrato finito que o
leitor sabe que vai terminar. Um número faz o trabalho de um parágrafo (`1540 posts`, um preço,
um benchmark); diga o ganho, não o processo. A capa é o maior gesto tipográfico da peça.

**P2 · Uma ideia por slide, headline primeiro.** Todo slide: headline (a conclusão, frase completa
que se sustenta sozinha, legível em ~1,5s), body opcional (o porquê, a ressalva, o exemplo),
prova opcional. Nunca rótulo, nunca teaser. **Teste de leitura corrida:** só as headlines, de cima
a baixo — se formarem um artigo coerente, o carrossel funciona. O leitor consome em duas
velocidades (passada rápida nas headlines, leitura lenta em 2–3 slides); slide que precisa do
anterior quebra a camada rápida.

**P3 · Trave um template, gaste a novidade no conteúdo.** Mesmos slots, mesma hierarquia, slide
após slide — o olho reaprende um layout novo em ~meio segundo, e em 12 slides isso é atenção gasta
em navegação. Só a posição no canvas respira. Invariantes: 4:5 (1080×1350); headline dona do terço
de cima (o de baixo é ilustração ou ar — ali moram a UI do Instagram e o dedão do leitor);
margem ~88px; sem indicador de página. Duas densidades, uma por peça: **leitura** (6–8 linhas de
body, o valor é a informação) ou **reconhecimento** (uma frase por slide, o valor é a
identificação). O meio do caminho funciona pior que qualquer um dos dois.

**P4 · Toda afirmação ancora no visualizável.** Nenhum slide argumenta com adjetivos; cada
afirmação se resolve num número, num artefato (um print prova a fonte mesmo ilegível), numa coisa
com nome (conceito que viaja e gera compartilhamento) ou numa cena exata (a forma mais afiada:
"sem um áudio de 7 minutos antes", não "comunicação ruim"). Especificidade produz reconhecimento,
e reconhecimento gera comentário. Faça a ressalva às claras — fonte, data, ou "não verificado":
honestidade dá autoridade.

**P5 · Virada, depois um pedido de baixo esforço.** O penúltimo slide é o ganho — onde a sequência
para de listar e começa a significar. O último pede uma coisa que o leitor já sabe responder:
palavra-chave para comentar (com recompensa dita, maior que o entregue) ou pergunta com resposta
pronta; nunca "o que você acha?". O CTA pode quebrar o registro visual e gritar mais alto que o
resto; pode ainda morar no rodapé de todo slide, sem depender do fim.

## Identidade: os slots

O Alvinegro (`design/identity.md`) preenche estes slots; declare-os uma vez no `<style>` e nunca
desvie entre slides: `GROUND` (fundo chapado, nunca degradê), `INK` (texto), `ACCENT` (exatamente
um, com um significado consistente do começo ao fim), `DISPLAY` / `BODY` (no máximo duas famílias;
o tamanho é a hierarquia), `MARK` (mobília de marca, mesmo canto e tamanho em todo slide), `ART`
(uma linguagem de ilustração ou `none` — sem ilustração é viável, mas é o modo difícil), `TEXTURE`
(opcional, sutil). **Teste do thumbnail:** a 20% e sem handle, ainda dá para identificar a conta?

## Frame e render

Cada slide: `<section class="slide">`, `1080×1350`, `overflow: hidden`, padding ≥ 88px,
`data-theme="light"` na raiz, estado final estático (sem hover, animação ou JS de conteúdo).
Todo slide carrega exatamente uma âncora visual com peso óptico dominante; "vazio" quase sempre é
espaço morto (conteúdo leve demais), não espaço negativo — corrija com escala e massa
tipográfica, nunca espalhando micro-elementos. Tipografia de referência a 1080 de largura:
headlines 70–110px, body 40–56px (nunca abaixo de ~36px no feed), capa acima disso.

```bash
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" --width 1080 --height 1350
```

Evite: foto de stock, degradê, emoji, biblioteca de ícones, terceira família tipográfica, dois
accents, slide sem frase, headline com ressalva (a ressalva mora no body).
