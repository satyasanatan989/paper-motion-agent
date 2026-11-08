"""
Master Director Engine for PaperMotion AI.
Orchestrates the entire topic-driven pipeline:
Topic -> Research -> Script -> Storyboard -> Cloned Voiceover -> Adaptive Foley BGM ->
Dynamic Web Stage Assembly -> Headless CDP Video -> Automated Quality Control (QC).
"""

from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import subprocess
import time
import json
import soundfile as sf
import numpy as np
import sys

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

try:
    from agent.script_engine import ScriptEngine, Chapter
    from voice.jugnu_cloner import JugnuVoiceCloner
    from voice.indicf5_engine import IndicF5VoiceEngine
    from voice.audio_master import AudioMasterEngine
    from pipeline.cdp_streamer import CDPVideoRenderer
    from storyboard.generator import StoryboardGenerator, StoryboardPlan
    from visual_engine.scene_composer import DynamicSceneComposer
    from quality_control.validator import QualityValidator, QualityReport
except ImportError:
    from .script_engine import ScriptEngine, Chapter
    from ..voice.jugnu_cloner import JugnuVoiceCloner
    from ..voice.indicf5_engine import IndicF5VoiceEngine
    from ..voice.audio_master import AudioMasterEngine
    from ..pipeline.cdp_streamer import CDPVideoRenderer
    from ..storyboard.generator import StoryboardGenerator, StoryboardPlan
    from ..visual_engine.scene_composer import DynamicSceneComposer
    from ..quality_control.validator import QualityValidator, QualityReport

