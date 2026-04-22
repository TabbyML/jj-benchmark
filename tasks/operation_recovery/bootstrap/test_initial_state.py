import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), "Project directory not found."

def test_op_log_has_commits():
    result = subprocess.run(["jj", "log"], capture_output=True, text=True, cwd=PROJECT_DIR)
    assert "Commit 5" in result.stdout, "Expected 'Commit 5' in jj log."
