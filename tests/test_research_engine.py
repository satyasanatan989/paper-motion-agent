"""Unit tests for offline Fact & Conceptual Research Engine."""

import unittest
from research.fact_engine import FactEngine, ResearchEngine

class TestResearchEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FactEngine()

    def test_health_domain_research(self):
        topic = "What happens inside your body after eating refined flour?"
        research = self.engine.research_topic(topic)
        self.assertEqual(research.domain, "biology_health")
        self.assertTrue(len(research.chapters) >= 5)
        self.assertTrue(len(research.key_facts) >= 3)
        self.assertTrue(any("endosperm" in f.claim.lower() for f in research.key_facts))

    def test_physics_domain_research(self):
        topic = "How does a nuclear reactor work?"
        research = self.engine.research_topic(topic)
        self.assertEqual(research.domain, "physics_engineering")
        self.assertTrue(len(research.chapters) >= 4)
        self.assertTrue(any("uranium" in f.claim.lower() or "fission" in f.claim.lower() for f in research.key_facts))

    def test_history_domain_research(self):
        topic = "Ashoka Samrat: The Emperor who gave up war"
        research = self.engine.research_topic(topic)
        self.assertEqual(research.domain, "history_warfare")
        self.assertTrue(len(research.chapters) >= 5)
        self.assertTrue(any("kalinga" in f.claim.lower() for f in research.key_facts))

    def test_generic_topic_research(self):
        topic = "Why do birds migrate across continents?"
        research = self.engine.research_topic(topic)
        self.assertEqual(research.domain, "general_science")
        self.assertTrue(len(research.chapters) >= 4)
        self.assertTrue(len(research.key_facts) >= 2)

if __name__ == '__main__':
    unittest.main()
