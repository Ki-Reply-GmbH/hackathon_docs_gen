from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.controller.file_retriever import FileRetriever

def main():
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")
    dAgent = DocsAgent(
        config.WORKING_DIR,
        config.prompts,
        LLModel(config, cache)
    )

    #TODO Change local path to your target repository
    fr = FileRetriever("../targets/IIRA")
    print(str(fr))

if __name__ == "__main__":
    main()