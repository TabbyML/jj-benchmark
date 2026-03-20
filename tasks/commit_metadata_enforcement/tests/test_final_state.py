import os
import subprocess
import pytest

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_final_state():
    home_dir = os.environ.get("BOOTSTRAP_HOME", "/home/user")
    repo_dir = os.path.join(home_dir, "repo")
    log_output_file = os.path.join(home_dir, "log_output.txt")
    
    # 1. Check config
    res = run_cmd("jj config get templates.log", cwd=repo_dir)
    assert res.returncode == 0, "Error: templates.log is not configured."
        
    template_val = res.stdout.strip()
    assert 'commit_id.short()' in template_val, "templates.log does not contain commit_id.short()"
    assert 'author.email()' in template_val, "templates.log does not contain author.email()"
    assert 'description.first_line()' in template_val, "templates.log does not contain description.first_line()"
        
    # 2. Check commit description
    res = run_cmd("jj log -r @ -T 'description'", cwd=repo_dir)
    assert "Update metadata policy" in res.stdout, "Current commit does not have the description 'Update metadata policy'."
        
    # 3. Check log_output.txt
    assert os.path.exists(log_output_file), f"Error: {log_output_file} does not exist."
        
    with open(log_output_file, "r") as f:
        log_content = f.read().strip()
        
    # It should look like: abc1234 | test@example.com | Update metadata policy
    assert " | " in log_content, "Error: log_output.txt does not contain the separator ' | '."
        
    parts = log_content.split(" | ")
    assert len(parts) >= 3, "Error: log_output.txt does not contain all required fields separated by ' | '."
        
    assert "test@example.com" in parts[1], "Error: log_output.txt does not contain the correct email."
    assert "Update metadata policy" in parts[2], "Error: log_output.txt does not contain the correct description."
