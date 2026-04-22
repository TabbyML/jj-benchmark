import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_app_log_is_tracked():
    result = subprocess.run(
        ["jj", "file", "list", "-r", "@-"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "app.log" in result.stdout, "Expected app.log to be tracked in the previous commit (@-)."

def test_gitignore_unchanged():
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), f".gitignore file {gitignore_path} does not exist."
    with open(gitignore_path) as f:
        content = f.read()
    assert "*.log" in content, "Expected .gitignore to contain '*.log'."

def test_commit_message():
    result = subprocess.run(
        ["jj", "log", "-r", "@-", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "Track log file" in result.stdout, f"Expected commit description to contain 'Track log file', got: {result.stdout}"
