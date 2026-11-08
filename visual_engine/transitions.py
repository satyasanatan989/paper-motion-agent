"""
Cinematic Transition Library for PaperMotion AI.
Provides directional wipes, zoom cuts, paper tears, mask reveals, and light flashes.
"""

from typing import Dict, Any

class TransitionLibrary:
    """Generates CSS & JS transition logic for smooth scene changes."""

    TRANSITION_STYLES = {
        "directional_wipe": """
        .scene.transition-exit-directional_wipe {
          transform: translateX(-100%) !important;
          opacity: 0.8 !important;
          transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .scene.transition-enter-directional_wipe {
          transform: translateX(100%) !important;
        }
        .scene.active.transition-enter-directional_wipe {
          transform: translateX(0) !important;
          opacity: 1 !important;
          transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        """,
        "cinematic_zoom": """
        .scene.transition-exit-cinematic_zoom {
          transform: scale(1.15) !important;
          opacity: 0 !important;
          filter: blur(10px) !important;
          transition: transform 0.45s ease-in, opacity 0.4s ease-in, filter 0.4s ease-in !important;
        }
        .scene.transition-enter-cinematic_zoom {
          transform: scale(0.88) !important;
          opacity: 0 !important;
        }
        .scene.active.transition-enter-cinematic_zoom {
          transform: scale(1.0) !important;
          opacity: 1 !important;
          transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease-out !important;
        }
        """,
        "paper_tear": """
        .scene.transition-exit-paper_tear {
          clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
          transition: clip-path 0.45s cubic-bezier(0.77, 0, 0.175, 1) !important;
        }
        .scene.transition-exit-paper_tear.tearing {
          clip-path: polygon(0 0, 100% 0, 0 100%, 0 100%) !important;
          opacity: 0 !important;
        }
        """,
        "mask_reveal": """
        .scene.transition-enter-mask_reveal {
          clip-path: circle(0% at 50% 50%);
          opacity: 1 !important;
        }
        .scene.active.transition-enter-mask_reveal {
          clip-path: circle(150% at 50% 50%);
          transition: clip-path 0.55s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        """
    }

    @classmethod
    def get_all_css(cls) -> str:
        """Returns consolidated CSS transition rules."""
        return "\n".join(cls.TRANSITION_STYLES.values())
