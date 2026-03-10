import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_readme_resolved():
    path = os.path.join(REPO_DIR, "README.md")
    content = open(path).read()
    assert "<<<<<<<" not in content, "README.md still has conflict markers."
    assert "Version: 3" in content, f"Expected Version: 3. Got: {content}"
    assert "Changelog" in content, f"Expected Changelog line. Got: {content}"


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "docs: resolve version conflict" in result.stdout


def test_commit_details_txt_exists():
    path = os.path.join(REPO_DIR, "commit_details.txt")
    assert os.path.isfile(path), "commit_details.txt missing."


def test_full_log_txt_exists():
    path = os.path.join(REPO_DIR, "full_log.txt")
    assert os.path.isfile(path), "full_log.txt missing."
    assert "docs: resolve version conflict" in open(path).read()


def test_verify_clean_is_empty():
    path = os.path.join(REPO_DIR, "verify_clean.txt")
    assert os.path.isfile(path), "verify_clean.txt missing."
    assert open(path).read().strip() == ""
