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
    # Check if .jj directory exists
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_v1_0_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "v1.0" in result.stdout, "Bookmark 'v1.0' does not exist in the repository."

def test_working_copy_files_exist():
    for filename in ["config.py", "utils.py", "app.py"]:
        file_path = os.path.join(PROJECT_DIR, filename)
        assert os.path.isfile(file_path), f"File {filename} does not exist in the working copy."

def test_working_copy_has_changes():
    result = subprocess.run(
        ["jj", "status"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "config.py" in result.stdout, "config.py is not modified in the working copy."
    assert "utils.py" in result.stdout, "utils.py is not modified in the working copy."
    assert "app.py" in result.stdout, "app.py is not modified in the working copy."
