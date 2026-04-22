import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_commit_b_description_updated():
    """Priority 1: Use jj CLI to verify the description of the commit with b.txt."""
    result = subprocess.run(
        ["jj", "log", "-r", "files(\"b.txt\")", "--no-graph", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "Add second file" in result.stdout, \
        f"Expected description 'Add second file' for commit with b.txt, got: {result.stdout}"

def test_working_copy_description_updated():
    """Priority 1: Use jj CLI to verify the description of the working copy."""
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "Add file D" in result.stdout, \
        f"Expected description 'Add file D' for working copy, got: {result.stdout}"

def test_d_txt_exists_and_content():
    """Priority 3 fallback: basic file existence and content check."""
    d_txt_path = os.path.join(PROJECT_DIR, "d.txt")
    assert os.path.isfile(d_txt_path), f"d.txt not found at {d_txt_path}"
    with open(d_txt_path, "r") as f:
        content = f.read().strip()
    assert content == "d", f"Expected content 'd' in d.txt, got: '{content}'"

def test_commit_c_still_exists():
    """Priority 1: Use jj CLI to verify the commit with c.txt still exists and has correct description."""
    result = subprocess.run(
        ["jj", "log", "-r", "files(\"c.txt\")", "--no-graph", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "Add file C" in result.stdout, \
        f"Expected description 'Add file C' for commit with c.txt, got: {result.stdout}"
