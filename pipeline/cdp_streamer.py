"""
Python Wrapper for CDP Video Renderer.
Spawns the Node.js memory pipe renderer with full error handling and progress monitoring.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

class CDPVideoRenderer:
    """Controls headless Chrome CDP rendering and FFmpeg encoding from Python."""

    def __init__(self, render_script: Optional[Union[str, Path]] = None):
        self.render_script = Path(render_script or Path(__file__).parent / "render.js")

    def render(
        self,
        html_path: Union[str, Path],
        audio_path: Optional[Union[str, Path]] = None,
        output_mp4: Optional[Union[str, Path]] = None,
        duration: float = 22.31,
        fps: int = 30
    ) -> Path:
        """
        Executes frame-accurate headless rendering into an MP4 file.
        """
        html_path = Path(html_path)
        output_mp4 = Path(output_mp4 or html_path.parent / "output" / "render.mp4")
        output_mp4.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "node",
            str(self.render_script),
            "--html", str(html_path),
            "--output", str(output_mp4),
            "--duration", str(duration),
            "--fps", str(fps)
        ]

        if audio_path and Path(audio_path).exists():
            cmd.extend(["--audio", str(audio_path)])

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()

        process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"CDP Video Rendering failed with exit code {process.returncode}")

        return output_mp4
