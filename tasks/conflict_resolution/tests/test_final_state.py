import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_conflict_resolved():
    file_path = os.path.join(PROJECT_DIR, "file.txt")
    with open(file_path, "r") as f:
        content = f.read()
    
    assert "Feature A and Feature B" in content, "Conflict not resolved as expected."
    assert "<<<<<<<" not in content, "Conflict markers still present."

def test_rebase_successful():
    result = subprocess.run(["jj", "log", "-r", "feature-b"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run jj log"
    
    # feature-b should be a descendant of feature-a
    result = subprocess.run(["jj", "log", "-r", "feature-a::feature-b"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "feature-b" in result.stdout, "feature-b is not a descendant of feature-a"

def test_no_conflicts():
    result = subprocess.run(["jj", "st"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "conflict" not in result.stdout.lower(), "Repository still has conflicts."
