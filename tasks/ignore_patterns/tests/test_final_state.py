import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_gitignore_exists_and_contains_log():
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), ".gitignore file does not exist."
    with open(gitignore_path) as f:
        content = f.read()
    assert "*.log" in content, ".gitignore does not contain '*.log'."

def test_debug_log_is_untracked():
    result = subprocess.run(
        ["jj", "-R", PROJECT_DIR, "file", "list"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to list jj files: {result.stderr}"
    assert not any(line.endswith("debug.log") for line in result.stdout.splitlines()), "debug.log is still tracked by jj."

def test_debug_log_exists_on_disk():
    log_path = os.path.join(PROJECT_DIR, "debug.log")
    assert os.path.isfile(log_path), "debug.log was deleted from disk."

def test_gitignore_is_tracked():
    result = subprocess.run(
        ["jj", "-R", PROJECT_DIR, "file", "list"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to list jj files: {result.stderr}"
    assert any(line.endswith(".gitignore") for line in result.stdout.splitlines()), ".gitignore is not tracked by jj."
