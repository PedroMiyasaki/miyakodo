# Origem

Código trazido de [paulmil11/manychat-lite-cloudflare](https://github.com/paulmil11/manychat-lite-cloudflare), commit `1217423462d692470c063204a60bd838f90c9d31`, licença MIT (`LICENSE`). O `README.md` original foi mantido, com um aviso no topo.

O que este repositório acrescenta:

- regras por post, lidas de `posts/**/respostas-comentarios.md` (`scripts/build-respostas.mjs`)
- correspondência estrita: o comentário é só a palavra-chave daquele post
- direct com botão, checagem de seguidor e entrega do material só depois
- polling opcional de comentários, desligado por padrão

O guia de uso é a skill `.agents/skills/deploy-instagram-autodm/SKILL.md`.
