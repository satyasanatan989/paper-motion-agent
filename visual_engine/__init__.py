"""
Cinematic Visual Engine for PaperMotion AI.
Provides 2.5D camera systems, kinetic typography, motion presets, transitions, and dynamic scene composition.
"""

from .camera import CameraController, CameraKeyframe
from .motion_presets import MotionEasing, ParticleField
from .transitions import TransitionLibrary
from .typography import KineticTypography
from .scene_composer import DynamicSceneComposer
from .food_science_library import FoodScienceVisuals, FOOD_CODE_THEME
from .comfy_adapter import ComfyUIAdapter

__all__ = [
    "CameraController",
    "CameraKeyframe",
    "MotionEasing",
    "ParticleField",
    "TransitionLibrary",
    "KineticTypography",
    "DynamicSceneComposer",
    "FoodScienceVisuals",
    "FOOD_CODE_THEME",
    "ComfyUIAdapter"
]
