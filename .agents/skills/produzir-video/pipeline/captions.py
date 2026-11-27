"""Agrupa palavras faladas no perfil de legenda do modo registrado."""

from pipeline.registry import require_mode


def normalize_token(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum())


def sanitize_words(words: list[dict]) -> list[dict]:
    ordered = sorted(words, key=lambda w: (float(w["start"]), float(w.get("end", w["start"]))))
    clean = []
    last_end = -1.0
    for word in ordered:
        text = str(word.get("text", "")).strip()
        if not text:
            continue
        start = float(word["start"])
        end = float(word.get("end", start))
        if end <= start:
            end = start + 0.08
        if start < last_end:
            start = last_end
            if end <= start:
                end = start + 0.08
        clean.append({**word, "text": text, "start": round(start, 4), "end": round(end, 4)})
        last_end = end
    return clean


def tag_roles(words: list[dict], emphasis=(), strong=(), cta=()) -> list[dict]:
    emphasis = {normalize_token(item) for item in emphasis}
    strong = {normalize_token(item) for item in strong}
    cta = {normalize_token(item) for item in cta}
    tagged = []
    for word in words:
        key = normalize_token(word["text"])
        role = word.get("role") or "normal"
        if key in cta:
            role = "cta"
        elif key in strong:
            role = "strong"
        elif key in emphasis:
            role = "emphasis"
        tagged.append({**word, "role": role})
    return tagged


def _flush(groups: list[list[dict]], current: list[dict]) -> None:
    if current:
        groups.append(list(current))
        current.clear()


def group_words(words: list[dict], mode: str) -> list[dict]:
    spec = require_mode(mode)
    max_n = spec.caption_max_words
    max_chars = spec.caption_max_chars
    max_dur = spec.caption_max_duration
    groups: list[list[dict]] = []
    current: list[dict] = []
    for word in words:
        if not current:
            current.append(word)
            continue
        gap = word["start"] - current[-1]["end"]
        joined = " ".join(item["text"] for item in current + [word])
        dur = word["end"] - current[0]["start"]
        ended = current[-1]["text"][-1] in ".?!"
        too_big = len(current) >= max_n or len(joined) > max_chars or dur > max_dur
        if gap > 0.34 or ended or too_big:
            _flush(groups, current)
        current.append(word)
    _flush(groups, current)
    if spec.caption_merge_orphans:
        groups = _merge_short(groups, max_n, max_chars)
    packed = []
    for index, group in enumerate(groups):
        start = group[0]["start"]
        end = group[-1]["end"]
        if index + 1 < len(groups):
            nxt = groups[index + 1][0]["start"]
            if nxt - end < 0.12:
                end = nxt
        end = max(end, start + 0.12)
        packed.append({
            "id": f"cap-{index}",
            "start": round(start, 4),
            "end": round(end, 4),
            "words": [
                {**word, "id": f"cap-{index}-w-{wi}"}
                for wi, word in enumerate(group)
            ],
        })
    return packed


def _merge_short(groups: list[list[dict]], max_n: int, max_chars: int) -> list[list[dict]]:
    if not groups:
        return groups
    merged: list[list[dict]] = []
    for group in groups:
        if merged and len(group) < 2:
            trial = merged[-1] + group
            text = " ".join(word["text"] for word in trial)
            if len(trial) <= max_n and len(text) <= max_chars + 6:
                merged[-1] = trial
                continue
        if merged and len(merged[-1]) < 2:
            trial = merged[-1] + group
            text = " ".join(word["text"] for word in trial)
            if len(trial) <= max_n and len(text) <= max_chars + 6:
                merged[-1] = trial
                continue
        merged.append(group)
    return merged


def words_from_lines(beats: list[dict]) -> list[dict]:
    words = []
    for beat in beats:
        tokens = " ".join(beat.get("lines") or []).split()
        if not tokens:
            continue
        span = max(0.2, float(beat["end"]) - float(beat["start"]))
        weights = [max(1, len(token)) for token in tokens]
        total = sum(weights)
        cursor = float(beat["start"])
        for token, weight in zip(tokens, weights):
            dur = span * weight / total
            words.append({
                "text": token,
                "start": round(cursor, 4),
                "end": round(cursor + dur * 0.92, 4),
            })
            cursor += dur
    return words
