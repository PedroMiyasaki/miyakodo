"""Rebuild the reel: captions, Instagram handle, company logos only."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DURATION = 161.35
WORDS = json.loads((ROOT / "transcript.json").read_text(encoding="utf-8"))


def q(t: float) -> float:
    return round(max(0.0, t) * 30) / 30


def groups(words):
    buf = []
    out = []
    for i, word in enumerate(words):
        buf.append(word)
        text = " ".join(item["text"] for item in buf)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["start"] - word["end"]) if nxt else 1
        sentence = word["text"].rstrip().endswith((".", "!", "?"))
        if sentence or len(buf) >= 6 or len(text) >= 34 or gap > 0.45 or nxt is None:
            out.append(buf)
            buf = []
    return out


def caption_html(chunks):
    boxes = []
    tweens = []
    for gi, chunk in enumerate(chunks):
        start = q(chunk[0]["start"])
        end = q(chunk[-1]["end"])
        if gi + 1 < len(chunks):
            end = min(end + 0.12, q(chunks[gi + 1][0]["start"]))
        end = max(end, q(start + 0.08))
        spans = []
        for wi, word in enumerate(chunk):
            wid = f"c{gi}w{wi}"
            spans.append(f'<span id="{wid}" class="caption-word">{html.escape(word["text"])}</span>')
            on = q(word["start"])
            if wi + 1 < len(chunk):
                off = q(chunk[wi + 1]["start"])
            else:
                off = q(word["end"])
            if off <= on:
                off = q(on + 1 / 30)
            tweens.append(
                f'tl.set("#{wid}", {{ color: "#0A0A0A", backgroundColor: "#FFFFFF" }}, {on:.4f});'
            )
            tweens.append(
                f'tl.set("#{wid}", {{ color: "#FFFFFF", backgroundColor: "transparent" }}, {off:.4f});'
            )
        boxes.append(
            f'<div id="cap-{gi}" class="clip caption-box" data-start="{start:.4f}" '
            f'data-duration="{end - start:.4f}" data-track-index="4" data-layout-allow-caption-zone>'
            f'<div class="caption-inner">{" ".join(spans)}</div></div>'
        )
    return "\n".join(boxes), "\n".join(tweens)


CAPS, TWEENS = caption_html(groups(WORDS))

INDEX = f"""<!doctype html>
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
      * {{ box-sizing: border-box; }}
      html, body {{
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;
      }}
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;
        font-family: "Inter", sans-serif;
      }}
      #bg-video {{
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
        z-index: 1;
      }}
      #handle {{
        position: absolute;
        top: 64px;
        left: 64px;
        z-index: 8;
        margin: 0;
        padding: 12px 16px 10px;
        background: #0A0A0A;
        color: #FFFFFF;
        font-family: "Inter", sans-serif;
        font-weight: 700;
        font-size: 22px;
        letter-spacing: 0.04em;
        line-height: 1;
      }}
      .logo-plate {{
        position: absolute;
        left: 72px;
        top: 168px;
        width: 936px;
        height: 200px;
        z-index: 5;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 28px;
        padding: 28px 32px;
        background: #FFFFFF;
        border: 4px solid #0A0A0A;
        box-shadow: 9px 9px 0 rgba(10, 10, 10, 0.8);
        visibility: hidden;
        opacity: 0;
      }}
      .logo-plate img {{
        height: 64px;
        width: auto;
        max-width: 270px;
        object-fit: contain;
      }}
      #logos-enter img {{
        height: 78px;
        max-width: 520px;
      }}
      .caption-box {{
        position: absolute;
        left: 72px;
        right: 72px;
        bottom: 238px;
        z-index: 6;
        display: flex;
        justify-content: center;
        pointer-events: none;
      }}
      .caption-inner {{
        width: max-content;
        max-width: 936px;
        padding: 18px 24px 15px;
        border: 4px solid #FFFFFF;
        background: #0A0A0A;
        box-shadow: 9px 9px 0 rgba(10, 10, 10, 0.8);
        color: #FFFFFF;
        font-family: "Inter", sans-serif;
        font-size: 48px;
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.12;
        text-align: center;
        text-wrap: balance;
      }}
      .caption-word {{
        display: inline;
        padding: 1px 2px 0;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="talking-head-recut"
      data-start="0"
      data-duration="{DURATION}"
      data-fps="30"
      data-width="1080"
      data-height="1920"
    >
      <video
        id="bg-video"
        src="input-video.mp4"
        playsinline
        data-has-audio="true"
        data-start="0"
        data-duration="{DURATION}"
        data-track-index="1"
      ></video>

      <div id="handle">@pedro.miyasaki.ia</div>

      <div
        id="logos-foreign"
        class="clip logo-plate"
        data-start="76.4333"
        data-duration="3.6000"
        data-track-index="5"
      >
        <img src="logos/harvey.svg" alt="Harvey" />
        <img src="logos/legora.svg" alt="Legora" />
        <img src="logos/evenup.svg" alt="EvenUp" />
      </div>

      <div
        id="logos-enter"
        class="clip logo-plate"
        data-start="85.6333"
        data-duration="4.5667"
        data-track-index="5"
      >
        <img src="logos/enter.svg" alt="Enter" />
      </div>

      {CAPS}

      <script src="vendor/gsap.min.js"></script>
      <script>
        const tl = gsap.timeline({{ paused: true }});
        function show(id, start, end) {{
          tl.set(id, {{ visibility: "visible" }}, start);
          tl.fromTo(id, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "power2.out" }}, start);
          tl.to(id, {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, end - 0.2);
          tl.set(id, {{ visibility: "hidden" }}, end);
        }}
        show("#logos-foreign", 76.4333, 80.0333);
        show("#logos-enter", 85.6333, 90.2000);
        {TWEENS}
        window.__timelines = window.__timelines || {{}};
        window.__timelines["talking-head-recut"] = tl;
      </script>
    </div>
  </body>
</html>
"""

(ROOT / "public" / "index.html").write_text(INDEX, encoding="utf-8")
print("groups", len(groups(WORDS)), "bytes", (ROOT / "public" / "index.html").stat().st_size)
