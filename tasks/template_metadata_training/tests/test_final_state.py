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
    
    # 1. Check author of current commit
    author_name = run_cmd(["jj", "log", "-r", "@", "-T", "author.name()", "--no-graph"])
    author_email = run_cmd(["jj", "log", "-r", "@", "-T", "author.email()", "--no-graph"])
    
    if author_name != "Trainer" or author_email != "trainer@example.com":
        print(f"Author is incorrect: {author_name} <{author_email}>")
        sys.exit(1)
        
    # 2. Check template alias
    config = run_cmd(["jj", "config", "get", "template-aliases.training_log"])
    if 'commit_id.short() ++ " - " ++ author.email() ++ " - " ++ description.first_line() ++ "\\n"' not in config and "commit_id.short() ++ ' - ' ++ author.email() ++ ' - ' ++ description.first_line() ++ '\\n'" not in config:
        print(f"Template alias is incorrect: {config}")
        sys.exit(1)
        
    # 3. Check formatted_log.txt
    log_file = "/home/user/repo/formatted_log.txt"
    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist.")
        sys.exit(1)
        
    with open(log_file, "r") as f:
        log_content = f.read().strip().splitlines()
        
    if len(log_content) != 2:
        print(f"Log file has {len(log_content)} lines, expected 2.")
        sys.exit(1)
        
    if "trainer@example.com - WIP commit" not in log_content[0]:
        print(f"First line of log file is incorrect: {log_content[0]}")
        sys.exit(1)
        
    if "default@example.com - Base commit" not in log_content[1]:
        print(f"Second line of log file is incorrect: {log_content[1]}")
        sys.exit(1)
        
    print("Final state is correct.")

if __name__ == "__main__":
    main()
