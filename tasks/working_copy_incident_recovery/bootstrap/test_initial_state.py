import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

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

def test_initial_files_exist_in_parent():
    # check if the parent commit has the files
    result = subprocess.run(
        ["jj", "file", "show", "-r", "@-", "data/cache.bin"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"data/cache.bin not found in parent commit: {result.stderr}"
    
    result = subprocess.run(
        ["jj", "file", "show", "-r", "@-", "scripts/deploy.sh"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"scripts/deploy.sh not found in parent commit: {result.stderr}"
    
    result = subprocess.run(
        ["jj", "file", "show", "-r", "@-", "config/settings.yaml"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"config/settings.yaml not found in parent commit: {result.stderr}"

def test_working_copy_modifications():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    status = result.stdout
    assert "data/cache.bin" in status and "D" in status.split("data/cache.bin")[0].split("\n")[-1], "data/cache.bin should be deleted in working copy"
    assert "scripts/deploy.sh" in status and "M" in status.split("scripts/deploy.sh")[0].split("\n")[-1], "scripts/deploy.sh should be modified in working copy"
    assert "config/settings.yaml" in status and "M" in status.split("config/settings.yaml")[0].split("\n")[-1], "config/settings.yaml should be modified in working copy"
