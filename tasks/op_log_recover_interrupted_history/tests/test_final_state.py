import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
INTERRUPTED_OP_FILE = "/home/user/interrupted_op.txt"
RESTORED_COMMIT_FILE = "/home/user/restored_commit.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_login_bookmark_restored():
    result = run_jj(["log", "--no-graph", "-r", "feature-login", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Finish feature-login" in result.stdout, \
        f"Expected 'feature-login' bookmark to point to 'Finish feature-login', but got: {result.stdout.strip()}"

def test_interrupted_op_file_exists_and_correct():
    assert os.path.exists(INTERRUPTED_OP_FILE), f"File {INTERRUPTED_OP_FILE} does not exist."
    with open(INTERRUPTED_OP_FILE, "r") as f:
        op_id = f.read().strip()
    assert op_id, f"File {INTERRUPTED_OP_FILE} is empty."

    # Verify the operation ID actually exists in the op log and has "rebase" in its description
    result = run_jj(["op", "log", "--no-graph"])
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert op_id in result.stdout, f"Operation ID {op_id} from {INTERRUPTED_OP_FILE} not found in jj op log."
    
    # Check if the operation was a rebase by looking at the specific operation
    op_result = run_jj(["op", "log", "--no-graph", "--at-op", op_id, "-T", 'description'])
    assert op_result.returncode == 0, f"jj op log for op {op_id} failed: {op_result.stderr}"
    assert "rebase" in op_result.stdout.lower(), f"Operation {op_id} does not appear to be a rebase operation."

def test_restored_commit_file_exists_and_correct():
    assert os.path.exists(RESTORED_COMMIT_FILE), f"File {RESTORED_COMMIT_FILE} does not exist."
    with open(RESTORED_COMMIT_FILE, "r") as f:
        commit_id = f.read().strip()
    assert commit_id, f"File {RESTORED_COMMIT_FILE} is empty."

    # Verify the commit ID matches the current feature-login bookmark
    result = run_jj(["log", "--no-graph", "-r", "feature-login", "-T", 'commit_id'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    actual_commit_id = result.stdout.strip()
    
    # jj commit IDs can be prefixes, so check if the file content matches the start of the actual commit ID
    assert actual_commit_id.startswith(commit_id), \
        f"Commit ID in {RESTORED_COMMIT_FILE} ({commit_id}) does not match the actual 'feature-login' commit ID ({actual_commit_id})."
