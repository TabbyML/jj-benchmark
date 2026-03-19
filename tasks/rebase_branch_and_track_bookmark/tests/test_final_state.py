import os
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def test_feature_bookmark_tip_description():
    """feature/add-metrics must point to the 'feat: add metrics dashboard endpoint' commit."""
    result = subprocess.run(
        ["jj", "log", "-r", "feature/add-metrics", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add metrics dashboard endpoint" in result.stdout, (
        f"Expected feature/add-metrics tip description 'feat: add metrics dashboard endpoint', got: {result.stdout}"
    )


def test_feature_bookmark_parent_description():
    """The parent of feature/add-metrics tip must be 'feat: scaffold metrics module'."""
    result = subprocess.run(
        ["jj", "log", "-r", "feature/add-metrics-", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: scaffold metrics module" in result.stdout, (
        f"Expected parent of feature/add-metrics to be 'feat: scaffold metrics module', got: {result.stdout}"
    )


def test_feature_bookmark_grandparent_is_main():
    """The grandparent of feature/add-metrics tip must be the commit at main."""
    # Get the commit ID of main
    result_main = subprocess.run(
        ["jj", "log", "-r", "main", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_main.returncode == 0, f"jj log main failed: {result_main.stderr}"
    main_commit_id = result_main.stdout.strip()

    # Get the commit ID of grandparent of feature/add-metrics
    result_gp = subprocess.run(
        ["jj", "log", "-r", "feature/add-metrics--", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_gp.returncode == 0, f"jj log grandparent failed: {result_gp.stderr}"
    grandparent_commit_id = result_gp.stdout.strip()

    assert main_commit_id == grandparent_commit_id, (
        f"Grandparent of feature/add-metrics ({grandparent_commit_id}) should equal main ({main_commit_id}). "
        "The feature branch may not have been rebased onto main."
    )


def test_grandparent_description_is_deploy_sh_commit():
    """The grandparent of feature/add-metrics tip must have description 'chore: add deploy.sh for CI pipeline'."""
    result = subprocess.run(
        ["jj", "log", "-r", "feature/add-metrics--", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log grandparent failed: {result.stderr}"
    assert "chore: add deploy.sh for CI pipeline" in result.stdout, (
        f"Expected grandparent description 'chore: add deploy.sh for CI pipeline', got: {result.stdout}"
    )


def test_deploy_sh_in_feature_branch():
    """deploy.sh must be present in feature/add-metrics after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "deploy.sh" in result.stdout, (
        f"deploy.sh should be in feature/add-metrics after rebase onto main. Got files: {result.stdout}"
    )


def test_metrics_module_in_feature_branch():
    """metrics/module.py must be present in feature/add-metrics after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "metrics/module.py" in result.stdout, (
        f"metrics/module.py should be in feature/add-metrics. Got files: {result.stdout}"
    )


def test_metrics_dashboard_in_feature_branch():
    """metrics/dashboard.py must be present in feature/add-metrics after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "metrics/dashboard.py" in result.stdout, (
        f"metrics/dashboard.py should be in feature/add-metrics. Got files: {result.stdout}"
    )


def test_scaffold_sh_in_feature_branch():
    """scaffold.sh must be present in feature/add-metrics after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "scaffold.sh" in result.stdout, (
        f"scaffold.sh should be in feature/add-metrics. Got files: {result.stdout}"
    )
