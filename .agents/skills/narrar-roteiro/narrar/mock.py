"""Sintetizador falso: tom curto, sem GPU, para teste e CI."""

from __future__ import annotations

import array
import math


class MockVoice:
    def __init__(self, sample_rate: int = 16000, seconds_per_word: float = 0.16):
        self.sample_rate = sample_rate
        self.seconds_per_word = seconds_per_word
        self.prepare_calls = 0
        self.texts: list[str] = []
        self.ref_audio = None
        self.ref_text = None
        self.x_vector_only = None
        self.runtime = ("mock", "pcm", "none")
        self._ready = False

    def prepare(self, ref_audio: str, ref_text: str | None, x_vector_only: bool) -> None:
        self.prepare_calls += 1
        self.ref_audio = ref_audio
        self.ref_text = ref_text
        self.x_vector_only = x_vector_only
        self._ready = True

    def synthesize(self, text: str):
        if not self._ready:
            raise RuntimeError("o prompt de voz ainda não foi criado")
        self.texts.append(text)
        words = max(1, len(text.split()))
        total = max(1, int(self.sample_rate * self.seconds_per_word * words))
        data: array.array = array.array("h")
        for index in range(total):
            value = int(8000 * math.sin(2 * math.pi * 220 * index / self.sample_rate))
            data.append(value)
        return data, self.sample_rate

    def close(self) -> None:
        self._ready = False
