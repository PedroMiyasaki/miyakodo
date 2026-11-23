"""Valida o roteiro e monta o modelo que o HTML consome."""

from pipeline.audio import range_duration, remap_time
from pipeline.avatar import avatar_motion
from pipeline.brand import (
    FPS,
    HEIGHT,
    LAYOUTS_FACELESS,
    LAYOUTS_RECORDED,
    MODES,
    PURPOSES,
    SCENE_TYPES,
    WIDTH,
)
from pipeline.captions import group_words, sanitize_words, tag_roles, words_from_lines
from pipeline.scenes import build_scene
from pipeline.zones import validate_zones, zones


class ScriptError(ValueError):
    pass


def compile_script(data: dict, cuts=None, mouth=None) -> dict:
    if not isinstance(data, dict):
        raise ScriptError("roteiro precisa ser um objeto")
    mode = data.get("mode")
    if mode not in MODES:
        raise ScriptError(f"mode inválido: {mode}")
    purpose = data.get("purpose")
    if purpose is not None and purpose not in PURPOSES:
        raise ScriptError(f"purpose inválido: {purpose}")
    voice = data.get("voice") or {}
    try:
        origin = float(voice.get("in", 0))
        voice_out = float(voice.get("out"))
    except (TypeError, ValueError) as exc:
        raise ScriptError("voice.in e voice.out são obrigatórios") from exc
    if voice_out <= origin:
        raise ScriptError("voice.out precisa ser maior que voice.in")

    beats = _normalize_beats(data.get("beats") or [], origin, voice_out, mode)
    words = _collect_words(data, beats, origin)
    if cuts:
        words = _remap_words(words, cuts)
        beats = _remap_beats(beats, cuts)
        duration = range_duration(cuts)
    else:
        duration = round(voice_out - origin, 4)
    if duration <= 0.2:
        raise ScriptError("duração curta demais depois dos cortes")
    beats = _extend_beats(beats, duration)
    if not beats:
        raise ScriptError("nenhum beat sobreviveu aos cortes")

    if mode == "gravacao":
        validate_zones()
    words = [word for word in words if word["end"] > 0 and word["start"] < duration]
    words = tag_roles(
        sanitize_words(words),
        data.get("emphasis") or [],
        data.get("strong") or [],
        data.get("cta") or [],
    )
    groups = _clamp_groups(group_words(words, mode), duration)
    if mode == "gravacao":
        groups = _split_groups_on_beats(groups, beats)
    scenes, ops, sfx = _scenes(beats, mode)
    moves = _avatar_moves(beats, mode, duration)
    emphasis_times = [word["start"] for word in words if word["role"] == "emphasis"]
    motion = avatar_motion(duration, emphasis_times, moves) if mode == "sem-gravacao" else None
    videos = _videos(beats) if mode == "gravacao" else []
    return {
        "mode": mode,
        "slug": _slug(data.get("slug") or "reel"),
        "title": str(data.get("title") or data.get("slug") or "reel"),
        "purpose": purpose,
        "fps": int(data.get("fps") or FPS),
        "width": WIDTH,
        "height": HEIGHT,
        "duration": round(duration, 3),
        "beats": beats,
        "groups": groups,
        "scenes_html": scenes,
        "ops": ops,
        "sfx": _cap_sfx(sfx, duration),
        "videos": videos,
        "avatar": motion,
        "mouth": mouth or [],
        "mouth_hz": 40,
        "voice_src": voice.get("src"),
        "footage": data.get("footage") or {},
        "burned_captions": bool((data.get("footage") or {}).get("burnedCaptions")),
    }


def _clamp_groups(groups, duration):
    clamped = []
    for group in groups:
        if group["start"] >= duration - 0.04:
            continue
        group["end"] = round(min(group["end"], duration), 4)
        if group["end"] - group["start"] < 0.08:
            group["end"] = round(min(duration, group["start"] + 0.08), 4)
        for word in group["words"]:
            word["start"] = round(min(word["start"], duration - 0.05), 4)
            word["end"] = round(min(max(word["end"], word["start"] + 0.05), duration), 4)
        clamped.append(group)
    return clamped


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in str(value)).strip("-")
    return cleaned or "reel"


