"""
AI Self-Enhancement System

This module serves as the main entry point for the AI Self-Enhancement system.
It integrates the capability registry, self-reflection components, autonomous project management,
and cross-domain knowledge linking to demonstrate the system's ability to perform tasks,
analyze its performance, manage its own development, and make innovative connections.
"""

import os
import sys
import logging
import importlib.util
from capability_registry import CapabilityRegistry
from self_reflection import SelfReflection
from time_utils import get_timestamp, get_time_difference
from error_handling import AISelfEnhancementError
from capability_decorator import load_capability, CapabilityValidationError
from autonomous_pm import AutonomousProjectManager
from visualization import plot_task_completion_rate, plot_task_priority_distribution, plot_progress_over_time
from knowledge_linker import KnowledgeLinker

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AISelfEnhancementSystem:
    """
    The main class for the AI Self-Enhancement System.

    This class integrates the capability registry, self-reflection modules, autonomous project management,
    and cross-domain knowledge linking to create a system that can perform tasks, analyze its own performance,
    manage its own development process, and make innovative connections between different domains.
    """

    def __init__(self):
        """Initialize the AI Self-Enhancement System."""
        self.capability_registry = CapabilityRegistry()
        self.self_reflection = SelfReflection(self.capability_registry)
        kanban_path = os.path.join(os.path.dirname(__file__), '..', 'kanban-board.md')
        self.project_manager = AutonomousProjectManager(kanban_path)
        self.knowledge_linker = KnowledgeLinker(self.capability_registry)

    def run(self):
        """
        Run the AI Self-Enhancement System.

        This method demonstrates the system's capabilities by registering initial
        capabilities, performing sample tasks, analyzing its performance, managing its own development,
        and making cross-domain connections.
        """
        try:
            start_time = get_timestamp()
            logging.info(f"AI Self-Enhancement System Initializing... (Start time: {start_time})")

            # Register initial capabilities
            self.register_initial_capabilities()
            self.load_custom_capabilities()

            # Build the knowledge graph
            self.knowledge_linker.build_knowledge_graph()

            while True:
                self.display_menu()
                choice = self.get_valid_input("Enter your choice (1-7): ", ['1', '2', '3', '4', '5', '6', '7'])

                if choice == '1':
                    self.perform_task_interface()
                elif choice == '2':
                    self.analyze_performance()
                elif choice == '3':
                    self.suggest_improvements()
                elif choice == '4':
                    self.run_autonomous_pm()
                elif choice == '5':
                    self.analyze_project_management_performance()
                elif choice == '6':
                    self.cross_domain_knowledge_interface()
                elif choice == '7':
                    print("Exiting AI Self-Enhancement System. Goodbye!")
                    break

            end_time = get_timestamp()
            total_runtime = get_time_difference(start_time, end_time)
            logging.info(f"Total runtime: {total_runtime:.2f} seconds")

        except AISelfEnhancementError as e:
            logging.error(f"An error occurred: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
        finally:
            logging.info("AI Self-Enhancement System shutting down.")

    # ... [other methods remain unchanged] ...

    def cross_domain_knowledge_interface(self):
        """Interface for cross-domain knowledge linking."""
        while True:
            print("\nCross-Domain Knowledge Linking")
            print("1. Extract concepts from text")
            print("2. Find cross-domain links for a concept")
            print("3. Suggest innovative applications")
            print("4. Return to main menu")
            
            choice = self.get_valid_input("Enter your choice (1-4): ", ['1', '2', '3', '4'])
            
            if choice == '1':
                self.extract_concepts_interface()
            elif choice == '2':
                self.find_cross_domain_links_interface()
            elif choice == '3':
                self.suggest_innovative_applications_interface()
            elif choice == '4':
                break

    def extract_concepts_interface(self):
        """Interface for extracting concepts from text."""
        text = input("Enter the text to extract concepts from: ")
        try:
            concepts = self.knowledge_linker.extract_concepts(text)
            print("\nExtracted concepts:")
            for concept in concepts:
                print(f"- {concept}")
        except Exception as e:
            print(f"An error occurred while extracting concepts: {str(e)}")

    def find_cross_domain_links_interface(self):
        """Interface for finding cross-domain links."""
        concept = input("Enter a concept to find cross-domain links: ")
        try:
            links = self.knowledge_linker.find_cross_domain_links(concept)
            print("\nCross-domain links:")
            for link in links:
                print(f"- {link['concept']} (Relevance: {link['relevance_score']:.2f})")
                print(f"  Common applications: {', '.join(link['common_applications'])}")
        except Exception as e:
            print(f"An error occurred while finding cross-domain links: {str(e)}")

    def suggest_innovative_applications_interface(self):
        """Interface for suggesting innovative applications."""
        capabilities = self.capability_registry.list_capabilities()
        print("Available capabilities:")
        for i, cap in enumerate(capabilities, 1):
            print(f"{i}. {cap}")
        
        selected = input("Enter the numbers of capabilities to combine (comma-separated): ")
        try:
            selected_capabilities = [capabilities[int(i)-1] for i in selected.split(',')]
            suggestions = self.knowledge_linker.suggest_innovative_applications(selected_capabilities)
            print("\nInnovative application suggestions:")
            for suggestion in suggestions[:10]:  # Limit to top 10 suggestions
                print(f"- {suggestion}")
        except Exception as e:
            print(f"An error occurred while suggesting innovative applications: {str(e)}")

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 40)
        print("AI Self-Enhancement System Menu:")
        print("=" * 40)
        print("1. Perform a task")
        print("2. Analyze performance")
        print("3. Suggest improvements")
        print("4. Run Autonomous Project Management")
        print("5. Analyze Project Management Performance")
        print("6. Cross-Domain Knowledge Linking")
        print("7. Exit")
        print("=" * 40)

    # ... [rest of the methods remain unchanged] ...

if __name__ == "__main__":
    ai_system = AISelfEnhancementSystem()
    ai_system.run()