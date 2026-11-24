import array
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from narrar.audio import probe_duration, write_wav  # noqa: E402
from narrar.reference import (  # noqa: E402
    extract_reference,
    ffmpeg_extract_command,
    parse_silences,
    pick_window,
    reference_audio_filter,
)


def tone_with_silence(rate: int = 8000) -> array.array:
    silence = array.array("h", [0]) * rate
    tone = array.array("h")
    for index in range(rate * 6):
        tone.append(int(8000 * math.sin(2 * math.pi * 440 * index / rate)))
    return silence + tone + silence


class WindowTests(unittest.TestCase):
    def test_prefers_the_span_closest_to_the_target(self):
        silences = [(0.0, 2.0), (22.0, 40.0), (58.0, 60.0)]
        start, duration = pick_window(60.0, silences, target=18.0, minimum=10.0, maximum=30.0)
        self.assertEqual(start, 40.0)
        self.assertEqual(duration, 18.0)

    def test_cuts_a_long_span_down_to_the_target(self):
        start, duration = pick_window(50.0, [(0.0, 5.0)], target=18.0)
        self.assertEqual(start, 5.0)
        self.assertEqual(duration, 18.0)

    def test_parse_silences(self):
        log = "silence_start: 1.0\nsilence_end: 1.8 | silence_duration: 0.8\n"
        self.assertEqual(parse_silences(log), [(1.0, 1.8)])


class ExtractTests(unittest.TestCase):
    def test_command_normalizes_and_trims_edges(self):
        command = ffmpeg_extract_command(Path("video.mp4"), Path("out.wav"), 12.0, 18.0)
        self.assertIn("video.mp4", command)
        self.assertIn("12.000", command)
        self.assertIn("18.000", command)
        audio_filter = reference_audio_filter()
        self.assertIn(audio_filter, command)
        self.assertIn("silenceremove", audio_filter)
        self.assertIn("loudnorm=I=-16", audio_filter)
        self.assertIn("-vn", command)

    def test_extracts_a_clean_window_from_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "fala.wav"
            write_wav(source, tone_with_silence(), 8000)
            destination = folder / "pedro.wav"
            result = extract_reference(source, destination, start=1.2, duration=3.0)
            self.assertTrue(destination.is_file())
            self.assertGreater(result["output_duration"], 2.4)
            self.assertLess(result["output_duration"], 3.4)
            self.assertAlmostEqual(probe_duration(destination), result["output_duration"], places=2)

    def test_transcribe_flag_uses_portuguese(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "fala.wav"
            write_wav(source, tone_with_silence(), 8000)
            destination = folder / "pedro.wav"
            transcript = folder / "pedro.txt"
            words = [{"text": "olá", "start": 0.0, "end": 0.4}, {"text": "mundo", "start": 0.4, "end": 0.8}]
            with mock.patch("narrar.align.transcribe", return_value=words) as transcribe:
                result = extract_reference(
                    source,
                    destination,
                    start=1.2,
                    duration=3.0,
                    transcribe_ref=True,
                    transcript_out=transcript,
                    whisper_model="small",
                    language="pt",
                )
            self.assertEqual(transcribe.call_args.kwargs["language"], "pt")
            self.assertEqual(transcribe.call_args.kwargs["model"], "small")
            self.assertEqual(transcript.read_text(encoding="utf-8").strip(), "olá mundo")
            self.assertEqual(result["transcript"], transcript)


if __name__ == "__main__":
    unittest.main()
