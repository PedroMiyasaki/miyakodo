import sys
import tempfile
import unittest
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.audio import keep_ranges, parse_silences, range_duration, remap_time, write_wav
from pipeline.brand import AVATAR_ASPECT, LAYOUT_SPOTS, SAFE_BOTTOM, SAFE_RIGHT, SCENE_TOP, SCENE_TYPES
from pipeline.captions import group_words, tag_roles
from pipeline.compile import ScriptError, compile_script
from pipeline.compose import render_html
from pipeline.scenes import build_scene


def words(text, start=0.0, step=0.3):
    out = []
    cursor = start
    for token in text.split():
        out.append({"text": token, "start": round(cursor, 3), "end": round(cursor + 0.24, 3)})
        cursor += step
    return out


class CaptionTests(unittest.TestCase):
    def test_sem_gravacao_groups_stay_short(self):
        grouped = group_words(words("um dois tres quatro cinco seis sete"), "sem-gravacao")
        for group in grouped:
            self.assertLessEqual(len(group["words"]), 4)
            self.assertLessEqual(len(" ".join(w["text"] for w in group["words"])), 32)
        self.assertGreaterEqual(len(grouped), 2)

    def test_gravacao_avoids_orphan_word(self):
        grouped = group_words(words("fica nesse vídeo"), "gravacao")
        self.assertTrue(all(len(group["words"]) >= 2 for group in grouped))

    def test_roles(self):
        tagged = tag_roles(words("evals e vídeo"), emphasis=["evals"], cta=["vídeo"])
        roles = {word["text"]: word["role"] for word in tagged}
        self.assertEqual(roles["evals"], "emphasis")
        self.assertEqual(roles["vídeo"], "cta")


class CutTests(unittest.TestCase):
    def test_parse_and_keep(self):
        log = "silence_start: 1.0\nsilence_end: 1.8 | silence_duration: 0.8\n"
        silences = parse_silences(log)
        ranges = keep_ranges(3.0, silences, pad=0.05)
        self.assertEqual(len(ranges), 2)
        self.assertLess(range_duration(ranges), 2.6)
        self.assertAlmostEqual(remap_time(0.4, ranges), 0.4, places=2)
        self.assertLess(remap_time(2.0, ranges), 1.6)

    def test_leading_silence_is_dropped(self):
        ranges = keep_ranges(4.0, [(0.0, 0.6), (2.0, 2.5)], pad=0.05)
        self.assertGreaterEqual(ranges[0][0], 0.5)
        self.assertLess(ranges[0][0], 0.7)

    def test_compile_remaps_gravacao(self):
        cuts = [(0.0, 1.0), (1.7, 3.0)]
        model = compile_script({
            "mode": "gravacao",
            "slug": "corte",
            "purpose": "historia",
            "voice": {"src": "voz.wav", "in": 0, "out": 3},
            "beats": [{
                "start": 0, "end": 3, "layout": "split", "label": "Cena",
                "scene": {"type": "badge", "text": "oi"},
            }],
            "words": words("fala antes e depois do corte", start=0.1, step=0.4),
        }, cuts=cuts)
        self.assertAlmostEqual(model["duration"], range_duration(cuts), places=2)
        self.assertLess(model["duration"], 2.6)
        self.assertTrue(model["videos"])
        self.assertEqual(model["videos"][0]["layout"], "split")


