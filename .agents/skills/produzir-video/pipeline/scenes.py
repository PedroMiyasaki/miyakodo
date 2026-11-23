"""Componentes visuais combináveis. O roteiro escolhe o tipo e os parâmetros."""

import re
from html import escape

from pipeline.brand import AZUL, BROWN, LARANJA, MASCOT_FILES, OLIVA, ROSA, VERDE


def build_scene(pid, x, y, w, h, scene, t0, t1):
    kind = (scene or {}).get("type")
    builder = BUILDERS.get(kind)
    if builder is None:
        raise ValueError(f"cena desconhecida: {kind}")
    html, ops, sfx = builder(pid, float(x), float(y), float(w), float(h), scene or {}, float(t0), float(t1))
    if f'id="{pid}-root"' in html:
        span = max(0.7, min(1.4, (float(t1) - float(t0)) * 0.35))
        ops = list(ops) + [{
            "kind": "to",
            "sel": f"#{pid}-root",
            "vars": {"y": -8, "duration": round(span, 3), "yoyo": True, "repeat": 1, "ease": "sine.inOut"},
            "at": round(float(t0) + 0.4, 4),
        }]
    return html, ops, sfx


def _box(pid, x, y, w, h, inner, cls=""):
    return (
        f'<div id="{pid}-root" class="piece {cls}" '
        f'style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px">{inner}</div>'
    )


def _pop(pid, t0, origin="50% 40%"):
    return [{
        "kind": "fromTo",
        "sel": f"#{pid}-root",
        "from": {"scale": 0.84, "opacity": 0},
        "to": {
            "scale": 1,
            "opacity": 1,
            "duration": 0.46,
            "ease": "back.out(1.7)",
            "transformOrigin": origin,
        },
        "at": round(t0, 4),
    }]


def _sfx(name, at):
    return [{"name": name, "at": round(at, 4)}]


def _lines(values, fallback):
    items = values or fallback
    return [str(item) for item in items]


def scene_stack(pid, x, y, w, h, scene, t0, t1):
    children = scene.get("children") or []
    if not children:
        raise ValueError("stack sem children")
    gap = 28
    each = (h - gap * (len(children) - 1)) / len(children)
    html, ops, sfx = [], [], []
    for index, child in enumerate(children):
        child_t = t0 + index * 0.42
        piece_html, piece_ops, piece_sfx = build_scene(
            f"{pid}s{index}", x, y + index * (each + gap), w, each, child, child_t, t1,
        )
        html.append(piece_html)
        ops.extend(piece_ops)
        sfx.extend(piece_sfx)
    return "".join(html), ops, sfx


def scene_timeline(pid, x, y, w, h, scene, t0, t1):
    items = _lines(scene.get("items"), ["Um", "Dois", "Três"])
    title = escape(str(scene.get("title") or "Roteiro"))
    rows = []
    ops = _pop(pid, t0)
    sfx = _sfx("pop", t0)
    span = max(0.4, (t1 - t0) * 0.75)
    for index, item in enumerate(items):
        at = t0 + 0.25 + span * index / max(1, len(items))
        rows.append(
            f'<div id="{pid}-row-{index}" class="tl-row">'
            f'<span class="tl-num">{index + 1}</span>'
            f'<span class="tl-label">{escape(item)}</span></div>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-row-{index}",
            "from": {"x": -28, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.35, "ease": "power3.out"},
            "at": round(at, 4),
        })
        sfx.append({"name": "click", "at": round(at, 4)})
    inner = f'<p class="kicker">{title}</p><div class="tl-list">{"".join(rows)}</div>'
    return _box(pid, x, y, w, h, inner, "card"), ops, sfx


def scene_mockup(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("title") or "Janela"))
    lines = _lines(scene.get("lines"), ["linha"])
    kind = escape(str(scene.get("kind") or "browser"))
    body = []
    ops = _pop(pid, t0, "50% 20%")
    sfx = _sfx("whoosh", t0)
    for index, line in enumerate(lines):
        at = t0 + 0.35 + index * 0.38
        body.append(f'<div id="{pid}-ln-{index}" class="mock-line">{escape(line)}</div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-ln-{index}",
            "from": {"y": 16, "opacity": 0},
            "to": {"y": 0, "opacity": 1, "duration": 0.28, "ease": "power2.out"},
            "at": round(at, 4),
        })
    scan = ""
    if scene.get("scan"):
        scan = f'<div id="{pid}-scan" class="scan"></div>'
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-scan",
            "from": {"y": 0},
            "to": {"y": max(80, h - 160), "duration": min(1.6, max(0.6, t1 - t0 - 0.4)), "ease": "none", "repeat": 2, "yoyo": True},
            "at": round(t0 + 0.3, 4),
        })
        sfx.append({"name": "whoosh", "at": round(t0 + 0.3, 4)})
    inner = (
        f'<div class="chrome"><span class="dot" style="background:{ROSA}"></span>'
        f'<span class="dot" style="background:{OLIVA}"></span>'
        f'<span class="dot" style="background:{VERDE}"></span>'
        f'<span class="chrome-title">{title}</span><em class="kind">{kind}</em></div>'
        f'<div class="mock-body">{"".join(body)}{scan}</div>'
    )
    return _box(pid, x, y, w, h, inner, "card window"), ops, sfx


