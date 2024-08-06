"""
This module provides the Config class which is used to manage configuration 
settings.

The Config class loads configuration settings from environment variables and 
provides methods to access these settings.
"""

import logging
import os
import sys
import tempfile
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "ERROR"))


@dataclass
class PromptConfig:
    """
    This class is used to manage the prompts used in the application.

    Attributes:
        log_prompt (str): The prompt used for logging.
        repair_prompt (str): The prompt used for repairing.
        commit_prompt (str): The prompt used for committing.
    """
    def __init__(self):
        pass

    def _read_file_content(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()

    def get_functional_suitability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "functional_suitability_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_maintainability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "maintainability_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_performance_efficiency_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "performance_efficiency_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_portability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "portability_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_reliability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "reliability_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_security_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "security_prompt.txt"
            )
        return self._read_file_content(prompt_path)
    
    def get_usability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "usability_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_observability_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "observability_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_class_plantuml_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "class_plantuml_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_system_context_plantuml_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "system_context_plantuml_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_system_context_diagram_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "system_context_diagram_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_system_context_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "system_context_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_readme_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "readme_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_document_class_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "document_class_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_document_method_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "document_method_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_exract_methods_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "extract_methods_prompt.txt"
            )
        return self._read_file_content(prompt_path)

    def get_exract_classes_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(
            base_dir, "prompts", "docs_agent",
            "extract_classes_prompt.txt"
            )
        return self._read_file_content(prompt_path)


@dataclass
class Config:
    """
    The Config class is responsible for managing configuration settings.

    This class loads configuration settings from environment variables and 
    provides methods to access these settings.

    Attributes:
        OPENAI_API_KEY (str): The API key for OpenAI.
        LLM_MODEL_NAME (str): The name of the language model to use.
        LLM_TEMPERATURE (float): The temperature setting for the language model.
    """
    _instance = None

    def __init__(self):
        """
        Initializes a Config and loads settings from environment variables.
        """
        ####################
        # Cache CONFIG
        ####################
        self.USE_CACHE = self._read_bool_value("USE_CACHE", "True")

        ####################
        # AGI CONFIG
        ####################
        self.prompts = PromptConfig()
        self.AGI_VERBOSE = True
        self.LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-4o-turbo")
        self.LLM_TEMPERATURE = os.environ.get("LLM_TEMPERATURE", 0.0)
        self.LLM_MAX_LENGTH = os.environ.get("LLM_MAX_LENGTH", 4096)
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

        ####################
        # WORKING DIR CONFIG
        ####################

        if os.environ.get("WORKING_DIR"):
            self.WORKING_DIR = os.environ.get("WORKING_DIR")
        else:
            temp_dir = os.path.join(tempfile.gettempdir(), "cdaas-merge")
            os.makedirs(temp_dir, exist_ok=True)
            self.WORKING_DIR = temp_dir
        LOGGER.info("Working directory: %s", self.WORKING_DIR)

    def _read_bool_value(self, env_name, default_value: bool) -> bool:
        """
        Read a boolean value from an environment variable.
        Args:
            env_value (str): The environment variable value.
        Returns:
            bool: The boolean value.
        """
        env_value = os.environ.get(env_name, default_value)
        if env_value is None:
            return default_value

        if isinstance(env_value, bool):
            return env_value
        return env_value.lower() in ["true", "1"]

    @classmethod
    def instance(cls):
        """Create a singleton instance of the Config class.
        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            logging.info("Creating new Config instance")
            cls._instance = Config()
            # cls._instance.validate_github_user()
            # cls._instance.validate_llm_setup()
            # Put any initialization here.
        return cls._instance

    def validate_llm_setup(self):
        """Validate the LLM setup.
        This function checks if all required environment variables are set.

        Raises:
            SystemExit: If any required environment variable is not set.
        """
        if not self.OPENAI_API_BASE:
            sys.stderr.write(
                "ERROR: OPENAI_API_BASE is not set. Please check your environment variables."
            )
            sys.exit(3)

        if not self.OPENAI_DEPLOYMENT_NAME:
            sys.stderr.write(
                "ERROR: OPENAI_DEPLOYMENT_NAME is not set. Please check your environment variables."
            )
            sys.exit(3)

        if not self.OPENAI_API_KEY:
            sys.stderr.write(
                "ERROR: OPENAI_API_KEY is not set. Please check your environment variables."
            )
            sys.exit(3)

        if not self.OPENAI_API_TYPE:
            sys.stderr.write(
                "ERROR: OPENAI_API_TYPE is not set. Please check your environment variables."
            )
            sys.exit(3)


def load_config():
    return Config.instance()
