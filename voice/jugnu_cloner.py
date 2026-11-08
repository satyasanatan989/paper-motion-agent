"""
Jugnu Pocket TTS Voice Cloning Engine.
Integrates AltSlate-Labs/jugnu-pocket-tts (based on Kyutai Pocket TTS / CALM architecture).
Supports zero-shot voice cloning for Hindi, English and code-switched Hinglish.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Union
import numpy as np

from .normalizer import normalize_hinglish_text

class JugnuVoiceCloner:
    """
    Zero-shot Hinglish Voice Cloner using AltSlate-Labs/jugnu-pocket-tts.
    Clones vocal timbre, cadence, and accent from a 5-15 second reference clip.
    """

    def __init__(
        self,
        model_variant: str = "lite",
        temperature: Optional[float] = 0.7,
        hf_token: Optional[str] = None
    ):
        """
        model_variant: 'lite' (6 layers, CPU fast), 'base' (12 layers, high fidelity)
        """
        self.variant = model_variant
        self.temperature = temperature
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")
        self._jugnu = None
        self._cached_voice = None

    def _ensure_model_loaded(self):
        """Lazy load Jugnu TTS runtime."""
        if self._jugnu is not None:
            return

        if self.hf_token:
            os.environ["HF_TOKEN"] = self.hf_token

        try:
            # First try local jugnu_tts package if cloned
            import sys
            repo_root = Path(__file__).resolve().parent.parent.parent / "jugnu-pocket-tts"
            if repo_root.exists() and str(repo_root) not in sys.path:
                sys.path.insert(0, str(repo_root))

            from jugnu_tts import Jugnu
            self._jugnu = Jugnu(model=self.variant, temperature=self.temperature)
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Jugnu Pocket TTS ({self.variant}): {e}\n"
                "Ensure huggingface-cli login is performed or HF_TOKEN is set for gated repo access: "
                "https://huggingface.co/altslate/jugnu-pocket-tts and https://huggingface.co/kyutai/pocket-tts"
            )

    def extract_reference_audio(self, video_path: Union[str, Path], output_wav: Union[str, Path], duration: int = 12) -> Path:
        """Extract high-quality vocal reference from an MP4 video."""
        video_path = Path(video_path)
        output_wav = Path(output_wav)
        output_wav.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg", "-y",
            "-ss", "00:00:01",
            "-t", str(duration),
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "24000",
            "-ac", "1",
            str(output_wav)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg audio extraction failed: {res.stderr.decode('utf-8', errors='ignore')}")
        return output_wav

    def clone_voice(self, reference_path: Union[str, Path], save_cache: Optional[Union[str, Path]] = None):
        """
        Extracts vocal characteristics from reference audio or video.
        """
        self._ensure_model_loaded()
        ref_p = Path(reference_path)
        if not ref_p.exists():
            raise FileNotFoundError(f"Reference file not found: {ref_p}")

        # If it's a video, extract wav first
        if ref_p.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]:
            temp_wav = ref_p.with_suffix(".ref_extracted.wav")
            ref_p = self.extract_reference_audio(ref_p, temp_wav)

        voice = self._jugnu.clone(str(ref_p))
        if save_cache:
            voice.save(str(save_cache))
        self._cached_voice = voice
        return voice

    def synthesize(
        self,
        text: str,
        voice = None,
        output_path: Optional[Union[str, Path]] = None,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Synthesize Hinglish speech using the cloned voice.
        """
        self._ensure_model_loaded()
        v = voice or self._cached_voice
        if v is None:
            raise ValueError("No cloned voice provided. Call clone_voice() first.")

        clean_text = normalize_hinglish_text(text) if normalize else text
        audio = self._jugnu.speak(clean_text, voice=v, out=output_path)
        return audio
