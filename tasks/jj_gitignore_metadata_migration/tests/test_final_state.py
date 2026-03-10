import os
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_final_state():
    repo_dir = os.path.expanduser("~/project")
    
    # 1. Check if files still exist on disk
    for f in ["app.log", "config.local.json", "main.py"]:
        if not os.path.isfile(os.path.join(repo_dir, f)):
            print(f"File {f} does not exist on disk.")
            sys.exit(1)
            
    # 2. Check if app.log and config.local.json are untracked
    res = run_cmd("jj file list", cwd=repo_dir)
    if res.returncode != 0:
        print("Failed to run jj file list")
        sys.exit(1)
        
    tracked_files = res.stdout.splitlines()
    for f in ["app.log", "config.local.json"]:
        if f in tracked_files:
            print(f"File {f} is still tracked by jj.")
            sys.exit(1)
            
    # Check if main.py is still tracked
    if "main.py" not in tracked_files:
        print("main.py is not tracked by jj.")
        sys.exit(1)
        
    # 3. Check if .gitignore exists and contains the patterns
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    if not os.path.isfile(gitignore_path):
        print(".gitignore does not exist.")
        sys.exit(1)
        
    with open(gitignore_path, "r") as f:
        content = f.read()
        if "*.log" not in content or "*.local.json" not in content:
            print(".gitignore does not contain required patterns.")
            sys.exit(1)
            
    # 4. Check if bookmark ignore-cleanup exists
    res = run_cmd("jj bookmark list ignore-cleanup", cwd=repo_dir)
    if res.returncode != 0 or "ignore-cleanup" not in res.stdout:
        print("Bookmark ignore-cleanup does not exist.")
        sys.exit(1)
        
    # 5. Check commit message for ignore-cleanup
    res = run_cmd("jj log -T description -r ignore-cleanup --no-graph", cwd=repo_dir)
    if res.returncode != 0:
        print("Failed to get commit description for ignore-cleanup")
        sys.exit(1)
    
    if "chore: ignore log and local config files" not in res.stdout:
        print(f"Commit message is incorrect. Got: {res.stdout.strip()}")
        sys.exit(1)
        
    # 6. Check bookmark_commit.txt
    bookmark_commit_path = os.path.join(repo_dir, "bookmark_commit.txt")
    if not os.path.isfile(bookmark_commit_path):
        print("bookmark_commit.txt does not exist.")
        sys.exit(1)
        
    with open(bookmark_commit_path, "r") as f:
        saved_commit = f.read().strip()
        
    # Get actual commit ID of ignore-cleanup
    res = run_cmd("jj log -T commit_id -r ignore-cleanup --no-graph", cwd=repo_dir)
    actual_commit = res.stdout.strip()
    
    if saved_commit != actual_commit:
        print(f"Saved commit ID {saved_commit} does not match actual {actual_commit}.")
        sys.exit(1)
        
    print("Final state validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    test_final_state()
