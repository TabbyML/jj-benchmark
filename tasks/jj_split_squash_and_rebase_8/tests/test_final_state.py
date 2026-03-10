import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
RESULT_FILE = "/home/user/result.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_result_file_exists_and_content():
    assert os.path.isfile(RESULT_FILE), f"Result file {RESULT_FILE} not found."
    with open(RESULT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert len(lines) == 3, f"Expected exactly 3 commit descriptions in result.txt, found {len(lines)}"
    assert "add tests" in lines[0], f"Expected top commit to be 'add tests', got {lines[0]}"
    assert "add utils.py" in lines[2], f"Expected bottom commit to be 'add utils.py', got {lines[2]}"

def test_commit_structure_and_files():
    # Get the 3 commits in main..feature
    result = run_jj(["log", "-r", "main..feature", "--no-graph", "-T", "commit_id ++ '\n'"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    commit_ids = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    
    assert len(commit_ids) == 3, f"Expected exactly 3 commits in main..feature, found {len(commit_ids)}"
    
    top_commit = commit_ids[0]
    middle_commit = commit_ids[1]
    bottom_commit = commit_ids[2]
    
    # Check top commit files (should add test_api.py)
    res_top = run_jj(["show", top_commit, "-T", ""])
    assert res_top.returncode == 0
    assert "test_api.py" in res_top.stdout, "Top commit should modify/add test_api.py"
    assert "api.py" not in res_top.stdout, "Top commit should not modify api.py"
    assert "utils.py" not in res_top.stdout, "Top commit should not modify utils.py"
    
    # Check middle commit files (should add api.py)
    res_mid = run_jj(["show", middle_commit, "-T", ""])
    assert res_mid.returncode == 0
    assert "api.py" in res_mid.stdout, "Middle commit should modify/add api.py"
    assert "utils.py" not in res_mid.stdout, "Middle commit should not modify utils.py"
    assert "test_api.py" not in res_mid.stdout, "Middle commit should not modify test_api.py"
    
    # Check bottom commit files (should add utils.py)
    res_bot = run_jj(["show", bottom_commit, "-T", ""])
    assert res_bot.returncode == 0
    assert "utils.py" in res_bot.stdout, "Bottom commit should modify/add utils.py"
    assert "api.py" not in res_bot.stdout, "Bottom commit should not modify api.py"
    assert "test_api.py" not in res_bot.stdout, "Bottom commit should not modify test_api.py"
    
    # Verify the content of utils.py at the bottom commit contains the fix
    res_file = run_jj(["file", "show", "utils.py", "-r", bottom_commit])
    assert res_file.returncode == 0
    assert "def helper(): return False" in res_file.stdout, "Bottom commit utils.py should contain the bug fix from commit 2"

def test_feature_bookmark_position():
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", "description"])
    assert result.returncode == 0
    assert "add tests" in result.stdout, "feature bookmark should point to the 'add tests' commit"
