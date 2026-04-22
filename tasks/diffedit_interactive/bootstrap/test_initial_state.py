import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"jj repository not initialized in {PROJECT_DIR}."

def test_initial_commit_content():
    # Verify that 'app.py' exists and contains both foo() and bar() in the commit 'add features'
    result = subprocess.run(
        ["jj", "show", "-r", "@-"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Could not find parent commit."
    assert "add features" in result.stdout, "Parent commit is not 'add features'."
    assert "def foo():" in result.stdout, "Initial commit does not contain foo()."
    assert "def bar():" in result.stdout, "Initial commit does not contain bar()."
