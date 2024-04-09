from agents.docs_agent import DocsAgent
from config import load_config
from models import LLModel
from utils.cache import DisabledCache, SimpleCache

def main():
    config = load_config()

    cache = SimpleCache() if config.CACHE_ENABLED else DisabledCache()
    dAgent = DocsAgent(
        config.WORKING_DIR,
        config.prompts,
        LLModel(config, cache)
    )

if __name__ == "__main__":
    main()