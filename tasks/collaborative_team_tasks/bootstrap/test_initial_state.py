import os
import shutil
import subprocess
import pytest

def test_wasp_cli_available():
    assert shutil.which("wasp") is not None, "wasp CLI not found in PATH."

def test_node_available():
    assert shutil.which("node") is not None, "Node.js not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm not found in PATH."

def test_home_directory_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
