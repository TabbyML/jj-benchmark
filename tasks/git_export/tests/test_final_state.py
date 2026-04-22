import os
import subprocess
import pytest

GIT_DIR = "/home/user/git-repo"

def test_feature_x_branch_exists_in_git():
    result = subprocess.run(["git", "branch", "--list", "feature-x"], cwd=GIT_DIR, capture_output=True, text=True)
    assert "feature-x" in result.stdout, "Branch feature-x was not exported to the Git repository."

def test_feature_x_commit_content():
    # Verify the commit has the expected message
    result = subprocess.run(["git", "log", "-1", "--format=%B", "feature-x"], cwd=GIT_DIR, capture_output=True, text=True)
    assert "jj commit" in result.stdout, "The exported branch feature-x does not have the expected commit."
