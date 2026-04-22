import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_commit_description():
    result = subprocess.run(
        ["jj", "log", "-r", "@-", "--no-graph", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "Add feature A and feature B", \
        f"Expected initial commit description to be 'Add feature A and feature B', got '{result.stdout.strip()}'."

def test_initial_commit_files():
    result = subprocess.run(
        ["jj", "diff", "-s", "-r", "@-"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert "feature_a.py" in result.stdout, "Expected feature_a.py in the initial commit."
    assert "feature_b.py" in result.stdout, "Expected feature_b.py in the initial commit."
