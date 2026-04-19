import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_dir_exists():
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".jj")), ".jj directory not found in project directory."

def test_git_dir_exists():
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".git")), ".git directory not found in project directory."

def test_jj_config_user_name():
    result = subprocess.run(
        ["jj", "config", "get", "user.name"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj config get user.name' failed: {result.stderr}"
    assert "Test User" in result.stdout, f"Expected user.name to be 'Test User', got: {result.stdout}"

def test_jj_config_user_email():
    result = subprocess.run(
        ["jj", "config", "get", "user.email"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj config get user.email' failed: {result.stderr}"
    assert "test@example.com" in result.stdout, f"Expected user.email to be 'test@example.com', got: {result.stdout}"
