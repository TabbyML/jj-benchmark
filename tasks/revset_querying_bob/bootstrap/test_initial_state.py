import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    result = subprocess.run(["jj", "root"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Directory {PROJECT_DIR} is not a valid jj repository."

def test_main_bookmark_exists():
    result = subprocess.run(["jj", "bookmark", "list"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "main:" in result.stdout, "The repository does not have a 'main' bookmark."
