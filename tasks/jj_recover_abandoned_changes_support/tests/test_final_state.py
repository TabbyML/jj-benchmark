import os
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/auth-service"
COMMIT_ID_FILE = "/home/user/workspace/auth-service/recovered_commit_id.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_recovered_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "recovered-login" in result.stdout, "Bookmark 'recovered-login' does not exist."

def test_recovered_commit_contents():
    # Check that the recovered-login bookmark points to a commit containing login.py
    result = run_jj(["file", "show", "login.py", "-r", "recovered-login"])
    assert result.returncode == 0, f"Failed to show login.py at recovered-login: {result.stderr}"
    assert "def login(): pass" in result.stdout, "The file login.py does not contain the expected content in the recovered commit."

def test_recovered_commit_parent_is_main():
    # The parent of recovered-login should be main
    result = run_jj(["log", "--no-graph", "-r", "recovered-login-", "-T", 'bookmarks'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "main" in result.stdout, "The parent of the recovered commit is not the 'main' branch."

def test_recovered_commit_id_file():
    assert os.path.isfile(COMMIT_ID_FILE), f"File {COMMIT_ID_FILE} does not exist."
    with open(COMMIT_ID_FILE, "r") as f:
        commit_id = f.read().strip()
    
    assert commit_id, "The recovered_commit_id.txt file is empty."
    
    # Check that the commit ID in the file actually refers to the original abandoned commit
    # It should have the description 'Add login feature' or contain login.py
    result = run_jj(["log", "--no-graph", "-r", commit_id, "-T", 'description'])
    assert result.returncode == 0, f"Failed to find commit {commit_id} in history. It may not be a valid commit ID."
    assert "Add login feature" in result.stdout, f"The commit ID in the file does not point to the original abandoned commit. Got description: {result.stdout}"
