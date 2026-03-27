"""
Tests for jj_workspace_conflict_cross_boundary.
"""
import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/cross_boundary_log.txt"


def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)


def test_feature_b_has_feature_a_as_ancestor():
    result = run_jj(
        ["log", "--no-graph", "-r", "ancestors(feature-b)", "-T", 'description ++ "\n"']
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add users endpoint" in result.stdout, \
        "feature-a commit not found in ancestry of feature-b (rebase not done)."


def test_api_py_at_feature_b_has_no_conflicts():
    result = run_jj(["file", "show", "src/api.py", "-r", "feature-b"])
    assert result.returncode == 0, f"Could not show src/api.py: {result.stderr}"
    assert "<<<<<<<" not in result.stdout, "Conflict markers in src/api.py."
    assert "=======" not in result.stdout, "Conflict markers in src/api.py."
    assert ">>>>>>>" not in result.stdout, "Conflict markers in src/api.py."


def test_api_py_has_users_endpoint():
    result = run_jj(["file", "show", "src/api.py", "-r", "feature-b"])
    assert result.returncode == 0, f"Could not show src/api.py: {result.stderr}"
    assert "/users" in result.stdout, "Missing /users endpoint in resolved src/api.py."


def test_api_py_has_products_endpoint():
    result = run_jj(["file", "show", "src/api.py", "-r", "feature-b"])
    assert result.returncode == 0, f"Could not show src/api.py: {result.stderr}"
    assert "/products" in result.stdout, "Missing /products endpoint in resolved src/api.py."


def test_main_has_both_features_as_ancestors():
    result = run_jj(
        ["log", "--no-graph", "-r", "ancestors(main)", "-T", 'description ++ "\n"']
    )
    assert result.returncode == 0, f"jj log ancestors(main) failed: {result.stderr}"
    assert "feat: add users endpoint" in result.stdout, \
        "main ancestry missing feat: add users endpoint."
    assert "feat: add products endpoint" in result.stdout, \
        "main ancestry missing feat: add products endpoint."


def test_main_is_merge_commit():
    result = run_jj(["log", "--no-graph", "-r", "main", "-T", 'parents.len() ++ "\n"'])
    assert result.returncode == 0, f"jj log main failed: {result.stderr}"
    assert result.stdout.strip() == "2", \
        f"main should be a merge commit with 2 parents, got: {result.stdout.strip()}"


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} not found."


def test_log_file_content():
    with open(LOG_FILE) as f:
        content = f.read()
    assert "ws-a-commit:" in content
    assert "ws-b-commit:" in content
    assert "merge-commit:" in content
    assert "conflict-file: src/api.py" in content
    assert "resolution: both-endpoints-kept" in content
