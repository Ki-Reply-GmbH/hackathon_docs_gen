import argparse
import sys
import io
import json
from src.agents.docs_agent import DocsAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.utils.observer import Observer
from src.controller.file_retriever import FileRetriever

def main():
    parser = argparse.ArgumentParser(description="Generate documentation for Python files in a specified directory.")
    parser.add_argument("--input-path", required=True, help="Path to the software project to be documented.")
    parser.add_argument("--output-path", required=True, help="Path where the generated documentation will be saved.")
    parser.add_argument("--create", action="append", choices=["in-code", "system-context", "class", "*"], 
                        help="Determines which actions the software will do. Options: 'in-code' for in-code documentation, 'system-context' for a system context diagram, 'class' for a class diagram, '*' for everything.")
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    create_items = args.create if args.create else []  # Falls keine --create Argumente angegeben wurden, wird eine leere Liste verwendet

    project_name = input_path.split("/")[-1] # TODO verbessern
    print(f"Input Path: {input_path}")
    print(f"Output Path: {output_path}")
    print(f"Create Items: {create_items}")
    print(f"Create Items: {project_name}")
    # Allow prinint utf-8 characters in console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    config = load_config()

    cache = SimpleCache(tmp_path="./.tmp")

    agents_observer = Observer()

    dAgent = DocsAgent(
        config.prompts,
        LLModel(config, cache),
        input_path
    )
    dAgent.attach(agents_observer)
    if "in-code" in create_items or "*" in create_items:
        print("Creating in code documentation...")
        dAgent.make_in_code_docs()
        dAgent.write_in_code_docs()

    if "system-context" in create_items or "*" in create_items:
        print("Creating system context diagram...")
        plantuml = dAgent.make_system_context_diagram()
        with open(output_path + f"/{project_name}_system_context_diagram.puml", "w", encoding="utf-8") as file:
            file.write(plantuml)
    

    if "class" in create_items or "*" in create_items:
        print("Creating class diagram...")
        plantuml = dAgent.make_class_diagram()
        with open(output_path + f"/{project_name}_class_diagram.puml", "w", encoding="utf-8") as file:
            file.write(plantuml)


def test():
    path = "C:\\Users\\t.kubera\\dev\\hackathon\\hackathon_code_gen\\resources\\simple-sw-projects-for-testing\\project"

    #for j in range(1, 3):
    #    print("Iteration " + str(j) + " ...")
    j = 3
    for i in range(1,5):
        input_path = path + str(i)
        project_name = input_path.split("\\")[-1]
        config = load_config()

        cache = DisabledCache(tmp_path="./.tmp")

        dAgent = DocsAgent(
            config.prompts,
            LLModel(config, cache),
            input_path
        )
        print("Creating system context diagram for " + input_path + " ...")
        plantuml = dAgent.make_system_context_diagram()
        with open(input_path + f"/{project_name}_system_context_diagram{j}.puml", "w", encoding="utf-8") as file:
            file.write(plantuml)

        print("Creating class diagram for " + input_path + " ...")
        plantuml = dAgent.make_class_diagram()
        with open(input_path + f"/{project_name}_class_diagram{j}.puml", "w", encoding="utf-8") as file:
            file.write(plantuml)

if __name__ == "__main__":
    test()