def _normalize_beats(beats, origin, voice_out, mode):
    if not beats:
        raise ScriptError("beats vazio")
    allowed = LAYOUTS_FACELESS if mode == "sem-gravacao" else LAYOUTS_RECORDED
    normal = []
    for index, beat in enumerate(beats):
        try:
            start = float(beat["start"]) - origin
            end = float(beat["end"]) - origin
        except (KeyError, TypeError, ValueError) as exc:
            raise ScriptError(f"beat {index} sem start/end") from exc
        start = max(0.0, start)
        end = min(voice_out - origin, end)
        if end - start < 0.15:
            continue
        layout = beat.get("layout") or ("guide" if mode == "sem-gravacao" else "split")
        if layout not in allowed:
            raise ScriptError(f"layout {layout} não cabe no modo {mode}")
        scene = beat.get("scene")
        if not scene or scene.get("type") not in SCENE_TYPES:
            raise ScriptError(f"beat {index} sem cena conhecida")
        normal.append({
            "id": f"b{index}",
            "start": round(start, 4),
            "end": round(end, 4),
            "layout": layout,
            "label": str(beat.get("label") or scene.get("title") or f"{index + 1}"),
            "scene": scene,
            "punch": bool(beat.get("punch", layout in {"creator", "zoom"})),
        })
    if len(normal) < 1:
        raise ScriptError("beats fora da janela da voz")
    normal.sort(key=lambda item: item["start"])
    for prev, nxt in zip(normal, normal[1:]):
        if nxt["start"] < prev["end"] - 0.05:
            raise ScriptError("beats sobrepostos")
    return normal


def _collect_words(data, beats, origin):
    raw = data.get("words")
    if raw:
        shifted = []
        for word in raw:
            shifted.append({
                **word,
                "start": float(word["start"]) - origin,
                "end": float(word.get("end", word["start"])) - origin,
            })
        return sanitize_words(shifted)
    source_beats = []
    for beat in data.get("beats") or []:
        source_beats.append({
            "start": float(beat["start"]) - origin,
            "end": float(beat["end"]) - origin,
            "lines": beat.get("lines") or [],
        })
    return sanitize_words(words_from_lines(source_beats))


def _remap_words(words, cuts):
    remapped = []
    for word in words:
        start = remap_time(word["start"], cuts)
        end = remap_time(word["end"], cuts)
        if end <= start:
            end = start + 0.08
        remapped.append({**word, "start": start, "end": end})
    return sanitize_words(remapped)


def _remap_beats(beats, cuts):
    remapped = []
    for beat in beats:
        start = remap_time(beat["start"], cuts)
        end = remap_time(beat["end"], cuts)
        if end - start < 0.2:
            continue
        remapped.append({**beat, "start": round(start, 4), "end": round(end, 4)})
    return remapped


def _extend_beats(beats, duration):
    if not beats:
        return beats
    ordered = sorted(beats, key=lambda beat: beat["start"])
    for prev, nxt in zip(ordered, ordered[1:]):
        prev["end"] = round(nxt["start"], 4)
    ordered[-1]["end"] = round(duration, 4)
    ordered[0]["start"] = 0.0
    return ordered


def _box_for(mode, layout, index, panel_count):
    if mode == "sem-gravacao":
        base = index * 1920
        if layout == "center":
            return (150, base + 280, 780, 620)
        return (170, base + 300, 860, 980)
    if layout == "split":
        return (64, 110, 952, 820)
    if layout == "creator":
        return (120, 1460, 840, 220)
    return (64, 160, 952, 1480)


def _split_groups_on_beats(groups, beats):
    """Uma legenda não atravessa a troca de layout. A faixa muda com a cena."""
    bounds = [beat["start"] for beat in beats[1:]]
    pieces = []
    for group in groups:
        current = []
        for word in group["words"]:
            if current and any(current[-1]["start"] < bound <= word["start"] + 0.02 for bound in bounds):
                pieces.append(current)
                current = []
            current.append(word)
        if current:
            pieces.append(current)
    packed = []
    for index, words in enumerate(pieces):
        start = words[0]["start"]
        end = words[-1]["end"]
        if index + 1 < len(pieces):
            nxt = pieces[index + 1][0]["start"]
            if nxt - end < 0.12:
                end = nxt
        end = max(end, start + 0.12)
        packed.append({
            "id": f"cap-{index}",
            "start": round(start, 4),
            "end": round(end, 4),
            "words": [{**word, "id": f"cap-{index}-w-{wi}"} for wi, word in enumerate(words)],
        })
    return packed


