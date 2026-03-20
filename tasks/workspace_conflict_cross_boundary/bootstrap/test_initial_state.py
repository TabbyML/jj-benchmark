"""
Initial state tests for jj_workspace_conflict_cross_boundary.
"""
import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
WS_A = "/home/user/ws-a"
WS_B = "/home/user/ws-b"


def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)


def test_jj_available():
    assert shutil.which("jj") is not None


def test_main_repo_exists():
    assert os.path.isdir(REPO_DIR) and os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_ws_a_exists():
    assert os.path.isdir(WS_A)


def test_ws_b_exists():
    assert os.path.isdir(WS_B)


def test_feature_a_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "feature-a", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"feature-a not found: {result.stderr}"
    assert "feat: add users endpoint" in result.stdout


def test_feature_b_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "feature-b", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"feature-b not found: {result.stderr}"
    assert "feat: add products endpoint" in result.stdout


def test_both_branches_from_main():
    # Both feature-a and feature-b should be children of main
    result = run_jj(["log", "--no-graph", "-r", "children(main)", "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    assert "feat: add users endpoint" in result.stdout
    assert "feat: add products endpoint" in result.stdout


def test_api_py_at_feature_a():
    result = run_jj(["file", "show", "src/api.py", "-r", "feature-a"])
    assert result.returncode == 0
    assert "/users" in result.stdout


def test_api_py_at_feature_b():
    result = run_jj(["file", "show", "src/api.py", "-r", "feature-b"])
    assert result.returncode == 0
    assert "/products" in result.stdout


def test_workspaces_listed():
    result = run_jj(["workspace", "list"])
    assert result.returncode == 0
    assert "ws-a" in result.stdout
    assert "ws-b" in result.stdout
