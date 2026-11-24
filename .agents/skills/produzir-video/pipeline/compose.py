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
from pipeline.zones import BURN_PLATE, zones


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
    {_masks(model)}
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
            const ink = word.role === "cta" ? "{LARANJA}" : "{VERDE}";
            tl.to(sel, {{
              backgroundColor: ink, color: "{OFFWHITE}", scale: 1.06,
              duration: 0.06, ease: "power2.out"
            }}, word.start);
            tl.to(sel, {{
              backgroundColor: "transparent", color: "{BROWN}", scale: 1,
              duration: 0.08, ease: "power2.out"
            }}, word.end);
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
        tl.fromTo("#" + video.id, {{ scale: 1 }}, {{
          scale: video.punch_scale || 1.08,
          duration: Math.max(0.4, video.duration - 0.05),
          ease: "power1.inOut",
          transformOrigin: "50% 28%"
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
    """O <video> é filho direto da composição. Sem caixa por cima, sem ancestral com data-start."""
    if model["mode"] != "gravacao":
        return ""
    blocks = []
    for video in model["videos"]:
        x, y, w, h = video["box"]
        blocks.append(
            f'<video id="{video["id"]}" class="clip face-video {video["host"]}" '
            f'src="assets/footage.mp4" muted playsinline '
            f'data-start="{video["start"]}" data-duration="{video["duration"]}" '
            f'data-media-start="{video["media_start"]}" data-track-index="1" '
            f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;'
            f'object-position:{video["object_position"]}"></video>'
        )
    return "".join(blocks)


def _masks(model: dict) -> str:
    if model["mode"] != "gravacao":
        return ""
    blocks = []
    for beat in model["beats"]:
        zone = zones(beat["layout"])
        if not zone["cover"]:
            continue
        box = BURN_PLATE if model.get("burned_captions") else zone["caption"]
        blocks.append(
            f'<div class="clip burn" data-start="{beat["start"]}" '
            f'data-duration="{round(beat["end"] - beat["start"], 3)}" data-track-index="7" '
            f'data-layout-allow-overlap="true" '
            f'style="left:{box.x}px;top:{box.y}px;width:{box.w}px;height:{box.h}px"></div>'
        )
    return "".join(blocks)


def _captions(model: dict) -> str:
    mode = model["mode"]
    chunks = []
    for group in model["groups"]:
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
            words.append(f'<span id="{word["id"]}" class="{cls}">{escape(word["text"])}</span>')
        dur = round(group["end"] - group["start"], 3)
        if mode == "sem-gravacao":
            box = 'style="top:156px"'
            kind = "face"
        else:
            zone = zones(_layout_at(model, group["start"]))
            rect = zone["caption"]
            kind = "grav cover" if zone["cover"] else "grav"
            box = (
                f'style="left:{rect.x}px;top:{rect.y}px;width:{rect.w}px;height:{rect.h}px"'
            )
        chunks.append(
            f'<div id="{group["id"]}" class="clip cap {kind}" data-start="{group["start"]}" '
            f'data-duration="{dur}" data-track-index="8" {box}>'
            f'<div class="cap-line">{"".join(words)}</div></div>'
        )
    return "".join(chunks)


def _layout_at(model, start):
    beat = model["beats"][-1]
    for item in model["beats"]:
        if item["start"] - 0.05 <= start <= item["end"] + 0.05:
            beat = item
            break
    return beat["layout"]


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
    .beat {{ z-index: 4; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
    .beat .piece.card, .beat .piece.board {{
      position: relative; left: auto !important; top: auto !important;
      width: calc(100% - 48px) !important; height: auto !important;
      max-height: calc(100% - 36px);
    }}
    .face-video {{ z-index: 3; background: transparent; }}
    .face-video.pip {{ z-index: 6; border-radius: 32px; border: 4px solid {BROWN}; box-shadow: 0 16px 28px rgba(40,14,3,.22); }}
    .face-video.full {{ z-index: 1; }}
    .face-video.split {{ z-index: 2; }}
    .burn {{ z-index: 7; background: {OFFWHITE}; border-radius: 28px; box-shadow: 0 16px 32px rgba(40,14,3,.16); }}
    #avatar {{ left: 36px; top: 1460px; width: 280px; z-index: 6; height: auto; }}
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
    .mock-line {{ display: flex; align-items: center; gap: 14px; margin: 12px 0; padding: 14px 16px; border-radius: 18px; background: {OFFWHITE}; box-shadow: 0 10px 22px rgba(40,14,3,.08); font-size: 32px; font-weight: 700; }}
    .mock-line i, .status-row i, .layer-card i {{ width: 42px; height: 42px; border-radius: 50%; background: {VERDE}; color: {OFFWHITE}; display: grid; place-items: center; font-style: normal; font-weight: 800; flex: 0 0 auto; }}
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
    .hero {{ display: flex; flex-direction: column; justify-content: center; height: 100%; gap: 18px; }}
    .hero.slam {{ justify-content: center; background: {OFFWHITE}; border: 3px solid {BROWN}; border-radius: 28px; box-shadow: 0 18px 36px rgba(40,14,3,.22); padding: 16px 28px; }}
    .hero.slam .hero-kicker {{ color: {LARANJA}; font-size: 26px; letter-spacing: .06em; }}
    .stage-swap {{ position: relative; }}
    .app-shell {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; gap: 14px; }}
    .layer-stack {{ position: relative; display: flex; flex-direction: column; gap: 14px; }}
    .app-head {{ background: {VERDE}; color: {OFFWHITE}; border-radius: 18px; padding: 12px 18px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; font-size: 22px; }}
    .app-btn {{ display: flex; align-items: center; justify-content: space-between; background: {PAPER}; border-radius: 18px; padding: 16px 18px; box-shadow: 0 12px 24px rgba(40,14,3,.1); font-size: 32px; font-weight: 700; }}
    .app-btn b {{ width: 42px; height: 42px; border-radius: 50%; background: {LARANJA}; color: {OFFWHITE}; display: grid; place-items: center; }}
    .layer-card, .status-row {{ display: flex; align-items: center; gap: 14px; background: {PAPER}; border-radius: 18px; padding: 16px 18px; box-shadow: 0 12px 24px rgba(40,14,3,.1); font-size: 32px; }}
    .layer-card {{ opacity: 0; }}
    .layer-stack .agent-pill {{ opacity: 0; }}
    .layer-card em, .status-row em {{ margin-left: auto; font-style: normal; color: {VERDE}; font-weight: 700; font-size: 22px; }}
    .board-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; background: {VERDE}; color: {OFFWHITE}; border-radius: 20px; padding: 16px 20px; margin-bottom: 16px; }}
    .board-head b {{ font-family: "Instrument Serif", serif; font-size: 48px; font-weight: 400; }}
    .board-head span {{ font-size: 22px; letter-spacing: .04em; text-transform: uppercase; }}
    .board-list {{ display: flex; flex-direction: column; gap: 12px; }}
    .hero-kicker {{ margin: 0; font-weight: 700; font-size: 28px; letter-spacing: .08em; text-transform: uppercase; color: {MUTED}; }}
    .hero-text {{ margin: 0; font-family: "Instrument Serif", serif; line-height: .92; color: {BROWN}; }}
    .chip-row {{ display: flex; flex-wrap: wrap; gap: 12px; }}
    .chip {{ background: {VERDE}; color: {OFFWHITE}; border-radius: 999px; padding: 12px 18px; font-weight: 800; font-size: 30px; }}
    .cast {{ display: grid; grid-template-columns: 44% 1fr; gap: 18px; height: 100%; align-items: center; }}
    .cast-fig {{ width: 100%; height: 92%; object-fit: contain; justify-self: center; }}
    .cast-copy {{ min-width: 0; display: flex; flex-direction: column; gap: 12px; }}
    .cast-line {{ margin: 0; font-family: "Instrument Serif", serif; font-size: 58px; line-height: 1.02; }}
    .cast-card {{ padding: 22px 24px; }}
    .say {{ background: {AZUL}; color: {BROWN}; border-radius: 22px; padding: 14px 16px; font-weight: 700; font-size: 30px; }}
    .ui-card {{ background: {PAPER}; border: 3px solid {BROWN}; border-radius: 24px; padding: 18px 20px; }}
    .ui-row {{ font-size: 34px; font-weight: 700; padding: 10px 0; border-bottom: 2px solid {CINZA}; }}
    .agent-pill {{ display: inline-flex; align-items: center; gap: 12px; background: {VERDE}; color: {OFFWHITE}; border-radius: 24px; padding: 16px 18px; font-weight: 800; font-size: 32px; }}
    .agent-pill img {{ height: 72px; width: auto; }}
    .cap.face {{ left: 60px; right: 160px; }}
    .cap {{ z-index: 9; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    .cap-line {{ position: relative; display: inline-flex; flex-wrap: wrap; justify-content: center; align-items: center; max-width: 100%; }}
    .cap.grav {{ background: {OFFWHITE}; }}
    .cap.grav .cap-line {{ background: transparent; border: 0; padding: 0; }}
    .cap.cover {{ align-items: center; padding-top: 0; background: transparent; }}
    .cap.cover .cap-line {{ background: transparent; border: 0; }}
    .cap-box {{ position: absolute; border: 3px solid {BROWN}; border-radius: 16px; }}
    .cap.face .word {{ color: {MUTED}; }}
    .cap.grav .word {{ opacity: 1; }}
    .word {{ display: inline-block; margin: 0 6px; font-weight: 600; font-size: 54px; line-height: 1.05; color: {BROWN}; }}
    .serif {{ font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; font-size: 62px; }}
    .cap.grav .word {{ font-weight: 800; font-size: 56px; padding: 2px 10px; border-radius: 14px; }}
    .word.key {{ color: {VERDE}; }}
    .word.pill {{ background: {BROWN}; color: {OFFWHITE}; border-radius: 999px; padding: 6px 16px; }}
    .word.pill.cta {{ background: {LARANJA}; }}
    """
