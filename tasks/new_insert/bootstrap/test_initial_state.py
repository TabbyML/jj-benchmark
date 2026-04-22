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
    assert os.path.isdir(jj_dir), f"jj repository not initialized at {PROJECT_DIR}."

def test_initial_commits_exist():
    # Verify that commits with descriptions "commit A", "commit B", and "commit C" exist
    result = subprocess.run(
        ["jj", "log", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "commit A" in output, "Expected 'commit A' in jj history."
    assert "commit B" in output, "Expected 'commit B' in jj history."
    assert "commit C" in output, "Expected 'commit C' in jj history."
