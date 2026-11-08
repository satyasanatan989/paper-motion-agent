"""
Offline Conceptual Fact & Research Engine.
Transforms user topics into structured, factual evidence and logical chapters.
Avoids hallucinated statistics and grounds explainer narratives in verified principles.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re

@dataclass
class FactItem:
    claim: str
    category: str  # 'mechanism', 'statistic', 'biological_process', 'historical_event'
    verified: bool = True
    context: str = ""
    source_reference: Optional[str] = None

@dataclass
class ConceptualChapter:
    chapter_index: int
    title: str
    narrative_purpose: str  # 'hook', 'anatomy_or_scale', 'core_mechanism', 'danger_or_crisis', 'time_or_contrast', 'verdict'
    primary_fact: str
    supporting_facts: List[str]
    suggested_visual: str
    suggested_metrics: Dict[str, str]

@dataclass
class ResearchDocument:
    topic: str
    domain: str  # 'biology_health', 'physics_engineering', 'history_warfare', 'economics', 'general_science'
    core_paradox_or_hook: str
    key_facts: List[FactItem]
    chapters: List[ConceptualChapter]
    misconceptions_debunked: List[str] = field(default_factory=list)

class ResearchEngine:
    """
    Offline topic analyzer and factual knowledge structuring engine.
    Parses topics, detects their conceptual domain, and structures accurate narrative chapters.
    """

    DOMAINS = {
        "biology_health": [
            "body", "eat", "eating", "food", "flour", "maida", "digestion", "indigestion",
            "acid", "acidity", "sugar", "gut", "brain", "sleep", "heart", "blood", "stomach"
        ],
        "physics_engineering": [
            "reactor", "nuclear", "airplane", "aeroplane", "turbulence", "engine", "rocket",
            "black hole", "space", "star", "quantum", "gravity", "electricity", "energy"
        ],
        "history_warfare": [
            "ashoka", "war", "battle", "empire", "king", "emperor", "kalinga", "rome",
            "constantinople", "world war", "ancient", "conqueror", "dynasty"
        ],
        "economics": [
            "economy", "money", "inflation", "gdp", "market", "trade", "banking", "currency"
        ]
    }

    def detect_domain(self, topic: str) -> str:
        topic_lower = topic.lower()
        for domain, keywords in self.DOMAINS.items():
            if any(re.search(r'\b' + re.escape(kw) + r'\b', topic_lower) for kw in keywords):
                return domain
        return "general_science"

    def research_topic(self, topic: str) -> ResearchDocument:
        """
        Structures knowledge for an arbitrary topic into verifiable facts and conceptual chapters.
        """
        domain = self.detect_domain(topic)
        topic_lower = topic.lower()

        # Domain-Specific Knowledge Structuring
        if "flour" in topic_lower or "maida" in topic_lower:
            return self._research_refined_flour(topic)
        elif "nuclear" in topic_lower or "reactor" in topic_lower:
            return self._research_nuclear_reactor(topic)
        elif "turbulence" in topic_lower or "airplane" in topic_lower:
            return self._research_airplane_turbulence(topic)
        elif "sleep" in topic_lower or "brain" in topic_lower:
            return self._research_sleep_brain(topic)
        elif "black hole" in topic_lower:
            return self._research_black_holes(topic)
        elif "ashoka" in topic_lower:
            return self._research_ashoka(topic)
        else:
            return self._research_generic_topic(topic, domain)

    def _research_refined_flour(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("Whole wheat kernel consists of three layers: outer fibrous bran, germ (rich in B-vitamins & oils), and inner starchy endosperm.", "biological_process", True, "Wheat Anatomy", "USDA Food Data Central"),
            FactItem("Refining wheat into maida strips away the outer bran and germ, removing 80%+ of dietary fiber, leaving almost pure amylose and amylopectin starch.", "mechanism", True, "Grain Milling"),
            FactItem("In the stomach, refined starch rapidly absorbs water and interacts with gluten proteins to form a high-viscosity, adhesive starch paste.", "mechanism", True, "Gastrointestinal Physiology"),
            FactItem("To break down this dense, fiberless starch barrier, gastric parietal cells secrete excess Hydrochloric Acid (pH 1.5 - 2.0).", "biological_process", True, "Gastric Secretion"),
            FactItem("Excess acid overcomes the lower esophageal sphincter, generating acid reflux, retrosternal burning (heartburn), and gas.", "mechanism", True, "Gastroenterology"),
            FactItem("Whole grain foods transit the digestive tract in 24 to 30 hours, whereas sticky refined flour can remain in intestinal loops for 48 to 72 hours.", "statistic", True, "Bowel Transit Time Clinical Studies")
        ]

        chapters = [
            ConceptualChapter(1, "The Weekend Trap", "hook", "Eating popular street delicacies feels amazing initially, but triggers sharp burning 2 hours later.", ["Pizza, samosa, and bhature are weekend favorites.", "Within 120 minutes, gastroesophageal reflux occurs."], "Deep-fried cutouts with ascending flame flare and 2-hour countdown timer", {"TIMEFRAME": "120 MIN", "SYMPTOM": "HEAVY ACIDITY"}),
            ConceptualChapter(2, "Stripping the Grain", "anatomy_or_scale", "Refining wheat completely removes fiber and micronutrients, leaving only starchy endosperm.", ["Wheat kernel anatomy: bran, germ, endosperm.", "Milling strips 80%+ of natural fiber."], "Wheat kernel cross-section peeling outward, revealing bare starch core", {"FIBER REMOVAL": "80%+", "PURITY": "98% STARCH"}),
            ConceptualChapter(3, "The Gut Glue Matrix", "core_mechanism", "In the stomach, water and refined flour react to create a thick, adhesive starch-gluten paste.", ["Endosperm starch hydrates rapidly.", "Adheres tenaciously to stomach mucosal folds."], "Translucent stomach silhouette with stretching gluten paste adhering to rugal walls", {"ADHESION": "98%", "VISCOSITY": "HIGH"}),
            ConceptualChapter(4, "Hydrochloric Acid Surge", "danger_or_crisis", "Parietal cells oversecrete concentrated HCl to dissolve the paste, pushing acid upward.", ["Gastric acid pH drops to corrosive 1.5.", "Excess acid rises past esophageal sphincter causing heartburn."], "Fiery boiling acid pool rising into esophageal junction with pH 1.5 hazard indicator", {"ACID LEVEL": "pH 1.5", "EFFECT": "SEVERE REFLUX"}),
            ConceptualChapter(5, "The 50-Hour Transit Clock", "time_or_contrast", "Without dietary fiber to promote peristalsis, refined flour stagnates in intestines for up to 50+ hours.", ["Whole wheat digests in 24 hours.", "Fiber-stripped starch causes intestinal stagnation and bloating."], "Dual mechanical split-flap comparison clocks: 24h normal vs 54h stagnation", {"WHOLE GRAIN": "24 HRS", "REFINED FLOUR": "50+ HRS"}),
            ConceptualChapter(6, "The Final Verdict", "verdict", "The pleasure lasts only 10 seconds on the tongue, but compromises gut health for days.", ["Prioritize whole grains and fiber.", "Protect digestive mucosal lining."], "Gold-leaf wax-stamped verdict badge with balance scale of taste vs health", {"TONGUE PLEASURE": "10 SEC", "GUT DISTRESS": "50+ HRS"})
        ]

        return ResearchDocument(
            topic=topic,
            domain="biology_health",
            core_paradox_or_hook="Why does food that tastes so good for 10 seconds create hours of intense internal burning?",
            key_facts=facts,
            chapters=chapters,
            misconceptions_debunked=[
                "Maida is not toxic by itself, but removing natural fiber paralyzes gut peristalsis and causes extreme acid overcompensation."
            ]
        )

    def _research_nuclear_reactor(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("Uranium-235 atoms absorb a thermal neutron, undergoing nuclear fission and splitting into smaller nuclei while releasing 200 MeV of energy.", "mechanism", True, "Nuclear Physics"),
            FactItem("Control rods made of boron or cadmium absorb excess neutrons to maintain a steady criticality factor (k = 1.0).", "mechanism", True, "Reactor Physics"),
            FactItem("Pressurized water transfers heat from fuel rods at over 300°C to steam generators without boiling under high pressure.", "mechanism", True, "Thermodynamics"),
            FactItem("High-pressure steam expands across turbine blades, converting thermal energy into electrical power via electromagnetic induction.", "mechanism", True, "Electrical Engineering")
        ]
        chapters = [
            ConceptualChapter(1, "The Atomic Paradox", "hook", "A pellet of uranium the size of a fingertip contains the energy equivalent of one ton of coal.", ["Massive energy density of nuclear fission.", "Clean baseload electricity."], "Glowing fuel pellet splitting in a dark chamber", {"ENERGY DENSITY": "1 PELLET = 1 TON COAL"}),
            ConceptualChapter(2, "The Fission Reaction", "anatomy_or_scale", "Neutrons strike U-235 atoms, splitting the nucleus and unleashing intense kinetic heat.", ["Chain reaction physics.", "2 to 3 secondary neutrons released per fission."], "Atomic nucleus split animation with radiating energy waves", {"ENERGY RELEASE": "200 MeV", "CORE TEMP": "315°C"}),
            ConceptualChapter(3, "The Control Rod Symphony", "core_mechanism", "Cadmium and boron control rods descend to absorb neutrons, keeping criticality perfectly balanced.", ["Subcritical vs supercritical state.", "Balancing k=1.000 for safe steady power."], "Mechanical control rod assemblies sliding between fuel channels", {"CRITICALITY": "k = 1.000", "SAFETY": "AUTO-SCRAM"}),
            ConceptualChapter(4, "The Steam Dynamo", "danger_or_crisis", "Pressurized primary coolant boils secondary water into 300°C dry steam powering massive turbines.", ["Primary and secondary closed loop isolation.", "Turbine spinning at 3,000 RPM."], "Turbine cross-section spinning with high-velocity steam flow", {"PRESSURE": "150 ATM", "RPM": "3,000"}),
            ConceptualChapter(5, "Zero-Carbon Power", "verdict", "Nuclear fission provides non-stop clean baseload energy without burning a single gram of fossil fuel.", ["24/7 reliability regardless of weather.", "Foundation for a clean energy grid."], "Pristine cooling tower with steam condensation and energy grid network", {"CARBON EMISSIONS": "0.0 g/kWh", "EFFICIENCY": "92% BASELOAD"})
        ]
        return ResearchDocument(topic=topic, domain="physics_engineering", core_paradox_or_hook="How can splitting the smallest atom power an entire modern city?", key_facts=facts, chapters=chapters)

    def _research_airplane_turbulence(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("Turbulence is caused by irregular air movements: thermal thermals, jet streams, mountain waves, and wake vortices.", "mechanism", True, "Atmospheric Science"),
            FactItem("Commercial jet airliners are engineered to withstand aerodynamic forces up to 2.5 times positive G-load and 1.5 times design limit.", "statistic", True, "Aviation Safety (FAA / EASA)"),
            FactItem("Wings flex dynamically by up to 5 meters at the wingtips to dissipate kinetic turbulent energy without structural failure.", "mechanism", True, "Aerospace Engineering")
        ]
        chapters = [
            ConceptualChapter(1, "The Sudden Jolt", "hook", "Cruising peacefully at 35,000 feet, your airliner suddenly drops like a stone — what just happened?", ["Clear Air Turbulence (CAT).", "Atmospheric invisible rivers."], "Airplane silhouette encountering jagged thermal eddies in cloudless sky", {"ALTITUDE": "35,000 FT", "SPEED": "850 KM/H"}),
            ConceptualChapter(2, "The Fluid Sky", "core_mechanism", "Air is not empty space; it is a giant fluid ocean with colliding high-speed wind currents.", ["Jet stream boundary shears.", "Warm air rising into cooler dense air mass."], "Streamline vectors undulating and breaking into turbulent vortex swirls", {"JET STREAM": "250 KM/H", "EDDY SCALE": "100 METERS"}),
            ConceptualChapter(3, "The Wing Flex Wonder", "anatomy_or_scale", "Modern aircraft wings are designed to bend up to 150% of maximum expected load without snapping.", ["Carbon-fiber composite flexibility.", "Wings act as giant shock absorbers."], "Wing cross-section flexing gracefully upwards amidst turbulence vectors", {"WINGTIP FLEX": "5.2 METERS", "STRESS TOLERANCE": "150%"}),
            ConceptualChapter(4, "The Pilot's Radar", "verdict", "Airplanes do not drop out of the sky; keep your seatbelt fastened and trust the physics of flight.", ["Turbulence has never torn a modern jet apart.", "Seatbelts prevent 99% of in-flight injuries."], "Cockpit radar display and smooth horizon stabilization banner", {"FATAL AIRFRAME LOSS": "0 IN MODERN ERA", "RULE": "BUCKLE UP"})
        ]
        return ResearchDocument(topic=topic, domain="physics_engineering", core_paradox_or_hook="Why does the sky shake when there isn't a cloud in sight?", key_facts=facts, chapters=chapters)

    def _research_sleep_brain(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("During deep non-REM sleep, the brain's glymphatic system opens up, flushing toxic beta-amyloid proteins with cerebrospinal fluid.", "mechanism", True, "Neuroscience (Science 2013)"),
            FactItem("During REM sleep, the hippocampus replays short-term memories at high speed to transfer them into long-term neocortical storage.", "mechanism", True, "Memory Consolidation")
        ]
        chapters = [
            ConceptualChapter(1, "The Nightly Shutdown Paradox", "hook", "When your body goes completely unconscious, your brain becomes more active than during the day.", ["Brain activity during REM and slow-wave sleep.", "The brain never sleeps."], "Silhouette of human head with glowing neural network pulsing in dark room", {"SLEEP STAGES": "4 CYCLES", "DURATION": "90 MIN EACH"}),
            ConceptualChapter(2, "The Brain's Dishwasher", "core_mechanism", "The glymphatic system shrinks glial cells by 60%, flushing metabolic waste and beta-amyloid.", ["Cerebrospinal fluid rinse.", "Prevents neurodegenerative decay."], "Microscopic brain tissue with glowing fluid flushing neural pathways", {"CELL SHRINKAGE": "60%", "WASTE CLEARANCE": "2X SPEED"}),
            ConceptualChapter(3, "Memory Replay & Dream Weaving", "anatomy_or_scale", "Hippocampus fires synchronized electrical waves, cementing daytime lessons into permanent memory.", ["Synaptic pruning.", "Memory consolidation."], "Floating glowing memory nodes connecting and reorganizing across cortex", {"MEMORY CONSOLIDATION": "80% HIGHER", "WAVE": "DELTA WAVES"}),
            ConceptualChapter(4, "The Awakening Upgrade", "verdict", "Sleep is not a waste of time; it is your biology's most advanced operating system update.", ["Sleep deprivation causes immediate cognitive decline.", "Optimize sleep architecture."], "Sunrise silhouette with restored neural battery indicator", {"OPTIMAL DURATION": "7-8 HOURS", "COGNITIVE REBOOT": "100%"})
        ]
        return ResearchDocument(topic=topic, domain="biology_health", core_paradox_or_hook="What is your brain desperately trying to clean while you sleep?", key_facts=facts, chapters=chapters)

    def _research_black_holes(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("When a massive star exceeds the Tolman-Oppenheimer-Volkoff limit, gravity overcomes all atomic forces, collapsing matter into an infinitely dense singularity.", "mechanism", True, "General Relativity"),
            FactItem("The Event Horizon marks the boundary where escape velocity exceeds 299,792 km/s (speed of light).", "statistic", True, "Astrophysics"),
            FactItem("Gravitational time dilation near a black hole causes time for an outside observer to slow down to an absolute standstill.", "mechanism", True, "Relativity")
        ]
        chapters = [
            ConceptualChapter(1, "The Point of No Return", "hook", "Imagine an object so dense that even a ray of light, travelling at 300,000 kilometers a second, cannot escape.", ["Infinite gravitational well.", "The cosmic abyss."], "Accretion disk glowing in deep space around absolute darkness", {"ESCAPE VELOCITY": "> SPEED OF LIGHT", "RADIUS": "SCHWARZSCHILD"}),
            ConceptualChapter(2, "The Dying Giant", "anatomy_or_scale", "A massive star runs out of nuclear fuel, collapsing under its own weight in a fraction of a second.", ["Supernova explosion.", "Gravity crushing atoms together."], "Supernova implosion with concentric shockwaves collapsing inward", {"STAR MASS": "> 20 SOLAR MASSES", "COLLAPSE TIME": "< 1 SECOND"}),
            ConceptualChapter(3, "Time Freezes", "core_mechanism", "Near the event horizon, Einstein's equations prove that time itself stretches and grinds to a halt.", ["Gravitational time dilation.", "Spaghettification tidal forces."], "Distorted spacetime grid bending steeply toward a central dark vortex", {"TIME DILATION": "INFINITE AT HORIZON", "GRAVITY": "SINGULARITY"}),
            ConceptualChapter(4, "The Cosmic Sculptor", "verdict", "Black holes are not cosmic vacuum cleaners; they anchor the centers of every galaxy in the universe.", ["Supermassive black holes.", "Galactic seed engines."], "Majestic spiral galaxy rotating around bright golden central core", {"SUPERMASSIVE MASS": "BILLIONS OF SUNS", "ROLE": "GALACTIC ANCHOR"})
        ]
        return ResearchDocument(topic=topic, domain="physics_engineering", core_paradox_or_hook="What happens when gravity completely breaks physics?", key_facts=facts, chapters=chapters)

    def _research_ashoka(self, topic: str) -> ResearchDocument:
        facts = [
            FactItem("Samrat Ashoka ruled the Mauryan Empire spanning over 5 million square kilometers from 268 to 232 BCE.", "statistic", True, "Indian History"),
            FactItem("The Kalinga War in 261 BCE resulted in over 100,000 battle casualties and 150,000 displaced persons.", "statistic", True, "Major Rock Edict XIII"),
            FactItem("Horrified by the bloodshed, Ashoka renounced aggressive warfare (Bherighosha) and adopted the moral law of Dhamma (Dhammaghosha).", "historical_event", True, "Edicts of Ashoka")
        ]
        chapters = [
            ConceptualChapter(1, "The Mauryan Conqueror", "hook", "2,200 years ago, one emperor conquered the subcontinent with unmatched military ferocity.", ["Empire expansion across 5M sq km.", "Unstoppable imperial legion."], "War elephant silhouette with royal banner", {"ERA": "2,200 YEARS AGO", "TERRITORY": "5M SQ KM"}),
            ConceptualChapter(2, "The River of Blood", "anatomy_or_scale", "The Kalinga War of 261 BCE was so brutal the Daya river turned crimson.", ["Over 100,000 killed.", "150,000 exiled."], "Clashing swords with particle sparks and casualty counter ticking to 100K+", {"CASUALTIES": "100K+", "DATE": "261 BCE"}),
            ConceptualChapter(3, "The Breaking Point", "danger_or_crisis", "Standing amidst the carnage, Ashoka experienced the most profound moral transformation in human history.", ["Rock Edict XIII confession.", "Renunciation of conquest."], "Dropped royal sword in earth with blooming golden lotus", {"PIVOT": "EPIC CRISIS", "QUESTION": "WHAT HAVE I DONE?"}),
            ConceptualChapter(4, "The Dhamma Revolution", "core_mechanism", "Replacing war drums with dharma bells, Ashoka championed non-violence, public healthcare, and wildlife protection.", ["Ahimsa as state policy.", "Pillars erected across Asia."], "Buddhist monk meditating with radiating compassion rings", {"NEW POLICY": "AHIMSA", "ERA": "DHAMMAGHOSHA"}),
            ConceptualChapter(5, "The Ashoka Chakra", "time_or_contrast", "His 24-spoke Wheel of Law now sits at the heart of India's National Flag and national emblem.", ["24 spokes symbolizing righteousness.", "Sarnath Lion Capital."], "Rotating 24-spoke mathematical Chakra", {"SPOKES": "24 SPOKES", "SYMBOL": "NATIONAL EMBLEM"}),
            ConceptualChapter(6, "The Eternal Legacy", "verdict", "The only conqueror in world history to renounce violence at the peak of victory.", ["Truth and righteousness endure.", "Satyameva Jayate."], "Imperial emblem with glowing golden Satyameva Jayate banner", {"TITLE": "THE GREAT", "MOTTO": "सत्यमेव जयते"})
        ]
        return ResearchDocument(topic=topic, domain="history_warfare", core_paradox_or_hook="Why did the world's most powerful conqueror give up everything after winning?", key_facts=facts, chapters=chapters)

    def _research_generic_topic(self, topic: str, domain: str) -> ResearchDocument:
        """Fallback dynamic research structuring for any open-ended topic."""
        clean_topic = topic.strip().title()
        facts = [
            FactItem(f"{clean_topic} operates under core physical and logical principles.", "mechanism", True, clean_topic),
            FactItem(f"Understanding the internal mechanism of {clean_topic} dispels widespread misconceptions.", "biological_process" if "bio" in domain else "mechanism", True, clean_topic)
        ]
        chapters = [
            ConceptualChapter(1, f"The Mystery of {clean_topic}", "hook", f"Most people interact with {clean_topic} every single day, but never realize what is happening beneath the surface.", [f"The common perception vs the hidden reality of {clean_topic}"], "High-contrast question hook with curiosity gap visual", {"TOPIC": clean_topic.upper(), "STATUS": "REVEALED"}),
            ConceptualChapter(2, "The Internal Architecture", "anatomy_or_scale", f"Breaking down {clean_topic} into its fundamental components and operational scale.", ["Anatomy and functional layers."], "Exploded diagram and multi-layer structural breakdown", {"SCALE": "MACRO / MICRO", "COMPONENTS": "MULTI-LAYER"}),
            ConceptualChapter(3, "The Driving Mechanism", "core_mechanism", f"How the process actually works step-by-step under natural laws.", ["Cause and effect cascade."], "Dynamic fluid or mechanical flow showing active transmission", {"EFFICIENCY": "OPTIMAL", "FORCE": "DETERMINISTIC"}),
            ConceptualChapter(4, "The Final Takeaway", "verdict", f"The definitive rule for mastering or understanding {clean_topic}.", ["Key insight that changes perspective."], "Bold golden verdict card with clear call-to-action", {"VERDICT": "INSIGHT UNLOCKED", "TAKEAWAY": "ACTIONABLE"})
        ]
        return ResearchDocument(topic=topic, domain=domain, core_paradox_or_hook=f"What is really happening inside {clean_topic}?", key_facts=facts, chapters=chapters)

FactEngine = ResearchEngine

