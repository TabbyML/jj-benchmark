import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_git_repo_exists():
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".git")), "Underlying Git repository not found."

def test_jj_repo_exists():
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".jj")), "Jujutsu repository not found."

def test_git_commit_exists():
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%s"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git log."
    assert "new commit" in result.stdout.strip(), "The new Git commit was not found in the Git repository."
