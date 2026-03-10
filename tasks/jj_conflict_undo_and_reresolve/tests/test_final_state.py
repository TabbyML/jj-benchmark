import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_config_py_resolved_correctly():
    path = os.path.join(REPO_DIR, "config.py")
    content = open(path).read()
    assert "<<<<<<<" not in content, "config.py still has conflict markers."
    assert "TIMEOUT = 60" in content, f"Expected TIMEOUT = 60. Got: {content}"
    assert "RETRY = 3" in content, f"Expected RETRY = 3. Got: {content}"


def test_no_conflicts_remain():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_re_conflict_txt_exists():
    path = os.path.join(REPO_DIR, "re_conflict.txt")
    assert os.path.isfile(path), "re_conflict.txt missing."


def test_final_status_txt_exists():
    path = os.path.join(REPO_DIR, "final_status.txt")
    assert os.path.isfile(path), "final_status.txt missing."


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: custom timeout (resolved)" in result.stdout
