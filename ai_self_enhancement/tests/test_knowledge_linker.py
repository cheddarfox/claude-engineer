import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from knowledge_linker import KnowledgeLinker
from capability_registry import CapabilityRegistry

class TestKnowledgeLinker(unittest.TestCase):

    def setUp(self):
        self.mock_registry = MagicMock(spec=CapabilityRegistry)
        self.knowledge_linker = KnowledgeLinker(self.mock_registry)

    def test_extract_concepts(self):
        text = "This is a test sentence for advanced concept extraction"
        concepts = self.knowledge_linker.extract_concepts(text)
        self.assertIn("test", concepts)
        self.assertIn("sentence", concepts)
        self.assertIn("concept", concepts)
        self.assertIn("extraction", concepts)
        self.assertIn("advanced concept", concepts)  # Test for bigram
        self.assertNotIn("is", concepts)  # Should not include stop words

    def test_get_synonyms(self):
        word = "happy"
        synonyms = self.knowledge_linker.get_synonyms(word)
        self.assertIsInstance(synonyms, list)
        self.assertGreater(len(synonyms), 0)
        self.assertNotIn(word, synonyms)  # Original word should not be in synonyms

    def test_generate_potential_applications(self):
        capability = "text_analysis"
        concepts = ["sentiment", "classification"]
        applications = self.knowledge_linker.generate_potential_applications(capability, concepts)
        self.assertIn("text_analysis for sentiment", applications)
        self.assertIn("sentiment optimization using text_analysis", applications)
        self.assertIn("text_analysis for classification", applications)
        self.assertIn("classification optimization using text_analysis", applications)
        
        # Check for synonym-based applications
        with patch.object(self.knowledge_linker, 'get_synonyms', return_value=["emotion"]):
            applications = self.knowledge_linker.generate_potential_applications(capability, ["sentiment"])
            self.assertIn("text_analysis for emotion", applications)
            self.assertIn("emotion enhancement with text_analysis", applications)

    def test_build_knowledge_graph(self):
        self.mock_registry.list_capabilities.return_value = ["capability1", "capability2"]
        self.mock_registry.get_capability.return_value = {"description": "This is a test capability for advanced analysis"}
        
        self.knowledge_linker.build_knowledge_graph()
        
        self.assertIn("capability1", self.knowledge_linker.knowledge_graph)
        self.assertIn("capability2", self.knowledge_linker.knowledge_graph)
        self.assertIn("test", self.knowledge_linker.knowledge_graph)
        self.assertIn("capability", self.knowledge_linker.knowledge_graph)
        self.assertIn("advanced analysis", self.knowledge_linker.knowledge_graph)

    def test_find_cross_domain_links(self):
        # Setup a simple knowledge graph for testing
        self.knowledge_linker.knowledge_graph = {
            "concept1": {"related_concepts": {"concept2"}, "potential_applications": {"app1", "app2"}},
            "concept2": {"related_concepts": {"concept1"}, "potential_applications": {"app2", "app3"}},
        }
        
        links = self.knowledge_linker.find_cross_domain_links("concept1")
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["concept"], "concept2")
        self.assertAlmostEqual(links[0]["relevance_score"], 0.5)
        self.assertIn("app2", links[0]["common_applications"])

    def test_suggest_innovative_applications(self):
        # Setup a simple knowledge graph for testing
        self.knowledge_linker.knowledge_graph = {
            "capability1": {"related_concepts": {"concept1", "concept2"}},
            "capability2": {"related_concepts": {"concept2", "concept3"}},
            "concept2": {"related_concepts": {"capability1", "capability2"}},
        }
        
        with patch.object(self.knowledge_linker, 'get_synonyms', return_value=["idea"]):
            suggestions = self.knowledge_linker.suggest_innovative_applications(["capability1", "capability2"])
            
            self.assertIn("Use capability1 and capability2 for concept2", suggestions)
            self.assertIn("Apply capability1 and capability2 to enhance idea", suggestions)

    def test_update_knowledge_graph(self):
        new_info = {
            "new_concept": {
                "related_concepts": {"existing_concept"},
                "potential_applications": {"new_app"}
            }
        }
        
        self.knowledge_linker.update_knowledge_graph(new_info)
        
        self.assertIn("new_concept", self.knowledge_linker.knowledge_graph)
        self.assertIn("existing_concept", self.knowledge_linker.knowledge_graph["new_concept"]["related_concepts"])
        self.assertIn("new_app", self.knowledge_linker.knowledge_graph["new_concept"]["potential_applications"])

if __name__ == '__main__':
    unittest.main()