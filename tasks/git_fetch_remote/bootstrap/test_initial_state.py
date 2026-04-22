import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"
REMOTE_DIR = "/home/user/remote.git"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_remote_dir_exists():
    assert os.path.isdir(REMOTE_DIR), f"Remote directory {REMOTE_DIR} does not exist."

def test_feature_bookmark_exists():
    result = subprocess.run(["jj", "bookmark", "list"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "feature" in result.stdout, "Expected 'feature' bookmark to exist in the local repo."
