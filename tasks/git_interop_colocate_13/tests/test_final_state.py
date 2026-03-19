import os
import subprocess
import pytest

REPO_DIR = "/home/user/my-project"

def run_cmd(cmd, *args):
    return subprocess.run([cmd] + list(args), cwd=REPO_DIR, capture_output=True, text=True)

def test_jj_directory_exists():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"The .jj directory does not exist. Did you run `jj git init --colocate`?"

def test_jj_bookmark_exists():
    result = run_cmd("jj", "bookmark", "list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-x" in result.stdout, "The jj bookmark 'feature-x' does not exist."

def test_git_branch_exists():
    result = run_cmd("git", "branch")
    assert result.returncode == 0, f"git branch failed: {result.stderr}"
    assert "feature-x" in result.stdout, "The git branch 'feature-x' does not exist. Make sure the jj bookmark was exported to Git."

def test_head_commit_description():
    result = run_cmd("jj", "log", "--no-graph", "-r", "@", "-T", "description")
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Add feature.txt" in result.stdout, f"Expected commit description 'Add feature.txt', but got: {result.stdout.strip()}"

def test_feature_file_exists_and_content():
    feature_file = os.path.join(REPO_DIR, "feature.txt")
    assert os.path.isfile(feature_file), "The file 'feature.txt' does not exist in the working copy."
    with open(feature_file, "r") as f:
        content = f.read().strip()
    assert content == "Hello jj", f"Expected 'feature.txt' to contain 'Hello jj', but got: '{content}'"
