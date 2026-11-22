SLIDE 1 - CAPA
Headline: A IA chamou o bug de impossível. Torvalds fez 4 movimentos de debug.
Sub: 24 patches, 18 boots e uma correção de uma linha.

SLIDE 2 - CENA
Headline: O sintoma era uma tela preta. A causa ocupava só 2 KiB.
Body: Numa Battlemage G21 de 16 GiB, o driver Intel Xe entregava parte do armazenamento de compressão como VRAM livre. Quando a page table do compositor caía ali, o GDM reiniciava sem parar.
Proof: Commit 818bebe, arquivo xe_vram.c.

SLIDE 3 - MOVIMENTO 1
Headline: 1. Torvalds não aceitou “impossível” como critério de parada.
Body: A IA disse várias vezes que o problema era insolúvel e sugeriu encerrar com um relatório. Torvalds mandou continuar e pediu mais código de debug.
Proof: “We should just write a report about it.” Linus Torvalds.

SLIDE 4 - MOVIMENTO 2
Headline: 2. Cada dúvida virou mais código de diagnóstico.
Body: Foram 24 patches adicionando informação de debug. Em vez de pedir outro palpite, ele usou a IA para instrumentar o kernel e analisar o que voltava.
Proof: 24 patches de debug registrados por Torvalds.

SLIDE 5 - MOVIMENTO 3
Headline: 3. Ele repetiu o teste até separar padrão de acaso.
Body: Foram 18 boots do kernel. Em todo cold boot, a page table de uma VM Mesa caía na página corrompida. Reiniciar o GDM mudava a alocação e fazia o sintoma sumir.
Proof: 18 boots. Cold boot falhava, e reiniciar o GDM funcionava.

SLIDE 6 - MOVIMENTO 4
Headline: 4. Os bytes mostraram quem estava invadindo a página.
Body: A página reservada revelou padrões 0xcccc… e 0xcc77…: metadados de compressão. A correção trocou round_up() por round_down() e excluiu exatamente uma página.
Proof: A mudança final teve 18 adições e 5 remoções em xe_vram.c.

SLIDE 7 - REFRAME
Headline: A IA executou o debug. Torvalds controlou a hora de parar.
Body: Quando pressionada, ela continuou adicionando código e analisando os resultados. Mas a confiança dela não virou evidência. O próximo teste e o critério de parada continuaram com o engenheiro.
Proof: Torvalds deixou a própria IA escrever a mensagem do commit.

SLIDE 8 - CTA
Headline: Quando a IA disser “impossível”, você fecha o relatório ou pede outro diagnóstico?
Action: Responda: relatório ou diagnóstico.

---

O ponto mais útil desse debug começou quando a IA disse que o bug era “impossible and unsolvable”.

No commit 818bebe, Linus Torvalds conta que o agente quis encerrar a investigação com um relatório. Ele fez o contrário: continuou pedindo código de debug, repetiu o boot, comparou o comportamento e inspecionou a página corrompida. Foram 24 patches e 18 boots até chegar à troca de round_up() por round_down().

A IA não foi inútil. Torvalds escreveu que ela fez muito do trabalho braçal, continuou adicionando debug e analisou os resultados quando pressionada. O erro seria aceitar a confiança dela como prova de que não havia solução. Nesse caso, o agente acelerou os experimentos. O critério de parada ficou com quem estava no teclado.

Você fecharia o relatório ou pediria outro diagnóstico?

Fontes: commit 818bebe, de Linus Torvalds (21 de agosto de 2026), e Simon Willison (22 de agosto de 2026).

#IA #Linux #Debugging #Programação #EngenhariaDeSoftware
