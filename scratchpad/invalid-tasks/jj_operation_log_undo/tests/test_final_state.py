import os
import subprocess
import pytest


REPO_DIR = "/home/user/project"


def test_auth_module_commit_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add user authentication module" in result.stdout, (
        "Expected 'add user authentication module' to be visible in jj log after recovery, "
        f"but got: {result.stdout}"
    )


def test_src_auth_py_exists():
    auth_path = os.path.join(REPO_DIR, "src", "auth.py")
    assert os.path.isfile(auth_path), (
        f"src/auth.py should exist after recovery, but was not found at: {auth_path}"
    )


def test_src_auth_py_contains_authenticate_function():
    auth_path = os.path.join(REPO_DIR, "src", "auth.py")
    with open(auth_path, "r") as f:
        content = f.read()
    assert "def authenticate" in content, (
        f"src/auth.py should contain 'def authenticate', but contents are: {content}"
    )


def test_op_log_has_undo_or_revert_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\n'"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    output_lower = result.stdout.lower()
    assert "undo" in output_lower or "revert" in output_lower, (
        "Expected an 'undo' or 'revert' operation in op log after recovery, "
        f"but got: {result.stdout}"
    )


def test_three_named_commits_exist():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial commit" in result.stdout, (
        f"'initial commit' not found in log: {result.stdout}"
    )
    assert "add config file" in result.stdout, (
        f"'add config file' not found in log: {result.stdout}"
    )
    assert "add user authentication module" in result.stdout, (
        f"'add user authentication module' not found in log: {result.stdout}"
    )


def test_op_log_most_recent_is_undo():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\n'", "--limit", "1"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    output_lower = result.stdout.lower()
    assert "undo" in output_lower or "revert" in output_lower, (
        "The most recent operation in op log should be an undo/revert, "
        f"but got: {result.stdout}"
    )
