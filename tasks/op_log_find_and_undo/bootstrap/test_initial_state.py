import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"
HOME_DIR = "/home/user"


def test_jj_binary_exists():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_repo_is_valid_jj_repo():
    result = subprocess.run(
        ["jj", "root"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Not a valid jj repo: {result.stderr}"
    assert REPO_DIR in result.stdout.strip(), f"Unexpected jj root: {result.stdout.strip()}"


def test_feature_bookmark_is_absent():
    """Before the task, the feature bookmark must NOT exist (it was accidentally lost)."""
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" not in result.stdout, (
        "feature bookmark should be absent in the initial state"
    )


def test_feature_file_is_absent():
    """Before the task, feature.txt must NOT exist (the commit was abandoned)."""
    feature_file = os.path.join(REPO_DIR, "feature.txt")
    assert not os.path.isfile(feature_file), (
        f"feature.txt should not exist in initial state: {feature_file}"
    )


def test_op_log_has_entries():
    """Operation log must have at least one entry (the abandon operation)."""
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "--limit", "5"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "Operation log is empty"


def test_initial_commit_exists():
    """The repo must have at least one non-root commit (the 'initial commit')."""
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "No commits found in repo"
