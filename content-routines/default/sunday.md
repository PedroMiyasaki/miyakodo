# Domingo — revisar os cortes, escrever LinkedIn e o artigo, agendar a semana

**Termina com:** 5 reels em `posts/script/<slug>/` (cada pasta de roteiro com `reels.mp4`, `caption.md` e `cover.png`), 3 posts de LinkedIn, 1 artigo no Substack, 9 posts agendados.
**Sessões no pico:** default: 9 (1 Substack + 5 retomadas + 3 LinkedIn) · multitask: 5 (1 Substack + 1 retomada + 3 LinkedIn). Contexto: [README](README.md).

## Substack — dispare primeiro, ele roda o dia inteiro

O artigo é a peça mais longa da semana e publica hoje. Comece antes de assistir a um único corte, depois vá dando uma olhada nele entre as revisões.

- [ ] **Escolha o assunto.** Ou a mais profunda das 5 ideias que você gravou, ou **notícia desta semana**: o artigo publica hoje, então nada aqui é perecível demais.
  Escolha pelo material, não pelo hook: o assunto certo é aquele em que você já consegue nomear três coisas que dá para ir capturar.
  ⚠️ Notícia só funciona se você alcança uma fonte primária: o paper, o model card, a página de preços. Sem isso não tem artigo, só o quinto resumo do mesmo anúncio.

- [ ] **Abra 1 sessão de agente e rode** `write-substack` nela. Depois deixe ela lá e vá assistir aos cortes.

- [ ] **Aprove o plano quando ele voltar**: espinha, outline, shot list. Faça isso entre duas revisões de corte. Leva dois minutos.
  🖋 É o lugar mais barato do dia inteiro para mudar de direção. Leia a shot list: se você não consegue imaginar a imagem, o agente não consegue capturar.

- [ ] **Itere o texto até travar, depois deixe o agente rodar a sessão de captura.** 3 a 8 capturas reais de navegador mais uma capa.
  ⚠️ Toda imagem é uma captura real de fonte primária. Se o agente oferecer foto de banco de imagens ou um diagrama que ele montou, é bug: devolva.

- [ ] **Revise o artigo com as imagens no lugar**, não só o texto. Cada imagem precisa de pista antes e de conclusão depois.

- [ ] **Gaste uma rodada só no título.** Ele é o assunto do email e a única coisa que a maior parte da lista vai ler.



## Revisar os 5 cortes

- [ ] **Retome o layout de ontem.** Reabra tudo que você precisa antes de revisar qualquer corte.
  - **default:** as 5 sessões de agente de ontem, uma por slug.
  - **multitask:** a sessão coordenadora de ontem. Ela já conhece os cinco slugs. Não abra cinco novas.

- [ ] **Assista a cada corte e devolva notas em linguagem simples**: abertura arrastada, ponto repetido, pausa morta, corte caindo na palavra errada. A sessão que escreveu o roteiro conhece ele, então fale do conteúdo, não de timestamp. Itere até dar para postar.
  🔥 Dois primeiros segundos: corte seco, zero intro. Se a abertura arrasta, essa é a primeira nota.
  Um corte que não precisa de nada está pronto. Aceite e siga.

- [ ] **Confira:** `video/inputs/` vazia, as 5 pastas de roteiro desta semana em `posts/script/`, cada uma com seu vídeo, sua legenda do post e sua capa.



## LinkedIn (3 sessões de agente novas, em paralelo)

- [ ] **Escolha as 3 mais técnicas das 5 ideias que você gravou.** Reaproveitar ganha de ideia nova do banco.

- [ ] **Abra 3 sessões de agente e rode** `build-linkedin` em cada uma. Itere até o "pronto" (texto + imagem).
  Presença, não alcance. Não force um hook nelas.

- [ ] **Se um dos 3 tem a mesma tese do artigo, entregue o artigo para esse agente.** Dê a ele `posts/substack/<slug>/final.md` para não repetir a peça, e faça o post fechar no link.
  🖋 Esse post é o motor de assinatura: leitor frio do LinkedIn a um clique da lista.



## Agendar

- [ ] **Monte a grade antes de abrir qualquer app.** A janela começa hoje.

  | Dia             | Instagram                | LinkedIn   | Substack  |
  | --------------- | ------------------------ | ---------- | --------- |
  | **Dom (hoje)**  | reel 1 🔥                | —          | artigo 🖋 |
  | Seg             | reel 2 🔥                | LinkedIn 1 | —         |
  | Ter             | reel 3 🔥                | —          | —         |
  | Qua             | reel 4 🔥                | LinkedIn 2 | —         |
  | Qui             | reel 5 🔥                | —          | —         |
  | Sex             | reel de stock, se houver | LinkedIn 3 | —         |
  | Sáb             | —                        | —          | —         |

  O reel mais perecível primeiro. Notícia hoje ou segunda. Uma tese atemporal sobrevive até quinta.
  ⏱️ O reel 1 sai hoje: se o horário já passou, publique agora em vez de agendar.
  🖋 O artigo também sai hoje, escrito hoje. Esse lag zero é o que deixa ele ser notícia.

- [ ] **Publique o artigo no Substack.** Está tudo em `posts/substack/<slug>/`: cole o `final.md`, arraste cada PNG para o marcador `![NN — …]` dele, cole as legendas das imagens, defina `cover.png` como capa.
  ⚠️ O Substack manda email. Um erro de digitação chega na lista inteira e não dá para editar depois de enviar: leia o título e o primeiro parágrafo mais uma vez antes de apertar publicar.

- [ ] **Agende os 5 reels** no Instagram, cada um com a legenda do seu roteiro.

- [ ] **Agende os 3 posts de LinkedIn.** Se um deles linka o artigo, coloque esse na segunda, logo atrás dele.

- [ ] **Confira a grade inteira antes de fechar.** Post no dia errado só aparece na quinta, tarde demais para consertar.

- [ ] **Feche as ideias no Notion:** `Status` → `Processed`.
  ⚠️ Uma ideia reaproveitada só carrega um `Format`: registre `Reel`. O artigo não adiciona nada aqui. `write-substack` pula a escrita no Notion de propósito quando reaproveita uma tese. Se o artigo veio de notícia nova, essa ideia fecha sozinha como `Substack`.

Próximo: **[Sábado](saturday.md)**
