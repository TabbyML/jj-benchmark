import os
import subprocess
import pytest


REPO_DIR = "/home/user/release-project"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_jj_metadata_directory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory does not exist in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_commit_initial_project_scaffold_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", 'description(substring:"initial project scaffold")',
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial project scaffold" in result.stdout


def test_commit_add_authentication_module_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", 'description(substring:"add authentication module")',
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add authentication module" in result.stdout


def test_commit_add_payment_gateway_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", 'description(substring:"add payment gateway")',
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add payment gateway" in result.stdout


def test_commit_add_reporting_dashboard_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", 'description(substring:"add reporting dashboard")',
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add reporting dashboard" in result.stdout


def test_main_bookmark_initially_on_auth_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "main", "--template", "description",
         "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for main bookmark failed: {result.stderr}"
    assert "add authentication module" in result.stdout
