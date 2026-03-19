import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"

def run_cmd(args):
    return subprocess.run(args, cwd=REPO_DIR, capture_output=True, text=True)

def test_dot_jj_directory_exists():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."

def test_app_py_has_migrate_function():
    app_py_path = os.path.join(REPO_DIR, "app.py")
    with open(app_py_path, "r") as f:
        content = f.read()
    assert "def migrate():" in content, "The 'migrate' function was not found in app.py."

def test_jj_bookmark_exists_and_points_to_migrate():
    # Check if the bookmark exists
    result = run_cmd(["jj", "bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "jj-migration" in result.stdout, "The bookmark 'jj-migration' does not exist in jj."
    
    # Check if the bookmark points to a commit that has the 'migrate' function
    # We can check the diff of the commit pointed to by the bookmark
    diff_result = run_cmd(["jj", "diff", "-r", "jj-migration"])
    assert diff_result.returncode == 0, f"jj diff failed: {diff_result.stderr}"
    assert "def migrate():" in diff_result.stdout, "The commit pointed to by 'jj-migration' does not contain the 'migrate' function."

def test_git_branch_exists():
    result = run_cmd(["git", "branch"])
    assert result.returncode == 0, f"git branch failed: {result.stderr}"
    assert "jj-migration" in result.stdout, "The Git branch 'jj-migration' does not exist."

def test_git_branch_points_to_same_commit_as_jj_bookmark():
    # Get the git commit hash for the branch
    git_result = run_cmd(["git", "rev-parse", "jj-migration"])
    assert git_result.returncode == 0, f"git rev-parse failed: {git_result.stderr}"
    git_hash = git_result.stdout.strip()
    
    # Get the jj commit hash for the bookmark (in git format)
    jj_result = run_cmd(["jj", "log", "--no-graph", "-r", "jj-migration", "-T", "commit_id"])
    assert jj_result.returncode == 0, f"jj log failed: {jj_result.stderr}"
    jj_hash = jj_result.stdout.strip()
    
    assert git_hash == jj_hash, f"Git branch and jj bookmark do not point to the same commit. Git: {git_hash}, jj: {jj_hash}"