def scene_counter(pid, x, y, w, h, scene, t0, t1):
    value = int(scene.get("value") or 3)
    value = max(1, min(value, 24))
    label = escape(str(scene.get("label") or ""))
    steps = min(value, 10)
    nums = []
    ops = _pop(pid, t0, "50% 50%")
    sfx = _sfx("impact", t0)
    span = max(0.4, (t1 - t0) * 0.7)
    for index in range(steps + 1):
        number = round(value * index / steps)
        nums.append(f'<div id="{pid}-n-{index}" class="giant">{number}</div>')
        at = t0 + span * index / steps
        ops.append({"kind": "set", "sel": f"#{pid}-n-{index}", "vars": {"opacity": 1}, "at": round(at, 4)})
        if index:
            ops.append({"kind": "set", "sel": f"#{pid}-n-{index-1}", "vars": {"opacity": 0}, "at": round(at, 4)})
            sfx.append({"name": "click", "at": round(at, 4)})
    inner = f'<div class="giant-wrap">{"".join(nums)}</div><p class="kicker center">{label}</p>'
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_diagram(pid, x, y, w, h, scene, t0, t1):
    center = escape(str(scene.get("center") or "Centro"))
    items = _lines(scene.get("items"), ["A", "B", "C"])
    ops = _pop(pid, t0, "50% 50%")
    sfx = _sfx("pop", t0)
    nodes = []
    for index, item in enumerate(items):
        at = t0 + 0.28 + index * 0.36
        nodes.append(f'<div id="{pid}-n-{index}" class="orbit o{index % 6}">{escape(item)}</div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-n-{index}",
            "from": {"scale": 0.4, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.4, "ease": "back.out(1.8)"},
            "at": round(at, 4),
        })
        sfx.append({"name": "pop", "at": round(at, 4)})
    inner = f'<div class="hub">{center}</div>{"".join(nodes)}'
    return _box(pid, x, y, w, h, inner, "open diagram"), ops, sfx


def scene_chat(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("title") or "Mensagens"))
    messages = scene.get("messages") or [{"from": "Pedro", "text": "Olha isso."}]
    ops = _pop(pid, t0)
    sfx = _sfx("notification", t0)
    bubbles = []
    for index, message in enumerate(messages):
        side = "me" if index % 2 == 0 else "them"
        at = t0 + 0.3 + index * 0.45
        who = escape(str(message.get("from") or ""))
        text = escape(str(message.get("text") or ""))
        bubbles.append(
            f'<div id="{pid}-m-{index}" class="bubble {side}">'
            f'<b>{who}</b><span>{text}</span></div>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-m-{index}",
            "from": {"y": 24, "opacity": 0, "scale": 0.9},
            "to": {"y": 0, "opacity": 1, "scale": 1, "duration": 0.32, "ease": "back.out(1.5)"},
            "at": round(at, 4),
        })
        if index:
            sfx.append({"name": "notification", "at": round(at, 4)})
    inner = f'<p class="kicker">{title}</p>{"".join(bubbles)}'
    return _box(pid, x, y, w, h, inner, "card"), ops, sfx


