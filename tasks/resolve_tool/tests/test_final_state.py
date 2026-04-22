import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_no_unresolved_conflicts():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "conflict" not in result.stdout, "Expected no unresolved conflicts."
    assert "file1.txt" not in result.stdout or "file1.txt" in result.stdout, "Expected file1.txt to be resolved."

def test_file1_resolved_with_ours():
    file1_path = os.path.join(PROJECT_DIR, "file1.txt")
    with open(file1_path) as f:
        content = f.read().strip()
    assert content == "side 1", f"Expected file1.txt to have content 'side 1', got: {content}"

def test_file2_resolved_with_theirs():
    file2_path = os.path.join(PROJECT_DIR, "file2.txt")
    with open(file2_path) as f:
        content = f.read().strip()
    assert content == "side 2", f"Expected file2.txt to have content 'side 2', got: {content}"
