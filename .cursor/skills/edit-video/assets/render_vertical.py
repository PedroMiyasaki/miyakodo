"""Reel render (source aspect preserved).

Reuses video-use's tested stages (concat -c copy, transcript word timings with
output-timeline offsets, two-pass loudnorm, overlay PTS-shift + subtitles-LAST
compositing). This layer customizes:

  1. extract_clip(): cut ranges with grade + 30ms audio fades (Hard Rule 3).
     Does NOT force 9:16 — keeps the source framing as shot. Never resizes the
     talking-head — image overlays (news_insert.py) float as a card on top,
     they don't reserve/crop any part of the frame.
  2. apply_plate_effects(): output-timeline effects on the talking-head plate,
     applied AFTER concat and BEFORE overlays, so third-band cards and captions
     never inherit them. Reads edl["plate_effects"]: `zoom_enfase` (punch-in /
     push-in, always resetting to 1.0x) and `preto_e_branco` (B&W grade window).
     Skipped entirely when the EDL has none — no re-encode, no cost.
  3. composite(): overlays then optional subtitles LAST (Hard Rule 1) when
     `--subtitles` is passed. Off by default here; edit-video passes it
     on the final render only. `--pop-it` mixes a click
     SFX (assets/sfx/click.wav) at each overlay's start_in_output — one click
     per image pop, before loudnorm swallows the final mix. Runs ffmpeg with
     cwd=edit_dir and RELATIVE master.ass / fontsdir paths (absolute Windows
     paths break libass — the drive colon is a filter-arg separator).
  4. build_master_ass(): captions as ASS, not SRT — sentence case, the
     Alvinegro face bundled in assets/fonts/, and short chunks that replace
     each other, like Instagram's own captions. ASS so the file carries its
     own style, sized to the real canvas. See assets/features/subtitles.md.

Honors video-use Hard Rules 1–7, 12. Run via:
  PYTHONUTF8=1 VIRTUAL_ENV= uv run --no-sync --project <video-use> python render_vertical.py <edl.json> -o <out.mp4>
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

HELPERS = Path.home() / ".claude" / "skills" / "video-use" / "helpers"
sys.path.insert(0, str(HELPERS))
import render as R  # the shared video-use helper

SFX_CLICK = Path(__file__).parent / "sfx" / "click.wav"

# extract_clip pins every segment to this rate; zoompan must be told the same
# one or it resamples the plate and the punch-in drifts off its landing word.
FPS = 24

# Captions — the Alvinegro DISPLAY voice (design/identity.md). The face isn't
# installed on Windows, so the TTF ships here and gets copied into <edit>/fonts/
# for libass to pick up via `fontsdir` (a relative path: see docstring note 3).
CAPTION_FONTS = Path(__file__).parent / "fonts"
CAPTION_TTFS = ("BricolageGrotesque-ExtraBold.ttf",)
BODY_FONT = "Bricolage Grotesque ExtraBold"   # Bold=0: the file is already 800, don't fake-bold.

# Fractions of the OUTPUT height/width, so one set of numbers holds whatever the
# phone shot. PlayRes is written as the real canvas, so nothing is rescaled.
CAP_SIZE = 0.0583        # 112px at 1920 — matches the reference caption weight
CAP_MARGIN_V = 0.3125    # bottom safe zone, unchanged from the SRT era
CAP_MARGIN_H = 0.074

CUE_WORDS = 4            # like Instagram's own captions: a short chunk that
                         # replaces the last one, never a block that grows
LINE_CHARS = 18          # wrap before the line reaches the safe margins
HOLD_MAX = 0.6           # seconds a cue rests through the pause after it
MIN_STEP = 0.25          # shorter than this is a flash, not a caption


def probe_output_dims(source: Path) -> tuple[int, int]:
    """Decoded (post-rotation) width/height — what ffmpeg actually outputs,
    not the raw stream dims (iPhone footage stores landscape + a rotate
    side_data; ffmpeg auto-applies it on decode/encode). Printed as a
    diagnostic so --width/--height passed to news_insert.py match the real
    canvas — a fixed 1080x1920 assumption was the session-2 "tiny image" bug."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries",
         "side_data=rotation", "-of", "json", str(source)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    stream = data["streams"][0]
    w, h = int(stream["width"]), int(stream["height"])
    rotation = 0
    for sd in stream.get("side_data_list", []):
        if "rotation" in sd:
            rotation = int(sd["rotation"])
            break
    if abs(rotation) in (90, 270):
        w, h = h, w
    return w, h


