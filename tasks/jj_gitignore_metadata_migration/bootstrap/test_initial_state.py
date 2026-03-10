import os
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_initial_state():
    repo_dir = os.path.expanduser("~/project")
    
    # Check if directory exists
    if not os.path.isdir(repo_dir):
        print(f"Directory {repo_dir} does not exist.")
        sys.exit(1)
        
    # Check if it's a jj repo
    if not os.path.isdir(os.path.join(repo_dir, ".jj")):
        print(f"Directory {repo_dir} is not a jj repository.")
        sys.exit(1)
        
    # Check if files exist
    for f in ["app.log", "config.local.json", "main.py"]:
        if not os.path.isfile(os.path.join(repo_dir, f)):
            print(f"File {f} does not exist in {repo_dir}.")
            sys.exit(1)
            
    # Check if files are tracked
    res = run_cmd("jj file list", cwd=repo_dir)
    if res.returncode != 0:
        print("Failed to run jj file list")
        sys.exit(1)
        
    tracked_files = res.stdout.splitlines()
    for f in ["app.log", "config.local.json", "main.py"]:
        if f not in tracked_files:
            print(f"File {f} is not tracked by jj.")
            sys.exit(1)
            
    print("Initial state validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    test_initial_state()
