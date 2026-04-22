import os
import shutil
import subprocess
import pytest
import json
from pathlib import Path

PROJECT_DIR = "/home/user/myproject"
WORKSPACE_B_DIR = "/home/user/workspace_b"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_workspace_b_directory_exists():
    assert os.path.isdir(WORKSPACE_B_DIR), f"Workspace B directory {WORKSPACE_B_DIR} does not exist."

def test_myproject_is_stale():
    result = subprocess.run(["jj", "st"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode != 0, "Expected 'jj st' to fail because the working copy should be stale."
    assert "stale" in result.stderr.lower() or "stale" in result.stdout.lower(), "Expected stale error message from 'jj st'."

def test_initial_config_json_content():
    config_path = os.path.join(WORKSPACE_B_DIR, "config.json")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist in workspace_b."
    with open(config_path) as f:
        content = json.load(f)
    assert content.get("status") == "pending", "Expected status to be 'pending' in config.json."
    assert content.get("new") is True, "Expected 'new' to be true in config.json."
