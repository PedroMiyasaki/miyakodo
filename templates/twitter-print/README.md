# Thread Cards Template

HTML template for generating thread cards with an X/Threads-like look for Instagram carousel posts. It no longer mimics the Twitter/X interface: it uses a profile picture, a description, free text and optional images.

## How to use

### 1. Start the local server

**Windows:**
```bash
# Double-click:
start-server.bat

# Or run in the terminal, from the project root:
python -m http.server 8000
```

### 2. Open the template

Open in the browser: **http://localhost:8000/templates/twitter-print/**

⚠️ **IMPORTANT:**
- Use **Chrome** or **Edge** (Firefox and Safari do not support the folder picker API)
- Do not open the HTML file directly (file://) - always use the local server
- The "Export PNG" button needs the server running to work

### 3. Use the template

1. Edit the name, the description and the text directly on the card
2. Optionally, click **Add images**
3. Type a **codename** (post name)
4. Click **Export PNG**
5. Select the destination folder
6. The PNG will be saved to: `selected-folder/codename/timestamp.png`

## Troubleshooting

### "This browser does not support folder selection"
→ Use Chrome or Edge

### "This page must be served over HTTPS or localhost"
→ You opened the file directly. Use `start-server.bat`

### "You cancelled the selection"
→ You cancelled the folder picker. Click Export PNG again.
