"""
Automated Video Quality Control Suite for PaperMotion AI.
Validates resolution, framerate, duration, broadcast loudness (-14 LUFS), black frames, and frozen holds.
"""

from .validator import QualityValidator, QualityReport, SceneQCResult

__all__ = ["QualityValidator", "QualityReport", "SceneQCResult"]
