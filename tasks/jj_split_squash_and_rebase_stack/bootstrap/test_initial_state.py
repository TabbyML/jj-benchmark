import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/repo"

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
    assert "feature-stack" in output, "Expected 'feature-stack' bookmark not found."

def test_initial_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "--template", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "Add feature A\n" in log, "Expected initial commit 'Add feature A' not found in log."
    assert "Update feature A and add feature B\n" in log, "Expected initial commit 'Update feature A and add feature B' not found in log."
    assert "Fix typo in feature A\n" in log, "Expected initial commit 'Fix typo in feature A' not found in log."

def test_files_exist_in_working_copy():
    # Since feature-stack points to the third commit, feature_a.py and feature_b.py should exist in the working copy.
    assert os.path.isfile(os.path.join(REPO_DIR, "feature_a.py")), "feature_a.py is missing from working copy."
    assert os.path.isfile(os.path.join(REPO_DIR, "feature_b.py")), "feature_b.py is missing from working copy."
