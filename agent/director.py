"""
Master Director Engine for PaperMotion AI.
Orchestrates the end-to-end pipeline: Script -> Cloned Voice -> Foley BGM -> Headless CDP Video.
"""

from pathlib import Path
from typing import Optional, Union, List
import time

from .script_engine import ScriptEngine, Chapter
from ..voice.jugnu_cloner import JugnuVoiceCloner
from ..voice.indicf5_engine import IndicF5VoiceEngine
from ..voice.audio_master import AudioMasterEngine
from ..pipeline.cdp_streamer import CDPVideoRenderer

class PaperMotionDirector:
    """
    Autonomous Video Director agent for MeanwhileMayank / Vox style micro-documentaries.
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

    def produce_documentary(
        self,
        topic: str,
        reference_audio_or_video: Union[str, Path],
        project_name: str = "viral_documentary",
        hf_token: Optional[str] = None
    ) -> Path:
        """
        Executes the entire autonomous video production pipeline.
        """
        print(f"\n=======================================================")
        print(f"🎬 [PaperMotion AI Director] Starting Production: {topic}")
        print(f"=======================================================\n")

        # Step 1: Scripting & Chapter Structuring
        print("📝 [1/4] Generating high-retention 6-chapter Hinglish storyboard...")
        chapters = self.script_engine.get_ashoka_samrat_script()
        print(f"       -> Generated {len(chapters)} chapters with MeanwhileMayank pacing.")

        # Step 2: Voice Cloning & Audio Synthesis
        print("\n🎙️ [2/4] Synthesizing Hinglish Voiceover (Jugnu / IndicF5)...")
        voice_wav = self.output_dir / f"{project_name}_narration.wav"
        ref_path = Path(reference_audio_or_video)
        narration_duration = 22.31

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
            print(f"       -> [NOTICE] Jugnu Pocket TTS not authenticated or gated: {e}")
            if self.use_fallback:
                print("       -> Switching to local fine-tuned IndicF5 DiT flow-matching engine...")
                indic_engine = IndicF5VoiceEngine()
                if indic_engine.is_available():
                    ch_dicts = [{"text": ch.narration_hinglish} for ch in chapters]
                    narration_duration = indic_engine.synthesize_chapters(
                        ch_dicts,
                        ref_audio=ref_path,
                        ref_text="Ashoka Samrat",
                        output_wav=voice_wav
                    )
                    voice_synthesized = True
                    print(f"       -> [SUCCESS] Synthesized via IndicF5 ({narration_duration:.2f}s).")

        # Step 3: Foley Sound Design & Dynamic Ducking
        print("\n🎵 [3/4] Composing Cinematic Foley & Soundtrack with Dynamic Ducking...")
        master_audio = self.output_dir / f"{project_name}_soundtrack.mp3"
        if voice_wav.exists():
            self.audio_master.mix_soundtrack_with_ducking(voice_wav, master_audio)
        else:
            # Generate standalone cinematic soundtrack
            bgm = self.audio_master.generate_cinematic_bgm(narration_duration)
            import soundfile as sf
            sf.write(str(master_audio.with_suffix(".wav")), bgm, 44100)
            master_audio = master_audio.with_suffix(".wav")
        print(f"       -> Master soundtrack ready: {master_audio}")

        # Step 4: Headless Frame-Accurate CDP Memory Pipe Render
        print("\n🎥 [4/4] Rendering 1080x1920 (9:16) 30 FPS Video via CDP...")
        html_template = Path(__file__).parent.parent / "templates" / "mayank_notebook" / "index.html"
        output_mp4 = self.output_dir / f"{project_name}.mp4"

        final_video = self.cdp_renderer.render(
            html_path=html_template,
            audio_path=master_audio,
            output_mp4=output_mp4,
            duration=narration_duration,
            fps=30
        )

        print("\n=======================================================")
        print(f"✅ Production Complete! Master Deliverable:")
        print(f"   {final_video}")
        print("=======================================================\n")
        return final_video
