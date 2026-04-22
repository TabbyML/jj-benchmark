import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_config_py_reverted():
    """Verify config.py matches the parent commit's state."""
    config_path = os.path.join(PROJECT_DIR, "config.py")
    with open(config_path, "r") as f:
        content = f.read().strip()
    
    assert "DEBUG = False" in content, \
        f"Expected config.py to be 'DEBUG = False', but got: {content}"

def test_utils_py_restored():
    """Verify utils.py matches the v1.0 state."""
    utils_path = os.path.join(PROJECT_DIR, "utils.py")
    with open(utils_path, "r") as f:
        content = f.read().strip()
    
    assert content == 'def helper(): return "v1"', \
        f"Expected utils.py to be 'def helper(): return \"v1\"', but got: {content}"

def test_app_py_unchanged():
    """Verify app.py retains the working copy changes."""
    app_path = os.path.join(PROJECT_DIR, "app.py")
    with open(app_path, "r") as f:
        content = f.read().strip()
    
    assert content == 'print("working copy app")', \
        f"Expected app.py to be 'print(\"working copy app\")', but got: {content}"

def test_working_copy_description():
    """Priority 1: Use jj CLI to verify the working copy description."""
    result = subprocess.run(
        ["jj", "log", "-r", "@", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    
    description = result.stdout.strip()
    expected_description = "Restore configuration and utilities"
    
    assert description == expected_description, \
        f"Expected working copy description to be '{expected_description}', but got: '{description}'"
