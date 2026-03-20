import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"
LOG_FILE = "/home/user/parents.log"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_integration_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "integration" in result.stdout, "Bookmark 'integration' does not exist."

def test_integration_has_three_parents():
    # Get the parents of the integration bookmark
    result = run_jj(["log", "-r", "parents(integration)", "--no-graph", "-T", "bookmarks ++ '\n'"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    
    parents_output = result.stdout.strip().split('\n')
    # Filter out empty strings
    parents = [p.strip() for p in parents_output if p.strip()]
    
    assert len(parents) == 3, f"Expected exactly 3 parents for 'integration', found {len(parents)}: {parents}"
    
    # Check that the parents are feature-a, feature-b, feature-c
    all_parents_text = " ".join(parents)
    assert "feature-a" in all_parents_text, "Parent 'feature-a' missing from integration parents."
    assert "feature-b" in all_parents_text, "Parent 'feature-b' missing from integration parents."
    assert "feature-c" in all_parents_text, "Parent 'feature-c' missing from integration parents."

def test_octopus_file_exists_and_content():
    result = run_jj(["file", "show", "octopus.txt", "-r", "integration"])
    assert result.returncode == 0, f"Failed to read octopus.txt from integration revision: {result.stderr}"
    content = result.stdout.strip()
    assert content == "merged", f"Expected octopus.txt to contain 'merged', but got '{content}'"

def test_parents_log_file_correct():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        content = f.read()
    
    assert "feature-a" in content, f"'feature-a' not found in {LOG_FILE}"
    assert "feature-b" in content, f"'feature-b' not found in {LOG_FILE}"
    assert "feature-c" in content, f"'feature-c' not found in {LOG_FILE}"
