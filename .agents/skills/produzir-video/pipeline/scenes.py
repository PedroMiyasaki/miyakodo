"""Componentes visuais combináveis. O roteiro escolhe o tipo e os parâmetros."""

import re
from html import escape

from pipeline.brand import AZUL, BROWN, LARANJA, OLIVA, ROSA, VERDE


def build_scene(pid, x, y, w, h, scene, t0, t1):
    kind = (scene or {}).get("type")
    builder = BUILDERS.get(kind)
    if builder is None:
        raise ValueError(f"cena desconhecida: {kind}")
    return builder(pid, float(x), float(y), float(w), float(h), scene or {}, float(t0), float(t1))


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


def scene_statement(pid, x, y, w, h, scene, t0, t1):
    kicker = escape(str(scene.get("kicker") or ""))
    lines = scene.get("lines") or [scene.get("text") or ""]
    lines = [str(item) for item in lines if str(item).strip()]
    if not lines:
        lines = [" "]
    chips = [str(item) for item in (scene.get("chips") or [])]
    size = int(min(h * 0.7 / max(1, len(lines)), w * 0.2))
    size = max(72, min(176, size))
    ops = _pop(pid, t0, "50% 50%")
    sfx = _sfx("impact", t0)
    rendered = []
    for index, line in enumerate(lines):
        at = t0 + 0.06 + index * 0.16
        rendered.append(f'<p id="{pid}-ln-{index}" class="big" style="font-size:{size}px">{escape(line)}</p>')
        if index:
            ops.append({
                "kind": "fromTo",
                "sel": f"#{pid}-ln-{index}",
                "from": {"y": 28, "opacity": 0},
                "to": {"y": 0, "opacity": 1, "duration": 0.36, "ease": "back.out(1.6)"},
                "at": round(at, 4),
            })
    pills = []
    for index, chip in enumerate(chips):
        at = t0 + 0.28 + index * 0.22
        pills.append(f'<span id="{pid}-c-{index}" class="pill">{escape(chip)}</span>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-c-{index}",
            "from": {"scale": 0.7, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.32, "ease": "back.out(1.8)"},
            "at": round(at, 4),
        })
        sfx.append({"name": "pop", "at": round(at, 4)})
    head = f'<p class="kicker">{kicker}</p>' if kicker else ""
    row = f'<div class="chip-row">{"".join(pills)}</div>' if pills else ""
    inner = f'<div class="statement">{head}{"".join(rendered)}{row}</div>'
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_peel(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("text") or "Sem interface"))
    kicker = escape(str(scene.get("kicker") or ""))
    chips = _lines(scene.get("items"), ["Botão", "Menu", "Tela"])
    lines = _lines(scene.get("lines"), ["API", "MCP", "CLI"])
    size = max(64, min(150, int(min(h * 0.22, w * 0.16))))
    ops = _pop(pid, t0, "50% 30%")
    sfx = _sfx("whoosh", t0)
    chip_html = []
    for index, chip in enumerate(chips):
        at = t0 + 0.2 + index * 0.18
        direction = -1 if index % 2 == 0 else 1
        chip_html.append(
            f'<span id="{pid}-c-{index}" class="pill gone peel-chip">{escape(chip)}</span>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-c-{index}",
            "from": {"scale": 0.6, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.28, "ease": "back.out(1.7)"},
            "at": round(at, 4),
        })
        ops.append({
            "kind": "to",
            "sel": f"#{pid}-c-{index}",
            "vars": {
                "y": -24,
                "opacity": 0.4,
                "rotation": 4 * direction,
                "duration": 0.7,
                "ease": "power2.in",
            },
            "at": round(at + 0.45, 4),
        })
        sfx.append({"name": "whoosh", "at": round(at + 0.45, 4)})
    head = f'<p class="kicker">{kicker}</p>' if kicker else ""
    if h >= 700:
        term = []
        for index, line in enumerate(lines):
            at = t0 + 0.7 + index * 0.28
            term.append(f'<div id="{pid}-t-{index}" class="ln">{escape(line)}</div>')
            ops.append({
                "kind": "fromTo",
                "sel": f"#{pid}-t-{index}",
                "from": {"y": 16, "opacity": 0},
                "to": {"y": 0, "opacity": 1, "duration": 0.3, "ease": "power3.out"},
                "at": round(at, 4),
            })
            sfx.append({"name": "key", "at": round(at, 4)})
        reveal = f'<div id="{pid}-term" class="term">{"".join(term)}</div>'
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-term",
            "from": {"scale": 0.92, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.4, "ease": "back.out(1.4)"},
            "at": round(t0 + 0.55, 4),
        })
    else:
        stay = []
        for index, line in enumerate(lines):
            at = t0 + 0.45 + index * 0.16
            stay.append(f'<span id="{pid}-t-{index}" class="pill">{escape(line)}</span>')
            ops.append({
                "kind": "fromTo",
                "sel": f"#{pid}-t-{index}",
                "from": {"scale": 0.7, "opacity": 0},
                "to": {"scale": 1, "opacity": 1, "duration": 0.28, "ease": "back.out(1.6)"},
                "at": round(at, 4),
            })
        reveal = f'<div class="chip-row">{"".join(stay)}</div>'
    inner = (
        f'<div class="peel">{head}'
        f'<p class="big" style="font-size:{size}px">{title}</p>'
        f'<div class="chip-row">{"".join(chip_html)}</div>'
        f'{reveal}</div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_flow(pid, x, y, w, h, scene, t0, t1):
    kicker = escape(str(scene.get("kicker") or ""))
    items = _lines(scene.get("items"), ["Um", "Dois", "Três", "Quatro"])
    ops = _pop(pid, t0, "50% 20%")
    sfx = _sfx("impact", t0)
    rows = []
    for index, item in enumerate(items):
        at = t0 + 0.16 + index * 0.32
        rows.append(
            f'<div id="{pid}-s-{index}" class="step"><b>{index + 1}</b><span>{escape(item)}</span></div>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-s-{index}",
            "from": {"x": 40, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.38, "ease": "back.out(1.5)"},
            "at": round(at, 4),
        })
        sfx.append({"name": "click", "at": round(at, 4)})
    head = f'<p class="kicker">{kicker}</p>' if kicker else ""
    inner = f'<div class="flow">{head}{"".join(rows)}</div>'
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


