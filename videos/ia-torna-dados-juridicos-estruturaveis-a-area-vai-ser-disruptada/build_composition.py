import json
from pathlib import Path

ROOT = Path(__file__).parent
CARDS = ROOT / "public" / "cards"
FPS = 30
DURATION = 161.35

def q(t):
    return round(t * FPS) / FPS

cards = [
    {
        "id": "card-01",
        "start": 0.40,
        "end": 8.90,
        "intent": "A aposta do gancho: a área jurídica",
        "kicker": "A aposta",
        "title": "Área jurídica",
        "detail": "",
    },
    {
        "id": "card-02",
        "start": 9.15,
        "end": 19.85,
        "intent": "O direito foi o patinho feio da TI",
        "kicker": "Por anos",
        "title": "Patinho feio da TI",
        "detail": "",
    },
    {
        "id": "card-03",
        "start": 20.10,
        "end": 29.90,
        "intent": "O paradigma do dado estruturado contra o dado solto",
        "kicker": "O paradigma",
        "title": "Estruturado ou solto",
        "detail": "",
    },
    {
        "id": "card-04",
        "start": 30.15,
        "end": 52.70,
        "intent": "O direito produzia dado que não cabia em tabela",
        "kicker": "O direito",
        "title": "Não cabia numa tabela",
        "detail": "Muito dado. Pouco use case.",
    },
    {
        "id": "card-05",
        "start": 52.95,
        "end": 67.75,
        "intent": "A IA passou a ler o processo",
        "kicker": "A virada",
        "title": "A IA lê o processo",
        "detail": "O arquivo virou analisável.",
    },
    {
        "id": "card-06",
        "start": 68.00,
        "end": 78.85,
        "intent": "Legaltech lá fora: Harvey, Legora, EvenUp",
        "kicker": "Lá fora",
        "title": "Harvey. Legora. EvenUp.",
        "detail": "O legaltech saiu do zero.",
    },
    {
        "id": "card-07",
        "start": 79.10,
        "end": 95.85,
        "intent": "Enter passou de um bilhão de dólares",
        "kicker": "No Brasil",
        "title": "Mais de 1 bilhão",
        "detail": "Enter, unicórnio este ano.",
    },
    {
        "id": "card-08",
        "start": 96.10,
        "end": 113.85,
        "intent": "Dois anos e meio de direito antes da tecnologia",
        "kicker": "Antes da tecnologia",
        "title": "Dois anos e meio",
        "detail": "De estágio em direito.",
    },
    {
        "id": "card-09",
        "start": 114.10,
        "end": 123.85,
        "intent": "A área era antiga e o processo era velho",
        "kicker": "O que muda",
        "title": "Processo velho",
        "detail": "Área antiga, até ontem.",
    },
    {
        "id": "card-10",
        "start": 124.10,
        "end": 145.75,
        "intent": "Escritórios grandes vão montar times de dados bem pagos",
        "kicker": "O que falta",
        "title": "Time de dados",
        "detail": "Grande. E bem pago.",
    },
    {
        "id": "card-11",
        "start": 146.00,
        "end": 161.35,
        "intent": "CTA: comentar DIREITO para receber o post",
        "kicker": "Substack",
        "title": "Comenta DIREITO",
        "detail": "Eu te mando o post.",
    },
]

storyboard = {
    "schemaVersion": 3,
    "composition": {
        "fps": FPS,
        "width": 1080,
        "height": 1920,
        "durationSeconds": DURATION,
        "layout": "portrait",
        "themeId": "mono",
        "seed": 4,
    },
    "videoTrack": {
        "sourcePath": "input-video.mp4",
        "startSec": 0,
        "endSec": DURATION,
        "bounds": {"x": 0, "y": 0, "width": 1080, "height": 1920},
    },
    "subtitles": {"enabled": False},
    "cards": [
        {
            "id": c["id"],
            "intent": c["intent"],
            "startSec": c["start"],
            "endSec": c["end"],
            "accentIndex": 0,
            "zone": "video-overlay",
            "contentHints": {
                "kicker": c["kicker"],
                "title": c["title"],
                "detail": c["detail"],
            },
        }
        for c in cards
    ],
}
(ROOT / "storyboard.json").write_text(
    json.dumps(storyboard, ensure_ascii=False, indent=2), encoding="utf-8"
)

