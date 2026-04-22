import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_first_commit_content():
    """Priority 1: Use jj CLI to verify the grandparent commit (@--)."""
    # Check description
    result_desc = subprocess.run(
        ["jj", "log", "-r", "@--", "--no-graph", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result_desc.returncode == 0, f"jj log failed: {result_desc.stderr}"
    assert result_desc.stdout.strip() == "Add feature A", \
        f"Expected first commit description to be 'Add feature A', got '{result_desc.stdout.strip()}'."
    
    # Check files
    result_diff = subprocess.run(
        ["jj", "diff", "-s", "-r", "@--"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result_diff.returncode == 0, f"jj diff failed: {result_diff.stderr}"
    assert "feature_a.py" in result_diff.stdout, "Expected feature_a.py to be added in the first commit."
    assert "feature_b.py" not in result_diff.stdout, "feature_b.py should not be in the first commit."

def test_second_commit_content():
    """Priority 1: Use jj CLI to verify the parent commit (@-)."""
    # Check description
    result_desc = subprocess.run(
        ["jj", "log", "-r", "@-", "--no-graph", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result_desc.returncode == 0, f"jj log failed: {result_desc.stderr}"
    assert result_desc.stdout.strip() == "Add feature B", \
        f"Expected second commit description to be 'Add feature B', got '{result_desc.stdout.strip()}'."
    
    # Check files
    result_diff = subprocess.run(
        ["jj", "diff", "-s", "-r", "@-"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result_diff.returncode == 0, f"jj diff failed: {result_diff.stderr}"
    assert "feature_b.py" in result_diff.stdout, "Expected feature_b.py to be added in the second commit."
    assert "feature_a.py" not in result_diff.stdout, "feature_a.py should not be in the second commit."

def test_working_copy_empty():
    """Priority 1: Use jj CLI to verify the working copy (@) is empty."""
    result_diff = subprocess.run(
        ["jj", "diff", "-s", "-r", "@"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result_diff.returncode == 0, f"jj diff failed: {result_diff.stderr}"
    assert result_diff.stdout.strip() == "", \
        f"Expected working copy to be empty, but it has changes: {result_diff.stdout}"