def scene_code(pid, x, y, w, h, scene, t0, t1):
    filename = escape(str(scene.get("filename") or "evals.ts"))
    lines = _lines(scene.get("lines"), ['const ok = avaliar(saida)'])
    ops = _pop(pid, t0, "50% 0%")
    sfx = _sfx("typing", t0)
    rendered = []
    cursor_at = t0 + 0.35
    for index, line in enumerate(lines):
        chars = []
        for ch_index, ch in enumerate(line):
            at = cursor_at
            cursor_at += 0.045
            token = _paint(line, ch_index)
            chars.append(f'<i id="{pid}-c-{index}-{ch_index}" class="{token}">{escape(ch)}</i>')
            if ch_index % 2 == 0:
                ops.append({
                    "kind": "set",
                    "sel": f"#{pid}-c-{index}-{ch_index}",
                    "vars": {"opacity": 1},
                    "at": round(at, 4),
                })
            else:
                ops.append({
                    "kind": "set",
                    "sel": f"#{pid}-c-{index}-{ch_index}",
                    "vars": {"opacity": 1},
                    "at": round(at, 4),
                })
        rendered.append(f'<div class="code-line">{"".join(chars)}</div>')
        sfx.append({"name": "key", "at": round(t0 + 0.4 + index * 0.45, 4)})
    inner = (
        f'<div class="chrome"><span class="chrome-title">{filename}</span></div>'
        f'<div class="code-body">{"".join(rendered)}</div>'
    )
    return _box(pid, x, y, w, h, inner, "card window code"), ops, sfx


def _paint(line, index):
    for match in re.finditer(r"\b(const|return|if|await|function)\b|\".*?\"|'.*?'", line):
        if match.start() <= index < match.end():
            token = match.group(0)
            return "str" if token[:1] in "\"'" else "kw"
    return "cd"


def scene_phone(pid, x, y, w, h, scene, t0, t1):
    handle = escape(str(scene.get("handle") or "@MIYAKODO"))
    comment = escape(str(scene.get("comment") or "explica isso"))
    dm = escape(str(scene.get("dm") or "te mando o material"))
    ops = _pop(pid, t0, "50% 80%")
    sfx = [
        {"name": "whoosh", "at": round(t0, 4)},
        {"name": "notification", "at": round(t0 + 0.45, 4)},
        {"name": "pop", "at": round(t0 + 0.9, 4)},
    ]
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-comment",
        "from": {"y": 20, "opacity": 0},
        "to": {"y": 0, "opacity": 1, "duration": 0.35, "ease": "power2.out"},
        "at": round(t0 + 0.45, 4),
    })
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-dm",
        "from": {"y": 20, "opacity": 0},
        "to": {"y": 0, "opacity": 1, "duration": 0.35, "ease": "back.out(1.4)"},
        "at": round(t0 + 0.9, 4),
    })
    inner = (
        f'<div class="phone">'
        f'<div class="profile"><img class="logo" src="assets/logo.png" alt="Miyakodo"/>'
        f'<div><b>Pedro</b><span>{handle}</span></div></div>'
        f'<div id="{pid}-comment" class="comment"><b>comentário</b><span>{comment}</span></div>'
        f'<div id="{pid}-dm" class="dm"><b>mensagem</b><span>{dm}</span></div>'
        f'</div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_grid(pid, x, y, w, h, scene, t0, t1):
    items = _lines(scene.get("items"), ["1", "2", "3", "4", "5", "6", "7", "8", "9"])[:9]
    ops = _pop(pid, t0)
    sfx = _sfx("click", t0)
    cells = []
    for index, item in enumerate(items):
        at = t0 + 0.12 + (index % 9) * 0.12
        cells.append(f'<div id="{pid}-g-{index}" class="cell">{escape(item)}</div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-g-{index}",
            "from": {"scale": 0.7, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.28, "ease": "back.out(2)"},
            "at": round(at, 4),
        })
        ops.append({
            "kind": "to",
            "sel": f"#{pid}-g-{index}",
            "vars": {"y": -8, "duration": 0.22, "yoyo": True, "repeat": 1, "ease": "sine.inOut"},
            "at": round(at + 0.55, 4),
        })
    while len(cells) % 3 != 0:
        cells.append('<div class="cell ghost"></div>')
    inner = f'<div class="grid">{"".join(cells)}</div>'
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_scanline(pid, x, y, w, h, scene, t0, t1):
    label = escape(str(scene.get("label") or "leitura"))
    ops = _pop(pid, t0)
    travel = max(60, h - 90)
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-bar",
        "from": {"y": 0},
        "to": {"y": travel, "duration": min(1.5, max(0.5, t1 - t0 - 0.3)), "ease": "none", "repeat": 2, "yoyo": True},
        "at": round(t0 + 0.2, 4),
    })
    inner = f'<p class="kicker">{label}</p><div id="{pid}-bar" class="scan fat"></div>'
    return _box(pid, x, y, w, h, inner, "card"), ops, _sfx("whoosh", t0)


