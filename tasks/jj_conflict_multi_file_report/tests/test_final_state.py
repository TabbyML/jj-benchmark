import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_all_files_resolved():
    for fname in ["api.py", "db.py", "ui.py"]:
        path = os.path.join(REPO_DIR, fname)
        content = open(path).read()
        assert "<<<<<<<" not in content, f"{fname} still has conflict markers."


def test_api_py_content():
    content = open(os.path.join(REPO_DIR, "api.py")).read()
    assert "API_VERSION=3" in content
    assert "API_COMPAT=2" in content


def test_db_py_content():
    content = open(os.path.join(REPO_DIR, "db.py")).read()
    assert "DB_VERSION=3" in content
    assert "DB_COMPAT=2" in content


def test_ui_py_content():
    content = open(os.path.join(REPO_DIR, "ui.py")).read()
    assert "UI_VERSION=3" in content
    assert "UI_COMPAT=2" in content


def test_no_conflicts_remain():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_conflict_report_exists():
    path = os.path.join(REPO_DIR, "conflict_report.txt")
    assert os.path.isfile(path), "conflict_report.txt missing."
    content = open(path).read()
    for f in ["api.py", "db.py", "ui.py"]:
        assert f in content


def test_post_report_empty():
    path = os.path.join(REPO_DIR, "post_report.txt")
    assert os.path.isfile(path), "post_report.txt missing."
    assert open(path).read().strip() == ""


def test_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: feature versions (all resolved)" in result.stdout
