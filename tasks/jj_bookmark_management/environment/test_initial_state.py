import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def test_jj_binary_exists():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."

def test_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"

def test_initial_files_exist():
    main_py = os.path.join(REPO_DIR, "main.py")
    auth_py = os.path.join(REPO_DIR, "auth.py")
    assert os.path.isfile(main_py), "Expected file 'main.py' does not exist."
    assert os.path.isfile(auth_py), "Expected file 'auth.py' does not exist."

def test_initial_bookmarks_present():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    output = result.stdout
    assert "main" in output, "Expected bookmark 'main' not found."
    assert "auth-feature" in output, "Expected bookmark 'auth-feature' not found."

def test_initial_commit_descriptions():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    assert "initial commit" in output, "Expected commit message 'initial commit' not found."
    assert "feat: basic auth" in output, "Expected commit message 'feat: basic auth' not found."

def test_user_config_set():
    result = subprocess.run(
        ["jj", "config", "list", "--repo"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj config list failed"
    output = result.stdout
    assert "user.name" in output, "user.name config not found"
    assert "user.email" in output, "user.email config not found"
