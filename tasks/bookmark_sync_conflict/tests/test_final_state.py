import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_login_bookmark_exists_and_not_conflicted():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-login" in result.stdout, "Bookmark 'feature-login' is missing."
    assert "(conflicted)" not in result.stdout, "Bookmark 'feature-login' is still conflicted."

def test_feature_login_points_to_my_local_commit():
    result = run_jj(["log", "--no-graph", "-r", "feature-login", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "My local commit" in result.stdout, \
        f"Expected 'feature-login' to point to 'My local commit', got: {result.stdout.strip()}"

def test_feature_login_parent_is_coworker_commit():
    result = run_jj(["log", "--no-graph", "-r", "feature-login-", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Coworker commit" in result.stdout, \
        f"Expected parent of 'feature-login' to be 'Coworker commit', got: {result.stdout.strip()}"

def test_feature_login_pushed_to_origin():
    # Fetch first to ensure we see the latest from remote
    fetch_result = run_jj(["git", "fetch"])
    assert fetch_result.returncode == 0, f"jj git fetch failed: {fetch_result.stderr}"
    
    # Check if feature-login and feature-login@origin point to the same commit
    local_rev = run_jj(["log", "--no-graph", "-r", "feature-login", "-T", 'commit_id'])
    assert local_rev.returncode == 0, f"jj log failed: {local_rev.stderr}"
    
    remote_rev = run_jj(["log", "--no-graph", "-r", "feature-login@origin", "-T", 'commit_id'])
    assert remote_rev.returncode == 0, f"jj log failed: {remote_rev.stderr}"
    
    assert local_rev.stdout.strip() == remote_rev.stdout.strip(), \
        f"Local feature-login ({local_rev.stdout.strip()}) does not match feature-login@origin ({remote_rev.stdout.strip()}). The bookmark was not successfully pushed."
