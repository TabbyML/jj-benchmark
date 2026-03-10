import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_env_sh_has_conflict():
    path = os.path.join(REPO_DIR, "env.sh")
    assert os.path.isfile(path), "env.sh not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "env.sh should have conflict markers."


def test_conflict_in_list():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "env.sh" in result.stdout


def test_output_files_not_created():
    for f in ["wc_status.txt", "wc_conflicts.txt", "wc_status_after.txt", "wc_conflicts_after.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
