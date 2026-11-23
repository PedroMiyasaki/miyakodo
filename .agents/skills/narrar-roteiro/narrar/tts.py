"""Backend Qwen3-TTS-12Hz-1.7B-Base.

API verificada no pacote `qwen-tts` 0.1.1 (QwenLM/Qwen3-TTS):

- `Qwen3TTSModel.from_pretrained(repo, device_map=, dtype=, attn_implementation=)`
- `create_voice_clone_prompt(ref_audio=, ref_text=, x_vector_only_mode=)`
- `generate_voice_clone(text=, language="Portuguese", voice_clone_prompt=)`
  devolve `(wavs: list[np.ndarray], sample_rate: int)`

`language` é o nome em inglês que o modelo publica (`Portuguese`), não o código `pt`.
O prompt de clonagem é calculado uma vez e reutilizado em todos os chunks.
"""

from __future__ import annotations

import gc

from narrar.audio import pcm_from_sequence

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
LANGUAGE = "Portuguese"


def resolve_runtime(
    *,
    has_cuda: bool,
    bf16: bool,
    flash_attn: bool,
    device: str = "auto",
    dtype: str = "auto",
    attn: str = "auto",
) -> tuple[str, str, str]:
    requested = (device or "auto").strip().lower()
    if requested in {"auto", ""}:
        chosen = "cuda:0" if has_cuda else "cpu"
    elif requested == "cuda":
        chosen = "cuda:0"
    else:
        chosen = requested
    if chosen.startswith("cuda") and not has_cuda:
        raise RuntimeError(
            "CUDA foi pedido, mas o torch não enxerga uma GPU NVIDIA. "
            "Use --device cpu, ou --device auto para cair na CPU."
        )
    if dtype == "auto":
        if chosen == "cpu":
            dtype_name = "float32"
        elif bf16:
            dtype_name = "bfloat16"
        else:
            dtype_name = "float16"
    else:
        dtype_name = dtype
    if attn == "auto":
        if chosen == "cpu" or dtype_name == "float32" or not flash_attn:
            attn_name = "sdpa"
        else:
            attn_name = "flash_attention_2"
    else:
        attn_name = attn
    if chosen == "cpu" and attn_name == "flash_attention_2":
        raise ValueError("flash_attention_2 não roda em CPU. Use sdpa.")
    if attn_name == "flash_attention_2" and dtype_name not in {"float16", "bfloat16"}:
        raise ValueError("flash_attention_2 exige float16 ou bfloat16.")
    return chosen, dtype_name, attn_name


def probe_hardware() -> dict:
    try:
        import torch
    except ImportError:
        return {"has_cuda": False, "bf16": False, "flash_attn": False, "torch": False}
    has_cuda = bool(torch.cuda.is_available())
    bf16 = False
    if has_cuda:
        checker = getattr(torch.cuda, "is_bf16_supported", None)
        bf16 = bool(checker()) if callable(checker) else False
    flash = False
    if has_cuda:
        try:
            import flash_attn  # noqa: F401

            flash = True
        except ImportError:
            flash = False
    return {"has_cuda": has_cuda, "bf16": bf16, "flash_attn": flash, "torch": True}


def load_kwargs(device: str, dtype_name: str, attn: str) -> dict:
    import torch

    dtype = {
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
        "float32": torch.float32,
    }[dtype_name]
    return {
        "device_map": device,
        "dtype": dtype,
        "attn_implementation": attn,
    }


class QwenVoice:
    def __init__(
        self,
        model_id: str = MODEL_ID,
        device: str = "auto",
        dtype: str = "auto",
        attn: str = "auto",
    ):
        self.model_id = model_id
        self.device_pref = device
        self.dtype_pref = dtype
        self.attn_pref = attn
        self.model = None
        self.prompt = None
        self.sample_rate = None
        self.runtime: tuple[str, str, str] | None = None
        self._ready = False

    def load(self) -> None:
        try:
            import torch
            from qwen_tts import Qwen3TTSModel
        except ImportError as exc:
            raise RuntimeError(
                "qwen-tts ou torch não estão instalados neste ambiente. "
                "No Windows com NVIDIA, siga o README desta skill."
            ) from exc
        del torch
        hardware = probe_hardware()
        device, dtype_name, attn = resolve_runtime(
            has_cuda=hardware["has_cuda"],
            bf16=hardware["bf16"],
            flash_attn=hardware["flash_attn"],
            device=self.device_pref,
            dtype=self.dtype_pref,
            attn=self.attn_pref,
        )
        self.runtime = (device, dtype_name, attn)
        self.model = Qwen3TTSModel.from_pretrained(
            self.model_id,
            **load_kwargs(device, dtype_name, attn),
        )

    def prepare(self, ref_audio: str, ref_text: str | None, x_vector_only: bool) -> None:
        if self.model is None:
            self.load()
        kwargs = {
            "ref_audio": ref_audio,
            "x_vector_only_mode": bool(x_vector_only),
        }
        if not x_vector_only:
            if not ref_text:
                raise ValueError("o modo ICL do Qwen3-TTS exige a transcrição da referência")
            kwargs["ref_text"] = ref_text
        self.prompt = self.model.create_voice_clone_prompt(**kwargs)
        self._ready = True

    def synthesize(self, text: str):
        if not self._ready or self.prompt is None or self.model is None:
            raise RuntimeError("o prompt de voz ainda não foi criado")
        wavs, sample_rate = self.model.generate_voice_clone(
            text=text,
            language=LANGUAGE,
            voice_clone_prompt=self.prompt,
        )
        if not wavs:
            raise RuntimeError("o Qwen3-TTS não devolveu áudio")
        self.sample_rate = int(sample_rate)
        return pcm_from_sequence(wavs[0]), int(sample_rate)

    def close(self) -> None:
        self.prompt = None
        self.model = None
        self._ready = False
        gc.collect()
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass
