import os
import subprocess
import sys

def test_initial_state():
    repo_dir = "/home/user/repo"
    assert os.path.exists(repo_dir), "Repository directory must exist"
    
    os.chdir(repo_dir)
    
    # Check that jj is initialized
    result = subprocess.run(["jj", "log", "-T", "bookmarks", "--no-pager"], capture_output=True, text=True)
    assert result.returncode == 0, "jj log must succeed"
    
    # Check that main and feature bookmarks exist
    output = result.stdout
    assert "main" in output, "main bookmark must exist"
    assert "feature" in output, "feature bookmark must exist"
    
    # Check feature-experiment does not exist
    assert "feature-experiment" not in output, "feature-experiment bookmark must not exist yet"

if __name__ == "__main__":
    test_initial_state()
    print("Initial state validation passed.")
