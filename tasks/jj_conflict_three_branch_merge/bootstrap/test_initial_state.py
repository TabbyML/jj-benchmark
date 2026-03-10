import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_main_py_has_conflict():
    path = os.path.join(REPO_DIR, "main.py")
    assert os.path.isfile(path), "main.py not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "main.py should have conflict markers."


def test_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "main.py" in result.stdout


def test_output_files_not_created():
    for f in ["conflicts.txt", "post_conflicts.txt", "merge_log.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