class CompileTests(unittest.TestCase):
    def test_lines_become_captions_and_avatar(self):
        model = compile_script({
            "mode": "sem-gravacao",
            "slug": "Opinião",
            "purpose": "opiniao",
            "voice": {"src": "voz.wav", "in": 0, "out": 4},
            "emphasis": ["evals"],
            "beats": [
                {"start": 0, "end": 2, "layout": "guide", "label": "Ideia", "lines": ["você precisa de evals"], "scene": {"type": "timeline", "title": "Passos", "items": ["A", "B"]}},
                {"start": 2, "end": 4, "layout": "center", "label": "Centro", "lines": ["o ponto é negócio"], "scene": {"type": "diagram", "center": "IA", "items": ["Produto"]}},
            ],
        })
        self.assertEqual(model["slug"], "opinião")
        self.assertIsNotNone(model["avatar"])
        self.assertTrue(model["groups"])
        html = render_html(model)
        self.assertIn("#280e03", html)
        self.assertIn("#f6f4ee", html)
        self.assertIn("#1a3010", html)
        self.assertIn("Instrument Serif", html)
        self.assertIn("Poppins", html)
        self.assertIn('id="avatar"', html)
        self.assertIn("boxShadow", html)
        self.assertIn("evals", html)

    def test_rejects_unknown_scene_and_bad_layout(self):
        with self.assertRaises(ScriptError):
            compile_script({
                "mode": "sem-gravacao",
                "voice": {"in": 0, "out": 2},
                "beats": [{"start": 0, "end": 2, "scene": {"type": "holograma"}}],
            })
        with self.assertRaises(ScriptError):
            compile_script({
                "mode": "gravacao",
                "voice": {"in": 0, "out": 2},
                "beats": [{"start": 0, "end": 2, "layout": "guide", "scene": {"type": "badge", "text": "x"}}],
            })

    def test_every_scene_type_renders(self):
        sample = {
            "timeline": {"title": "Lista", "items": ["Um"]},
            "mockup": {"title": "App", "lines": ["item"], "kind": "browser"},
            "counter": {"label": "itens", "value": 3},
            "diagram": {"center": "Núcleo", "items": ["A", "B"]},
            "chat": {"title": "Papo", "messages": [{"from": "Ana", "text": "oi"}]},
            "code": {"filename": "a.ts", "lines": ['const x = "ok"']},
            "phone": {"handle": "@MIYAKODO", "comment": "quero", "dm": "segue"},
            "grid": {"items": ["a", "b", "c", "d", "e", "f", "g", "h", "i"]},
            "scanline": {"label": "leitura"},
            "folders": {"root": "contratos", "items": [{"name": "a.pdf", "depth": 1}]},
            "bullets": {"kicker": "Notas", "items": ["uma"]},
            "quote": {"text": "Uma frase.", "by": "Pedro"},
            "badge": {"text": "fica"},
            "stack": {"children": [{"type": "badge", "text": "a"}, {"type": "quote", "text": "b", "by": ""}]},
            "statement": {"kicker": "Ideia", "text": "Sem interface"},
            "carlos": {"pose": "boss", "line": "o empresário"},
            "versus": {"left": "Pessoa", "right": "Agente", "left_items": ["tela"], "right_items": ["API"], "pose": "squat"},
        }
        for kind in SCENE_TYPES:
            html, ops, sfx = build_scene("p", 0, 0, 400, 300, {"type": kind, **sample[kind]}, 0.2, 2.0)
            self.assertIn("p", html)
            self.assertTrue(ops)
            self.assertTrue(sfx)


class SafeZoneTests(unittest.TestCase):
    def test_faceless_spots_clear_caption_footer_and_buttons(self):
        def overlaps(a, b):
            ax, ay, aw, ah = a
            bx, by, bw, bh = b
            return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

        for name, spot in LAYOUT_SPOTS.items():
            sx, sy, sw, sh = spot["scene"]
            self.assertGreaterEqual(sy, SCENE_TOP, name)
            self.assertLessEqual(sx + sw, SAFE_RIGHT, name)
            self.assertLessEqual(sy + sh, SAFE_BOTTOM, name)
            left, top, width, opacity = spot["avatar"]
            height = width * AVATAR_ASPECT
            if not opacity:
                continue
            box = (left, top, width, height)
            self.assertGreaterEqual(top, SCENE_TOP, name)
            self.assertLessEqual(left + width, SAFE_RIGHT, name)
            self.assertLessEqual(top + height, SAFE_BOTTOM + 0.5, name)
            self.assertFalse(overlaps(box, (sx, sy, sw, sh)), name)


class BuildTests(unittest.TestCase):
    def test_build_writes_project(self):
        from pipeline.cli import build_project, find_repo

        repo = find_repo(Path(__file__).resolve().parents[1])
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            voice = folder / "voz.wav"
            write_wav(voice, 2.0)
            roteiro = folder / "roteiro.json"
            roteiro.write_text(
                '{"mode":"sem-gravacao","slug":"teste-build","purpose":"cta",'
                '"voice":{"src":"%s","in":0,"out":2},'
                '"beats":[{"start":0,"end":2,"layout":"guide","label":"Fica","lines":["fica no vídeo"],'
                '"scene":{"type":"phone","handle":"@MIYAKODO","comment":"oi","dm":"dm"}}]}' % voice,
                encoding="utf-8",
            )
            import json
            data_path = roteiro
            out = build_project(data_path, folder / "projeto", repo)
            html = (out / "index.html").read_text(encoding="utf-8")
            self.assertTrue((out / "assets" / "voice.wav").exists())
            self.assertTrue((out / "assets" / "logo.png").exists())
            self.assertTrue((out / "assets" / "gsap.min.js").exists())
            self.assertIn("Miyakodo", html)
            with wave.open(str(out / "assets" / "voice.wav")) as handle:
                self.assertGreater(handle.getnframes(), 1000)
            json.loads((out / "meta.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
