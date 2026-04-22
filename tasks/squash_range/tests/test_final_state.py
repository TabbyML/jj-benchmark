import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_commits_squashed():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "commit_id ++ \"\\n\""],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    
    # 4 commits expected: root, initial commit, feat: initial structure (squashed), feat: add more stuff
    assert len(lines) == 4, f"Expected 4 commits remaining, but found {len(lines)}. Commits were not properly squashed."

def test_squashed_contents():
    result = subprocess.run(
        ["jj", "show", "-r", "feature"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout
    assert "logic fixed" in output, "Target commit does not contain the squashed changes."
    
    # Also check the description of the feature commit
    result_desc = subprocess.run(
        ["jj", "log", "-r", "feature", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    desc = result_desc.stdout
    assert "fix: syntax error" in desc or "feat: initial structure" in desc, "Target commit description should contain the squashed descriptions or the original one."
