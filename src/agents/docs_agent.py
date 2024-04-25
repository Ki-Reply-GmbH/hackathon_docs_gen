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
        self.responses = {}

        #TODO extract this on the fly (instead of argument)
        self.tmp_file_paths = tmp_file_paths
    
    def make_in_code_docs(self):
        #TODO nur temporär funktionalität zum debuggen
        for file_path in self.tmp_file_paths:
            pass
    
    def _document_methods(self, file_path, method_names):
        self.responses[file_path] = {}
        for method_name in method_names:
            self.responses[file_path][method_name] = self._document_method(file_path, method_name)

    def _document_method(self, file_path, method_name):
        prompt = self._prompts.document_method_prompt
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code,
                method_name=method_name
                )
            )

    def _extract_methods(self, file_path):
        prompt = self._prompts.extract_methods_prompt
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code
                )
            )

    def write_files(self):
        for i, response in enumerate(self.responses):
            with open(f"./generated_docs/docs_{i}.py", "w") as file:
                file.write(response)