import os
import subprocess

def test_final_state():
    repo_dir = "/home/user/repo"
    feature_dir = "/home/user/feature-workspace"
    
    assert os.path.isdir(repo_dir), "Original repository directory should still exist"
    assert os.path.isdir(feature_dir), "Feature workspace directory should still exist"
    
    # Check if the feature file was created and contains the right content
    feature_file_path = os.path.join(feature_dir, "feature.txt")
    assert os.path.isfile(feature_file_path), "feature.txt should be created in the feature workspace"
    with open(feature_file_path, "r") as f:
        content = f.read().strip()
        assert content == "new feature", f"Expected 'new feature', got '{content}'"
    
    # Check if the workspace is forgotten
    result = subprocess.run(["jj", "workspace", "list"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, "jj workspace list should succeed"
    assert "feature-workspace:" not in result.stdout, "The feature-workspace should be forgotten"
    
    # Check if the commit was made
    result = subprocess.run(["jj", "log", "-T", "description", "-r", "all()"], cwd=repo_dir, capture_output=True, text=True)
    assert "Add feature" in result.stdout, "The commit 'Add feature' should be in the repository history"
    
    print("Final state verification passed.")

if __name__ == "__main__":
    test_final_state()