import os
import subprocess

def test_initial_state():
    repo_path = "/home/user/repo"
    assert os.path.exists(repo_path), "Repository directory must exist"
    assert os.path.exists(os.path.join(repo_path, ".jj")), ".jj directory must exist"

    os.chdir(repo_path)
    
    # Check if commits exist
    log_output = subprocess.check_output(["jj", "log", "-T", "description"], text=True)
    assert "Add feature 1" in log_output, "Commit 'Add feature 1' must exist"
    assert "Add feature 2" in log_output, "Commit 'Add feature 2' must exist"
    assert "Add feature 3" in log_output, "Commit 'Add feature 3' must exist"

if __name__ == "__main__":
    test_initial_state()
