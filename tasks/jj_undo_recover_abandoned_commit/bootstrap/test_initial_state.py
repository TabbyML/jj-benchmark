import os
import subprocess
import pytest


HOME_DIR = "/home/user"
REPO_DIR = os.path.join(HOME_DIR, "support-repo")


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists_in_initial_commit():
    result = subprocess.run(
        ["jj", "file", "show", "-r", "root()+", "README.md"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"README.md not found in initial commit: {result.stderr}"
    assert "# Support Repo" in result.stdout, (
        f"README.md does not contain expected content. Got: {result.stdout!r}"
    )


def test_abandoned_commit_not_visible_in_default_log():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: patch null pointer dereference in request handler" not in result.stdout, (
        "The abandoned commit should NOT be visible in the default jj log output at initial state"
    )


def test_working_copy_is_empty():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    assert "The working copy is clean" in result.stdout or "no changes" in result.stdout.lower() or "Working copy changes" not in result.stdout, (
        f"Expected working copy to be clean/empty. Status output: {result.stdout!r}"
    )


def test_op_log_has_abandon_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "abandon" in result.stdout.lower(), (
        f"Expected 'abandon' operation in op log. Got: {result.stdout!r}"
    )
