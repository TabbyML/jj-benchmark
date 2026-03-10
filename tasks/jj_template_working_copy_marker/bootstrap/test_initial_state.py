import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/wc-marker-repo"
REPORT_FILE = "/home/user/wc-marker-repo/wc_marker_report.txt"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_repo_has_multiple_commits():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "all()", "-T", 'change_id.short(4) ++ "\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) >= 2, f"Expected at least 2 commits, got: {lines}"


def test_report_file_does_not_exist_yet():
    assert not os.path.isfile(REPORT_FILE), "wc_marker_report.txt should not exist before task is run."
