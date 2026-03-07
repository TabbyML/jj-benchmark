import os
import subprocess

import pytest

REPO_DIR = "/home/user/workspace"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory not found: {REPO_DIR}"


def test_jj_directory_exists():
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


def test_server_py_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "server.py" in result.stdout, (
        f"src/server.py not listed as conflicted.\njj resolve --list output:\n{result.stdout}"
    )


def test_routes_py_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "routes.py" in result.stdout, (
        f"src/routes.py not listed as conflicted.\njj resolve --list output:\n{result.stdout}"
    )


def test_bookmark_main_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Bookmark 'main' not found in repository"


def test_bookmark_feature_api_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-api" in result.stdout, (
        "Bookmark 'feature-api' not found in repository"
    )


def test_bookmark_feature_logging_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-logging" in result.stdout, (
        "Bookmark 'feature-logging' not found in repository"
    )


def test_working_copy_is_merge_commit():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "parents.len()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "2" in result.stdout, (
        "Working copy commit does not have 2 parents (expected merge commit)"
    )


def test_working_copy_has_conflict_flag():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "conflict"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "true" in result.stdout.lower(), (
        f"Working copy commit is not marked as conflicted.\nGot: {result.stdout!r}"
    )
