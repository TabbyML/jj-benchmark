import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
REMOTE_DIR = "/home/user/remote.git"

def test_jj_repo_exists():
    """Priority 3: Check if the .jj directory exists indicating a jj clone."""
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found at {jj_dir}, did you clone with jj?"

def test_feature_file_content():
    """Priority 3: Check if feature.txt contains the expected text."""
    file_path = os.path.join(REPO_DIR, "feature.txt")
    assert os.path.isfile(file_path), f"feature.txt not found at {file_path}"
    with open(file_path) as f:
        content = f.read()
    assert "hello world" in content, f"Expected 'hello world' in feature.txt, got: {content}"

def test_bookmark_exists_in_jj():
    """Priority 1: Use jj CLI to verify the bookmark was created."""
    result = subprocess.run(
        ["jj", "log", "-r", "my-feature", "--no-pager"],
        capture_output=True, text=True, cwd=REPO_DIR
    )
    assert result.returncode == 0, f"'jj log -r my-feature' failed: {result.stderr}"

def test_bookmark_pushed_to_remote():
    """Priority 1: Use git CLI to verify the bookmark was pushed to the remote."""
    result = subprocess.run(
        ["git", "show-ref", "--verify", "refs/heads/my-feature"],
        capture_output=True, text=True, cwd=REMOTE_DIR
    )
    assert result.returncode == 0, f"The bookmark 'my-feature' was not found in the remote repository: {result.stderr}"
