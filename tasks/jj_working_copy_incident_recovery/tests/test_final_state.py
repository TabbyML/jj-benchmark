import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
STATUS_FILE = "/home/user/recovery_status.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_cache_bin_restored():
    assert os.path.exists(os.path.join(REPO_DIR, "data/cache.bin")), "data/cache.bin was not restored"

def test_deploy_sh_unmodified():
    # Should not be in diff (no local modifications from parent)
    result = run_jj(["diff", "-r", "@", "--stat"])
    assert result.returncode == 0
    assert "scripts/deploy.sh" not in result.stdout, "scripts/deploy.sh should not have modifications"
    # Actually wait, the user committed the settings change. The deploy.sh should just be identical to the parent.
    # We can check its content
    with open(os.path.join(REPO_DIR, "scripts/deploy.sh"), "r") as f:
        content = f.read()
    assert "deploying... error" not in content, "scripts/deploy.sh edits were not discarded"
    assert "deploying" in content, "scripts/deploy.sh should match pristine state"

def test_commit_description():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", 'description'])
    assert result.returncode == 0
    assert "chore: update settings for incident recovery" in result.stdout, "Expected commit description not found"

def test_settings_yaml_in_commit():
    # The commit should have modified config/settings.yaml
    result = run_jj(["show", "-r", "@", "--stat"])
    assert result.returncode == 0
    assert "config/settings.yaml" in result.stdout, "config/settings.yaml was not committed"

def test_recovery_status_file():
    assert os.path.exists(STATUS_FILE), f"{STATUS_FILE} does not exist"
    with open(STATUS_FILE, "r") as f:
        commit_id = f.read().strip()
    
    # Check that this commit ID matches the current commit
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", 'commit_id'])
    assert result.returncode == 0
    expected_id = result.stdout.strip()
    
    # We can check if the commit ID starts with the one in the file, or matches exactly
    assert commit_id and expected_id.startswith(commit_id), f"Commit ID in {STATUS_FILE} does not match current commit ID"
