import os
import subprocess
import sys

def test_final_state():
    repo_dir = "/home/user/repo"
    assert os.path.exists(repo_dir), "Repository directory must exist"
    
    os.chdir(repo_dir)
    
    # Check that feature-experiment bookmark exists
    result = subprocess.run(["jj", "log", "-T", "bookmarks", "--no-pager"], capture_output=True, text=True)
    assert result.returncode == 0, "jj log must succeed"
    assert "feature-experiment" in result.stdout, "feature-experiment bookmark must exist"
    
    # Check that feature-experiment is a child of main
    # Find the commit ID of feature-experiment
    result = subprocess.run(["jj", "log", "-r", "feature-experiment", "-T", "commit_id", "--no-pager", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0
    feature_exp_id = result.stdout.strip()
    
    # Find the commit ID of main
    result = subprocess.run(["jj", "log", "-r", "main", "-T", "commit_id", "--no-pager", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0
    main_id = result.stdout.strip()
    
    # Check parents of feature-experiment
    result = subprocess.run(["jj", "log", "-r", "parents(feature-experiment)", "-T", "commit_id\n", "--no-pager", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0
    parents = result.stdout.strip().split()
    assert main_id in parents, f"feature-experiment parent should be main ({main_id}), but found {parents}"
    
    # Check that feature bookmark still exists and hasn't moved (its parent is not main)
    # The original feature's parent was the first commit on main, which is not the current main.
    result = subprocess.run(["jj", "log", "-r", "parents(feature)", "-T", "commit_id", "--no-pager", "--no-graph"], capture_output=True, text=True)
    assert result.returncode == 0
    feature_parent = result.stdout.strip()
    assert feature_parent != main_id, "The original feature bookmark should not be rebased to the new main"

    # Check the content of app.py in feature-experiment
    result = subprocess.run(["jj", "file", "show", "app.py", "-r", "feature-experiment"], capture_output=True, text=True)
    assert result.returncode == 0
    content = result.stdout
    assert "def hello_world():" in content, "feature-experiment should include the hello_world function"

    # Check that utils.py exists in feature-experiment (inherited from main)
    result = subprocess.run(["jj", "file", "show", "utils.py", "-r", "feature-experiment"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "def helper():" in result.stdout, "feature-experiment should include changes from main (utils.py)"

if __name__ == "__main__":
    test_final_state()
    print("Final state validation passed.")
