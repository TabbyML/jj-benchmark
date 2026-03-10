import os
import shutil
import subprocess
import pytest


REPO_DIR = "/home/user/support-repo"


def test_jj_binary_in_path():
    assert shutil.which("jj") is not None, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_dot_directory_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), \
        f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Expected 'main' bookmark to exist"


def test_abandoned_commit_not_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "ticket-1042" not in result.stdout, \
        "The ticket-1042 commit should be abandoned (not visible in default log)"


def test_op_log_has_abandon_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "abandon" in result.stdout.lower(), \
        "Expected an 'abandon' operation in op log"


def test_auth_fix_file_not_in_working_copy():
    auth_fix = os.path.join(REPO_DIR, "auth_fix.py")
    assert not os.path.isfile(auth_fix), \
        "auth_fix.py should not be present in working copy before recovery"
