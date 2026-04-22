import os
import subprocess
import pytest

REMOTE_DIR = "/home/user/remote.git"

def test_remote_branch_exists():
    """Priority 1: Use Git CLI to verify the branch exists in the remote repository."""
    result = subprocess.run(
        ["git", "branch", "--list", "my-feature"],
        capture_output=True, text=True, cwd=REMOTE_DIR
    )
    assert result.returncode == 0, f"'git branch' failed: {result.stderr}"
    assert "my-feature" in result.stdout, f"Expected branch 'my-feature' in remote repo, got: {result.stdout}"

def test_remote_branch_contains_file():
    """Priority 1: Use Git CLI to verify the branch contains the expected file."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "my-feature"],
        capture_output=True, text=True, cwd=REMOTE_DIR
    )
    assert result.returncode == 0, f"'git ls-tree' failed: {result.stderr}"
    assert "feature.txt" in result.stdout, f"Expected 'feature.txt' in branch 'my-feature', got: {result.stdout}"
