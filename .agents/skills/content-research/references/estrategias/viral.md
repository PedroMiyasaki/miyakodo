# Viral

ID: `viral`. Nome nas notas: Viral. Teto: 4.

Você procura conteúdo de IA e negócio que está circulando agora, e guarda por que circulou. A ideia não é repetir o vídeo. É o mecanismo que viajou e a pergunta que ele abre para o dono de uma empresa média no Brasil. Leia a lente e o contrato. Não percorra `sources.md`. Essa lista não limita a busca.

Busca aberta, em português e em inglês. Criador em inglês serve como matéria-prima. A peça da Miyakodo sai em português, sem copiar o gancho.

Não faça login. Não curta, não comente, não siga, não salve, não reposte e não abra mensagem privada. Página que pede conta é lacuna: registre e siga nas páginas abertas. Não peça navegador logado ao orquestrador.

## Onde olhar, nesta ordem

A rodada das 6h roda nesta máquina. Busca de Instagram, LinkedIn e YouTube pela página de resultados não devolve data confiável aqui. Não comece por elas.

Rode o coletor. Ele não usa chave e não pede login. `--horas` é a janela da rodada. Na diária, 24.

```bash
python3 .agents/skills/content-research/scripts/fontes_virais.py --horas 24
```

O JSON traz uma lista por fonte. Fonte com `"ok": false` é lacuna: siga nas outras e copie o `erro` no resumo. Não invente o que ela teria trazido.

| Fonte | O que volta | Data | Engajamento | Segredo |
|---|---|---|---|---|
| Hacker News, API Algolia | História com pontos e comentários | `created_at` absoluto | pontos, já filtrados em 40 ou mais | não |
| YouTube, RSS do canal | Vídeo de Fireship, Y Combinator e a16z | `published` do feed | views e a mediana dos vídeos do mesmo feed | não |
| Product Hunt, feed Atom | Lançamento do dia | `published` | não tem voto | não |
| Google Trends Brasil | Termo do dia, só se o nome for de IA | a lista é a do dia, não a data de uma peça | tráfego aproximado | não |
| Reddit `.json` | Top do dia, se o site responder | `created_utc` | pontos e comentários | não |

Product Hunt sem voto não vira ideia sozinha. Trends sem uma peça datada também não. Reddit, quando responde 403, fica na lacuna e a rodada segue.

## O que não é fonte de descoberta aqui

Testado nesta máquina, sem chave:

- Instagram (perfil e tag) abre uma página sem data e sem o link de cada reel. Login seria obrigatório. Não use como busca.
- LinkedIn (busca `past-24h` e `site:linkedin.com/posts`) cai em 403 ou em tela de entrar. Não use a busca.
- X: a busca não devolve o post. `api.fxtwitter.com` só data um status quando o id já está na mão. Não varra o X.
- A página de resultados do YouTube vem sem lista de vídeos. O filtro `sp` não prova data.

A busca livre do YouTube, com data e views de qualquer canal, pede a YouTube Data API. A variável seria `YOUTUBE_API_KEY`. Ela destrava a busca por termo e por data, fora da lista fixa de canais. Não crie a chave e não peça o valor. Sem ela, fique no RSS.

Se outra fonte já trouxe uma URL dessas redes, leia assim:

- **Instagram.** Leia legenda e data. View de Reel pode não aparecer. Não invente. Sem data absoluta, descarte.
- **X.** Confirme a hora em `api.fxtwitter.com`. Separe o comentário da peça citada. Não misture as métricas. Se o endpoint falhar, descarte.
- **LinkedIn.** Post público de operador ou de empresa, com data absoluta. Anúncio da própria empresa não prova circulação. Os comentários dizem se a tese pegou.
- **YouTube.** Confira idade e views. Patrocinado e recomendação podem furar um filtro de busca. O RSS do canal não tem esse problema.

## Regra de data

Só entra timestamp absoluto: ISO do RSS ou da API, ou `created_utc`. A hora em que você abriu a página não conta.

Descarte rótulo relativo (`5h`, `21h`, `Nov 24` sem hora) quando a janela corta esse dia. Um dia inteiro dentro da janela pode usar a data do dia. Se a precisão não deixar decidir, descarte.

## Regra de engajamento

O número tem de vir do JSON ou do RSS, com o nome da medida.

- Hacker News: 40 pontos ou mais na janela. Registre também os comentários. Não chame isso de view.
- YouTube: views do RSS. Passe se as views forem pelo menos 100 mil, ou se passarem a mediana dos outros vídeos do mesmo canal no feed. A mediana é a base daquele canal. Sem esse número, o vídeo não é viral, é só um upload.
- Reddit, se a fonte respondeu: o post está no top do dia e tem data na janela. A pontuação é a daquele sub, não um ranking global.
- Product Hunt e Trends não têm essa prova. Não promovem candidato.

Views acumuladas, presença no Explorar e selo de popular não explicam esta janela. Sem a mediana do canal, não diga que foi acima da média. Não compare like, ponto e view entre redes.

## Como filtrar

O mecanismo tem de estar no texto que você abriu:

- a primeira frase segura o scroll (medo, status, número, crença invertida, chamada a quem tem empresa)
- a prova cabe numa tela (conta de custo, antes e depois, print de uma regra)
- a briga é clara para um dono (ferramenta contra governança, promessa contra operação)

O `por_que_entrou` descreve o mecanismo. As notas ficam com o fato e a pergunta para o dono, em uma a três frases.

Leia a página da `url`, não só o título do JSON. Legenda, descrição e capítulos bastam para explicar a ideia. Não afirme que assistiu se só leu texto. Thumbnail isolada não sustenta o candidato. Anúncio da própria empresa, demonstração de ferramenta sem aposta de negócio, isca de engajamento, fofoca e corrida de benchmark sem consequência para a operação saem, mesmo com número alto.

## Corte

Dois caminhos, os dois com data absoluta:

- publicado dentro da janela, com engajamento visível. Não precisa de curva de crescimento
- peça mais antiga com sinal datado de circulação dentro da janela (onda de repost, fio novo, comentários novos). Sem data nesse sinal, descarte

Peça antiga com contador alto, sem sinal datado, fica de fora.

## Quantas

Até 4. No máximo uma ideia por publicação. Se a mesma crença apareceu em três lugares, guarde uma e use a fonte com data e engajamento mais claros. Zero é resultado válido. Não complete com lançamento sem circulação.
