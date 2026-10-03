---
name: carousel
description: >
  Produz um carrossel de Instagram completo, de ponta a ponta: lê uma ideia do
  banco Ideas, escreve a copy dos slides e a legenda do post na voz do usuário,
  depois compõe e renderiza a arte dos slides como PNGs 4:5. Ative com comandos
  como "escreve o carrossel da última ideia", "faz um carrossel", "renderiza o
  carrossel <slug>", "redesenha a arte do carrossel", ou quando o feedback é
  sobre espaço vazio, hierarquia fraca ou narrativa nos slides do carrossel.
  Não serve para carrossel de thread em X-cosplay (isso é build-thread-carousel).
---

# SKILL · Carrossel

Transforme uma ideia crua num carrossel pronto: copy **e** arte, numa entrega só. A headline é a
âncora, o template só trava se a copy tiver uma forma que se repete, e mexer na copy costuma ser a
resposta certa para um problema visual.

Atue como copywriter sênior e diretor de arte na mesma peça, na voz do usuário.

## Entrada

**Ideias** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`): se o usuário não citou nenhuma, pegue a mais
recente com `Status = Pending` e confirme antes de seguir. Essa leitura e a escrita de fechamento
são o único contato com o Notion — o conteúdo nunca sobe.

**Antes de escrever** (copy e HTML): leia `assets/carousel-craft.md` e `design/identity.md`
(Alvinegro). Em caso de divergência, o craft doc ganha. Não existe documento de audiência nem de
pilar: se a peça precisar de leitor-alvo ou ângulo, pergunte.

**Entrando no meio do fluxo:** se `posts/carousel/<slug>/sketch/v<N>.md` já existe, trabalhe da
versão mais alta; pedido de arte pula direto para a arte, mudança de copy gera `v(N+1)` e
re-renderiza.

## Fluxo

1. **Copy.** Extraia da ideia o ângulo (a posição, não o tema), a unidade contável do carrossel
   (passos, achados, erros…), a tese em 1–2 frases e as provas (números, artefatos, nomes, cenas).
   Escolha a densidade e segure ela na peça inteira: **reconhecimento** (uma frase por slide,
   swipe rápido) ou **leitura** (6–8 linhas de body por slide, feito para salvar).
2. **Apresente copy + legenda, salve e itere.** Slides e legenda separados; cada correção do
   usuário gera `v(N+1)` copiando os blocos imutados **verbatim**, só o diff. Pergunte se pode
   partir para a arte.
3. **Arte.** Trave um template único (slots, hierarquia e posições; capa e CTA invertem por
   padrão) e componha `sketch/carousel.html`: um arquivo só, N × `<section class="slide">`, sem
   stylesheet externa, partindo do `<style>` e `<defs>` de `design/proof/proof.html`.
4. **Renderize, revise, apresente.** Renderize, abra os PNGs com Read, corrija e re-renderize
   antes de entregar. **Problema visual costuma ser problema de copy** — conserte a copy
   (novo `v(N+1)`), não encolha a tipografia para caber copy ruim.

```bash
uv sync # uma vez por máquina; + `uv run playwright install chromium` se precisar de navegador
uv run python scripts/render_html_to_pngs.py \
  --html "posts/carousel/<slug>/sketch/carousel.html" \
  --out "posts/carousel/<slug>" \
  --selector ".slide" --width 1080 --height 1350
```

## Formato da copy

```
SLIDE 1 — COVER
Headline: [a unidade contável + o ganho, com número de verdade se existir]
Sub: [opcional, 1 linha]

SLIDE 2…N-1 — [uma ideia por slide]
Headline: [a conclusão, frase completa que se sustenta sozinha]
Body: [o apoio] / Proof: [número, artefato, nome ou cena exata]

SLIDE N-1 — REFRAME
Headline: [o que a lista significa no fim]

SLIDE N — CTA
Headline: [o pedido] / Action: [a palavra, ou a pergunta]
```

Legenda do post: primeira linha para o scroll sozinha, 2–4 parágrafos curtos ampliando o argumento
(industrial, não repetição dos slides), um CTA específico, 3–5 hashtags, 80–180 palavras.

> Calibração de capa — bom: "Eu li 1540 posts do Reddit para ver como as pessoas estão ganhando
> dinheiro com IA". Ruim: "Tudo sobre IA para negócios" (tema, não unidade contável).

## Restrições

- **Teto rígido: 10 slides.** Capa e CTA ocupam dois; se as unidades passarem de oito, junte
  irmãos, corte contexto, estreite a promessa da capa ou mude de formato — nunca trunque a lista.
- Headline é conclusão, nunca rótulo nem teaser; teste de leitura corrida: só as headlines, de
  cima a baixo, formam um artigo coerente.
- CTA: uma palavra para comentar (com recompensa dita) ou pergunta com resposta óbvia; nunca
  "o que você acha?".
- Template travado: elementos e hierarquia não mudam de um slide para outro, só a posição respira.
- 1080×1350 fixo, margens ~88px; o overflow não é checado sozinho — revise os renders.
- Slug: minúsculas, sem acento, hífens. `sketch/` guarda `v<N>.md` + `carousel.html`; a raiz do
  slug guarda só o publicado (`01.png`…`10.png` e, no fechamento, `final.md`).

## Fechamento ("pronto")

No "pronto" explícito, copie o `v<N>.md` mais alto **verbatim** para `posts/carousel/<slug>/final.md`
e atualize a ideia de origem: `Status` → `Processed`, `Format` → `IG Carousel`. Vale também parando
na copy (sem PNGs). Entregue os caminhos do `final.md` e dos PNGs e informe o número de slides.

## Fora do escopo

Ideias cruas (`registrar-ideia`), Reel (`write-script`), thread (`write-thread`), LinkedIn
(`build-linkedin`), estética X-cosplay (`build-thread-carousel`), adaptação para outra plataforma
sem pedido, publicação (manual, pelo usuário, a partir dos arquivos finais).
