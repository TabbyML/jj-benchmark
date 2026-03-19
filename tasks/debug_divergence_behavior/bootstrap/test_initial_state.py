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

def test_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, "Bookmark 'feature' not found in repository."

def test_divergence_exists():
    result = subprocess.run(
        ["jj", "log", "-r", "bookmarks(exact:feature)", "--no-graph", "-T", "commit_id ++ \"\\n\""],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    assert len(lines) > 1, f"Expected divergent commits for 'feature' bookmark, but found {len(lines)} commits."

def test_main_py_exists():
    main_py_path = os.path.join(REPO_DIR, "main.py")
    # In jj, divergence means the working copy might be at one of the divergent commits or a conflict.
    # We just check that main.py exists in the working copy.
    assert os.path.isfile(main_py_path), "main.py does not exist in the working copy."
