"""
TODO Berücksichtigen, dass GPT nun Json-Objekte zurückgibt. Es gibt einen 
'Payload', sowie einen 'Reasoning' key.
"""
import ast
import astor
import os
from src.utils.ast_helpers import ClassFunctionVisitor, IndentLevelVisitor
from src.utils.observer import ObservableAgent
from src.config import PromptConfig
from src.models import LLModel
from src.controller.file_retriever import FileRetriever

class DocsAgent(ObservableAgent):
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            target_path: str,
            programming_language: str = "Python"
            ):
        super().__init__()
        self._prompts = prompts
        self._model = model
        self._programming_language = programming_language
        self.file_retriever = FileRetriever(target_path)
        self.project_name = os.path.basename(target_path.rstrip(os.sep)) # Letzter Ordername vom target_path, z.B. './path/to/IIRA' -> 'IIRA'

    def _add_observability(self, prompt):
        obs_prompt = self._prompts.get_observability_prompt()
        return "\n".join([prompt, obs_prompt])

    def _clean_list(self, lst):
        return [x for x in lst if x]

    def _get_class_name(self):
        return self.__class__.__name__

class InCodeAgent(DocsAgent):
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            target_path: str,
            programming_language: str = "Python"
            ):
        super().__init__(prompts, model, target_path, programming_language)
        self.in_code_docs_responses = {} # Datenstruktur mit allen Klassen- und Methodendokumentationen

    def make_in_code_docs(self):
        if self._programming_language == "Python":
            code_file_paths = self.file_retriever.get_mapping("py")
        elif self._programming_language == "Java":
            code_file_paths = self.file_retriever.get_mapping("java")
        else:
            raise ValueError("Programming language {} not supported."\
                             .format(self._programming_language))

        for file_path in code_file_paths:
            class_names = self._extract_classes(file_path)
            self._document_methods(file_path, class_names)

            if class_names:
                for class_name in class_names:
                    self._document_class(file_path, class_name)
    
    def _document_methods(self, file_path, class_names):
        self.in_code_docs_responses[file_path] = []
        for class_name in class_names + ["global"]:
            method_names = self._extract_methods(file_path, class_name)
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            if code.strip():
                # Files with content
                class_dict = {class_name: {}}
                for method_name in method_names:
                    class_dict[class_name][method_name] = self._document_method(
                        file_path,
                        method_name,
                        class_name
                        )
                self.in_code_docs_responses[file_path].append(class_dict)
            else:
                # Empty files
                self.in_code_docs_responses[file_path].append("This file is empty.")
                break

    def _document_method(self, file_path, method_name, class_name):
        prompt = self._prompts.get_document_method_prompt()
        prompt = self._add_observability(prompt)
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        return self._model.get_completion(
            prompt.format(
                source_code=code,
                method_name=method_name,
                class_name=class_name
                )
            )

    def _document_class(self, file_path, class_name):
        # Documentation purely based on docstrings in self.in_code_docs_resp
        prompt = self._prompts.get_document_class_prompt()
        prompt = self._add_observability(prompt)
        for i in range(len(self.in_code_docs_responses[file_path])):
            if class_name in self.in_code_docs_responses[file_path][i]:
                index = i
                break
        response = self._model.get_completion(
            prompt.format(
                class_name=class_name,
                class_dict=self.in_code_docs_responses[file_path][index][class_name]
                )
            )
        self.in_code_docs_responses[file_path][index][class_name][class_name] = response
        return response
   

    def _extract_classes(self, file_path):
        prompt = self._prompts.get_exract_classes_prompt()
        prompt = self._add_observability(prompt)
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
        prompt = self._add_observability(prompt)
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
    
    def write_in_code_docs(self):
        for file_path in self.in_code_docs_responses:
            if self.in_code_docs_responses[file_path] == ["This file is empty."]:
                # Skip files without any source code.
                continue
            self.write_with_ast(file_path, self.in_code_docs_responses[file_path])

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

    def make_readme(self):
        prompt = self._prompts.get_readme_prompt()
        prompt = self._add_observability(prompt)
        return self._model.get_completion(
            prompt.format(
                programming_language=self._programming_language,
                project_information=self.in_code_docs_responses
                )
            )

