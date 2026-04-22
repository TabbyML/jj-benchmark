import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_commit_content_updated():
    # Find the commit with description 'add features'
    log_result = subprocess.run(
        ["jj", "log", "-T", 'change_id ++ " " ++ description ++ "END"'],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert log_result.returncode == 0, "Failed to run jj log."
    
    change_id = None
    for line in log_result.stdout.split("END"):
        if "add features" in line:
            parts = line.strip().split()
            for p in parts:
                if len(p) > 20 and p.isalpha():
                    change_id = p
                    break
            break
            
    assert change_id is not None, "Could not find commit with description 'add features'."

    # Check the commit
    result = subprocess.run(
        ["jj", "show", "-r", change_id],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Could not show commit {change_id}."
    assert "def foo():" in result.stdout, "The commit is missing foo()."
    assert "def bar():" not in result.stdout, "The commit still contains bar()."

def test_working_copy_clean():
    # Check that the working copy has no modifications
    result = subprocess.run(
        ["jj", "status"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj status."
    # A clean working copy should say "The working copy has no changes."
    assert "The working copy has no changes." in result.stdout, "Working copy is not clean."
