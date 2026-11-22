import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def hlg_graphics(value):
    srgb = value / 255
    linear = srgb / 12.92 if srgb <= 0.04045 else ((srgb + 0.055) / 1.055) ** 2.4
    linear *= 0.265
    return (math.sqrt(3 * linear) if linear <= 1 / 12 else 0.17883277 * math.log(12 * linear - 0.28466892) + 0.55991073) * 255


def main():
    assert hlg_graphics(0) == 0
    assert 191 < hlg_graphics(255) < 192
    # HLG graphics white is 75% signal (about 203 nits); the footage keeps its original transfer.
    linear = "(if(lte(val/255,0.04045),val/255/12.92,pow((val/255+0.055)/1.055,2.4))*0.265)"
    curve = f"255*if(lte({linear},1/12),sqrt(3*{linear}),0.17883277*log(12*{linear}-0.28466892)+0.55991073)"
    filters = (
        "[0:v]scale=1080:1920:flags=lanczos:in_color_matrix=bt2020:out_color_matrix=bt2020:out_range=tv,"
        "setsar=1,setpts=(PTS-STARTPTS)/1.1,fps=60,format=yuv420p10le[base];"
        "[1:v]format=rgba,drawbox=x=0:y=0:w=1080:h=128:color=black@0:t=fill:replace=1[ui];"
        "[ui][2:v]overlay=0:0:format=rgb:alpha=straight:repeatlast=1[complete-ui];"
        f"[complete-ui]format=rgba,lutrgb=r='{curve}':g='{curve}':b='{curve}',"
        "scale=in_color_matrix=bt2020:out_color_matrix=bt2020:out_range=tv,"
        "format=yuva420p10le,setpts=PTS-STARTPTS[graphics];"
        "[base][graphics]overlay=0:0:format=yuv420p10:alpha=straight:shortest=1[out]"
    )
    subprocess.run([
        "rtk", "proxy", "ffmpeg", "-hide_banner", "-loglevel", "warning", "-nostats", "-stats_period", "5", "-progress", "pipe:1", "-y",
        "-i", str(ROOT / "assets/input-video.mp4"), "-i", str(ROOT / "renders/overlays.mov"), "-i", str(ROOT / "assets/profile-overlay.png"),
        "-filter_complex", filters, "-map", "[out]", "-map", "0:a:0", "-af", "atempo=1.1", "-t", "140.166667",
        "-c:v", "hevc_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr", "-cq", "15", "-b:v", "0", "-profile:v", "main10", "-pix_fmt", "p010le", "-tag:v", "hvc1",
        "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(ROOT / "hype_ia_editado_1-1x.mp4")
    ], check=True)


if __name__ == "__main__":
    main()
