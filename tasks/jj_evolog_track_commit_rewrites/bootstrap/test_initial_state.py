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
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"


def test_working_copy_commit_description():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add authentication module" in result.stdout, (
        f"Expected working-copy commit 'feat: add authentication module' not found. Got: {result.stdout.strip()}"
    )


def test_auth_py_exists():
    auth_py = os.path.join(REPO_DIR, "auth.py")
    assert os.path.isfile(auth_py), f"Expected file auth.py not found in {REPO_DIR}."


def test_evolog_has_predecessors():
    result = subprocess.run(
        ["jj", "evolog", "-r", "@", "--no-graph", "-T", 'change_id ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj evolog failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) >= 3, (
        f"Expected at least 3 evolog entries (current + 2 predecessors), found {len(lines)}."
    )
