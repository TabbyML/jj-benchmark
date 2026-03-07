import os
import subprocess
import pytest


REPO_DIR = "/home/user/myproject"
ORIGIN_REMOTE = "/home/user/remotes/origin.git"
UPSTREAM_REMOTE = "/home/user/remotes/upstream.git"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_jj_dir_exists():
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


def test_origin_remote_bare_repo_exists():
    assert os.path.isdir(ORIGIN_REMOTE), f"Origin bare repo {ORIGIN_REMOTE} does not exist"
    head_file = os.path.join(ORIGIN_REMOTE, "HEAD")
    assert os.path.isfile(head_file), f"Not a bare git repo (no HEAD file): {ORIGIN_REMOTE}"


def test_upstream_remote_bare_repo_exists():
    assert os.path.isdir(UPSTREAM_REMOTE), f"Upstream bare repo {UPSTREAM_REMOTE} does not exist"
    head_file = os.path.join(UPSTREAM_REMOTE, "HEAD")
    assert os.path.isfile(head_file), f"Not a bare git repo (no HEAD file): {UPSTREAM_REMOTE}"


def test_origin_remote_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "origin" in result.stdout, f"'origin' remote not found in: {result.stdout}"


def test_upstream_remote_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "upstream" in result.stdout, f"'upstream' remote not found in: {result.stdout}"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, f"'main' bookmark not found in: {result.stdout}"


def test_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, f"'feature' bookmark not found in: {result.stdout}"


def test_initial_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'initial commit')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial commit" in result.stdout, f"No commit with description 'initial commit' found"


def test_add_feature_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description(substring:'add feature')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add feature" in result.stdout, f"No commit with description 'add feature' found"


def test_main_tracked_from_origin():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--tracked"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list --tracked failed: {result.stderr}"
    assert "main" in result.stdout, f"'main' is not tracked from origin. Output: {result.stdout}"


def test_main_exists_on_origin_remote():
    result = subprocess.run(
        ["git", "-C", ORIGIN_REMOTE, "branch", "--list", "main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch list failed: {result.stderr}"
    assert "main" in result.stdout, f"'main' branch not found in origin remote: {result.stdout}"


def test_main_exists_on_upstream_remote():
    result = subprocess.run(
        ["git", "-C", UPSTREAM_REMOTE, "branch", "--list", "main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch list failed: {result.stderr}"
    assert "main" in result.stdout, f"'main' branch not found in upstream remote: {result.stdout}"


def test_feature_not_yet_on_upstream():
    result = subprocess.run(
        ["git", "-C", UPSTREAM_REMOTE, "branch", "--list", "feature"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch list failed: {result.stderr}"
    assert "feature" not in result.stdout, (
        f"'feature' branch already exists on upstream (should not yet): {result.stdout}"
    )
