import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_data_json_has_conflict():
    path = os.path.join(REPO_DIR, "data.json")
    assert os.path.isfile(path), "data.json not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "data.json should have conflict markers."


def test_conflict_in_list():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "data.json" in result.stdout


def test_final_log_not_yet_created():
    assert not os.path.exists(os.path.join(REPO_DIR, "final_log.txt"))
