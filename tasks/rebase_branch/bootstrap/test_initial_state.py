import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {PROJECT_DIR}. Repository not initialized."

def test_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj bookmark list' failed: {result.stderr}"
    assert "main" in result.stdout, "Expected 'main' bookmark to exist."
    assert "feature-branch" in result.stdout, "Expected 'feature-branch' bookmark to exist."

def test_data_txt_exists():
    # It might be in the history or working copy, let's just check if it's in the repo
    result = subprocess.run(
        ["jj", "file", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj file list' failed: {result.stderr}"
    assert "data.txt" in result.stdout, "Expected 'data.txt' to exist in the repository."