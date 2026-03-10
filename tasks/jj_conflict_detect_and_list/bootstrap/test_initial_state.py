import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), ".jj directory missing."


def test_conflict_exists():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "config.txt" in result.stdout, f"Expected conflict in config.txt. Got: {result.stdout}"


def test_status_shows_conflict():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    assert "conflict" in result.stdout.lower() or "C " in result.stdout, \
        f"Expected conflict indicator in jj status. Got: {result.stdout}"


def test_output_files_do_not_exist_yet():
    for fname in ["status_output.txt", "conflict_list.txt", "log_output.txt"]:
        path = os.path.join(REPO_DIR, fname)
        assert not os.path.exists(path), f"{fname} should not exist yet."
