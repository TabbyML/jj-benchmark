import os
import shutil
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/myproject-workspace2"

def test_workspace_dir_exists():
    assert os.path.isdir(WORKSPACE_DIR), f"Workspace directory {WORKSPACE_DIR} was not created."

def test_workspace_is_jj_repo():
    jj_dir = os.path.join(WORKSPACE_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"{WORKSPACE_DIR} is not a valid jj workspace."

def test_jj_status_in_workspace():
    result = subprocess.run(
        ["jj", "status"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj status failed in {WORKSPACE_DIR} with output: {result.stderr}"
