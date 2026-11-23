import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "cli.py"
PRODUZIR = Path(__file__).resolve().parents[2] / "produzir-video"
sys.path.insert(0, str(SKILL))
sys.path.insert(0, str(PRODUZIR))

from narrar.audio import write_wav  # noqa: E402
from pipeline.compile import compile_script  # noqa: E402
import array  # noqa: E402


def run_cli(args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CliTests(unittest.TestCase):
    def test_texto_prints_literal_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "roteiro.md"
            script.write_text(
                "[HOOK] · literal\nFala que entra.\n\n[DEGRAU] · tópicos\n- tópico que fica de fora\n",
                encoding="utf-8",
            )
            result = run_cli(["texto", str(script), "--mode", "literal"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Fala que entra.", result.stdout)
        self.assertNotIn("fica de fora", result.stdout)

    def test_narrar_mock_writes_voice_words_and_snippet(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text(
                "[HOOK] · literal\nPrimeira frase aqui. Segunda frase aqui.\n\n[CTA] · literal\nFica no vídeo.\n",
                encoding="utf-8",
            )
            ref = folder / "ref.wav"
            write_wav(ref, array.array("h", [0]) * 1600, 8000)
            out = folder / "saida"
            result = run_cli([
                "narrar", str(script),
                "--ref", str(ref),
                "--ref-text", "fala de referência do pedro",
                "--out", str(out),
                "--backend", "mock",
                "--align", "mock",
                "--mode", "literal",
                "--max-chars", "28",
                "--no-loudnorm",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            words = json.loads((out / "words.json").read_text(encoding="utf-8"))
            snippet = json.loads((out / "produzir-video.snippet.json").read_text(encoding="utf-8"))
            self.assertTrue((out / "voice.wav").is_file())
            self.assertGreater(len(words), 3)
            model = compile_script({
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
            self.assertTrue(model["groups"])

    def test_english_whisper_model_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text("Uma frase.", encoding="utf-8")
            ref = folder / "ref.wav"
            write_wav(ref, array.array("h", [0]) * 800, 8000)
            result = run_cli([
                "narrar", str(script),
                "--ref", str(ref),
                "--out", str(folder / "out"),
                "--backend", "mock",
                "--whisper-model", "small.en",
            ])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".en", result.stderr)

    def test_missing_reference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            script = folder / "roteiro.md"
            script.write_text("Uma frase.", encoding="utf-8")
            result = run_cli([
                "narrar", str(script),
                "--ref", str(folder / "nao-existe.wav"),
                "--out", str(folder / "out"),
                "--backend", "mock",
            ])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("referência", result.stderr)

    def test_extract_command_writes_a_reference_wav(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "bruto.wav"
            silence = array.array("h", [0]) * 8000
            tone = array.array("h")
            for index in range(8000 * 4):
                tone.append(int(6000 * __import__("math").sin(2 * 3.14159265 * 330 * index / 8000)))
            write_wav(source, silence + tone + silence, 8000)
            destination = folder / "voice-ref" / "pedro.wav"
            result = run_cli([
                "extrair-referencia", str(source),
                "--start", "1.2",
                "--duration", "2.5",
                "--out", str(destination),
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("pedro.wav", result.stdout)
            self.assertTrue(destination.is_file())


if __name__ == "__main__":
    unittest.main()
