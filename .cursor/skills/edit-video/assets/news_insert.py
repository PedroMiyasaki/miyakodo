# -*- coding: utf-8 -*-
"""Lower-third news reference card for `news` mode.

Floats one still image as a card over the video, centered in the lower-third
zone (not stuck to the bottom edge). The talking-head is never resized or
cropped — the card just sits on top for a few seconds, then goes away. Pops
in with a quick scale-overshoot (pairs with a click SFX mixed in by
render_vertical.py's --pop-it) and a slow Ken Burns while it holds, fades out
at the end.

Output drops straight into edl.json "overlays". No burned captions.

CLI:
    python news_insert.py --image print.png --out <slotdir> --duration 5 \
        --source "openai.com" --fit contain --width 2160 --height 3840

  --width/--height: the BASE VIDEO's actual output resolution (post-rotation
                     decode), not a fixed default — get it from
                     render_vertical.py's `canvas:` print line. A mismatch
                     here is the classic "insert renders tiny in the corner"
                     bug (ffmpeg's overlay filter doesn't auto-scale).
  --fit contain (default): fit the whole image inside the card — never
                           crops content. Right for article screenshots / charts.
  --fit cover:             fill the card, cropping overflow. Right for photos /
                           logos meant to bleed, mostly-empty framing.

Writes <slotdir>/frames/*.png and <slotdir>/render.mov.
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920        # overridden in main() from --width/--height
FPS = 24                 # overridden in main() from --fps

# Card geometry, as fractions of canvas — resolution-independent.
MARGIN_X_FRAC = 0.08     # side margins
ZONE_H_FRAC = 0.70       # card max height, as a fraction of the lower third's
                         # own height (not the full canvas) — leaves it
                         # centered with air above/below, never touching the
                         # bottom edge.
PAD_FRAC = 0.018         # inner padding between image and card edge
RADIUS_FRAC = 0.04       # corner radius, relative to min(card_w, card_h)
SHADOW_BLUR_FRAC = 0.012
SHADOW_DY_FRAC = 0.006

# Card colours
INK = (0, 0, 0)
PAPER = (255, 255, 255)
SEAL = (141, 69, 61)

FONTS = Path(__file__).parent / "fonts"
JETBRAINS = str(FONTS / "JetBrainsMono.ttf")

ZOOM_END = 1.05
POP_DUR = 0.15            # scale-overshoot pop, paired with the click SFX
FADE_OUT = 0.2


def ease_in_out(p: float) -> float:
    if p < 0.5:
        return 4 * p ** 3
    return 1 - (-2 * p + 2) ** 3 / 2


def _fit_size(iw, ih, fit, box_w, box_h):
    """Size at zoom=1.0 inside box_w x box_h."""
    br = box_w / box_h
    ir = iw / ih
    if fit == "cover":
        if ir > br:
            return round(box_h * ir), box_h
        return box_w, round(box_w / ir)
    if ir > br:
        return box_w, round(box_w / ir)
    return round(box_h * ir), box_h


def _chyron_font_size():
    return max(16, round(W * 0.016))


def _chyron_reserved_h(source_label):
    """Vertical space the chyron needs, reserved above the image so a tight
    crop's own heading never sits under the pill (measured bug: tight crops
    put the image content right at the card's top edge, same place the
    chyron paints, so title text and 'FONTE:' pill overlapped)."""
    if not source_label:
        return 0
    font_size = _chyron_font_size()
    pad = max(16, round(W * PAD_FRAC))
    return pad + font_size + 13 + pad  # pill's own top inset + text/accent height + gap before image


def _chyron(card_w, source_label, pad):
    """Small mono source pill, pinned inside the card's top-left, within the
    band reserved by _chyron_reserved_h."""
    layer = Image.new("RGBA", (card_w, 200), (0, 0, 0, 0))
    if not source_label:
        return layer
    draw = ImageDraw.Draw(layer)
    font_size = _chyron_font_size()
    font = ImageFont.truetype(JETBRAINS, font_size)
    txt = f"FONTE: {source_label}"
    tx, ty = pad, pad
    bb = draw.textbbox((tx, ty), txt, font=font)
    bg_pad = 6
    draw.rectangle(
        [bb[0] - bg_pad, bb[1] - bg_pad, bb[2] + bg_pad, bb[3] + bg_pad],
        fill=INK + (200,),
    )
    draw.text((tx, ty), txt, font=font, fill=PAPER + (255,))
    accent_y = bb[3] + bg_pad + 4
    draw.rectangle([tx - bg_pad, accent_y, tx - bg_pad + 56, accent_y + 3], fill=SEAL + (255,))
    return layer


def _build_card(image_path: Path, fit: str, source_label: str) -> Image.Image:
    """The settled (z=1.0) card: white rounded panel + inset image + chyron +
    soft drop shadow, sized to fit the lower-third zone. Everything scales
    together per-frame in build_insert (one resize = pop + Ken Burns)."""
    img = Image.open(image_path).convert("RGBA")

    zone_h = round(H / 3 * ZONE_H_FRAC)
    card_max_w = round(W * (1 - 2 * MARGIN_X_FRAC))
    card_max_h = zone_h
    pad = max(16, round(W * PAD_FRAC))
    top_pad = pad + _chyron_reserved_h(source_label)

    inner_w, inner_h = card_max_w - 2 * pad, card_max_h - pad - top_pad
    fw, fh = _fit_size(img.width, img.height, fit, inner_w, inner_h)
    fitted = img.resize((fw, fh), Image.LANCZOS)
    if fit == "cover":
        # _fit_size intentionally overflows one axis for cover — crop it back
        # down to the box, otherwise the card itself balloons to the
        # overflowing size instead of staying clamped to card_max_w/h.
        left, top = (fw - inner_w) // 2, (fh - inner_h) // 2
        fitted = fitted.crop((left, top, left + inner_w, top + inner_h))
        fw, fh = inner_w, inner_h

    card_w, card_h = fw + 2 * pad, fh + pad + top_pad
    radius = max(12, round(min(card_w, card_h) * RADIUS_FRAC))

    # the image gets its own rounded corners — a square print inside the
    # rounded card reads dated. Multiply keeps any transparency the source has.
    img_mask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(img_mask).rounded_rectangle([0, 0, fw - 1, fh - 1], radius=radius, fill=255)
    fitted.putalpha(ImageChops.multiply(fitted.getchannel("A"), img_mask))

    card = Image.new("RGBA", (card_w, card_h), PAPER + (255,))
    px, py = (card_w - fw) // 2, top_pad
    card.alpha_composite(fitted, (px, py))

    chyron = _chyron(card_w, source_label, pad)
    card.alpha_composite(chyron, (0, 0))

    mask = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=radius, fill=255)
    card.putalpha(mask)

    # soft drop shadow, composed into the same image so it scales with the pop
    blur = max(4, round(W * SHADOW_BLUR_FRAC))
    dy = max(2, round(W * SHADOW_DY_FRAC))
    pad_s = blur * 3
    combo = Image.new("RGBA", (card_w + 2 * pad_s, card_h + 2 * pad_s), (0, 0, 0, 0))
    shadow_mask = Image.new("L", combo.size, 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle(
        [pad_s, pad_s + dy, pad_s + card_w - 1, pad_s + dy + card_h - 1],
        radius=radius, fill=110,
    )
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(blur))
    shadow = Image.new("RGBA", combo.size, INK + (0,))
    shadow.putalpha(shadow_mask)
    combo.alpha_composite(shadow)
    combo.alpha_composite(card, (pad_s, pad_s))
    return combo


def _scale_at(t: float, duration: float) -> float:
    """Overshoot pop (0.90 -> 1.03 -> 1.00) over POP_DUR, then a slow Ken
    Burns drift to ZOOM_END for the rest of the hold."""
    if t < POP_DUR:
        p = t / POP_DUR
        if p < 0.6:
            return 0.90 + (1.03 - 0.90) * ease_in_out(p / 0.6)
        return 1.03 + (1.00 - 1.03) * ease_in_out((p - 0.6) / 0.4)
    rest = max(1e-6, duration - POP_DUR)
    p2 = min(1.0, (t - POP_DUR) / rest)
    return 1.0 + (ZOOM_END - 1.0) * p2


def _alpha_at(t: float, duration: float) -> float:
    if t < POP_DUR * 0.6:
        return ease_in_out(t / (POP_DUR * 0.6))
    if t > duration - FADE_OUT:
        return ease_in_out(max(0.0, (duration - t) / FADE_OUT))
    return 1.0


def encode_mov(frames_dir: Path, out_mov: Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", str(frames_dir / "%04d.png"),
        "-c:v", "prores_ks", "-profile:v", "4444",
        "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
        str(out_mov),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def build_insert(out_dir: Path, image_path: Path, duration: float,
                 source_label: str, fit: str) -> Path:
    combo = _build_card(image_path, fit, source_label)
    cw, ch = combo.size
    cx = W // 2
    cy = round(H * 2 / 3 + (H / 3) / 2)  # vertical center = middle of the lower third

    frames = out_dir / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    for old in frames.glob("*.png"):
        old.unlink()

    n = round(duration * FPS)
    for i in range(n):
        t = i / FPS
        z = _scale_at(t, duration)
        a = _alpha_at(t, duration)
        w, h = max(1, round(cw * z)), max(1, round(ch * z))
        scaled = combo.resize((w, h), Image.LANCZOS)
        if a < 1.0:
            ch_a = scaled.getchannel("A").point(lambda v, a=a: int(round(v * a)))
            scaled.putalpha(ch_a)
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(scaled, (cx - w // 2, cy - h // 2))
        canvas.save(frames / f"{i + 1:04d}.png")

    mov = out_dir / "render.mov"
    encode_mov(frames, mov)
    return mov


def main():
    global W, H, FPS
    ap = argparse.ArgumentParser(description="Lower-third news reference card")
    ap.add_argument("--image", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--source", default="", help="source chyron, e.g. openai.com (omit = no chyron)")
    ap.add_argument("--fit", choices=("contain", "cover"), default="contain")
    ap.add_argument("--width", type=int, default=1080, help="canvas width — match the base video's actual output width")
    ap.add_argument("--height", type=int, default=1920, help="canvas height — match the base video's actual output height")
    ap.add_argument("--fps", type=float, default=24, help="frame rate — match the base video's (the render's `canvas:` line)")
    a = ap.parse_args()

    W, H, FPS = a.width, a.height, a.fps

    a.out.mkdir(parents=True, exist_ok=True)
    mov = build_insert(a.out, a.image, a.duration, a.source, a.fit)
    print(
        f"news_insert: {mov}  ({a.duration:.2f}s, {round(a.duration * FPS)} frames, "
        f"fit={a.fit}, canvas={W}x{H})"
    )


if __name__ == "__main__":
    main()
