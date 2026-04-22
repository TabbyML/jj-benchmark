import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/my-project"

def test_bookmark_exists_via_cli():
    """Priority 1: Use jj CLI to verify the bookmark exists."""
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj bookmark list' failed: {result.stderr}"
    assert "feature-x" in result.stdout, f"Expected 'feature-x' in bookmarks, got: {result.stdout}"

def test_bookmark_target_description_via_cli():
    """Priority 1: Use jj CLI to verify the commit description of the bookmark."""
    result = subprocess.run(
        ["jj", "log", "-r", "feature-x", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "add feature y" in result.stdout, f"Expected commit description to be 'add feature y', got: {result.stdout}"
