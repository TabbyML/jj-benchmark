import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/signature_verification.log"

def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)

def test_global_config_signing():
    result = run_jj(["config", "list", "--user"])
    assert result.returncode == 0, f"jj config list failed: {result.stderr}"
    
    output = result.stdout
    assert 'signing.backend = "gpg"' in output, "jj is not globally configured to use GPG backend."
    assert 'signing.key = "signing@example.com"' in output, "jj is not globally configured to use signing@example.com key."
    assert 'signing.behavior = "own"' in output or 'signing.behavior = "force"' in output, "jj signing.behavior is not configured."

def test_global_config_show_signatures():
    result = run_jj(["config", "list", "--user"])
    assert result.returncode == 0, f"jj config list failed: {result.stderr}"
    assert 'ui.show-cryptographic-signatures = true' in result.stdout, "jj is not globally configured to show cryptographic signatures."

def test_commit_created_and_signed():
    # Check that a commit adding signature_test.txt exists and is signed
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n" ++ signature.status() ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Add signature test file" in result.stdout, "Commit with description 'Add signature test file' not found."
    
    # Check file content
    file_path = os.path.join(REPO_DIR, "signature_test.txt")
    assert os.path.isfile(file_path), "signature_test.txt does not exist in the working copy."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "signed content", f"Expected 'signed content', got '{content}'"
    
    # Check signature
    result = run_jj(["log", "--no-graph", "-r", "description('Add signature test file')", "-T", 'signature.status()'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "good", f"Expected signature status 'good', got '{result.stdout.strip()}'"

def test_signature_verification_log():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        log_content = f.read().strip()
    
    # The log should contain the short commit ID and "good"
    assert "good" in log_content, f"Log file does not contain 'good' signature status. Content: {log_content}"
    
    # Verify the commit ID matches the actual commit ID
    result = run_jj(["log", "--no-graph", "-r", "description('Add signature test file')", "-T", 'commit_id.short()'])
    commit_id = result.stdout.strip()
    assert commit_id in log_content, f"Log file does not contain the correct commit ID ({commit_id}). Content: {log_content}"
