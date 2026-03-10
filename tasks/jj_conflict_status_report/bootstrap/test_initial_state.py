import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_service_yaml_has_conflict():
    path = os.path.join(REPO_DIR, "service.yaml")
    assert os.path.isfile(path), "service.yaml not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "service.yaml should have conflict markers."


def test_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "service.yaml" in result.stdout


def test_report_files_not_created():
    for f in ["status_before.txt", "conflicts_before.txt", "log_before.txt",
              "status_after.txt", "conflicts_after.txt", "log_after.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
