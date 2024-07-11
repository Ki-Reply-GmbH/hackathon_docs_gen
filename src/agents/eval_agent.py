"""
Dependencies: Java and PlantUML being installed.
"""
import os
import subprocess
from src.utils.observer import Observable
from src.config import PromptConfig
from src.models import LLModel

class EvalAgent(Observable):
    def __init__(
            self,
            prompts: PromptConfig,
            model: LLModel,
            resources: dict[str, list[str]],
            num_episodes: int = 3
            ):
        #self._system_context_diagrams = resources["system_context_diagrams"]
        #self._class_diagrams = resources["class_diagrams"]
        self._num_episodes = num_episodes

        self.improved_system_context_diagram = None
        self.improved_class_diagram = None

    def _evaluate_system_context_diagram(self):
        pass

    def _evaluate_class_diagram(self):
        pass

    def _improve_system_context_diagram(self):
        pass

    def _improve_class_diagram(self):
        pass

    def _validate_puml(self, puml_string: str):
        plantuml_jar_path = os.getenv("PLANTUML_JAR")
        if not plantuml_jar_path:
            raise EnvironmentError("PLANTUML_JAR environment variable not set.")
        
        command = ["java", "-jar", plantuml_jar_path, "-pipe", "-checksyntax"]

        try:
            result = subprocess.run(
                command,
                input=puml_string,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
                )
            
            result_str = f"Validation results: {result.stdout}"
        except subprocess.CalledProcessError as e:
            result_str = f"Error checking PUML string: {e.stderr}"
        
        return result_str 

if __name__ == "__main__":
    plantuml_str0 = """
    @startuml
    ' System Context Diagram for IIRA

    ' Define the system (Process Name) as the central element
    rectangle "IIRA" as IIRA #pink

    ' Define the external entities
    actor "Users" as Users
    database "Internal Database" as Database
    file "Files" as Files
    actor "Web Browser" as WebBrowser

    ' Define the primary data flows
    Users --> IIRA : Input Data (file selection, profile information, analysis parameters)
    IIRA --> Users : Output Data (analysis results, error messages, help information)
    IIRA --> Database : Profile Management (create, update, retrieve profiles)
    IIRA --> Files : File Interactions (import data, export results)
    IIRA --> WebBrowser : Open external URLs for help information

    @enduml

    """   
    eval_agent = EvalAgent(None, None, None)
    result_str = eval_agent._validate_puml(plantuml_str0)
    print(result_str)