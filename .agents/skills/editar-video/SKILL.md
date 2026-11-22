---
name: editar-video
description: Edita um vídeo de entrada em video/inputs usando HyperFrames, a partir das observações do usuário. Sempre mostra um plano de sequência barato e espera aprovação antes de qualquer render final. Use quando o usuário pedir para editar, legendar, cortar, animar ou montar overlays de um vídeo de video/inputs.
---

# Edição de vídeo (editar-video)

Esta skill edita um vídeo de `video/inputs/` com base nele e nas observações do usuário. Antes de preparar o plano, leia [comportamentos-padrao.md](comportamentos-padrao.md) e o documento do modo solicitado em [`padroes-de-edicao/`](padroes-de-edicao/), quando houver: toda edição inclui legenda `legenda-evals` e corte de espaço morto rente à fala, independentemente da categoria; o modo pode ativar opcionais e definir overlays adicionais. Sem modo, `perfil-pb` e `aviso-2x` permanecem desligados, salvo pedido explícito. A implementação técnica dos padrões e dos demais pedidos fica com o roteador `.agents/skills/hyperframes/SKILL.md` e com as skills que ele aponta.

## Referências e assets permanentes

Os padrões reutilizáveis moram nesta skill: [comportamentos-padrao.md](comportamentos-padrao.md), [video-patterns.md](video-patterns.md) e `assets/` (prints e fontes Instrument Serif e Poppins, com licenças). Consulte o catálogo antes de planejar os elementos visuais. No modo `Lista com gancho`, o pré-plano textual vem primeiro: siga o caminho rápido descrito no modo e adie a leitura dos catálogos, de `design/identity.md` e das skills do HyperFrames até a aprovação dos textos. Não dependa de composições, scripts ou assets de vídeos anteriores em `video/` ou `videos/` para reproduzir os padrões. Essas pastas guardam entradas e arquivos de trabalho das peças; somente o material e o projeto da edição em curso precisam ser lidos. A execução técnica continua delegada às skills do HyperFrames.

## Entradas

- **Vídeo:** caminho dentro de `video/inputs/`. Se o caminho não existir ou não estiver nessa pasta, pergunte antes de seguir. Exceção: o modo `Lista com gancho` não usa vídeo de `video/inputs/`; sua entrada é uma lista (ideia do Notion ou descrita na chamada) e o vídeo de abertura vem de `video/hooks/`.
- **Modo:** se o usuário nomear um modo (ex.: `Notícias`), leia seu arquivo em `padroes-de-edicao/` antes de planejar. Os arquivos usam slug minúsculo sem acentos e com hífens entre palavras: `Notícias` corresponde a `noticias.md` e `Lista com gancho`, a `lista-com-gancho.md`. Se a intenção corresponder claramente a um modo, aplique-o; se houver ambiguidade que altere overlays ou outras decisões, pergunte antes de planejar. Registre o modo no plano. Não combine modos sem solicitação.
- **Observações:** tudo que o usuário disser sobre a edição. Registre-as literalmente no plano, na seção "Pedido do usuário".

## Regra central: plano antes de render

Nenhum render final acontece sem plano aprovado. Este é o comportamento padrão da skill, não uma opção.

Fluxo:

1. **Plano.** Gerar `plano.md` e a prévia barata (seção abaixo). Apresentar no chat, com os caminhos das imagens.
2. **Espera.** Parar e aguardar. Não renderizar o vídeo completo, não criar mais composições além do necessário para o plano.
3. **Ajuste.** Quando o usuário pedir mudanças, alterar apenas o que foi citado, atualizar `plano.md` com o histórico curto de versões (`v2`, `v3`) e apresentar o plano de novo.
4. **Pronto.** Só quando o usuário disser "pronto" (ou equivalente claro, como "pode renderizar") a skill faz o render final. Antes disso, a versão apresentada é só um plano.

Se o usuário pedir uma prévia do vídeo em movimento, isso é uma decisão dele. Atenda com um trecho curto, não com o vídeo inteiro.

## Plano de sequência

O plano precisa ser barato de gerar para que a iteração seja rápida. Por isso ele usa frames e texto, não renderização completa.

### O que entra no plano

Criar a pasta `video/projects/<slug>/` com:

- `plano.md`: documento de controle, com as seções abaixo.
- `plano/`: capturas (PNG pequeno) que o `plano.md` referencia.

Estrutura do `plano.md`:

