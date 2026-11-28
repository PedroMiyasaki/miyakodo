"""Avatar ilustrado do Pedro no modo sem gravação.

Quatro bocas e uma piscada em assets/pedro/*.png, fundo transparente,
sem borda de adesivo. Carlos continua sendo o público.
"""


def avatar_html() -> str:
    faces = ["m0", "m1", "m2", "m3", "blink"]
    images = []
    for name in faces:
        hidden = "" if name == "m0" else ' style="opacity:0"'
        images.append(
            f'<img id="av-{name}" class="av-face" src="assets/pedro/{name}.png" alt=""{hidden}>'
        )
    return f'<div id="av-bob"><div id="av-pulse">{"".join(images)}</div></div>'


def avatar_motion(duration: float, emphasis_times: list[float], moves: list[dict]) -> dict:
    blinks = []
    cursor = 0.55
    slow = False
    while cursor < duration - 0.25:
        blinks.append(round(cursor, 3))
        cursor += 3.15 if slow else 2.35
        slow = not slow
    return {
        "blinks": blinks,
        "lifts": [round(t, 4) for t in emphasis_times if 0 <= t < duration],
        "moves": moves,
        "bob_repeats": max(1, int(duration / 0.9)),
    }
