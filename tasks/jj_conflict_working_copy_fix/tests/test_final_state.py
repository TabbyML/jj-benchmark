import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_env_sh_resolved():
    path = os.path.join(REPO_DIR, "env.sh")
    content = open(path).read()
    assert "<<<<<<<" not in content, "env.sh still has conflict markers."
    assert "ENV=prod" in content, f"Expected ENV=prod. Got: {content}"
    assert "DEV_OVERRIDE=true" in content, f"Expected DEV_OVERRIDE=true. Got: {content}"


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_wc_status_txt_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "wc_status.txt"))


def test_wc_conflicts_txt_exists():
    path = os.path.join(REPO_DIR, "wc_conflicts.txt")
    assert os.path.isfile(path), "wc_conflicts.txt missing."
    assert "env.sh" in open(path).read()


def test_wc_conflicts_after_empty():
    path = os.path.join(REPO_DIR, "wc_conflicts_after.txt")
    assert os.path.isfile(path), "wc_conflicts_after.txt missing."
    assert open(path).read().strip() == ""


def test_wc_status_after_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "wc_status_after.txt"))


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "wc: set ENV with dev override" in result.stdout
