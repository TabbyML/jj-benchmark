import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_feature_is_rebased_onto_main():
    # Verify that 'feature' bookmark's parent is 'main'
    result = subprocess.run(
        ["jj", "log", "-r", "feature", "--no-graph", "-T", "parents.map(|p| p.bookmarks()).join(',')"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, f"Failed to get jj log: {result.stderr}"
    
    # The output should contain 'main', meaning the parent of feature has the 'main' bookmark
    assert "main" in result.stdout, f"Expected 'feature' to be rebased onto 'main'. Output: {result.stdout}"
