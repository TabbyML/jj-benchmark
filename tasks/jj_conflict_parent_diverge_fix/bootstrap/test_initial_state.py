import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_params_env_has_conflict():
    path = os.path.join(REPO_DIR, "params.env")
    assert os.path.isfile(path), "params.env not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "params.env should have conflict markers."


def test_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "params.env" in result.stdout


def test_output_files_not_created():
    for f in ["diverge_conflicts.txt", "final_log.txt", "final_params.txt", "verify.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
