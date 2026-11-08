"""
Script Engine for Viral Hinglish Papercraft Explainers.
Structures any topic into a 6-chapter high-retention micro-documentary storyboard.
"""

from dataclasses import dataclass
from typing import List, Dict

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

class ScriptEngine:
    """Generates structured 6-chapter viral video storyboards."""

    @staticmethod
    def get_ashoka_samrat_script() -> List[Chapter]:
        """Built-in flagship script for Ashoka Samrat documentary."""
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
                metric_sub="AFGHANISTAN TO BENGAL"
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
                metric_sub="SLAIN IN BATTLE · 150,000 EXILED"
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
                metric_sub="WHAT HAVE I DONE?"
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
                metric_sub="BHERIGHOSHA TO DHAMMAGHOSHA"
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
                metric_sub="SARNATH LION CAPITAL"
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
                metric_sub="TRUTH ALONE TRIUMPHS"
            )
        ]
