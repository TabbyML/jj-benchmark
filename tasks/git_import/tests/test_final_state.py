import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_op_log_contains_git_import():
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj op log."
    
    # Check if the log contains an operation with `args: jj git import`
    assert "args: jj git import" in result.stdout, "The operation log does not contain 'args: jj git import'. You must run the `jj git import` command explicitly."
    
    # Optional: check that they didn't just run `jj log` or `jj status` to import
    # But since they could run it after `jj git import`, we just check that `jj git import` exists.
    # To be strict, we check that `jj git import` was the FIRST command after the git commit.
    # The git commit itself doesn't show up in jj op log until it's imported.
    # So the first operation that imports it should be `jj git import`.
