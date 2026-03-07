import os
import subprocess

def test_final_state():
    repo_path = "/home/user/repo"
    assert os.path.exists(repo_path), "Repository directory should exist"
    
    os.chdir(repo_path)
    
    # Check that feature-x exists
    result = subprocess.run(["jj", "log", "-r", "feature-x", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0, "feature-x branch should exist"
    
    # Check that feature-x is a child of main
    result = subprocess.run(["jj", "log", "-r", "feature-x", "--no-graph", "-T", "parents.map(|c| c.bookmarks()).join(', ')"], capture_output=True, text=True)
    assert "main" in result.stdout, "feature-x should be a child of main"
    
    # Check that log.txt exists
    log_path = "/home/user/log.txt"
    assert os.path.exists(log_path), "log.txt should exist"
    
    with open(log_path, "r") as f:
        log_content = f.read()
        assert "feature-x work" in log_content, "log.txt should contain 'feature-x work'"
