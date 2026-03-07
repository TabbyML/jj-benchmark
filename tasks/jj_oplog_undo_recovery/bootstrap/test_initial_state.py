import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory not found: {REPO_DIR}"


def test_jj_subdirectory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj status failed with exit code {result.returncode}: "
        f"{result.stderr.decode()}"
    )


def test_readme_file_exists_in_history():
    """README.md must exist in at least one commit in the repo."""
    result = subprocess.run(
        ["jj", "file", "list", "--no-pager", "-r", "description(substring:'add initial readme')"],
        capture_output=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        "Could not find commit with description 'add initial readme'"
    )
    output = result.stdout.decode()
    assert "README.md" in output, f"README.md not found in initial readme commit. Output: {output}"


def test_bad_description_commit_exists():
    """The bad-description commit must be present in the initial bad state."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "description(substring:'WIP: bad description do not merge')"],
        capture_output=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        "jj log failed when searching for bad-description commit"
    )
    output = result.stdout.decode()
    assert "WIP: bad description do not merge" in output, (
        f"Bad description commit not found. Output: {output}"
    )


def test_operation_log_has_entries():
    """Operation log must have entries showing the bad operations."""
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager"],
        capture_output=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj op log failed: {result.stderr.decode()}"
    )
    output = result.stdout.decode()
    assert len(output.strip()) > 0, "Operation log is empty"


def test_initial_readme_commit_description():
    """The 'add initial readme' commit must be visible with jj log."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "description(substring:'add initial readme')"],
        capture_output=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        "Could not find 'add initial readme' commit in log"
    )
    output = result.stdout.decode()
    assert "add initial readme" in output, (
        f"'add initial readme' not found in output: {output}"
    )