class SystemContextAgent(DocsAgent):
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            target_path: str,
            programming_language: str = "Python"
            ):
        super().__init__(prompts, model, target_path, programming_language)
        self.system_context_responses = []
        self.system_context_summary = ""

    def make_system_context_diagram(self):
        relevant_file_paths = self.file_retriever.get_mapping("py") \
                                #+ self.file_retriever.get_mapping("csv") \
                                #+ self.file_retriever.get_mapping("xlsx")

        for file_path in relevant_file_paths:
            self.system_context_responses.append(
                (
                    file_path,
                    self._find_context(file_path)
                )
            )
        self.system_context_summary = self._summarize_context()
        
        # Actually create the diagram using openai
        prompt = self._prompts.get_system_context_plantuml_prompt().format(
                system_context=self.system_context_summary,
                process_name=self.project_name
                )
        prompt = self._add_observability(prompt)
        data = self._model.get_completion(prompt)
        if data["payload"].startswith("```plantuml"):
            data["payload"] = data["payload"][11:]
        if data["payload"].endswith("```"):
            data["payload"] = data["payload"][:-3]

        event_type, data = self._format_data(
            data=data,
            prompt=prompt,
            class_name=self._get_class_name(),
            method_name="make_system_context_diagram",
            model_name=self._model._model_name
            )
        self.notify(event_type, data)

        return data["payload"]
    
    def _find_context(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        prompt = self._prompts.get_system_context_prompt().format(
            file_content=file_content
            )
        prompt = self._add_observability(prompt)
        data = self._model.get_completion(prompt)

        event_type, data = self._format_data(
            data=data,
            prompt=prompt,
            class_name=self._get_class_name(),
            method_name="_find_context",
            model_name=self._model._model_name
            )
        self.notify(event_type, data)

        return data["payload"]

    def _summarize_context(self):
        prompt = self._prompts.get_system_context_diagram_prompt().format(
                summaries_of_file_analyses=self.system_context_responses
                )
        prompt = self._add_observability(prompt)
        data = self._model.get_completion(prompt)

        event_type, data = self._format_data(
            data=data,
            prompt=prompt,
            class_name=self._get_class_name(),
            method_name="_summarize_context",
            model_name=self._model._model_name
            )
        self.notify(event_type, data)

        return data["payload"]

class ClassAgent(DocsAgent):
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            target_path: str,
            programming_language: str = "Python"
            ):
        super().__init__(prompts, model, target_path, programming_language)
        pass

class SWQAgent(DocsAgent):
    
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            target_path: str,
            programming_language: str = "Python"
            ):
        super().__init__(prompts, model, target_path, programming_language)
        self.quality_dimension_funcs = [ #Compatibility is missing
        prompts.get_functional_suitability_prompt,
        prompts.get_maintainability_prompt,
        prompts.get_performance_efficiency_prompt,
        prompts.get_portability_prompt,
        prompts.get_reliability_prompt,
        prompts.get_security_prompt,
        prompts.get_usability_prompt
        ]
        self.sqw_responses = { #Compatibility is missing
            "functional_suitability": {},
            "maintainability": {},
            "performance_efficiency": {},
            "portability": {},
            "reliability": {},
            "security": {},
            "usability": {}
        }


    def make_swq_docs(self):
        file_paths = self.file_retriever.get_mapping()
        print(file_paths)
        for file_path in file_paths:
            print(file_path)
            self._make_swq_docs(file_path)
    
    def _make_swq_docs(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        for func in self.quality_dimension_funcs:
            prompt_function = getattr(self._prompts, func.__name__)
            prompt = prompt_function()
            prompt = self._add_observability(prompt)
            #TODO Flawed, because the keys func.__name__ is not defined inside self.sqw_responses.
            print("Hello")
            self.sqw_responses[func.__name__][file_path] = self._model.get_completion(
                prompt.format(
                    source_code=code
                    )
                )

    def shafaits_new_method(self):
        pass