import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_final_commit_description():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description('Feature X*')"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj log."
    assert "Feature X - variant 2" in result.stdout, "Final commit description should be 'Feature X - variant 2'."
    assert "Feature X - variant 1" not in result.stdout, "Variant 1 should be abandoned."

def test_no_divergence():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "divergent", "-r", "description('Feature X*')"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj log."
    assert "true" not in result.stdout, "The commit should not be divergent."

def test_operation_log_has_reconcile():
    result = subprocess.run(
        ["jj", "op", "log"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj op log."
    assert "reconcile divergent operations" in result.stdout, "The operation log should contain 'reconcile divergent operations' to indicate the concurrent modification was simulated."
