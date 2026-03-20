import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_a_is_merge_commit():
    # Check the number of parents for the commit pointed to by feature-a
    result = run_jj(["log", "--no-graph", "-r", "feature-a", "-T", "parents.map(|c| c.commit_id()).join(' ')"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    parents = result.stdout.strip().split()
    assert len(parents) == 2, f"Expected feature-a to point to a merge commit with 2 parents, but found {len(parents)} parents: {parents}"

def test_app_py_resolved_content():
    # Check the content of app.py in feature-a
    result = run_jj(["file", "show", "app.py", "-r", "feature-a"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    content = result.stdout.strip()
    
    expected_content = 'def main():\n    print("Feature A")\n    print("Feature B")'
    assert content == expected_content, f"app.py does not have the expected resolved content. Got:\n{content}"

def test_no_conflict_markers_in_feature_a():
    # Ensure there are no conflicts in feature-a
    # If there are no conflicts, `jj resolve --list` will return 2 and output "Error: No conflicts found at this revision"
    # If there are conflicts, it will return 0 and list them.
    result_resolve = run_jj(["resolve", "--list", "-r", "feature-a"])
    if result_resolve.returncode == 0:
        assert result_resolve.stdout.strip() == "", f"Conflicts still exist in feature-a: {result_resolve.stdout}"
    else:
        # If it failed, it should be because there are no conflicts
        assert "No conflicts found" in result_resolve.stderr, f"Unexpected error from jj resolve: {result_resolve.stderr}"
