---
workflow: general-video
flow: automation
storyboard: no
message: "Quais aplicações de IA valem o investimento de uma empresa, na avaliação de Pedro."
destination: instagram-reel
aspect: 1080x1920
language: pt-BR
audience: empresários, stakeholders e responsáveis pelo orçamento de IA
length: aproximadamente 2 minutos e 42 segundos
---

## Intent

Editar a gravação de tier list. A esposa lê cada aplicação nas pausas antes de Pedro responder. O pedido já define footage, voz, tratamento das legendas, perfil e animação das notas. Execução direta, sem entrevista ou storyboard para aprovação.

## Assets

- `../../inputs/tier_list/tier_list.MP4`: gravação original, 186,95 s, 1440 × 2560, 60 fps, Dolby Vision/HLG. Cópia original adotada em `.media/`; derivação SDR para preview e exportação.
- `../../inputs/tier_list/edit/transcripts/tier_list.json`: transcrição existente por palavra.
- `../../inputs/tier_list/audios_esposa/`: cinco áudios originais com os nomes das categorias e suas transcrições.

## Customizations

- `perfil-pb`: identificação canônica, em minúsculas e fixa no canto superior esquerdo.
- `legenda-evals`: frases inteiras em caixa preta, borda branca, destaque branco por palavra. Legendar ambos os interlocutores.
- Os áudios da esposa terminam antes da resposta de Pedro, sem sobreposição de fala.
- Remover o silêncio de gravação dos áudios e apenas o excesso de espera entre os cinco blocos. Preservar toda a fala de Pedro. A montagem final inteira está em 1,1x, incluindo as duas vozes, as legendas e as animações.
- Tier list cumulativa nas notas: WhatsApp D, conteúdo C, reuniões C, RAG Enterprise B e especialistas S. A linha A permanece vazia. O item novo entra no instante em que Pedro pronuncia a letra da nota.
- Mostrar o quadro por poucos segundos nas cinco avaliações. O usuário antecipou o quadro de RAG e removeu a recapitulação pelo Studio; esses ajustes foram preservados. Deixar rosto e boca livres; não manter o quadro durante toda a peça.
- Manter o CTA gravado para comentar "especialista".

## Notes

Tipografia local Inter e Bricolage Grotesque, preto e branco. Movimentos de chegada e saída curtos, sem bounce. Sem música ou sons que concorram com a conversa. Loudness consistente entre as duas vozes; reduzir o ambiente da gravação durante as falas dela.

O original fica intacto. A conversão HLG para Rec.709/SDR segue o pipeline já usado em evals-reel; não é um novo look criativo. O usuário revisou a prévia e aprovou a exportação com uma única mudança: acelerar 10%.

Os HTMLs atuais são a fonte da edição final. `scripts/build.mjs` registra a montagem inicial e não deve ser reexecutado sobre os ajustes do Studio. `scripts/retime.mjs` aplicou a aceleração uma única vez, preservando o conteúdo e os pontos de corte da mídia.
