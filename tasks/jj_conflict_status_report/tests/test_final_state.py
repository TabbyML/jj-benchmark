import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

ALL_REPORTS = ["status_before.txt", "conflicts_before.txt", "log_before.txt",
               "status_after.txt", "conflicts_after.txt", "log_after.txt"]


def test_all_report_files_exist():
    for f in ALL_REPORTS:
        path = os.path.join(REPO_DIR, f)
        assert os.path.isfile(path), f"{f} missing."


def test_conflicts_before_has_service_yaml():
    content = open(os.path.join(REPO_DIR, "conflicts_before.txt")).read()
    assert "service.yaml" in content


def test_service_yaml_resolved():
    path = os.path.join(REPO_DIR, "service.yaml")
    content = open(path).read()
    assert "<<<<<<<" not in content
    assert "replicas: 5" in content
    assert "strategy: RollingUpdate" in content


def test_conflicts_after_empty():
    content = open(os.path.join(REPO_DIR, "conflicts_after.txt")).read().strip()
    assert content == "", f"conflicts_after.txt should be empty. Got: {content}"


def test_log_after_has_updated_description():
    content = open(os.path.join(REPO_DIR, "log_after.txt")).read()
    assert "feat: scale to 5 (resolved)" in content


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: scale to 5 (resolved)" in result.stdout