def scene_folders(pid, x, y, w, h, scene, t0, t1):
    root = escape(str(scene.get("root") or "pasta"))
    items = scene.get("items") or [{"name": "arquivo", "depth": 1}]
    ops = _pop(pid, t0)
    sfx = _sfx("click", t0)
    rows = [f'<div class="folder-root">{root}</div>']
    for index, item in enumerate(items):
        if isinstance(item, str):
            name, depth = item, 1
        else:
            name, depth = item.get("name", "item"), int(item.get("depth") or 1)
        at = t0 + 0.22 + index * 0.28
        pad = 18 + depth * 28
        rows.append(
            f'<div id="{pid}-f-{index}" class="folder-row" style="padding-left:{pad}px">{escape(str(name))}</div>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-f-{index}",
            "from": {"x": -16, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.28, "ease": "power2.out"},
            "at": round(at, 4),
        })
    inner = "".join(rows)
    return _box(pid, x, y, w, h, inner, "card"), ops, sfx


def scene_bullets(pid, x, y, w, h, scene, t0, t1):
    kicker = escape(str(scene.get("kicker") or "Lista"))
    items = _lines(scene.get("items"), ["ponto"])
    ops = _pop(pid, t0)
    sfx = _sfx("pop", t0)
    rows = []
    for index, item in enumerate(items):
        at = t0 + 0.24 + index * 0.32
        rows.append(f'<div id="{pid}-b-{index}" class="bullet"><i></i><span>{escape(item)}</span></div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-b-{index}",
            "from": {"y": 12, "opacity": 0},
            "to": {"y": 0, "opacity": 1, "duration": 0.28, "ease": "power2.out"},
            "at": round(at, 4),
        })
    inner = f'<p class="kicker">{kicker}</p>{"".join(rows)}'
    return _box(pid, x, y, w, h, inner, "card"), ops, sfx


def scene_quote(pid, x, y, w, h, scene, t0, t1):
    text = escape(str(scene.get("text") or ""))
    by = escape(str(scene.get("by") or ""))
    inner = f'<p class="quote">{text}</p><p class="by">{by}</p>'
    return _box(pid, x, y, w, h, inner, "card quote-card"), _pop(pid, t0), _sfx("chime", t0)


def scene_badge(pid, x, y, w, h, scene, t0, t1):
    text = escape(str(scene.get("text") or ""))
    inner = f'<div class="badge" style="background:{LARANJA}">{text}</div>'
    return _box(pid, x, y, w, h, inner, "open badge-wrap"), _pop(pid, t0, "50% 50%"), _sfx("pop", t0)


def scene_hero(pid, x, y, w, h, scene, t0, t1):
    text = str(scene.get("text") or "")
    kicker = escape(str(scene.get("kicker") or ""))
    size = 48 if h < 220 else (120 if len(text) <= 14 else 92 if len(text) <= 22 else 76)
    items = [str(item) for item in (scene.get("items") or [])]
    chips = []
    ops = _pop(pid, t0, "50% 60%")
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-hero",
        "from": {"y": 36, "scale": 0.92, "opacity": 0},
        "to": {"y": 0, "scale": 1, "opacity": 1, "duration": 0.42, "ease": "power3.out"},
        "at": round(t0 + 0.06, 4),
    })
    for index, item in enumerate(items):
        at = t0 + 0.32 + index * 0.22
        chips.append(f'<span id="{pid}-chip-{index}" class="chip">{escape(item)}</span>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-chip-{index}",
            "from": {"y": 16, "opacity": 0},
            "to": {"y": 0, "opacity": 1, "duration": 0.28, "ease": "back.out(1.6)"},
            "at": round(at, 4),
        })
    kicker_html = f'<p class="hero-kicker">{kicker}</p>' if kicker else ""
    chip_html = f'<div class="chip-row">{"".join(chips)}</div>' if chips else ""
    inner = (
        f'{kicker_html}'
        f'<p id="{pid}-hero" class="hero-text" style="font-size:{size}px">{escape(text)}</p>'
        f'{chip_html}'
    )
    return _box(pid, x, y, w, h, inner, "open hero"), ops, _sfx("impact", t0)


