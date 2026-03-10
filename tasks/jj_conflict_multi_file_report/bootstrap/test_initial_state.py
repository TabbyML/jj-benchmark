import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_three_conflicts_exist():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    for f in ["api.py", "db.py", "ui.py"]:
        assert f in result.stdout, f"{f} should be in conflict list."


def test_all_files_have_conflict_markers():
    for fname in ["api.py", "db.py", "ui.py"]:
        path = os.path.join(REPO_DIR, fname)
        assert os.path.isfile(path), f"{fname} not found."
        content = open(path).read()
        assert "<<<<<<<" in content, f"{fname} should have conflict markers."


def test_report_files_not_created():
    for f in ["conflict_report.txt", "conflict_count.txt", "post_report.txt", "final_log.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
