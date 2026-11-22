[HOOK] · literal
Se você tá desenvolvendo qualquer use-case com IA,
você precisa conhecer uma coisa chamada **evals**.

[pause]

Evals são um assunto técnico,
mas são muito importantes tanto pra pessoa técnica
quanto pra pessoa de negócio que tá querendo fazer a adoção de IA.
Então, mesmo que você não seja técnico,
eu sugeriria você ver esse vídeo.

[PROMESSA] · tópicos
- imagina um: lê os milhares de contratos de fornecedor que chegam na sua empresa
- aponta as cláusulas críticas pro seu negócio: multa, renovação automática → triagem antes do jurídico

[DEGRAU] · tópicos
Num mundo sem evals, você faria assim.
- joga os contratos no agente, instruções no prompt = o texto que diz pra IA o que fazer
- e torce: que ele aponte as mesmas cláusulas que o seu jurídico apontaria

[VIRADA] · tópicos
- e se ele apontar cláusula demais?
- e se ele deixar passar justo a que importa?

[DEGRAU] · tópicos
- cláusula demais → jurídico relê tudo → perde mais tempo do que ganha
- deixou passar → a multa que ninguém viu → contrato assinado

[VIRADA] · literal
E mesmo que você vá pra esse caminho de tentar arrumar essas cláusulas excessivas, ou essas cláusulas faltantes, de maneira manual.
Quem garante que, mexendo na resposta do agente pra um contrato específico, você não tá causando problema em outros contratos?
Efetivamente você arruma um problema, mas faz o resto do sistema regredir em qualidade.

[VIRADA] · literal
É aqui que os evals entram.
Um eval é uma prova com gabarito pro seu agente.

[DEGRAU] · tópicos
- 50 contratos que o seu jurídico já analisou, inclusive os cheios de pegadinha
- resposta certa de cada um = golden dataset, o gabarito da prova

[VIRADA] · literal
Então, toda vez que você mexer no agente, ele faz essa prova de novo.

[DEGRAU] · tópicos
- roda nos 50 → compara cada resposta com o gabarito → acertou 46 de 50
- os dois "e se" lá de trás viram número: quantas apontou à toa, quantas deixou passar
- mexeu no prompt, caiu pra 44 → você vê quais dois quebraram antes de chegar no jurídico

[DEGRAU] · tópicos
Só que o maior ganho nem é pegar erro.
- quem monta o gabarito é o jurídico, não o programador → o negócio define o certo
- sem gabarito, "o agente tá bom?" = opinião de quem testou por último
- contrato novo, regra nova no prompt → os 50 antigos continuam passando
- melhorar vira meta: 46 → 48, sai do palpite

[pause]

[RECOMPENSA] · literal
Com evals, você **não torce**.
Você sabe que ele acerta 46 de 50, sabe quais são os 4 que ele erra,
e sabe se a próxima mudança deixou ele melhor ou pior.

[CTA] · literal
Esse assunto é muito grande, então eu não consigo falar tudo nesse Reel de três minutos.
Mas ele é dos assuntos mais quentes do Vale do Silício nesse momento,
e há muitos grandes laboratórios escrevendo ótimos guias
de como você pode incorporar essa prática
em qualquer produto de IA que você esteja desenvolvendo.
E se você quiser receber o que eu considero dos melhores guias sobre esse assunto,
comenta EVALS aqui embaixo que eu te mando o link.

---
Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.
Nos dois degraus que abrem com frase, a frase é lida e os tópicos são falados no mesmo take.
