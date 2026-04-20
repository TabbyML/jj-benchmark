import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_repo_is_colocated():
    """Priority 3: Check if both .jj and .git directories exist."""
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".jj")), "Expected .jj directory to exist in /home/user/myproject."
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".git")), "Expected .git directory to exist in /home/user/myproject."

def test_remotes_configured_correctly():
    """Priority 1: Use jj CLI to verify the remotes."""
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj git remote list' failed: {result.stderr}"
    
    stdout = result.stdout
    
    # Verify public remote exists and points to the correct URL
    assert "public" in stdout, f"Expected 'public' remote to exist, got: {stdout}"
    assert "https://github.com/example/up.git" in stdout, f"Expected 'public' remote to point to https://github.com/example/up.git, got: {stdout}"
    
    # Verify origin and upstream do not exist
    assert "origin" not in stdout, f"Expected 'origin' remote to not exist, got: {stdout}"
    assert "upstream" not in stdout, f"Expected 'upstream' remote to not exist, got: {stdout}"
