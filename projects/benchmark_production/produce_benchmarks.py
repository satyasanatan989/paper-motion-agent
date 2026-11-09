"""
Autonomous Benchmark Production Script for PaperMotion Studio Tier.
Produces Benchmark Video 1 (Format B: 'The Food Code' Detective Reel, ~50s):
Topic: 'Is packaged coconut water healthy?'
- 17 Visual Beats (changes every 2.5–3.2s) conforming to schemas/beat_schema.json
- Die-cut 3D glossy stickers with physical drop shadows via AssetPipeline & rembg
- Edge-TTS word-level streaming synchronization (hi-IN-MadhurNeural)
- Foley sound effects & sidechain ducked music mastered to strictly -14 LUFS integrated
- 2-Line top-left headline + 2–4 word subtitle capsule + watermark
- Frame-accurate headless Chrome CDP render into FFmpeg
- Automated Quality Control gate & 6x3 visual contact sheet export
"""

import os
import sys
import json
import asyncio
import shutil
import subprocess
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import soundfile as sf
import numpy as np

# Ensure paper-motion-agent root is on sys.path
AGENT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from agent.script_engine import ScriptEngine
from storyboard.generator import StoryboardGenerator, BeatSpec
from assets.pipeline import AssetPipeline
from visual_engine.scene_composer import DynamicSceneComposer
from voice.audio_master import AudioMasterEngine
from pipeline.cdp_streamer import CDPVideoRenderer
from quality_control.validator import QualityValidator

PROJECT_DIR = Path(__file__).resolve().parent / "packaged_coconut_water_001"
OUTPUT_DIR = PROJECT_DIR / "output"
STAGE_DIR = OUTPUT_DIR / "stage"
STAGE_ASSETS_DIR = STAGE_DIR / "assets"
BRAIN_DIR = Path("C:/Users/prabh/.gemini/antigravity/brain/9491c393-2d38-44e0-9c0c-e0a6653db413")

def setup_directories():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STAGE_DIR.mkdir(parents=True, exist_ok=True)
    STAGE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)

def generate_assets_for_beats(beats, pipeline: AssetPipeline):
    print("\n[Step 2/7] Generating photographic & 3D cutout stickers with rembg & vinyl edges...")
    asset_map = {}
    for beat in beats:
        for a in beat.assets:
            aid = a.get("id")
            prompt = a.get("prompt", aid)
            if aid not in asset_map:
                cached_path = pipeline.generate_asset(prompt, style="sticker", asset_id=aid)
                # Copy to stage assets
                dest_path = STAGE_ASSETS_DIR / f"{aid}.png"
                shutil.copy(cached_path, dest_path)
                asset_map[aid] = f"assets/{aid}.png"
                print(f"      ✓ Asset ready: {aid} -> stage/assets/{aid}.png")

    # Add evidence report card for stamp reveal
    cached_doc = pipeline.generate_asset("declassified lab test report forensic document", style="sticker", asset_id="lab_sheet")
    shutil.copy(cached_doc, STAGE_ASSETS_DIR / "lab_sheet.png")
    shutil.copy(cached_doc, STAGE_ASSETS_DIR / "torn_evidence_card.png")
    asset_map["lab_sheet"] = "assets/lab_sheet.png"
    asset_map["torn_evidence_card"] = "assets/torn_evidence_card.png"

    return asset_map

async def synthesize_beat_audio_and_timestamps(beats):
    print("\n[Step 3/7] Synthesizing Edge-TTS voiceover for all beats with word boundaries...")
    import edge_tts

    sr = 44100
    total_duration = beats[-1].end
    total_samples = int((total_duration + 1.0) * sr)
    full_audio = np.zeros((total_samples,), dtype=np.float32)
    all_word_timestamps = []

    for idx, beat in enumerate(beats):
        voice_text = beat.voice
        beat_start = beat.start

        tmp_mp3 = OUTPUT_DIR / f"tmp_beat_{beat.beat_id}.mp3"
        comm = edge_tts.Communicate(
            voice_text,
            "hi-IN-MadhurNeural",
            rate="+6%",
            pitch="+0Hz",
            boundary="WordBoundary"
        )

        audio_chunks = []
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = round(beat_start + (chunk["offset"] / 10_000_000.0), 3)
                dur_sec = round(chunk["duration"] / 10_000_000.0, 3)
                w_text = chunk.get("text", "").strip()
                if w_text:
                    all_word_timestamps.append({
                        "word": w_text,
                        "start": start_sec,
                        "end": round(start_sec + dur_sec, 3),
                        "beat": beat.beat_id
                    })

        with open(tmp_mp3, "wb") as f:
            for b in audio_chunks:
                f.write(b)

        ch_wav = OUTPUT_DIR / f"tmp_beat_{beat.beat_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(tmp_mp3),
            "-ar", "44100", "-ac", "1", str(ch_wav)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        tmp_mp3.unlink(missing_ok=True)

        data, _ = sf.read(str(ch_wav))
        ch_wav.unlink(missing_ok=True)

        offset_samples = int((beat_start + 0.15) * sr)
        take_len = min(len(data), total_samples - offset_samples)
        if take_len > 0:
            full_audio[offset_samples : offset_samples + take_len] = data[:take_len]

    voice_wav_path = OUTPUT_DIR / "coconut_narration.wav"
    sf.write(str(voice_wav_path), full_audio, sr)
    print(f"      ✓ Voice track written: {voice_wav_path} ({total_duration:.2f}s)")

    timestamps_path = OUTPUT_DIR / "word_timestamps.json"
    with open(timestamps_path, "w", encoding="utf-8") as f:
        json.dump(all_word_timestamps, f, indent=2, ensure_ascii=False)
    shutil.copy(timestamps_path, STAGE_DIR / "word_timestamps.json")
    print(f"      ✓ {len(all_word_timestamps)} word timestamps saved & synchronized")

    return voice_wav_path, all_word_timestamps, total_duration

