import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_working_copy_empty():
    result = subprocess.run(
        ["jj", "st"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Working copy changes:" not in result.stdout, "Working copy is not empty. There are still changes."
    assert "The working copy has no changes" in result.stdout or "(empty)" in result.stdout, "Working copy does not appear to be empty."

def test_feature_a_absorbed():
    # Find the commit with description "Add feature A"
    result = subprocess.run(
        ["jj", "log", "-r", "description(\"Add feature A\\n\")", "-T", "commit_id", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    commit_id = result.stdout.strip()
    assert commit_id, "Could not find commit with description 'Add feature A'."
    
    # Check the contents of feature_a.py in that commit
    file_content = subprocess.run(
        ["jj", "file", "show", "-r", commit_id, "feature_a.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Feature A fixed" in file_content.stdout, "Changes to feature_a.py were not absorbed into 'Add feature A' commit."

def test_feature_b_absorbed():
    # Find the commit with description "Add feature B"
    result = subprocess.run(
        ["jj", "log", "-r", "description(\"Add feature B\\n\")", "-T", "commit_id", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    commit_id = result.stdout.strip()
    assert commit_id, "Could not find commit with description 'Add feature B'."
    
    # Check the contents of feature_b.py in that commit
    file_content = subprocess.run(
        ["jj", "file", "show", "-r", commit_id, "feature_b.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Feature B fixed" in file_content.stdout, "Changes to feature_b.py were not absorbed into 'Add feature B' commit."
