import io
import sys
import json
from unittest.mock import patch, mock_open
import pytest
from app.hackathon_docs_gen.src.controller.make_readme import make_readme
from app.hackathon_docs_gen.src.agents.docs_agent import DocsAgent
from src.models import LLModel
from src.config import load_config
from src.utils.cache import SimpleCache

@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch('sys.stdout', new_callable=io.StringIO)
    mocker.patch('src.config.load_config', return_value=mocker.MagicMock())
    mocker.patch('src.utils.cache.SimpleCache', return_value=mocker.MagicMock())
    mocker.patch('json.load', return_value={'key': 'value'})
    mocker.patch('app.hackathon_docs_gen.src.agents.docs_agent.DocsAgent', return_value=mocker.MagicMock())
    mocker.patch('src.models.LLModel', return_value=mocker.MagicMock())
    mocker.patch('builtins.open', new_callable=mock_open, read_data='data')

def test_make_readme_success(mock_dependencies):
    # Given: Setup the environment and dependencies
    config_mock = load_config()
    cache_mock = SimpleCache(tmp_path='./.tmp')
    docs_agent_mock = DocsAgent(config_mock.WORKING_DIR, [], config_mock.prompts, LLModel(config_mock, cache_mock))

    # When: Calling the make_readme function
    make_readme()

    # Then: Check if README.md file is written correctly
    open.assert_called_with('README.md', 'w')
    handle = open()
    handle.write.assert_called_once_with(docs_agent_mock.make_readme())

def test_make_readme_exception_handling(mock_dependencies):
    # Given: Setup the environment and dependencies with an exception in json loading
    json.load.side_effect = json.JSONDecodeError('Expecting value', 'doc', 0)

    # When & Then: Calling the make_readme function should handle JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        make_readme()