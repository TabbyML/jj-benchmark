import os
import subprocess
import pytest

REPO_DIR = "/home/user/project-alpha"
LOG_FILE = "/home/user/jj_conflict_resolution_log.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_config_yaml_is_resolved():
    result = run_jj(["resolve", "--list"])
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    assert "config.yaml" not in result.stdout, "config.yaml is still reported as conflicted by jj."

def test_config_yaml_contents():
    config_path = os.path.join(REPO_DIR, "config.yaml")
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read()
    
    assert "environment: production" in content, "config.yaml does not contain 'environment: production'."
    assert "feature_flag: enabled" in content, "config.yaml does not contain 'feature_flag: enabled'."
    assert "<<<<<<<" not in content, "config.yaml still contains conflict markers."
    assert "=======" not in content, "config.yaml still contains conflict markers."
    assert ">>>>>>>" not in content, "config.yaml still contains conflict markers."

def test_log_file_exists_and_shows_no_conflicts():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        content = f.read()
    
    # The log for the current revision should not show it as a conflict
    # In jj, a conflicted commit has "(conflict)" in its log output.
    assert "(conflict)" not in content, f"The log file indicates the commit is still conflicted: {content}"
    
    # Also verify that the log file actually looks like `jj log` output
    assert "@" in content or "Commit ID" in content or "Author" in content or "Date" in content or "merge: main and feature" in content, \
        "The log file does not appear to contain valid `jj log` output."
