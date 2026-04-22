import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "feature-x" in result.stdout, "Bookmark 'feature-x' does not exist in the initial state."
