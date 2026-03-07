import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/my-project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_git_binary_available():
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_repo_is_valid_git_repo():
    dot_git = os.path.join(REPO_DIR, ".git")
    assert os.path.isdir(dot_git), f"{REPO_DIR} is not a valid git repository (.git directory missing)."

def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"

def test_initial_branch_present():
    result = subprocess.run(
        ["git", "branch"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch failed: {result.stderr}"
    assert "feature-x" in result.stdout, "Expected initial git branch 'feature-x' not found."