class PaperMotionDirector:
    """
    Autonomous Video Director agent for MeanwhileMayank / Vox style micro-documentaries.
    Capable of handling arbitrary topics, dynamic visual storyboards, and automated QC.
    """

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        use_indicf5_fallback: bool = True
    ):
        self.output_dir = Path(output_dir or Path.cwd() / "output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_fallback = use_indicf5_fallback
        self.script_engine = ScriptEngine()
        self.audio_master = AudioMasterEngine()
        self.cdp_renderer = CDPVideoRenderer()
        self.storyboard_gen = StoryboardGenerator()
        self.scene_composer = DynamicSceneComposer()
        self.qc_validator = QualityValidator()

    def produce_documentary(
        self,
        topic: str,
        reference_audio_or_video: Union[str, Path],
        project_name: str = "viral_documentary",
        hf_token: Optional[str] = None,
        language: str = "hinglish",
        fps: int = 30,
        skip_qc: bool = False
    ) -> Path:
        """
        Executes the entire autonomous video production pipeline.
        """
        print(f"\n=======================================================")
        print(f"🎬 [PaperMotion AI Director] Starting Production: {topic}")
        print(f"=======================================================\n")

        # Step 1: Topic-Driven Scripting & Chapter Structuring
        print("📝 [1/5] Generating topic-driven high-retention script...")
        chapters = self.script_engine.generate_script(topic=topic, language=language)
        genre = chapters[0].genre if hasattr(chapters[0], 'genre') else "general_explainer"
        print(f"       -> Generated {len(chapters)} chapters (Domain: {genre}).")

        # Step 2: Intelligent Visual Storyboard Generation
        print("\n📋 [2/5] Synthesizing validated multi-layer visual storyboard...")
        storyboard = self.storyboard_gen.generate_storyboard(
            topic=topic,
            chapters=chapters,
            project_name=project_name,
            language=language,
            genre=genre,
            fps=fps
        )
        storyboard_path = self.output_dir / f"{project_name}_storyboard.json"
        storyboard.save_json(storyboard_path)
        print(f"       -> Storyboard saved & validated: {storyboard_path}")

        # Step 3: Voice Cloning & Audio Synthesis
        print("\n🎙️ [3/5] Synthesizing Voiceover (Jugnu / IndicF5 / Edge-TTS)...")
        voice_wav = self.output_dir / f"{project_name}_narration.wav"
        ref_path = Path(reference_audio_or_video)
        narration_duration = 0.0

        # Attempt Jugnu Pocket TTS first
        voice_synthesized = False
        try:
            cloner = JugnuVoiceCloner(hf_token=hf_token)
            print("       -> Initializing Jugnu Pocket TTS (AltSlate-Labs)...")
            cloner.clone_voice(ref_path)
            full_text = " ".join(ch.narration_hinglish for ch in chapters)
            cloner.synthesize(full_text, output_path=voice_wav)
            voice_synthesized = True
            print("       -> [SUCCESS] Synthesized via Jugnu Pocket TTS.")
        except Exception as e:
            print(f"       -> [NOTICE] Jugnu Pocket TTS not active: {e}")
            if self.use_fallback:
                # Try IndicF5 next
                try:
                    indic_engine = IndicF5VoiceEngine()
                    if indic_engine.is_available():
                        print("       -> Synthesizing via local IndicF5 DiT flow-matching engine...")
                        ch_dicts = [{"text": ch.narration_hinglish} for ch in chapters]
                        narration_duration = indic_engine.synthesize_chapters(
                            ch_dicts,
                            ref_audio=ref_path,
                            ref_text=topic,
                            output_wav=voice_wav
                        )
                        voice_synthesized = True
                        print(f"       -> [SUCCESS] Synthesized via IndicF5 ({narration_duration:.2f}s).")
                except Exception as e_ind:
                    print(f"       -> [NOTICE] IndicF5 fallback exception: {e_ind}")

                # Edge-TTS fallback (100% reliable local neural Hinglish)
                if not voice_synthesized:
                    print("       -> Engaging neural speech synthesizer (hi-IN-MadhurNeural)...")
                    try:
                        narration_duration = self._synthesize_neural_hinglish(chapters, voice_wav)
                        voice_synthesized = True
                        print(f"       -> [SUCCESS] Synthesized via Neural Speech Engine ({narration_duration:.2f}s).")
                    except Exception as e_edge:
                        print(f"       -> [NOTICE] Neural TTS exception: {e_edge}")

        # Calculate actual audio duration
        if voice_wav.exists():
            v_data, v_sr = sf.read(str(voice_wav))
            narration_duration = len(v_data) / v_sr
            # Synchronize storyboard scenes with actual chapter durations
            for i, ch in enumerate(chapters):
                if i < len(storyboard.scenes):
                    if hasattr(ch, 'end_sec') and ch.end_sec and hasattr(ch, 'start_sec'):
                        storyboard.scenes[i].duration = round(ch.end_sec - ch.start_sec, 2)
            storyboard.estimated_duration = round(narration_duration, 2)
            storyboard_path = self.output_dir / f"{project_name}_storyboard.json"
            storyboard.save_json(storyboard_path)
        else:
            narration_duration = storyboard.estimated_duration

        # Step 4: Foley Sound Design & Dynamic Ducking
        print("\n🎵 [4/5] Composing Genre-Adaptive Foley & Sidechain Ducked Soundtrack...")
        master_audio = self.output_dir / f"{project_name}_soundtrack.mp3"
        if voice_wav.exists():
            self.audio_master.mix_soundtrack_with_ducking_adaptive(
                voiceover_wav=voice_wav,
                output_mp3=master_audio,
                genre=genre,
                bgm_volume=0.20
            )
        else:
            bgm = self.audio_master.generate_adaptive_bgm(narration_duration, genre=genre)
            sf.write(str(master_audio.with_suffix(".wav")), bgm, 44100)
            master_audio = master_audio.with_suffix(".wav")
        print(f"       -> Master soundtrack ready: {master_audio}")

        # Step 5: Dynamic Scene Assembly & Headless CDP Render
        print("\n🎥 [5/5] Assembling Stage & Rendering 1080x1920 (9:16) Video...")
        stage_dir = self.output_dir / "stage"
        html_entry = self.scene_composer.compose_stage(storyboard, stage_dir)
        output_mp4 = self.output_dir / f"{project_name}.mp4"

        final_video = self.cdp_renderer.render(
            html_path=html_entry,
            audio_path=master_audio,
            output_mp4=output_mp4,
            duration=narration_duration,
            fps=fps
        )

        # Step 6: Automated Video Quality Control
        if not skip_qc:
            print("\n🔍 [Quality Control] Running automated compliance check...")
            qc_report = self.qc_validator.inspect_video(output_mp4, expected_duration=narration_duration)
            qc_report_path = self.output_dir / "quality_report.json"
            qc_report.save_json(qc_report_path)
            print(f"       -> QC Status: {qc_report.status} (Report: {qc_report_path})")
            if qc_report.warnings:
                for w in qc_report.warnings:
                    print(f"          [WARN] {w}")

        print("\n=======================================================")
        print(f"✅ Production Complete! Master Deliverable:")
        print(f"   {final_video}")
        print("=======================================================\n")
        return final_video

    def _synthesize_neural_hinglish(self, chapters: List[Chapter], output_wav: Path) -> float:
        """Fallback neural Hinglish speech synthesis using local edge-tts."""
        import edge_tts
        import asyncio

        async def _run():
            segments = []
            cur_t = 0.0
            sr = 44100

            for ch in chapters:
                tmp_mp3 = self.output_dir / f"tmp_ch_{ch.chapter_num}.mp3"
                comm = edge_tts.Communicate(ch.narration_hinglish, "hi-IN-MadhurNeural", rate="+12%", pitch="+0Hz")
                await comm.save(str(tmp_mp3))

                ch_wav = self.output_dir / f"tmp_ch_{ch.chapter_num}.wav"
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(tmp_mp3),
                    "-ar", "44100", "-ac", "1", str(ch_wav)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                tmp_mp3.unlink(missing_ok=True)

                data, _ = sf.read(str(ch_wav))
                dur = len(data) / sr
                ch.start_sec = round(cur_t, 2)
                ch.end_sec = round(cur_t + dur, 2)

                segments.append(data)
                # 350ms silence pause between chapters
                silence = np.zeros(int(0.35 * sr), dtype=np.float32)
                segments.append(silence)
                cur_t += dur + 0.35
                ch_wav.unlink(missing_ok=True)

            master_data = np.concatenate(segments)
            sf.write(str(output_wav), master_data, sr)
            return round(cur_t, 2)

        return asyncio.run(_run())
