import json
from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever

def main():
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")

    #TODO Change local path to your target repository
    fr = FileRetriever("..")
    py_file_paths = fr.file_mapping["py"]

    print("Python files found: ")
    print(str(py_file_paths))
    dAgent = DocsAgent(
        config.WORKING_DIR,
        py_file_paths,
        config.prompts,
        LLModel(config, cache)
    )

    print("Processing file ... " + py_file_paths[0])
    #tmp_write_file(
    #    "./generated_docs/partially_documented_cod3.py",
    #    partially_documented_code
    #    )
    print("Extracting methods ...")
    extracted_methods = dAgent._extract_methods(py_file_paths[0])
    print(extracted_methods)
    #TODO check functionality 1 by 1; formatting content is sometimes provided
    # in the response that should not be there. Dictionary in self.responses
    # is also not properly formatted (keys are weird).

    """
    print("Documenting methods and functions ...")
    dAgent._document_methods(
        py_file_paths[0],
        method_names=extracted_methods
        )
    partially_documented_code = dAgent.responses
    print(partially_documented_code)

    print("Writing files ...")
    print(partially_documented_code)
    json_string = str(partially_documented_code).replace("'", '"').replace('\\\\', '\\')
    dict_data = json.loads(json_string)
    with open('data.json', 'w') as f:
        json.dump(dict_data, f)
    """


if __name__ == "__main__":
    main()