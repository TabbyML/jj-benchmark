import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
REMOTE_DIR = "/home/user/remote.git"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_git_binary_available():
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_remote_directory_exists():
    assert os.path.isdir(REMOTE_DIR), f"Remote directory {REMOTE_DIR} does not exist."

def test_remote_is_bare_git_repo():
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=REMOTE_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Git command failed in {REMOTE_DIR}: {result.stderr}"
    assert result.stdout.strip() == "true", f"{REMOTE_DIR} is not a bare git repository."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

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

def test_local_commit_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "My local commit" in result.stdout, "Expected initial commit 'My local commit' not found in local jj repo."

def test_local_bookmark_present():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-login" in result.stdout, "Expected bookmark 'feature-login' not found in local jj repo."

def test_remote_commit_present():
    result = subprocess.run(
        ["git", "log", "--format=%B", "feature-login"],
        cwd=REMOTE_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git log failed in remote repo: {result.stderr}"
    assert "Coworker commit" in result.stdout, "Expected commit 'Coworker commit' not found in remote git repo."
