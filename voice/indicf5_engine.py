"""
IndicF5 DiT Flow-Matching Voice Synthesis Engine.
Provides local, offline fine-tuned Hinglish voice generation with Vocos neural vocoder.
"""

import os
from pathlib import Path
from typing import Optional, Union, List
import soundfile as sf
import numpy as np

class IndicF5VoiceEngine:
    """
    Offline neural speech synthesis using IndicF5 DiT flow-matching + Vocos vocoder.
    """

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        device: str = "cpu"
    ):
        self.ckpt_path = Path(checkpoint_path or r"C:\HinglishVoice\indicf5-finetune\checkpoints\model.safetensors")
        self.device = device
        self._model = None
        self._vocos = None

    def is_available(self) -> bool:
        """Check if local checkpoint exists."""
        return self.ckpt_path.exists()

    def _ensure_loaded(self):
        if self._model is not None:
            return

        if not self.ckpt_path.exists():
            raise FileNotFoundError(f"IndicF5 checkpoint not found at {self.ckpt_path}")

        import torch
        from vocos import Vocos
        import sys

        # Add f5_tts to path if present in HinglishVoice directory
        hf_src = Path(r"C:\HinglishVoice\indicf5-finetune\src")
        if hf_src.exists() and str(hf_src) not in sys.path:
            sys.path.insert(0, str(hf_src))

        from f5_tts.model import DiT
        from f5_tts.infer.utils_infer import load_model, load_checkpoint

        self._vocos = Vocos.from_pretrained("charactr/vocos-mel-24khz")

        model_cls = DiT
        model_cfg = dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4)
        vocab_path = Path(r"C:\HinglishVoice\indicf5-finetune\src\f5_tts\infer\examples\vocab.txt")

        self._model = load_model(model_cls, model_cfg, str(vocab_path), device=self.device)
        self._model = load_checkpoint(self._model, str(self.ckpt_path), self.device, use_ema=True)

    def synthesize_chapters(
        self,
        chapters: List[dict],
        ref_audio: Union[str, Path],
        ref_text: str,
        output_wav: Union[str, Path]
    ) -> float:
        """
        Synthesizes a list of narrative chapter segments and concatenates them with audio pauses.
        Returns total audio duration in seconds.
        """
        self._ensure_loaded()
        import torch
        from f5_tts.infer.utils_infer import infer_process

        full_wave = []
        sr = 24000
        pause_silence = np.zeros(int(sr * 0.45), dtype=np.float32)

        for ch in chapters:
            gen_text = ch.get("text", "")
            wav, _, _ = infer_process(
                str(ref_audio),
                ref_text,
                gen_text,
                self._model,
                self._vocos,
                device=self.device,
                speed=1.05
            )
            full_wave.append(wav)
            full_wave.append(pause_silence)

        master_wav = np.concatenate(full_wave)
        sf.write(str(output_wav), master_wav, sr)
        duration = len(master_wav) / sr
        return duration
