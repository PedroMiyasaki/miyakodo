"""Zonas do modo gravação. Legenda, cena e rosto não se cruzam.

O PiP fica no canto superior esquerdo, abaixo do topo do Reels.
A legenda é uma faixa fixa em y 1340–1460, acima dos 450 px de rodapé
e longe da coluna de botões. O desenho para em y 1300.
"""

from pipeline.brand import HEIGHT, LAYOUTS_RECORDED, WIDTH


IG_TOP = 150
IG_BOTTOM = 450
IG_RIGHT = 150
GAP = 24
SCENE_BOTTOM = 1300

SAFE_RIGHT = WIDTH - IG_RIGHT
SAFE_BOTTOM = HEIGHT - IG_BOTTOM


class Rect:
    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

    def box(self):
        return (self.x, self.y, self.w, self.h)


def overlaps(a, b, gap=0):
    return not (
        a.right + gap <= b.x
        or b.right + gap <= a.x
        or a.bottom + gap <= b.y
        or b.bottom + gap <= a.y
    )


def _zone(scene, caption, face=None, video=None, host="full", object_position="center 32%", cover=False):
    return {
        "scene": scene,
        "caption": caption,
        "face": face,
        "video": video,
        "host": host,
        "object_position": object_position,
        "cover": cover,
    }


# Uma faixa só de legenda, em todos os layouts.
CAPTION = Rect(64, 1340, 820, 120)

LAYOUT_ZONES = {
    "pip": _zone(
        scene=Rect(48, 524, 876, 756),
        caption=CAPTION,
        face=Rect(52, 160, 360, 340),
        video=Rect(52, 160, 360, 340),
        host="pip",
        object_position="center 23%",
    ),
    "motion": _zone(
        scene=Rect(48, 168, 876, 1112),
        caption=CAPTION,
        face=None,
        video=None,
        host="full",
    ),
    "split": _zone(
        scene=Rect(48, 156, 876, 420),
        caption=CAPTION,
        face=Rect(0, 596, WIDTH, 640),
        video=Rect(0, 596, WIDTH, 640),
        host="split",
        object_position="center 40%",
    ),
    "creator": _zone(
        scene=Rect(64, 248, 852, 176),
        caption=CAPTION,
        face=Rect(140, 460, 800, 760),
        video=Rect(0, 0, WIDTH, HEIGHT),
        host="full",
        object_position="center 46%",
        cover=True,
    ),
    "zoom": _zone(
        scene=Rect(64, 248, 852, 176),
        caption=CAPTION,
        face=Rect(140, 460, 800, 760),
        video=Rect(0, 0, WIDTH, HEIGHT),
        host="full",
        object_position="center 42%",
        cover=True,
    ),
}

# Placa opaca nos layouts de tela cheia quando o bruto já tem legenda queimada.
# A legenda antiga chega perto de 78% da altura. A placa vai até y 1544
# para não sobrar ponta de letra, e deixa 376 px livres no rodapé.
BURN_PLATE = Rect(28, 1248, 1024, 296)


class ZoneError(ValueError):
    pass


def zones(layout):
    found = LAYOUT_ZONES.get(layout)
    if found is None:
        raise ZoneError(f"layout sem zona: {layout}")
    return found


def _inside_text(rect, what):
    if rect.x < 40:
        raise ZoneError(f"{what} entra na borda esquerda")
    if rect.y < IG_TOP:
        raise ZoneError(f"{what} entra no topo do Reels")
    if rect.right > SAFE_RIGHT:
        raise ZoneError(f"{what} entra na coluna de botões")
    if rect.bottom > SAFE_BOTTOM:
        raise ZoneError(f"{what} entra no rodapé da legenda do post")


def validate_zones():
    if set(LAYOUT_ZONES) != set(LAYOUTS_RECORDED):
        raise ZoneError("zonas e layouts de gravação divergem")
    for name, zone in LAYOUT_ZONES.items():
        scene, caption, face = zone["scene"], zone["caption"], zone["face"]
        _inside_text(scene, f"{name} cena")
        _inside_text(caption, f"{name} legenda")
        if scene.bottom > SCENE_BOTTOM:
            raise ZoneError(f"{name}: cena passa de y {SCENE_BOTTOM}")
        if caption.y < 1340 or caption.bottom > 1460:
            raise ZoneError(f"{name}: legenda fora da faixa 1340–1460")
        if overlaps(scene, caption, GAP - 4):
            raise ZoneError(f"{name}: cena e legenda se cruzam")
        if face is not None:
            if overlaps(face, caption, GAP - 4):
                raise ZoneError(f"{name}: rosto e legenda se cruzam")
            if overlaps(face, scene, 12):
                raise ZoneError(f"{name}: rosto e cena se cruzam")
        video = zone["video"]
        if name == "pip":
            if video.y < 150 or video.bottom > 520:
                raise ZoneError("pip fora do canto superior esquerdo")
            if video.x > 80:
                raise ZoneError("pip não está na esquerda")
        if video is not None and name == "split":
            if video.h < 600:
                raise ZoneError("split: faixa do rosto baixa demais")
            if video.bottom > SCENE_BOTTOM:
                raise ZoneError("split: rosto entra na faixa da legenda")
        plate = BURN_PLATE
        if zone["cover"]:
            if plate.bottom > 1560:
                raise ZoneError(f"{name}: placa da legenda desce demais")
            if face is not None and overlaps(face, plate, GAP - 4):
                raise ZoneError(f"{name}: placa cobre o rosto")
    return True
