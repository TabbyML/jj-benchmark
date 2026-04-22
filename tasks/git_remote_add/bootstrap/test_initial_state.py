import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_repo_not_initialized():
    assert not os.path.exists(os.path.join(PROJECT_DIR, ".jj")), "Expected .jj directory to not exist initially."
    assert not os.path.exists(os.path.join(PROJECT_DIR, ".git")), "Expected .git directory to not exist initially."
