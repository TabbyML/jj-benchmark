import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_config_restored():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."
    
    with open(config_path) as f:
        content = f.read().strip()
    
    assert content == "version=2", f"Expected config.txt to be restored to 'version=2', but got '{content}'."

def test_jj_repo_intact():
    # Verify it's still a valid jj repo by running a simple command
    result = subprocess.run(["jj", "log", "-n", "1"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj command failed, repository might be corrupted: {result.stderr}"
