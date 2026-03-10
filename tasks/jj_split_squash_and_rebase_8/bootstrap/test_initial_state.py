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

def test_initial_commits_present():
    result = subprocess.run(
        ["jj", "log", "-r", "main..feature", "--no-graph", "-T", "description ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "add tests" in log, "Expected initial commit 'add tests' not found in log."
    assert "mixed changes" in log, "Expected initial commit 'mixed changes' not found in log."
    assert "add utils.py" in log, "Expected initial commit 'add utils.py' not found in log."

def test_initial_files_present():
    assert os.path.isfile(os.path.join(REPO_DIR, "utils.py")), "utils.py not found in repo."
    assert os.path.isfile(os.path.join(REPO_DIR, "api.py")), "api.py not found in repo."
    assert os.path.isfile(os.path.join(REPO_DIR, "test_api.py")), "test_api.py not found in repo."

def test_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, "Bookmark 'feature' not found."
