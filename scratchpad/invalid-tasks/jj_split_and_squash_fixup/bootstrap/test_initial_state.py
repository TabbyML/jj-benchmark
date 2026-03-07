import os
import subprocess
import pytest

REPO_DIR = "/home/user/myproject"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_jj_metadata_exists():
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


def test_bundled_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", "description(substring:\"add README and config\")"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add README and config" in result.stdout, (
        "Expected commit 'add README and config' not found in log"
    )


def test_fixup_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", "description(substring:\"fixup: correct typo in README\")"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fixup: correct typo in README" in result.stdout, (
        "Expected fixup commit not found in log"
    )


def test_readme_file_in_bundled_commit():
    result = subprocess.run(
        ["jj", "file", "list",
         "-r", "description(substring:\"add README and config\")"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "README.md" in result.stdout


def test_config_file_in_bundled_commit():
    result = subprocess.run(
        ["jj", "file", "list",
         "-r", "description(substring:\"add README and config\")"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "config.toml" in result.stdout
