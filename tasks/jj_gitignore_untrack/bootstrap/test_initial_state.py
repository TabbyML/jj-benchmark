import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myrepo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Expected .jj directory at {jj_dir}; not a valid jj repo."


def test_jj_status_exits_cleanly():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj status failed with exit code {result.returncode}.\n"
        f"stderr: {result.stderr}"
    )


def test_src_main_py_exists_and_tracked():
    src_file = os.path.join(REPO_DIR, "src", "main.py")
    assert os.path.isfile(src_file), f"Expected {src_file} to exist as pre-existing tracked file."
    result = subprocess.run(
        ["jj", "file", "list", "-r", "@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/main.py" in result.stdout, (
        "src/main.py should be tracked in the working-copy commit."
    )


def test_build_output_bin_exists_and_tracked():
    build_file = os.path.join(REPO_DIR, "build", "output.bin")
    assert os.path.isfile(build_file), f"Expected {build_file} to exist as pre-existing tracked file."
    result = subprocess.run(
        ["jj", "file", "list", "-r", "@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "build/output.bin" in result.stdout, (
        "build/output.bin should be tracked in the working-copy commit before the task."
    )


def test_no_gitignore_present():
    gitignore_path = os.path.join(REPO_DIR, ".gitignore")
    assert not os.path.isfile(gitignore_path), (
        f".gitignore already exists at {gitignore_path}; it should not exist before the task starts."
    )
