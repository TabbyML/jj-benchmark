import os
import shutil
import subprocess
import pytest

UPSTREAM_REPO = "/home/user/upstream.git"
PROJECT_REPO = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_directories_exist():
    assert os.path.isdir(UPSTREAM_REPO), f"Upstream repository {UPSTREAM_REPO} does not exist."
    assert os.path.isdir(PROJECT_REPO), f"Project repository {PROJECT_REPO} does not exist."

def test_upstream_is_bare_git_repo():
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=UPSTREAM_REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git rev-parse failed in {UPSTREAM_REPO}: {result.stderr}"
    assert result.stdout.strip() == "true", f"{UPSTREAM_REPO} is not a bare Git repository."

def test_project_is_git_repo():
    dot_git = os.path.join(PROJECT_REPO, ".git")
    assert os.path.isdir(dot_git), f"{PROJECT_REPO} is not a valid Git repository (.git directory missing)."
    result = subprocess.run(
        ["git", "status"],
        cwd=PROJECT_REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git status failed in {PROJECT_REPO}: {result.stderr}"

def test_project_is_not_jj_repo():
    dot_jj = os.path.join(PROJECT_REPO, ".jj")
    assert not os.path.isdir(dot_jj), f"{PROJECT_REPO} should not be a jj repository yet."
