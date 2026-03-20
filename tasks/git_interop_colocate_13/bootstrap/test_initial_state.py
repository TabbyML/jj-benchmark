import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/my-project"

def test_binaries_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_is_git_repo_but_not_jj():
    dot_git = os.path.join(REPO_DIR, ".git")
    assert os.path.isdir(dot_git), f"{REPO_DIR} is not a valid Git repository (.git directory missing)."
    
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert not os.path.exists(dot_jj), f"{REPO_DIR} is already a jj repository (.jj directory exists), but it shouldn't be yet."

def test_initial_git_commit_exists():
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git log failed in {REPO_DIR}: {result.stderr}"
    lines = result.stdout.strip().split("\n")
    assert len(lines) >= 1, "Expected at least one initial Git commit."
