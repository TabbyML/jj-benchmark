import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f".jj directory missing in {REPO_DIR}."
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "bookmark 'main' not found."


def test_helper_py_exists():
    path = os.path.join(REPO_DIR, "helper.py")
    assert os.path.isfile(path), "helper.py not found in working directory."


def test_working_copy_is_feat_add_helper():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add helper" in result.stdout, (
        f"Working copy should be 'feat: add helper', got: {result.stdout.strip()}"
    )


def test_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: project setup" in result.stdout, "'chore: project setup' not found in log."
    assert "feat: add helper" in result.stdout, "'feat: add helper' not found in log."


def test_working_copy_based_on_root():
    """Before rebase: @ should be based on root() — exactly 1 commit above root."""
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "root()..@", "-T", 'description ++ "\\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descs) == 1, (
        f"Expected exactly 1 commit above root() before rebase, found {len(descs)}: {descs}"
    )
