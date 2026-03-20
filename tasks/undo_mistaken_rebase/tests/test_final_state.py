import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/rebase_verification.log"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_feature_is_direct_child_of_main():
    result = run_jj(["log", "-r", "main..feature", "--no-graph", "-T", "bookmarks"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # If feature is a direct child of main, `main..feature` should contain exactly one commit (the feature commit)
    # Wait, the task says "direct child", but it was originally off main's parent. 
    # Actually, the truth just says "The `feature` bookmark is a direct child of the `main` bookmark."
    # We can check if `main` is the parent of `feature`.
    result_parents = run_jj(["log", "-r", "feature-", "--no-graph", "-T", "bookmarks"])
    assert result_parents.returncode == 0, f"jj log failed: {result_parents.stderr}"
    assert "main" in result_parents.stdout, f"Expected 'main' to be the parent of 'feature', but got: {result_parents.stdout}"

def test_feature_is_not_child_of_dev():
    result = run_jj(["log", "-r", "dev..feature", "--no-graph", "-T", "bookmarks"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # If feature is not a descendant of dev, dev..feature might be empty or just feature, 
    # but the simplest way to check is to ensure dev is NOT an ancestor of feature.
    result_ancestors = run_jj(["log", "-r", "::feature", "--no-graph", "-T", "bookmarks"])
    assert result_ancestors.returncode == 0, f"jj log failed: {result_ancestors.stderr}"
    assert "dev" not in result_ancestors.stdout, "Expected 'feature' to NOT be a child/descendant of 'dev', but 'dev' was found in its ancestors."

def test_rebase_verification_log_exists_and_correct():
    assert os.path.exists(LOG_FILE), f"Verification log {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        content = f.read()
    assert "feature" in content, f"Expected 'feature' in {LOG_FILE}, but got: {content}"
