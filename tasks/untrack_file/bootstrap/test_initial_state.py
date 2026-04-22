import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_env_file_exists():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f"File {env_path} does not exist."
    with open(env_path) as f:
        content = f.read()
    assert "SECRET=" in content, f"Expected {env_path} to contain 'SECRET='."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_env_file_is_tracked():
    result = subprocess.run(
        ["jj", "file", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run 'jj file list'."
    assert ".env" in result.stdout.splitlines(), ".env is not tracked by jj."
