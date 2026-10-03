# assets/ — arquétipos do carrossel derivado de thread

Arquétipos executáveis da skill `build-thread-carousel`: cada HTML abre no navegador e renderiza um slide de demonstração com placeholders. Duas subpastas, mesma estrutura (`_carousel.css`, `hook-display.html`, `body-paragraph.html`):

- **`default/`**: modo padrão — layout X-cosplay (cabeçalho do X: avatar + nome + selo azul + handle; conteúdo centralizado na vertical) em paleta clara e neutra.
- **`x/`**: modo X — dark mode, clone fiel do Twitter/X (serve também como stills de fundo de Reel).

| Arquivo | Papel |
|---|---|
| `_carousel.css` | Chrome compartilhado do modo (1080×1350, cabeçalho, centralização vertical, slot de mídia, render de markdown). Autocontido: valores inline, sem stylesheet externo. Mudou aqui, mudou em todo carrossel do modo. |
| `hook-display.html` | Primeiro slide (T1): primeiro parágrafo como headline em negrito de 40px, resto em body de 30px. |
| `body-paragraph.html` | Demais slides (T2–T(N)): texto de 30px com markdown rico. Sem arquétipo de fechamento: dê peso à frase final com `**negrito**` ou `> citação` dentro do body. |

**Placeholders:** `{{NAME}}`, `{{HANDLE}}`, `{{AVATAR_URL}}` no cabeçalho (e `{{IMAGE_URL}}` no slot de exemplo). A skill pergunta os três ao usuário antes de gerar — nunca invente.

**Imagens:** slot `.tweet-media` opcional embaixo do texto (cantos de 18px, altura fixa de 360px, `object-fit: cover` corta sozinho). Regras — manual em `sketch/images/` sempre ganha; T1 sempre tem imagem; T2+ só slide curto (~250 caracteres sem setas). Procedimento de busca e formato da copy: `SKILL.md` §§ 1–2 (não duplicado aqui).

**Limites:** tudo otimizado para 1080×1350; overflow de texto longo + imagem não é checado sozinho — revise o HTML antes de renderizar. O único azul do X que sobrou é o do selo de verificado (`#1d9bf0`); o resto da paleta é neutra.
