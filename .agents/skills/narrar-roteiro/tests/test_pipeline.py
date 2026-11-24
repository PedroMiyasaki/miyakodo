import json
import sys
import tempfile
import unittest
import wave
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
PRODUZIR = Path(__file__).resolve().parents[2] / "produzir-video"
sys.path.insert(0, str(SKILL))
sys.path.insert(0, str(PRODUZIR))

from narrar.audio import write_wav  # noqa: E402
from narrar.mock import MockVoice  # noqa: E402
from narrar.pipeline import narrate  # noqa: E402
from narrar.tts import resolve_runtime  # noqa: E402
from pipeline.compile import compile_script  # noqa: E402
import array  # noqa: E402


class RuntimeTests(unittest.TestCase):
    def test_cuda_prefers_bfloat16_and_flash_when_present(self):
        device, dtype, attn = resolve_runtime(has_cuda=True, bf16=True, flash_attn=True)
        self.assertEqual((device, dtype, attn), ("cuda:0", "bfloat16", "flash_attention_2"))

    def test_cuda_without_flash_or_bf16_uses_float16_sdpa(self):
        device, dtype, attn = resolve_runtime(has_cuda=True, bf16=False, flash_attn=False)
        self.assertEqual((device, dtype, attn), ("cuda:0", "float16", "sdpa"))

    def test_auto_without_gpu_falls_back_to_cpu(self):
        device, dtype, attn = resolve_runtime(has_cuda=False, bf16=False, flash_attn=False)
        self.assertEqual((device, dtype, attn), ("cpu", "float32", "sdpa"))

    def test_explicit_cuda_without_gpu_fails(self):
        with self.assertRaises(RuntimeError):
            resolve_runtime(has_cuda=False, bf16=False, flash_attn=False, device="cuda:0")

    def test_flash_requires_half_precision(self):
        with self.assertRaises(ValueError):
            resolve_runtime(has_cuda=True, bf16=True, flash_attn=True, dtype="float32", attn="flash_attention_2")
        with self.assertRaises(ValueError):
            resolve_runtime(has_cuda=True, bf16=False, flash_attn=False, device="cpu", attn="flash_attention_2")


class PipelineTests(unittest.TestCase):
    def test_mock_narration_matches_produzir_video_schema(self):
        roteiro = "[HOOK] · literal\nPrimeira frase aqui. Segunda frase aqui.\n\n[pause]\n\n[CTA] · literal\nFica no vídeo.\n\n[DEGRAU] · tópicos\n- isto não entra\n"
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text(roteiro, encoding="utf-8")
            ref = folder / "ref.wav"
            write_wav(ref, array.array("h", [0]) * 1600, 8000)
            backend = MockVoice()
            closed = {}

            class Align:
                def __init__(self):
                    from narrar.align import ProportionalAligner
                    self.inner = ProportionalAligner()

                def __call__(self, wav_path, chunks, spans):
                    closed["before_align"] = backend._ready is False
                    return self.inner(wav_path, chunks, spans)

            result = narrate(
                script,
                ref,
                folder / "out",
                ref_text="amostra de voz do pedro",
                mode="literal",
                backend=backend,
                aligner=Align(),
                repo=folder,
                max_chars=24,
                loudnorm=False,
                log=lambda _message: None,
            )
            self.assertEqual(backend.prepare_calls, 1)
            self.assertGreater(result["chunks"], 1)
            self.assertEqual(len(backend.texts), result["chunks"])
            self.assertTrue(closed["before_align"])
            self.assertFalse(backend.x_vector_only)
            words = json.loads(result["words"].read_text(encoding="utf-8"))
            snippet = json.loads(result["snippet"].read_text(encoding="utf-8"))
            self.assertNotIn("não entra", " ".join(word["text"] for word in words))
            self.assertEqual(snippet["mode"], "sem-gravacao")
            self.assertEqual(snippet["words"], words)
            for word in words:
                self.assertEqual(set(word), {"text", "start", "end"})
                self.assertLess(word["start"], word["end"])
            self.assertLessEqual(words[-1]["end"], snippet["voice"]["out"])
            model = compile_script({
                **snippet,
                "slug": "teste",
                "purpose": "opiniao",
                "beats": [{
                    "start": 0,
                    "end": snippet["voice"]["out"],
                    "layout": "guide",
                    "label": "Fala",
                    "scene": {"type": "badge", "text": "oi"},
                }],
            })
            self.assertEqual(model["mode"], "sem-gravacao")
            self.assertTrue(model["groups"])
            with wave.open(str(result["voice"])) as handle:
                self.assertEqual(handle.getnchannels(), 1)
                self.assertGreater(handle.getnframes() / handle.getframerate(), 0.2)

    def test_missing_transcript_uses_x_vector_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text("Uma frase falada sem tópicos no meio dela.", encoding="utf-8")
            ref = folder / "ref.wav"
            write_wav(ref, array.array("h", [0]) * 800, 8000)
            backend = MockVoice()
            from narrar.align import ProportionalAligner
            narrate(
                script,
                ref,
                folder / "out",
                ref_text=None,
                mode="all",
                backend=backend,
                aligner=ProportionalAligner(),
                loudnorm=False,
                snippet=False,
                log=lambda _message: None,
            )
            self.assertTrue(backend.x_vector_only)
            self.assertIsNone(backend.ref_text)

    def test_loudnorm_delivery_stays_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text("Uma frase falada com voz de teste para o reel.", encoding="utf-8")
            ref = folder / "ref.wav"
            write_wav(ref, array.array("h", [0]) * 800, 8000)
            from narrar.align import ProportionalAligner
            result = narrate(
                script,
                ref,
                folder / "out",
                ref_text="referência",
                mode="all",
                backend=MockVoice(),
                aligner=ProportionalAligner(),
                loudnorm=True,
                log=lambda _message: None,
            )
            self.assertEqual(result["sample_rate"], 48000)
            snippet = json.loads(result["snippet"].read_text(encoding="utf-8"))
            self.assertLessEqual(snippet["words"][-1]["end"], snippet["voice"]["out"])
            compile_script({
                **snippet,
                "purpose": "opiniao",
                "beats": [{
                    "start": 0,
                    "end": snippet["voice"]["out"],
                    "layout": "guide",
                    "label": "Fala",
                    "scene": {"type": "badge", "text": "oi"},
                }],
            })


if __name__ == "__main__":
    unittest.main()
