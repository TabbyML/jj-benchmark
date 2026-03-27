import os
import subprocess
import pytest

REPO = "/home/user/repo"
SECONDARY_WS = "/home/user/secondary-ws"


def run(cmd, cwd=REPO):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result


def test_secondary_workspace_no_longer_stale():
    result = run(["jj", "status"], cwd=SECONDARY_WS)
    combined = result.stdout + result.stderr
    assert "stale" not in combined.lower(), "Secondary workspace should no longer be stale"
    assert result.returncode == 0, f"jj status in secondary workspace should succeed: {result.stderr}"


def test_secondary_workspace_on_valid_commit():
    result = run(["jj", "log", "--no-graph", "-T", "change_id ++ '\n'", "-r", "@"], cwd=SECONDARY_WS)
    assert result.returncode == 0, f"Should be able to get working copy commit in secondary: {result.stderr}"
    commit_id = result.stdout.strip()
    assert len(commit_id) > 0, "Secondary workspace should have a valid working copy commit"


def test_workspace_list_shows_valid_commits():
    result = run(["jj", "workspace", "list"])
    assert result.returncode == 0
    assert "secondary" in result.stdout, "secondary workspace must appear in list"
    # Should not show any error state
    assert "stale" not in result.stdout.lower(), "workspace list should not show stale workspaces"


def test_main_workspace_still_healthy():
    result = run(["jj", "status"])
    assert result.returncode == 0, f"Main workspace should still be healthy: {result.stderr}"


def test_recovery_status_report_exists():
    report_path = "/home/user/recovery_status.txt"
    assert os.path.isfile(report_path), "recovery_status.txt must exist at /home/user/recovery_status.txt"
    with open(report_path) as f:
        content = f.read()
    assert len(content) > 30, "Recovery status report must have content"
    assert any(kw in content.lower() for kw in ["workspace", "secondary", "stale", "update", "recover"]), \
        "Recovery status must mention workspace recovery"
