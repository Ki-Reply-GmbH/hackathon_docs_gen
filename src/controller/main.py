from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever

def main():
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")

    #TODO Change local path to your target repository
    fr = FileRetriever("../targets/IIRA")
    py_file_paths = fr.file_mapping["py"]

    print("Python files found: ")
    print(str(py_file_paths))
    dAgent = DocsAgent(
        config.WORKING_DIR,
        py_file_paths,
        config.prompts,
        LLModel(config, cache)
    )

    partially_documented_code = dAgent._document_file(py_file_paths[0])
    tmp_write_file("partially_documented_code.py", partially_documented_code)

def tmp_write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

if __name__ == "__main__":
    main()