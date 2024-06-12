import ast
import astor
import re
from src.utils.ast_helpers import ClassFunctionVisitor, IndentLevelVisitor
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
        self.responses = {} # Datenstruktur mit allen Klassen- und Methodendokumentationen

        #TODO extract this on the fly (instead of argument)
        self.tmp_file_paths = tmp_file_paths
    
    def make_in_code_docs(self):
        for file_path in self.tmp_file_paths:
            class_names = self._extract_classes(file_path) 
            self._document_methods(file_path, class_names)

            if class_names:
                #print("--- Documentating class ---")
                #print("file_path: ", file_path)
                #print("class_names: ", class_names)
                for class_name in class_names:
                    #print("class_name: ", class_name)
                    #print(self._document_class(file_path, class_name))
                    #print()
                    self._document_class(file_path, class_name)
    
    def _document_methods(self, file_path, class_names):
        self.responses[file_path] = []
        for class_name in class_names + ["global"]:
            method_names = self._extract_methods(file_path, class_name)
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            if code.strip():
                # Files with content
                class_dict = {class_name: {}}
                for method_name in method_names:
                    class_dict[class_name][method_name] = self._document_method(file_path, method_name)
                self.responses[file_path].append(class_dict)
            else:
                # Empty files
                self.responses[file_path].append("This file is empty.")
                break

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

    def _document_class(self, file_path, class_name):
        # Documentation purely based on docstrings in self.responses
        prompt = self._prompts.get_document_class_prompt()
        for i in range(len(self.responses[file_path])):
            print("self.responses[file_path]["+str(i)+"]")
            print(self.responses[file_path][i])
            if class_name in self.responses[file_path][i]:
                index = i
                break
        response = self._model.get_completion(
            prompt.format(
                class_name=class_name,
                class_dict=self.responses[file_path][index][class_name]
                )
            )
        self.responses[file_path][index][class_name][class_name] = response
        return response
   

    def _extract_classes(self, file_path):
        prompt = self._prompts.get_exract_classes_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        # Überprüfen, ob der Code nur aus Leerzeichen oder Zeilenumbrüchen besteht
        if not code.strip():
            return []
        
        return self._clean_list(
            self._model.get_completion(
                prompt.format(
                    source_code=code
                    )
                ).split(";")
            )

    def _extract_methods(self, file_path, class_name="global"):
        prompt = self._prompts.get_exract_methods_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._clean_list(
            self._model.get_completion(
                prompt.format(
                    source_code=code,
                    class_name=class_name
                    )
                ).split(";")
            )

    def _clean_list(self, lst):
        return [x for x in lst if x]
    
    def write_in_code_docs(self):
        for file_path in self.responses:
            if self.responses[file_path] == ["This file is empty."]:
                # Skip files without any source code.
                continue
            self.write_with_ast(file_path, self.responses[file_path])

    def write_with_ast(self, file_path, data):
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)
        indent_level_visitor = IndentLevelVisitor()
        indent_level_visitor.visit(tree)

        class_visitor = ClassFunctionVisitor(data, indent_level_visitor)
        class_visitor.visit(tree)

        modified_source_code = astor.to_source(tree)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_source_code)
        """
        for node in ast.walk(tree):
            # Check if the node has a 'name' attribute before trying to print it
            print("Node: ", node)
            if hasattr(node, 'name'):
                print("Node name: ", node.name)
            else:
                print("Node type without 'name': ", type(node).__name__)
            print()
        """