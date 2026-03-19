import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_bookmark_points_to_third():
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "third" in result.stdout, f"Expected bookmark 'feature' to point to commit described as 'third', got: {result.stdout.strip()}"

def test_bugfix_bookmark_points_to_second():
    result = run_jj(["log", "-r", "bugfix", "--no-graph", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "second" in result.stdout, f"Expected bookmark 'bugfix' to point to commit described as 'second', got: {result.stdout.strip()}"

def test_working_copy_is_second():
    result = run_jj(["log", "-r", "@", "--no-graph", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "second" in result.stdout, f"Expected working copy (@) to be at commit described as 'second', got: {result.stdout.strip()}"
