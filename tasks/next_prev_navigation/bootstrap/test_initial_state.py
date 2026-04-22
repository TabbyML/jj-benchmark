import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_state_history():
    result = subprocess.run(
        ["jj", "log", "-T", "description", "--no-graph"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "commit D" in result.stdout, "Expected 'commit D' in history."
    assert "commit C" in result.stdout, "Expected 'commit C' in history."
    assert "commit B" in result.stdout, "Expected 'commit B' in history."
    assert "commit A" in result.stdout, "Expected 'commit A' in history."

def test_initial_state_working_copy_parent():
    result = subprocess.run(
        ["jj", "log", "-r", "@-", "-T", "description", "--no-graph"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "commit D" in result.stdout, "Expected the working copy to be a child of 'commit D'."
