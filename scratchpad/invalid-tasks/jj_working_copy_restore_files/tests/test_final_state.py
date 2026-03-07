import os
import subprocess
import pytest

REPO_DIR = "/home/user/incident-repo"


def test_jj_status_clean():
    """After restore, the working-copy diff must be empty (no modified files)."""
    result = subprocess.run(
        ["jj", "diff", "--no-pager", "--summary"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Expected empty diff (clean working copy) but got:\n{result.stdout}"
    )


def test_src_metrics_py_correct_content():
    """src/metrics.py must contain the clean 'collect_metrics' function, not corruption."""
    path = os.path.join(REPO_DIR, "src", "metrics.py")
    with open(path) as fh:
        content = fh.read()
    assert "def collect_metrics():" in content, (
        f"'def collect_metrics():' not found in src/metrics.py.\nContent:\n{content}"
    )
    assert "DEBUG_GARBAGE" not in content, (
        f"Corruption marker 'DEBUG_GARBAGE' still present in src/metrics.py.\nContent:\n{content}"
    )


def test_config_settings_toml_correct_content():
    """config/settings.toml must contain the [database] section, not corruption."""
    path = os.path.join(REPO_DIR, "config", "settings.toml")
    with open(path) as fh:
        content = fh.read()
    assert "[database]" in content, (
        f"'[database]' section missing from config/settings.toml.\nContent:\n{content}"
    )
    assert "CORRUPTED" not in content, (
        f"Corruption marker 'CORRUPTED' still present in config/settings.toml.\nContent:\n{content}"
    )


def test_operation_log_contains_restore():
    """The jj operation log must contain a restore operation."""
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager", "--no-graph", "--limit", "10",
         "-T", "description ++ '\\n'"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "restore" in result.stdout, (
        f"Expected 'restore' operation in op log but not found.\nOutput:\n{result.stdout}"
    )


def test_parent_commit_description_still_wip():
    """The parent of the working-copy commit must still be 'wip: integrate metrics module'."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "--no-graph", "-T", "description ++ '\\n'",
         "-r", "@-"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: integrate metrics module" in result.stdout, (
        f"Expected parent commit 'wip: integrate metrics module' but got:\n{result.stdout}"
    )


def test_all_three_original_commits_still_exist():
    """All three original commits must still be present in history."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "--no-graph", "-T", "description ++ '\\n'",
         "-r", "::@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    for desc in ["init: project scaffold", "feat: add config module", "wip: integrate metrics module"]:
        assert desc in result.stdout, (
            f"Commit '{desc}' missing from history.\nOutput:\n{result.stdout}"
        )


def test_jj_status_output():
    """jj status must report a clean working copy."""
    result = subprocess.run(
        ["jj", "status", "--no-pager"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    # A clean jj working copy shows no modified/added/removed files in the status output
    # The output should not list any M/A/D file entries
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    file_change_lines = [l for l in lines if l and l[0] in ("M", "A", "D") and len(l) > 2]
    assert file_change_lines == [], (
        f"Unexpected file changes in 'jj status':\n{chr(10).join(file_change_lines)}"
    )