def scene_reveal(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("title") or "Headless Software"))
    rows = _lines(scene.get("lines"), ["Botão", "Menu", "Tela"])
    agent = escape(str(scene.get("agent") or "o agente"))
    pose = str(scene.get("pose") or "estrelas")
    filename = MASCOT_FILES.get(pose, MASCOT_FILES["estrelas"])
    ops = _pop(pid, t0, "50% 20%")
    sfx = _sfx("whoosh", t0)
    row_html = []
    for index, row in enumerate(rows):
        at = t0 + 0.28 + index * 0.28
        row_html.append(f'<div id="{pid}-row-{index}" class="ui-row">{escape(row)}</div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-row-{index}",
            "from": {"x": 0, "opacity": 1},
            "to": {"x": 80, "opacity": 0, "duration": 0.35, "ease": "power2.in"},
            "at": round(at, 4),
        })
        sfx.append({"name": "whoosh", "at": round(at, 4)})
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-agent",
        "from": {"y": 24, "scale": 0.8, "opacity": 0},
        "to": {"y": 0, "scale": 1, "opacity": 1, "duration": 0.4, "ease": "back.out(1.7)"},
        "at": round(t0 + 0.9, 4),
    })
    ops.append({
        "kind": "to",
        "sel": f"#{pid}-agent",
        "vars": {"y": -6, "duration": 0.8, "yoyo": True, "repeat": 1, "ease": "sine.inOut"},
        "at": round(t0 + 1.35, 4),
    })
    sfx.append({"name": "pop", "at": round(t0 + 0.9, 4)})
    inner = (
        f'<p id="{pid}-title" class="hero-text" style="font-size:78px">{title}</p>'
        f'<div class="ui-card">{"".join(row_html)}</div>'
        f'<div id="{pid}-agent" class="agent-pill">'
        f'<img src="assets/{filename}" alt="Carlos"/>'
        f'<span>{agent}</span></div>'
    )
    return _box(pid, x, y, w, h, inner, "open hero"), ops, sfx


def scene_mascot(pid, x, y, w, h, scene, t0, t1):
    pose = str(scene.get("pose") or "chefe")
    filename = MASCOT_FILES.get(pose)
    if not filename:
        raise ValueError(f"pose de mascote desconhecida: {pose}")
    kicker = escape(str(scene.get("kicker") or ""))
    line = escape(str(scene.get("line") or scene.get("text") or ""))
    chips = [str(item) for item in (scene.get("chips") or scene.get("items") or [])]
    bubbles = [str(item) for item in (scene.get("bubbles") or [])]
    chip_html = []
    bubble_html = []
    ops = _pop(pid, t0, "30% 80%")
    ops.append({
        "kind": "to",
        "sel": f"#{pid}-fig",
        "vars": {"y": -10, "duration": 0.7, "yoyo": True, "repeat": 3, "ease": "sine.inOut"},
        "at": round(t0 + 0.2, 4),
    })
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-line",
        "from": {"y": 18, "opacity": 0},
        "to": {"y": 0, "opacity": 1, "duration": 0.32, "ease": "power2.out"},
        "at": round(t0 + 0.18, 4),
    })
    sfx = _sfx("pop", t0)
    for index, chip in enumerate(chips):
        at = t0 + 0.34 + index * 0.18
        chip_html.append(f'<span id="{pid}-chip-{index}" class="chip">{escape(chip)}</span>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-chip-{index}",
            "from": {"scale": 0.7, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.26, "ease": "back.out(1.8)"},
            "at": round(at, 4),
        })
    for index, bubble in enumerate(bubbles):
        at = t0 + 0.5 + index * 0.28
        bubble_html.append(f'<div id="{pid}-say-{index}" class="say">{escape(bubble)}</div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-say-{index}",
            "from": {"x": 20, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.28, "ease": "power2.out"},
            "at": round(at, 4),
        })
        sfx.append({"name": "notification", "at": round(at, 4)})
    inner = (
        f'<div class="cast">'
        f'<img id="{pid}-fig" class="cast-fig" src="assets/{filename}" alt="Carlos"/>'
        f'<div class="cast-copy">'
        f'<p class="kicker">{kicker}</p>'
        f'<p id="{pid}-line" class="cast-line">{line}</p>'
        f'<div class="chip-row">{"".join(chip_html)}</div>'
        f'{"".join(bubble_html)}'
        f'</div></div>'
    )
    return _box(pid, x, y, w, h, inner, "card cast-card"), ops, sfx


BUILDERS = {
    "stack": scene_stack,
    "timeline": scene_timeline,
    "mockup": scene_mockup,
    "counter": scene_counter,
    "diagram": scene_diagram,
    "chat": scene_chat,
    "code": scene_code,
    "phone": scene_phone,
    "grid": scene_grid,
    "scanline": scene_scanline,
    "folders": scene_folders,
    "bullets": scene_bullets,
    "quote": scene_quote,
    "badge": scene_badge,
    "hero": scene_hero,
    "reveal": scene_reveal,
    "mascot": scene_mascot,
}

# Cores usadas no SVG/CSS inline acima ficam explícitas para o teste de paleta.
ACCENT_SAMPLE = (AZUL, BROWN, LARANJA, ROSA, VERDE)
