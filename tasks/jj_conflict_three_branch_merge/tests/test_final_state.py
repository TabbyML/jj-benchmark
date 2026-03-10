import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_main_py_resolved():
    path = os.path.join(REPO_DIR, "main.py")
    content = open(path).read()
    assert "<<<<<<<" not in content, "main.py still has conflict markers."
    assert "MODE = 'AB'" in content, f"Expected MODE = 'AB'. Got: {content}"
    assert "FEATURES" in content and "'A'" in content and "'B'" in content, \
        f"Expected FEATURES list. Got: {content}"


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_conflicts_txt_exists():
    path = os.path.join(REPO_DIR, "conflicts.txt")
    assert os.path.isfile(path), "conflicts.txt missing."
    assert "main.py" in open(path).read()


def test_post_conflicts_empty():
    path = os.path.join(REPO_DIR, "post_conflicts.txt")
    assert os.path.isfile(path), "post_conflicts.txt missing."
    assert open(path).read().strip() == ""


def test_merge_log_exists():
    path = os.path.join(REPO_DIR, "merge_log.txt")
    assert os.path.isfile(path), "merge_log.txt missing."
    assert "feat: merge modes A and B" in open(path).read()


def test_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: merge modes A and B" in result.stdout
