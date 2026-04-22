import os
import subprocess
import pytest

REMOTE_DIR = "/home/user/remote.git"

def test_feature_pushed_to_remote():
    # Check if feature branch exists in remote
    result = subprocess.run(["git", "branch", "--list", "feature"], cwd=REMOTE_DIR, capture_output=True, text=True)
    assert "feature" in result.stdout, "Expected 'feature' branch to be pushed to the remote repository."

def test_feature_rebased_on_main():
    # Check if main is an ancestor of feature in the remote repository
    result = subprocess.run(["git", "merge-base", "--is-ancestor", "main", "feature"], cwd=REMOTE_DIR)
    assert result.returncode == 0, "Expected 'feature' to be rebased onto the latest 'main'."
