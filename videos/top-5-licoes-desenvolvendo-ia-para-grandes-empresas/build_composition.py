import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
FPS = 30
SOURCE_DURATION = 193.3167

# The second-lesson sentence was recorded after the examples.
# Move "A segunda é que ... mirabolantes aí." to just before
# "Eu percebo que tem muitas coisas".
# End the first block before he leans into the camera to start
# "Eu percebo". That lean begins around 35.83. Leaving it on the
# tail of this block made the approach flash for a fraction of a
# second, then the same approach played again after the insert.
A_END = 35.70
C_START = 75.64
C_END = 83.70
D_START = 84.02


def q(t):
    return round(t * FPS) / FPS


def qf(t):
    return int(t * FPS) / FPS


def main():
    words = json.loads((ROOT / "words.json").read_text(encoding="utf-8"))
    fixed = correct(words)
    (ROOT / "transcript.json").write_text(
        json.dumps(fixed, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    a_end, c_start, c_end, d_start = map(qf, (A_END, C_START, C_END, D_START))
    d_end = qf(SOURCE_DURATION)
    dur_a = a_end
    dur_c = c_end - c_start
    dur_b = c_start - a_end
    dur_d = d_end - d_start
    duration = q(dur_a + dur_c + dur_b + dur_d)
    b_at = q(dur_a + dur_c)
    d_at = q(dur_a + dur_c + dur_b)

    def place(t):
        t = float(t)
        if t < a_end:
            return t
        if c_start <= t < c_end:
            return dur_a + (t - c_start)
        if a_end <= t < c_start:
            return b_at + (t - a_end)
        if t >= d_start:
            return d_at + (t - d_start)
        return None

    placed = []
    for w in fixed:
        start = place(w["start"])
        end = place(min(w["end"], SOURCE_DURATION))
        if start is None or end is None or end <= start:
            continue
        placed.append({**w, "start": round(start, 4), "end": round(end, 4)})
    placed.sort(key=lambda w: (w["start"], w["end"]))

    cues = group(placed)
    news = news_window(placed)
    (PUBLIC / "index.html").write_text(
        render(duration, cues, news, a_end, c_start, dur_c, b_at, dur_b, d_at, d_start, dur_d),
        encoding="utf-8",
    )
    print(
        f"duration {duration:.4f} cues {len(cues)} "
        f"news {news['start']:.2f}-{news['end']:.2f} "
        f"moved {dur_a:.2f}s then {dur_c:.2f}s"
    )
    sample = " ".join(w["text"] for w in placed if 36 <= w["start"] < 48)
    print(sample)


def correct(words):
    fixed = []
    i = 0
    repl = {
        "cloud": "Claude",
        "coworking,": "Cowork,",
        "code,": "Code,",
        "milaborantes": "mirabolantes",
    }
    while i < len(words):
        w = dict(words[i])
        text = w["text"]
        if text == "chat" and i + 1 < len(words) and words[i + 1]["text"] == "EPT":
            w["text"] = "ChatGPT"
            w["end"] = words[i + 1]["end"]
            fixed.append(w)
            i += 2
            continue
        w["text"] = repl.get(text, text)
        if w["end"] <= w["start"]:
            w["end"] = w["start"] + 0.05
        fixed.append(w)
        i += 1
    return fixed


def group(words):
    raw = []
    cur = []
    for w in words:
        if not cur:
            cur = [w]
            continue
        proposal = cur + [w]
        text = " ".join(item["text"] for item in proposal)
        span = w["end"] - cur[0]["start"]
        boundary = cur[-1]["text"].endswith((".", "?", "!"))
        if boundary or len(proposal) > 6 or len(text) > 36 or span > 2.7:
            raw.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        raw.append(cur)

    merged = []
    for g in raw:
        if not merged:
            merged.append(g)
            continue
        prev = merged[-1]
        span = prev[-1]["end"] - prev[0]["start"]
        gap = g[0]["start"] - prev[-1]["end"]
        text = " ".join(item["text"] for item in prev + g)
        sentence = prev[-1]["text"].endswith((".", "?", "!"))
        if span < 0.45 and gap < 0.55 and not sentence and len(text) <= 36 and len(prev) + len(g) <= 6:
            prev.extend(g)
        else:
            merged.append(g)

    cues = []
    for i, g in enumerate(merged):
        start = g[0]["start"]
        end = g[-1]["end"]
        if i + 1 < len(merged):
            end = min(max(end, start + 0.35), merged[i + 1][0]["start"])
        end = max(end, start + 0.2)
        cues.append(
            {
                "start": round(start, 4),
                "end": round(end, 4),
                "words": [
                    {"text": w["text"], "start": round(w["start"], 4), "end": round(w["end"], 4)}
                    for w in g
                ],
            }
        )
    return cues


def news_window(words):
    start = None
    end = None
    for w in words:
        if start is None and w["text"] in {"estudo", "MIT"}:
            start = w["start"]
        if start is not None and "financeiro" in w["text"]:
            end = w["end"]
            break
    if start is None:
        start = 141.0
    if end is None:
        end = start + 6
    return {"start": q(max(0, start - 0.15)), "end": q(end + 1.4)}


def render(duration, cues, news, a_end, c_start, dur_c, b_at, dur_b, d_at, d_start, dur_d):
    cards = []
    for i, cue in enumerate(cues):
        spans = []
        for j, w in enumerate(cue["words"]):
            spans.append(
                f'<span id="cg-{i}-w-{j}" class="caption-word">{html.escape(w["text"])}</span>'
            )
        cards.append(
            "\n".join(
                [
                    f'        <div id="cg-{i}" class="caption-box clip" data-start="{cue["start"]}" data-duration="{round(cue["end"] - cue["start"], 4)}" data-track-index="3" data-layout-allow-caption-zone>',
                    "          " + " ".join(spans),
                    "        </div>",
                ]
            )
        )
    cue_json = json.dumps(cues, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <style>
      @font-face {{
        font-family: "Inter";
        src: url("fonts/inter-latin-wght-normal.woff2") format("woff2");
        font-style: normal;
        font-weight: 100 900;
        font-display: block;
      }}
      * {{ box-sizing: border-box; }}
      html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #000;
      }}
      #stage {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #000;
      }}
      video.clip {{
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
      }}
      .caption-track {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 8;
      }}
      .caption-box {{
        position: absolute;
        inset: auto 72px 238px;
        width: max-content;
        max-width: 936px;
        margin: 0 auto;
        padding: 18px 24px 15px;
        border: 4px solid #FFFFFF;
        background: #0A0A0A;
        box-shadow: 9px 9px 0 rgba(10, 10, 10, 0.8);
        color: #FFFFFF;
        font-family: "Inter", sans-serif;
        font-size: 48px;
        font-weight: 650;
        letter-spacing: -0.025em;
        line-height: 1.12;
        text-align: center;
        text-wrap: balance;
        visibility: hidden;
      }}
      .caption-word {{
        display: inline;
        padding: 1px 2px 0;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
      }}
      #news-card {{
        position: absolute;
        left: 72px;
        right: 72px;
        bottom: 470px;
        z-index: 6;
        visibility: hidden;
      }}
      #news-card img {{
        display: block;
        width: 100%;
        height: auto;
        background: #fff;
        border: 4px solid #0A0A0A;
      }}
      #speed-hint-inner {{
        position: absolute;
        top: 880px;
        right: 48px;
        z-index: 9;
        padding: 9px 12px 7px;
        border: 4px solid #FFFFFF;
        background: #0A0A0A;
        box-shadow: 6px 6px 0 rgba(10, 10, 10, 0.8);
        color: #FFFFFF;
        font-family: "Inter", sans-serif;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.08em;
        line-height: 1;
        text-transform: uppercase;
        white-space: nowrap;
        transform-origin: 100% 50%;
        opacity: 0;
      }}
      #persistent-handle {{
        position: absolute;
        inset: 0;
        z-index: 12;
        pointer-events: none;
      }}
      #persistent-handle-inner {{
        position: absolute;
        top: 66px;
        left: 54px;
        padding: 12px 15px 9px;
        border: 4px solid #FFFFFF;
        background: #0A0A0A;
        color: #FFFFFF;
        font-family: "Inter", sans-serif;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 0.08em;
        line-height: 1;
        text-transform: uppercase;
        opacity: 0;
      }}
    </style>
  </head>
  <body>
    <div
      id="stage"
      data-composition-id="talking-head-recut"
      data-start="0"
      data-duration="{duration}"
      data-fps="30"
      data-width="1080"
      data-height="1920"
    >
      <video id="seg-a" class="clip" src="input-video.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{a_end}" data-media-start="0" data-track-index="1"></video>
      <video id="seg-c" class="clip" src="input-video.mp4" playsinline data-has-audio="true" data-start="{a_end}" data-duration="{dur_c}" data-media-start="{c_start}" data-track-index="1"></video>
      <video id="seg-b" class="clip" src="input-video.mp4" playsinline data-has-audio="true" data-start="{b_at}" data-duration="{dur_b}" data-media-start="{a_end}" data-track-index="1"></video>
      <video id="seg-d" class="clip" src="input-video.mp4" playsinline data-has-audio="true" data-start="{d_at}" data-duration="{dur_d}" data-media-start="{d_start}" data-track-index="1"></video>

      <div id="news-card" class="clip" data-start="{news["start"]}" data-duration="{round(news["end"] - news["start"], 4)}" data-track-index="2">
        <img src="cards/fortune-mit.png" alt="Fortune: MIT report, 95 percent of generative AI pilots at companies are failing" />
      </div>

      <div id="speed-hint-inner">SEGURE PARA 2X</div>

      <div id="persistent-handle" data-layout-ignore>
        <div id="persistent-handle-inner">@pedro.miyasaki.ia</div>
      </div>

      <div class="caption-track" id="captions" data-start="0" data-duration="{duration}" data-track-index="3" data-track-kind="captions">
{chr(10).join(cards)}
      </div>

      <script src="vendor/gsap.min.js"></script>
      <script>
        (function () {{
          const tl = window.gsap.timeline({{ paused: true }});
          const cues = {cue_json};
          const q = function (t) {{ return Math.round(t * 30) / 30; }};

          cues.forEach(function (cue, i) {{
            var card = "#cg-" + i;
            tl.set(card, {{ visibility: "visible", opacity: 1 }}, q(cue.start));
            tl.set(card, {{ visibility: "hidden", opacity: 0 }}, q(cue.end));
            cue.words.forEach(function (word, j) {{
              var el = "#cg-" + i + "-w-" + j;
              tl.set(el, {{ color: "#0A0A0A", backgroundColor: "#FFFFFF" }}, q(word.start));
              tl.set(el, {{ color: "#FFFFFF", backgroundColor: "transparent" }}, q(word.end));
            }});
          }});

          tl.fromTo(
            "#persistent-handle-inner",
            {{ opacity: 0, y: -18 }},
            {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }},
            0.2
          );

          tl.fromTo(
            "#speed-hint-inner",
            {{ opacity: 0, y: 12 }},
            {{ opacity: 1, y: 0, duration: 0.34, ease: "power3.out" }},
            0.45
          );

          var newsIn = q({news["start"]});
          var newsOut = q({news["end"]} - 0.3);
          tl.set("#news-card", {{ visibility: "visible" }}, newsIn);
          tl.fromTo("#news-card", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, newsIn);
          tl.to("#news-card", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, newsOut);
          tl.set("#news-card", {{ visibility: "hidden" }}, q({news["end"]}));

          window.__timelines = window.__timelines || {{}};
          window.__timelines["talking-head-recut"] = tl;
        }})();
      </script>
    </div>
  </body>
</html>
"""


if __name__ == "__main__":
    main()
