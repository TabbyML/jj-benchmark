import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_working_copy_parent_is_B():
    """Priority 1: Use jj CLI to verify the parent of the working copy."""
    result = subprocess.run(
        ["jj", "log", "-r", "@-", "-T", "description", "--no-graph"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "commit B" in result.stdout, f"Expected the working copy to be a child of 'commit B', but got: {result.stdout}"

def test_working_copy_is_empty():
    """Priority 1: Use jj CLI to verify the working copy is empty."""
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj status' failed: {result.stderr}"
    assert "Working copy changes:" not in result.stdout, f"Expected the working copy to be empty, but got: {result.stdout}"
