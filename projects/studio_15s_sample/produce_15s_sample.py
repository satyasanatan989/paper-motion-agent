"""
Master 15-Second Studio Tier Explainer Production Script.
Topic: The Palm Oil Ice Cream Scam: 10% Dairy Law vs 90% Fat Replacement.
Duration: 15.0 seconds (450 frames @ 30fps).
"""

import os
import sys
import json
import math
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
agent_root = Path(__file__).resolve().parent.parent.parent
if str(agent_root) not in sys.path:
    sys.path.insert(0, str(agent_root))

from storyboard.generator import StoryboardPlan, ScenePlan, TypographySpec, CameraSpec, TransitionSpec
from visual_engine.scene_composer import DynamicSceneComposer
from voice.audio_master import AudioMasterEngine
from pipeline.cdp_streamer import CDPVideoRenderer
from projects.studio_15s_sample.generate_sample_assets import (
    make_die_cut_ice_cream_sticker,
    make_torn_evidence_card,
    make_rubber_stamp_seal
)

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"
STAGE_DIR = OUTPUT_DIR / "stage"
STAGE_ASSETS_DIR = STAGE_DIR / "assets"

def setup_directories():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STAGE_DIR.mkdir(parents=True, exist_ok=True)
    STAGE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def generate_procedural_assets():
    print("[1/5] Generating procedural & photographic collage assets...")
    make_die_cut_ice_cream_sticker(STAGE_ASSETS_DIR / "ice_cream_sticker.png")
    make_torn_evidence_card(STAGE_ASSETS_DIR / "torn_evidence_card.png")
    make_rubber_stamp_seal(STAGE_ASSETS_DIR / "rubber_stamp_seal.png")
    print("      ✓ Assets generated in stage/assets/")

