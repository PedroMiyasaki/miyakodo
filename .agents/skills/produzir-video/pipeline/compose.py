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
    OLIVA,
    PAPER,
    ROSA,
    SFX_FILES,
    VERDE,
)
from pipeline.registry import require_mode


def render_html(model: dict) -> str:
    duration = f'{model["duration"]:.3f}'
    mode = model["mode"]
    spec = require_mode(mode)
    groups_html = _captions(model, spec)
    videos_html = _videos(model, spec)
    stage = model["scenes_html"]
    grain = ""
    if spec.grain:
        grain = (
            f'<div id="grain" class="clip" data-start="0" data-duration="{duration}" '
            f'data-track-index="1"></div>'
        )
    avatar = ""
    if spec.avatar:
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
    # sem-gravacao e gravacao mantêm o teste antigo no player, para o HTML não mudar.
    # Modo novo com legenda faixa despacha por captionProfile.
    highlight = 'PROJECT.mode === "sem-gravacao"'
    if spec.caption_profile == "faixa" and spec.slug != "sem-gravacao":
        highlight = 'PROJECT.captionProfile === "faixa"'
        payload["captionProfile"] = spec.caption_profile
    if spec.caption_profile == "duas-vozes":
        payload["captionProfile"] = "duas-vozes"
    css = _css()
    caption_js = _caption_js(highlight)
    if spec.boxes == "studio" or spec.caption_profile == "duas-vozes":
        css += _css_studio()
        if spec.caption_profile == "duas-vozes":
            caption_js = _caption_js_duo()
    data = json.dumps(payload, ensure_ascii=False)
    title = escape(model["title"])
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <script src="assets/gsap.min.js"></script>
  <style>
    {css}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{duration}" data-fps="{model["fps"]}">
    <div id="bg" class="clip" data-start="0" data-duration="{duration}" data-track-index="0"></div>
    {grain}
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
{caption_js}
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
        avatar.moves.forEach((move) => {{
          const vars = {{
            x: move.x, y: move.y, scale: move.scale,
            opacity: move.opacity == null ? 1 : move.opacity,
            transformOrigin: "0 0"
          }};
          if (!move.duration) tl.set("#avatar", vars, move.at);
          else tl.to("#avatar", {{ ...vars, duration: move.duration, ease: "power3.out" }}, move.at);
        }});
        const mouths = ["#av-m0", "#av-m1", "#av-m2", "#av-m3"];
        const hz = PROJECT.mouthHz || 40;
        let lastViseme = -1;
        PROJECT.mouth.forEach((level, index) => {{
          if (index % 3) return;
          const viseme = level < 0.08 ? 0 : level < 0.2 ? 1 : level < 0.42 ? 2 : 3;
          if (viseme === lastViseme) return;
          lastViseme = viseme;
          const at = index / hz;
          mouths.forEach((sel, which) => tl.set(sel, {{ opacity: which === viseme ? 1 : 0 }}, at));
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


def _caption_js(highlight: str) -> str:
    """O bloco histórico, com as chaves já resolvidas, para o HTML dos modos antigos não mudar."""
    return (
        f"          if ({highlight}) {{\n"
        "            tl.to(sel, {\n"
        '              color: ink, scale: 1.08, duration: 0.08, ease: "power2.out", transformOrigin: "50% 60%",\n'
        f'              boxShadow: "0 0 0 3px {BROWN}", borderRadius: "14px"\n'
        "            }, word.start);\n"
        f'            tl.to(sel, {{ scale: 1, boxShadow: "0 0 0 0px {BROWN}", duration: 0.07, ease: "power2.out" }}, word.end);\n'
        "          } else {\n"
        "            tl.to(sel, { opacity: 1, duration: 0.05 }, word.start);\n"
        "          }"
    )


def _caption_js_duo() -> str:
    return """          if (PROJECT.captionProfile === "duas-vozes") {
            const words = group.words;
            const index = words.indexOf(word);
            tl.to(sel, { opacity: 1, filter: "blur(0px)", duration: 0.08, ease: "power2.out" }, word.start);
            const nxt = words[index + 1];
            if (nxt) tl.set("#" + nxt.id, { opacity: 0.38, filter: "blur(6px)" }, word.start);
          }"""


def _css_studio() -> str:
    return f"""
    .head-well {{ position: absolute; border-radius: 48px; background: {OFFWHITE}; border: 3px solid {BROWN};
      box-shadow: 0 18px 36px rgba(40,14,3,.16); }}
    .chapter-flash {{ inset: 0; z-index: 7; background: {OFFWHITE}; pointer-events: none; }}
    .chapter-flash::after {{ content: ""; position: absolute; left: 0; right: 0; top: 46%; height: 10px; background: {LARANJA}; }}
    .piece:has(.alca-card) {{ overflow: visible; }}
    .glass-card {{ height: 100%; border-radius: 36px; border: 3px solid {BROWN}; background: rgba(246,244,238,.78);
      padding: 28px 32px; box-shadow: 0 24px 44px rgba(40,14,3,.12); }}
    .glass-label, .alca-label {{ margin: 0 0 12px; font-family: "Instrument Serif", serif; font-style: italic;
      font-size: 42px; letter-spacing: .04em; text-transform: uppercase; color: {BROWN}; }}
    .glass-title {{ margin: 0 0 8px; font-weight: 800; font-size: 64px; line-height: 1; color: {BROWN}; }}
    .glass-line, .alca-line {{ margin: 10px 0; font-weight: 600; font-size: 36px; color: {BROWN}; }}
    .alca-card {{ position: relative; height: 100%; border-radius: 28px; border: 3px solid {BROWN}; background: {PAPER};
      box-shadow: 0 0 0 8px {OLIVA}; padding: 36px 32px; }}
    .handle {{ position: absolute; width: 16px; height: 16px; background: {OFFWHITE}; border: 3px solid {BROWN}; box-sizing: border-box; }}
    .handle.nw {{ left: -8px; top: -8px; }} .handle.n {{ left: calc(50% - 8px); top: -8px; }}
    .handle.ne {{ right: -8px; top: -8px; }} .handle.e {{ right: -8px; top: calc(50% - 8px); }}
    .handle.se {{ right: -8px; bottom: -8px; }} .handle.s {{ left: calc(50% - 8px); bottom: -8px; }}
    .handle.sw {{ left: -8px; bottom: -8px; }} .handle.w {{ left: -8px; top: calc(50% - 8px); }}
    .cap.duo .cap-line {{ background: {OFFWHITE}; border: 3px solid {BROWN}; border-radius: 18px; padding: 8px 16px; flex-wrap: nowrap; }}
    .cap.duo .word {{ font-weight: 800; font-size: 48px; filter: blur(6px); opacity: 0.38; }}
    .cap.duo .word.lead {{ filter: none; opacity: 1; }}
    .cap.duo .duo-script {{ font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; font-size: 56px; }}
    .cap.duo .duo-cta {{ color: {LARANJA}; text-shadow: 0 0 16px rgba(219,60,5,.55); }}
    .cap-logo {{ height: 46px; width: auto; vertical-align: middle; }}
    """


def _videos(model: dict, spec) -> str:
    if not spec.footage:
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


def _captions(model: dict, spec) -> str:
    chunks = []
    for group in model["groups"]:
        top = _top(model, group["start"], spec)
        words = []
        for index, word in enumerate(group["words"]):
            role = word["role"]
            text = escape(word["text"])
            if spec.caption_profile == "faixa":
                cls = "word serif" if role in {"emphasis", "strong", "cta"} else "word"
                inner = text
            elif spec.caption_profile == "duas-vozes":
                if role == "logo":
                    cls = "word duo-logo"
                    inner = f'<img class="cap-logo" src="assets/logo.png" alt="{text}"/>'
                elif role in {"emphasis", "strong"}:
                    cls = "word duo-script"
                    inner = text
                elif role == "cta":
                    cls = "word duo-cta"
                    inner = text
                else:
                    cls = "word duo-sans"
                    inner = text
                if index == 0:
                    cls += " lead"
            elif role == "cta":
                cls = "word pill cta"
                inner = text
            elif role == "strong":
                cls = "word pill"
                inner = text
            elif role == "emphasis":
                cls = "word key"
                inner = text
            else:
                cls = "word"
                inner = text
            words.append(
                f'<span id="{word["id"]}" class="{cls}" data-layout-allow-overlap="true">{inner}</span>'
            )
        box = ""
        dur = round(group["end"] - group["start"], 3)
        kind = spec.caption_css
        chunks.append(
            f'<div id="{group["id"]}" class="clip cap {kind}" data-start="{group["start"]}" '
            f'data-duration="{dur}" data-track-index="8" style="top:{top}px">'
            f'<div class="cap-line">{box}{"".join(words)}</div></div>'
        )
    return "".join(chunks)


def _top(model, start, spec):
    if spec.caption_anchor == "faixa":
        return spec.caption_top
    beat = model["beats"][-1]
    for item in model["beats"]:
        if item["start"] - 0.05 <= start <= item["end"] + 0.05:
            beat = item
            break
    return spec.caption_tops[beat["layout"]]


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
    #grain {{ inset: 0; z-index: 1; pointer-events: none; opacity: 0.28; mix-blend-mode: multiply;
      background: url("assets/noise.png") repeat; }}
    .beat {{ inset: 0; z-index: 4; }}
    .beat-in {{ position: absolute; inset: 0; }}
    .wash {{ position: absolute; inset: 0; }}
    .tone-ink .wash {{ background: {BROWN}; }}
    .tone-verde .wash {{ background: {VERDE}; }}
    .tone-azul .wash {{ background: {AZUL}; }}
    .tone-rosa .wash {{ background: {ROSA}; }}
    .tone-oliva .wash {{ background: {OLIVA}; }}
    .tone-ink .open, .tone-verde .open {{ color: {OFFWHITE}; }}
    .tone-ink .open .kicker, .tone-verde .open .kicker,
    .tone-ink .open .giant, .tone-verde .open .giant,
    .tone-ink .open .big, .tone-verde .open .big,
    .tone-ink .open .say, .tone-verde .open .say {{ color: {OFFWHITE}; }}
    .tone-ink .card, .tone-verde .card {{ background: {OFFWHITE}; color: {BROWN}; }}
    .tone-ink .card .kicker, .tone-verde .card .kicker {{ color: {BROWN}; }}
    .tone-ink .orbit, .tone-verde .orbit, .tone-ink .cell, .tone-verde .cell {{ color: {BROWN}; background: {OFFWHITE}; }}
    .host {{ position: absolute; overflow: hidden; z-index: 2; }}
    .host.split {{ left: 0; right: 0; top: 52%; height: 48%; }}
    .host.full {{ inset: 0; }}
    .punch {{ position: absolute; inset: 0; }}
    .host video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    .host.split video {{ object-position: center 16%; }}
    .host.full video {{ object-position: center 24%; }}
    #avatar {{ left: 48px; top: 1196px; width: 220px; z-index: 6; height: auto; transform-origin: 0 0;
      filter: drop-shadow(5px 0 0 {OFFWHITE}) drop-shadow(-5px 0 0 {OFFWHITE}) drop-shadow(0 5px 0 {OFFWHITE}) drop-shadow(0 -5px 0 {OFFWHITE}); }}
    #av-lid-l, #av-lid-r, #av-mouth-open, #av-mouth-closed, #av-rig, #av-brows {{ transform-box: fill-box; }}
    .piece {{ position: absolute; overflow: hidden; }}
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
    .statement {{ height: 100%; display: flex; flex-direction: column; justify-content: center; }}
    .big {{ margin: 0; font-family: "Instrument Serif", serif; font-size: 92px; line-height: 0.96; }}
    .carlos-wrap {{ height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 8px; }}
    .carlos-wrap img {{ width: auto; max-width: 100%; height: 74%; object-fit: contain; }}
    .say {{ margin: 0; font-family: "Instrument Serif", serif; font-size: 46px; line-height: 1.05; text-align: center; }}
    .versus {{ height: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
    .vcol {{ background: {PAPER}; color: {BROWN}; border: 3px solid {BROWN}; border-radius: 28px; padding: 22px; display: flex; flex-direction: column; min-height: 0; }}
    .vcol .kicker {{ color: inherit; }}
    .vcol.agent {{ background: {VERDE}; color: {OFFWHITE}; border-color: {VERDE}; }}
    .vcol img {{ width: auto; height: 42%; object-fit: contain; align-self: center; }}
    .vitem {{ font-size: 32px; font-weight: 700; margin: 10px 0; }}
    .cap {{ left: 48px; right: 176px; z-index: 8; display: flex; justify-content: center; }}
    .cap-line {{ position: relative; display: inline-flex; flex-wrap: wrap; justify-content: center; max-width: 820px; }}
    .cap.face .cap-line {{ background: {OFFWHITE}; border: 3px solid {BROWN}; border-radius: 22px; padding: 12px 18px 14px; }}
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
