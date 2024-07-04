import tkinter as tk
from tkinter import ttk, filedialog

class DocumentationGUI:
    def __init__(self, root):
        self.root = root
        root.title("Software Project Documentation Tool")
        root.geometry("600x400")

        # Styling
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TCheckbutton', font=('Arial', 12))

        # Project Path
        ttk.Label(root, text="Project Path:").pack(pady=(20, 0))
        self.project_path_entry = ttk.Entry(root, width=50)
        self.project_path_entry.pack(pady=(0, 20))
        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_project_path)
        self.browse_button.pack(pady=(0, 20))

        # Options
        ttk.Label(root, text="Select Documentation Options:").pack()
        self.docstring_var = tk.BooleanVar()
        self.system_context_var = tk.BooleanVar()
        self.class_diagram_var = tk.BooleanVar()

        self.docstring_cb = ttk.Checkbutton(root, text="In Code Documentation with Docstrings", variable=self.docstring_var)
        self.docstring_cb.pack()
        self.system_context_cb = ttk.Checkbutton(root, text="System Context Diagram", variable=self.system_context_var)
        self.system_context_cb.pack()
        self.class_diagram_cb = ttk.Checkbutton(root, text="Class Diagram", variable=self.class_diagram_var)
        self.class_diagram_cb.pack()

        # Save Path
        ttk.Label(root, text="Save Diagrams To:").pack(pady=(20, 0))
        self.save_path_entry = ttk.Entry(root, width=50)
        self.save_path_entry.pack(pady=(0, 20))
        self.save_browse_button = ttk.Button(root, text="Browse", command=self.browse_save_path)
        self.save_browse_button.pack(pady=(0, 20))

        # Generate Button
        self.generate_button = ttk.Button(root, text="Generate Documentation", command=self.generate_documentation)
        self.generate_button.pack(pady=(20, 0))

    def browse_project_path(self):
        path = filedialog.askdirectory()
        self.project_path_entry.delete(0, tk.END)
        self.project_path_entry.insert(0, path)

    def browse_save_path(self):
        path = filedialog.askdirectory()
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, path)

    def generate_documentation(self):
        project_path = self.project_path_entry.get()
        save_path = self.save_path_entry.get()
        docstring = self.docstring_var.get()
        system_context = self.system_context_var.get()
        class_diagram = self.class_diagram_var.get()

        # Here you would add the logic to generate the documentation based on the selected options.
        # This could involve parsing the project files for docstrings, generating diagrams, etc.
        print(f"Project Path: {project_path}")
        print(f"Save Path: {save_path}")
        print(f"Docstrings: {docstring}, System Context Diagram: {system_context}, Class Diagram: {class_diagram}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentationGUI(root)
    root.mainloop()