import os
import shutil
import subprocess

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
    output = result.stdout
    assert "main" in output, "Expected 'main' bookmark not found."
    assert "dev" in output, "Expected 'dev' bookmark not found."
    assert "feature" in output, "Expected 'feature' bookmark not found."

def test_feature_is_rebased_on_dev():
    result = subprocess.run(
        ["jj", "log", "-r", "dev..feature", "--no-graph", "-T", "bookmarks"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feature" in result.stdout, "Expected 'feature' to be a descendant of 'dev' initially."
