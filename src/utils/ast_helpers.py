import ast

class ClassFunctionVisitor(ast.NodeVisitor):
    def __init__(self, data, indent_levels):
        self.current_class = None  # Speichert den aktuellen Klassenkontext
        self.data = data  # Enthält u.A. die docstrings. Ausschnit von self.responses aus docsAgent Klasse
        self.indent_levels = indent_levels  # Objekt der Klasse IndentLevelVisitor

    def visit_ClassDef(self, node):
        self.current_class = node.name  # Aktualisiert den Klassenkontext
        val = self._make_docstring(self.current_class, node.name)

        # Überprüfen, ob die Klasse bereits einen Docstring hat
        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            docstring = ast.Expr(value=ast.Constant(value=val))
            node.body.insert(0, docstring)

        self.generic_visit(node)  # Besucht rekursiv die Kinder des Knotens
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            print(f"Klasse: {self.current_class}, Funktion: {node.name}")
            val = self._make_docstring(self.current_class, node.name)
        else:
            print(f"Top-Level Funktion: {node.name}")
            val = self._make_docstring("global", node.name)

        # Überprüfen, ob die Funktion bereits einen Docstring hat
        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            # Erstellen des Docstring-Knotens
            docstring = ast.Expr(value=ast.Constant(value=val))
            
            # Hinzufügen des Docstring-Knotens am Anfang der body-Liste der Funktion
            node.body.insert(0, docstring)

        self.generic_visit(node)  # Besucht rekursiv die Kinder des Knotens
    
    def _make_docstring(self, class_name, method_name):
        #TODO Auch für Klassen implementieren
        raw_docstring = self._extract_docstring(class_name, method_name)
        indent_level = self.indent_levels.get_indent_level(method_name)
        return self._adjust_docstring_indentation(indent_level, raw_docstring)

    def _extract_docstring(self, class_name, method_name):
        for dic in self.data:
            if class_name in dic:
                docstring = dic[class_name][method_name]
                if docstring.startswith('```python') and docstring.endswith('```'):
                    docstring = docstring[9:-3]
                if docstring.startswith('"""') and docstring.endswith('"""'):
                    # ast fügt """""" hinzu, daher entfernen
                    docstring = docstring[3:-3]
                return docstring

    def _adjust_docstring_indentation(self, indent_level, docstring):
        # Fügt Leerzeichen für jede Zeile im Docstring hinzu, basierend auf dem Einrückungslevel
        indentation = " " * (indent_level + 4)  # +4 für die Standard-Einrückung in Python
        docstring_lines = docstring.split("\n")
                
        if docstring_lines[0].strip() != "":
            # So fängt der Docstring immer in der nächsten Zeile an, nicht direkt nach """
            docstring_lines.insert(0, "")

        # Überprüfen und anpassen der Einrückung für jede Zeile, außer der ersten und letzten, wenn sie nur """ enthalten
        adjusted_lines = [docstring_lines[0]] + [indentation + line if line.strip() else line for line in docstring_lines[1:-1]] + [docstring_lines[-1]]

        # Überprüfen, ob die letzte Zeile nur aus "" besteht, und entsprechend einrücken
        if adjusted_lines[-1].strip() == "":
            adjusted_lines[-1] = indentation
        
        adjusted_docstring = "\n".join(adjusted_lines)
        return adjusted_docstring    

class IndentLevelVisitor(ast.NodeVisitor):
    def __init__(self):
        self.indent_levels = {}  # Speichert Einrückungslevel für node.names

    def visit(self, node):
        # Prüfe, ob der Knoten ein name Attribut hat
        if hasattr(node, "name") and hasattr(node, "col_offset"):
            # Aktualisiere das Einrückungslevel für diesen node.name
            self.indent_levels[node.name] = node.col_offset
        # Führe die Standard-Verarbeitung fort, um alle Knoten zu besuchen
        super().generic_visit(node)

    def get_indent_level(self, name):
        # Gibt das Einrückungslevel für den gegebenen node.name zurück
        return self.indent_levels.get(name, None)