import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
EXPERIMENT_DIR = "/home/user/myproject-experiment"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_experiment_dir_exists():
    assert os.path.isdir(EXPERIMENT_DIR), f"Experiment workspace directory {EXPERIMENT_DIR} does not exist."

def test_experiment_workspace_tracked():
    result = subprocess.run(
        ["jj", "workspace", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj workspace list' failed: {result.stderr}"
    assert "experiment: " in result.stdout, "Expected 'experiment' workspace to be tracked by jj initially."
