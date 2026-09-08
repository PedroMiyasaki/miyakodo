# Template de cards de thread

Template HTML para gerar cards de thread com cara de X/Threads para posts de carrossel no Instagram. Ele não imita mais a interface do Twitter/X: usa foto de perfil, descrição, texto livre e imagens opcionais.

## Como usar

### 1. Suba o servidor local

**Windows:**
```bash
# Clique duas vezes em:
start-server.bat

# Ou rode no terminal, a partir da raiz do projeto:
python -m http.server 8000
```

### 2. Abra o template

Abra no navegador: **http://localhost:8000/templates/twitter-print/**

⚠️ **IMPORTANTE:**
- Use **Chrome** ou **Edge** (Firefox e Safari não suportam a API de seleção de pasta)
- Não abra o arquivo HTML direto (file://) - use sempre o servidor local
- O botão "Export PNG" precisa do servidor rodando para funcionar

### 3. Use o template

1. Edite o nome, a descrição e o texto direto no card
2. Se quiser, clique em **Add images**
3. Digite um **codename** (nome do post)
4. Clique em **Export PNG**
5. Selecione a pasta de destino
6. O PNG vai ser salvo em: `pasta-escolhida/codename/timestamp.png`

## Resolução de problemas

### "This browser does not support folder selection"
→ Use Chrome ou Edge

### "This page must be served over HTTPS or localhost"
→ Você abriu o arquivo direto. Use o `start-server.bat`

### "You cancelled the selection"
→ Você cancelou o seletor de pasta. Clique em Export PNG de novo.
