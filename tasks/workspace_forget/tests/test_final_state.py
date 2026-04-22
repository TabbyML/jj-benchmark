import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
EXPERIMENT_DIR = "/home/user/myproject-experiment"

def test_experiment_workspace_forgotten_via_cli():
    """Priority 1: Use jj CLI to verify the experiment workspace is no longer tracked."""
    result = subprocess.run(
        ["jj", "workspace", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj workspace list' failed: {result.stderr}"
    assert "experiment: " not in result.stdout, \
        f"Expected 'experiment' workspace to be forgotten, but it is still tracked in: {result.stdout}"

def test_experiment_dir_removed():
    """Priority 3 fallback: Verify the experiment workspace directory was removed."""
    assert not os.path.exists(EXPERIMENT_DIR), \
        f"Expected experiment directory {EXPERIMENT_DIR} to be removed, but it still exists."
