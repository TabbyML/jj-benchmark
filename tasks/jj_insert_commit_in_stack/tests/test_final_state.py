import os
import subprocess
import pytest

def test_final_state():
    repo_dir = "/home/user/repo"
    
    # 1. Check the history is linear and in the correct order: @, C, B, "Add config", A
    result = subprocess.run(
        ["jj", "log", "-T", "description.first_line() ++ '|'", "--no-graph", "-r", "::@"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    
    lines = result.stdout.strip().split('|')
    
    assert len(lines) >= 6, f"Expected at least 6 elements, got: {lines}"
    
    # Working copy should be empty (no description)
    assert lines[0] == "", "Working copy should be an empty commit with no description"
    assert lines[1] == "C", "The parent of the working copy must be C"
    assert lines[2] == "B", "The parent of C must be B"
    assert lines[3] == "Add config", "The parent of B must be 'Add config'"
    assert lines[4] == "A", "The parent of 'Add config' must be A"
    
    # 2. Check that the working copy is empty
    result_empty = subprocess.run(
        ["jj", "log", "-T", "empty", "--no-graph", "-r", "@"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result_empty.returncode == 0
    assert result_empty.stdout.strip() == "true", "Working copy is not empty"
    
    # 3. Check that 'Add config' contains config.txt with 'base=true'
    result_cat = subprocess.run(
        ["jj", "file", "show", "config.txt", "-r", "description('*Add config*')"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result_cat.returncode == 0, f"config.txt not found in 'Add config' commit. Stderr: {result_cat.stderr}"
    assert result_cat.stdout.strip() == "base=true", f"Expected 'base=true', got '{result_cat.stdout.strip()}'"

    # 4. Check that 'config.txt' also exists in the working copy (inherited)
    assert os.path.exists(os.path.join(repo_dir, "config.txt")), "config.txt does not exist in the working directory"
    with open(os.path.join(repo_dir, "config.txt"), "r") as f:
        content = f.read().strip()
    assert content == "base=true", f"Working copy config.txt has wrong content: {content}"
