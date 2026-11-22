#!/usr/bin/env python3
"""Classifica vídeos do repositório em manter, excluir e rever.

Sem --apply, só imprime o relatório. Com --apply, apaga a lista excluir
e os caminhos de rever passados em --incluir. Recusa entrega e ganchos.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
SKIP_DIRS = {"node_modules", ".git", ".venv", "__pycache__"}
SCRAP_DIRS = {"assets", ".media", "renders", ".transcode-cache"}
GENERIC_SLUGS = {
    "input",
    "input-video",
    "video",
    "video-001",
    "overlays",
    "gancho",
    "assets",
    "public",
    "renders",
    "output",
}
MIN_SLUG = 6


@dataclass(frozen=True)
class Item:
    rel: Path
    size: int
    bucket: str
    reason: str


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if (parent / "AGENTS.md").is_file() and (parent / "pyproject.toml").is_file():
            return parent
    raise SystemExit("Não achei a raiz do repositório (AGENTS.md + pyproject.toml).")


def norm(value: str) -> str:
    return value.lower().replace("_", "-").replace(" ", "-")


def norm_path(rel: Path) -> str:
    return "/".join(norm(part) for part in rel.parts)


def is_video(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXT


def is_protected(rel: Path) -> bool:
    parts = rel.parts
    if not parts:
        return True
    if parts[0] in {"posts", ".agents"}:
        return True
    return len(parts) >= 2 and parts[0] == "video" and parts[1] in {"outputs", "hooks"}


def is_delivery_name(rel: Path) -> bool:
    """Arquivo solto em videos/<slug>/, fora de assets, renders e public."""
    parts = rel.parts
    if parts[0] != "videos" or len(parts) != 3:
        return False
    stem = norm(Path(parts[2]).stem)
    return "editado" in stem or stem in {"reels", "video"}


def is_numbered_export(rel: Path) -> bool:
    """output-N.mp4 na raiz de videos/<slug>/. Pode ser versão anterior da entrega."""
    parts = rel.parts
    if parts[0] != "videos" or len(parts) != 3:
        return False
    return parts[2].lower().startswith("output-")


def is_public_input(rel: Path) -> bool:
    parts = rel.parts
    if parts[0] != "videos" or len(parts) < 3 or parts[2] != "public":
        return False
    stem = norm(Path(parts[-1]).stem)
    return stem in {"input", "input-video"} or stem.startswith("input-")


def is_scrap(rel: Path) -> bool:
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "video" and parts[1] == "inputs":
        return True
    if len(parts) >= 4 and parts[0] == "video" and parts[1] == "projects":
        return parts[3] in SCRAP_DIRS
    if parts[0] == "videos" and len(parts) >= 3 and parts[2] in SCRAP_DIRS:
        return True
    if is_public_input(rel):
        return True
    return False


def piece_slug(rel: Path) -> str | None:
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == "video" and parts[1] == "projects":
        return norm(parts[2])
    if len(parts) >= 2 and parts[0] == "videos":
        return norm(parts[1])
    if len(parts) >= 3 and parts[0] == "video" and parts[1] == "inputs":
        if len(parts) == 3:
            return norm(Path(parts[2]).stem)
        return norm(parts[2])
    return None


def iter_videos(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        base = Path(dirpath)
        for name in filenames:
            path = base / name
            if is_video(path):
                yield path


def classify(root: Path) -> list[Item]:
    found: list[tuple[Path, int]] = []
    for path in iter_videos(root):
        rel = path.relative_to(root)
        found.append((rel, path.stat().st_size))

    manter: list[tuple[Path, int]] = []
    pending: list[tuple[Path, int]] = []
    items: list[Item] = []

    for rel, size in found:
        if is_protected(rel) or is_delivery_name(rel):
            manter.append((rel, size))
        elif is_numbered_export(rel):
            items.append(Item(rel, size, "rever", "export numerado na pasta de trabalho"))
        elif is_scrap(rel):
            pending.append((rel, size))
        else:
            items.append(Item(rel, size, "rever", "caminho desconhecido"))

    haystack = [
        norm_path(rel)
        for rel, _size in manter
        if not (len(rel.parts) >= 2 and rel.parts[0] == "video" and rel.parts[1] == "hooks")
    ]

    for rel, size in manter:
        items.append(Item(rel, size, "manter", "entrega"))
    for rel, size in pending:
        slug = piece_slug(rel)
        linked = (
            slug is not None
            and slug not in GENERIC_SLUGS
            and len(slug) >= MIN_SLUG
            and any(slug in path for path in haystack)
        )
        if linked:
            items.append(Item(rel, size, "excluir", "input ou intermediario com entrega"))
        else:
            items.append(Item(rel, size, "rever", "sem entrega associada"))
    return items


def fmt_size(size: int) -> str:
    mb = size / 1048576
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.1f} MB"


def posix(rel: Path) -> str:
    return rel.as_posix()


def print_report(items: list[Item]) -> None:
    order = {"excluir": 0, "rever": 1, "manter": 2}
    for bucket in ("excluir", "rever", "manter"):
        group = [item for item in items if item.bucket == bucket]
        total = sum(item.size for item in group)
        print(f"{bucket}: {len(group)} arquivos, {fmt_size(total)}")
    print()
    for item in sorted(items, key=lambda it: (order[it.bucket], posix(it.rel))):
        line = f"{item.bucket}\t{fmt_size(item.size):>10}\t{posix(item.rel)}"
        if item.bucket == "rever":
            line += f"\t{item.reason}"
        print(line)


def guard(items: list[Item]) -> None:
    blocked = [item for item in items if item.bucket == "excluir" and is_protected(item.rel)]
    if blocked:
        for item in blocked:
            print(f"recusado\t{posix(item.rel)}", file=sys.stderr)
        raise SystemExit(2)


def resolve_in_repo(root: Path, rel: Path) -> Path:
    target = (root / rel).resolve()
    target.relative_to(root.resolve())
    return target


def apply_deletions(root: Path, items: list[Item], extra: list[str]) -> None:
    guard(items)
    by_path = {posix(item.rel): item for item in items}
    chosen = [item for item in items if item.bucket == "excluir"]
    for raw in extra:
        key = Path(raw).as_posix().lstrip("./")
        item = by_path.get(key)
        if item is None or item.bucket != "rever":
            print(f"recusado\t{key}", file=sys.stderr)
            raise SystemExit(2)
        chosen.append(item)

    if not chosen:
        print("Nada a apagar.")
        return

    freed = 0
    for item in chosen:
        target = resolve_in_repo(root, item.rel)
        if is_protected(item.rel) or not is_video(target):
            print(f"recusado\t{posix(item.rel)}", file=sys.stderr)
            raise SystemExit(2)
        target.unlink()
        freed += item.size
        print(f"apagado\t{fmt_size(item.size):>10}\t{posix(item.rel)}")
    print(f"liberado\t{fmt_size(freed)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Classifica vídeos de input e intermediários.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apaga a lista excluir. Sem esta flag, só imprime o relatório.",
    )
    parser.add_argument(
        "--incluir",
        action="append",
        default=[],
        metavar="CAMINHO",
        help="Caminho hoje em rever, apagado junto com excluir. Exige --apply.",
    )
    args = parser.parse_args()
    if args.incluir and not args.apply:
        raise SystemExit("--incluir só vale com --apply.")

    root = repo_root()
    items = classify(root)
    guard(items)
    if not args.apply:
        print_report(items)
        return
    apply_deletions(root, items, args.incluir)


if __name__ == "__main__":
    main()
