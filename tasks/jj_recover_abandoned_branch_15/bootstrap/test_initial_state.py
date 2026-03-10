import os
import subprocess
import sys

def test_initial_state():
    repo_dir = os.path.join(os.environ.get("BOOTSTRAP_HOME", "/home/user"), "myrepo")
    
    assert os.path.isdir(repo_dir), "Repository directory should exist"
    
    # Check that main exists
    result = subprocess.run(
        ["jj", "log", "-T", "description", "-r", "main", "--no-pager"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "main bookmark should exist"
    assert "Initial commit" in result.stdout
    
    # Check that feature-login does NOT exist
    result = subprocess.run(
        ["jj", "log", "-r", "feature-login", "--no-pager"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "feature-login bookmark should not exist"

    # Check that the commit was abandoned in the operation log
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert "abandon commit" in result.stdout, "The abandon operation should be in the op log"

    # Try to find the commit by searching op log and then using its ID
    op_log_lines = result.stdout.splitlines()
    abandon_line = next(line for line in op_log_lines if "abandon commit" in line)
    commit_id = abandon_line.split("abandon commit ")[1].strip()

    # Verify we can read the commit description if we explicitly provide the ID
    result = subprocess.run(
        ["jj", "log", "-T", "description", "-r", commit_id, "--no-pager"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert "feat: implement login page" in result.stdout, "The abandoned commit should have the correct description"

if __name__ == "__main__":
    test_initial_state()
    print("Initial state validation passed.")
