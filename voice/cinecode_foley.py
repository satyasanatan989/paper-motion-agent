"""
CineCode-Inspired Procedural Foley Engine for Food Code Explainers.
Synthesizes documentary-grade tactile sound effects:
- Paper card whooshes & table slides
- Scotch tape snap & peel clicks
- Pushpin metallic pings & wooden desk thuds
- Heavy rubber evidence stamp slams (with sub-bass body)
- Mechanical split-flap & odometer ticks
- Gastric acid bubble pops & scanner chirps
"""

import math
from pathlib import Path
from typing import List, Optional, Union
import numpy as np
import soundfile as sf
import subprocess

class CineCodeFoleyEngine:
    """
    Synthesizes tactile, documentary-standard Foley effects aligned to kinetic animation cues.
    """

    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate

    def generate_card_whoosh(self, duration: float = 0.35) -> np.ndarray:
        """Paper card sliding fast across desk: filtered noise sweep with exponential decay."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        # White noise base
        noise = (np.random.rand(num_samples) - 0.5) * 2.0
        # Envelope: rapid attack (0.05s) followed by smooth dissipation
        attack_len = int(self.sr * 0.05)
        attack = np.linspace(0, 1, attack_len)
        decay = np.exp(-12.0 * (t[attack_len:] - t[attack_len]))
        env = np.concatenate([attack, decay])[:num_samples]
        # Frequency modulation: pitch drops as card slows down
        sweep = np.sin(2 * np.pi * (450 + 600 * (1.0 - t / duration)) * t)
        whoosh = (noise * 0.75 + sweep * 0.25) * env * 0.35
        return whoosh.astype(np.float32)

    def generate_tape_snap(self, duration: float = 0.18) -> np.ndarray:
        """Scotch tape adhesive slap: sharp transient + adhesive stretch click."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        # Dual pulse
        p1 = np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 60)
        p2 = (np.random.rand(num_samples) - 0.5) * np.exp(-t * 35) * 0.6
        tape = (p1 * 0.7 + p2 * 0.5) * 0.40
        return tape.astype(np.float32)

    def generate_pushpin_thud(self, duration: float = 0.22) -> np.ndarray:
        """Pushpin slammed into desk: high metallic ping + wood board thump."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        # Metallic needle ping (3.2 kHz)
        ping = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 45) * 0.35
        # Wood desk body (125 Hz)
        thump = np.sin(2 * np.pi * 125 * t) * np.exp(-t * 22) * 0.55
        pin = (ping + thump) * 0.50
        return pin.astype(np.float32)

    def generate_rubber_stamp_slam(self, duration: float = 0.45) -> np.ndarray:
        """Heavy warning rubber stamp: low-end sub boom (70 Hz) + sharp slap transient."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        # Sub-bass body (70 Hz decaying)
        sub = np.sin(2 * np.pi * (70 - 25 * t / duration) * t) * np.exp(-t * 8.5) * 0.85
        # Rubber impact slap transient (850 Hz)
        slap = (np.random.rand(num_samples) - 0.5) * np.exp(-t * 50) * 0.55
        mid = np.sin(2 * np.pi * 850 * t) * np.exp(-t * 35) * 0.30
        stamp = (sub * 0.65 + slap * 0.45 + mid * 0.25) * 0.65
        return stamp.astype(np.float32)

    def generate_split_flap_click(self, duration: float = 0.05) -> np.ndarray:
        """Crisp mechanical split-flap / odometer notch click."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        click = (
            np.sin(2 * np.pi * 2600 * t) * 0.5 +
            np.sin(2 * np.pi * 4200 * t) * 0.3 +
            (np.random.rand(num_samples) - 0.5) * 0.4
        ) * np.exp(-t * 90) * 0.28
        return click.astype(np.float32)

    def generate_acid_bubble_pop(self, duration: float = 0.12) -> np.ndarray:
        """Gastric acid liquid bubble pop: ascending chirp with rapid damping."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        freq = 420 + 380 * (t / duration)
        phase = 2 * np.pi * np.cumsum(freq) / self.sr
        pop = np.sin(phase) * np.exp(-t * 32) * 0.30
        return pop.astype(np.float32)

    def generate_scanner_tick(self, duration: float = 0.08) -> np.ndarray:
        """Digital nutrition barcode laser tick / data beep."""
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        beep = np.sin(2 * np.pi * 1750 * t) * np.exp(-t * 40) * 0.25
        return beep.astype(np.float32)

    def build_food_code_foley_track(
        self,
        total_duration: float,
        scene_starts: List[float]
    ) -> np.ndarray:
        """
        Builds a comprehensive, time-aligned Foley track across all 8 scenes.
        """
        num_samples = int(self.sr * total_duration)
        track = np.zeros(num_samples, dtype=np.float32)

        whoosh = self.generate_card_whoosh()
        tape = self.generate_tape_snap()
        pin = self.generate_pushpin_thud()
        stamp = self.generate_rubber_stamp_slam()
        click = self.generate_split_flap_click()
        pop = self.generate_acid_bubble_pop()
        scan = self.generate_scanner_tick()

        def overlay(sample: np.ndarray, at_sec: float, gain: float = 1.0):
            idx = int(at_sec * self.sr)
            if idx < 0 or idx >= num_samples:
                return
            avail = min(len(sample), num_samples - idx)
            track[idx:idx + avail] += (sample[:avail] * gain)

        for s_idx, st in enumerate(scene_starts):
            # 1. Card entry whoosh on every scene start
            overlay(whoosh, st + 0.02, gain=0.45)
            # 2. Scotch tape slap
            overlay(tape, st + 0.25, gain=0.50)
            # 3. Pushpin click
            overlay(pin, st + 0.35, gain=0.55)

            # 4. Rubber warning stamp slams on every scene at t = 0.85s (synchronized with impact shake)
            overlay(stamp, st + 0.85, gain=0.75)

            # 5. Scene-specific kinetic audio cues:
            if s_idx == 0:  # Scene 001: Split-flap clock rapid flipping
                for flip_t in np.linspace(st + 0.5, st + 2.5, 8):
                    overlay(click, flip_t, gain=0.35)
            elif s_idx == 2:  # Scene 003: Acid bubbles & clock flip
                for bub_t in [st + 0.8, st + 1.4, st + 2.1, st + 2.9, st + 3.8, st + 4.7]:
                    overlay(pop, bub_t, gain=0.40)
                for flip_t in np.linspace(st + 0.6, st + 2.8, 6):
                    overlay(click, flip_t, gain=0.30)
            elif s_idx == 5:  # Scene 006: Sodium odometer rapid climbing clicks
                for odo_t in np.linspace(st + 0.5, st + 2.8, 18):
                    overlay(click, odo_t, gain=0.38)
                for scan_t in [st + 0.6, st + 1.2, st + 1.8]:
                    overlay(scan, scan_t, gain=0.40)
            elif s_idx == 7:  # Scene 008: Final Food Code signature slam
                overlay(stamp, st + 1.10, gain=0.90)

        # Normalize overall Foley track so it sits beautifully in mix
        max_peak = np.max(np.abs(track))
        if max_peak > 0:
            track = (track / max_peak) * 0.70

        return track

    def mix_production_soundtrack(
        self,
        voiceover_wav: Union[str, Path],
        output_path: Union[str, Path],
        total_duration: float,
        scene_starts: List[float],
        bgm_volume: float = 0.16,
        foley_volume: float = 0.32,
        ducking_ratio: float = 0.30
    ) -> Path:
        """
        Renders the complete studio master audio track:
        [Voiceover] + [Genre-Adaptive BGM] + [Tactile Foley]
        Applies sidechain ducking and masters cleanly to broadcast standards.
        """
        voiceover_wav = Path(voiceover_wav)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        v_data, v_sr = sf.read(str(voiceover_wav))
        if v_data.ndim > 1:
            v_data = np.mean(v_data, axis=1)

        dur = len(v_data) / v_sr
        target_dur = max(dur, total_duration)

        # Build Foley track
        foley = self.build_food_code_foley_track(target_dur, scene_starts)
        temp_foley_wav = output_path.parent / "temp_foley.wav"
        sf.write(str(temp_foley_wav), foley, self.sr)

        # Generate Adaptive BGM
        from voice.audio_master import AudioMasterEngine
        master_engine = AudioMasterEngine(sample_rate=self.sr)
        bgm = master_engine.generate_adaptive_bgm(target_dur + 0.5, genre="health_bio")
        temp_bgm_wav = output_path.parent / "temp_bgm.wav"
        sf.write(str(temp_bgm_wav), bgm, self.sr)

        # FFmpeg Multi-layer Mix with Sidechain Ducking
        # Music & Foley are ducked when voiceover is active
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_bgm_wav),
            "-i", str(temp_foley_wav),
            "-i", str(voiceover_wav),
            "-filter_complex",
            f"[0:a]volume={bgm_volume}[m];"
            f"[1:a]volume={foley_volume}[f];"
            f"[m][f]amix=inputs=2:duration=first[bed];"
            f"[bed][2:a]sidechaincompress=threshold=0.08:ratio=4:attack=40:release=300[ducked_bed];"
            f"[ducked_bed][2:a]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
            f"[mixed]volume=2.25,alimiter=limit=-1.0dB:attack=5:release=50[outa]",
            "-map", "[outa]",
            "-ar", "44100",
            "-b:a", "256k",
            str(output_path)
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            # Software fallback
            target_len = int(target_dur * self.sr)
            v_resampled = np.interp(
                np.linspace(0, len(v_data), target_len, False),
                np.arange(len(v_data)),
                v_data
            )
            bgm_cut = bgm[:target_len]
            foley_cut = foley[:target_len]
            mixed = (v_resampled * 0.90) + (bgm_cut * bgm_volume * ducking_ratio) + (foley_cut * foley_volume * 0.7)
            sf.write(str(output_path), mixed, self.sr)

        if temp_bgm_wav.exists():
            temp_bgm_wav.unlink(missing_ok=True)
        if temp_foley_wav.exists():
            temp_foley_wav.unlink(missing_ok=True)

        return output_path
