import sys
import io
from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever
from pprint import pprint

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
        py_file_paths[:1],
        config.prompts,
        LLModel(config, cache)
    )

    #print("Processing file ... " + py_file_paths[0])
    #tmp_write_file(
    #    "./generated_docs/partially_documented_cod3.py",
    #    partially_documented_code
    #    )
    print("Extracting methods ...")
    extracted_methods = dAgent._extract_methods(py_file_paths[0])
    print("Extracted methods: ")
    print(extracted_methods)
    #TODO check functionality 1 by 1; formatting content is sometimes provided
    # in the response that should not be there. Dictionary in self.responses
    # is also not properly formatted (keys are weird).

    print("Documenting methods and functions ...")
    """
    dAgent._document_methods(
        py_file_paths[0],
        )
    """
    dAgent.make_in_code_docs()
    print()
    print(dAgent.methods_loc)
    print()
    print(dAgent.responses)
    print()
    #print(type(dAgent.responses["C:\\Users\\t.kubera\\dev\\hackathon\\targets\\IIRA\\app.py"]["show_frame"]))
    #print(dAgent.responses["C:\\Users\\t.kubera\\dev\\hackathon\\targets\\IIRA\\app.py"]["show_frame"])


if __name__ == "__main__":
    main()