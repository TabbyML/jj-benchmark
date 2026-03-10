import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found."


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), ".jj missing."


def test_two_conflicts_exist():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "server.cfg" in result.stdout, f"server.cfg conflict missing. Got: {result.stdout}"
    assert "client.cfg" in result.stdout, f"client.cfg conflict missing. Got: {result.stdout}"


def test_conflict_markers_in_files():
    for fname in ["server.cfg", "client.cfg"]:
        fpath = os.path.join(REPO_DIR, fname)
        assert os.path.isfile(fpath), f"{fname} not found."
        content = open(fpath).read()
        assert "<<<<<<<" in content, f"{fname} should have conflict markers."


def test_output_files_not_yet_created():
    for fname in ["conflicts_before.txt", "conflicts_after.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, fname)), f"{fname} should not exist yet."
