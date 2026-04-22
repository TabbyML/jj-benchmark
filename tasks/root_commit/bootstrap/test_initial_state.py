import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    # Verify it's a valid jj repo by running jj root
    result = subprocess.run(
        ["jj", "root"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to run jj root in {PROJECT_DIR}. Is it a valid jj repository?"
    assert result.stdout.strip() == PROJECT_DIR, f"Expected jj root to be {PROJECT_DIR}, but got {result.stdout.strip()}"

def test_initial_state_not_root_child():
    # The working copy should NOT currently be a direct child of the root commit
    # We'll create some commits in the Dockerfile so the working copy has a history
    result = subprocess.run(
        ["jj", "log", "-T", 'commit_id.short() ++ "\\n"', "-r", "@-", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    parent_id = result.stdout.strip()
    assert parent_id != "000000000000", "Working copy is already a direct child of the root commit. The initial state should have some history."
