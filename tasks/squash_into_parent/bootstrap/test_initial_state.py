import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f".jj directory missing in {REPO_DIR}."
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_makefile_exists():
    path = os.path.join(REPO_DIR, "Makefile")
    assert os.path.isfile(path), "Makefile not found."


def test_makefile_has_errors_only():
    path = os.path.join(REPO_DIR, "Makefile")
    content = open(path).read()
    assert "pylint --errors-only src/" in content, "Makefile missing 'pylint --errors-only src/'."


def test_initial_commit_descriptions():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "build: add base Makefile" in log, "'build: add base Makefile' not found."
    assert "build: add lint target" in log, "'build: add lint target' not found."
    assert "wip: fixup lint flag" in log, "'wip: fixup lint flag' not found."


def test_working_copy_is_fixup():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: fixup lint flag" in result.stdout, f"Expected working copy 'wip: fixup lint flag', got: {result.stdout.strip()}"
