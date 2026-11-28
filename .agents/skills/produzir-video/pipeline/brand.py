"""Paleta e tipos da identidade Miyakodo. Ver design/identity.md."""

OFFWHITE = "#f6f4ee"
CINZA = "#aba199"
MUTED = "#5e564f"
BROWN = "#280e03"
VERDE = "#1a3010"
AZUL = "#b6cadb"
OLIVA = "#c1c167"
ROSA = "#d39ca7"
LARANJA = "#db3c05"
PAPER = "#fffcf6"

WIDTH = 1080
HEIGHT = 1920
FPS = 30

PURPOSES = ("tutorial", "opiniao", "noticia", "lista", "historia", "cta")
MODES = ("sem-gravacao", "gravacao")

SCENE_TYPES = (
    "timeline",
    "mockup",
    "counter",
    "diagram",
    "chat",
    "code",
    "phone",
    "grid",
    "scanline",
    "folders",
    "bullets",
    "quote",
    "badge",
    "stack",
    "statement",
    "carlos",
    "versus",
    "peel",
    "flow",
    "chart",
    "clutter",
    "maze",
    "close",
)

# Palco termina em 63% (y=1210), acima da legenda (67%).
# Direita livre: 140px. PiP fica no topo esquerdo.
CAPTION_TOP = 1288
SCENE_TOP = 128
SAFE_RIGHT = 940
SAFE_BOTTOM = 1210
AVATAR_ASPECT = 404 / 217

LAYOUT_SPOTS = {
    "full": {
        "scene": (40, 128, 880, 1082),
        "avatar": (40, 211, 180, 0),
    },
    "hero": {
        "scene": (40, 128, 880, 400),
        "avatar": (280, 560, 320, 1),
    },
    "center": {
        "scene": (40, 128, 880, 400),
        "avatar": (280, 560, 320, 1),
    },
    "guide": {
        "scene": (320, 128, 600, 1082),
        "avatar": (32, 180, 260, 1),
    },
    "pip": {
        "scene": (248, 128, 672, 1082),
        "avatar": (40, 211, 180, 1),
    },
    "corner": {
        "scene": (248, 128, 672, 1082),
        "avatar": (40, 211, 180, 1),
    },
}

TONES = ("paper", "ink", "verde", "azul", "rosa", "oliva")

LAYOUTS_FACELESS = ("guide", "center", "corner", "hero", "pip", "full")
LAYOUTS_RECORDED = ("split", "motion", "creator")

SFX_FILES = {
    "pop": "pop.mp3",
    "whoosh": "whoosh-short.mp3",
    "click": "click.mp3",
    "typing": "typing.mp3",
    "notification": "notification.mp3",
    "chime": "chime.mp3",
    "impact": "impact-bass-1.mp3",
    "key": "key-press.mp3",
}
