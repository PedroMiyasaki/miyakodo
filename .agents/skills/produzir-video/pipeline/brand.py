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
)

# guide: Pedro à esquerda, cena à direita.
# hero e center: frase em cima, busto grande embaixo.
# pip e corner: a cena ocupa o miolo e o busto fica pequeno, acima do rodapé.
# full: a cena toma a área segura e o avatar sai.
# A legenda mora numa faixa própria (CAPTION_TOP até o início da cena).
# Direita livre para os botões do Reels. Rodapé livre para a legenda do post.
CAPTION_TOP = 220
SCENE_TOP = 448
SAFE_RIGHT = 900
SAFE_BOTTOM = 1468
AVATAR_ASPECT = 860 / 720

LAYOUT_SPOTS = {
    "full": {
        "scene": (48, 448, 840, 1000),
        "avatar": (48, 1180, 200, 0),
    },
    "hero": {
        "scene": (48, 448, 840, 220),
        "avatar": (80, 700, 600, 1),
    },
    "center": {
        "scene": (48, 448, 840, 220),
        "avatar": (80, 700, 600, 1),
    },
    "guide": {
        "scene": (400, 448, 488, 1000),
        "avatar": (36, 620, 340, 1),
    },
    "pip": {
        "scene": (48, 448, 840, 720),
        "avatar": (48, 1196, 220, 1),
    },
    "corner": {
        "scene": (48, 448, 840, 720),
        "avatar": (48, 1196, 220, 1),
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
