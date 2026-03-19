import os
import subprocess

def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_initial_state():
    repo_dir = "/home/user/repo"
    
    assert os.path.exists(repo_dir), f"Repository directory {repo_dir} does not exist."
    assert os.path.exists(os.path.join(repo_dir, ".jj")), f"{repo_dir} is not a jj repository."
        
    res = run_command("jj bookmark list -T 'name ++ \"\\n\"'", cwd=repo_dir)
    assert "main" in res.stdout, "'main' bookmark not found."
    assert "feature-x" in res.stdout, "'feature-x' bookmark not found."
    assert "bugfix-y" not in res.stdout, "'bugfix-y' bookmark should not exist yet."
