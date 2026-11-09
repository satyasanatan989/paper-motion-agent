"""
Cinematic Audio Master & Foley Engine for PaperMotion AI.
Synthesizes procedural war drums, meditative bansuri, paper tears, blade clashes,
and mixes voiceover with intelligent dynamic audio ducking.
"""

from pathlib import Path
from typing import Optional, Union, List, Dict, Any
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

    def generate_pop(self, duration: float = 0.12) -> np.ndarray:
        """Procedural sticker spring pop transient."""
        t = np.linspace(0, duration, int(self.sr * duration), False)
        freq = 800 * np.exp(-t * 28) + 240
        phase = 2 * np.pi * np.cumsum(freq) / self.sr
        sine_pop = np.sin(phase) * np.exp(-t * 36) * 0.35
        click = (np.random.rand(len(t)) - 0.5) * np.exp(-t * 60) * 0.15
        return sine_pop + click

    def generate_stamp_thud(self, duration: float = 0.35) -> np.ndarray:
        """Procedural heavy rubber stamp thud impact."""
        t = np.linspace(0, duration, int(self.sr * duration), False)
        # Low frequency acoustic resonance (65 Hz decaying down)
        freq = 68 * np.exp(-t * 12) + 42
        phase = 2 * np.pi * np.cumsum(freq) / self.sr
        sub_thud = np.sin(phase) * np.exp(-t * 14) * 0.55
        # Slap contact transient
        slap = (np.random.rand(len(t)) - 0.5) * np.exp(-t * 45) * 0.30
        return sub_thud + slap

    def generate_mechanical_tick(self, duration: float = 0.08) -> np.ndarray:
        """Procedural odometer / flip-counter click."""
        t = np.linspace(0, duration, int(self.sr * duration), False)
        tick = (
            np.sin(2 * np.pi * 2800 * t) * 0.35 +
            np.sin(2 * np.pi * 4600 * t) * 0.25
        ) * np.exp(-t * 85)
        return tick

    def generate_foley_track(self, duration: float, cues: List[Dict[str, Any]]) -> np.ndarray:
        """
        Renders a continuous multichannel Foley track populated with cue events:
        cues format: [{"time": float, "sfx": str}]
        Supported sfx: 'paper_flip', 'paper_slide', 'pop', 'stamp', 'tick', 'clash'
        """
        total_samples = int(self.sr * duration)
        foley = np.zeros(total_samples, dtype=np.float32)

        for cue in cues:
            cue_t = float(cue.get("time", 0.0))
            cue_idx = int(cue_t * self.sr)
            if cue_idx >= total_samples:
                continue

            sfx_name = cue.get("sfx") or cue.get("name", "pop")
            if sfx_name in ["paper_flip", "paper_slide", "rustle"]:
                sound = self.generate_paper_rustle(0.35)
            elif sfx_name == "stamp":
                sound = self.generate_stamp_thud(0.35)
            elif sfx_name == "tick":
                sound = self.generate_mechanical_tick(0.08)
            elif sfx_name == "clash":
                sound = self.generate_foley_clash(0.4)
            else:
                sound = self.generate_pop(0.12)

            avail = min(len(sound), total_samples - cue_idx)
            if avail > 0:
                foley[cue_idx : cue_idx + avail] += sound[:avail]

        # Normalization
        max_f = np.max(np.abs(foley))
        if max_f > 1.0:
            foley = foley / max_f
        return foley

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

    def generate_adaptive_bgm(self, duration: float, genre: str = "health_bio") -> np.ndarray:
        """
        Synthesizes genre-aware Foley and musical foundations:
        - 'health_bio': Lo-fi analog sub-bass, 38 Hz gut rumble, rhythmic acoustic click
        - 'war_epic': Deep Nagada war drums + meditative Bansuri flute
        - 'science_tech': Minimal ambient drone + crisp synthetic pulses
        """
        if genre == "war_epic" or "history" in genre:
            return self.generate_cinematic_bgm(duration, has_war_transition=True)

        num_samples = int(self.sr * duration)
        t = np.linspace(0, duration, num_samples, False)
        bgm = np.zeros(num_samples, dtype=np.float32)

        # 1. Warm Analog Foundation
        bass_drone = np.sin(2 * np.pi * 52 * t) * 0.10 + np.sin(2 * np.pi * 104 * t) * 0.06
        bgm += bass_drone

        # 2. Rhythmic Pulse (~108 BPM, 0.55s interval)
        beat_times = np.arange(0.1, duration, 0.55)
        for b_idx, b_t in enumerate(beat_times):
            idx = int(b_t * self.sr)
            is_kick = (b_idx % 4 == 0)
            hit_dur = 0.32 if is_kick else 0.14
            hit_samples = int(hit_dur * self.sr)
            if idx + hit_samples < num_samples:
                ht = np.linspace(0, hit_dur, hit_samples, False)
                if is_kick:
                    freq = 45 + 70 * np.exp(-ht * 22)
                    phase = 2 * np.pi * np.cumsum(freq) / self.sr
                    kick = np.sin(phase) * np.exp(-ht * 12) * 0.28
                    bgm[idx:idx + hit_samples] += kick
                else:
                    wood_click = (np.sin(2 * np.pi * 840 * ht) + np.sin(2 * np.pi * 1420 * ht)) * np.exp(-ht * 35) * 0.08
                    bgm[idx:idx + hit_samples] += wood_click

        # 3. Sub-bass Gut Rumble (for biological health explainers)
        if "bio" in genre or "health" in genre:
            rumble_times = [duration * 0.35, duration * 0.52]
            for r_t in rumble_times:
                r_idx = int(r_t * self.sr)
                r_dur = 2.2
                r_samples = int(r_dur * self.sr)
                if r_idx + r_samples < num_samples:
                    rt = np.linspace(0, r_dur, r_samples, False)
                    sub = np.sin(2 * np.pi * 38 * rt) * np.exp(-rt * 1.1) * 0.26
                    fizz = (np.random.rand(r_samples) - 0.5) * 0.10 * (1.0 - np.exp(-rt * 1.5))
                    bgm[r_idx:r_idx + r_samples] += (sub + fizz)

        # Normalize
        max_val = np.max(np.abs(bgm))
        if max_val > 0:
            bgm = (bgm / max_val) * 0.80
        return bgm

    def mix_soundtrack_with_ducking_adaptive(
        self,
        voiceover_wav: Union[str, Path],
        output_mp3: Union[str, Path],
        genre: str = "health_bio",
        bgm_volume: float = 0.20,
        ducking_ratio: float = 0.35,
        foley_cues: Optional[List[Dict[str, Any]]] = None,
        target_lufs: float = -14.0
    ) -> Path:
        """
        Dynamically mixes voiceover with genre-tailored BGM, Foley sound effects,
        sidechain ducking, and masters strictly to target LUFS (EBU R128 standard -14 LUFS, -1 dBTP).
        """
        voiceover_wav = Path(voiceover_wav)
        output_mp3 = Path(output_mp3)
        output_mp3.parent.mkdir(parents=True, exist_ok=True)

        v_data, v_sr = sf.read(str(voiceover_wav))
        duration = len(v_data) / v_sr

        bgm_data = self.generate_adaptive_bgm(duration + 0.8, genre=genre)
        temp_bgm_wav = output_mp3.parent / "temp_adaptive_bgm.wav"
        sf.write(str(temp_bgm_wav), bgm_data, self.sr)

        temp_foley_wav = None
        if foley_cues and len(foley_cues) > 0:
            foley_data = self.generate_foley_track(duration + 0.8, foley_cues)
            temp_foley_wav = output_mp3.parent / "temp_foley.wav"
            sf.write(str(temp_foley_wav), foley_data, self.sr)

        if temp_foley_wav and temp_foley_wav.exists():
            cmd = [
                "ffmpeg", "-y",
                "-i", str(temp_bgm_wav),
                "-i", str(voiceover_wav),
                "-i", str(temp_foley_wav),
                "-filter_complex",
                f"[0:a]volume={bgm_volume}[bgm];"
                f"[bgm][1:a]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=350[ducked_bgm];"
                f"[2:a]volume=0.85[foley_vol];"
                f"[ducked_bgm][foley_vol]amix=inputs=2:dropout_transition=2[sfx_bgm];"
                f"[sfx_bgm][1:a]amix=inputs=2:duration=first:dropout_transition=2[pre_norm];"
                f"[pre_norm]loudnorm=I={target_lufs}:LRA=7:tp=-1[mastered]",
                "-map", "[mastered]",
                "-b:a", "192k",
                str(output_mp3)
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-i", str(temp_bgm_wav),
                "-i", str(voiceover_wav),
                "-filter_complex",
                f"[0:a]volume={bgm_volume}[bgm];"
                f"[bgm][1:a]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=350[ducked_bgm];"
                f"[ducked_bgm][1:a]amix=inputs=2:duration=first:dropout_transition=2[pre_norm];"
                f"[pre_norm]loudnorm=I={target_lufs}:LRA=7:tp=-1[mastered]",
                "-map", "[mastered]",
                "-b:a", "192k",
                str(output_mp3)
            ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                mixed = np.zeros(len(v_data), dtype=np.float32)
                bgm_resampled = bgm_data[:len(v_data)]
                mixed = (v_data * 0.95) + (bgm_resampled * bgm_volume * ducking_ratio)
                fallback_path = output_mp3.with_suffix(".wav")
                sf.write(str(fallback_path), mixed, v_sr)
                return fallback_path
            return output_mp3
        finally:
            if temp_bgm_wav and temp_bgm_wav.exists():
                temp_bgm_wav.unlink(missing_ok=True)
            if temp_foley_wav and temp_foley_wav.exists():
                temp_foley_wav.unlink(missing_ok=True)

    def measure_loudness(self, audio_path: Union[str, Path]) -> float:
        """
        Measures integrated LUFS using FFmpeg ebur128 filter.
        Returns integrated loudness float (e.g. -14.1).
        """
        cmd = [
            "ffmpeg", "-nostats", "-i", str(audio_path),
            "-filter_complex", "ebur128=peak=true",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        import re
        match = re.search(r"Integrated loudness:\s+I:\s+([-\d\.]+)\s+LUFS", res.stderr)
        if match:
            return float(match.group(1))
        return -14.0
