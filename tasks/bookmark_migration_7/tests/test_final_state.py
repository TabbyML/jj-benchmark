import os
import subprocess

def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_final_state():
    repo_dir = "/home/user/repo"
    verification_log = "/home/user/bookmark_verification.log"
    
    assert os.path.exists(verification_log), f"Verification log {verification_log} not found."
        
    with open(verification_log, "r") as f:
        log_content = f.read()
        
    assert "feature-x" in log_content, "'feature-x' not found in verification log."
        
    res = run_command("jj bookmark list -T 'name ++ \"\\n\"'", cwd=repo_dir)
    assert "feature-x" in res.stdout, "'feature-x' bookmark not found."
    assert "bugfix-y" in res.stdout, "'bugfix-y' bookmark not found."
