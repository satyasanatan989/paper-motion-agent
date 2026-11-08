"""
Voice cloning and cinematic Foley audio synthesis for PaperMotion AI.
Supports Jugnu Pocket TTS (AltSlate-Labs) and IndicF5 flow-matching DiT.
"""

from .normalizer import normalize_hinglish_text
from .jugnu_cloner import JugnuVoiceCloner
from .indicf5_engine import IndicF5VoiceEngine
from .audio_master import AudioMasterEngine

__all__ = [
    "normalize_hinglish_text",
    "JugnuVoiceCloner",
    "IndicF5VoiceEngine",
    "AudioMasterEngine",
]
