"""
Script Engine for Viral Hinglish / Hindi / English Papercraft Explainers.
Structures arbitrary topics into high-retention micro-documentary storyboards.
Preserves existing get_ashoka_samrat_script() for backward compatibility.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add research engine to sys.path
AGENT_ROOT = Path(__file__).resolve().parent.parent
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from research.fact_engine import ResearchEngine, ResearchDocument, ConceptualChapter

@dataclass
class Chapter:
    chapter_num: int
    title: str
    start_sec: float
    end_sec: float
    narration_hinglish: str
    visual_cue: str
    headline_sub: str
    headline_main: str
    metric_title: str
    metric_val: str
    metric_sub: str
    keywords: List[str] = field(default_factory=list)
    genre: str = "general_explainer"
    narration_lex: Optional[str] = None

class ScriptEngine:
    """Generates structured viral video storyboards from research or built-in topics."""

    def __init__(self):
        self.research_engine = ResearchEngine()

    def generate_script(self, topic: str, language: str = "hinglish") -> List[Chapter]:
        """
        Dynamically generates a structured, high-retention script for any topic.
        Does NOT hard-code chapter count: adapts dynamically to the topic.
        """
        # If topic specifically asks for Ashoka, return the flagship script
        if "ashoka" in topic.lower():
            return self.get_ashoka_samrat_script()

        # Step 1: Research and extract verified factual chapters
        research_doc = self.research_engine.research_topic(topic)
        return self.generate_script_from_research(research_doc, language=language)

    def generate_script_from_research(self, doc: ResearchDocument, language: str = "hinglish") -> List[Chapter]:
        """
        Converts a factual research document into a timed narrative script.
        Supports Hinglish, Hindi, and English phrasing with punchy delivery.
        """
        chapters: List[Chapter] = []
        current_time = 0.0

        for c_idx, concept in enumerate(doc.chapters):
            ch_num = concept.chapter_index
            title = concept.title

            # Generate natural conversational narration per language
            narration = self._craft_narration(doc, concept, language)

            # Estimate duration based on word count (~150 WPM comfortable delivery)
            word_count = len(narration.split())
            estimated_duration = max(5.0, round(word_count / 2.5, 2))

            start_t = round(current_time, 2)
            end_t = round(current_time + estimated_duration, 2)
            current_time = end_t + 0.35  # 350ms breather between scenes

            # Metrics
            metrics = concept.suggested_metrics
            m_keys = list(metrics.keys())
            m_title = m_keys[0] if m_keys else "KEY METRIC"
            m_val = metrics[m_title] if m_keys else "VERIFIED"
            m_sub = f"{m_keys[1]}: {metrics[m_keys[1]]}" if len(m_keys) > 1 else title.upper()

            # Keywords for kinetic typography highlights
            keywords = [w for w in narration.replace(',', '').replace('!', '').replace('?', '').replace('.', '').split() if len(w) > 4][:5]

            ch = Chapter(
                chapter_num=ch_num,
                title=title,
                start_sec=start_t,
                end_sec=end_t,
                narration_hinglish=narration,
                visual_cue=concept.suggested_visual,
                headline_sub=f"CHAPTER {ch_num:02d} · {concept.narrative_purpose.upper()}",
                headline_main=title.upper(),
                metric_title=m_title,
                metric_val=m_val,
                metric_sub=m_sub,
                keywords=keywords,
                genre=doc.domain
            )
            chapters.append(ch)

        return chapters

    def _craft_narration(self, doc: ResearchDocument, concept: ConceptualChapter, language: str) -> str:
        """Crafts punchy, conversational narrative lines according to narrative purpose."""
        purpose = concept.narrative_purpose

        # 1. Specialized Refined Flour (Maida) Script
        if doc.domain == "biology_health" and ("flour" in doc.topic.lower() or "maida" in doc.topic.lower()):
            if purpose == "hook":
                return "Kabhi socha hai? Saturday night ko jab aap garma-garam pizza, samosa ya chhole bhature khate hain, to maza to bohot aata hai... Lekin theek do ghante baad, aapke seene me aag si lagti hai aur heavy acidity hone lagti hai! Aakhir kyun?"
            elif purpose == "anatomy_or_scale":
                return "Khel shuru hota hai gehu ke daane se. Ek whole wheat grain me teen parts hote hain: fibrous bran, nutrient-rich germ aur endosperm. Lekin maida banate waqt, saara fiber strip kar diya jata hai! Bachta hai sirf pure refined starch."
            elif purpose == "core_mechanism":
                return "Pet me jaate hi yeh starch paani se milkar ek viscous, sticky glue banata hai — bilkul wahi leyi jisse kagaz chipkate hain! Yeh aapki stomach lining par buri tarah chipak jata hai."
            elif purpose == "danger_or_crisis":
                return "Is chipchipi deewar ko todne ke liye, pet ko release karna padta hai extreme Hydrochloric Acid, pH level 1.5! Yahi corrosive acid jab upar gale me surge karta hai, to hoti hai severe heartburn aur acid reflux."
            elif purpose == "time_or_contrast":
                return "Normal fiber 24 hours me digest hokar nikal jata hai, lekin maida aapki intestines me 50 ghanto se bhi zyada samay tak atka rehta hai — causing massive gut bloating and constipation."
            elif purpose == "verdict":
                return "Toh agli baar bhature khane se pehle yaad rakhna: yeh taste sirf 10 second jeebh ka hai, lekin andar yeh aapke digestive system ka sabse bada dushman hai!"

        # 2. Specialized Nuclear Reactor Script
        elif doc.domain == "physics_engineering" and "nuclear" in doc.topic.lower():
            if purpose == "hook":
                return "A finger-sized pellet of uranium holds the same energy as one whole ton of coal! But how does a single atomic split power millions of homes safely?"
            elif purpose == "anatomy_or_scale":
                return "Inside the reactor core, stray thermal neutrons strike Uranium-235 atoms, splitting the nucleus and unleashing a ferocious 200 mega-electronvolts of thermal energy."
            elif purpose == "core_mechanism":
                return "To prevent a runaway explosion, boron control rods slide down between the fuel assemblies, absorbing excess neutrons and keeping criticality locked at exactly 1.000."
            elif purpose == "danger_or_crisis":
                return "Superheated water at 150 atmospheres pressure boils secondary loops into 300-degree dry steam, spinning massive turbine dynamos at 3,000 RPM."
            elif purpose == "verdict":
                return "Zero carbon emissions, non-stop 24/7 power — nuclear fission is not a bomb, it is humanity's most concentrated clean energy machine."

        # 3. Dynamic Knowledge Synthesis for any other topic
        facts_summary = " ".join(concept.supporting_facts)
        if language == "hinglish":
            if purpose == "hook":
                return f"Kabhi socha hai {doc.topic}? {concept.primary_fact}. Lekin iske peeche ka asli sach kya hai?"
            elif purpose == "anatomy_or_scale":
                return f"Agar hum iske andar dekhein, to {concept.primary_fact}. {facts_summary}."
            elif purpose == "core_mechanism":
                return f"Asli process shuru hota hai jab {concept.primary_fact}. Iske baad {facts_summary}."
            elif purpose == "danger_or_crisis":
                return f"Sabse bada turning point yahan aata hai: {concept.primary_fact}! Iska sidha impact padta hai."
            elif purpose == "verdict":
                return f"Toh final conclusion yeh hai: {concept.primary_fact}. {facts_summary}."
            else:
                return f"{concept.primary_fact}. {facts_summary}."
        else:
            return f"{concept.primary_fact}. {facts_summary}."

    @staticmethod
    def get_ashoka_samrat_script() -> List[Chapter]:
        """Built-in flagship script for Ashoka Samrat documentary (Preserved)."""
        return [
            Chapter(
                chapter_num=1,
                title="The Mauryan Conqueror",
                start_sec=0.0,
                end_sec=3.8,
                narration_hinglish="Bais sau saal pehle, Bharat par raaj tha ek aise samrat ka jiska naam sunkar dushman kaamp jaate the — Samrat Ashoka.",
                visual_cue="War elephant silhouette swaying gently with golden howdah and imperial flag.",
                headline_sub="2,200 YEARS AGO",
                headline_main="SAMRAT ASHOKA",
                metric_title="EMPIRE EXPANSION",
                metric_val="5M SQ KM",
                metric_sub="AFGHANISTAN TO BENGAL",
                keywords=["Bais", "sau", "Bharat", "samrat", "Ashoka"],
                genre="history_epic"
            ),
            Chapter(
                chapter_num=2,
                title="The Battle of Kalinga",
                start_sec=3.8,
                end_sec=8.0,
                narration_lex="Two sixty-one BCE ka Kalinga war itna bhayanak tha ki Daya nadi ka paani laal ho gaya, aur ek lakh se zyada log maare gaye.",
                narration_hinglish="Two sixty-one BCE ka Kalinga war itna bhayanak tha ki Daya nadi ka paani laal ho gaya, aur ek lakh se zyada log maare gaye.",
                visual_cue="Clashing swords with particle sparks, Daya river turning red, mechanical flip counter ticking to 100K+.",
                headline_sub="261 BCE · THE CARNAGE",
                headline_main="RIVER OF BLOOD",
                metric_title="KALINGA CASUALTIES",
                metric_val="100K+",
                metric_sub="SLAIN IN BATTLE · 150,000 EXILED",
                keywords=["Kalinga", "war", "Daya", "nadi", "lakh"],
                genre="history_epic"
            ),
            Chapter(
                chapter_num=3,
                title="The Breaking Point",
                start_sec=8.0,
                end_sec=11.8,
                narration_hinglish="Lekin us jeet ke baad, Ashoka ne charo taraf dekha aur unka dil kaamp utha — 'Yeh kaisi jeet hai jisme sirf maut hai?'",
                visual_cue="Dropped royal sword stuck in the battlefield earth, golden lotus blooming from ashes.",
                headline_sub="VICTORY IN BLOOD",
                headline_main="THE HORROR",
                metric_title="ROCK EDICT XIII",
                metric_val="EPIC PIVOT",
                metric_sub="WHAT HAVE I DONE?",
                keywords=["jeet", "Ashoka", "dekha", "maut"],
                genre="history_epic"
            ),
            Chapter(
                chapter_num=4,
                title="The Dhamma Revolution",
                start_sec=11.8,
                end_sec=15.6,
                narration_hinglish="Aur wahi se shuru hua vishva ka sabse bada badlaav — Ashoka ne talwaar chhodkar ahimsa aur Dhamma ka raasta apnaya.",
                visual_cue="Buddhist monk silhouette in meditation with radiating golden compassion light rings.",
                headline_sub="WAR DRUMS TO DHARMA BELLS",
                headline_main="DHAMMAGHOSHA",
                metric_title="ROYAL DECREE",
                metric_val="AHIMSA",
                metric_sub="BHERIGHOSHA TO DHAMMAGHOSHA",
                keywords=["vishva", "badlaav", "talwaar", "ahimsa", "Dhamma"],
                genre="history_epic"
            ),
            Chapter(
                chapter_num=5,
                title="The Ashoka Chakra",
                start_sec=15.6,
                end_sec=19.2,
                narration_hinglish="Unhone pure bharat me stambh banwaye, aur wahi chaubees teeliyo wala Ashoka Chakra aaj hamare Tirange ki shaan hai.",
                visual_cue="Mathematically rendered 24-spoke Navy Ashoka Chakra rotating smoothly at 60 deg/sec.",
                headline_sub="THE WHEEL OF LAW",
                headline_main="ASHOKA CHAKRA",
                metric_title="NATIONAL FLAG OF INDIA",
                metric_val="24 SPOKES",
                metric_sub="SARNATH LION CAPITAL",
                keywords=["bharat", "stambh", "chaubees", "Chakra", "Tirange"],
                genre="history_epic"
            ),
            Chapter(
                chapter_num=6,
                title="Eternal Legacy",
                start_sec=19.2,
                end_sec=22.31,
                narration_hinglish="Itihaas ka ekmatra raja jisne jeet ke baad yuddh ka tyaag kiya — Samrat Ashoka. Satyameva Jayate.",
                visual_cue="Sarnath Lion Capital monument emblem cutout with glowing golden Satyameva Jayate banner.",
                headline_sub="THE ONLY CONQUEROR",
                headline_main="ASHOKA THE GREAT",
                metric_title="NATIONAL MOTTO",
                metric_val="सत्यमेव जयते",
                metric_sub="TRUTH ALONE TRIUMPHS",
                keywords=["Itihaas", "raja", "yuddh", "tyaag", "Satyameva"],
                genre="history_epic"
            )
        ]
