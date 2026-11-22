---
slug: as-cinco-areas-mais-expostas-a-disrupcao-por-ai
entrada: video/hooks/trabalho_cortado.mp4
versao: v2
status: aprovado
duracao_original: 5.0
duracao_prevista: 27.5
---

## Pedido do usuário
(observações literais, sem reinterpretação)

- Pedido na conversa: "Legal, agora execute a skill de edição de vídeo no modo lista com gancho para essa ideia que acabamos de registrar."
- Aprovação da estrutura e instrução de produção: "Tá muito bom. É, pode produzir o vídeo, e na hora de você produzir, lembra que as imagens dos banners devem ser um fundo branco... e o contraste preto. A intenção é que o título pareça uma referência a uma imagem que vem de um recurso externo e a legenda pareça uma legenda sobre uma imagem que vem de fora, mesmo que na prática as imagens estejam sendo feitas por você."
- Ideia de origem: "As cinco áreas mais expostas à disrupção por AI", banco Ideas, Status Pending, Format Reel. https://app.notion.com/p/3fcffe7442fd81cfb15bfac4d5fcaa43
- Pedido original da ideia, em conversa anterior: "A ideia é fazer vídeo. Com gancho chamativo. E falando de cada área e pouco dos motivos. Do por que ela é tão disruptável."

## Comportamentos padrão
- Legenda: não se aplica. Pelas medições, o gancho sorteado não tem fala, então `legenda-evals` não entra. As legendas do gancho, dos banners e do CTA são overlays próprios deste modo.
- Espaço morto: não se aplica. Sem fala, não há corte rente à voz; o take 1 entra inteiro, de 0,0 s a 5,0 s.
- Modo: lista-com-gancho
- Opcionais: perfil-pb desligado; aviso-2x desligado.
- Exceções: nenhuma pedida pelo usuário.

## Decisões e intenção
- Sorteio: `random.SystemRandom` entre os seis .mp4 da raiz de `video/hooks/` (normais e espelhados; `originais/` ficou fora). Resultado: `trabalho_cortado.mp4`. Não foi repetido nem trocado.
- Ausência de fala: o áudio não foi transcrito nem ouvido. As medições indicam que não há fala: o áudio fica abaixo de -35 dB quase o clipe inteiro, com um único evento de cerca de 60 ms em 2,15 s. Pico do clipe: -29,7 dB; média: -50,0 dB. Se houver voz, reabrir o plano.
- Áudio do gancho: o original tem nível muito baixo (cerca de -50 dB) e nenhuma fala detectada pela medição. Se mantido, vai em `<audio>` separado, com o `<video>` mudo. Decisão pendente do usuário.
- Formato do gancho: HEVC 10 bits com HLG (bt2020), 2160 × 3840, 60 fps. Convertido para SDR 1080 × 1920 em `assets/gancho-sdr.mp4` (H.264, 60 fps, AAC).
- Take 1: "Cinco áreas na mira da IA. Uma pode ser a sua." Chamada de curiosidade com relevância pessoal.
- Cartões dos banners: fundo branco, tinta preta, moldura preta de 4 px. Cada cartão traz o rótulo "Fig. NN" acima do título, como referência a uma figura externa. O take mostra o cartão centralizado sobre tela preta, com a legenda branca abaixo, separada por um filete e com "Fig. NN." em negrito.
- Sem crédito de fonte nas figuras: não há "Fonte: Sequoia" nem outro nome real, porque as figuras são desenhos originais e atribuí-las ao artigo seria falso. O efeito de imagem externa vem do rótulo "Fig." e da legenda.
- Categoria das legendas dos banners: motivo da exposição, como pede a nota ("pouco dos motivos"). A imagem explica a área; a legenda dá a razão em uma frase.
- Itens: as cinco primeiras verticais do mapa de oportunidades do artigo, na ordem dele, conforme a nota registrada no Notion. O artigo diz que a lista é ilustrativa, então o gancho não promete ranking.
- Dados das legendas, todos do artigo: falta de contadores nos EUA e 80% a 90% do trabalho de tributária como inteligência.
- Banners de 3,5 s, e não 3 s, porque as legendas têm de 9 a 11 palavras e a skill manda ajustar ao tempo de leitura.
- Palavra-chave: `riscos`. Em uso nos `respostas-comentarios.md` de `posts/`: `especialista` e `evals`, sem conflito.
- Frase do CTA: "Eu envio o material no direct para quem quiser saber mais." O material ainda não foi definido; nenhum recurso foi presumido.
- Notion: somente leitura nesta etapa. Format segue como Reel, preenchido na captura (ver pendências).

## Cortes propostos
- Nenhum. O gancho entra inteiro. Banners e CTA são takes sem vídeo de fonte.

## Linha do tempo (tempos da edição)
Textos v2 aprovados em 2026-10-18. Capturas atualizadas em `plano/take-01.png` a `plano/take-07.png`; folha completa em `plano/sequencia.png`. Layout e carregamento de imagens verificados nos sete takes.

