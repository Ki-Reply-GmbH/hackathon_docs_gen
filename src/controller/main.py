#TODO Refactor file to follow clean code principles
import argparse
import sys
import io
import json
from src.agents.docs_agent import DocsAgent, InCodeAgent, SystemContextAgent, ClassAgent, SWQAgent
from src.config import load_config
from src.models import LLModel
from src.utils.cache import DisabledCache, SimpleCache
from src.utils.observer import AgentObserver
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

    agent_observer = AgentObserver()

    dAgent = DocsAgent(
        config.prompts,
        LLModel(config, cache),
        input_path
    )
    dAgent.attach(agent_observer)
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
    path = "C:\\Users\\t.kubera\\dev\\documentation-generation\\resources\\IIRA"
    agent_observer = AgentObserver()

    config = load_config()

    cache = DisabledCache(tmp_path="./.tmp")

    agent = SWQAgent(
        config.prompts,
        LLModel(config, cache),
        path
    )
    agent.attach(agent_observer)
    agent.make_swq_docs()


    agent_observer.calc_total_costs()

    try:
        serializable_updates = {k: v for k, v in agent_observer.updates.items()}
        with open("./.tmp/observer.json", "w") as file:
            json.dump(serializable_updates, file, indent=4)
        
        with open("./.tmp/swq_output.json", "w") as file:
            json.dump(agent.sqw_responses, file, indent=4)
    except TypeError as e:
        with open("./.tmp/observer.txt", "w") as file:
            file.write(str(agent_observer.updates))
        with open("./.tmp/swq_output.txt", "w") as file:
            file.write(str(agent.sqw_responses))

if __name__ == "__main__":
    test()