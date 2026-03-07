import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myrepo"


def _jj(*args, cwd=REPO_DIR):
    """Run a jj command in the repo and return CompletedProcess."""
    return subprocess.run(
        ["jj"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_gitignore_file_exists():
    gitignore_path = os.path.join(REPO_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), (
        f".gitignore does not exist at {gitignore_path}. "
        "The user must create a .gitignore file with the build/ pattern."
    )


def test_gitignore_contains_build_pattern():
    gitignore_path = os.path.join(REPO_DIR, ".gitignore")
    with open(gitignore_path) as fh:
        contents = fh.read()
    lines = [line.strip() for line in contents.splitlines()]
    assert "build/" in lines, (
        f".gitignore must contain 'build/' pattern. "
        f"Actual contents: {repr(contents)}"
    )


def test_build_output_bin_still_on_disk():
    build_file = os.path.join(REPO_DIR, "build", "output.bin")
    assert os.path.isfile(build_file), (
        f"build/output.bin should still exist on disk at {build_file}. "
        "Untracking a file does not delete it from the filesystem."
    )


def test_build_output_bin_not_tracked():
    result = _jj("file", "list", "-r", "@")
    assert result.returncode == 0, (
        f"jj file list failed with exit code {result.returncode}.\nstderr: {result.stderr}"
    )
    assert "build/output.bin" not in result.stdout, (
        f"build/output.bin should NOT be tracked in the working-copy commit. "
        f"jj file list output: {result.stdout}"
    )
    assert "build/" not in result.stdout, (
        f"No build/ path should be tracked in the working-copy commit. "
        f"jj file list output: {result.stdout}"
    )


def test_src_main_py_still_tracked():
    result = _jj("file", "list", "-r", "@")
    assert result.returncode == 0, (
        f"jj file list failed with exit code {result.returncode}.\nstderr: {result.stderr}"
    )
    assert "src/main.py" in result.stdout, (
        f"src/main.py must remain tracked in the working-copy commit. "
        f"jj file list output: {result.stdout}"
    )


def test_gitignore_tracked():
    result = _jj("file", "list", "-r", "@")
    assert result.returncode == 0, (
        f"jj file list failed with exit code {result.returncode}.\nstderr: {result.stderr}"
    )
    assert ".gitignore" in result.stdout, (
        f".gitignore should be tracked in the working-copy commit. "
        f"jj file list output: {result.stdout}"
    )


def test_jj_status_does_not_show_build_artifact():
    result = _jj("status")
    assert result.returncode == 0, (
        f"jj status failed with exit code {result.returncode}.\nstderr: {result.stderr}"
    )
    assert "build/output.bin" not in result.stdout, (
        f"jj status must NOT show build/output.bin. "
        f"jj status output: {result.stdout}"
    )
