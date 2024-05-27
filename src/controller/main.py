import sys
import io
from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever
from pprint import pprint

"""
1. Format vom Dictionary anpassen. 
2. Prompt für Klassendokumentation erstellen
3. Prompt for Module based documentation; least priority; best practices prüfen
"""

def main():
    # Allow prinint utf-8 characters in console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")

    #TODO Change local path to your target repository
    fr = FileRetriever("../targets/IIRA")
    py_file_paths = fr.file_mapping["py"]

    print("Python files found: ")
    print(str(py_file_paths))
    dAgent = DocsAgent(
        config.WORKING_DIR,
        py_file_paths[:3],
        config.prompts,
        LLModel(config, cache)
    )

    print("Documenting methods and functions ...")
    dAgent.make_in_code_docs()
    print()
    print("Methods loc:")
    print(dAgent.methods_loc)
    print()
    print("Responses:")
    print(dAgent.responses)
    print()

    
 


if __name__ == "__main__":
    main()