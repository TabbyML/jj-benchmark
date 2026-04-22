import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_commits():
    # Verify that the initial commits are present
    result = subprocess.run(
        ["jj", "log", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "add feature A" in output, "Commit 'add feature A' not found."
    assert "add feature B" in output, "Commit 'add feature B' not found."
    assert "add feature C" in output, "Commit 'add feature C' not found."

def test_app_py_exists():
    app_py_path = os.path.join(PROJECT_DIR, "app.py")
    assert os.path.isfile(app_py_path), f"{app_py_path} does not exist."
