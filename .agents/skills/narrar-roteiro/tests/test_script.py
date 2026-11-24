import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(SKILL))

from narrar.script import (  # noqa: E402
    classify_bracket,
    clean_inline,
    looks_hybrid,
    prepare_speech,
    split_long,
)


HYBRID = """[HOOK] · literal
Top 5 lições que eu aprendi desenvolvendo IA pra grandes empresas.
E como bom aspirante a blogueiro, eu vou deixar a melhor lição por último.

[pause]

[VIRADA] · literal
E a primeira vai contra o meu próprio trabalho.

[DEGRAU] · tópicos
- organizar = cada processo escrito → um estagiário novo segue sem perguntar
- IA não adivinha o jeito da sua empresa

[insert: gráfico do relatório do MIT]

# Não ler este título

<!-- comentário interno -->

[CTA] · literal
Se você achou esse conteúdo útil, usa IA **de menos** e lê o [guia](https://example.com).

---
Gravação: um take por bloco. Literal lido, tópicos falados olhando pra lente.
"""

PLAIN = """# Título que entra

Este é um parágrafo **importante** com [um link](https://example.com) e `código`.

- item da lista

<!-- comentário -->

```
print("não narrar")
```

Outro parágrafo com Dr. Pedro e 90%.
"""


class ParserTests(unittest.TestCase):
    def test_hybrid_literal_skips_topics_notes_and_stage_directions(self):
        speech = prepare_speech(HYBRID, mode="auto")
        text = speech.text
        self.assertIn("lições", text)
        self.assertIn("de menos", text)
        self.assertIn("guia", text)
        self.assertNotIn("estagiário", text)
        self.assertNotIn("adivinha", text)
        self.assertNotIn("gráfico", text)
        self.assertNotIn("Não ler", text)
        self.assertNotIn("comentário", text)
        self.assertNotIn("Gravação", text)
        self.assertNotIn("**", text)
        self.assertNotIn("http", text)
        self.assertNotIn("pause", text.lower())
        self.assertTrue(any(chunk.break_after == "beat" for chunk in speech.chunks))

    def test_auto_detects_hybrid_and_plain(self):
        self.assertTrue(looks_hybrid(HYBRID))
        self.assertFalse(looks_hybrid(PLAIN))
        self.assertEqual(prepare_speech(HYBRID, "auto").text, prepare_speech(HYBRID, "literal").text)
        plain = prepare_speech(PLAIN, "auto")
        self.assertIn("Título que entra", plain.text)
        self.assertIn("importante", plain.text)
        self.assertIn("um link", plain.text)
        self.assertIn("código", plain.text)
        self.assertIn("item da lista", plain.text)
        self.assertIn("Outro parágrafo", plain.text)
        self.assertNotIn("não narrar", plain.text)
        self.assertNotIn("comentário", plain.text)
        self.assertNotIn("example.com", plain.text)

    def test_all_mode_speaks_topic_bullets(self):
        speech = prepare_speech(HYBRID, mode="all")
        self.assertIn("estagiário", speech.text)
        self.assertNotIn("gráfico do relatório", speech.text)
        self.assertNotIn("→", speech.text)

    def test_literal_on_plain_markdown_still_speaks(self):
        speech = prepare_speech("Um parágrafo corrido, sem bloco.", mode="literal")
        self.assertIn("parágrafo corrido", speech.text)

    def test_unmarked_sections_are_spoken(self):
        path = REPO / "posts/script/saida-de-jacob-coxon-da-anthropic-e-o-alerta-sobre-risco-existencial-da-ia/final.md"
        speech = prepare_speech(path.read_text(encoding="utf-8"), mode="auto")
        self.assertIn("humanidade", speech.text)
        self.assertIn("desesperar", speech.text)
        self.assertIn("laboratórios estão avançando", speech.text)
        self.assertNotIn("print do post", speech.text)
        self.assertNotIn("Fontes dos inserts", speech.text)

    def test_real_teleprompter_keeps_only_literal(self):
        path = REPO / "posts/script/top-5-licoes-desenvolvendo-ia-para-grandes-empresas/final.md"
        speech = prepare_speech(path.read_text(encoding="utf-8"), mode="literal")
        self.assertIn("lições", speech.text)
        self.assertIn("de menos", speech.text)
        self.assertNotIn("estagiário", speech.text)
        self.assertNotIn("um take por bloco", speech.text)
        self.assertNotIn("**", speech.text)

    def test_clean_inline(self):
        self.assertEqual(clean_inline("**negrito** e [rótulo](https://x.test) e `api`"), "negrito e rótulo e api")
        self.assertEqual(clean_inline("![foto](a.png) fica"), "fica")

    def test_stage_direction_classes(self):
        self.assertEqual(classify_bracket("pause"), "pause")
        self.assertEqual(classify_bracket("insert: gráfico"), "skip")
        self.assertEqual(classify_bracket("HOOK"), "section")
        self.assertEqual(classify_bracket("O PIOR ERRO"), "section")

    def test_examples_parse(self):
        hybrid = (SKILL / "examples" / "hibrido.md").read_text(encoding="utf-8")
        plain = (SKILL / "examples" / "corrido.md").read_text(encoding="utf-8")
        spoken = prepare_speech(hybrid, "auto").text
        self.assertIn("Reel", spoken)
        self.assertNotIn("teleprompter", spoken)
        corrido = prepare_speech(plain, "auto").text
        self.assertIn("noventa por cento", corrido)
        self.assertNotIn("não é falado", corrido)


class ChunkTests(unittest.TestCase):
    def test_sentence_and_paragraph_breaks(self):
        text = "Primeira frase aqui. Segunda frase aqui.\n\nTerceira frase longa."
        speech = prepare_speech(text, mode="all", max_chars=24)
        kinds = [chunk.break_after for chunk in speech.chunks]
        self.assertEqual(kinds[0], "sentence")
        self.assertIn("paragraph", kinds)
        self.assertEqual(kinds[-1], "end")
        self.assertTrue(all(len(chunk.text) <= 24 or " " not in chunk.text for chunk in speech.chunks))

    def test_long_sentence_splits_on_comma_without_cutting_words(self):
        sentence = "Esta frase ficou longa, com uma vírgula no meio, e ainda continua até passar do limite combinado."
        pieces = split_long(sentence, 48)
        self.assertGreater(len(pieces), 1)
        self.assertTrue(all(len(piece) <= 48 for piece in pieces))
        self.assertTrue(all(" " not in piece or piece == piece.strip() for piece in pieces))
        rebuilt = " ".join(piece.replace(",", "") for piece in pieces).split()
        self.assertEqual(rebuilt, sentence.replace(",", "").split())

    def test_pause_marker_becomes_beat(self):
        text = "[HOOK] · literal\nPrimeira fala curta.\n\n[pause]\n\n[CTA] · literal\nSegunda fala curta."
        speech = prepare_speech(text, mode="literal", max_chars=80)
        self.assertEqual(speech.chunks[0].break_after, "beat")
        self.assertEqual(speech.chunks[-1].break_after, "end")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            prepare_speech("oi", mode="verso")


if __name__ == "__main__":
    unittest.main()
