import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_no_stale_error():
    result = subprocess.run(["jj", "st"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Expected 'jj st' to succeed, but it failed with: {result.stderr}"
    assert "stale" not in result.stderr.lower(), "The working copy is still stale."

def test_config_json_content():
    config_path = os.path.join(PROJECT_DIR, "config.json")
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."
    with open(config_path) as f:
        content = json.load(f)
    assert content.get("status") == "active", "Expected 'status' to be 'active' in config.json."
    assert content.get("new") is True, "Expected 'new' to be true in config.json (should be preserved from workspace_b)."

def test_commit_message():
    result = subprocess.run(["jj", "log", "-T", "description", "-r", "@-"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run 'jj log'"
    assert "Activate config" in result.stdout, "Expected commit message to contain 'Activate config'."
