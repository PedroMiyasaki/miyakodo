"""Composição HyperFrames standalone, 1080×1920."""

import json
from html import escape

from pipeline.avatar import avatar_svg
from pipeline.brand import (
    AZUL,
    BROWN,
    CINZA,
    LARANJA,
    MUTED,
    OFFWHITE,
    PAPER,
    SFX_FILES,
    VERDE,
)


def render_html(model: dict) -> str:
    duration = f'{model["duration"]:.3f}'
    mode = model["mode"]
    groups_html = _captions(model)
    videos_html = _videos(model)
    stage = _stage(model)
    avatar = ""
    if mode == "sem-gravacao":
        avatar = (
            f'<div id="avatar" class="clip" data-start="0" data-duration="{duration}" '
            f'data-track-index="6">{avatar_svg()}</div>'
        )
    audio = _audio(model, duration)
    payload = {
        "mode": mode,
        "ops": model["ops"],
        "groups": [
            {
                "id": group["id"],
                "words": [
                    {"id": word["id"], "start": word["start"], "end": word["end"], "role": word["role"]}
                    for word in group["words"]
                ],
            }
            for group in model["groups"]
        ],
        "avatar": model.get("avatar"),
        "mouth": model.get("mouth") or [],
        "mouthHz": model.get("mouth_hz") or 40,
        "videos": model.get("videos") or [],
    }
    data = json.dumps(payload, ensure_ascii=False)
    title = escape(model["title"])
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <script src="assets/gsap.min.js"></script>
  <style>
    {_css()}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{duration}" data-fps="{model["fps"]}">
    <div id="bg" class="clip" data-start="0" data-duration="{duration}" data-track-index="0"></div>
    {videos_html}
    {stage}
    {avatar}
    {groups_html}
    {audio}
  </div>
  <script>
    const PROJECT = {data};
    function apply(tl, op) {{
      if (op.kind === "to") tl.to(op.sel, op.vars, op.at);
      else if (op.kind === "fromTo") tl.fromTo(op.sel, op.from, op.to, op.at);
      else if (op.kind === "set") tl.set(op.sel, op.vars, op.at);
    }}
    function build() {{
      const tl = gsap.timeline({{ paused: true }});
      PROJECT.ops.forEach((op) => apply(tl, op));
      const ink = "{BROWN}";
      PROJECT.groups.forEach((group) => {{
        group.words.forEach((word) => {{
          const sel = "#" + word.id;
          if (PROJECT.mode === "sem-gravacao") {{
            tl.to(sel, {{
              color: ink, scale: 1.08, duration: 0.08, ease: "power2.out", transformOrigin: "50% 60%",
              boxShadow: "0 0 0 3px {BROWN}", borderRadius: "14px"
            }}, word.start);
            tl.to(sel, {{ scale: 1, boxShadow: "0 0 0 0px {BROWN}", duration: 0.07, ease: "power2.out" }}, word.end);
          }} else {{
            tl.to(sel, {{ opacity: 1, duration: 0.05 }}, word.start);
          }}
        }});
      }});
      const avatar = PROJECT.avatar;
      if (avatar) {{
        tl.to("#av-rig", {{
          y: 7, rotation: 1.6, duration: 0.48, yoyo: true, repeat: avatar.bob_repeats,
          ease: "sine.inOut", transformOrigin: "50% 80%"
        }}, 0);
        avatar.blinks.forEach((at) => {{
          tl.to("#av-lid-l", {{ opacity: 1, duration: 0.06, yoyo: true, repeat: 1, ease: "power1.inOut" }}, at);
          tl.to("#av-lid-r", {{ opacity: 1, duration: 0.06, yoyo: true, repeat: 1, ease: "power1.inOut" }}, at);
        }});
        avatar.lifts.forEach((at) => {{
          tl.to("#av-brows", {{ y: -7, duration: 0.16, yoyo: true, repeat: 1, ease: "power2.out" }}, at);
        }});
        avatar.moves.forEach((move, index) => {{
          const vars = {{ x: move.x, y: move.y, scale: move.scale, duration: index ? move.duration : 0.01, ease: "power3.out", transformOrigin: "50% 80%" }};
          tl.to("#avatar", vars, move.at);
        }});
        const hz = PROJECT.mouthHz || 40;
        PROJECT.mouth.forEach((level, index) => {{
          const at = index / hz;
          tl.set("#av-mouth-open", {{ scaleY: 0.18 + level * 2.5, scaleX: 0.82 + level * 0.45 }}, at);
          tl.set("#av-mouth-closed", {{ opacity: Math.max(0, 1 - level * 3.4) }}, at);
        }});
      }}
      PROJECT.videos.forEach((video) => {{
        if (!video.punch) return;
        tl.fromTo("#punch-" + video.id, {{ scale: 1 }}, {{
          scale: 1.14, duration: Math.max(0.4, video.duration - 0.05), ease: "power1.inOut", transformOrigin: "50% 30%"
        }}, video.start);
      }});
      window.__timelines["main"] = tl;
      if (window.__hfForceTimelineRebind) window.__hfForceTimelineRebind();
    }}
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
    else build();
  </script>