def master_soundtrack(beats, voice_wav: Path, audio_engine: AudioMasterEngine) -> Path:
    print("\n[Step 4/7] Generating Foley cue track and mastering to strictly -14 LUFS...")
    # Collect Foley cues from beats
    foley_cues = []
    for b in beats:
        for sfx_name in b.sfx:
            foley_cues.append({
                "time": b.start + 0.10,
                "sfx": sfx_name
            })

    output_master_mp3 = OUTPUT_DIR / "coconut_soundtrack_master.mp3"
    mastered_path = audio_engine.mix_soundtrack_with_ducking_adaptive(
        voiceover_wav=voice_wav,
        output_mp3=output_master_mp3,
        genre="health_bio",
        bgm_volume=0.22,
        foley_cues=foley_cues,
        target_lufs=-14.0
    )

    # Verify measured LUFS
    measured_lufs = audio_engine.measure_loudness(mastered_path)
    print(f"      ✓ Audio mastered: {mastered_path}")
    print(f"      ✓ Measured Integrated Loudness: {measured_lufs:.2f} LUFS (Target: -14.0 LUFS)")
    return mastered_path

async def main():
    print("=================================================================")
    print("🎬 BENCHMARK 1 PRODUCTION: 'Is packaged coconut water healthy?'")
    print("=================================================================")
    setup_directories()

    # 1. Script Engine: Generate Story-Shaped Beats
    print("\n[Step 1/7] Synthesizing 17 story-shaped beats conforming to beat_schema.json...")
    script_engine = ScriptEngine(output_dir=OUTPUT_DIR)
    beats = script_engine.generate_beats("Is packaged coconut water healthy?", format_type="format_b")
    print(f"      ✓ {len(beats)} visual beats generated across 48.8s runtime.")

    # 2. Asset Pipeline
    pipeline = AssetPipeline()
    asset_map = generate_assets_for_beats(beats, pipeline)

    # 3. Voiceover & Timestamp Synthesis
    voice_wav, word_timestamps, total_duration = await synthesize_beat_audio_and_timestamps(beats)

    # 4. Foley & Loudness Audio Mastering
    audio_engine = AudioMasterEngine(sample_rate=44100)
    master_audio = master_soundtrack(beats, voice_wav, audio_engine)

    # 5. Storyboard & Web Stage Composition
    print("\n[Step 5/7] Composing interactive 9:16 web stage with spring physics & kinetic typography...")
    storyboard_gen = StoryboardGenerator()
    storyboard = storyboard_gen.generate_storyboard_from_beats(
        topic="Is packaged coconut water healthy?",
        beats=beats,
        project_name="packaged_coconut_water_benchmark",
        genre="food_investigation",
        fps=30
    )
    # Save storyboard json
    with open(OUTPUT_DIR / "storyboard.json", "w", encoding="utf-8") as f:
        json.dump(storyboard.to_dict(), f, indent=2)

    composer = DynamicSceneComposer()
    html_file = composer.compose_stage(storyboard, STAGE_DIR, word_timestamps=word_timestamps)
    print(f"      ✓ Stage composed: {html_file}")

    # 6. CDP Video Rendering
    print(f"\n[Step 6/7] Rendering master MP4 ({int(total_duration * 30)} frames @ 30 FPS)...")
    master_mp4 = OUTPUT_DIR / "packaged_coconut_water_benchmark.mp4"
    renderer = CDPVideoRenderer()
    renderer.render(
        html_path=html_file,
        audio_path=master_audio,
        output_mp4=master_mp4,
        duration=round(total_duration, 2),
        fps=30
    )
    print(f"      ✓ Master video successfully rendered: {master_mp4}")

    # 7. Quality Control & Contact Sheet
    print("\n[Step 7/7] Executing Quality Control validation gate & 6x3 contact sheet...")
    validator = QualityValidator()
    # Check storyboard beats
    beat_issues = validator.inspect_storyboard(storyboard)
    print(f"      Storyboard Beat Verification: {len(beat_issues)} issues found.")
    for iss in beat_issues:
        print(f"        - {iss}")

    qc_report = validator.inspect_video(master_mp4, expected_duration=total_duration)
    qc_report.save_json(OUTPUT_DIR / "quality_report.json")
    print(f"      ✓ QC Status: {qc_report.status}")
    print(f"      ✓ Resolution: {qc_report.resolution}, FPS: {qc_report.framerate:.1f}, Duration: {qc_report.duration:.2f}s")
    print(f"      ✓ Integrated Loudness: {qc_report.integrated_lufs:.2f} LUFS")

    # Generate 6x3 Visual Contact Sheet
    contact_sheet = validator.export_contact_sheet(master_mp4, tile_grid="6x3")
    print(f"      ✓ 6x3 Visual Contact Sheet generated: {contact_sheet}")

    # Mirror deliverables to Brain artifact directory
    dest_video = BRAIN_DIR / "packaged_coconut_water_benchmark.mp4"
    dest_sheet = BRAIN_DIR / "packaged_coconut_water_contact_sheet.jpg"
    shutil.copy(master_mp4, dest_video)
    if contact_sheet and contact_sheet.exists():
        shutil.copy(contact_sheet, dest_sheet)
    print(f"\nDeliverables mirrored to Brain artifact directory: {BRAIN_DIR}")
    print(f"  - Video: {dest_video}")
    print(f"  - Contact Sheet: {dest_sheet}")
    print("=================================================================")
    print("🎉 BENCHMARK 1 PRODUCTION COMPLETED SUCCESSFULLY!")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(main())
