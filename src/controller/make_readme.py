import sys
import io
import json
from app.hackathon_docs_gen.src.agents.docs_agent import DocsAgent
from app.hackathon_docs_gen.src.config import load_config
from app.hackathon_docs_gen.src.models import LLModel
from app.hackathon_docs_gen.src.utils.cache import DisabledCache, SimpleCache


def make_readme():
    # Allow prinint utf-8 characters in console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    config = load_config()
    cache = SimpleCache(tmp_path="./.tmp")
    with open('responses.json', 'r') as f:
        responses = json.load(f)

    dAgent = DocsAgent(
        config.WORKING_DIR,
        [],
        config.prompts,
        LLModel(config, cache)
    )

    dAgent.responses = rename_keys(responses)
    readme = dAgent.make_readme()

    with open('README.md', 'w') as file:
        # Markdown-Code in die Datei schreiben
        file.write(readme)



def shorten_filepath(filepath):
    # Find the index of "IIRA" in the filepath
    iira_index = filepath.find("IIRA")
    # Check if "IIRA" is found
    if iira_index != -1:
        # Return the filepath from "IIRA" onwards
        return filepath[iira_index:]
    else:
        # "IIRA" not found, return the original filepath or handle as needed
        return filepath


def rename_keys(dict):
    key_mapping = {}
    for key in dict:
        key_mapping[key] = shorten_filepath(key)
    # Schlüsselnamen ändern
    for old_key, new_key in key_mapping.items():
        if old_key in dict:
            dict[new_key] = dict.pop(old_key)

    return dict

make_readme()