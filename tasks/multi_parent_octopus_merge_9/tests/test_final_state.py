import os
import subprocess
import pytest

REPO_DIR = "/home/user/octopus_repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_octopus_merge_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "octopus_merge", "-T", "commit_id"])
    assert result.returncode == 0, f"Bookmark 'octopus_merge' not found or jj log failed: {result.stderr}"
    assert result.stdout.strip() != "", "Bookmark 'octopus_merge' does not resolve to a commit."

def test_octopus_merge_has_three_parents():
    result = run_jj(["log", "--no-graph", "-r", "octopus_merge", "-T", "parents.map(|c| c.commit_id()).join(' ')"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    parents = result.stdout.strip().split()
    assert len(parents) == 3, f"Expected 'octopus_merge' to have exactly 3 parents, found {len(parents)}: {parents}"

def test_files_exist_in_octopus_merge():
    result = run_jj(["file", "list", "-r", "octopus_merge"])
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    files = result.stdout.splitlines()
    
    expected_files = ["base.txt", "a.txt", "b.txt", "c.txt"]
    for f in expected_files:
        assert f in files, f"Expected file '{f}' not found in the 'octopus_merge' commit."
