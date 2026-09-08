# Sábado — 5 roteiros, 5 gravações, primeira passada de edição

**Termina com:** 5 roteiros em `posts/script/`, 5 vídeos em `video/inputs/`, 5 primeiros cortes renderizando. O que fica aberto depende do modo.
**Não publica nada.** Contexto e o teste 🔥: [README](README.md).

**Modo: escolha antes de abrir qualquer coisa.** `default`, a não ser que você queira velocidade.

| Modo | Quando | O que você abre |
|---|---|---|
| **default** | Isolamento. Uma conversa por peça. | 5 sessões de agente |
| **multitask** | Velocidade. Uma conversa tocando o dia. | 1 sessão abrangendo 5 agentes |

- [ ] **Leia os [aprendizados](../aprendizados.md) mais recentes**, as entradas do topo primeiro, antes de qualquer coisa.
  ⚠️ O que quebrou na semana passada repete hoje se você não ler agora. Erro novo hoje → entrada nova lá.

- [ ] **Escolha 5 ideias de fase A** no banco Ideas (`ACP Phase` = `A · Audience`), todas passando no teste 🔥.
  ⚠️ Nada de notícia perecível: um reel gravado hoje pode só ir ao ar na quinta.
  🖋 Tente deixar pelo menos uma das 5 com profundidade de verdade embaixo: um número, uma decisão que você tomou, código que dá para colar. O artigo de domingo normalmente sai de uma delas. Não é regra dura: notícia da semana pode ocupar esse slot no lugar.

- [ ] **Escreva os 5 roteiros.** Itere até o "pronto" nos 5.
  🔥 Gaste as iterações nas duas primeiras linhas. Um hook que não segura o scroll invalida o resto.
  - **default:** Abra 5 sessões de agente, uma por roteiro, e rode `write-script` em cada uma.
  - **multitask:** Abra 1 sessão coordenadora. Ela abrange 5 agentes, um por roteiro, roda `write-script` em cada um e é dona do processo: você fala com a sessão, não com os cinco agentes. Os agentes se coordenam por ela (slugs compartilhados, sem hook colidindo, sem dois agentes na mesma peça).

- [ ] **Grave os 5 no teleprompter, num lote só**: mesma luz, mesma roupa, mesmo setup.
  💡 Grave um 6º se o dia permitir. Ele pula o agendamento e vira stock.

- [ ] **Tire as gravações do celular** para `video/inputs/`, cada arquivo **com o nome do slug do roteiro**.
  ⚠️ Daqui em diante todo passo é endereçado por slug. Não deixe cinco exports sem nome.

- [ ] **Dispare a primeira passada de edição** no mesmo layout em que você escreveu. Rode `edit-video` uma vez por roteiro, no mode que encaixa:
  - puxado por notícia → `news`
  - tese / posição → `baseline`
  - legenda queimada no vídeo → só se você pedir (`subtitles` é opt-in, o Instagram gera a dele)
  **Dispare e vá embora.** Não revise hoje à noite: isso é a primeira tarefa de amanhã.
  - **default:** dispare nas mesmas 5 sessões de agente.
  - **multitask:** dispare da sessão coordenadora, que despacha `edit-video` para cada um dos 5 agentes.

- [ ] **Deixe uma nota de retomada para o domingo.**
  - **default:** qual sessão de agente é dona de qual slug. Amanhã retoma as 5.
  - **multitask:** que este fim de semana é multitask, e o nome da sessão coordenadora. Amanhã retoma essa única sessão.

Próximo: **[Domingo](sunday.md)**
