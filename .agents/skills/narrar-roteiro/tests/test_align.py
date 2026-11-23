import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from narrar.align import (  # noqa: E402
    ProportionalAligner,
    align_chunks,
    canonical_language,
    guard_whisper_model,
    hyperframes_transcribe_command,
    normalize_words,
    transcribe,
    whisper_cli_command,
    words_from_whisper_payload,
)
from narrar.script import Chunk  # noqa: E402


class GuardTests(unittest.TestCase):
    def test_rejects_english_only_models(self):
        for model in ("small.en", "medium.en", "tiny.en", "base.en"):
            with self.assertRaises(ValueError):
                guard_whisper_model(model)
        self.assertEqual(guard_whisper_model("small"), "small")
        self.assertEqual(guard_whisper_model("large-v3"), "large-v3")

    def test_language_is_portuguese(self):
        self.assertEqual(canonical_language("pt"), "pt")
        self.assertEqual(canonical_language("pt-BR"), "pt")
        self.assertEqual(canonical_language("Portuguese"), "pt")
        with self.assertRaises(ValueError):
            canonical_language("en")

    def test_commands_match_the_repo_pattern(self):
        command = whisper_cli_command("voz.wav", "small", "pt", "/tmp/out")
        self.assertEqual(command[command.index("--language") + 1], "pt")
        self.assertEqual(command[command.index("--model") + 1], "small")
        self.assertNotIn("small.en", command)
        hyper = hyperframes_transcribe_command("voz.wav", "medium", "pt")
        self.assertEqual(hyper[:4], ["npx", "hyperframes", "transcribe", "voz.wav"])
        self.assertEqual(hyper[hyper.index("--language") + 1], "pt")
        self.assertFalse(any(part.endswith(".en") for part in hyper))


class WordSchemaTests(unittest.TestCase):
    def test_whisper_payload_becomes_the_produzir_video_shape(self):
        payload = {
            "segments": [
                {"words": [
                    {"word": " Olá", "start": 0.0, "end": 0.4},
                    {"word": "mundo.", "start": 0.4, "end": 0.9},
                ]},
                {"words": [{"text": "♪", "start": 1.0, "end": 1.1}]},
            ]
        }
        words = words_from_whisper_payload(payload)
        self.assertEqual([word["text"] for word in words], ["Olá", "mundo."])
        for word in words:
            self.assertEqual(set(word), {"text", "start", "end"})
            self.assertLess(word["start"], word["end"])

    def test_flat_list_and_monotonic_clip(self):
        words = normalize_words(
            [
                {"text": "segunda", "start": 0.4, "end": 0.2},
                {"text": "primeira", "start": 0.0, "end": 0.3},
            ],
            duration=0.5,
        )
        self.assertEqual([word["text"] for word in words], ["primeira", "segunda"])
        self.assertLess(words[0]["end"], words[1]["start"] + 0.001)
        self.assertTrue(all(word["start"] < word["end"] <= 0.5 for word in words))

    def test_chunk_alignment_stays_inside_spans(self):
        chunks = [Chunk("um dois", "sentence"), Chunk("três.", "end")]
        spans = [(0.1, 0.5), (0.9, 1.3)]
        words = align_chunks(chunks, spans, duration=1.4)
        self.assertEqual([word["text"] for word in words], ["um", "dois", "três."])
        self.assertGreaterEqual(words[0]["start"], 0.1)
        self.assertLessEqual(words[1]["end"], 0.5)
        self.assertGreaterEqual(words[2]["start"], 0.9)
        self.assertLess(words[1]["end"], words[2]["start"])

    def test_missing_whisper_explains_language(self):
        def missing(path, model, language):
            raise ImportError("faster-whisper não instalado")

        with self.assertRaises(RuntimeError) as caught:
            transcribe("voz.wav", model="small", language="pt", runners=(missing,))
        self.assertIn("pt", str(caught.exception))
        self.assertIn(".en", str(caught.exception))

    def test_proportional_aligner_rejects_english_model(self):
        with self.assertRaises(ValueError):
            ProportionalAligner(model="small.en")


if __name__ == "__main__":
    unittest.main()
