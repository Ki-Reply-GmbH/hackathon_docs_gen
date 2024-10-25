# Author: Daniel Hummel (d.hummel@reply.de)
# Company: Ki Reply GmbH
# Version: 1.0
#
# License: This program is licensed under the GNU General Public License version 3.
# The full license can be found in the LICENSE file or at https://www.gnu.org/licenses/gpl-3.0.en.html.
#
from app.hackathon_docs_gen.src.utils.observer import Observable


class Agent(Observable):
    """
    Base class for all agents.

    Attributes:
        _agent_id (str): The id of the agent.
        _name (str): The name of the agent.
        _description (str): The description of the agent.
        _agent_config: The configuration for the agent.
    """

    def __init__(self, agent_id: str, name: str, description: str, agent_config):
        super().__init__()
        self._agent_id = agent_id
        self._name = name
        self._description = description
        self._agent_config = agent_config

    from typing import List
    
    def determine_tasks(self, objective: str, context) -> List:
        """
        Determines the tasks to be executed.

        :param objective: The objective to determine the tasks for.
        :type objective: str
        :param context: The context to determine the tasks for.
        :type context: dict
        :return: The tasks to be executed.
        :rtype: list
        :raises NotImplementedError: If the determine_tasks function is not implemented.
        """
        raise NotImplementedError("determine_tasks function is not implemented")

    def execute(self, task, context):
        """
        Executes the given task with the provided context.

        :param task: The task to execute.
        :type task: Task
        :param context: The context to execute the task in.
        :type context: dict
        :raises NotImplementedError: If the execute function is not implemented.
        """
        raise NotImplementedError("execute function is not implemented")

    def get_id(self):
        """
        Returns the id of the agent.

        :return: The id of the agent.
        :rtype: str
        """
        return self._agent_id

    def get_name(self):
        """
        Returns the name of the agent.

        :return: The name of the agent.
        :rtype: str
        """
        return self._name

    def get_description(self):
        """
        Returns the description of the agent.

        :return: The description of the agent.
        :rtype: str
        """
        return self._description