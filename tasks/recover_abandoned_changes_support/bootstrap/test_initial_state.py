import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/auth-service"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"

def test_main_files_exist():
    readme_path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme_path), f"Expected file {readme_path} not found."
    
    utils_path = os.path.join(REPO_DIR, "utils.py")
    assert os.path.isfile(utils_path), f"Expected file {utils_path} not found."

def test_abandoned_commit_exists():
    result = subprocess.run(
        ["jj", "op", "log"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "abandon commit" in result.stdout, "Abandoned commit operation not found in the operation log."

def test_feature_login_bookmark_does_not_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feature-login" not in result.stdout, "Bookmark 'feature-login' should not exist."

def test_login_file_not_in_working_copy():
    login_path = os.path.join(REPO_DIR, "login.py")
    assert not os.path.exists(login_path), f"File {login_path} should not be in the working copy initially."
