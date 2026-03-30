import os
import shutil
import pytest

def test_wasp_cli_available():
    assert shutil.which("wasp") is not None, "Wasp CLI not found in PATH."

def test_node_available():
    assert shutil.which("node") is not None, "Node.js not found."

def test_project_dir_not_exists():
    project_dir = "/home/user/todo-app"
    assert not os.path.exists(project_dir), f"Project directory {project_dir} should not exist before the task starts."
