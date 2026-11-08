"""
Cinematic Audio Master & Foley Engine for PaperMotion AI.
Synthesizes procedural war drums, meditative bansuri, paper tears, blade clashes,
and mixes voiceover with intelligent dynamic audio ducking.
"""

from pathlib import Path
from typing import Optional, Union, List
import numpy as np
import soundfile as sf
import subprocess

class AudioMasterEngine:
    """
    Audio post-production and Foley generator for viral papercraft explainers.
    """

    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate

    def generate_foley_clash(self, duration: float = 0.6) -> np.ndarray:
        """Procedural metallic blade clash transient with reverb tail."""
        t = np.linspace(0, duration, int(self.sr * duration), False)
        # Metallic high frequencies + impact noise burst
        metallic = (
            np.sin(2 * np.pi * 2150 * t) * 0.4 +
            np.sin(2 * np.pi * 3420 * t) * 0.3 +
            np.sin(2 * np.pi * 5180 * t) * 0.2
        )
        noise = (np.random.rand(len(t)) - 0.5) * 0.5
        envelope = np.exp(-t * 14)
        return (metallic + noise) * envelope * 0.4

    def generate_paper_rustle(self, duration: float = 0.4) -> np.ndarray:
        """Procedural tactile paper texture rustle / page turn."""
        t = np.linspace(0, duration, int(self.sr * duration), False)
        noise = (np.random.rand(len(t)) - 0.5)
        # Bandpass filter approximation via windowed modulation
        envelope = np.sin(np.pi * t / duration) ** 2
        flutter = 1.0 + 0.3 * np.sin(2 * np.pi * 35 * t)
        return noise * envelope * flutter * 0.25

    def generate_cinematic_bgm(self, duration: float, has_war_transition: bool = True) -> np.ndarray:
        """
        Synthesizes a multi-section soundtrack:
        - Section A: Deep Nagada war drums with intense cinematic cadence
        - Section B: Meditative Bansuri flute with peaceful ambient harmonics
        """
        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        bgm = np.zeros(num_samples, dtype=np.float32)

        # 1. Warm sub-bass foundation (45 Hz & 90 Hz drone)
        drone = np.sin(2 * np.pi * 45 * t) * 0.08 + np.sin(2 * np.pi * 90 * t) * 0.05
        bgm += drone

        # 2. Section A: War Drums (0s to 38% of total duration)
        war_cutoff = duration * 0.38 if has_war_transition else duration
        drum_interval = 0.55  # ~110 BPM
        drum_times = np.arange(0.2, war_cutoff, drum_interval)

        for d_t in drum_times:
            d_idx = int(d_t * self.sr)
            hit_dur = 0.4
            hit_samples = int(hit_dur * self.sr)
            if d_idx + hit_samples < num_samples:
                ht = np.linspace(0, hit_dur, hit_samples, False)
                # Pitch sweep from 140Hz down to 55Hz
                freq = 55 + 85 * np.exp(-ht * 20)
                phase = 2 * np.pi * np.cumsum(freq) / self.sr
                drum_hit = np.sin(phase) * np.exp(-ht * 9) * 0.45
                bgm[d_idx:d_idx + hit_samples] += drum_hit

        # 3. Section B: Meditative Bansuri Flute (from war_cutoff to end)
        if has_war_transition:
            peace_t = t[t >= war_cutoff] - war_cutoff
            peace_idx = int(war_cutoff * self.sr)
            if len(peace_t) > 0:
                # Pentatonic notes: D4 (293.66), F#4 (369.99), A4 (440), B4 (493.88)
                notes = [293.66, 369.99, 440.0, 493.88]
                flute_signal = np.zeros(len(peace_t), dtype=np.float32)
                note_dur = 2.0
                for i, n_t in enumerate(np.arange(0, peace_t[-1], note_dur)):
                    n_idx = int(n_t * self.sr)
                    cur_note = notes[(i % len(notes))]
                    avail = min(int(note_dur * self.sr), len(peace_t) - n_idx)
                    if avail > 0:
                        seg_t = peace_t[n_idx:n_idx + avail]
                        vibrato = 1.0 + 0.02 * np.sin(2 * np.pi * 5.5 * seg_t)
                        flute = np.sin(2 * np.pi * cur_note * vibrato * seg_t)
                        # Add warm second harmonic
                        flute += 0.3 * np.sin(2 * np.pi * cur_note * 2 * seg_t)
                        env = np.sin(np.pi * (seg_t - seg_t[0]) / (seg_t[-1] - seg_t[0] + 1e-5)) ** 1.5
                        flute_signal[n_idx:n_idx + avail] += (flute * env * 0.18).astype(np.float32)
                bgm[peace_idx:] += flute_signal

        # Normalize and master
        max_val = np.max(np.abs(bgm))
        if max_val > 0:
            bgm = (bgm / max_val) * 0.85
        return bgm

    def mix_soundtrack_with_ducking(
        self,
        voiceover_wav: Union[str, Path],
        output_mp3: Union[str, Path],
        bgm_volume: float = 0.18,
        ducking_ratio: float = 0.35
    ) -> Path:
        """
        Dynamically ducks background music under the vocal narration using FFmpeg sidechain filter.
        """
        voiceover_wav = Path(voiceover_wav)
        output_mp3 = Path(output_mp3)
        output_mp3.parent.mkdir(parents=True, exist_ok=True)

        # Get voiceover duration
        v_data, v_sr = sf.read(str(voiceover_wav))
        duration = len(v_data) / v_sr

        # Generate synced BGM
        bgm_data = self.generate_cinematic_bgm(duration + 0.8)
        temp_bgm_wav = output_mp3.parent / "temp_bgm.wav"
        sf.write(str(temp_bgm_wav), bgm_data, self.sr)

        # FFmpeg Sidechain Compression (Ducking)
        # Music (stream 0) volume drops when voice (stream 1) speaks
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_bgm_wav),
            "-i", str(voiceover_wav),
            "-filter_complex",
            f"[0:a]volume={bgm_volume}[bgm];"
            f"[bgm][1:a]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=350[ducked_bgm];"
            f"[ducked_bgm][1:a]amix=inputs=2:duration=first:dropout_transition=2[outa]",
            "-map", "[outa]",
            "-b:a", "192k",
            str(output_mp3)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            # Fallback direct software mixing
            mixed = np.zeros(len(v_data), dtype=np.float32)
            bgm_resampled = bgm_data[:len(v_data)]
            mixed = (v_data * 0.95) + (bgm_resampled * bgm_volume * ducking_ratio)
            sf.write(str(output_mp3.with_suffix(".wav")), mixed, v_sr)
            return output_mp3.with_suffix(".wav")

        if temp_bgm_wav.exists():
            temp_bgm_wav.unlink(missing_ok=True)

        return output_mp3
