import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_module_py_has_resolved_content():
    path = os.path.join(REPO_DIR, "module.py")
    content = open(path).read()
    assert "<<<<<<<" not in content, "module.py still has conflict markers."
    assert "VALUE = 20" in content, f"Expected VALUE = 20. Got: {content}"


def test_before_absorb_txt_exists():
    path = os.path.join(REPO_DIR, "before_absorb.txt")
    assert os.path.isfile(path), "before_absorb.txt missing."
    assert "module.py" in open(path).read()


def test_after_absorb_txt_exists():
    path = os.path.join(REPO_DIR, "after_absorb.txt")
    assert os.path.isfile(path), "after_absorb.txt missing."


def test_feature_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: update value to 20 (resolved)" in result.stdout
