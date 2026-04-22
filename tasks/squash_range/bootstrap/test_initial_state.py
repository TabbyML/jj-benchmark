import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_commits_exist():
    result = subprocess.run(
        ["jj", "log", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout
    assert "feat: initial structure" in output, "Target commit not found."
    assert "fix: syntax error" in output, "First fix commit not found."
    assert "fix: logic error" in output, "Second fix commit not found."
    assert "feat: add more stuff" in output, "Descendant commit not found."
