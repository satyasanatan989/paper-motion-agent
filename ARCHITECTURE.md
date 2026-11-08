# PaperMotion AI — System Architecture

```mermaid
flowchart TD
    subgraph InputStage["1. INGESTION & TOPIC ANALYSIS"]
        UserTopic["User Topic / Prompt<br/>(e.g., 'What happens after eating refined flour?')"] --> ResearchEngine["Fact & Knowledge Engine<br/>(research/fact_engine.py)"]
        ResearchEngine --> DomainDetect["Domain Classifier & Fact Ontologies<br/>(Health, Physics, History, Tech)"]
    end

    subgraph ScriptStoryboard["2. SCRIPTING & STORYBOARD SCHEMA"]
        DomainDetect --> ScriptEngine["Topic-Driven Script Engine<br/>(agent/script_engine.py)"]
        ScriptEngine --> Chapters["6-Chapter Retention Arc<br/>(Hook, Anatomy, Mechanism, Crisis, Time, Verdict)"]
        Chapters --> StoryboardGen["Autonomous Storyboard Generator<br/>(storyboard/generator.py)"]
        StoryboardGen --> JsonSchema["Formal JSON Schema Validation<br/>(schemas/storyboard_schema.json)"]
    end

    subgraph AudioEngine["3. VOICE CLONING & ACOUSTIC DESIGN"]
        Chapters --> VoiceChooser{"Voice Cloner Selector"}
        VoiceChooser -->|Primary| JugnuTTS["Jugnu Pocket TTS Cloner<br/>(AltSlate-Labs)"]
        VoiceChooser -->|Fallback 1| IndicF5["IndicF5 DiT Flow Matching"]
        VoiceChooser -->|Fallback 2| EdgeNeural["Neural Speech Synthesizer<br/>(hi-IN-MadhurNeural)"]
        
        JugnuTTS --> Normalizer["Hinglish Normalizer<br/>(voice/normalizer.py)"]
        IndicF5 --> Normalizer
        EdgeNeural --> Normalizer
        
        Normalizer --> NarrationWav["Narration Audio Track (WAV)"]
        NarrationWav --> AudioMaster["Adaptive Audio Master Engine<br/>(voice/audio_master.py)"]
        AudioMaster --> FoleySoundscape["Genre-Adaptive Foley & Sub-Bass<br/>(38Hz Gut Rumble, Sizzles, Flip Clicks)"]
        FoleySoundscape --> SidechainDucking["Automatic Sidechain Ducking (-16dB)"]
        SidechainDucking --> MasterSoundtrack["Master Mastered Soundtrack (MP3)"]
    end

    subgraph VisualEngine["4. 2.5D HYBRID VISUAL & MOTION ENGINE"]
        JsonSchema --> DynamicComposer["Dynamic Scene Composer<br/>(visual_engine/scene_composer.py)"]
        
        CameraController["2.5D Physical Camera Controller<br/>(Dolly, Push, Pull-back, Tilt, Pan)"] --> DynamicComposer
        ParallaxEngine["Multi-Plane Depth Parallax<br/>(Background 0.1x, Midground 0.5x, Foreground 1.4x)"] --> DynamicComposer
        MotionPresets["Motion Easing & Particle Simulation<br/>(Cubic Bézier, Spring Overshoots, Steam/Acid/Sparks)"] --> DynamicComposer
        KineticTypo["Kinetic Typography Engine<br/>(Split-Flap Counters, Word-by-Word Glow, Badges)"] --> DynamicComposer
        
        DynamicComposer --> WebStage["1080x1920 (9:16) Standalone HTML/CSS/JS Stage<br/>(output/stage/index.html)"]
    end

    subgraph RenderAndQC["5. ZERO-DISK-IO RENDER & QUALITY CONTROL"]
        WebStage --> CDPStreamer["Headless Chrome DevTools Protocol<br/>(pipeline/render.js)"]
        MasterSoundtrack --> CDPStreamer
        
        CDPStreamer --> FFmpegPipe["Direct In-Memory Buffer Stream into FFmpeg stdin"]
        FFmpegPipe --> MasterVideo["Final Deliverable MP4<br/>(output/maida_cinematic_explainer.mp4)"]
        
        MasterVideo --> QCValidator["Automated Quality Control Validator<br/>(quality_control/validator.py)"]
        QCValidator --> QCReport["Structured Audit Report<br/>(quality_report.json)"]
    end
```

---

## Architectural Principles

### 1. Topic Agnostic Decoupling
Earlier iterations coupled the rendering pipeline to a hardcoded historical script (`Ashoka Samrat`). PaperMotion 2.0 decouples topic ingestion from visual execution. Any topic is transformed into an abstract `StoryboardPlan` conforming to `schemas/storyboard_schema.json`, ensuring infinite scalability across scientific, historical, medical, and technical disciplines.

### 2. Multi-Plane 2.5D Parallax Physics
Flat 2D animation suffers from rapid viewer disengagement. PaperMotion employs a 3-layer parallax camera model:
- **Background Layer ($z \approx -400\text{px}$, Parallax factor $0.1\times - 0.2\times$)**: Aged parchment canvases, vignette textures, scorched perimeter burns.
- **Midground Layer ($z \approx 0\text{px}$, Parallax factor $0.5\times - 1.0\times$)**: Anatomical organs, wheat kernels, clashing swords, nuclear reactor fuel rods.
- **Foreground Layer ($z \approx +200\text{px}$, Parallax factor $1.2\times - 1.4\times$)**: Rising steam particles, boiling acid flares, flying sparks, mechanical flip-tiles.
- **Overlay Layer**: Kinetic typography, highlighted keyword banners, and chapter milestone badges positioned safely within 9:16 social reel margins.

### 3. Frame-Accurate Zero-Disk CDP Memory Pipe
Rather than rendering thousands of `.png` image frames to disk—which introduces disk I/O bottlenecks and SSD wear—PaperMotion AI utilizes Chrome DevTools Protocol (`Page.captureScreenshot`). Uncompressed raw frame buffers are written directly into an active FFmpeg standard input pipe (`ffmpeg -f image2pipe -i -`). This achieves maximum render speed with zero temporary disk artifacts.

### 4. Broadcast EBU R128 Audio Compliance
Voiceover intelligibility is preserved through dynamic sidechain ducking. When narration occurs, background Foley soundscapes are automatically compressed by $-16\text{ dB}$. The final render is inspected by `quality_control/validator.py` ensuring $-14\text{ LUFS} \pm 1.5\text{ LUFS}$ integrated loudness and peak levels under $-1.0\text{ dBTP}$.
