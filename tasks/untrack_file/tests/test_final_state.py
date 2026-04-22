import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_env_file_exists():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), "The .env file was deleted! It should remain on the filesystem."
    with open(env_path) as f:
        content = f.read()
    assert "SECRET=" in content, "The .env file content was modified."

def test_env_in_gitignore():
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), ".gitignore file does not exist."
    with open(gitignore_path) as f:
        content = f.read().splitlines()
    assert ".env" in content, ".env is not in .gitignore."

def test_env_not_tracked_by_jj():
    result = subprocess.run(
        ["jj", "file", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run 'jj file list'."
    tracked_files = result.stdout.splitlines()
    assert ".env" not in tracked_files, ".env is still tracked by jj."
