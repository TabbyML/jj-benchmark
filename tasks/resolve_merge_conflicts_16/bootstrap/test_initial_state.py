import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

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

def test_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-a" in result.stdout, "Bookmark 'feature-a' not found."
    assert "feature-b" in result.stdout, "Bookmark 'feature-b' not found."

def test_app_py_exists_in_history():
    # Check that app.py exists in feature-a
    result_a = subprocess.run(
        ["jj", "file", "show", "app.py", "-r", "feature-a"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result_a.returncode == 0, f"app.py not found in feature-a: {result_a.stderr}"
    
    # Check that app.py exists in feature-b
    result_b = subprocess.run(
        ["jj", "file", "show", "app.py", "-r", "feature-b"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result_b.returncode == 0, f"app.py not found in feature-b: {result_b.stderr}"
