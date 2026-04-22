import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"
NESTED_DIR = "/home/user/repo/deeply/nested/dir"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_nested_directory_exists():
    assert os.path.isdir(NESTED_DIR), f"Nested directory {NESTED_DIR} does not exist."

def test_is_jj_workspace():
    # Verify that the project directory is a jj workspace
    result = subprocess.run(
        ["jj", "workspace", "root"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Expected {PROJECT_DIR} to be a jj workspace."
    assert result.stdout.strip() == PROJECT_DIR, f"Expected workspace root to be {PROJECT_DIR}."
