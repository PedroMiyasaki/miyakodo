"""Avatar do Pedro no modo sem gravação.

O desenho está em assets/pedro.svg: o mesmo sistema do mascote Carlos
(contorno dark brown, chapado, grão de papel, paleta de design/identity.md),
com o rosto do Pedro no vídeo headless (cabelo escuro com mecha clara,
sobrancelha grossa, barba curta, pinta, camiseta e lapela).
Carlos continua sendo o público, não o apresentador.
"""

from pathlib import Path


def avatar_svg() -> str:
    path = Path(__file__).resolve().parents[1] / "assets" / "pedro.svg"
    return path.read_text(encoding="utf-8").strip()


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
