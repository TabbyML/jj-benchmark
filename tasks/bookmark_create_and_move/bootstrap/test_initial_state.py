import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/my-project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_is_jj_repo():
    result = subprocess.run(
        ["jj", "root"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"Not a valid jj repository at {PROJECT_DIR}: {result.stderr}"

def test_no_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "feature-x" not in result.stdout, "Bookmark 'feature-x' should not exist initially."
