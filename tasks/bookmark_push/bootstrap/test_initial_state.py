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

def test_remote_repo_exists():
    assert os.path.isdir(REMOTE_DIR), f"Remote bare Git repository {REMOTE_DIR} does not exist."
    assert os.path.isfile(os.path.join(REMOTE_DIR, "config")), f"Not a valid bare Git repo: {REMOTE_DIR}"

def test_local_repo_exists():
    assert os.path.isdir(REPO_DIR), f"Local jj repository {REPO_DIR} does not exist."
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), f"Not a valid jj repo: {REPO_DIR}"

def test_feature_file_exists():
    feature_file = os.path.join(REPO_DIR, "feature.txt")
    assert os.path.isfile(feature_file), f"Expected file {feature_file} to exist in the local repo."

def test_bookmark_does_not_exist_yet():
    # Verify that the bookmark my-feature does not exist yet.
    result = subprocess.run(["jj", "bookmark", "list"], capture_output=True, text=True, cwd=REPO_DIR)
    assert "my-feature" not in result.stdout, "Bookmark 'my-feature' should not exist initially."
