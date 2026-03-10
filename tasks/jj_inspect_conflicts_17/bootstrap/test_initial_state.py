import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project-alpha"

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

def test_config_yaml_exists_and_is_conflicted():
    config_path = os.path.join(REPO_DIR, "config.yaml")
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "config.yaml" in result.stdout, "config.yaml is not reported as conflicted by jj."
