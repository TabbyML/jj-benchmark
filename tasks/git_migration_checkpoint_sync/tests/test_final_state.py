import os
import subprocess
import pytest

REPO_DIR = "/home/user/my-project"

def run_cmd(cmd_list):
    return subprocess.run(cmd_list, cwd=REPO_DIR, capture_output=True, text=True)

def test_new_feature_file_exists():
    file_path = os.path.join(REPO_DIR, "new_feature.txt")
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "Hello jj", f"Expected file content 'Hello jj', got '{content}'."

def test_jj_bookmark_created():
    result = run_cmd(["jj", "bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "jj-feature-y" in result.stdout, "jj bookmark 'jj-feature-y' was not created."

def test_git_branches_log_contains_bookmark():
    log_path = os.path.join(REPO_DIR, "git_branches.log")
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "jj-feature-y" in content, "git_branches.log does not contain 'jj-feature-y'."

def test_git_branch_actually_exported():
    result = run_cmd(["git", "branch"])
    assert result.returncode == 0, f"git branch failed: {result.stderr}"
    assert "jj-feature-y" in result.stdout, "Git does not see 'jj-feature-y' branch. Export may have failed."
