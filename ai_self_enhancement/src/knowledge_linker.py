"""
Cross-Domain Knowledge Linker Module

This module implements the cross-domain knowledge linking capabilities for the AI Self-Enhancement System.
It enables the system to make innovative connections between different areas of expertise.
"""

from typing import List, Dict, Any
from capability_registry import CapabilityRegistry
from collections import defaultdict
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

class KnowledgeLinker:
    def __init__(self, capability_registry: CapabilityRegistry):
        self.capability_registry = capability_registry
        self.knowledge_graph = defaultdict(lambda: {"related_concepts": set(), "potential_applications": set()})
        self.stop_words = set(stopwords.words('english'))

    def build_knowledge_graph(self):
        """
        Builds a knowledge graph based on the capabilities in the registry.
        """
        capabilities = self.capability_registry.list_capabilities()
        for capability in capabilities:
            capability_info = self.capability_registry.get_capability(capability)
            concepts = self.extract_concepts(capability_info['description'])
            self.knowledge_graph[capability]["related_concepts"].update(concepts)
            
            # Find relationships between concepts
            for concept in concepts:
                self.knowledge_graph[concept]["related_concepts"].add(capability)
            
            # Generate potential applications
            applications = self.generate_potential_applications(capability, concepts)
            self.knowledge_graph[capability]["potential_applications"].update(applications)

    def extract_concepts(self, text: str) -> List[str]:
        """
        Extracts key concepts from a given text using NLTK.
        
        Args:
            text (str): The text to extract concepts from.
            
        Returns:
            List[str]: A list of extracted concepts.
        """
        # Tokenize and tag parts of speech
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)
        
        # Extract nouns and adjectives as concepts
        concepts = []
        for word, tag in tagged:
            if tag.startswith('NN') or tag.startswith('JJ'):  # Nouns and adjectives
                if word not in self.stop_words and len(word) > 3:
                    concepts.append(word)
        
        # Add compound concepts (bigrams)
        bigrams = list(nltk.bigrams(tokens))
        for bg in bigrams:
            if all(word not in self.stop_words and len(word) > 3 for word in bg):
                concepts.append(' '.join(bg))
        
        return list(set(concepts))  # Remove duplicates

    def generate_potential_applications(self, capability: str, concepts: List[str]) -> List[str]:
        """
        Generates potential applications by combining the capability with extracted concepts.
        
        Args:
            capability (str): The name of the capability.
            concepts (List[str]): A list of concepts related to the capability.
            
        Returns:
            List[str]: A list of potential applications.
        """
        applications = []
        for concept in concepts:
            applications.append(f"{capability} for {concept}")
            applications.append(f"{concept} optimization using {capability}")
            
            # Add synonyms for more diverse applications
            synonyms = self.get_synonyms(concept)
            for synonym in synonyms:
                applications.append(f"{capability} for {synonym}")
                applications.append(f"{synonym} enhancement with {capability}")
        
        return list(set(applications))  # Remove duplicates

    def get_synonyms(self, word: str) -> List[str]:
        """
        Get synonyms for a given word using WordNet.
        
        Args:
            word (str): The word to find synonyms for.
            
        Returns:
            List[str]: A list of synonyms.
        """
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym != word and synonym not in synonyms:
                    synonyms.append(synonym)
        return synonyms[:5]  # Limit to 5 synonyms to avoid explosion

    def find_cross_domain_links(self, concept: str) -> List[Dict[str, Any]]:
        """
        Finds cross-domain links for a given concept.

        Args:
            concept (str): The concept to find links for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing linked concepts and their relevance scores.
        """
        links = []
        related_concepts = self.knowledge_graph[concept]["related_concepts"]
        for related_concept in related_concepts:
            common_applications = self.knowledge_graph[concept]["potential_applications"].intersection(
                self.knowledge_graph[related_concept]["potential_applications"]
            )
            relevance_score = len(common_applications) / len(self.knowledge_graph[related_concept]["potential_applications"])
            links.append({
                "concept": related_concept,
                "relevance_score": relevance_score,
                "common_applications": list(common_applications)
            })
        return sorted(links, key=lambda x: x["relevance_score"], reverse=True)

    def suggest_innovative_applications(self, capabilities: List[str]) -> List[str]:
        """
        Suggests innovative applications by combining multiple capabilities.

        Args:
            capabilities (List[str]): A list of capabilities to combine.

        Returns:
            List[str]: A list of suggested innovative applications.
        """
        suggestions = []
        for r in range(2, len(capabilities) + 1):
            for combo in itertools.combinations(capabilities, r):
                common_concepts = set.intersection(*(self.knowledge_graph[cap]["related_concepts"] for cap in combo))
                for concept in common_concepts:
                    suggestion = f"Use {' and '.join(combo)} for {concept}"
                    suggestions.append(suggestion)
                    
                    # Add suggestions using synonyms
                    synonyms = self.get_synonyms(concept)
                    for synonym in synonyms:
                        suggestion = f"Apply {' and '.join(combo)} to enhance {synonym}"
                        suggestions.append(suggestion)
        
        return list(set(suggestions))  # Remove duplicates

    def update_knowledge_graph(self, new_information: Dict[str, Any]):
        """
        Updates the knowledge graph with new information.

        Args:
            new_information (Dict[str, Any]): New information to be added to the knowledge graph.
        """
        for key, value in new_information.items():
            self.knowledge_graph[key]["related_concepts"].update(value.get("related_concepts", []))
            self.knowledge_graph[key]["potential_applications"].update(value.get("potential_applications", []))

# Add any additional methods or classes as needed