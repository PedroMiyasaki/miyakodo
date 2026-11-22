import html
import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DURATION = 154.183333
RATE = 1.1
DURATION = SOURCE_DURATION / RATE
NEWS_START, NEWS_END = 59.35 / RATE, 68.0 / RATE


def main():
    words = json.loads((ROOT / "transcript-raw.json").read_text(encoding="utf-8"))["words"]
    for w in words:
        w["text"] = re.sub(r"\bAI\b", "IA", w["text"])
        if w["text"] in ("23,", "24,"):
            w["text"] = "20" + w["text"]

    # Whisper sometimes gives consecutive words the same timestamp.
    i = 0
    while i < len(words):
        if words[i]["end"] > words[i]["start"]:
            i += 1
            continue
        j = i
        while j < len(words) and words[j]["end"] == words[j]["start"]:
            j += 1
        stop = min(j + 1, len(words))
        cluster = words[i:stop]
        end = cluster[-1]["end"]
        start = max(words[i - 1]["end"] if i else 0, min(cluster[0]["start"], end - 0.06 * len(cluster)))
        weights = [max(2, len(w["text"].strip(".,?!"))) for w in cluster]
        unit = (end - start) / sum(weights)
        cursor = start
        for w, weight in zip(cluster, weights):
            w["start"], w["end"] = round(cursor, 4), round(cursor + weight * unit, 4)
            cursor = w["end"]
        i = stop

    for i, w in enumerate(words):
        assert 0 <= w["start"] < w["end"] <= SOURCE_DURATION
        if i:
            assert w["start"] >= words[i - 1]["end"] - 0.001

    group = runpy.run_path(str(ROOT.parent / "top-5-licoes-desenvolvendo-ia-para-grandes-empresas/build_composition.py"))["group"]
    cues = group(words)
    for i, cue in enumerate(cues):
        next_start = cues[i + 1]["start"] if i + 1 < len(cues) else SOURCE_DURATION
        cue["end"] = round(min(cue["end"] + 0.12, next_start, SOURCE_DURATION), 4)
        assert cue["end"] > cue["start"]
        assert len(" ".join(w["text"] for w in cue["words"])) <= 36
        assert cue["end"] - cue["start"] <= 2.82
    for cue in cues:
        cue["start"] /= RATE
        cue["end"] /= RATE
        for w in cue["words"]:
            w["start"] /= RATE
            w["end"] /= RATE
    for w in words:
        w["start"] /= RATE
        w["end"] /= RATE
    (ROOT / "transcript.json").write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "captions.json").write_text(json.dumps(cues, ensure_ascii=False, indent=2), encoding="utf-8")

    font = '@font-face {font-family: Inter; src: url("fonts/inter-latin-wght-normal.woff2") format("woff2"); font-weight: 100 900; font-style: normal;}'
    base = font + '\n#root {position: absolute; inset: 0; width: 100%; height: 100%; font-family: Inter, sans-serif; pointer-events: none;} * {box-sizing: border-box;}'

    def scene(name, duration, css, body, js=""):
        path = ROOT / "compositions" / (name + ".html")
        path.parent.mkdir(exist_ok=True)
        path.write_text(f'''<template>
<style>{base}\n{css}</style>
<div id="root" data-composition-id="{name}" data-width="1080" data-height="1920" data-duration="{duration}">{body}</div>
<script>const tl = gsap.timeline({{paused: true}});\n{js}\nwindow.__timelines["{name}"] = tl;</script>
</template>\n''', encoding="utf-8")

    boxes, highlights = [], []
    for i, cue in enumerate(cues):
        highlights.append(f'tl.set("#caption-visual-{i}", {{opacity: 1}}, {cue["start"]});')
        highlights.append(f'tl.set("#caption-visual-{i}", {{opacity: 0}}, {cue["end"]});')
        spans = []
        for j, w in enumerate(cue["words"]):
            word_id = f"caption-{i}-word-{j}"
            spans.append(f'<span id="{word_id}" class="caption-word">{html.escape(w["text"])}</span>')
            highlights.append(f'tl.set("#{word_id}", {{color: "#0A0A0A", backgroundColor: "#FFFFFF"}}, {w["start"]});')
            highlights.append(f'tl.set("#{word_id}", {{color: "#FFFFFF", backgroundColor: "transparent"}}, {w["end"]});')
        boxes.append(f'<div id="caption-{i}" class="clip caption-clip" data-start="{cue["start"]}" data-duration="{round(cue["end"]-cue["start"],4)}" data-track-index="0" data-layout-allow-caption-zone><div id="caption-visual-{i}" class="caption-box">{" ".join(spans)}</div></div>')
    scene("captions", DURATION, '''
.caption-clip {position: absolute; inset: 0;}
.caption-box {position: absolute; inset: auto 72px 238px; margin: 0 auto; width: max-content; max-width: 936px; padding: 18px 24px 15px; background: #0A0A0A; color: #FFFFFF; border: 4px solid #FFFFFF; box-shadow: 9px 9px 0 rgba(10,10,10,.8); font-size: 48px; font-weight: 650; letter-spacing: -.025em; line-height: 1.12; text-align: center; text-wrap: balance; opacity: 0;}
.caption-word {display: inline; padding: 1px 2px 0; box-decoration-break: clone; -webkit-box-decoration-break: clone;}
''', "\n".join(boxes), "\n".join(highlights))
    scene("profile", DURATION, '''
#profile-label {position: absolute; top: 56px; left: 48px; width: max-content; padding: 10px 14px 8px; background: #0A0A0A; color: #FFFFFF; border: 3px solid #FFFFFF; font-size: 22px; font-weight: 740; letter-spacing: .02em; line-height: 1;}
''', '<div id="profile-label">@pedro.miyasaki.ia</div>')
    scene("speed-hint", 3.4 / RATE, '''
#speed-hint-inner {position: absolute; top: 1704px; left: 112px; padding: 9px 12px 7px; background: #0A0A0A; color: #FFFFFF; border: 4px solid #FFFFFF; box-shadow: 6px 6px 0 rgba(10,10,10,.8); font-size: 20px; font-weight: 800; letter-spacing: .08em; line-height: 1; white-space: nowrap; transform-origin: 0% 70%;}
''', '<div id="speed-hint-inner">SEGURE PARA 2X</div>', f'''
tl.fromTo("#speed-hint-inner", {{opacity: 0, scale: .86, y: 12}}, {{opacity: 1, scale: 1, y: 0, duration: {0.34 / RATE}, ease: "power3.out"}}, {0.12 / RATE});
tl.to("#speed-hint-inner", {{opacity: 0, duration: {0.22 / RATE}, ease: "power1.in"}}, {3.05 / RATE});
''')
    scene("openai-source", NEWS_END - NEWS_START, '''
#openai-card {position: absolute; top: 1360px; left: 72px; width: 936px; padding: 8px; border: 4px solid #FFFFFF; background: #0A0A0A; color: #FFFFFF;}
#openai-print {display: block; width: 100%; height: auto;}
#openai-credit {margin: 10px 4px 0; font-size: 22px; font-weight: 650; line-height: 1.2;}
''', '<div id="openai-card"><img id="openai-print" src="assets/openai-custom-gpts.jpg" alt="Aviso oficial: Custom GPTs in ChatGPT Enterprise are being retired"><p id="openai-credit">Fonte: OpenAI · learn.chatgpt.com · ChatGPT Enterprise</p></div>')

    def host(name, start, duration, track, kind, z):
        return f'<div id="{name}-host" class="clip" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{start}" data-duration="{duration}" data-track-index="{track}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index: {z}"></div>'

    (ROOT / "index.html").write_text(f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<title>Hype de IA</title><script src="vendor/gsap.min.js"></script>
<style>html, body {{margin: 0; width: 100%; height: 100%; overflow: hidden;}} #root {{position: relative; width: 100%; height: 100%; overflow: hidden;}} .clip {{position: absolute; inset: 0;}} #a-roll {{width: 100%; height: 100%; object-fit: contain;}}</style>
</head><body>
<div id="root" data-composition-id="hype-ia" data-start="0" data-width="1080" data-height="1920" data-duration="{DURATION}">
<video id="a-roll" class="clip" src="assets/input-video.mp4" data-start="0" data-duration="{DURATION}" data-playback-rate="{RATE}" data-track-index="0" data-has-audio="true" playsinline></video>
{host("openai-source", NEWS_START, NEWS_END-NEWS_START, 1, "graphics", 10)}
{host("profile", 0, DURATION, 2, "graphics", 20)}
{host("speed-hint", 0.45 / RATE, 3.4 / RATE, 3, "graphics", 30)}
{host("captions", 0, DURATION, 4, "captions", 40)}
</div><script>window.__timelines["hype-ia"] = gsap.timeline({{paused: true}});</script>
</body></html>\n''', encoding="utf-8")
    overlay_html = (ROOT / "index.html").read_text(encoding="utf-8")
    overlay_html = re.sub(r'<video\b[^>]*></video>\n', '', overlay_html)
    overlay_html = overlay_html.replace('data-composition-id="hype-ia"', 'data-composition-id="hype-ia-overlays"').replace('window.__timelines["hype-ia"]', 'window.__timelines["hype-ia-overlays"]')
    (ROOT / "renders").mkdir(exist_ok=True)
    (ROOT / "renders" / "overlays.html").write_text(overlay_html, encoding="utf-8")
    print(f"Built {len(cues)} caption groups, {len(words)} words; news {NEWS_START}-{NEWS_END}s")


if __name__ == "__main__":
    main()
