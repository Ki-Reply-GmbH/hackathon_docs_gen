import ast
from src.config import PromptConfig
from src.models import LLModel

class DocsAgent:
    def __init__(
            self,
            directory,
            tmp_file_paths,
            prompts: PromptConfig,
            model: LLModel
            ):
        self._directory = directory
        self._prompts = prompts
        self._model = model
        self.responses = {} #TODO Klassenhierarchie mit einbauen
        self.methods_loc = {}

        #TODO extract this on the fly (instead of argument)
        self.tmp_file_paths = tmp_file_paths
    
    def make_in_code_docs(self):
        for file_path in self.tmp_file_paths:
            self._document_methods(file_path)
    
    def _document_methods(self, file_path):
        class_names = self._extract_classes(file_path)  # Angenommen, diese Funktion gibt eine Liste der Klassennamen zurück
        self.responses[file_path] = []
        for class_name in class_names + ["global"]:
            method_names = self._extract_methods(file_path, class_name)  # Angenommen, diese Funktion gibt eine Liste von Methodennamen für die gegebene Klasse zurück
            locs = []
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            for method_name in method_names:
                locs.append(self._extract_methods_LoCs(code, method_name))
            self.methods_loc = dict(zip(method_names, locs))
            class_dict = {class_name: {}}
            for method_name in method_names:
                class_dict[class_name][method_name] = self._document_method(file_path, method_name)
            self.responses[file_path].append(class_dict)

    def _document_method(self, file_path, method_name):
        prompt = self._prompts.get_document_method_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code,
                method_name=method_name
                )
            )
    def _extract_classes(self, file_path):
        prompt = self._prompts.get_exract_classes_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code
                )
            ).split(";")

    def _extract_methods(self, file_path, class_name="global"):
        #TODO class_name Funktionalität implementieren.
        #Also, dass die Methoden nur für eine Klasse extrahiert werden.
        prompt = self._prompts.get_exract_methods_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code,
                class_name=class_name
                )
            ).split(";")

    def _extract_methods_LoCs(self, code, method_name, language="Python"):
        if language=="Python":
            lines = code.split('\n')
            method_indent = None
            for i, line in enumerate(lines, start=1):
                stripped = line.lstrip()
                if stripped.startswith("def " + method_name):
                    method_indent = len(line) - len(stripped)
                    return i
            return None
    
    def write_files(self):
        for i, response in enumerate(self.responses):
            with open(f"./generated_docs/docs_{i}.py", "w") as file:
                file.write(response)