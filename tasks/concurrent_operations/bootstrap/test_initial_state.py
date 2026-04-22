import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj log."
    assert "Feature X - variant 1" in result.stdout, "Initial commit 'Feature X - variant 1' not found in jj log."

def test_operation_log_has_original_commit():
    result = subprocess.run(
        ["jj", "op", "log"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj op log."
    assert "jj new -m 'Feature X'" in result.stdout, "Original operation 'jj new -m 'Feature X'' not found in operation log."
