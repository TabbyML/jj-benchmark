import os
import subprocess
import pytest

def test_initial_state():
    repo_dir = "/home/user/repo"
    
    # Check if the repository exists
    assert os.path.exists(os.path.join(repo_dir, ".jj")), "Repository not found at /home/user/repo"
    
    # Check the commit history
    result = subprocess.run(
        ["jj", "log", "-T", "description.first_line() ++ '|'", "--no-graph", "-r", "::@"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    
    lines = result.stdout.strip().split('|')
    # The output from jj log with --no-graph for linear history is from top to bottom
    # So we expect: "", "C", "B", "A", "" (root)
    assert len(lines) >= 5, f"Expected at least 5 elements, got: {lines}"
    
    assert lines[0] == "", "Expected working copy to be empty (no description)"
    assert lines[1] == "C", "Expected commit C"
    assert lines[2] == "B", "Expected commit B"
    assert lines[3] == "A", "Expected commit A"