```markdown
---
slug: <slug>
entrada: video/inputs/<arquivo>
versao: v1
status: rascunho | aprovado
duracao_original: <segundos>
duracao_prevista: <segundos>
---

## Pedido do usuário
(observações literais, sem reinterpretação)

## Comportamentos padrão
- Legenda: legenda-evals em toda a fala, com destaque da palavra pronunciada; amostra em plano/legenda.png.
- Espaço morto: cortes rentes à fala, sem truncar palavras; registrar abaixo intervalos mantidos/removidos na origem, posição editada e tempo removido.
- Modo: nenhum | <modo ativo>
- Opcionais: perfil-pb desligado; aviso-2x desligado. Ativar conforme o modo documentado ou pedido explícito para este vídeo; registrar cada estado. Para aviso-2x, incluir trecho e posição.
- Exceções: (somente as explicitamente pedidas pelo usuário ou comportamentos sem aplicação no material)

## Decisões e intenção
(uma linha por decisão: o que muda e por quê)

## Cortes propostos
- Exemplo: remover 00:00.0–00:03.2 da origem (3,2 s). A fala que começa em 00:03.2 passa a começar em 00:00.0 da edição.
- (listar todos os intervalos mantidos/removidos e seu mapeamento para a edição)

## Linha do tempo (tempos da edição)
| # | Início | Fim | Tipo | Conteúdo | Captura | Motivo |
|---|--------|-----|------|----------|---------|--------|
| 1 | 00:00.0 | 00:06.6 | legenda | legenda-evals sobre a fala | plano/legenda.png | comportamento padrão |
| 2 | 00:06.6 | 00:08.8 | overlay | imagem da notícia, se solicitada | plano/02.png | pedido do usuário |

## Pendências e dúvidas
(o que a skill não conseguiu decidir sozinha)

## Histórico
- v1: ...
```

### Como gerar barato

1. **Transcrição e silêncios.** No modo `Lista com gancho`, pule esta etapa: o vídeo é visual, o áudio dos ganchos é ignorado e a música será adicionada pelo usuário no Instagram. Nos demais casos com fala, use a transcrição e a detecção de silêncio via `/media-use` (ou `ffmpeg silencedetect` como alternativa). Use os resultados para propor cortes e confira o áudio nas bordas, conforme [comportamentos-padrao.md](comportamentos-padrao.md); não é necessário abrir o vídeo quadro a quadro. Recalcule os timestamps das legendas para a timeline editada.
2. **Capturas, não render.** Extraia um frame por trecho visual relevante com `ffmpeg`, no instante em que a intenção aparece, em resolução reduzida (por exemplo, largura 540). Mostre uma amostra estática de `legenda-evals` sobre o vídeo. Não gere uma captura para cada corte de silêncio ou grupo de legenda: registre os cortes em lista compacta e reutilize a amostra.
3. **Animações e overlays em still.** Para elementos gerados pelo HyperFrames, use a captura de frame do próprio CLI (`npx hyperframes snapshot`, conforme `/hyperframes-cli`) no instante-chave de cada elemento. Não renderize o MP4 para isso.
4. **Não recalcular o que não mudou.** Na versão seguinte, regenere só as capturas das linhas alteradas.

### Critério de custo

Se gerar o plano demorar mais que alguns minutos ou exigir render completo, a estrutura está errada. Reduza a resolução das capturas, use menos frames por trecho ou pule o snapshot de elementos que ainda não mudaram.

## Como executar a edição depois de aprovada

1. Ler `.agents/skills/hyperframes/SKILL.md` e seguir a tabela de estado. Este projeto já tem plano, então a entrada relevante é "edição de projeto existente" ou "criação com briefing", conforme o caso.
2. Carregar as skills de domínio que a operação exigir (`/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-audio`, `/hyperframes-cli`, entre outras), conforme a tabela de skills de domínio do roteador.
3. Montar a composição em `video/projects/<slug>/`, seguindo a timeline aprovada linha por linha.
4. Validar com `npx hyperframes check` antes de qualquer render.
5. Renderizar em `video/outputs/` só após "pronto". Nome do arquivo: slug do vídeo, sem data.
6. Mudar `status` para `aprovado` no momento em que o usuário disser "pronto", e registrar a versão final no histórico.

## Limites desta versão

- Modos documentados ficam em [`padroes-de-edicao/`](padroes-de-edicao/). Atualmente há `noticias.md` e `lista-com-gancho.md`; nenhum outro modo é presumido.
- Os únicos comportamentos automáticos universais são os de [comportamentos-padrao.md](comportamentos-padrao.md): legenda `legenda-evals` e corte de espaço morto rente à fala. `perfil-pb` e `aviso-2x` ficam desligados fora dos modos que os ativam ou de pedido explícito. Símbolos da marca e outras intervenções dependem de solicitação ou de regra explícita de modo.
- Não editar o roteador `hyperframes` nem as skills que ele aponta.
