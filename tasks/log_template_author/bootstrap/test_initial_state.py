import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), "Jujutsu repository not initialized in the project directory."

def test_jj_author_configured():
    try:
        output = subprocess.check_output(["jj", "config", "get", "user.name"], cwd=PROJECT_DIR, text=True)
        assert "Test User" in output, "jj user.name is not configured correctly."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to get jj user.name config.")
