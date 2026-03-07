import os
import subprocess
import pytest


REPO_DIR = "/home/user/project"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["jj", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj not found in PATH: {result.stderr}"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory does not exist: {REPO_DIR}"


def test_jj_repo_dot_jj_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in repo: {jj_dir}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_initial_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial commit" in result.stdout, (
        f"'initial commit' not found in log output: {result.stdout}"
    )


def test_add_config_file_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add config file" in result.stdout, (
        f"'add config file' not found in log output: {result.stdout}"
    )


def test_auth_module_commit_not_in_visible_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add user authentication module" not in result.stdout, (
        "The abandoned commit 'add user authentication module' should not be "
        f"visible in the current log: {result.stdout}"
    )


def test_src_auth_py_not_present():
    auth_path = os.path.join(REPO_DIR, "src", "auth.py")
    assert not os.path.exists(auth_path), (
        f"src/auth.py should not exist before recovery, but found: {auth_path}"
    )


def test_operation_log_has_abandon_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\n'"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "abandon" in result.stdout.lower(), (
        f"Expected an 'abandon' operation in op log, got: {result.stdout}"
    )


def test_config_file_exists():
    config_path = os.path.join(REPO_DIR, "config.toml")
    assert os.path.isfile(config_path), (
        f"config.toml should be present in the repo: {config_path}"
    )


def test_src_directory_exists():
    src_path = os.path.join(REPO_DIR, "src")
    assert os.path.isdir(src_path), (
        f"src/ directory should exist in the repo: {src_path}"
    )
