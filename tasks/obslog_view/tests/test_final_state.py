import os
import subprocess
import pytest

OBSLOG_FILE = "/home/user/obslog.txt"
REPO_DIR = "/home/user/repo"

def test_obslog_file_exists():
    assert os.path.isfile(OBSLOG_FILE), f"Expected output file not found at {OBSLOG_FILE}"

def test_obslog_file_content():
    # Get the actual obslog output
    result = subprocess.run(
        ["jj", "obslog", "--color=never"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    expected_output = result.stdout.strip()
    
    # Read the user's file
    with open(OBSLOG_FILE, "r") as f:
        actual_output = f.read().strip()
    
    # Check if the file contains the key parts of the obslog
    # We check for the presence of the commit messages and the working copy indicator
    assert "v1" in actual_output, "The obslog output should contain the history of 'v1'"
    assert "v2" in actual_output, "The obslog output should contain the history of 'v2'"
    assert "Test User" in actual_output or "test@example.com" in actual_output, "The obslog output should contain the author information"
    
    # A basic check to see if it looks like an obslog
    assert "working copy" in actual_output.lower() or "@" in actual_output, "The output does not appear to be a valid jj obslog output"
