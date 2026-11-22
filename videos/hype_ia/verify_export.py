import array
import json
import math
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO = ROOT / "hype_ia_editado_1-1x.mp4"
DURATION = 154.183333 / 1.1


def samples(path):
    with wave.open(str(path)) as audio:
        assert (audio.getnchannels(), audio.getsampwidth(), audio.getframerate()) == (1, 2, 16000)
        return array.array("h", audio.readframes(audio.getnframes()))


def main():
    metadata = json.loads(subprocess.check_output([
        "rtk", "proxy", "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(VIDEO)
    ]))
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    audio = next(s for s in metadata["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"], video["r_frame_rate"]) == (1080, 1920, "60/1")
    assert video["pix_fmt"] == "yuv420p10le"
    assert (video["color_primaries"], video["color_transfer"], video["color_space"]) == ("bt2020", "arib-std-b67", "bt2020nc")
    assert abs(float(metadata["format"]["duration"]) - DURATION) < 0.15
    assert abs(float(audio["duration"]) - DURATION) < 0.15
    decoded = ROOT / "audio-export-check.wav"
    subprocess.run(["rtk", "proxy", "ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(decoded)], check=True)
    reference = ROOT / "audio-reference-1-1x.wav"
    subprocess.run(["rtk", "proxy", "ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "assets/input-video.mp4"), "-vn", "-af", "atempo=1.1", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(reference)], check=True)
    source, exported = samples(reference), samples(decoded)
    checks = []
    for second in (5, 55, 125):
        start, end, step = second * 16000, (second + 4) * 16000, 20
        x = source[start:end:step]
        x_mean = sum(x) / len(x)
        x = [n - x_mean for n in x]
        x_power = sum(n * n for n in x)
        correlations = []
        for lag in range(-40, 41):
            y = exported[start + lag * step:end + lag * step:step]
            y_mean = sum(y) / len(y)
            y = [n - y_mean for n in y]
            correlation = sum(a * b for a, b in zip(x, y)) / math.sqrt(x_power * sum(n * n for n in y))
            correlations.append((correlation, lag / 800))
        correlation, lag = max(correlations)
        assert correlation > 0.97, (second, correlation)
        assert abs(lag) <= 0.03, (second, lag)
        checks.append({"at": second, "correlation": round(correlation, 6), "lag_seconds": lag})
    result = {"video": video, "audio": audio, "duration": metadata["format"]["duration"], "audio_checks": checks}
    (ROOT / "export-validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"duration": result["duration"], "fps": video["r_frame_rate"], "color": "HDR HLG BT.2020", "audio_checks": checks}))


if __name__ == "__main__":
    main()
