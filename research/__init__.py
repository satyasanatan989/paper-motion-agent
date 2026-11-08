"""
Research & Knowledge Extraction Layer for PaperMotion AI.
Transforms arbitrary user topics into structured, verified conceptual knowledge.
"""

from .fact_engine import ResearchEngine, FactEngine, ResearchDocument, FactItem, ConceptualChapter

__all__ = ["ResearchEngine", "FactEngine", "ResearchDocument", "FactItem", "ConceptualChapter"]
