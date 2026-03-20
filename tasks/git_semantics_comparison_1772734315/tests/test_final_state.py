import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_git_branch_bookmark():
    result = run_jj(["log", "--no-graph", "-r", "git_branch", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add git semantics" in result.stdout, "Expected commit description 'add git semantics' for bookmark 'git_branch'."

def test_jj_branch_bookmark():
    result = run_jj(["log", "--no-graph", "-r", "jj_branch", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add jj semantics" in result.stdout, "Expected commit description 'add jj semantics' for bookmark 'jj_branch'."

def test_git_semantics_file():
    result = run_jj(["file", "show", "git_semantics.txt", "-r", "git_branch"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "git semantics" in result.stdout, "File git_semantics.txt does not contain 'git semantics'."

def test_jj_semantics_file():
    result = run_jj(["file", "show", "jj_semantics.txt", "-r", "jj_branch"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "jj semantics" in result.stdout, "File jj_semantics.txt does not contain 'jj semantics'."

def test_git_export():
    git_branch_path = os.path.join(REPO_DIR, ".git", "refs", "heads", "git_branch")
    jj_branch_path = os.path.join(REPO_DIR, ".git", "refs", "heads", "jj_branch")
    assert os.path.isfile(git_branch_path), "git_branch was not exported to git."
    assert os.path.isfile(jj_branch_path), "jj_branch was not exported to git."

def test_comparison_log():
    log_file = "/home/user/comparison_log.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} not found."
    with open(log_file, "r") as f:
        content = f.read()
    assert "add git semantics" in content, "Log file missing git_branch commit."
    assert "add jj semantics" in content, "Log file missing jj_branch commit."
