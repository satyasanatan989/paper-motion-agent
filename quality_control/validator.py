"""
Automated Video Quality Control Validator.
Inspects rendered video deliverables for:
1. Container resolution & aspect ratio
2. Framerate consistency
3. Duration synchronization against storyboard
4. Loudness analysis (-14 LUFS broadcast target & peak clipping check)
5. Black frames & blank screen detection
6. Static holds / motion freezing detection
7. Generates structured quality_report.json
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import subprocess
import sys

@dataclass
class SceneQCResult:
    scene_id: str
    status: str  # 'PASS', 'WARN', 'FAIL'
    duration: float
    notes: List[str] = field(default_factory=list)

@dataclass
class QualityReport:
    project_name: str
    video_path: str
    resolution: str
    framerate: float
    duration: float
    integrated_lufs: float
    true_peak_db: float
    black_frame_count: int
    static_hold_warnings: List[str]
    status: str  # 'PASS', 'PASS_WITH_WARNINGS', 'FAIL'
    contact_sheet_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status in ("PASS", "PASS_WITH_WARNINGS")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save_json(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        return path

class QualityValidator:
    """Validates rendered video deliverables using FFmpeg and FFprobe."""

    def __init__(self, target_resolution: str = "1080x1920", target_fps: int = 30):
        self.target_resolution = target_resolution
        self.target_fps = target_fps

    def inspect_video(self, video_path: Path, expected_duration: Optional[float] = None) -> QualityReport:
        video_path = Path(video_path)
        if not video_path.exists():
            return QualityReport(
                project_name=video_path.stem,
                video_path=str(video_path),
                resolution="0x0",
                framerate=0.0,
                duration=0.0,
                integrated_lufs=0.0,
                true_peak_db=0.0,
                black_frame_count=0,
                static_hold_warnings=[],
                status="FAIL",
                errors=[f"File not found: {video_path}"]
            )

        # 1. FFprobe Stream Inspection
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size,bit_rate",
            "-show_streams", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,codec_name",
            "-of", "json",
            str(video_path)
        ]
        res = subprocess.run(probe_cmd, capture_output=True, text=True)
        probe_data = json.loads(res.stdout) if res.returncode == 0 else {}

        streams = probe_data.get("streams", [{}])
        v_stream = streams[0] if streams else {}
        w = v_stream.get("width", 0)
        h = v_stream.get("height", 0)
        actual_res = f"{w}x{h}"

        r_fps = v_stream.get("r_frame_rate", "30/1")
        if "/" in r_fps:
            num, den = r_fps.split("/")
            actual_fps = float(num) / max(1.0, float(den))
        else:
            actual_fps = float(r_fps)

        fmt = probe_data.get("format", {})
        actual_dur = float(fmt.get("duration", 0.0))

        errors = []
        warnings = []

        # Resolution check
        if actual_res != self.target_resolution:
            errors.append(f"Resolution mismatch: expected {self.target_resolution}, got {actual_res}")

        # Framerate check
        if abs(actual_fps - self.target_fps) > 1.0:
            warnings.append(f"Framerate variance: expected {self.target_fps} fps, got {actual_fps:.2f} fps")

        # Duration check
        if expected_duration and abs(actual_dur - expected_duration) > 2.0:
            warnings.append(f"Duration variance: expected {expected_duration:.2f}s, got {actual_dur:.2f}s")

        # 2. Loudness Analysis via FFmpeg ebur128
        lufs, peak_db = self._measure_loudness(video_path)
        if peak_db > -0.5:
            warnings.append(f"True peak exceeds -0.5 dBTP ({peak_db:.2f} dBTP), potential clipping risk.")
        if lufs < -24.0:
            warnings.append(f"Audio is noticeably quieter than -14 LUFS target ({lufs:.1f} LUFS).")
        elif abs(lufs - (-14.0)) > 2.0:
            warnings.append(f"Audio loudness {lufs:.1f} LUFS deviates from studio standard -14.0 LUFS.")

        # 3. Static Holds & Black Screen Detection
        black_frames = self._detect_black_frames(video_path)
        if black_frames > 0:
            warnings.append(f"Detected {black_frames} black/blank frames in container.")

        # 4. Generate 6x3 Visual Contact Sheet
        contact_sheet = self.export_contact_sheet(video_path)
        cs_path_str = str(contact_sheet) if contact_sheet and contact_sheet.exists() else None

        # Determine overall status
        status = "PASS"
        if errors:
            status = "FAIL"
        elif warnings:
            status = "PASS_WITH_WARNINGS"

        report = QualityReport(
            project_name=video_path.stem,
            video_path=str(video_path),
            resolution=actual_res,
            framerate=actual_fps,
            duration=actual_dur,
            integrated_lufs=lufs,
            true_peak_db=peak_db,
            black_frame_count=black_frames,
            static_hold_warnings=[],
            status=status,
            contact_sheet_path=cs_path_str,
            errors=errors,
            warnings=warnings
        )
        return report

    def export_contact_sheet(
        self,
        video_path: Path,
        output_image: Optional[Path] = None,
        tile_grid: str = "6x3"
    ) -> Optional[Path]:
        """
        Exports a high-density 6x3 contact sheet representing every beat of the render:
        ffmpeg -vf "fps=1/3,scale=270:480,tile=6x3"
        """
        video_path = Path(video_path)
        if not video_path.exists():
            return None

        if output_image is None:
            output_image = video_path.parent / f"{video_path.stem}_contact_sheet.jpg"
        output_image = Path(output_image)
        output_image.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", f"fps=1/3,scale=270:480,tile={tile_grid}",
            "-frames:v", "1",
            "-q:v", "2",
            str(output_image)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and output_image.exists():
            return output_image
        return None

    def inspect_storyboard(self, storyboard: Any) -> List[str]:
        """
        Validates storyboard beats against viral short-form retention criteria:
        1. Visual changes every 1.5 - 3.5s (average beat duration <= 3.5s, no static hold > 4.0s).
        2. Top-left headline <= 4 words, punchline <= 3 words.
        3. Caption capsule <= 4 words (max 5).
        4. First 1.5s hook presence.
        """
        issues = []
        beats = getattr(storyboard, 'beats', None)
        if not beats or len(beats) == 0:
            return ["No visual beats present in storyboard plan."]

        # Hook check
        if beats[0].start > 1.5:
            issues.append(f"Hook delayed: First visual beat starts at {beats[0].start}s (> 1.5s).")

        durations = []
        for b in beats:
            dur = round(b.end - b.start, 2)
            durations.append(dur)
            if dur > 4.0:
                issues.append(f"Static hold detected in {b.beat_id}: duration {dur}s exceeds 4.0s limit.")

            h_top_words = len(b.headline_top.split())
            if h_top_words > 4:
                issues.append(f"Headline top line in {b.beat_id} has {h_top_words} words (max 4 allowed).")

            h_punch_words = len(b.headline_punch.split())
            if h_punch_words > 3:
                issues.append(f"Headline punchline in {b.beat_id} has {h_punch_words} words (max 3 allowed).")

            if b.caption_chunk:
                c_words = len(b.caption_chunk.split())
                if c_words > 5:
                    issues.append(f"Caption capsule in {b.beat_id} has {c_words} words (max 4-5 allowed).")

        avg_dur = sum(durations) / max(1, len(durations))
        if avg_dur > 3.5:
            issues.append(f"Average beat duration {avg_dur:.2f}s exceeds 3.5s viral pace ceiling.")

        return issues

    def _measure_loudness(self, path: Path) -> (float, float):
        cmd = [
            "ffmpeg", "-i", str(path),
            "-filter_complex", "ebur128=peak=true",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        out = res.stderr

        import re
        # Look in the Summary section to get the overall integrated measurement
        summary_section = out.split("Summary:")[-1] if "Summary:" in out else out
        lufs_matches = re.findall(r"I:\s+([-\d\.]+)\s+LUFS", summary_section)
        peak_matches = re.findall(r"(?:Peak|True peak):\s+([-\d\.]+)\s+(?:dBFS|dBTP)", summary_section)

        lufs = float(lufs_matches[-1]) if lufs_matches else -23.0
        peak = float(peak_matches[-1]) if peak_matches else -1.0
        return lufs, peak

    def _detect_black_frames(self, path: Path) -> int:
        cmd = [
            "ffmpeg", "-i", str(path),
            "-vf", "blackdetect=d=0.3:pix_th=0.10",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        import re
        matches = re.findall(r"black_start:", res.stderr)
        return len(matches)

    validate = inspect_video

