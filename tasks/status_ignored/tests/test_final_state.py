import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_build_log_exists():
    """Priority 3 fallback: basic file existence check."""
    log_path = os.path.join(PROJECT_DIR, "build.log")
    assert os.path.isfile(log_path), f"File {log_path} must not be deleted."

def test_gitignore_contains_build_log():
    """Priority 3 fallback: check .gitignore content."""
    gitignore_path = os.path.join(PROJECT_DIR, ".gitignore")
    assert os.path.isfile(gitignore_path), ".gitignore file must exist."
    with open(gitignore_path) as f:
        content = f.read()
    assert "build.log" in content, ".gitignore must contain 'build.log'."

def test_build_log_is_not_tracked_via_cli():
    """Priority 1: Use jj file list to verify build.log is not tracked."""
    result = subprocess.run(
        ["jj", "file", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj file list' failed: {result.stderr}"
    assert "build.log" not in result.stdout.splitlines(), \
        "Expected build.log to no longer be tracked by jj."

def test_build_log_not_in_status_via_cli():
    """Priority 1: Use jj status to verify build.log is not shown as added or modified."""
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj status' failed: {result.stderr}"
    # It might show as 'D build.log' if it was committed previously, which is fine.
    # It just shouldn't be 'A build.log' or 'M build.log' or 'build.log' without D.
    lines = result.stdout.splitlines()
    for line in lines:
        if "build.log" in line:
            assert line.strip().startswith("D "), \
                f"build.log should only appear as deleted (D) in status, but got: {line.strip()}"
