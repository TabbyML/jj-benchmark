import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_repo_is_jj_repo():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_bookmarks_exist():
    # Check if feature-a and feature-b bookmarks exist
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "feature-a" in result.stdout, "Bookmark 'feature-a' does not exist."
    assert "feature-b" in result.stdout, "Bookmark 'feature-b' does not exist."