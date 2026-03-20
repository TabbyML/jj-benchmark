import os
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/repo"
FINAL_LOG_FILE = "/home/user/workspace/final_log.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_stack_bookmark_points_to_correct_commit():
    result = run_jj(["log", "--no-graph", "-r", "feature-stack", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Add feature B" in result.stdout, f"Expected feature-stack to point to 'Add feature B', got: {result.stdout}"

def test_feature_stack_commit_contents():
    # Check that feature-stack only modifies feature_b.py relative to its parent
    result = run_jj(["diff", "-r", "feature-stack", "--summary"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert "feature_b.py" in result.stdout, "feature_b.py should be modified in the feature-stack commit."
    assert "feature_a.py" not in result.stdout, "feature_a.py should NOT be modified in the feature-stack commit."

def test_parent_of_feature_stack_description():
    result = run_jj(["log", "--no-graph", "-r", "feature-stack-", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Add feature A complete" in result.stdout, f"Expected parent of feature-stack to have description 'Add feature A complete', got: {result.stdout}"

def test_parent_of_feature_stack_contents():
    result = run_jj(["diff", "-r", "feature-stack-", "--summary"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert "feature_a.py" in result.stdout, "feature_a.py should be modified in the parent of feature-stack commit."
    assert "feature_b.py" not in result.stdout, "feature_b.py should NOT be modified in the parent of feature-stack commit."

def test_grandparent_of_feature_stack_is_main():
    # The parent of the 'Add feature A complete' commit is the `main` bookmark.
    # So main should be feature-stack--
    result = run_jj(["log", "--no-graph", "-r", "feature-stack--", "-T", 'bookmarks'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "main" in result.stdout, f"Expected grandparent of feature-stack to be 'main', got bookmarks: {result.stdout}"

def test_final_log_file_exists_and_correct():
    assert os.path.isfile(FINAL_LOG_FILE), f"The file {FINAL_LOG_FILE} was not created."
    with open(FINAL_LOG_FILE, "r") as f:
        content = f.read()
    
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert len(lines) == 2, f"Expected exactly 2 commit descriptions in the log file, found {len(lines)}: {lines}"
    assert lines[0] == "Add feature A complete", f"Expected first line to be 'Add feature A complete', got: {lines[0]}"
    assert lines[1] == "Add feature B", f"Expected second line to be 'Add feature B', got: {lines[1]}"
