import os
import shutil
import subprocess
import pytest

GIT_DIR = "/home/user/git-repo"
JJ_DIR = "/home/user/jj-repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_git_binary_available():
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_git_repo_exists():
    assert os.path.isdir(GIT_DIR), f"Git repo directory {GIT_DIR} does not exist."
    assert os.path.isdir(os.path.join(GIT_DIR, ".git")), f"{GIT_DIR} is not a git repository."

def test_jj_repo_exists():
    assert os.path.isdir(JJ_DIR), f"Jujutsu repo directory {JJ_DIR} does not exist."
    assert os.path.isdir(os.path.join(JJ_DIR, ".jj")), f"{JJ_DIR} is not a jujutsu repository."

def test_jj_repo_is_not_colocated():
    assert not os.path.isdir(os.path.join(JJ_DIR, ".git")), f"{JJ_DIR} is colocated, but it should not be."

def test_git_target_is_correct():
    git_target = os.path.join(JJ_DIR, ".jj", "repo", "store", "git_target")
    assert os.path.isfile(git_target), f"{git_target} does not exist."
    with open(git_target, "r") as f:
        target = f.read().strip()
    assert target == os.path.join(GIT_DIR, ".git") or target.endswith("/git-repo/.git"), "The backing git repo is not correct."

def test_feature_x_bookmark_exists_in_jj():
    result = subprocess.run(["jj", "bookmark", "list"], cwd=JJ_DIR, capture_output=True, text=True)
    assert "feature-x" in result.stdout, "Bookmark feature-x does not exist in Jujutsu repo."

def test_feature_x_branch_not_in_git():
    result = subprocess.run(["git", "branch", "--list", "feature-x"], cwd=GIT_DIR, capture_output=True, text=True)
    assert "feature-x" not in result.stdout, "Branch feature-x already exists in Git repo, but it should not."