</body>
</html>
"""


def _stage(model: dict) -> str:
    if model["mode"] != "sem-gravacao":
        return model["scenes_html"]
    panels = max(1, len(model["beats"]))
    height = panels * 1920
    duration = f'{model["duration"]:.3f}'
    return (
        f'<section id="stage" class="clip" data-start="0" data-duration="{duration}" data-track-index="2">'
        f'<div id="world" data-layout-allow-overflow="true" style="height:{height}px">{model["scenes_html"]}</div>'
        f'</section>'
    )


def _videos(model: dict) -> str:
    if model["mode"] != "gravacao":
        return ""
    blocks = []
    for video in model["videos"]:
        klass = "split" if video["layout"] == "split" else "full"
        blocks.append(
            f'<div class="host {klass}">'
            f'<div id="punch-{video["id"]}" class="punch">'
            f'<video id="{video["id"]}" class="clip" src="assets/footage.mp4" muted playsinline '
            f'data-start="{video["start"]}" data-duration="{video["duration"]}" '
            f'data-media-start="{video["media_start"]}" data-track-index="1"></video>'
            f'</div></div>'
        )
    return "".join(blocks)


def _captions(model: dict) -> str:
    mode = model["mode"]
    chunks = []
    for group in model["groups"]:
        top = _top(model, group["start"])
        words = []
        for word in group["words"]:
            role = word["role"]
            if mode == "sem-gravacao":
                cls = "word serif" if role in {"emphasis", "strong", "cta"} else "word"
            elif role == "cta":
                cls = "word pill cta"
            elif role == "strong":
                cls = "word pill"
            elif role == "emphasis":
                cls = "word key"
            else:
                cls = "word"
            words.append(
                f'<span id="{word["id"]}" class="{cls}" data-layout-allow-overlap="true">{escape(word["text"])}</span>'
            )
        box = ""
        dur = round(group["end"] - group["start"], 3)
        kind = "face" if mode == "sem-gravacao" else "grav"
        chunks.append(
            f'<div id="{group["id"]}" class="clip cap {kind}" data-start="{group["start"]}" '
            f'data-duration="{dur}" data-track-index="8" style="top:{top}px">'
            f'<div class="cap-line">{box}{"".join(words)}</div></div>'
        )
    return "".join(chunks)


def _top(model, start):
    if model["mode"] == "sem-gravacao":
        return 156
    beat = model["beats"][-1]
    for item in model["beats"]:
        if item["start"] - 0.05 <= start <= item["end"] + 0.05:
            beat = item
            break
    return {"split": 900, "motion": 188, "creator": 220}[beat["layout"]]


def _audio(model, duration: str) -> str:
    tags = [
        f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{duration}" data-track-index="10" data-volume="1"></audio>',
        f'<audio id="bed" src="assets/bed.wav" data-start="0" data-duration="{duration}" data-track-index="11" data-volume="0.075"></audio>',
    ]
    for index, event in enumerate(model["sfx"]):
        filename = SFX_FILES.get(event["name"])
        if not filename:
            continue
        tags.append(
            f'<audio id="sfx-{index}" src="assets/sfx/{filename}" data-start="{event["at"]}" '
            f'data-track-index="{12 + index}" data-volume="0.42"></audio>'
        )
    return "".join(tags)


def _css() -> str:
    return f"""
    @font-face {{ font-family: Poppins; src: url("assets/fonts/Poppins-Regular.ttf") format("truetype"); font-weight: 400; }}
    @font-face {{ font-family: Poppins; src: url("assets/fonts/Poppins-SemiBold.ttf") format("truetype"); font-weight: 600; }}
    @font-face {{ font-family: Poppins; src: url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight: 700; }}
    @font-face {{ font-family: Poppins; src: url("assets/fonts/Poppins-ExtraBold.ttf") format("truetype"); font-weight: 800; }}
    @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/InstrumentSerif-Regular.ttf") format("truetype"); font-weight: 400; font-style: normal; }}
    @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/InstrumentSerif-Italic.ttf") format("truetype"); font-weight: 400; font-style: italic; }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; background: {OFFWHITE}; }}
    #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {OFFWHITE}; font-family: Poppins, sans-serif; color: {BROWN}; }}
    .clip {{ position: absolute; }}
    #bg {{ inset: 0; z-index: 0; background-color: {OFFWHITE};
      background-image:
        radial-gradient(circle at 18% 12%, rgba(182,202,219,.45), transparent 28%),
        radial-gradient(circle at 80% 70%, rgba(211,156,167,.28), transparent 26%),
        linear-gradient({CINZA}33 1px, transparent 1px),
        linear-gradient(90deg, {CINZA}33 1px, transparent 1px);
      background-size: auto, auto, 72px 72px, 72px 72px; }}
    #stage {{ inset: 0; overflow: hidden; z-index: 2; }}
    #world {{ position: absolute; left: 0; top: 0; width: 100%; }}
    .beat {{ inset: 0; z-index: 4; }}
    .host {{ position: absolute; overflow: hidden; z-index: 2; }}
    .host.split {{ left: 0; right: 0; top: 52%; height: 48%; }}
    .host.full {{ inset: 0; }}
    .punch {{ position: absolute; inset: 0; }}
    .host video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    .host.split video {{ object-position: center 16%; }}
    .host.full video {{ object-position: center 24%; }}
    #avatar {{ left: 36px; top: 1460px; width: 280px; z-index: 6; height: auto; }}
    #av-lid-l, #av-lid-r, #av-mouth-open, #av-mouth-closed, #av-rig, #av-brows {{ transform-box: fill-box; }}
    .piece {{ position: absolute; }}
    .card {{ background: {PAPER}; border: 3px solid {BROWN}; border-radius: 28px; box-shadow: 0 24px 44px rgba(40,14,3,.16); padding: 28px 32px; overflow: hidden; }}
    .kicker {{ margin: 0 0 18px; font-family: "Instrument Serif", serif; font-size: 52px; line-height: 1; color: {BROWN}; }}
    .kicker.center {{ text-align: center; }}
    .tl-row {{ display: flex; align-items: center; gap: 18px; margin: 18px 0; font-size: 40px; font-weight: 600; }}
    .tl-num {{ width: 64px; height: 64px; border-radius: 50%; background: {VERDE}; color: {OFFWHITE}; display: grid; place-items: center; font-family: "Instrument Serif", serif; font-size: 34px; }}
    .chrome {{ display: flex; align-items: center; gap: 10px; margin: -8px 0 18px; }}
    .dot {{ width: 16px; height: 16px; border-radius: 50%; }}
    .chrome-title {{ font-weight: 700; font-size: 28px; }}
    .kind {{ margin-left: auto; color: {MUTED}; font-style: normal; font-size: 22px; }}
    .mock-line {{ font-size: 36px; font-weight: 600; padding: 14px 0; border-bottom: 2px solid {CINZA}; }}
    .mock-body {{ position: relative; min-height: 180px; }}
    .scan {{ position: absolute; left: 8px; right: 8px; height: 8px; background: {LARANJA}; border-radius: 8px; }}
    .scan.fat {{ height: 16px; }}
    .giant-wrap {{ position: relative; height: 68%; }}
    .giant {{ position: absolute; inset: 0; display: grid; place-items: center; font-family: "Instrument Serif", serif; font-size: 240px; line-height: .85; color: {BROWN}; opacity: 0; }}
    .hub {{ position: absolute; left: 28%; top: 36%; width: 44%; height: 28%; display: grid; place-items: center; background: {VERDE}; color: {OFFWHITE}; border-radius: 50%; font-family: "Instrument Serif", serif; font-size: 42px; text-align: center; padding: 12px; }}
    .orbit {{ position: absolute; min-width: 180px; padding: 16px 18px; background: {PAPER}; border: 3px solid {BROWN}; border-radius: 18px; font-weight: 700; font-size: 28px; text-align: center; }}
    .o0 {{ left: 4%; top: 6%; }} .o1 {{ right: 4%; top: 14%; }} .o2 {{ left: 6%; bottom: 10%; }}
    .o3 {{ right: 6%; bottom: 8%; }} .o4 {{ left: 34%; top: 0; }} .o5 {{ left: 30%; bottom: 0; }}
    .bubble {{ max-width: 86%; margin: 14px 0; padding: 16px 18px; border-radius: 22px; display: flex; flex-direction: column; gap: 4px; font-size: 30px; }}
    .bubble b {{ font-size: 18px; letter-spacing: .04em; text-transform: uppercase; }}
    .bubble.me {{ background: {VERDE}; color: {OFFWHITE}; margin-left: auto; }}
    .bubble.them {{ background: {AZUL}; color: {BROWN}; }}
    .code-body {{ font-family: Poppins, sans-serif; font-size: 30px; line-height: 1.45; }}
    .code-line {{ min-height: 1.45em; }}
    .code-body i {{ font-style: normal; opacity: 0; }}
    .kw {{ color: {VERDE}; font-weight: 700; }}
    .str {{ color: {LARANJA}; }}
    .phone {{ height: 100%; border: 3px solid {BROWN}; border-radius: 48px; background: {PAPER}; padding: 28px; box-shadow: 0 24px 44px rgba(40,14,3,.16); }}
    .profile {{ display: flex; gap: 16px; align-items: center; margin-bottom: 22px; }}
    .profile b {{ display: block; font-size: 32px; }}
    .profile span {{ color: {MUTED}; font-size: 24px; }}
    .logo {{ height: 72px; width: auto; }}
    .comment, .dm {{ margin-top: 16px; padding: 16px 18px; border-radius: 20px; display: flex; flex-direction: column; gap: 6px; font-size: 30px; }}
    .comment {{ background: {OFFWHITE}; border: 2px solid {CINZA}; }}
    .dm {{ background: {VERDE}; color: {OFFWHITE}; }}
    .comment b, .dm b {{ font-size: 16px; letter-spacing: .06em; text-transform: uppercase; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; height: 100%; }}
    .cell {{ background: {PAPER}; border: 3px solid {BROWN}; border-radius: 22px; display: grid; place-items: center; font-weight: 700; font-size: 30px; text-align: center; padding: 8px; }}
    .cell.ghost {{ opacity: 0; border: 0; }}
    .folder-root {{ font-family: "Instrument Serif", serif; font-size: 48px; margin-bottom: 8px; }}
    .folder-row {{ font-size: 32px; font-weight: 600; padding: 10px 0; border-bottom: 2px solid {CINZA}; }}
    .bullet {{ display: flex; gap: 14px; align-items: center; font-size: 36px; font-weight: 600; margin: 16px 0; }}
    .bullet i {{ width: 18px; height: 18px; border-radius: 50%; background: {LARANJA}; display: block; }}
    .quote {{ margin: 0; font-family: "Instrument Serif", serif; font-style: italic; font-size: 48px; line-height: 1.15; }}
    .by {{ margin: 16px 0 0; color: {MUTED}; font-size: 24px; }}
    .badge {{ display: inline-flex; align-items: center; justify-content: center; min-height: 96px; padding: 12px 28px; border-radius: 999px; color: {OFFWHITE}; font-weight: 800; font-size: 40px; text-align: center; }}
    .badge-wrap {{ display: flex; align-items: center; justify-content: center; }}
    .rail {{ position: absolute; left: 76px; top: 120px; width: 4px; background: {CINZA}; }}
    .rail-node {{ position: absolute; left: 46px; display: flex; align-items: center; gap: 18px; }}
    .rail-node span {{ width: 64px; height: 64px; border-radius: 50%; background: {BROWN}; color: {OFFWHITE}; display: grid; place-items: center; font-family: "Instrument Serif", serif; font-size: 32px; }}
    .rail-node b {{ font-size: 30px; font-weight: 600; }}
    .cap {{ left: 0; right: 0; z-index: 8; display: flex; justify-content: center; }}
    .cap-line {{ position: relative; display: inline-flex; flex-wrap: wrap; justify-content: center; max-width: 960px; }}
    .cap.grav .cap-line {{ background: {OFFWHITE}; border: 3px solid {BROWN}; border-radius: 18px; padding: 10px 16px; }}
    .cap-box {{ position: absolute; border: 3px solid {BROWN}; border-radius: 16px; }}
    .cap.face .word {{ color: {MUTED}; }}
    .cap.grav .word {{ opacity: 0; }}
    .word {{ display: inline-block; margin: 0 8px; font-weight: 600; font-size: 54px; line-height: 1.15; color: {BROWN}; }}
    .serif {{ font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; font-size: 62px; }}
    .cap.grav .word {{ font-weight: 800; font-size: 50px; }}
    .word.key {{ color: {VERDE}; }}
    .word.pill {{ background: {BROWN}; color: {OFFWHITE}; border-radius: 999px; padding: 6px 16px; }}
    .word.pill.cta {{ background: {LARANJA}; }}
    """
