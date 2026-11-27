"""Registro dos modos de vídeo.

Cada pasta em modos/<slug>/ com MODE.md é um modo. cli.py e compile.py
leem este módulo para validar e despachar o campo mode do roteiro.
"""

from dataclasses import dataclass
from pathlib import Path

from pipeline.brand import LAYOUT_SPOTS, RECORDED_BOXES, STUDIO_SPOTS


class RegistryError(ValueError):
    pass


class UnknownMode(RegistryError):
    pass


_ROOT = Path(__file__).resolve().parents[1] / "modos"

CAPTION_CSS = {"faixa": "face", "gravada": "grav", "duas-vozes": "duo"}
MEDIA_VALUES = ("voz", "bruto")
WRAPPERS = ("wash", "plain")
BOX_CATALOGS = ("faceless", "recorded", "studio")
ANCHORS = ("faixa", "layout")

_FIELDS = (
    "slug",
    "layouts",
    "default_layout",
    "validate_tone",
    "caption_profile",
    "caption_max_words",
    "caption_max_chars",
    "caption_max_duration",
    "caption_merge_orphans",
    "caption_anchor",
    "media",
    "whoosh_on_change",
    "avatar",
    "grain",
    "scene_wrapper",
    "boxes",
)

_HEADINGS = (
    "## Quando usar",
    "## Entradas",
    "## Layouts",
    "## Legenda",
    "## Ritmo de corte",
    "## Motion",
    "## O que reaproveita",
)


@dataclass(frozen=True)
class Mode:
    slug: str
    layouts: tuple[str, ...]
    default_layout: str
    validate_tone: bool
    caption_profile: str
    caption_max_words: int
    caption_max_chars: int
    caption_max_duration: float
    caption_merge_orphans: bool
    caption_anchor: str
    caption_top: int | None
    caption_tops: dict[str, int]
    media: str
    whoosh_on_change: bool
    avatar: bool
    grain: bool
    scene_wrapper: str
    boxes: str
    path: Path

    @property
    def caption_css(self) -> str:
        return CAPTION_CSS[self.caption_profile]

    @property
    def footage(self) -> bool:
        return self.media == "bruto"

    @property
    def remove_silence(self) -> bool:
        return self.media == "bruto"

    def top_for(self, layout: str) -> int:
        if self.caption_anchor == "faixa":
            return int(self.caption_top)
        return self.caption_tops[layout]


def load_modes(root: Path | None = None) -> dict[str, Mode]:
    base = root or _ROOT
    if not base.is_dir():
        raise RegistryError(f"registro de modos não encontrado: {base}")
    found: dict[str, Mode] = {}
    for folder in sorted(path for path in base.iterdir() if path.is_dir()):
        if folder.name.startswith("."):
            continue
        doc = folder / "MODE.md"
        if not doc.is_file():
            raise RegistryError(f"{folder.relative_to(base.parent)} está sem MODE.md")
        mode = _load_mode(doc, folder.name)
        if mode.slug in found:
            raise RegistryError(f"slug repetido: {mode.slug}")
        found[mode.slug] = mode
    if not found:
        raise RegistryError(f"nenhum modo em {base}")
    return found


def require_mode(slug) -> Mode:
    modes = load_modes()
    if isinstance(slug, str) and slug in modes:
        return modes[slug]
    known = ", ".join(sorted(modes))
    if slug is None or slug == "":
        shown = "ausente"
    elif isinstance(slug, str):
        shown = slug
    else:
        shown = repr(slug)
    raise UnknownMode(f"modo desconhecido: {shown}. Modos registrados: {known}.")


def _load_mode(doc: Path, folder: str) -> Mode:
    text = doc.read_text(encoding="utf-8")
    raw, body = _split_frontmatter(text, doc)
    for heading in _HEADINGS:
        if heading not in body:
            raise RegistryError(f"{_where(doc)}: falta a seção {heading}")
    data = _parse_block(raw, doc)
    unknown = sorted(set(data) - set(_FIELDS) - {"caption_top", "caption_tops"})
    if unknown:
        raise RegistryError(f"{_where(doc)}: campo desconhecido: {', '.join(unknown)}")
    for key in _FIELDS:
        if key not in data:
            raise RegistryError(f"{_where(doc)}: falta {key}")

    slug = _as_str(data["slug"], doc, "slug")
    if slug != folder:
        raise RegistryError(f"{_where(doc)}: slug {slug} não bate com a pasta {folder}")
    layouts = _as_str_tuple(data["layouts"], doc, "layouts")
    if len(layouts) != len(set(layouts)):
        raise RegistryError(f"{_where(doc)}: layouts repetidos")
    default_layout = _as_str(data["default_layout"], doc, "default_layout")
    if default_layout not in layouts:
        raise RegistryError(f"{_where(doc)}: default_layout {default_layout} fora de layouts")

    profile = _as_choice(data["caption_profile"], CAPTION_CSS, doc, "caption_profile")
    anchor = _as_choice(data["caption_anchor"], ANCHORS, doc, "caption_anchor")
    boxes = _as_choice(data["boxes"], BOX_CATALOGS, doc, "boxes")
    _check_layouts(doc, boxes, layouts)
    caption_top, caption_tops = _caption_position(doc, data, anchor, layouts)

    return Mode(
        slug=slug,
        layouts=layouts,
        default_layout=default_layout,
        validate_tone=_as_bool(data["validate_tone"], doc, "validate_tone"),
        caption_profile=profile,
        caption_max_words=_as_int(data["caption_max_words"], doc, "caption_max_words"),
        caption_max_chars=_as_int(data["caption_max_chars"], doc, "caption_max_chars"),
        caption_max_duration=_as_float(data["caption_max_duration"], doc, "caption_max_duration"),
        caption_merge_orphans=_as_bool(data["caption_merge_orphans"], doc, "caption_merge_orphans"),
        caption_anchor=anchor,
        caption_top=caption_top,
        caption_tops=caption_tops,
        media=_as_choice(data["media"], MEDIA_VALUES, doc, "media"),
        whoosh_on_change=_as_bool(data["whoosh_on_change"], doc, "whoosh_on_change"),
        avatar=_as_bool(data["avatar"], doc, "avatar"),
        grain=_as_bool(data["grain"], doc, "grain"),
        scene_wrapper=_as_choice(data["scene_wrapper"], WRAPPERS, doc, "scene_wrapper"),
        boxes=boxes,
        path=doc,
    )


