import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_working_copy_parent_is_root():
    # Verify that the parent of the working copy is the root commit
    result = subprocess.run(
        ["jj", "log", "-T", 'commit_id.short() ++ "\\n"', "-r", "@-", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    parent_id = result.stdout.strip()
    
    # The root commit ID in jj is always 0000000000000000000000000000000000000000
    # In short format, it's a prefix of 0s. Let's check if it's all 0s.
    assert parent_id == "000000000000" or set(parent_id) == {'0'}, f"Expected working copy parent to be the root commit (all 0s), but got {parent_id}"

def test_working_copy_has_no_other_ancestors():
    # Verify that the working copy (@) only has the root commit as an ancestor
    # The revset `@::` should only contain the root commit and the working copy.
    # Wait, `::@` means ancestors of @.
    result = subprocess.run(
        ["jj", "log", "-T", 'commit_id.short() ++ "\\n"', "-r", "::@", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    commits = result.stdout.strip().splitlines()
    
    # It should have exactly two commits: the root commit and the working copy
    assert len(commits) == 2, f"Expected exactly 2 commits in the ancestry of the working copy, but got {len(commits)}: {commits}"
    
    # One of them must be the root commit (all 0s)
    root_commits = [c for c in commits if set(c) == {'0'}]
    assert len(root_commits) == 1, "Root commit not found in the ancestry of the working copy."
