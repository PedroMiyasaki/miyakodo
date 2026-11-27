"""Valida o roteiro e monta o modelo que o HTML consome.

O campo mode sai do registro em modos/<slug>/MODE.md.
"""

from pipeline.audio import range_duration, remap_time
from pipeline.avatar import avatar_motion
from pipeline.brand import (
    FPS,
    HEIGHT,
    LAYOUT_SPOTS,
    PURPOSES,
    RECORDED_BOXES,
    SCENE_TYPES,
    TONES,
    WIDTH,
)
from pipeline.captions import group_words, sanitize_words, tag_roles, words_from_lines
from pipeline.registry import UnknownMode, require_mode
from pipeline.scenes import build_scene


class ScriptError(ValueError):
    pass


def compile_script(data: dict, cuts=None, mouth=None) -> dict:
    if not isinstance(data, dict):
        raise ScriptError("roteiro precisa ser um objeto")
    try:
        spec = require_mode(data.get("mode"))
    except UnknownMode as exc:
        raise ScriptError(str(exc)) from exc
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

    beats = _normalize_beats(data.get("beats") or [], origin, voice_out, spec)
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

    words = [word for word in words if word["end"] > 0 and word["start"] < duration]
    words = tag_roles(
        sanitize_words(words),
        data.get("emphasis") or [],
        data.get("strong") or [],
        data.get("cta") or [],
    )
    groups = _clamp_groups(group_words(words, spec.slug), duration)
    scenes, ops, sfx = _scenes(beats, spec)
    moves = _avatar_moves(beats, spec, duration)
    emphasis_times = [word["start"] for word in words if word["role"] == "emphasis"]
    motion = avatar_motion(duration, emphasis_times, moves) if spec.avatar else None
    videos = _videos(beats) if spec.footage else []
    return {
        "mode": spec.slug,
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


def _normalize_beats(beats, origin, voice_out, spec):
    if not beats:
        raise ScriptError("beats vazio")
    allowed = spec.layouts
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
        layout = beat.get("layout") or spec.default_layout
        if layout not in allowed:
            raise ScriptError(f"layout {layout} não cabe no modo {spec.slug}")
        scene = beat.get("scene")
        if not scene or scene.get("type") not in SCENE_TYPES:
            raise ScriptError(f"beat {index} sem cena conhecida")
        tone = str(beat.get("tone") or "paper")
        if spec.validate_tone and tone not in TONES:
            raise ScriptError(f"tom {tone} fora da paleta")
        normal.append({
            "id": f"b{index}",
            "start": round(start, 4),
            "end": round(end, 4),
            "layout": layout,
            "tone": tone,
            "label": str(beat.get("label") or scene.get("title") or scene.get("text") or f"{index + 1}"),
            "scene": scene,
            "punch": bool(beat.get("punch", layout == "creator")),
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


def _box_for(spec, layout, index, panel_count):
    if spec.boxes == "faceless":
        return LAYOUT_SPOTS[layout]["scene"]
    return RECORDED_BOXES[layout]


def _scenes(beats, spec):
    html_parts = []
    ops = []
    sfx = []
    for index, beat in enumerate(beats):
        x, y, w, h = _box_for(spec, beat["layout"], index, len(beats))
        piece, piece_ops, piece_sfx = build_scene(
            beat["id"], x, y, w, h, beat["scene"], beat["start"] + 0.08, beat["end"],
        )
        dur = round(beat["end"] - beat["start"], 3)
        if spec.scene_wrapper == "plain":
            html_parts.append(
                f'<section id="beat-{beat["id"]}" class="clip beat" data-start="{beat["start"]}" '
                f'data-duration="{dur}" data-track-index="4">'
                f'{piece}</section>'
            )
        elif spec.scene_wrapper == "wash":
            html_parts.append(
                f'<section id="beat-{beat["id"]}" class="clip beat tone-{beat["tone"]}" '
                f'data-start="{beat["start"]}" data-duration="{dur}" data-track-index="4">'
                f'<div class="wash"></div>'
                f'<div id="beat-{beat["id"]}-in" class="beat-in">{piece}</div>'
                f'</section>'
            )
            ops.append({
                "kind": "fromTo",
                "sel": f'#beat-{beat["id"]}-in',
                "from": {"opacity": 0},
                "to": {"opacity": 1, "duration": 0.16, "ease": "power1.out"},
                "at": beat["start"],
            })
        else:
            raise ScriptError(f"scene_wrapper desconhecido no modo {spec.slug}: {spec.scene_wrapper}")
        ops.extend(piece_ops)
        sfx.extend(piece_sfx)
        if spec.whoosh_on_change and index:
            sfx.append({"name": "whoosh", "at": beat["start"]})
    return "".join(html_parts), ops, sfx


def _avatar_moves(beats, spec, duration):
    if not spec.avatar:
        return []
    anchor_left, anchor_top, anchor_width, _anchor_opacity = LAYOUT_SPOTS["pip"]["avatar"]
    moves = []
    for beat in beats:
        left, top, width, opacity = LAYOUT_SPOTS[beat["layout"]]["avatar"]
        moves.append({
            "at": beat["start"],
            "duration": 0.38 if beat["start"] else 0,
            "x": left - anchor_left,
            "y": top - anchor_top,
            "scale": round(width / anchor_width, 3),
            "opacity": opacity,
        })
    return moves


def _videos(beats):
    videos = []
    for beat in beats:
        if beat["layout"] == "motion":
            continue
        videos.append({
            "id": f'vid-{beat["id"]}',
            "start": beat["start"],
            "duration": round(beat["end"] - beat["start"], 3),
            "media_start": beat["start"],
            "layout": "full" if beat["layout"] == "creator" else "split",
            "punch": beat["punch"] and beat["layout"] == "creator",
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
