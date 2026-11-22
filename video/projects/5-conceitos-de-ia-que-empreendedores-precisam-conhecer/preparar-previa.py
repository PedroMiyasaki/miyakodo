"""Prepara e exporta somente imagens estáticas do plano, nunca um MP4."""
from pathlib import Path
import argparse
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[2]
ASSETS = PROJECT / "assets"
PLAN = PROJECT / "plano"
PANEL = (80, 570, 1000, 1446)  # painel branco do diagrama, em pixels do canvas 1080 × 1920
NAMES = ["01-gancho", "02-arquiteturas", "03-contexto", "04-dependencias", "05-ai-ops", "06-evals", "07-cta"]
LABELS = ["01 · Gancho · 5 s", "02 · Arquiteturas · 7 s", "03 · Contexto · 5 s", "04 · Dependências · 5 s", "05 · AI Ops · 5 s", "06 · Evals · 6 s", "07 · CTA · 4 s"]


def prepare():
    ASSETS.mkdir(exist_ok=True)
    fonts = ASSETS / "fonts"
    fonts.mkdir(exist_ok=True)
    source = REPO / ".agents/skills/editar-video/assets/fonts"
    for name in ["inter-latin-wght-normal.woff2", "bricolage-grotesque-latin-wght-normal.woff2", "Inter-LICENSE.txt", "Bricolage-LICENSE.txt"]:
        shutil.copy2(source / name, fonts / name)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "1.5",
        "-i", str(REPO / "video/hooks/cafe_cortado.mp4"), "-frames:v", "1",
        "-vf", "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=full,format=rgb24,scale=1080:1920", str(ASSETS / "gancho-frame.png"),
    ], check=True)
    shutil.copytree(fonts, PLAN / "assets/fonts", dirs_exist_ok=True)
    shutil.copy2(ASSETS / "gancho-frame.png", PLAN / "assets/gancho-frame.png")
    print("Fontes locais e frame real do gancho preparados.")


def export():
    shots = PLAN / "capturas"
    subprocess.run([
        "npx.cmd", "hyperframes", "snapshot", str(PLAN), "--at", "2,8.5,14.5,19.5,24.5,30,35",
        "--no-end", "--output", str(shots), "--describe", "false",
    ], check=True)
    frames = sorted(shots.glob("frame-*.png"))
    if len(frames) != len(NAMES):
        raise RuntimeError(f"Esperadas 7 capturas, encontradas {len(frames)}: {[p.name for p in shots.iterdir()]}")
    for src, name in zip(frames, NAMES):
        with Image.open(src) as frame:
            if frame.size != (1080, 1920):
                raise RuntimeError(f"Dimensão inesperada: {src.name} {frame.size}")
            if name not in ["01-gancho", "07-cta"]:
                frame.save(ASSETS / f"{name}.png")
                frame.crop(PANEL).save(ASSETS / f"{name}-overlay.png")
            frame.resize((540, 960), Image.Resampling.LANCZOS).save(PLAN / f"{name}.png")
    sheet = Image.new("RGB", (1440, 1480), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 23)
    for i, (name, label) in enumerate(zip(NAMES, LABELS)):
        x, y = 32 + (i % 4) * 356, 18 + (i // 4) * 730
        draw.text((x, y), label, font=font, fill="#0A0A0A")
        with Image.open(PLAN / f"{name}.png") as frame:
            sheet.paste(frame.resize((324, 576), Image.Resampling.LANCZOS), (x, y + 42))
    sheet.save(PLAN / "sequencia.png")
    print("Banners em assets/, painéis em assets/*-overlay.png, prévias e sequência em plano/. Nenhum vídeo renderizado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("etapa", choices=["preparar", "exportar"])
    args = parser.parse_args()
    if args.etapa == "preparar":
        prepare()
    else:
        export()
