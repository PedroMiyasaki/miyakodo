"""Right-edge 'Aperte aqui para 2X' in the caption font.

Vertical: label center sits 1cm above the frame center on a ~14cm-tall
9:16 phone. Horizontal: flush right, not in the top corner.
ffmpeg overlay: x=W-w-24:y=(H-h)/2-182
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = Path(__file__).resolve().parent / "fonts/BricolageGrotesque-ExtraBold.ttf"

PHONE_CM = 14.07
CANVAS_H = 2560
ONE_CM_PX = round(CANVAS_H * (1.0 / PHONE_CM))  # 182
OVERLAY = f"x=W-w-24:y=(H-h)/2-{ONE_CM_PX}"


def make_tap2x(dest: Path, size: int = 32) -> Path:
    font = ImageFont.truetype(str(FONT), size)
    text = "Aperte aqui para 2X"
    dummy = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy)
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    pad = 10
    w, h = (x1 - x0) + pad * 2, (y1 - y0) + pad * 2
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((pad - x0 + 2, pad - y0 + 2), text, font=font, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(1.6))
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(shadow)
    ImageDraw.Draw(canvas).text((pad - x0, pad - y0), text, font=font, fill=(255, 255, 255, 235))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest)
    return dest


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    make_tap2x(root / "tap2x.png")
    print(OVERLAY)
    print(root / "tap2x.png")
