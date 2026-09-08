# Domingo — o artigo, 3 carrosséis, 2 posts de LinkedIn, agendar a semana

**Termina com:** 7 carrosséis de Instagram, 3 posts de LinkedIn, 1 artigo no Substack e os 11 posts agendados.
**Sem gravação e sem edição de vídeo.**
**Times de agentes são obrigatórios.** Retome a coordenadora do sábado para as atribuições e os slugs continuarem consistentes.

- [ ] **Retome a sessão coordenadora do sábado.**
  Confirme os 3 rascunhos de carrossel esperando correção, seus agentes originais, as 2 atribuições de reuso do LinkedIn, os 5 slugs fechados ontem e o assunto do artigo que você deixou escolhido.

## Substack — dispare primeiro, ele roda o dia inteiro

O artigo é a peça mais longa da semana e publica hoje. Comece antes da primeira revisão de carrossel, depois vá dando uma olhada nele entre as revisões.

- [ ] **Confirme o assunto** pela nota de ontem: uma das teses da semana, ou **notícia desta semana**. O artigo publica hoje, então nada aqui é perecível demais.
  Escolha pelo material, não pelo hook: o assunto certo é aquele em que você já consegue nomear três coisas que dá para ir capturar.
  ⚠️ Notícia só funciona se você alcança uma fonte primária: o paper, o model card, a página de preços. Sem isso não tem artigo, só o quinto resumo do mesmo anúncio.

- [ ] **Abra 1 sessão de agente e rode** `write-substack` nela. Depois deixe ela lá e comece as revisões de carrossel.

- [ ] **Aprove o plano quando ele voltar**: espinha, outline, shot list. Faça isso entre duas revisões. Leva dois minutos.
  🖋 É o lugar mais barato do dia inteiro para mudar de direção. Leia a shot list: se você não consegue imaginar a imagem, o agente não consegue capturar.

- [ ] **Itere o texto até travar, depois deixe o agente rodar a sessão de captura.** 3 a 8 capturas reais de navegador mais uma capa.
  ⚠️ Toda imagem é uma captura real de fonte primária. Se o agente oferecer foto de banco de imagens ou um diagrama que ele montou, é bug: devolva.

- [ ] **Revise o artigo com as imagens no lugar**, não só o texto. Cada imagem precisa de pista antes e de conclusão depois.

- [ ] **Gaste uma rodada só no título.** Ele é o assunto do email e a única coisa que a maior parte da lista vai ler.

## Revisão e correção — 3 carrosséis

Os primeiros rascunhos já existem. Retome os agentes originais para cada correção virar uma versão local nova em vez de uma reescrita.

- [ ] **Passe os 3 carrosséis restantes pelo loop de correção completo, uma revisão por vez:**
  1. Leia a copy completa dos slides e a legenda do post.
  2. Dê notas concretas ao agente daquela peça.
  3. Revise a versão corrigida e repita até o texto ser aprovado.
  4. Inspecione cada slide renderizado: hierarquia, overflow, quebra estranha, repetição e composição visual fraca.
  5. Mande as correções visuais ou de copy de volta para o mesmo agente e renderize de novo.
  6. Diga "pronto" só quando copy e slides renderizados estiverem publicáveis.

  Enquanto você revisa a próxima peça, os agentes corrigem as que já foram devolvidas. Nunca use dois agentes na mesma peça.

## LinkedIn — 2 agentes em paralelo

- [ ] **Despache 2 agentes de LinkedIn**, uma ideia de reuso reservada por agente. Cada um roda `build-linkedin`.
  Reaproveite a tese, não o texto do carrossel.

- [ ] **Passe os dois posts de LinkedIn pelo loop de correção completo:**
  1. Revise cada texto completo e devolva notas.
  2. Revise a versão corrigida e repita até a escrita ser aprovada.
  3. Revise cada imagem escolhida junto com seu post.
  4. Peça substituições ou correções de texto até cada par estar publicável.

  Primeiro rascunho não conta como pronto. Use o tempo de correção dos agentes para revisar o outro post ou fechar um carrossel.

- [ ] **Se um dos 3 posts de LinkedIn tem a mesma tese do artigo, entregue o artigo para esse agente.** Dê a ele `posts/substack/<slug>/final.md` para não repetir a peça, e faça o post fechar no link.
  🖋 Esse post é o motor de assinatura: leitor frio do LinkedIn a um clique da lista.

- [ ] **Confira a saída completa da semana:**
  - 7 pastas de carrossel em `posts/carousel/`, cada uma com `final.md` e os slides renderizados
  - 3 pastas de LinkedIn em `posts/linkedin/`, cada uma com `final.md` e `image.png`
  - 1 pasta de Substack em `posts/substack/`, com `final.md`, `cover.png` e as capturas numeradas
  - nenhuma peça ainda esperando sua revisão ou correção de agente

## Agendar

- [ ] **Só comece a agendar depois das 11 peças aprovadas.**
  Agendamento é trabalho protegido, não o lugar para descobrir copy inacabada ou slide quebrado.

- [ ] **Monte a grade antes de abrir qualquer app.** A janela começa hoje.

  | Dia             | Instagram   | LinkedIn   | Substack  |
  | --------------- | ----------- | ---------- | --------- |
  | **Dom (hoje)**  | carrossel 1 | —          | artigo 🖋 |
  | Seg             | carrossel 2 | LinkedIn 1 | —         |
  | Ter             | carrossel 3 | —          | —         |
  | Qua             | carrossel 4 | LinkedIn 2 | —         |
  | Qui             | carrossel 5 | —          | —         |
  | Sex             | carrossel 6 | LinkedIn 3 | —         |
  | Sáb             | carrossel 7 | —          | —         |

  O carrossel mais urgente primeiro. Guarde a peça evergreen mais forte para o fim da janela.
  ⏱️ O carrossel 1 sai hoje: se o horário já passou, publique agora em vez de agendar.
  🖋 O artigo também sai hoje, escrito hoje. Esse lag zero é o que deixa ele ser notícia.

- [ ] **Publique o artigo no Substack.** Está tudo em `posts/substack/<slug>/`: cole o `final.md`, arraste cada PNG para o marcador `![NN — …]` dele, cole as legendas das imagens, defina `cover.png` como capa.
  ⚠️ O Substack manda email. Um erro de digitação chega na lista inteira e não dá para editar depois de enviar: leia o título e o primeiro parágrafo mais uma vez antes de apertar publicar.

- [ ] **Agende os 7 carrosséis** no Instagram, cada um com sua legenda.

- [ ] **Agende os 3 posts de LinkedIn.** Se um deles linka o artigo, coloque esse na segunda, logo atrás dele.

- [ ] **Confira a grade inteira antes de fechar.**
  Confirme datas, canais, legendas, ordem dos slides, imagens do LinkedIn e as capturas do artigo.

- [ ] **Feche as 7 ideias no Notion:** `Status` → `Processed`, `Format` → `IG Carousel`.
  ⚠️ As 3 ideias reaproveitadas só carregam um `Format`. Mantenha o formato primário do Instagram. O artigo não adiciona nada aqui. `write-substack` pula a escrita no Notion de propósito quando reaproveita uma tese. Se o artigo veio de notícia nova, essa ideia fecha sozinha como `Substack`.

Próximo: **[Sábado](saturday.md)**
