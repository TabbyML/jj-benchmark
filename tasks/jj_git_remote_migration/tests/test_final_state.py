import os
import subprocess
import pytest

PROJECT_REPO = "/home/user/project"

def test_project_is_colocated_repo():
    dot_jj = os.path.join(PROJECT_REPO, ".jj")
    dot_git = os.path.join(PROJECT_REPO, ".git")
    assert os.path.isdir(dot_jj), f"{PROJECT_REPO} is not a valid jj repository (.jj directory missing)."
    assert os.path.isdir(dot_git), f"{PROJECT_REPO} is not a valid git repository (.git directory missing)."
    
    result = subprocess.run(
        ["jj", "status"],
        cwd=PROJECT_REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {PROJECT_REPO}: {result.stderr}"

def test_upstream_remote_added():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        cwd=PROJECT_REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "upstream" in result.stdout, "Git remote 'upstream' not found in jj."
    assert "/home/user/upstream.git" in result.stdout, "Git remote 'upstream' URL is incorrect."

def test_working_copy_rebased():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "parents.map(|c| c.bookmarks()).join(', ')"],
        cwd=PROJECT_REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "main@upstream" in result.stdout, "Working copy parent is not main@upstream."
