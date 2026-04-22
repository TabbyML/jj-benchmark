import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_file_content():
    file_path = os.path.join(PROJECT_DIR, "base.txt")
    with open(file_path) as f:
        content = f.read().strip()
    assert content == "new", f"Expected 'new', got '{content}'."

def test_jj_log():
    result = subprocess.run(["jj", "log", "-T", "description"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "Commit 3" in result.stdout, "Expected 'Commit 3' in jj log."
    assert "Commit 2" in result.stdout, "Expected 'Commit 2' in jj log."
    assert "Commit 1" in result.stdout, "Expected 'Commit 1' in jj log."
    assert "Base" in result.stdout, "Expected 'Base' in jj log."
