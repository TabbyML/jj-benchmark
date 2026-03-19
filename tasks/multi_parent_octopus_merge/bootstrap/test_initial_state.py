import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"

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
    assert "feature-a" in output, "Bookmark 'feature-a' not found."
    assert "feature-b" in output, "Bookmark 'feature-b' not found."
    assert "feature-c" in output, "Bookmark 'feature-c' not found."

def test_files_exist_in_revisions():
    # Check that feature-a has a.txt
    res_a = subprocess.run(["jj", "file", "show", "a.txt", "-r", "feature-a"], cwd=REPO_DIR, capture_output=True)
    assert res_a.returncode == 0, "File a.txt not found in feature-a revision."

    # Check that feature-b has b.txt
    res_b = subprocess.run(["jj", "file", "show", "b.txt", "-r", "feature-b"], cwd=REPO_DIR, capture_output=True)
    assert res_b.returncode == 0, "File b.txt not found in feature-b revision."

    # Check that feature-c has c.txt
    res_c = subprocess.run(["jj", "file", "show", "c.txt", "-r", "feature-c"], cwd=REPO_DIR, capture_output=True)
    assert res_c.returncode == 0, "File c.txt not found in feature-c revision."