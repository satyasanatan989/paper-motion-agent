"""
Headless rendering pipelines, CDP WebSocket streamer, and FFmpeg video muxing.
"""

from .cdp_streamer import CDPVideoRenderer
from .batch_stitcher import BatchStitcher

__all__ = ["CDPVideoRenderer", "BatchStitcher"]
