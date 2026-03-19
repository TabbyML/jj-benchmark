import os
import subprocess

def test_initial_state():
    repo_path = "/home/user/repo"
    assert os.path.exists(repo_path), "Repository directory should exist"
    
    os.chdir(repo_path)
    
    # Check that main exists
    result = subprocess.run(["jj", "log", "-r", "main", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0, "main branch should exist"
    
    # Check that feature-x does NOT exist
    result = subprocess.run(["jj", "log", "-r", "feature-x", "--no-graph"], capture_output=True, text=True)
    assert result.returncode != 0, "feature-x branch should NOT exist initially"
    
    # Check that there is a commit with description "feature-x work" in the previous operation
    result = subprocess.run(["jj", "log", "--at-op", "@-", "-r", 'description("*feature-x work*")', "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0, "Hidden commit should exist in previous operation"
    assert "feature-x work" in result.stdout, "Hidden commit should have description 'feature-x work'"
