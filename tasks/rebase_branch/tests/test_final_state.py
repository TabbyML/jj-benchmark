import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_feature_branch_rebased_onto_main():
    """Priority 1: Use jj CLI to verify feature-branch is rebased onto main."""
    result = subprocess.run(
        ["jj", "log", "-r", "main..feature-branch", "--no-graph", "-T", "commit_id\n"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    
    commits = [line for line in result.stdout.strip().split('\n') if line]
    assert len(commits) == 2, f"Expected exactly 2 commits in main..feature-branch, got {len(commits)}: {commits}"

def test_conflict_resolved_content():
    """Priority 1: Use jj CLI to check the content of data.txt in feature-branch."""
    result = subprocess.run(
        ["jj", "file", "show", "data.txt", "-r", "feature-branch"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj file show' failed: {result.stderr}"
    
    expected_content = "Line from main\nLine from feature\n"
    assert result.stdout == expected_content, f"Expected data.txt to contain exactly '{expected_content}', got '{result.stdout}'"

def test_no_unresolved_conflicts():
    """Priority 1: Use jj CLI to verify no unresolved conflicts exist."""
    result = subprocess.run(
        ["jj", "resolve", "--list", "-r", "feature-branch"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    # If there are no conflicts, jj resolve --list returns exit code 2 and an error message
    if result.returncode != 0:
        assert "No conflicts found" in result.stderr or "No conflicts found" in result.stdout, f"Unexpected error from jj resolve: {result.stderr}"
    else:
        assert result.stdout.strip() == "", f"Expected no unresolved conflicts, but found: {result.stdout}"