import os
import hashlib
import yaml
from abc import ABC, abstractmethod

class FileSystemScanner:
    def scan(self, root_dir):
        file_info = {}
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_info[file_path] = self._get_file_hash(file_path)
        return file_info

    def _get_file_hash(self, file_path):
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

class ChangeDetector:
    def detect_changes(self, current_state, previous_state):
        changes = set(current_state.keys()) - set(previous_state.keys())
        for file_path in set(current_state.keys()) & set(previous_state.keys()):
            if current_state[file_path] != previous_state[file_path]:
                changes.add(file_path)
        return changes

class DocumentationBuilder(ABC):
    @abstractmethod
    def build(self, file_path):
        pass

class PythonDocBuilder(DocumentationBuilder):
    def build(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        # Simple documentation: just count functions and classes
        functions = content.count('def ')
        classes = content.count('class ')
        return f"# {os.path.basename(file_path)}\n\nFunctions: {functions}\nClasses: {classes}\n"

class MarkdownDocBuilder(DocumentationBuilder):
    def build(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        # Simple documentation: return first 100 characters
        return f"# {os.path.basename(file_path)}\n\n{content[:100]}...\n"

class DocumentationManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.scanner = FileSystemScanner()
        self.detector = ChangeDetector()
        self.builders = {
            '.py': PythonDocBuilder(),
            '.md': MarkdownDocBuilder(),
        }

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def update_documentation(self):
        current_state = self.scanner.scan(self.config['root_dir'])
        changes = self.detector.detect_changes(current_state, self.load_previous_state())
        documentation = []
        for file_path in changes:
            ext = os.path.splitext(file_path)[1]
            if ext in self.builders:
                documentation.append(self.builders[ext].build(file_path))
        self.save_state(current_state)
        return '\n'.join(documentation)

    def load_previous_state(self):
        if os.path.exists('previous_state.yml'):
            with open('previous_state.yml', 'r') as f:
                return yaml.safe_load(f)
        return {}

    def save_state(self, state):
        with open('previous_state.yml', 'w') as f:
            yaml.dump(state, f)

if __name__ == "__main__":
    doc_manager = DocumentationManager('doc_config.yaml')
    updated_docs = doc_manager.update_documentation()
    with open('documentation.md', 'w') as f:
        f.write(updated_docs)
    print("Documentation updated. Check 'documentation.md' for results.")
