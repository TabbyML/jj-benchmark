import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def run_jj_cmd(cmd, cwd=PROJECT_DIR):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def test_commit_3():
    # Verify current working copy commit (@)
    desc = run_jj_cmd(["jj", "log", "-r", "@", "-T", "description", "--no-graph"])
    assert desc == "commit 3", f"Expected description 'commit 3' for @, got '{desc}'"
    
    # Verify file3.txt exists and contains 'third' in @
    content = run_jj_cmd(["jj", "file", "show", "file3.txt", "-r", "@"])
    assert "third" in content, f"Expected 'third' in file3.txt at @, got '{content}'"

def test_commit_2():
    # Verify parent commit (@-)
    desc = run_jj_cmd(["jj", "log", "-r", "@-", "-T", "description", "--no-graph"])
    assert desc == "commit 2", f"Expected description 'commit 2' for @-, got '{desc}'"
    
    # Verify file2.txt exists and contains 'second' in @-
    content = run_jj_cmd(["jj", "file", "show", "file2.txt", "-r", "@-"])
    assert "second" in content, f"Expected 'second' in file2.txt at @-, got '{content}'"

def test_commit_1():
    # Verify grandparent commit (@--)
    desc = run_jj_cmd(["jj", "log", "-r", "@--", "-T", "description", "--no-graph"])
    assert desc == "commit 1", f"Expected description 'commit 1' for @--, got '{desc}'"
    
    # Verify file1.txt exists and contains 'first' in @--
    content = run_jj_cmd(["jj", "file", "show", "file1.txt", "-r", "@--"])
    assert "first" in content, f"Expected 'first' in file1.txt at @--, got '{content}'"