def _check_layouts(doc: Path, boxes: str, layouts: tuple[str, ...]) -> None:
    if boxes == "faceless":
        catalog = LAYOUT_SPOTS
    elif boxes == "studio":
        catalog = STUDIO_SPOTS
    else:
        catalog = RECORDED_BOXES
    missing = [name for name in layouts if name not in catalog]
    if missing:
        raise RegistryError(
            f"{_where(doc)}: layout sem caixa em {boxes}: {', '.join(missing)}"
        )


def _caption_position(doc, data, anchor, layouts):
    if anchor == "faixa":
        if "caption_tops" in data:
            raise RegistryError(f"{_where(doc)}: caption_anchor faixa não usa caption_tops")
        if "caption_top" not in data:
            raise RegistryError(f"{_where(doc)}: falta caption_top")
        return _as_int(data["caption_top"], doc, "caption_top"), {}
    if "caption_top" in data:
        raise RegistryError(f"{_where(doc)}: caption_anchor layout não usa caption_top")
    tops = data.get("caption_tops")
    if not isinstance(tops, dict) or not tops:
        raise RegistryError(f"{_where(doc)}: falta caption_tops")
    cleaned = {
        _as_str(key, doc, "caption_tops"): _as_int(value, doc, f"caption_tops.{key}")
        for key, value in tops.items()
    }
    if set(cleaned) != set(layouts):
        raise RegistryError(f"{_where(doc)}: caption_tops tem de cobrir os layouts do modo")
    return None, cleaned


def _split_frontmatter(text: str, doc: Path) -> tuple[list[str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise RegistryError(f"{_where(doc)}: sem frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    raise RegistryError(f"{_where(doc)}: frontmatter sem fecho")


def _parse_block(lines: list[str], doc: Path) -> dict:
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]

    def parent():
        return stack[-1][1]

    index = 0
    while index < len(lines):
        raw = lines[index]
        index += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        container = parent()
        if line.startswith("- "):
            if not isinstance(container, list):
                raise RegistryError(f"{_where(doc)}: item fora de lista: {line}")
            container.append(_scalar(line[2:].strip()))
            continue
        key, sep, rest = line.partition(":")
        if not sep or not key.strip():
            raise RegistryError(f"{_where(doc)}: linha sem chave: {line}")
        key = key.strip()
        rest = rest.strip()
        if not isinstance(container, dict):
            raise RegistryError(f"{_where(doc)}: chave fora de mapa: {key}")
        if rest == "":
            nxt = _next_content(lines, index)
            child: object = [] if nxt is not None and nxt.strip().startswith("- ") else {}
            container[key] = child
            stack.append((indent, child))
            continue
        container[key] = _scalar(rest)
    return root


def _next_content(lines: list[str], start: int) -> str | None:
    for line in lines[start:]:
        if line.strip() and not line.lstrip().startswith("#"):
            return line
    return None


def _scalar(token: str):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in {'"', "'"}:
        return token[1:-1]
    if token == "true":
        return True
    if token == "false":
        return False
    if token == "null":
        return None
    if _is_int(token):
        return int(token)
    if _is_float(token):
        return float(token)
    return token


def _is_int(token: str) -> bool:
    if token.startswith("-"):
        token = token[1:]
    return token.isdigit()


def _is_float(token: str) -> bool:
    left, dot, right = token.partition(".")
    return bool(dot) and _is_int(left or "0") and right.isdigit()


def _where(doc: Path) -> str:
    return doc.as_posix()


def _as_str(value, doc: Path, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(f"{_where(doc)}: {label} precisa ser texto")
    return value.strip()


def _as_str_tuple(value, doc: Path, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise RegistryError(f"{_where(doc)}: {label} precisa ser uma lista")
    return tuple(_as_str(item, doc, label) for item in value)


def _as_bool(value, doc: Path, label: str) -> bool:
    if not isinstance(value, bool):
        raise RegistryError(f"{_where(doc)}: {label} precisa ser true ou false")
    return value


def _as_int(value, doc: Path, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RegistryError(f"{_where(doc)}: {label} precisa ser inteiro")
    return value


def _as_float(value, doc: Path, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RegistryError(f"{_where(doc)}: {label} precisa ser número")
    return float(value)


def _as_choice(value, allowed, doc: Path, label: str) -> str:
    text = _as_str(value, doc, label)
    choices = allowed.keys() if isinstance(allowed, dict) else allowed
    if text not in choices:
        joined = ", ".join(choices)
        raise RegistryError(f"{_where(doc)}: {label} {text} fora de {joined}")
    return text
