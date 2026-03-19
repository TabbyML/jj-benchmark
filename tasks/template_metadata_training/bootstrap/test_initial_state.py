import os
import subprocess
import sys

def run_cmd(cmd, cwd="/home/user/repo"):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    repo_dir = "/home/user/repo"
    if not os.path.exists(repo_dir):
        print(f"Repo dir {repo_dir} does not exist.")
        sys.exit(1)

    # Check jj repo
    if not os.path.exists(os.path.join(repo_dir, ".jj")):
        print(f"Not a jj repo: {repo_dir}")
        sys.exit(1)

    # Check commits
    log = run_cmd(["jj", "log", "-T", "coalesce(description.first_line(), '') ++ '\n'", "--no-graph"], cwd=repo_dir).splitlines()
    if "WIP commit" not in log:
        print("Missing WIP commit")
        sys.exit(1)
    if "Base commit" not in log:
        print("Missing Base commit")
        sys.exit(1)

    print("Initial state is correct.")

if __name__ == "__main__":
    main()
