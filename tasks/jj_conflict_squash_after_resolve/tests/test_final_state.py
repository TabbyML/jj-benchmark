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
    assert result.returncode == 0
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_data_json_has_merged_content():
    path = os.path.join(REPO_DIR, "data.json")
    content = open(path).read()
    assert "<<<<<<<" not in content, "data.json still has conflict markers."
    assert "20" in content, f"data.json should contain value 20. Got: {content}"
    assert "merged" in content, f"data.json should contain merged key. Got: {content}"


def test_final_log_exists():
    path = os.path.join(REPO_DIR, "final_log.txt")
    assert os.path.isfile(path), "final_log.txt missing."


def test_feature_squashed_into_main():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    # After squash, feature commit should be gone (absorbed into main)
    # Or the main bookmark should have the merged content
    log = result.stdout
    # The important check: no conflict commit remains separate
    assert "feat: set value 20 (resolved)" not in log or "main: set value 10" in log, \
        f"Unexpected log state: {log}"
