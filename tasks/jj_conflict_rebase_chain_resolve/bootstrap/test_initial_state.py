import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_conflict_exists_in_chain():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "vars.sh" in result.stdout, f"Expected vars.sh conflict. Got: {result.stdout}"


def test_chain_commits_exist():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "chain: set X=2" in result.stdout
    assert "chain: set Y=X" in result.stdout


def test_output_files_not_created():
    for f in ["before.txt", "chain_log.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
