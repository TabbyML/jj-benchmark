import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_config_file_exists():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

def test_app_file_exists():
    app_path = os.path.join(PROJECT_DIR, "app.py")
    assert os.path.isfile(app_path), f"App file {app_path} does not exist."

def test_initial_config_state():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    with open(config_path) as f:
        content = f.read()
    assert "port=9090" in content, "Expected initial config.txt to have port=9090."

def test_initial_app_state():
    app_path = os.path.join(PROJECT_DIR, "app.py")
    with open(app_path) as f:
        content = f.read()
    assert "Hello World - v2" in content, "Expected initial app.py to have Hello World - v2."

def test_jj_repo_initialized():
    result = subprocess.run(["jj", "root"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, "Jujutsu repository is not initialized in the project directory."
