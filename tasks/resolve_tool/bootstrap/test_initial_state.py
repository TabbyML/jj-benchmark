import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_unresolved_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "file1.txt" in result.stdout, "Expected file1.txt to have unresolved conflicts."
    assert "file2.txt" in result.stdout, "Expected file2.txt to have unresolved conflicts."
