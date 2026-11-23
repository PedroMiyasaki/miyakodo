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
    "hero",
    "reveal",
    "mascot",
    "stack",
)

# Carlos, o público. PNGs de design/mascote-e-textura/, copiados para assets/.
MASCOT_FILES = {
    "agachado": "carlos-agachado.png",
    "chefe": "carlos-chefe.png",
    "dinheiro": "carlos-dinheiro.png",
    "cafe": "carlos-cafe.png",
    "estrelas": "carlos-estrelas.png",
}

MASCOT_SOURCES = {
    "carlos-agachado.png": "design/mascote-e-textura/png/MASCOTE_1.png",
    "carlos-chefe.png": "design/mascote-e-textura/png/MASCOTE_2.png",
    "carlos-dinheiro.png": "design/mascote-e-textura/png/MASCOTE_3.png",
    "carlos-cafe.png": "design/mascote-e-textura/png/MASCOTE_4.png",
    "carlos-estrelas.png": "design/mascote-e-textura/png/MASCOTE_5.png",
}

LAYOUTS_FACELESS = ("guide", "center", "corner")
LAYOUTS_RECORDED = ("pip", "split", "motion", "creator", "zoom")

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
