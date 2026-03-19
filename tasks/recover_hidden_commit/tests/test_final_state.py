import os
import subprocess
import pytest

REPO_DIR = "/home/user/kernel-patch"


def test_watchdog_commit_is_visible_in_default_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add watchdog timer support" in result.stdout, (
        "Expected commit 'feat: add watchdog timer support' to be visible in default jj log, "
        "but it was not found. The hidden commit must be restored into visible history."
    )


def test_watchdog_commit_not_marked_hidden_in_log():
    result = subprocess.run(
        [
            "jj", "log",
            "-r", 'description(substring:"watchdog")',
            "--no-graph",
            "-T", 'description ++ " hidden=" ++ if(hidden, "true", "false")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log revset for watchdog commit failed: {result.stderr}"
    assert "feat: add watchdog timer support" in result.stdout, (
        "Watchdog commit must be visible (not hidden)"
    )
    assert "hidden=true" not in result.stdout, (
        "Watchdog commit must not be hidden"
    )


def test_watchdog_file_content_accessible():
    result = subprocess.run(
        [
            "jj", "file", "show", "watchdog.c",
            "-r", 'description(substring:"watchdog")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj file show watchdog.c failed: {result.stderr}. "
        "The watchdog.c file must be accessible in the recovered commit."
    )
    assert "/* watchdog timer implementation */" in result.stdout, (
        f"Expected '/* watchdog timer implementation */' in watchdog.c, got: {result.stdout!r}"
    )
