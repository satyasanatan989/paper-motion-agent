"""
Autonomous Storyboard Generator.
Converts script chapters and conceptual research into complete, schema-compliant visual production plans.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
import jsonschema

@dataclass
class LayerSpec:
    name: str
    depth_level: str  # 'background', 'midground', 'foreground', 'overlay'
    type: str         # 'svg_vector', 'particle_emitter', 'html_mesh', 'metric_tile', 'procedural_canvas'
    content_id: str
    animation: str
    parallax_factor: float = 0.5

@dataclass
class CameraSpec:
    movement: str  # 'slow_dolly_in', 'fast_push_in', 'smooth_pull_back', 'pan_left', 'pan_right', 'tilt_up', 'tilt_down', 'subtle_orbit', 'static_focus'
    depth_parallax: bool = True
    zoom_start: float = 1.0
    zoom_end: float = 1.08
    easing: str = "cubic_bezier"

@dataclass
class TypographySpec:
    badge: str
    headline_main: str
    headline_sub: str
    highlight_words: List[str]
    animation: str = "word_by_word"

@dataclass
class TransitionSpec:
    type: str  # 'cinematic_zoom', 'directional_wipe', 'mask_reveal', 'paper_tear', 'light_flash', 'parallax_push'
    duration: float = 0.45
    direction: str = "center"

@dataclass
class FoleySpec:
    effect: str
    time_offset: float
    volume: float = 0.7

@dataclass
class ScenePlan:
    scene_id: str
    chapter_num: int
    title: str
    duration: float
    narration: str
    visual_type: str
    environment: str
    background_tone: Dict[str, Any]
    camera: CameraSpec
    layers: List[LayerSpec]
    typography: TypographySpec
    transition: TransitionSpec
    foley: List[FoleySpec] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    metric_title: Optional[str] = None
    metric_val: Optional[str] = None
    widget: Optional[Dict[str, Any]] = None
    annotation: Optional[Dict[str, Any]] = None
    paper_transition: Optional[Dict[str, Any]] = None
    cadence: Optional[Dict[str, Any]] = None
    color_field: Optional[str] = None
    assemble_from_empty: bool = True
    custom_html: Optional[str] = None

@dataclass
class StoryboardPlan:
    project_name: str
    topic: str
    language: str
    genre: str
    aspect_ratio: str
    resolution: Dict[str, int]
    fps: int
    estimated_duration: float
    soundtrack_preset: str = "health_bio"
    scenes: List[ScenePlan] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    def save_json(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        return path

class StoryboardGenerator:
    """Generates schema-validated multi-layer cinematic visual storyboards."""

    def __init__(self, schema_path: Optional[Path] = None):
        if schema_path is None:
            schema_path = Path(__file__).resolve().parent.parent / "schemas" / "storyboard_schema.json"
        self.schema_path = Path(schema_path)
        self.schema = None
        if self.schema_path.exists():
            with open(self.schema_path, "r", encoding="utf-8") as f:
                self.schema = json.load(f)

    def generate_storyboard(
        self,
        topic: str,
        chapters: list,
        project_name: str = "explainer_production",
        language: str = "hinglish",
        genre: str = "science_bio",
        fps: int = 30
    ) -> StoryboardPlan:
        """
        Creates a complete multi-layer storyboard tailored to the topic and chapters.
        """
        total_duration = round(sum(ch.end_sec - ch.start_sec for ch in chapters), 2)
        scenes: List[ScenePlan] = []

        # Camera movements cycle for dynamic visual interest
        camera_movements = [
            "slow_dolly_in", "pan_right", "fast_push_in", "tilt_up", "smooth_pull_back", "subtle_orbit"
        ]

        # Transitions cycle
        transition_types = [
            "directional_wipe", "paper_tear", "mask_reveal", "light_flash", "parallax_push", "cinematic_zoom"
        ]

        for idx, ch in enumerate(chapters):
            ch_num = ch.chapter_num
            ch_dur = round(ch.end_sec - ch.start_sec, 2)
            cam_move = camera_movements[idx % len(camera_movements)]
            trans_type = transition_types[idx % len(transition_types)]

            # Environment & Background tone per genre
            bg_tone, env_name, vis_type = self._derive_visual_setting(genre, ch_num, ch.title)

            # Build Multi-Depth Layers
            layers = self._build_scene_layers(genre, ch_num, ch.title)

            # Build Typography Spec
            typo = TypographySpec(
                badge=f"CHAPTER {ch_num:02d} · {ch.headline_sub.replace('CHAPTER ' + str(ch_num) + ' · ', '')}",
                headline_main=ch.headline_main,
                headline_sub=ch.headline_sub,
                highlight_words=ch.keywords[:4] if hasattr(ch, 'keywords') and ch.keywords else ["KEY", "CONCEPT"],
                animation="word_by_word"
            )

            # Camera Spec
            camera = CameraSpec(
                movement=cam_move,
                depth_parallax=True,
                zoom_start=1.0,
                zoom_end=1.07 if "push" in cam_move or "dolly" in cam_move else 1.0,
                easing="cubic_bezier"
            )

            # Transition Spec
            transition = TransitionSpec(
                type=trans_type,
                duration=0.45,
                direction="right" if "right" in cam_move else "center"
            )

            # Foley sound effects per chapter
            foley_cues = self._derive_foley(genre, ch_num)

            ch_widget = getattr(ch, 'widget', None)
            ch_metric_title = getattr(ch, 'metric_title', None) or (ch_widget.get('metric_title') if isinstance(ch_widget, dict) else None)
            ch_metric_val = getattr(ch, 'metric_val', None) or (ch_widget.get('metric_val') if isinstance(ch_widget, dict) else None)
            ch_annotation = getattr(ch, 'annotation', None)
            if not ch_annotation and getattr(ch, 'keywords', None):
                is_food_topic = ("bio" in genre or "health" in genre or any(k in topic.lower() for k in ["ice cream", "frozen dessert", "food", "maida", "flour"]))
                matched_kw = ch.keywords[0]
                note = "CRITICAL FACTOR"
                style = "circle"
                accent = "burnt_orange"

                if is_food_topic:
                    for k_cand in ch.keywords:
                        kl = k_cand.lower()
                        if "palm" in kl or "oil" in kl or "vanaspati" in kl:
                            matched_kw = k_cand
                            note = "HYDROGENATED VEG FAT"
                            style = "scribble"
                            accent = "burnt_orange"
                            break
                        elif "milk" in kl or "dairy" in kl or "cream" in kl or "pure" in kl:
                            matched_kw = k_cand
                            note = "10% PURE MILK FAT"
                            style = "highlight"
                            accent = "warm_gold"
                            break
                        elif "dessert" in kl or "frozen" in kl or "fake" in kl or "trap" in kl:
                            matched_kw = k_cand
                            note = "NON-DAIRY EMULSION"
                            style = "circle"
                            accent = "crimson_alert"
                            break
                        elif "label" in kl or "verdict" in kl or "choice" in kl:
                            matched_kw = k_cand
                            note = "CONSUMER PROTECTION"
                            style = "highlight"
                            accent = "toxic_green"
                            break

                ch_annotation = {
                    "keyword": matched_kw,
                    "note": note,
                    "style": style,
                    "accent": accent,
                    "draw_at": 0.8
                }

            ch_paper_transition = getattr(ch, 'paper_transition', None) or {
                "type": "torn_paper_rip",
                "direction": "left-to-right",
                "roughness": 55,
                "tone": "cream"
            }
            ch_cadence = getattr(ch, 'cadence', None) or {
                "fps": 12,
                "boil": True,
                "hold_frames": 2,
                "jitter_px": 1.6,
                "jitter_deg": 0.45,
                "seed": 42 + ch_num * 101
            }

            # Derive Color Field (gbro-collage-broll color field theory)
            ch_color_field = getattr(ch, 'color_field', None)
            if not ch_color_field:
                cf_map = {
                    1: "burnt_orange",     # Hook, labor, heat, urgency
                    2: "mustard_yellow",   # Alert, regulation, warning
                    3: "teal_cyan",        # Scientific test, biological lab
                    4: "dark_purple",      # Gastric acid, legal rules
                    5: "mustard_yellow",   # Flight board, data metrics
                    6: "forest_green",     # Natural truth, healthy choice
                }
                ch_color_field = cf_map.get(ch_num, "charcoal_parchment")

            ch_assemble_from_empty = getattr(ch, 'assemble_from_empty', True)

            scene = ScenePlan(
                scene_id=f"scene_{ch_num:03d}",
                chapter_num=ch_num,
                title=ch.title,
                duration=ch_dur,
                narration=ch.narration_hinglish,
                visual_type=vis_type,
                environment=env_name,
                background_tone=bg_tone,
                camera=camera,
                layers=layers,
                typography=typo,
                transition=transition,
                foley=foley_cues,
                keywords=ch.keywords if hasattr(ch, 'keywords') else [],
                metric_title=ch_metric_title,
                metric_val=ch_metric_val,
                widget=ch_widget,
                annotation=ch_annotation,
                paper_transition=ch_paper_transition,
                cadence=ch_cadence,
                color_field=ch_color_field,
                assemble_from_empty=ch_assemble_from_empty
            )
            scenes.append(scene)

        # Map sound preset
        sound_preset = "health_bio" if "bio" in genre else ("war_epic" if "history" in genre else "science_tech")

        storyboard = StoryboardPlan(
            project_name=project_name,
            topic=topic,
            language=language,
            genre=genre if genre in ["science_bio", "history_epic", "technology", "finance_economy", "general_explainer"] else "general_explainer",
            aspect_ratio="9:16",
            resolution={"width": 1080, "height": 1920},
            fps=fps,
            estimated_duration=total_duration,
            soundtrack_preset=sound_preset,
            scenes=scenes
        )

        # Validate against schema if available
        if self.schema:
            jsonschema.validate(instance=storyboard.to_dict(), schema=self.schema)

        return storyboard

    def _derive_visual_setting(self, genre: str, ch_num: int, title: str):
        if "bio" in genre or "health" in genre:
            if ch_num == 1:
                return {"primary": "#1A140E", "secondary": "#2A1F16", "vignette": True}, "Street Food & Fast Dining", "cinematic_2_5d"
            elif ch_num == 2:
                return {"primary": "#18140F", "secondary": "#282015", "vignette": True}, "Microscopic Grain Laboratory", "biological_macro"
            elif ch_num == 3:
                return {"primary": "#161210", "secondary": "#241B15", "vignette": True}, "Gastric Lumen & Mucosal Surface", "biological_macro"
            elif ch_num == 4:
                return {"primary": "#240E10", "secondary": "#361418", "vignette": True}, "Acidic Gastric Cauldron", "biological_macro"
            elif ch_num == 5:
                return {"primary": "#1B1712", "secondary": "#2C241C", "vignette": True}, "Intestinal Transit Flight Board", "infographic_data"
            else:
                return {"primary": "#1A140E", "secondary": "#281D14", "vignette": True}, "Imperial Hall of Health Truth", "dramatic_verdict"
        elif "history" in genre:
            return {"primary": "#1C140D", "secondary": "#2B1D12", "vignette": True}, "Ancient Mauryan Empire", "vector_papercraft"
        else:
            return {"primary": "#111827", "secondary": "#1F2937", "vignette": True}, "Modern Science Laboratory", "cinematic_2_5d"

    def _build_scene_layers(self, genre: str, ch_num: int, title: str) -> List[LayerSpec]:
        """Constructs multi-depth planes for 2.5D parallax."""
        layers = [
            LayerSpec("aged_parchment_canvas", "background", "procedural_canvas", "bg_parchment", "subtle_drift", 0.1),
            LayerSpec("scorched_vignette", "background", "html_mesh", "vignette_overlay", "flicker_pulse", 0.15)
        ]

        if "bio" in genre or "health" in genre:
            if ch_num == 1:
                layers.append(LayerSpec("samosa_pizza_plate", "midground", "svg_vector", "plate_vector", "hover_breathe", 0.5))
                layers.append(LayerSpec("rising_fryer_steam", "foreground", "particle_emitter", "steam_particles", "upward_drift", 0.8))
                layers.append(LayerSpec("esophagus_flare", "foreground", "svg_vector", "flare_glow", "pulse_heat", 0.9))
            elif ch_num == 2:
                layers.append(LayerSpec("wheat_kernel_endosperm", "midground", "svg_vector", "core_starch", "glow_core", 0.4))
                layers.append(LayerSpec("peeling_bran_layers", "foreground", "svg_vector", "bran_peel", "split_reveal", 0.7))
                layers.append(LayerSpec("floating_fiber_dust", "overlay", "particle_emitter", "fiber_particles", "scatter", 0.9))
            elif ch_num == 3:
                layers.append(LayerSpec("stomach_mucosal_wall", "midground", "svg_vector", "stomach_folds", "peristaltic_wave", 0.4))
                layers.append(LayerSpec("viscous_glue_paste", "foreground", "svg_vector", "glue_matrix", "stretch_adhere", 0.8))
            elif ch_num == 4:
                layers.append(LayerSpec("hydrochloric_acid_pool", "midground", "svg_vector", "acid_reservoir", "wave_surge", 0.6))
                layers.append(LayerSpec("corrosive_bubbles", "foreground", "particle_emitter", "acid_bubbles", "boil_rise", 0.9))
            elif ch_num == 5:
                layers.append(LayerSpec("split_flap_board", "midground", "metric_tile", "mechanical_tiles", "ratchet_flip", 0.5))
                layers.append(LayerSpec("intestinal_transit_arrow", "foreground", "svg_vector", "slow_arrow", "sluggish_progress", 0.8))
            else:
                layers.append(LayerSpec("golden_wax_seal", "midground", "svg_vector", "verdict_seal", "rubber_stamp", 0.6))
                layers.append(LayerSpec("verdict_balance_scale", "foreground", "svg_vector", "scale_balance", "tilt_balance", 0.85))
        else:
            layers.append(LayerSpec("central_infographic", "midground", "svg_vector", "main_vector", "scale_impact", 0.5))
            layers.append(LayerSpec("ambient_sparks", "foreground", "particle_emitter", "spark_emitter", "twinkle", 0.8))

        return layers

    def _derive_foley(self, genre: str, ch_num: int) -> List[FoleySpec]:
        foley = []
        if "bio" in genre or "health" in genre:
            if ch_num == 1:
                foley.append(FoleySpec("frying_sizzle", 0.3, 0.75))
            elif ch_num == 2:
                foley.append(FoleySpec("paper_tear", 0.5, 0.65))
            elif ch_num == 3:
                foley.append(FoleySpec("gut_rumble_sub", 0.2, 0.85))
                foley.append(FoleySpec("glue_squelch", 1.8, 0.6))
            elif ch_num == 4:
                foley.append(FoleySpec("boiling_acid_hiss", 0.2, 0.85))
            elif ch_num == 5:
                foley.append(FoleySpec("mechanical_ratchet_tick", 0.1, 0.7))
            else:
                foley.append(FoleySpec("verdict_gong_hit", 0.2, 0.85))
        elif "history" in genre:
            if ch_num in [1, 2]:
                foley.append(FoleySpec("blade_clash", 0.8, 0.8))
            elif ch_num == 4:
                foley.append(FoleySpec("dharma_bell", 0.5, 0.7))
        return foley
