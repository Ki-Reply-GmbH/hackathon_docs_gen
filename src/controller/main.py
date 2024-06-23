import argparse
import sys
import io
from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever

"""
1. Format vom Dictionary anpassen. 
2. Prompt für Klassendokumentation erstellen
3. Prompt for Module based documentation; least priority; best practices prüfen
"""

def main():
    parser = argparse.ArgumentParser(description="Generate documentation for Python files in a specified directory.")
    parser.add_argument("--target-path", required=True, help="Path to the target repository containing Python files.")
    args = parser.parse_args()
    target_path = args.target_path


    # Allow prinint utf-8 characters in console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")

    fr = FileRetriever(target_path)
    py_file_paths = fr.file_mapping["py"]

    print("Python files found: ")
    print(str(py_file_paths))
    dAgent = DocsAgent(
        config.WORKING_DIR,
        py_file_paths,
        config.prompts,
        LLModel(config, cache)
    )
    print("Documenting methods and functions ...")
    dAgent.make_in_code_docs()
    print()
    print("Responses for files:")
    keys = [key for key in dAgent.responses.keys()]
    print(keys)
    print()
    print("Responses for methods and functions:")
    print(dAgent.responses)

    print("Writing in code docs ...")
    dAgent.write_in_code_docs()

 


if __name__ == "__main__":
    main()