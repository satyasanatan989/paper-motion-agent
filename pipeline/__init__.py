"""
Headless rendering pipelines, CDP WebSocket streamer, and FFmpeg video muxing.
"""

from .cdp_streamer import CDPVideoRenderer

__all__ = ["CDPVideoRenderer"]