def _scenes(beats, mode):
    html_parts = []
    ops = []
    sfx = []
    for index, beat in enumerate(beats):
        if mode == "gravacao":
            box = zones(beat["layout"])["scene"]
            pad = 16
            x, y, w, h = pad, pad, box.w - pad * 2, box.h - pad * 2
        else:
            box = None
            x, y, w, h = _box_for(mode, beat["layout"], index, len(beats))
        piece, piece_ops, piece_sfx = build_scene(
            beat["id"], x, y, w, h, beat["scene"], beat["start"] + 0.08, beat["end"],
        )
        if mode == "gravacao":
            html_parts.append(
                f'<section id="beat-{beat["id"]}" class="clip beat" data-start="{beat["start"]}" '
                f'data-duration="{round(beat["end"] - beat["start"], 3)}" data-track-index="4" '
                f'style="left:{box.x}px;top:{box.y}px;width:{box.w}px;height:{box.h}px">'
                f'{piece}</section>'
            )
        else:
            html_parts.append(piece)
        ops.extend(piece_ops)
        sfx.extend(piece_sfx)
        if mode == "gravacao" and index and beat["layout"] != beats[index - 1]["layout"]:
            sfx.append({"name": "whoosh", "at": beat["start"]})
    if mode == "sem-gravacao":
        html_parts.append(_rail(beats))
        ops.extend(_camera(beats))
    return "".join(html_parts), ops, sfx


def _rail(beats):
    height = len(beats) * 1920
    nodes = []
    for index, beat in enumerate(beats):
        top = index * 1920 + 860
        nodes.append(
            f'<div id="rail-{beat["id"]}" class="rail-node" style="top:{top}px">'
            f'<span>{index + 1}</span><b>{_escape(beat["label"])}</b></div>'
        )
    return (
        f'<div class="rail" data-layout-allow-overflow="true" style="height:{height}px"></div>'
        + "".join(nodes)
    )


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _camera(beats):
    ops = []
    for index, beat in enumerate(beats):
        if index == 0:
            continue
        ops.append({
            "kind": "to",
            "sel": "#world",
            "vars": {"y": -index * 1920, "duration": 0.62, "ease": "power2.inOut"},
            "at": beat["start"],
        })
        ops.append({
            "kind": "fromTo",
            "sel": f'#rail-{beat["id"]}',
            "from": {"scale": 0.4, "opacity": 0},
            "to": {"scale": 1, "opacity": 1, "duration": 0.35, "ease": "back.out(1.6)"},
            "at": round(beat["start"] + 0.1, 4),
        })
    if len(beats) > 1:
        zoom_at = max(0.2, beats[-1]["end"] - 1.25)
        ops.append({
            "kind": "to",
            "sel": "#world",
            "vars": {
                "y": 0,
                "scale": round(1 / len(beats), 4),
                "duration": 1.05,
                "ease": "power3.inOut",
                "transformOrigin": "50% 0%",
            },
            "at": round(zoom_at, 4),
        })
    return ops


def _avatar_moves(beats, mode, duration):
    if mode != "sem-gravacao":
        return []
    anchor_left, anchor_top, anchor_width = 36, 1460, 280
    spots = {
        "guide": (36, 1460, 280),
        "corner": (36, 1460, 250),
        "center": (250, 980, 520),
    }
    moves = []
    for beat in beats:
        left, top, width = spots[beat["layout"]]
        moves.append({
            "at": beat["start"],
            "duration": 0.45,
            "x": left - anchor_left,
            "y": top - anchor_top,
            "scale": round(width / anchor_width, 3),
        })
    if len(beats) > 1:
        moves.append({
            "at": round(max(0.2, duration - 1.25), 4),
            "duration": 0.5,
            "x": 760 - anchor_left,
            "y": 1560 - anchor_top,
            "scale": round(220 / anchor_width, 3),
        })
    return moves


def _videos(beats):
    videos = []
    for beat in beats:
        zone = zones(beat["layout"])
        if zone["video"] is None:
            continue
        videos.append({
            "id": f'vid-{beat["id"]}',
            "start": beat["start"],
            "duration": round(beat["end"] - beat["start"], 3),
            "media_start": beat["start"],
            "layout": beat["layout"],
            "host": zone["host"],
            "box": zone["video"].box(),
            "object_position": zone["object_position"],
            "punch": bool(beat["punch"]) and beat["layout"] in {"creator", "zoom"},
            "punch_scale": 1.14 if beat["layout"] == "zoom" else 1.08,
        })
    return videos


def _cap_sfx(events, duration=30, limit=None):
    if limit is None:
        limit = max(28, min(80, int(float(duration) / 2)))
    cleaned = []
    seen = set()
    for event in sorted(events, key=lambda item: (item["at"], item["name"])):
        key = (event["name"], round(float(event["at"]), 2))
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"name": event["name"], "at": round(float(event["at"]), 3)})
    return cleaned[:limit]
