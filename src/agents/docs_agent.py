import ast
import re
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
        self.responses = {} # Datenstruktur mit allen Klassen- und Methodendokumentationen, sowie LoC

        #TODO extract this on the fly (instead of argument)
        self.tmp_file_paths = tmp_file_paths
    
    def make_in_code_docs(self):
        for file_path in self.tmp_file_paths:
            self._document_methods(file_path)
    
    def _document_methods(self, file_path):
        class_names = self._extract_classes(file_path) 
        self.responses[file_path] = []
        for class_name in class_names + ["global"]:
            method_names = self._extract_methods(file_path, class_name)
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            if code.strip():
                # Files with content
                class_dict = {class_name: {}}
                for method_name in method_names:
                    methods_loc = self._extract_methods_LoCs(code, method_name)
                    class_dict[class_name][method_name] = ["Method's LoC: " + str(methods_loc) ,self._document_method(file_path, method_name)]
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
    
    def _extract_classes(self, file_path):
        prompt = self._prompts.get_exract_classes_prompt()
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
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

    def _extract_methods_LoCs(self, code, method_name, language="Python"):
        if language=="Python":
            lines = code.split('\n')
            for i, line in enumerate(lines, start=1):
                stripped = line.lstrip()
                if stripped.startswith("def " + method_name):
                    return i
            return None

    def extract_number(s):
        match = re.search(r"Method's LoC: (\d+)", s)
        if match:
            return int(match.group(1))
        return None

    def _clean_list(self, lst):
        return [x for x in lst if x]
    
    def write_in_code_docs(self):
        for file_path, classes in self.responses.items():
            # Überspringen, wenn der Dateipfad auf eine leere Datei oder globale Einstellungen verweist
            if isinstance(classes, str) or 'global' in classes[0]:
                continue

            # Dateiinhalt vor Änderungen lesen
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Durch jede Klasse im Dateipfad iterieren
            for class_dict in classes:
                if isinstance(class_dict, str):
                    continue
                for class_name, methods in class_dict.items():
                    # Durch jede Methode in der Klasse iterieren
                    for method_name, method_info in methods.items():
                        # Zeilennummer und Dokumentation extrahieren
                        try:
                            line_number = int(method_info[0].split(': ')[1]) - 1  # 0-basierter Index. Daher wird bei LoC + 1 geschrieben.
                            docstring = method_info[1]
                        except ValueError:
                            print(f"Error: Invalid line number format in method_info: {method_info[0]}")
                            print(f"Error: Class Name: {class_name}")
                            print(f"Error: Method Name: {method_name}")
                            continue

                        # Dokumentation an der spezifizierten Zeilennummer einfügen
                        lines.insert(line_number, docstring + '\n')

            # Dateiinhalt nach Änderungen schreiben
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
