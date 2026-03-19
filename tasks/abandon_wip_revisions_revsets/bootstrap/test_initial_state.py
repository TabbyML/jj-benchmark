import os
import subprocess
import pytest


REPO_DIR = "/home/user/mylib"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_jj_subdirectory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(path), f"README.md not found in {REPO_DIR}"


def test_src_lib_rs_exists():
    path = os.path.join(REPO_DIR, "src", "lib.rs")
    assert os.path.isfile(path), f"src/lib.rs not found in {REPO_DIR}"


def test_bookmark_main_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, f"bookmark 'main' not found in output:\n{result.stdout}"


def test_bookmark_feature_core_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/core" in result.stdout, f"bookmark 'feature/core' not found in output:\n{result.stdout}"


def test_wip_revisions_present_initially():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'change_id ++ "\\n"', "-r",
         'mutable() & description("") & ~::bookmarks()'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log revset query failed: {result.stderr}"
    # There should be at least 2 WIP revisions (the two scratch commits)
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) >= 2, (
        f"Expected at least 2 WIP revisions before task, found {len(lines)}.\n"
        f"Output:\n{result.stdout}"
    )
