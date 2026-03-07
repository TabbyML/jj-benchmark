import os
import subprocess
import pytest

HOME = "/home/user"
REPO_DIR = os.path.join(HOME, "myproject")
ORIGIN_BARE = os.path.join(HOME, "remotes", "origin.git")
UPSTREAM_BARE = os.path.join(HOME, "remotes", "upstream.git")


def jj(*args, cwd=REPO_DIR):
    result = subprocess.run(
        ["jj"] + list(args),
        capture_output=True,
        cwd=cwd,
        env={**os.environ, "HOME": HOME},
    )
    return result


def test_main_bookmark_points_to_upstream_feature():
    """Local 'main' bookmark must point to the upstream feature commit."""
    result = jj("log", "--no-graph", "-r", "main", "-T", "description")
    assert result.returncode == 0, f"jj log failed: {result.stderr.decode()}"
    output = result.stdout.decode().strip()
    assert "Add upstream feature" in output, (
        f"Expected 'main' to point to 'Add upstream feature' commit, got: {output}"
    )


def test_wip_feature_parent_is_upstream_feature():
    """wip-feature commit must have the upstream feature commit as its parent."""
    # Get description of parent of wip-feature
    result = jj("log", "--no-graph", "-r", "wip-feature-", "-T", "description")
    assert result.returncode == 0, f"jj log for parent failed: {result.stderr.decode()}"
    output = result.stdout.decode().strip()
    assert "Add upstream feature" in output, (
        f"Expected parent of wip-feature to be 'Add upstream feature', got: {output}"
    )


def test_wip_feature_description_unchanged():
    """wip-feature commit must still have its original description."""
    result = jj("log", "--no-graph", "-r", "wip-feature", "-T", "description")
    assert result.returncode == 0
    output = result.stdout.decode().strip()
    assert "Add WIP feature work" in output, (
        f"Expected wip-feature description 'Add WIP feature work', got: {output}"
    )


def test_origin_main_has_3_commits():
    """origin remote's main branch must have 3 commits after push."""
    result = subprocess.run(
        ["git", "log", "--oneline", "main"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0, f"git log on origin failed: {result.stderr.decode()}"
    lines = [l for l in result.stdout.decode().strip().splitlines() if l]
    assert len(lines) == 3, (
        f"Expected 3 commits on origin/main, got {len(lines)}: {result.stdout.decode()}"
    )


def test_origin_main_tip_is_upstream_feature():
    """The tip of origin/main must be the upstream feature commit."""
    result = subprocess.run(
        ["git", "log", "--oneline", "-1", "main"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0
    output = result.stdout.decode().strip()
    assert "Add upstream feature" in output, (
        f"Expected origin/main tip to be 'Add upstream feature', got: {output}"
    )


def test_origin_wip_feature_exists():
    """origin remote must have a wip-feature branch."""
    result = subprocess.run(
        ["git", "branch"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0
    output = result.stdout.decode()
    assert "wip-feature" in output, (
        f"Expected 'wip-feature' branch on origin, got: {output}"
    )


def test_origin_wip_feature_has_4_commits():
    """origin remote's wip-feature branch must have 4 commits."""
    result = subprocess.run(
        ["git", "log", "--oneline", "wip-feature"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0, f"git log on origin wip-feature failed: {result.stderr.decode()}"
    lines = [l for l in result.stdout.decode().strip().splitlines() if l]
    assert len(lines) == 4, (
        f"Expected 4 commits on origin/wip-feature, got {len(lines)}: {result.stdout.decode()}"
    )


def test_origin_wip_feature_tip_is_wip_commit():
    """The tip of origin/wip-feature must be the WIP commit."""
    result = subprocess.run(
        ["git", "log", "--oneline", "-1", "wip-feature"],
        capture_output=True,
        cwd=ORIGIN_BARE,
    )
    assert result.returncode == 0
    output = result.stdout.decode().strip()
    assert "Add WIP feature work" in output, (
        f"Expected origin/wip-feature tip to be 'Add WIP feature work', got: {output}"
    )


def test_local_main_and_upstream_at_same_commit():
    """Local main and upstream@upstream must reference the same commit."""
    result_main = jj("log", "--no-graph", "-r", "main", "-T", "commit_id")
    result_upstream = jj("log", "--no-graph", "-r", "main@upstream", "-T", "commit_id")
    assert result_main.returncode == 0
    assert result_upstream.returncode == 0
    main_id = result_main.stdout.decode().strip()
    upstream_id = result_upstream.stdout.decode().strip()
    assert main_id == upstream_id, (
        f"Expected local main ({main_id}) to equal upstream@upstream ({upstream_id})"
    )
