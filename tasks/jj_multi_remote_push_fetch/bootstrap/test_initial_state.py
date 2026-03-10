import os
import subprocess
import pytest


REPO_DIR = "/home/user/myrepo"
ORIGIN_BARE = "/home/user/remotes/origin.git"
UPSTREAM_BARE = "/home/user/remotes/upstream.git"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory not found: {REPO_DIR}"


def test_jj_dir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found inside repo: {jj_dir}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj status failed in {REPO_DIR}:\n{result.stderr}"
    )


def test_origin_bare_repo_exists():
    assert os.path.isdir(ORIGIN_BARE), (
        f"Origin bare git repo not found: {ORIGIN_BARE}"
    )


def test_upstream_bare_repo_exists():
    assert os.path.isdir(UPSTREAM_BARE), (
        f"Upstream bare git repo not found: {UPSTREAM_BARE}"
    )


def test_origin_remote_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "origin" in result.stdout, (
        f"Remote 'origin' not found in remote list:\n{result.stdout}"
    )


def test_upstream_remote_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "upstream" in result.stdout, (
        f"Remote 'upstream' not found in remote list:\n{result.stdout}"
    )


def test_init_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"init: project scaffold")', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Could not find 'init: project scaffold' commit:\n{result.stderr}"
    )
    assert "init: project scaffold" in result.stdout


def test_release_notes_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"feat: add release notes")', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Could not find 'feat: add release notes' commit:\n{result.stderr}"
    )
    assert "feat: add release notes" in result.stdout


def test_upstream_bare_has_integration_bookmark():
    result = subprocess.run(
        ["git", "branch", "--list", "integration"],
        cwd=UPSTREAM_BARE,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"git branch list failed in upstream bare repo: {result.stderr}"
    )
    assert "integration" in result.stdout, (
        f"'integration' branch not found in upstream bare repo:\n{result.stdout}"
    )
