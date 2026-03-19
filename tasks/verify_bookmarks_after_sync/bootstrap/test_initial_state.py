import subprocess
import os
import sys

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    repo_path = "/home/user/repo"
    remote_path = "/home/user/remote_repo"
    
    if not os.path.isdir(repo_path):
        print(f"Error: Directory {repo_path} does not exist.")
        sys.exit(1)
        
    if not os.path.isdir(remote_path):
        print(f"Error: Directory {remote_path} does not exist.")
        sys.exit(1)

    # Verify repo is a jj repo
    run_cmd("jj root", cwd=repo_path)
    
    # Verify the remote is set
    remotes = run_cmd("jj git remote list", cwd=repo_path)
    if "origin" not in remotes:
        print("Error: origin remote not set.")
        sys.exit(1)

    # Verify feature-x exists
    bookmarks = run_cmd("jj bookmark list feature-x", cwd=repo_path)
    if "feature-x" not in bookmarks:
        print("Error: feature-x bookmark not found.")
        sys.exit(1)

    print("Initial state verification passed.")

if __name__ == "__main__":
    main()
