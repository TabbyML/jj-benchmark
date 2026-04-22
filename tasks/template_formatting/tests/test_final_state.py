import os
import re
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_repo_exists():
    assert os.path.isdir(os.path.join(PROJECT_DIR, ".jj")), "jj repository not initialized."

def test_jj_log_output():
    # Run jj log to verify the template formatting
    result = subprocess.run(
        ["jj", "log", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    
    lines = result.stdout.strip().split('\n')
    assert len(lines) >= 3, f"Expected at least 3 commits (Second, Initial, and root), but got {len(lines)}"
    
    # Check the latest commit (Second commit)
    assert re.match(r"^[a-z0-9]+ \| test \| Second commit$", lines[0]), f"First line did not match expected format: {lines[0]}"
    
    # Check the previous commit (Initial commit)
    assert re.match(r"^[a-z0-9]+ \| test \| Initial commit$", lines[1]), f"Second line did not match expected format: {lines[1]}"
    
    # Check the root commit
    assert re.match(r"^000000000000 \|  \|.*$", lines[2]) or re.match(r"^000000000000 \|.*\|.*$", lines[2]), f"Third line did not match expected root commit format: {lines[2]}"