async def synthesize_narration_and_timestamps():
    print("[2/5] Synthesizing voiceover with Edge-TTS streaming timestamps...")
    import edge_tts

    chapters = [
        {
            "id": 1,
            "text": "Jisko aap ice cream samajh ke kha rahe ho, usme doodh nahi, palm oil hai!",
            "target_duration": 5.0,
            "start": 0.0,
            "end": 5.0
        },
        {
            "id": 2,
            "text": "Legal rule yeh hai ki 10% dairy fat ke bina koi bhi brand ise ice cream nahi bol sakta.",
            "target_duration": 5.0,
            "start": 5.0,
            "end": 10.0
        },
        {
            "id": 3,
            "text": "Toh agli baar packet dhyan se padho: Frozen Dessert ya Real Ice Cream!",
            "target_duration": 5.0,
            "start": 10.0,
            "end": 15.0
        }
    ]

    all_word_timestamps = []
    sr = 44100
    total_samples = int(15.0 * sr)
    full_audio = np.zeros((total_samples,), dtype=np.float32)

    for ch in chapters:
        ch_id = ch["id"]
        ch_text = ch["text"]
        ch_start = ch["start"]

        tmp_mp3 = OUTPUT_DIR / f"tmp_ch_{ch_id}.mp3"
        comm = edge_tts.Communicate(
            ch_text,
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
                # offset is in 100ns units
                start_sec = round(ch_start + (chunk["offset"] / 10_000_000.0), 3)
                dur_sec = round(chunk["duration"] / 10_000_000.0, 3)
                w_text = chunk.get("text", "").strip()
                if w_text:
                    all_word_timestamps.append({
                        "word": w_text,
                        "start": start_sec,
                        "end": round(start_sec + dur_sec, 3),
                        "chapter": ch_id
                    })

        with open(tmp_mp3, "wb") as f:
            for b in audio_chunks:
                f.write(b)

        ch_wav = OUTPUT_DIR / f"tmp_ch_{ch_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(tmp_mp3),
            "-ar", "44100", "-ac", "1", str(ch_wav)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        tmp_mp3.unlink(missing_ok=True)

        data, _ = sf.read(str(ch_wav))
        ch_wav.unlink(missing_ok=True)

        # Place audio at chapter start with natural offset (0.2s padding)
        offset_samples = int((ch_start + 0.20) * sr)
        take_len = min(len(data), total_samples - offset_samples)
        full_audio[offset_samples : offset_samples + take_len] = data[:take_len]

    voice_wav_path = OUTPUT_DIR / "sample_15s_narration.wav"
    sf.write(str(voice_wav_path), full_audio, sr)
    print(f"      ✓ Voice audio written to {voice_wav_path} (15.0s)")

    timestamps_path = OUTPUT_DIR / "word_timestamps.json"
    with open(timestamps_path, "w", encoding="utf-8") as f:
        json.dump(all_word_timestamps, f, indent=2, ensure_ascii=False)
    # Also copy into stage directory
    shutil.copy(timestamps_path, STAGE_DIR / "word_timestamps.json")
    print(f"      ✓ {len(all_word_timestamps)} word timestamps saved & synchronized")

    return voice_wav_path, all_word_timestamps

def master_soundtrack_with_foley(voice_wav: Path) -> Path:
    print("[3/5] Mixing Foley sound effects & ducked background score...")
    sr = 44100
    voice_data, _ = sf.read(str(voice_wav))
    dur = len(voice_data) / sr

    # 1. Generate ambient low-frequency hum & rhythm bed
    t = np.linspace(0, dur, len(voice_data), endpoint=False)
    # Smooth drone chords (D minor / cinematic investigative)
    drone1 = 0.08 * np.sin(2 * np.pi * 73.42 * t)  # D2
    drone2 = 0.06 * np.sin(2 * np.pi * 110.00 * t) # A2
    drone3 = 0.04 * np.sin(2 * np.pi * 174.61 * t) # F3
    bgm = drone1 + drone2 + drone3

    # Add subtle lo-fi vinyl crackle
    rng = np.random.default_rng(42)
    crackle = rng.normal(0, 0.012, len(voice_data))
    bgm += crackle

    # 2. Add Foley hits at key moments:
    # 2A. Paper whoosh/rustle at 0.15s (sticker landing)
    whoosh_idx = int(0.15 * sr)
    whoosh_len = int(0.40 * sr)
    w_t = np.linspace(0, 1, whoosh_len)
    whoosh = 0.18 * np.sin(2 * np.pi * (180 - 120 * w_t) * w_t) * np.sin(np.pi * w_t)
    bgm[whoosh_idx : whoosh_idx + whoosh_len] += whoosh

    # 2B. Tape snap / click at 5.15s (widget & tape entrance)
    tape_idx = int(5.15 * sr)
    tape_len = int(0.20 * sr)
    t_t = np.linspace(0, 1, tape_len)
    tape_snap = 0.22 * np.sin(2 * np.pi * 650 * t_t) * np.exp(-12 * t_t)
    bgm[tape_idx : tape_idx + tape_len] += tape_snap

    # 2C. Deep rubber stamp slam at 10.40s (stamp thud)
    stamp_idx = int(10.40 * sr)
    stamp_len = int(0.60 * sr)
    s_t = np.linspace(0, 1, stamp_len)
    stamp_thud = 0.35 * np.sin(2 * np.pi * 55 * s_t) * np.exp(-7 * s_t)
    bgm[stamp_idx : stamp_idx + stamp_len] += stamp_thud

    # 3. Dynamic ducking under voiceover
    voice_abs = np.abs(voice_data)
    # Simple moving average envelope
    kernel = np.ones(int(0.15 * sr)) / int(0.15 * sr)
    envelope = np.convolve(voice_abs, kernel, mode="same")
    duck_gain = np.clip(1.0 - (envelope * 2.5), 0.25, 1.0)
    bgm_ducked = bgm * duck_gain

    # 4. Mix voice + ducked Foley BGM
    master = (voice_data * 0.90) + (bgm_ducked * 0.35)
    max_val = np.max(np.abs(master))
    if max_val > 0.95:
        master = master * (0.95 / max_val)

    soundtrack_mp3 = OUTPUT_DIR / "sample_15s_master_soundtrack.mp3"
    soundtrack_wav = OUTPUT_DIR / "sample_15s_master_soundtrack.wav"
    sf.write(str(soundtrack_wav), master, sr)

    # Encode to MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", str(soundtrack_wav),
        "-b:a", "192k", str(soundtrack_mp3)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    soundtrack_wav.unlink(missing_ok=True)

    print(f"      ✓ Master soundtrack mixed: {soundtrack_mp3}")
    return soundtrack_mp3

def assemble_storyboard_stage(word_timestamps):
    print("[4/5] Assembling 2.5D multi-plane stage with spring physics & widgets...")

    scene1_html = """
    <div class="assemble-piece craft-sticker-container" style="position:relative;width:500px;height:520px;margin:0 auto;display:flex;align-items:center;justify-content:center;">
      <div class="craft-washi-tape tape-tr"></div>
      <img src="assets/ice_cream_sticker.png" alt="Ice Cream Sticker" style="width:440px;height:auto;filter:drop-shadow(0 14px 28px rgba(0,0,0,0.65));animation:springStickerPop 0.65s forwards;" />
      <div class="hazard-ribbon" style="position:absolute;bottom:40px;background:#E53E3E;color:#FFF;padding:12px 28px;border-radius:8px;font-family:'Impact',sans-serif;font-size:26px;letter-spacing:0.12em;box-shadow:0 8px 20px rgba(0,0,0,0.6);border:2px solid #FFF;">
        0% DAIRY FAT DETECTED
      </div>
    </div>
    """

    scene2_html = """
    <div class="assemble-piece widgets-container" style="position:relative;width:680px;height:520px;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;">
      <div class="craft-washi-tape tape-tl"></div>
      <div style="display:flex;gap:35px;align-items:center;justify-content:center;margin-bottom:30px;">
        <div class="hanging-tag-widget" id="s2-tag" style="position:relative;top:0;left:0;transform:scale(1.2);animation:springTagSwing 0.85s forwards;">
          <div class="hanging-tag-string"></div>
          <div class="hanging-tag-hole"></div>
          <div class="hanging-tag-title">PALM OIL COST</div>
          <div class="hanging-tag-value">Rs 90/KG</div>
          <div class="hanging-tag-sub">VS Rs 450 DAIRY</div>
        </div>
        <div class="odometer-widget" id="s2-odometer" style="position:relative;bottom:0;right:0;transform:scale(1.15);">
          <div class="odometer-title">CALORIC RATIO (KCAL)</div>
          <div class="odometer-value-box">
            <div class="odometer-dial">
              <span class="odometer-digit">4</span>
              <span class="odometer-digit">5</span>
              <span class="odometer-digit">0</span>
            </div>
          </div>
        </div>
      </div>
      <div class="vox-annotate-container" style="margin-top:15px;background:rgba(20,15,12,0.92);padding:14px 28px;border-radius:10px;border-left:5px solid #F28C28;">
        <span style="font-family:'Cinzel',serif;font-weight:900;color:#F28C28;font-size:20px;">STATUTORY RULE:</span>
        <span style="font-family:'Montserrat',sans-serif;color:#FFFDF8;font-size:18px;margin-left:8px;">10% Milk Fat Mandatory for Ice Cream</span>
      </div>
    </div>
    """

    scene3_html = """
    <div class="assemble-piece verdict-container" style="position:relative;width:640px;height:520px;margin:0 auto;display:flex;align-items:center;justify-content:center;">
      <img src="assets/torn_evidence_card.png" alt="Torn Evidence Card" style="width:580px;height:auto;filter:drop-shadow(0 16px 32px rgba(0,0,0,0.7));" />
      <div class="craft-rubber-stamp" style="bottom:65px;right:60px;animation:springStampSlam 0.65s forwards;transform:rotate(-12deg);background:rgba(254,242,242,0.95);box-shadow:0 8px 24px rgba(0,0,0,0.5);">
        <div style="font-size:16px;letter-spacing:0.18em;margin-bottom:4px;">OFFICIAL MANDATE</div>
        <div style="font-size:26px;font-weight:900;">10% MILK FAT</div>
        <div style="font-size:14px;letter-spacing:0.1em;margin-top:4px;">VERIFIED STANDARD</div>
      </div>
    </div>
    """

    scenes = [
        ScenePlan(
            scene_id="scene-01",
            chapter_num=1,
            title="The Trap",
            narration="Jisko aap ice cream samajh ke kha rahe ho, usme doodh nahi, palm oil hai!",
            duration=5.0,
            keywords=["ICE CREAM", "PALM OIL"],
            visual_type="specialized",
            typography=TypographySpec(
                badge="CHAPTER 01 / CONSUMER ALERT",
                headline_sub="WHAT ARE YOU EATING?",
                headline_main="PALM OIL CONE",
                highlight_words=["PALM", "OIL"]
            ),
            camera=CameraSpec(
                movement="handheld_desk_wander",
                zoom_start=1.00,
                zoom_end=1.06
            ),
            environment="Desk",
            background_tone={"primary": "#1A140E"},
            layers=[],
            transition=TransitionSpec(type="directional_wipe"),
            color_field="burnt_orange",
            assemble_from_empty=True,
            custom_html=scene1_html
        ),
        ScenePlan(
            scene_id="scene-02",
            chapter_num=2,
            title="The Legal Formula",
            narration="Legal rule yeh hai ki 10% dairy fat ke bina koi bhi brand ise ice cream nahi bol sakta.",
            duration=5.0,
            keywords=["10% DAIRY FAT", "LEGAL RULE"],
            visual_type="specialized",
            typography=TypographySpec(
                badge="CHAPTER 02 / DAIRY MANDATE",
                headline_sub="CALORIC REPLACEMENT",
                headline_main="ZERO DAIRY FAT",
                highlight_words=["ZERO", "DAIRY"]
            ),
            camera=CameraSpec(
                movement="dolly_in",
                zoom_start=1.02,
                zoom_end=1.10
            ),
            environment="Desk",
            background_tone={"primary": "#1A140E"},
            layers=[],
            transition=TransitionSpec(type="directional_wipe"),
            color_field="dark_purple",
            assemble_from_empty=True,
            custom_html=scene2_html
        ),
        ScenePlan(
            scene_id="scene-03",
            chapter_num=3,
            title="The Regulatory Verdict",
            narration="Toh agli baar packet dhyan se padho: Frozen Dessert ya Real Ice Cream!",
            duration=5.0,
            keywords=["FROZEN DESSERT", "REAL ICE CREAM"],
            visual_type="specialized",
            typography=TypographySpec(
                badge="CHAPTER 03 / CONSUMER VERDICT",
                headline_sub="CHECK THE LABEL",
                headline_main="FROZEN DESSERT",
                highlight_words=["FROZEN", "DESSERT"]
            ),
            camera=CameraSpec(
                movement="subtle_drift",
                zoom_start=1.05,
                zoom_end=1.02
            ),
            environment="Desk",
            background_tone={"primary": "#1A140E"},
            layers=[],
            transition=TransitionSpec(type="directional_wipe"),
            color_field="teal_cyan",
            assemble_from_empty=True,
            custom_html=scene3_html
        )
    ]

    storyboard = StoryboardPlan(
        project_name="sample_15s_studio_demo",
        topic="The Palm Oil Ice Cream Scam: 10% Dairy Law vs 90% Fat Replacement",
        language="hinglish",
        genre="food_investigation",
        aspect_ratio="9:16",
        resolution={"width": 1080, "height": 1920},
        fps=30,
        estimated_duration=15.0,
        scenes=scenes
    )

    composer = DynamicSceneComposer()
    html_file = composer.compose_stage(storyboard, STAGE_DIR, word_timestamps=word_timestamps)
    print(f"      ✓ Web Stage composed successfully: {html_file}")
    return html_file

def render_master_video(html_path: Path, audio_path: Path) -> Path:
    print("[5/5] Executing frame-accurate CDP rendering (450 frames @ 30 FPS)...")
    output_mp4 = OUTPUT_DIR / "sample_15s_studio_demo.mp4"
    renderer = CDPVideoRenderer()
    final_video = renderer.render(
        html_path=html_path,
        audio_path=audio_path,
        output_mp4=output_mp4,
        duration=15.0,
        fps=30
    )
    print(f"      ✓ Master MP4 rendered: {final_video}")
    return final_video

def extract_contact_sheet(video_path: Path) -> Path:
    print("Generating keyframe contact sheet...")
    frames_dir = OUTPUT_DIR / "contact_sheet_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    timestamps = [2.5, 7.5, 12.5]
    frame_paths = []
    for idx, ts in enumerate(timestamps, start=1):
        fpath = frames_dir / f"keyframe_{idx:02d}.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ts),
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(fpath)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        frame_paths.append(fpath)

    # Stitch into 1x3 horizontal or 3x1 contact sheet
    contact_sheet_path = OUTPUT_DIR / "sample_15s_contact_sheet.jpg"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(frame_paths[0]),
        "-i", str(frame_paths[1]),
        "-i", str(frame_paths[2]),
        "-filter_complex", "hstack=inputs=3[out]",
        "-map", "[out]",
        "-q:v", "2",
        str(contact_sheet_path)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"      ✓ Contact sheet saved: {contact_sheet_path}")
    return contact_sheet_path

async def main():
    print("================================================================")
    print("🎬 STUDIO TIER 15-SECOND SAMPLE VIDEO PRODUCTION PIPELINE")
    print("================================================================")
    setup_directories()
    generate_procedural_assets()
    voice_wav, word_timestamps = await synthesize_narration_and_timestamps()
    master_soundtrack = master_soundtrack_with_foley(voice_wav)
    html_file = assemble_storyboard_stage(word_timestamps)
    master_mp4 = render_master_video(html_file, master_soundtrack)
    contact_sheet = extract_contact_sheet(master_mp4)

    # Copy deliverables to Brain artifact directory
    brain_dir = Path("C:/Users/prabh/.gemini/antigravity/brain/9491c393-2d38-44e0-9c0c-e0a6653db413")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(master_mp4, brain_dir / "sample_15s_studio_demo.mp4")
    shutil.copy(contact_sheet, brain_dir / "sample_15s_contact_sheet.jpg")
    print(f"\nDeliverables mirrored to Brain artifact directory: {brain_dir}")
    print("================================================================")
    print("🎉 PRODUCTION COMPLETE!")
    print("================================================================")

if __name__ == "__main__":
    asyncio.run(main())
