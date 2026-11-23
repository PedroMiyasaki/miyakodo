import array
import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from narrar.audio import (  # noqa: E402
    DELIVERY_RATE,
    TARGET_I,
    TARGET_TP,
    apply_loudnorm,
    loudnorm_filter,
    measure_loudness,
    parse_loudnorm_stats,
    read_wav,
    stitch,
    write_wav,
)


def tone(samples: int, amplitude: int = 8000, rate: int = 8000) -> array.array:
    data = array.array("h")
    for index in range(samples):
        data.append(int(amplitude * math.sin(2 * math.pi * 220 * index / rate)))
    return data


class StitchTests(unittest.TestCase):
    def test_pauses_tail_and_clickless_edges(self):
        rate = 8000
        chunk = tone(1000, rate=rate)
        result = stitch(
            [(chunk, "sentence"), (array.array("h", chunk), "end")],
            rate,
            sentence_pause=0.2,
            crossfade_ms=10,
            tail_s=0.1,
        )
        self.assertEqual(len(result.samples), 4400)
        self.assertAlmostEqual(result.spans[1][0] - result.spans[0][1], 0.2, places=3)
        self.assertEqual(result.samples[999], 0)
        self.assertEqual(result.samples[1000], 0)
        self.assertGreater(abs(result.samples[500]), 1000)
        self.assertEqual(result.samples[-1], 0)

    def test_paragraph_pause_is_longer_than_sentence(self):
        rate = 4000
        chunk = tone(200, rate=rate)
        sentence = stitch([(chunk, "sentence"), (array.array("h", chunk), "end")], rate, sentence_pause=0.28, paragraph_pause=0.52, tail_s=0)
        paragraph = stitch([(chunk, "paragraph"), (array.array("h", chunk), "end")], rate, sentence_pause=0.28, paragraph_pause=0.52, tail_s=0)
        self.assertGreater(paragraph.spans[1][0] - paragraph.spans[0][1], sentence.spans[1][0] - sentence.spans[0][1])

    def test_wav_roundtrip(self):
        chunk = tone(400, rate=8000)
        result = stitch([(chunk, "end")], 8000, tail_s=0, crossfade_ms=0)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "voz.wav"
            write_wav(path, result.samples, result.sample_rate)
            samples, rate = read_wav(path)
        self.assertEqual(rate, 8000)
        self.assertEqual(samples, result.samples)


class LoudnessTests(unittest.TestCase):
    def test_filter_targets_reel_loudness(self):
        plain = loudnorm_filter()
        self.assertIn("I=-16", plain)
        self.assertIn("TP=-1", plain)
        measured = loudnorm_filter({
            "input_i": "-23.0",
            "input_tp": "-3.0",
            "input_lra": "5.0",
            "input_thresh": "-33.0",
            "target_offset": "0.4",
        })
        self.assertIn("measured_I=-23.0", measured)
        self.assertIn("linear=true", measured)
        stats = parse_loudnorm_stats('log\n{\n\t"input_i" : "-23.0"\n}\n')
        self.assertEqual(stats["input_i"], "-23.0")

    def test_ffmpeg_hits_minus_16_lufs(self):
        rate = 16000
        data = tone(rate * 2, amplitude=4000, rate=rate)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tone.wav"
            write_wav(path, data, rate)
            apply_loudnorm(path)
            samples, out_rate = read_wav(path)
            stats = measure_loudness(path)
        self.assertEqual(out_rate, DELIVERY_RATE)
        self.assertGreater(len(samples), rate)
        integrated = float(stats["input_i"])
        true_peak = float(stats["input_tp"])
        self.assertAlmostEqual(integrated, TARGET_I, delta=1.5)
        self.assertLessEqual(true_peak, TARGET_TP + 0.3)


if __name__ == "__main__":
    unittest.main()
