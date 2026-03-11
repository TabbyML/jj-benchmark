"""
Bootstrap tests for jj_oplog_branch_diverge_recovery.
Verify the initial state: two diverged branches.
"""

import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_jj_binary_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(REPO_DIR)


def test_repo_is_valid():
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0


def test_main_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "main" in result.stdout


def test_develop_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "develop" in result.stdout


def test_main_has_release_commits():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert "release: v1.1" in result.stdout
    assert "release: v1.2" in result.stdout


def test_develop_has_feature_commits():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert "feat: feature-x-start" in result.stdout
    assert "feat: feature-x-complete" in result.stdout


def test_shared_base_exists():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert "feat: shared-utils" in result.stdout, "shared base commit should exist"


def test_lca_is_shared_utils():
    result = run_jj(["log", "--no-graph", "-r", "heads(::develop & ::main)",
                     "-T", 'description'])
    assert result.returncode == 0, f"LCA query failed: {result.stderr}"
    assert "feat: shared-utils" in result.stdout, \
        f"LCA should be 'feat: shared-utils', got: {result.stdout.strip()}"
