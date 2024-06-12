import ast

class ClassFunctionVisitor(ast.NodeVisitor):
    def __init__(self, data):
        self.current_class = None  # Speichert den aktuellen Klassenkontext
        self.data = data  # Enthält u.A. die docstrings. Ausschnit von self.responses aus docsAgent Klasse

    def visit_ClassDef(self, node):
        self.current_class = node.name  # Aktualisiert den Klassenkontext

        # Überprüfen, ob die Klasse bereits einen Docstring hat
        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            docstring = ast.Expr(value=ast.Constant(value=f'Dies ist die Dokumentation für die Klasse {node.name}.'))
            node.body.insert(0, docstring)

        self.generic_visit(node)  # Besucht rekursiv die Kinder des Knotens
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            print(f"Klasse: {self.current_class}, Funktion: {node.name}")
            val = self._extract_docstring(self.current_class, node.name)
        else:
            print(f"Top-Level Funktion: {node.name}")
            val = self._extract_docstring("global", node.name)

        # Überprüfen, ob die Funktion bereits einen Docstring hat
        if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            # Erstellen des Docstring-Knotens
            docstring = ast.Expr(value=ast.Constant(value=val))
            
            # Hinzufügen des Docstring-Knotens am Anfang der body-Liste der Funktion
            node.body.insert(0, docstring)

        self.generic_visit(node)  # Besucht rekursiv die Kinder des Knotens
    
    def _extract_docstring(self, class_name, method_name):
        for dic in self.data:
            if class_name in dic:
                return dic[class_name][method_name]
            

class IndentLevelVisitor(ast.NodeVisitor):
    def __init__(self):
        self.indent_levels = {}  # Speichert Einrückungslevel für node.names

    def visit(self, node):
        # Prüfe, ob der Knoten ein name Attribut hat
        if hasattr(node, 'name') and hasattr(node, 'col_offset'):
            # Aktualisiere das Einrückungslevel für diesen node.name
            self.indent_levels[node.name] = node.col_offset
        # Führe die Standard-Verarbeitung fort, um alle Knoten zu besuchen
        super().generic_visit(node)

    def get_indent_level(self, name):
        # Gibt das Einrückungslevel für den gegebenen node.name zurück
        return self.indent_levels.get(name, None)