| # | Início | Fim | Tipo | Conteúdo | Captura | Motivo |
|---|--------|-----|------|----------|---------|--------|
| 1 | 00:00.0 | 00:05.0 | gancho | "As 5 áreas com mais oportunidade de disrupção com AI"; linha menor: "(segundo a Sequoia Capital)" | a atualizar | pedido do usuário |
| 2 | 00:05.0 | 00:08.5 | banner | Corretagem de seguros: "Comparar propostas e preencher formulários sem crescer a equipe na mesma proporção." | a atualizar | eficiência e escala |
| 3 | 00:08.5 | 00:12.0 | banner | Contabilidade e auditoria: "Automatizar rotinas para atender mais clientes com a equipe que você já tem." | a atualizar | eficiência e escala |
| 4 | 00:12.0 | 00:15.5 | banner | Ciclo de receita em saúde: "Transformar notas clínicas em códigos de faturamento com menos trabalho manual." | a atualizar | eficiência e escala |
| 5 | 00:15.5 | 00:19.0 | banner | Regulação de sinistros: "Agilizar a análise de apólices e danos, mantendo especialistas nas exceções." | a atualizar | eficiência e escala |
| 6 | 00:19.0 | 00:22.5 | banner | Consultoria tributária: "Processar regras de várias jurisdições e liberar especialistas para decisões complexas." | a atualizar | eficiência e escala |
| 7 | 00:22.5 | 00:27.5 | CTA | comenta: "operação"; frase: "Eu envio o material no direct para quem quiser saber mais." | a atualizar | take final |

## Revisão editorial v2 (prevalece sobre as decisões da v1)
- Público: empresários e gestores que já operam nessas áreas. Oportunidade de eficiência, capacidade e escala, não ameaça ao emprego nem renda extra para iniciantes.
- Gancho ditado pelo usuário, com correção apenas de "áres" para "áreas" e capitalização de Sequoia Capital.
- Ressalva factual: o artigo traz um mapa ilustrativo, não um ranking das cinco maiores oportunidades. A chamada aprovada não deve ser apresentada na legenda da publicação como ranking formal da Sequoia.
- Imagens: preservar cartões brancos com contraste preto e legenda externa. Substituir gráficos de saída de profissionais por fluxos de entrega do serviço.
- Palavra-chave: "operação", substituindo "riscos".
- Textos aprovados; sequência visual v2 atualizada e aguardando revisão. Figuras agora mostram fluxos de execução, revisão de exceções e entrega, sem gráficos de saída de profissionais.
- Áudio: conforme a versão atual do modo Lista com gancho, ignorar o áudio do gancho. Música será adicionada pelo usuário no Instagram; as antigas pendências de áudio da v1 deixam de valer.
- v2 (2026-10-18): chamada aprovada com subtítulo da Sequoia Capital, cinco legendas orientadas a gestores, fluxos de oportunidade e CTA "operação". Sete quadros e sequência regenerados, sem render final.

## Composição
- Ainda não montada. Será feita depois da aprovação da sequência, com a timeline acima (root de 27,5 s, clips com `data-start` e `data-duration`).
- Mídias já prontas em `assets/`: `gancho-sdr.mp4`, `card-01.png` a `card-05.png` e as fontes em `assets/fonts/`.
- Antes do render, o `<video>` precisa de `id`. Um rascunho descartado foi bloqueado por isso no `check`.
- `assets/html/`, `assets/gerar_banners.py` e `assets/figuras.py` regeneram os cartões e os quadros de conferência.

## Pendências e dúvidas
- Render autorizado em 2026-10-18: "Pode gerar o video". Composição em `index.html`, sem áudio, 1080 × 1920, 27,5 s e 30 fps.
- `hyperframes@0.8.169 check` passou: zero erros de runtime, layout ou motion em sete amostras. Um aviso de organização de track densa, sem erro de render. Exportação final concluída e verificada: `posts/script/as-cinco-areas-mais-expostas-a-disrupcao-por-ai/as-cinco-areas-mais-expostas-a-disrupcao-por-ai.mp4` (movido para a pasta da peça a pedido do usuário), H.264, 1080 × 1920, 30 fps, 825 frames, 27,5 s, 6.255.055 bytes, sem trilha de áudio. Decodificação completa pelo FFmpeg sem erros. Captura por screenshot com GPU de hardware; render em aproximadamente 55 s.
- Conferência visual: as imagens foram checadas por medição (fontes carregadas, posições, cores), não por inspeção visual. Conferir `plano/sequencia.png` antes de aprovar.
- Áudio do gancho: não ouvido. Decidir se mantém ou muta.
- Quadro do gancho: não inspecionado visualmente. Conferir se a caixa de legenda do take 1 não cobre o assunto principal.
- Material do CTA: não definido. A frase promete "o material", então o recurso precisa existir antes da publicação.
- Format no Notion: o registrar-ideia pede o campo vazio na captura. Preenchi Reel. Manter ou limpar?
- Resposta automática (última etapa): exige a pasta da peça em `posts/` e o link do post publicado. Hoje nenhum dos dois existe.

## Histórico
- v1: estrutura aprovada pelo usuário. Cartões, quadros de conferência e sequência gerados. Um rascunho de composição foi montado antes da aprovação, bloqueado pelo `check` e removido. Sem render.
