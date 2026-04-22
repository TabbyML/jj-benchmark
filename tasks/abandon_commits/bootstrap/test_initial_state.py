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
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_initial_files_exist():
    for filename in ["a.txt", "b.txt", "c.txt", "d.txt"]:
        file_path = os.path.join(PROJECT_DIR, filename)
        assert os.path.isfile(file_path), f"Expected file {filename} does not exist in the working copy."

def test_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "feature-a" in output, "Bookmark 'feature-a' does not exist."
    assert "experiment" in output, "Bookmark 'experiment' does not exist."
    assert "draft" in output, "Bookmark 'draft' does not exist."
