import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"

def test_git_binary_available():
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_repo_is_valid_git_repo():
    dot_git = os.path.join(REPO_DIR, ".git")
    assert os.path.isdir(dot_git), f"{REPO_DIR} is not a valid git repository (.git directory missing)."
    result = subprocess.run(
        ["git", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git status failed in {REPO_DIR}: {result.stderr}"

def test_repo_is_not_jj_repo_yet():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert not os.path.exists(dot_jj), f"{REPO_DIR} is already a jj repository (.jj directory exists)."

def test_main_branch_exists():
    result = subprocess.run(
        ["git", "branch"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch failed in {REPO_DIR}: {result.stderr}"
    assert "main" in result.stdout, "Expected initial branch 'main' not found."

def test_app_py_exists():
    app_py_path = os.path.join(REPO_DIR, "app.py")
    assert os.path.isfile(app_py_path), f"Expected file {app_py_path} does not exist."
