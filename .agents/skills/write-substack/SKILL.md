---
name: write-substack
description: >
  Produz um artigo ilustrado completo para o Substack: uma história sequencial com
  espinha narrativa de verdade, 3 a 8 imagens capturadas ao vivo de fontes primárias
  no navegador, e um título feito para ser aberto. Parte de uma tese que já saiu como
  Reel, de uma notícia recém-saída ou de uma ideia crua. Ative com comandos como
  "escreve o Substack da semana", "transforma <slug> em artigo",
  "escreve o artigo do Substack sobre <notícia>".
---

# SKILL · write-substack

## Propósito

Produzir um **artigo acabado** para a lista própria: uma história sequencial que o leitor escolhe ler com calma e responde. O LinkedIn publica a conclusão; aqui sai **o caminho até ela, mostrado** — com capturas reais da coisa primária no lugar certo.

Escreva como o usuário fala e pensa, na voz dele. Sem documento de audiência nem pilar: se faltar leitor-alvo ou ângulo, pergunte. Mire a resposta — o mesmo problema nomeado em dezenas de respostas é a próxima coisa que vale construir.

## Quando agir

- "escreve o Substack da semana"
- "transforma `<slug>` em artigo"
- "escreve o artigo do Substack sobre [notícia]"
- "escreve a versão em artigo do reel sobre X"
- qualquer variação que signifique peça longa e ilustrada de newsletter

## Dois caminhos de entrada

**Reuso.** Uma tese que já saiu como Reel (às vezes LinkedIn) levada a fundo. O `final.md` irmão existe em `posts/` e a ideia de origem já está `Processed`. **Este caminho não escreve nada no Notion** — a ideia carrega um único `Format`, e escrever `Substack` por cima apagaria o formato primário. Diga que está pulando a escrita, e por quê.

**Standalone.** Ideia nova do banco **Ideas** (`e2970ca3-7724-4a81-8f12-7ea34c048c67`) ou notícia trazida pelo usuário, sem irmãos. Filtre `Status = "Pending"`, ordene por `Date` decrescente, confirme a mais recente antes de seguir. No "pronto" explícito: `Status` → `Processed` + `Format` → `Substack`. Se a opção `Substack` não existir em `Format`, **pare e peça ao usuário para criar pela interface do Notion** (nunca pelo MCP). O conteúdo nunca sobe ao Notion.

## Entrada e saída

Slug em minúsculas, sem acento, hífens no lugar de espaço e pontuação. No reuso, reaproveite o slug do irmão para a tese morar sob um nome só. Tudo mora em `posts/substack/<slug>/`: a raiz guarda só o publicável (`final.md`, `cover.png`, `01.png`…`NN.png`); `sketch/` guarda o trabalho (`v1.md`, `v(N+1).md`, `shotlist.md`).

O primeiro rascunho é salvo em `sketch/v1.md` ao ser apresentado. Cada correção gera `v(N+1).md`: leia a versão anterior, copie os blocos imutados **verbatim**, aplique só o diff. No "pronto" explícito, copie o `v<N>` mais alto para `final.md`.

Ferramentas: MCP do Notion (ler o banco; escrever só no standalone) e automação do navegador para as capturas (invocar a skill de captura antes de usá-la).

## Como produzir

**1. Escolher o assunto.** No reuso, leia `posts/script/<slug>/final.md` inteiro (e o LinkedIn irmão, se existir) e separe o queimado (o que a audiência já viu) do cortado por tempo (o que 60 segundos jogou fora — isso é o artigo). No standalone, leia a ideia e vá às fontes primárias antes de planejar (anúncio, paper, model card, preços, changelog, repositório — nunca só a cobertura). Escolha pela profundidade do material capturável: se não dá para nomear três coisas a capturar antes de escrever, o assunto é magro — diga isso e proponha outro.

**2. Planejar antes de escrever.** Defina a espinha narrativa (investigação, reconstrução, teste ou decisão — use como repertório, não como formulário), um outline de 5 a 9 seções com headings-frase que contam a história na ordem, e a shot list em `sketch/shotlist.md` (âncora no texto, o que mostrar, onde capturar). Apresente espinha + outline + shot list e só escreva depois do OK — é o ponto mais barato para mudar de direção.

**3. Escrever e iterar.** Título declara a tese ou descoberta (ex.: "O que o model card do GPT-5 diz na página 14"); subtítulo acrescenta consequência ou custo, sem repetir. Abertura fria numa cena com número; corpo prepara cada imagem (diz o que olhar antes, o que levar depois) com marcadores `![NN — caption](NN.png)` inline; fecho termina numa pergunta que pede o material do leitor, sem CTA de assinatura nem despedida. Trave o texto antes de capturar.

**4. Capturar, legendar, fechar.** Capture cada take ao vivo no navegador, registre a URL da fonte na shot list na hora, salve na raiz do slug. Se um take não existe após tentativas honestas, reescreva o trecho para não depender dele — nunca preencha com decorativa. Legende dirigindo o olhar + fonte com link, leia o conjunto como leitor, e entregue com o comando de publicação (colar `final.md`, arrastar cada PNG sobre seu marcador, definir `cover.png` como capa).

## Restrições

1. O artigo é sequência, não argumento: headings lidos na ordem soam como uma coisa acontecendo depois da outra.
2. De 3 a 8 imagens no corpo mais a capa, cada uma captura real de fonte primária respondendo a uma pergunta que o texto acabou de levantar; nunca IA, stock, HTML montado ou print de tweet no lugar do fato; nada atrás de paywall ou privado.
3. No reuso, nenhuma frase passa verbatim do Reel; o material é o que a versão curta cortou.
4. Calibração: leia os dois `posts/substack/*/final.md` mais recentes (na primeira rodada, pule em vez de inventar).
5. Cada 400 palavras entrega algo checável (número, nome, captura, citação, link); o resto é cortado.

## Formato do final.md

```
# <título>
### <subtítulo>

<o artigo, com os marcadores ![NN — caption](NN.png) no lugar>

---
Palavras: <contagem>
ACP: <fase>
Espinha: <investigação | reconstrução | teste | decisão>
Artefato: <a coisa que não caberia num post de LinkedIn>
Imagens: <N>, ver shotlist.md
Fontes: <URLs primárias>
Reuso de: <slug>   <- só no reuso
```

## Fora do escopo

Não captura ideia crua (`registrar-ideia`), não escreve outros formatos, não gera arte, não publica — colar no Substack é manual.
