import os
import subprocess
import pytest

REPO = "/home/user/repo"
SECONDARY_WS = "/home/user/secondary-ws"


def run(cmd, cwd=REPO):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result


def test_main_repo_exists():
    assert os.path.isdir(REPO), "Main repository /home/user/repo must exist"


def test_secondary_workspace_exists():
    assert os.path.isdir(SECONDARY_WS), "Secondary workspace /home/user/secondary-ws must exist"


def test_workspace_list_shows_two_workspaces():
    result = run(["jj", "workspace", "list"])
    assert result.returncode == 0
    assert "default" in result.stdout, "default workspace must be listed"
    assert "secondary" in result.stdout, "secondary workspace must be listed"


def test_main_workspace_is_healthy():
    result = run(["jj", "status"])
    assert result.returncode == 0, f"Main workspace status failed: {result.stderr}"


def test_secondary_workspace_is_stale():
    result = run(["jj", "status"], cwd=SECONDARY_WS)
    # Secondary workspace should be stale
    assert result.returncode != 0 or "stale" in result.stderr.lower() or "stale" in result.stdout.lower(), \
        "Secondary workspace should be in stale state"


def test_stale_hint_present():
    result = run(["jj", "status"], cwd=SECONDARY_WS)
    combined = result.stdout + result.stderr
    assert "stale" in combined.lower() or "update-stale" in combined.lower(), \
        "jj should report stale workspace condition"


def test_main_bookmark_intact():
    result = run(["jj", "bookmark", "list"])
    assert result.returncode == 0
    assert "main" in result.stdout, "main bookmark must exist"