def card_html(c):
    cid = c["id"]
    detail = ""
    if c["detail"]:
        detail = f"""
      <p class="detail" id="{cid}-detail" data-anim="fade-in" data-anim-at="0.55" data-anim-duration="0.35">{c["detail"]}</p>"""
    return f"""<div class="card" data-card-id="{cid}">
  <style>
    .card[data-card-id="{cid}"] .root {{
      width: 100%;
      height: 100%;
      position: relative;
      background: transparent;
    }}
    .card[data-card-id="{cid}"] .panel {{
      position: absolute;
      left: 48px;
      top: 1508px;
      width: 984px;
      height: 340px;
      box-sizing: border-box;
      background: #ffffff;
      color: #0a0a0a;
      padding: 36px 44px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
      font-family: "Inter", ui-sans-serif, system-ui, sans-serif;
    }}
    .card[data-card-id="{cid}"] .kicker {{
      font: 500 22px/1 "Inter", ui-sans-serif, system-ui, sans-serif;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #0a0a0a;
    }}
    .card[data-card-id="{cid}"] .title {{
      margin: 0;
      font: 700 64px/0.96 "Inter", ui-sans-serif, system-ui, sans-serif;
      letter-spacing: -0.03em;
      color: #0a0a0a;
    }}
    .card[data-card-id="{cid}"] .detail {{
      margin: 0;
      font: 400 32px/1.25 "Inter", ui-sans-serif, system-ui, sans-serif;
      color: #0a0a0a;
    }}
  </style>
  <div class="root">
    <div class="panel">
      <span class="kicker" id="{cid}-kicker" data-anim="fade-in" data-anim-at="0.08" data-anim-duration="0.3">{c["kicker"]}</span>
      <h1 class="title" id="{cid}-title" data-anim="slide-in" data-anim-at="0.16" data-anim-duration="0.4" data-anim-from="bottom" data-anim-distance="24">{c["title"]}</h1>{detail}
    </div>
  </div>
</div>
"""

CARDS.mkdir(parents=True, exist_ok=True)
for c in cards:
    (CARDS / f"{c['id']}.html").write_text(card_html(c), encoding="utf-8")

hosts = []
tweens = []
for c in cards:
    cid = c["id"]
    start = q(c["start"])
    end = q(c["end"])
    dur = q(end - start)
    body = (CARDS / f"{cid}.html").read_text(encoding="utf-8").strip()
    hosts.append(
        f"""      <div
        class="card-host clip"
        data-card-id="{cid}"
        data-start="{start:.4f}"
        data-duration="{dur:.4f}"
        data-track-index="2"
        style="left:0;top:0;width:1080px;height:1920px;visibility:hidden;opacity:0;z-index:3;"
      >
        {body}
      </div>"""
    )
    exit_at = q(end - 0.28)
    tweens.append(
        f"""
          tl.set('.card-host[data-card-id="{cid}"]', {{ visibility: "visible" }}, {start:.4f});
          tl.fromTo('.card-host[data-card-id="{cid}"]', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.28, ease: "power2.out" }}, {start:.4f});
          tl.fromTo('.card[data-card-id="{cid}"] #{cid}-kicker', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {q(start + 0.08):.4f});
          tl.fromTo('.card[data-card-id="{cid}"] #{cid}-title', {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {q(start + 0.16):.4f});"""
    )
    if c["detail"]:
        tweens.append(
            f"""
          tl.fromTo('.card[data-card-id="{cid}"] #{cid}-detail', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {q(start + 0.55):.4f});"""
        )
    tweens.append(
        f"""
          tl.to('.card-host[data-card-id="{cid}"]', {{ opacity: 0, duration: 0.28, ease: "power2.in" }}, {exit_at:.4f});
          tl.set('.card-host[data-card-id="{cid}"]', {{ visibility: "hidden" }}, {end:.4f});"""
    )

html = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <style>
      @font-face {{
        font-family: "Inter";
        src: url("fonts/Inter-400-latin.woff2") format("woff2");
        font-weight: 400;
        font-display: block;
      }}
      @font-face {{
        font-family: "Inter";
        src: url("fonts/Inter-700-latin.woff2") format("woff2");
        font-weight: 700;
        font-display: block;
      }}
      :root {{
        --bg: #ffffff;
        --text: #0a0a0a;
        --accent-0: #0a0a0a;
        --accent-1: #555555;
        --accent-2: #888888;
        --accent-3: #aaaaaa;
        --accent-4: #cccccc;
      }}
      * {{ box-sizing: border-box; }}
      html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #000;
        font-family: "Inter", ui-sans-serif, system-ui, sans-serif;
      }}
      #stage {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;
      }}
      .video-wrapper {{
        position: absolute;
        left: 0;
        top: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        z-index: 1;
      }}
      .video-wrapper video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
      }}
      .legibility {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 2;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 68%, rgba(0,0,0,.35) 100%);
      }}
      .card-host {{
        position: absolute;
        pointer-events: none;
        overflow: hidden;
      }}
      .card-host .card {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }}
    </style>
  </head>
  <body>
    <div
      id="stage"
      data-composition-id="talking-head-recut"
      data-start="0"
      data-duration="{DURATION}"
      data-fps="{FPS}"
      data-width="1080"
      data-height="1920"
    >
      <div class="video-wrapper" id="video-wrap">
        <video
          id="bg-video"
          src="input-video.mp4"
          playsinline
          data-has-audio="true"
          data-start="0"
          data-duration="{DURATION}"
          data-track-index="1"
        ></video>
      </div>
      <div class="legibility"></div>
{chr(10).join(hosts)}
      <script src="vendor/gsap.min.js"></script>
      <script>
        (function () {{
          const tl = window.gsap.timeline({{ paused: true }});
          {''.join(tweens)}
          window.__timelines = window.__timelines || {{}};
          window.__timelines["talking-head-recut"] = tl;
        }})();
      </script>
    </div>
  </body>
</html>
"""
(ROOT / "public" / "index.html").write_text(html, encoding="utf-8")
print("cards", len(cards))
