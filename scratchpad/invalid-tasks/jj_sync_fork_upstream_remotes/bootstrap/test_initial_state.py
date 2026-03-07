import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "myproject")
ORIGIN_BARE = os.path.join(HOME, "remotes", "origin.git")
UPSTREAM_BARE = os.path.join(HOME, "remotes", "upstream.git")


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_dir_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_jj_subdir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr.decode()}"


def test_origin_bare_repo_exists():
    assert os.path.isdir(ORIGIN_BARE), f"Origin bare repo not found at {ORIGIN_BARE}"


def test_upstream_bare_repo_exists():
    assert os.path.isdir(UPSTREAM_BARE), f"Upstream bare repo not found at {UPSTREAM_BARE}"


def test_remotes_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0
    output = result.stdout.decode()
    assert "origin" in output, "Remote 'origin' not configured"
    assert "upstream" in output, "Remote 'upstream' not configured"


def test_wip_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0
    output = result.stdout.decode()
    assert "wip-feature" in output, "wip-feature bookmark not found"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0
    output = result.stdout.decode()
    assert "main" in output, "main bookmark not found"


def test_upstream_has_3_commits():
    result = subprocess.run(
        ["git", "log", "--oneline", "main"],
        capture_output=True,
        cwd=UPSTREAM_BARE,
    )
    assert result.returncode == 0
    lines = [l for l in result.stdout.decode().strip().splitlines() if l]
    assert len(lines) == 3, f"Expected 3 commits on upstream main, got {len(lines)}"


def test_origin_has_2_commits():
    result = subprocess.run(
        ["git", "log", "--oneline", "main"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0
    lines = [l for l in result.stdout.decode().strip().splitlines() if l]
    assert len(lines) == 2, f"Expected 2 commits on origin main, got {len(lines)}"


def test_wip_commit_description():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "wip-feature", "-T", "description"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0
    output = result.stdout.decode().strip()
    assert "Add WIP feature work" in output, f"Expected wip commit description, got: {output}"
