import subprocess
import os

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result

def test_final_state():
    repo_path = "/home/user/repo"
    
    # Check if we can get the bookmark feature-x
    bookmarks = run_cmd("jj bookmark list feature-x", cwd=repo_path)
    assert bookmarks.returncode == 0, f"Command failed: jj bookmark list feature-x\n{bookmarks.stderr}"
    
    # It should not have (diverged) in the output
    assert "(diverged)" not in bookmarks.stdout, "Error: feature-x is still diverged."
        
    # Get the revision ID of feature-x
    local_rev = run_cmd("jj log -r feature-x -T 'commit_id' --no-graph", cwd=repo_path)
    assert local_rev.returncode == 0, f"Command failed: jj log -r feature-x\n{local_rev.stderr}"
    
    # Get the revision ID of feature-x@origin
    remote_rev = run_cmd("jj log -r feature-x@origin -T 'commit_id' --no-graph", cwd=repo_path)
    assert remote_rev.returncode == 0, f"Command failed: jj log -r feature-x@origin\n{remote_rev.stderr}"
    
    local_id = local_rev.stdout.strip()
    remote_id = remote_rev.stdout.strip()
    
    assert local_id, "Error: Could not determine local revision ID."
    assert remote_id, "Error: Could not determine remote revision ID."
        
    assert local_id == remote_id, f"Error: feature-x ({local_id}) does not point to feature-x@origin ({remote_id})."
