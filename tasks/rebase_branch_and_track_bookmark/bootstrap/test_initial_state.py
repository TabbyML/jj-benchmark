import os
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory not found: {REPO_DIR}"


def test_jj_subdirectory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_scaffold_sh_exists():
    # scaffold.sh is in the working copy (on main)
    path = os.path.join(REPO_DIR, "scaffold.sh")
    assert os.path.isfile(path), f"scaffold.sh not found at {path}"


def test_deploy_sh_exists():
    # deploy.sh is in the working copy (on main)
    path = os.path.join(REPO_DIR, "deploy.sh")
    assert os.path.isfile(path), f"deploy.sh not found at {path}"


def test_metrics_module_py_in_feature_branch():
    # metrics/module.py is tracked in feature/add-metrics bookmark
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "metrics/module.py" in result.stdout, "metrics/module.py not found in feature/add-metrics"


def test_metrics_dashboard_py_in_feature_branch():
    # metrics/dashboard.py is tracked in feature/add-metrics bookmark
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "metrics/dashboard.py" in result.stdout, "metrics/dashboard.py not found in feature/add-metrics"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "bookmark 'main' not found"


def test_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/add-metrics" in result.stdout, "bookmark 'feature/add-metrics' not found"


def test_feature_branch_tip_description():
    result = subprocess.run(
        ["jj", "log", "-r", "feature/add-metrics", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add metrics dashboard endpoint" in result.stdout


def test_deploy_sh_not_in_feature_branch():
    # Before rebase, deploy.sh should NOT be in feature/add-metrics
    result = subprocess.run(
        ["jj", "file", "list", "-r", "feature/add-metrics"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "deploy.sh" not in result.stdout, "deploy.sh should not yet be in feature/add-metrics (rebase not done)"
