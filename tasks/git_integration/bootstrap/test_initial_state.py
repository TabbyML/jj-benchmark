import os
import shutil
import pytest

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_remote_git_repo_exists():
    remote_path = "/home/user/remote.git"
    assert os.path.isdir(remote_path), f"Bare git repository {remote_path} does not exist."
    assert os.path.isdir(os.path.join(remote_path, "objects")), f"{remote_path} is not a bare git repo."

def test_repo_directory_does_not_exist():
    repo_path = "/home/user/repo"
    assert not os.path.exists(repo_path), f"Directory {repo_path} should not exist before the task."
