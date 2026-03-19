import os
import subprocess
import pytest

REPO_DIR = "/home/user/secure_repo"

def test_repo_exists():
    assert os.path.exists(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), f"{REPO_DIR} is not a valid jj repository."

def test_config_toml_contents():
    config_path = os.path.join(REPO_DIR, ".jj/repo/config.toml")
    assert os.path.exists(config_path), f"Config file {config_path} does not exist."
    
    with open(config_path, "r") as f:
        content = f.read()
        
    assert 'behavior = "own"' in content, "signing.behavior is not set to 'own'."
    assert 'backend = "gpg"' in content, "signing.backend is not set to 'gpg'."
    assert 'name = "Security Admin"' in content, "user.name is not set to 'Security Admin'."
    assert 'email = "admin@security.local"' in content, "user.email is not set to 'admin@security.local'."

def test_audit_log_exists():
    audit_file = os.path.join(REPO_DIR, "audit.log")
    assert os.path.exists(audit_file), f"audit.log does not exist in the working copy."

def test_audit_log_in_commit():
    result = subprocess.run(["jj", "log", "-T", "description"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    
    result_files = subprocess.run(["jj", "file", "list"], cwd=REPO_DIR, capture_output=True, text=True)
    assert "audit.log" in result_files.stdout, "audit.log is not tracked in the current commit."
