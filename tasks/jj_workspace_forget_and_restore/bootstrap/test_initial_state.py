import os
import subprocess

def test_initial_state():
    repo_dir = "/home/user/repo"
    assert os.path.isdir(repo_dir), "Repository directory should exist"
    
    # Check it's a jj repo
    result = subprocess.run(["jj", "status"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, "Should be a valid jj repository"
    
    # Check workspaces
    result = subprocess.run(["jj", "workspace", "list"], cwd=repo_dir, capture_output=True, text=True)
    assert "default:" in result.stdout, "Should have a default workspace"
    assert "feature-workspace:" not in result.stdout, "Should not have feature-workspace yet"
    
    print("Initial state verification passed.")

if __name__ == "__main__":
    test_initial_state()