import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_is_jj_repo():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"{PROJECT_DIR} is not a jj repository."

def test_gitignore_exists_and_content():
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), f".gitignore file {gitignore_path} does not exist."
    with open(gitignore_path) as f:
        content = f.read()
    assert "*.log" in content, "Expected .gitignore to contain '*.log'."

def test_app_log_exists():
    app_log_path = os.path.join(PROJECT_DIR, "app.log")
    assert os.path.isfile(app_log_path), f"app.log file {app_log_path} does not exist."

def test_app_log_is_untracked():
    result = subprocess.run(
        ["jj", "file", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "app.log" not in result.stdout, "Expected app.log to be untracked initially."
