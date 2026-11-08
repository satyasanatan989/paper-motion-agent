"""
PaperMotion Autonomous Agent Architecture.
Coordinates scriptwriting, Jugnu Hinglish voice cloning, papercraft motion graphics, and CDP rendering.
"""

from .prompts import MAYANK_DIRECTOR_SYSTEM_PROMPT
from .script_engine import ScriptEngine
from .director import PaperMotionDirector

__all__ = [
    "MAYANK_DIRECTOR_SYSTEM_PROMPT",
    "ScriptEngine",
    "PaperMotionDirector",
]
