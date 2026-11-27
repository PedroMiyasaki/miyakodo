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
# Modos ficam em modos/<slug>/MODE.md. pipeline/registry.py é quem valida o slug.

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
    "vidro",
    "alca",
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

# Caixas do talking head. split: pessoa embaixo. creator: faixa do CTA. motion: quadro cheio.
RECORDED_BOXES = {
    "split": (64, 110, 952, 820),
    "creator": (120, 1460, 840, 220),
    "motion": (64, 160, 952, 1480),
}

# jason-cooperson. painel: card em cima, avatar com a cabeça vazando do poço.
# full: motion sem avatar. hero: opinião e CTA, busto grande.
# A âncora do movimento continua o pip de LAYOUT_SPOTS (left 48, top 1196, width 220).
STUDIO_SPOTS = {
    "painel": {
        "scene": (72, 236, 800, 440),
        "avatar": (300, 920, 440, 1),
        "well": (160, 1080, 700, 340),
    },
    "full": {
        "scene": (72, 220, 800, 860),
        "avatar": (48, 1180, 200, 0),
    },
    "hero": {
        "scene": (48, 448, 840, 220),
        "avatar": (80, 700, 600, 1),
    },
}

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
