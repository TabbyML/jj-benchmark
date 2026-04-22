import os
import subprocess

def run_cmd(cmd, cwd="/home/user/repo"):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
    return result.stdout.strip()

def get_change_id_by_desc(desc):
    log_output = run_cmd(["jj", "log", "--no-graph", "-T", "change_id ++ \"|\" ++ description.first_line() ++ \"\\n\""])
    for line in log_output.splitlines():
        if "|" in line:
            cid, cdesc = line.split("|", 1)
            if desc in cdesc:
                return cid.strip()
    return None

def test_final_state():
    repo_path = "/home/user/repo"
    
    # 1. Verify feature1-docs.txt exists in "Add feature 1"
    feature1_id = get_change_id_by_desc("Add feature 1")
    assert feature1_id, "Could not find 'Add feature 1' commit"
    
    # Check file exists and content
    file_content = run_cmd(["jj", "file", "show", "feature1-docs.txt", "-r", feature1_id])
    assert file_content == "Docs for feature 1", f"Expected 'Docs for feature 1', got '{file_content}'"
    
    # 2. Verify Stack Intact
    feature3_id = get_change_id_by_desc("Add feature 3")
    assert feature3_id, "Could not find 'Add feature 3' commit"
    
    log_output = run_cmd(["jj", "log", "-r", f"{feature1_id}::{feature3_id}", "-T", "description"])
    assert "Add feature 1" in log_output
    assert "Add feature 2" in log_output
    assert "Add feature 3" in log_output
    
    # 3. Verify Tip
    current_parent = run_cmd(["jj", "log", "-r", "@-", "-T", "description"])
    current_self = run_cmd(["jj", "log", "-r", "@", "-T", "description"])
    
    assert "Add feature 3" in current_parent or "Add feature 3" in current_self, "Working copy should be at the tip of the stack (Add feature 3)"

if __name__ == "__main__":
    test_final_state()
