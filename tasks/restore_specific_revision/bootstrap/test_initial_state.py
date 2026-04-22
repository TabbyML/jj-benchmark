import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_config_file_exists():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_initial_config_content():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    with open(config_path) as f:
        content = f.read().strip()
    assert content == "version=3", f"Expected initial config.txt to contain 'version=3', got '{content}'."