def extract_clip(source: Path, seg_start: float, duration: float,
                 grade_filter: str, out_path: Path, preview: bool) -> None:
    """Extract a cut range; preserve source resolution/aspect. Never crops or
    resizes — image overlays float as a card, they don't need reserved space."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fo = max(0.0, duration - 0.03)
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fo:.3f}:d=0.03"
    preset, crf = ("medium", "22") if preview else ("fast", "20")
    cmd = [
        "ffmpeg", "-y", "-ss", f"{seg_start:.3f}", "-i", str(source),
        "-t", f"{duration:.3f}",
    ]
    vf_parts: list[str] = []
    if R.is_hdr_source(source):
        vf_parts.append(R.TONEMAP_CHAIN)
    if grade_filter:
        vf_parts.append(grade_filter)
    if vf_parts:
        cmd += ["-vf", ",".join(vf_parts)]
    cmd += [
        "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _ss(num: str, dur: float) -> str:
    """smoothstep (3u^2-2u^3) over a normalized ramp — eases both ends so the
    scale never starts or stops with a visible jerk."""
    u = f"(({num})/{dur:.4f})"
    return f"(3*{u}*{u}-2*{u}*{u}*{u})"


def _bw_expr(effects: list[dict], default_fade: float = 0.10) -> str:
    """hue saturation over output time: 1.0 normally, 0.0 inside each window,
    with short ramps at the edges (feature spec: 80-120ms, never a hard cut)."""
    expr = "1"
    for e in reversed(effects):          # reversed: earlier windows test first
        a, b = float(e["start_in_output"]), float(e["end_in_output"])
        f = max(0.02, min(float(e.get("fade", default_fade)), (b - a) / 2))
        inside = (
            f"if(lt(t,{a + f:.4f}),1-(t-{a:.4f})/{f:.4f},"
            f"if(lt(t,{b - f:.4f}),0,(t-{b - f:.4f})/{f:.4f}))"
        )
        expr = f"if(between(t,{a:.4f},{b:.4f}),{inside},{expr})"
    return expr


def _zoom_expr(effects: list[dict]) -> str:
    """zoompan z over output time. Every gesture lands back at 1.0 by its
    end_in_output — the feature's hard rule, enforced by construction.

    Note the clock: zoompan spells seconds `time`, while hue (and most filters)
    spell it `t`. Using `t` here fails to configure the filter outright."""
    T = "time"
    expr = "1"
    for e in reversed(effects):
        a, b = float(e["start_in_output"]), float(e["end_in_output"])
        mode = e.get("mode", "slow")
        peak = float(e.get("scale_peak", 1.14 if mode == "fast" else 1.07))
        gain = peak - 1.0
        if mode == "fast":
            land = float(e["land_at"])
            rise = max(0.02, min(0.22, land - a))
            hold, fall = 0.30, 0.20
            avail = b - land
            if avail < hold + fall:      # squeeze the gesture into the window
                k = max(0.0, avail) / (hold + fall)
                hold, fall = hold * k, fall * k
            hold, fall = max(hold, 0.01), max(fall, 0.02)
            r0, h0, f0 = land - rise, land + hold, land + hold + fall
            inside = (
                f"if(lt({T},{r0:.4f}),1,"
                f"if(lt({T},{land:.4f}),1+{gain:.4f}*{_ss(f'{T}-{r0:.4f}', rise)},"
                f"if(lt({T},{h0:.4f}),{peak:.4f},"
                f"if(lt({T},{f0:.4f}),{peak:.4f}-{gain:.4f}*{_ss(f'{T}-{h0:.4f}', fall)},1))))"
            )
        else:
            d = max(b - a, 0.04)
            rise, fall = d * 0.7, d * 0.3
            m = a + rise
            inside = (
                f"if(lt({T},{m:.4f}),1+{gain:.4f}*{_ss(f'{T}-{a:.4f}', rise)},"
                f"{peak:.4f}-{gain:.4f}*{_ss(f'{T}-{m:.4f}', fall)})"
            )
        expr = f"if(between({T},{a:.4f},{b:.4f}),{inside},{expr})"
    return expr


def build_plate_filter(effects: list[dict], w: int, h: int) -> str:
    """-vf chain for the plate. B&W first (cheap), zoom last so the punch-in
    resamples once. Empty string when there is nothing to do."""
    known = {"preto_e_branco", "zoom_enfase"}
    unknown = sorted({str(e.get("type")) for e in effects} - known)
    if unknown:
        raise SystemExit(f"unknown plate_effect type(s): {unknown}")
    bw = [e for e in effects if e["type"] == "preto_e_branco"]
    zoom = [e for e in effects if e["type"] == "zoom_enfase"]
    # Overlapping zooms would silently pick one and drop the other.
    spans = sorted((float(e["start_in_output"]), float(e["end_in_output"])) for e in zoom)
    for (_, prev_end), (nxt_start, _) in zip(spans, spans[1:]):
        if nxt_start < prev_end:
            raise SystemExit(
                f"overlapping zoom_enfase windows near {nxt_start:.2f}s — "
                "the feature forbids stacking zooms"
            )
    chain = []
    if bw:
        chain.append(f"hue=s='{_bw_expr(bw)}'")
    if zoom:
        chain.append(
            f"zoompan=z='{_zoom_expr(zoom)}':d=1"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={FPS}"
        )
    return ",".join(chain)


def apply_plate_effects(base: Path, effects: list[dict], w: int, h: int,
                        out_path: Path, preview: bool) -> None:
    """Re-encode the concatenated plate with its output-timeline effects.
    Audio is copied — this pass never touches the mix."""
    vf = build_plate_filter(effects, w, h)
    preset, crf = ("veryfast", "23") if preview else ("medium", "18")
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-i", str(base), "-vf", vf,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _ass_time(seconds: float) -> str:
    cs = int(round(max(0.0, seconds) * 100))
    h, rem = divmod(cs, 360_000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_header(w: int, h: int) -> str:
    """One style, BODY, for every cue."""
    size = round(h * CAP_SIZE)
    return "\n".join([
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {w}",
        f"PlayResY: {h}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        # Outline 0: no black edge on the default caption. Separation from the
        # footage is the drop shadow alone (BackColour, semi-transparent).
        f"Style: BODY,{BODY_FONT},{size},&H00FFFFFF,&H00FFFFFF,&H000A0A0A,"
        f"&H90000000,0,0,0,0,100,100,0,0,1,0,"
        f"{round(size * 0.045)},2,{round(w * CAP_MARGIN_H)},"
        f"{round(w * CAP_MARGIN_H)},{round(h * CAP_MARGIN_V)},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text",
        "",
    ])


def _chunks(words: list[dict]) -> list[list[dict]]:
    """Split a segment's words into short caption chunks: break after any
    punctuation, once the chunk reaches CUE_WORDS, or before it would wrap
    to a third line."""
    out, cur = [], []
    for w in words:
        text = (w.get("text") or "").strip()
        if not text:
            continue
        if cur and _wrap([x["text"].strip() for x in cur] + [text]).count("\\N") >= 2:
            out.append(cur)
            cur = []
        cur.append(w)
        if text[-1] in ".!?…,;:" or len(cur) >= CUE_WORDS:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _wrap(words: list[str]) -> str:
    lines, cur = [], ""
    for word in words:
        if cur and len(cur) + 1 + len(word) > LINE_CHARS:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return "\\N".join(lines)


def build_master_ass(edl: dict, edit_dir: Path, out_path: Path,
                     canvas: tuple[int, int]) -> None:
    """Build an output-timeline ASS from the per-source transcripts.

    One cue per chunk; the next chunk replaces it, nothing accumulates. A cue
    holds through the pause after it. Sentence case is kept as transcribed —
    the transcript already capitalises names and sentence starts, and forcing
    UPPERCASE throws that away."""
    transcripts_dir = edit_dir / "transcripts"
    w, h = canvas
    lines: list[str] = []
    seg_offset = 0.0

    for r in edl["ranges"]:
        seg_start, seg_end = float(r["start"]), float(r["end"])
        seg_dur = seg_end - seg_start
        tr_path = transcripts_dir / f"{r['source']}.json"
        if not tr_path.exists():
            print(f"  no transcript for {r['source']}, skipping its captions")
            seg_offset += seg_dur
            continue

        transcript = json.loads(tr_path.read_text(encoding="utf-8"))
        chunks = _chunks(R._words_in_range(transcript, seg_start, seg_end))

        for ci, chunk in enumerate(chunks):
            start = max(seg_start, chunk[0].get("start", seg_start))
            # Nothing may run past the next cue, or across the hard cut.
            limit = min(chunks[ci + 1][0].get("start", seg_end)
                        if ci + 1 < len(chunks) else seg_end, seg_end)
            end = chunk[-1].get("end", seg_end) + HOLD_MAX
            # Floor first, cap second — the cap has to win, or a cue can
            # be pushed past the next one and the two draw stacked.
            end = min(max(end, start + MIN_STEP), limit)
            text = _wrap([(x.get("text") or "").strip() for x in chunk])
            text = text.rstrip(",;:.").replace("{", "(").replace("}", ")")
            lines.append(
                f"Dialogue: 0,"
                f"{_ass_time(start - seg_start + seg_offset)},"
                f"{_ass_time(end - seg_start + seg_offset)},"
                f"BODY,,0,0,0,,{text}"
            )

        seg_offset += seg_dur

    out_path.write_text(_ass_header(w, h) + "\n".join(lines) + "\n",
                        encoding="utf-8")
    print(f"built {out_path.name}: {len(lines)} cue(s) at {w}x{h}")


def _build_fc(overlays: list[dict], subs: Path | None,
             click_idx: int | None, click_ts: list[float]) -> str:
    parts = []
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"])
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{t}/TB[a{idx}]")
    cur = "[0:v]"
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"]); dur = float(ov["duration"])
        parts.append(
            f"{cur}[a{idx}]overlay=enable='between(t,{t:.3f},{t+dur:.3f})'[v{idx}]"
        )
        cur = f"[v{idx}]"
    if subs is not None:
        # No force_style: master.ass carries its own [V4+ Styles].
        parts.append(f"{cur}subtitles={subs.name}:fontsdir=fonts[outv]")
    elif overlays:
        parts[-1] = parts[-1].rsplit("[", 1)[0] + "[outv]"
    else:
        parts.append("[0:v]format=yuv420p[outv]")

    if click_idx is not None and click_ts:
        # click.wav's own peak is -7.5dBFS. Clicks land at overlay start —
        # exactly where the VO is usually mid-word, not a pause — so a click
        # that just sits "under" the voice gets masked entirely. +4dB (peak
        # ~-3.5dBFS, 24dB above the silent floor) still wasn't audible on
        # playback — likely the click's own timbre (hipass/lopass-filtered
        # white noise) is thin next to voice on small speakers, not just
        # level. +10dB (peak ~+2.5dBFS pre-mix) to compensate; loudnorm's
        # -1dBTP ceiling downstream catches any overs from the sum.
        n = len(click_ts)
        parts.append(
            f"[{click_idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"volume=+10dB,asplit={n}" + "".join(f"[cs{i}]" for i in range(n))
        )
        for i, t in enumerate(click_ts):
            parts.append(f"[cs{i}]adelay={round(t*1000)}:all=1[cd{i}]")
        clicks = "".join(f"[cd{i}]" for i in range(n))
        # alimiter is load-bearing, not belt-and-braces: click.wav peaks at
        # -7.5dBFS, so volume=+10dB puts the click alone at +2.5dBFS and the
        # sum clips inside THIS stage's AAC encode. Downstream loudnorm cannot
        # undo it — worse, it runs linear=true (constant gain, no peak
        # limiting) and measures the already-clipped file as TP~0, reads that
        # as headroom, and adds another ~3dB. Cap the mix here, before the
        # encode, or the deliverable ships clipped.
        parts.append(
            f"[0:a]{clicks}amix=inputs={n+1}:normalize=0:dropout_transition=0,"
            f"alimiter=limit=0.891:level=disabled[outa]"
        )

    return ";".join(parts)


def composite(base: Path, overlays: list[dict], subs: Path | None,
              out_path: Path, edit_dir: Path, pop_it: bool = False) -> None:
    """Overlays (PTS-shifted), then subtitles LAST when present. pop_it mixes
    a click SFX at each overlay's start_in_output (one image pop = one click)."""
    click_ts = [float(ov["start_in_output"]) for ov in overlays] if pop_it else []
    if click_ts and not SFX_CLICK.exists():
        print(f"warning: pop-it requested but {SFX_CLICK} is missing — skipping SFX")
        click_ts = []

    if not overlays and subs is None:
        print(f"compositing -> {out_path.name}  (overlays: 0, subs: no)")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(base), "-c", "copy",
             "-movflags", "+faststart", str(out_path)],
            check=True, cwd=str(edit_dir), stderr=subprocess.PIPE,
        )
        return

    inputs = ["-i", str(base)]
    for ov in overlays:
        inputs += ["-i", str(R.resolve_path(ov["file"], edit_dir))]
    click_idx = None
    if click_ts:
        click_idx = 1 + len(overlays)
        inputs += ["-i", str(SFX_CLICK)]

    fc = _build_fc(overlays, subs, click_idx, click_ts)
    audio_map = "[outa]" if click_ts else "0:a"
    audio_codec = ["-c:a", "aac", "-b:a", "192k"] if click_ts else ["-c:a", "copy"]
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc,
           "-map", "[outv]", "-map", audio_map,
           "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
           *audio_codec, "-movflags", "+faststart", str(out_path)]
    print(
        f"compositing -> {out_path.name}  "
        f"(overlays: {len(overlays)}, subs: {'yes' if subs else 'no'}, "
        f"pop-it: {'yes (' + str(len(click_ts)) + ' clicks)' if click_ts else 'no'})"
    )
    subprocess.run(cmd, check=True, cwd=str(edit_dir), stderr=subprocess.PIPE)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("edl", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--no-loudnorm", action="store_true")
    ap.add_argument("--subtitles", action="store_true",
                    help="Burn captions (off by default; edit-video passes it "
                         "on the final render only)")
    ap.add_argument("--no-subtitles", action="store_true",
                    help="Deprecated no-op; subtitles are off unless --subtitles")
    ap.add_argument("--pop-it", action="store_true",
                    help="Mix a click SFX at each overlay's start_in_output (opt-in; off by default)")
    args = ap.parse_args()

    edl = json.loads(args.edl.read_text())
    edit_dir = args.edl.resolve().parent
    out_path = args.output.resolve()

    grade = R.resolve_grade_filter(edl.get("grade"))
    clips_dir = edit_dir / ("clips_preview" if args.preview else "clips_graded")
    clips_dir.mkdir(parents=True, exist_ok=True)

    first_src = R.resolve_path(next(iter(edl["sources"].values())), edit_dir)
    canvas = probe_output_dims(first_src)
    print(f"canvas: {canvas[0]}x{canvas[1]}  (pass this as --width/--height to news_insert.py)")

    seg_paths = []
    print(f"extracting {len(edl['ranges'])} segment(s) -> {clips_dir.name}/")
    for i, r in enumerate(edl["ranges"]):
        src = R.resolve_path(edl["sources"][r["source"]], edit_dir)
        s, e = float(r["start"]), float(r["end"])
        op = clips_dir / f"seg_{i:02d}.mp4"
        print(f"  [{i:02d}] {s:7.2f}-{e:7.2f} ({e-s:5.2f}s)")
        extract_clip(src, s, e - s, grade, op, args.preview)
        seg_paths.append(op)

    base = edit_dir / ("base_preview.mp4" if args.preview else "base.mp4")
    R.concat_segments(seg_paths, base, edit_dir)

    # Plate effects run on the concatenated talking-head, before overlays, so
    # third-band cards and captions stay in colour and at 1.0x on top of them.
    plate_fx = edl.get("plate_effects") or []
    if plate_fx:
        plate = edit_dir / ("plate_preview.mp4" if args.preview else "plate.mp4")
        print(f"plate effects -> {len(plate_fx)} (zoom/B&W)")
        apply_plate_effects(base, plate_fx, canvas[0], canvas[1], plate, args.preview)
        base = plate

    subs = None
    if args.subtitles:
        subs = edit_dir / "master.ass"
        fonts_dir = edit_dir / "fonts"
        fonts_dir.mkdir(exist_ok=True)
        for ttf in CAPTION_TTFS:
            if not (fonts_dir / ttf).exists():
                shutil.copy2(CAPTION_FONTS / ttf, fonts_dir / ttf)
        # ponytail: keep a hand-edited master.ass (e.g. a fixed transcription
        # typo) instead of regenerating over it. Delete the file to rebuild it from
        # the transcripts.
        if subs.exists():
            print(f"reusing existing {subs.name} (delete it to regenerate)")
        else:
            build_master_ass(edl, edit_dir, subs, canvas)

    overlays = edl.get("overlays") or []
    if args.no_loudnorm:
        composite(base, overlays, subs, out_path, edit_dir, pop_it=args.pop_it)
    else:
        tmp = out_path.with_suffix(".prenorm.mp4")
        composite(base, overlays, subs, tmp, edit_dir, pop_it=args.pop_it)
        print("loudnorm -> -14 LUFS / -1 dBTP / LRA 11")
        R.apply_loudnorm_two_pass(tmp, out_path, preview=args.preview)
        tmp.unlink(missing_ok=True)

    mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\ndone: {out_path} ({mb:.1f} MB)")


if __name__ == "__main__":
    main()
