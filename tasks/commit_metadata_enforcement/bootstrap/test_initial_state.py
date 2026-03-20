import os
import subprocess
import pytest

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_initial_state():
    home_dir = os.environ.get("BOOTSTRAP_HOME", "/home/user")
    repo_dir = os.path.join(home_dir, "repo")
    
    assert os.path.exists(repo_dir), f"Error: {repo_dir} does not exist."
    assert os.path.exists(os.path.join(repo_dir, ".jj")), f"Error: {repo_dir} is not a jj repository."
        
    # Check that the default log template is still the original one
    res = run_cmd("jj log -r @ --no-graph", cwd=repo_dir)
    assert "|" not in res.stdout, "Error: custom template already configured."
