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

        #TODO extract this on the fly (instead of argument)
        self.tmp_file_paths = tmp_file_paths
    
    def make_in_code_docs(self):
        for file_path in self.tmp_file_paths:
            self._document_methods(file_path)
    
    def _document_methods(self, file_path):
        method_names = self._extract_methods(file_path)
        self.responses[file_path] = {}
        for method_name in method_names:
            self.responses[file_path][method_name] = self._document_method(file_path, method_name)

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

    def _extract_methods(self, file_path):
        #TODO Damit umgehen können, dass Methodennamen mehrfach vorkommen
        # können (wenn sie zu unterschiedlichen Klassen gehören).
        prompt = self._prompts.get_exract_methods_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code
                )
            ).split(";")

    def write_files(self):
        for i, response in enumerate(self.responses):
            with open(f"./generated_docs/docs_{i}.py", "w") as file:
                file.write(response)