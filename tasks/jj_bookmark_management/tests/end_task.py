import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_log_file_exists():
    log_path = os.path.join(REPO_DIR, "repo_state.log")
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

def test_current_revision_description():
    result = run_jj(["log", "-r", "@", "--no-graph", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    description = result.stdout.strip()
    assert "feat: refine auth logic" in description, f"Expected description 'feat: refine auth logic', got '{description}'"

def test_auth_feature_bookmark_position():
    # Get commit ID of auth-feature
    res_bm = run_jj(["log", "-r", "auth-feature", "--no-graph", "-T", "commit_id"])
    assert res_bm.returncode == 0, f"jj log for auth-feature failed: {res_bm.stderr}"
    bm_id = res_bm.stdout.strip()
    
    # Get commit ID of @
    res_wc = run_jj(["log", "-r", "@", "--no-graph", "-T", "commit_id"])
    assert res_wc.returncode == 0, f"jj log for @ failed: {res_wc.stderr}"
    wc_id = res_wc.stdout.strip()
    
    assert bm_id == wc_id, f"Bookmark 'auth-feature' ({bm_id}) does not point to working copy ({wc_id})"

def test_backup_bookmark_description():
    result = run_jj(["log", "-r", "auth-backup", "--no-graph", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    description = result.stdout.strip()
    assert "feat: basic auth" in description, f"Expected 'auth-backup' to point to commit with description 'feat: basic auth', got '{description}'"

def test_graph_structure():
    # Verify auth-backup is a parent of auth-feature
    # We check the bookmarks of the parents of auth-feature
    result = run_jj(["log", "-r", "parents(auth-feature)", "--no-graph", "-T", "bookmarks"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    parents_bookmarks = result.stdout.strip()
    assert "auth-backup" in parents_bookmarks, f"Expected 'auth-backup' to be a parent of 'auth-feature'. Parent bookmarks found: '{parents_bookmarks}'"