CARLOS_POSES = {
    "squat": "MASCOTE_1.png",
    "boss": "MASCOTE_2.png",
    "money": "MASCOTE_3.png",
    "coffee": "MASCOTE_4.png",
    "stars": "MASCOTE_5.png",
}


def _carlos_src(pose: str) -> str:
    return f'assets/carlos/{CARLOS_POSES.get(pose, CARLOS_POSES["boss"])}'


def scene_carlos(pid, x, y, w, h, scene, t0, t1):
    line = escape(str(scene.get("line") or scene.get("text") or ""))
    src = _carlos_src(str(scene.get("pose") or "boss"))
    props = _lines(scene.get("props"), [])
    ops = _pop(pid, t0, "50% 70%")
    sfx = _sfx("pop", t0)
    ops.append({
        "kind": "to",
        "sel": f"#{pid}-fig",
        "vars": {"y": -12, "duration": 0.8, "yoyo": True, "repeat": 3, "ease": "sine.inOut"},
        "at": round(t0 + 0.3, 4),
    })
    chips = []
    for index, prop in enumerate(props):
        at = t0 + 0.25 + index * 0.22
        chips.append(f'<span id="{pid}-p-{index}" class="pill">{escape(prop)}</span>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-p-{index}",
            "from": {"y": 16, "opacity": 0},
            "to": {"y": 0, "opacity": 1, "duration": 0.3, "ease": "back.out(1.6)"},
            "at": round(at, 4),
        })
        sfx.append({"name": "click", "at": round(at, 4)})
    say = f'<p class="say">{line}</p>' if line else ""
    row = f'<div class="chip-row">{"".join(chips)}</div>' if chips else ""
    inner = (
        f'<div class="carlos-wrap">{say}{row}'
        f'<img id="{pid}-fig" src="{src}" alt="Carlos"/></div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_versus(pid, x, y, w, h, scene, t0, t1):
    left = escape(str(scene.get("left") or "Pessoa"))
    right = escape(str(scene.get("right") or "Agente"))
    left_items = _lines(scene.get("left_items"), ["Pessoa"])
    right_items = _lines(scene.get("right_items"), ["Agente"])
    pose = scene.get("pose")
    ops = _pop(pid, t0)
    sfx = _sfx("whoosh", t0)
    figure = ""
    if pose:
        figure = f'<img src="{_carlos_src(str(pose))}" alt="Carlos"/>'
    left_html = []
    right_html = []
    for index, item in enumerate(left_items):
        at = t0 + 0.22 + index * 0.28
        left_html.append(f'<div id="{pid}-l-{index}" class="vitem"><i></i><span>{escape(item)}</span></div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-l-{index}",
            "from": {"x": -12, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.26, "ease": "power2.out"},
            "at": round(at, 4),
        })
    for index, item in enumerate(right_items):
        at = t0 + 0.32 + index * 0.28
        right_html.append(f'<div id="{pid}-r-{index}" class="vitem"><i></i><span>{escape(item)}</span></div>')
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-r-{index}",
            "from": {"x": 12, "opacity": 0},
            "to": {"x": 0, "opacity": 1, "duration": 0.26, "ease": "power2.out"},
            "at": round(at, 4),
        })
        sfx.append({"name": "click", "at": round(at, 4)})
    inner = (
        f'<div class="versus">'
        f'<div class="vcol">{figure}<p class="kicker">{left}</p>{"".join(left_html)}</div>'
        f'<div class="vcol agent"><p class="kicker">{right}</p>{"".join(right_html)}</div>'
        f'</div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_badge(pid, x, y, w, h, scene, t0, t1):
    text = escape(str(scene.get("text") or ""))
    inner = f'<div class="badge" style="background:{LARANJA}">{text}</div>'
    return _box(pid, x, y, w, h, inner, "open badge-wrap"), _pop(pid, t0, "50% 50%"), _sfx("pop", t0)


def scene_chart(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("text") or "Crescendo"))
    kicker = escape(str(scene.get("kicker") or ""))
    heights = [28, 42, 58, 76, 100]
    ops = _pop(pid, t0, "50% 80%")
    sfx = _sfx("impact", t0)
    bars = []
    for index, height in enumerate(heights):
        at = t0 + 0.12 + index * 0.14
        bars.append(
            f'<div class="bar-col"><i id="{pid}-bar-{index}" style="height:{height}%"></i></div>'
        )
        ops.append({
            "kind": "fromTo",
            "sel": f"#{pid}-bar-{index}",
            "from": {"scaleY": 0.05},
            "to": {"scaleY": 1, "duration": 0.45, "ease": "back.out(1.4)", "transformOrigin": "50% 100%"},
            "at": round(at, 4),
        })
        sfx.append({"name": "click", "at": round(at, 4)})
    head = f'<p class="kicker">{kicker}</p>' if kicker else ""
    inner = (
        f'<div class="chart">{head}<p class="big" style="font-size:92px">{title}</p>'
        f'<div class="bars">{"".join(bars)}</div>'
        f'<p id="{pid}-trend" class="trend late">volume sobe com o agente</p></div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_clutter(pid, x, y, w, h, scene, t0, t1):
    line = escape(str(scene.get("line") or "Não para você"))
    src = _carlos_src(str(scene.get("pose") or "boss"))
    fields = _lines(scene.get("props"), ["Nome", "Email", "Cargo", "Empresa", "Telefone", "CNPJ"])
    ops = _pop(pid, t0, "70% 60%")
    sfx = _sfx("whoosh", t0)
    rows = []
    for index, field in enumerate(fields):
        at = t0 + 0.12 + index * 0.12
        late = " late" if index >= 3 else ""
        rows.append(
            f'<div id="{pid}-f-{index}" class="field{late}"><span>{escape(field)}</span><b>X</b></div>'
        )
        if index < 3:
            ops.append({
                "kind": "fromTo",
                "sel": f"#{pid}-f-{index}",
                "from": {"opacity": 0},
                "to": {"opacity": 1, "duration": 0.28, "ease": "power2.out"},
                "at": round(at, 4),
            })
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-fig",
        "from": {"scale": 0.8, "opacity": 0},
        "to": {"scale": 1, "opacity": 1, "duration": 0.45, "ease": "back.out(1.5)"},
        "at": round(t0 + 0.2, 4),
    })
    inner = (
        f'<div class="clutter"><div class="form-card"><div class="form">{"".join(rows)}</div></div>'
        f'<div class="clutter-side"><p class="say">{line}</p>'
        f'<img id="{pid}-fig" src="{src}" alt="Carlos"/></div></div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_maze(pid, x, y, w, h, scene, t0, t1):
    line = escape(str(scene.get("line") or "Ruim para o agente"))
    src = _carlos_src(str(scene.get("pose") or "stars"))
    cards = _lines(scene.get("props"), ["Modal", "Dropdown", "Popup", "Cookie", "Menu", "Alerta"])
    ops = _pop(pid, t0, "50% 60%")
    sfx = _sfx("notification", t0)
    pops = []
    for index, card in enumerate(cards):
        at = t0 + 0.1 + (index % 3) * 0.16
        late = " late" if index >= 3 else ""
        rot = (-8, 6, -4, 9, -6, 5)[index % 6]
        pops.append(
            f'<div id="{pid}-z-{index}" class="popup{late}" style="transform:rotate({rot}deg)">{escape(card)}</div>'
        )
        if index < 3:
            ops.append({
                "kind": "fromTo",
                "sel": f"#{pid}-z-{index}",
                "from": {"scale": 0.4, "opacity": 0},
                "to": {"scale": 1, "opacity": 1, "duration": 0.32, "ease": "back.out(1.7)"},
                "at": round(at, 4),
            })
            sfx.append({"name": "pop", "at": round(at, 4)})
    inner = (
        f'<div class="maze"><div class="popups">{"".join(pops)}</div>'
        f'<img id="{pid}-fig" src="{src}" alt="Carlos"/>'
        f'<p class="say">{line}</p></div>'
    )
    ops.append({
        "kind": "fromTo",
        "sel": f"#{pid}-fig",
        "from": {"scale": 0.86, "opacity": 0},
        "to": {"scale": 1, "opacity": 1, "duration": 0.4, "ease": "back.out(1.4)"},
        "at": round(t0 + 0.15, 4),
    })
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


def scene_close(pid, x, y, w, h, scene, t0, t1):
    title = escape(str(scene.get("text") or "Headless"))
    handle = escape(str(scene.get("handle") or "@pedro.miyasaki.ia"))
    ops = _pop(pid, t0, "50% 40%")
    sfx = _sfx("chime", t0)
    left = ["Botão", "Menu", "Tela"]
    left_html = "".join(
        f'<span class="pill gone">{escape(item)}</span>' for item in left
    )
    inner = (
        f'<div class="close"><p class="kicker">A virada</p>'
        f'<div class="close-card">'
        f'<p class="lane">UI tradicional</p>'
        f'<div class="chip-row">{left_html}</div>'
        f'<p class="lane headless">{title}</p>'
        f'<p class="api-line">API · MCP · CLI</p>'
        f'</div>'
        f'<p class="handle">Miyakodo · {handle}</p></div>'
    )
    return _box(pid, x, y, w, h, inner, "open"), ops, sfx


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
    "statement": scene_statement,
    "carlos": scene_carlos,
    "versus": scene_versus,
    "peel": scene_peel,
    "flow": scene_flow,
    "chart": scene_chart,
    "clutter": scene_clutter,
    "maze": scene_maze,
    "close": scene_close,
}

# Cores usadas no SVG/CSS inline acima ficam explícitas para o teste de paleta.
ACCENT_SAMPLE = (AZUL, BROWN, LARANJA, ROSA, VERDE)
