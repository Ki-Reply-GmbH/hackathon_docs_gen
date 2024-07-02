You receive a Python dictionary that describes the functionality of a software \
project. The project was mainly developed in the language {programming_language}.
The keys in the dictionary consist of file paths, with the root directory \
being the root directory of the project. This allows you to implicitly learn \
the package structure of the software project from the keys.
The values ​​are lists in which the classes that appear in the respective file \
are stored. You will also find the entry "global" in the lists, which \
describes the logic of global functions in the file. Both are stored as a \
nested dictionary. In these nested dictionaries you can finally find textual \
descriptions of the functions that are in the respective class or that have \
been defined globally.

--- Minimalist example ---
####
{{
    "project_root_dir/main.py": [
        {{
            "Main": {{
                "__init__": "This docstring is documenting the __init__ method in the Main function.",
                "Main": "This docstring is documenting the Main class itself."
            }}
        }},
        {{
            "global": {{
                "global_function": "This docstring is documenting the global function global_function."
            }}
        }}
    ],
    "project_root_dir/__init__.py": [
        "This file is empty."
    ],
}}
####

--- Data sructure containing project information ---
####
{project_information}
####

Your task is to create a readme file (in markdown code) for the software \
project using such a data structure.
Here is a sample readme file. Learn the pattern and use it as a template. Fill \
the template with relevant information you learned from the data structure.
If you are missing information to complete certain sections in the template, \
leave the sections out.

--- Readme sample ---
####
TODO: Write me
####

To summarize your tasks again:
1. Learn the semantics of the project using the data structure.
2. Learn the patterns used in the Readme template.
3. Create a readme file using what you learned in 1. and 2.
4. Return the Markdown code of the readme file and nothing else. In \
particular, do not return any formatting information or other metadata.
