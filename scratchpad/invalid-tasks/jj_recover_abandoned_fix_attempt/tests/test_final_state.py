import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(*args, check=True):
    result = subprocess.run(
        ["jj", "--no-pager", "--color", "never"] + list(args),
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"jj command failed: jj {' '.join(args)}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


def test_fix_commit_is_visible_in_log():
    """The abandoned commit must now be visible in jj log."""
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'description(substring:"billing amount rounding error")'
    )
    assert "fix: billing amount rounding error" in result.stdout, (
        "Commit 'fix: billing amount rounding error' is not visible in jj log after recovery"
    )


def test_fix_commit_file_content():
    """The file src/payments/billing.py must exist in the fix commit with correct content."""
    result = run_jj(
        "file", "show",
        "-r", 'description(substring:"billing amount rounding error")',
        "src/payments/billing.py"
    )
    expected = "# Hotfix: round to 2 decimal places\namount = round(amount, 2)\n"
    assert result.stdout == expected, (
        f"src/payments/billing.py content mismatch.\n"
        f"Expected: {repr(expected)}\n"
        f"Got:      {repr(result.stdout)}"
    )


def test_recovered_fix_bookmark_exists():
    """A bookmark named 'recovered-fix' must exist."""
    result = run_jj("bookmark", "list")
    assert "recovered-fix" in result.stdout, (
        "Bookmark 'recovered-fix' does not exist after task completion"
    )


def test_recovered_fix_bookmark_points_to_fix_commit():
    """Bookmark 'recovered-fix' must point to the fix commit."""
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", "recovered-fix"
    )
    assert "billing amount rounding error" in result.stdout, (
        "Bookmark 'recovered-fix' does not point to the 'fix: billing amount rounding error' commit"
    )


def test_invoice_generation_commit_still_visible():
    """The 'feat: add invoice generation' commit must still be visible."""
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'description(substring:"add invoice generation")'
    )
    assert "feat: add invoice generation" in result.stdout, (
        "Commit 'feat: add invoice generation' is no longer visible after recovery"
    )


def test_scaffold_commit_still_visible():
    """The 'feat: initial payments service scaffold' commit must still be visible."""
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'description(substring:"initial payments service scaffold")'
    )
    assert "feat: initial payments service scaffold" in result.stdout, (
        "Commit 'feat: initial payments service scaffold' is no longer visible after recovery"
    )


def test_main_bookmark_still_points_to_scaffold():
    """Bookmark 'main' must still point to the scaffold commit."""
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", "main"
    )
    assert "initial payments service scaffold" in result.stdout, (
        "Bookmark 'main' no longer points to 'feat: initial payments service scaffold'"
    )


def test_working_copy_is_empty():
    """The working copy commit must have no file changes (be empty)."""
    result = run_jj("status")
    lines = result.stdout.splitlines()
    file_change_lines = [
        l for l in lines
        if l.startswith("M ") or l.startswith("A ") or l.startswith("D ")
    ]
    assert len(file_change_lines) == 0, (
        f"Working copy should be empty after task completion, but got changes: {file_change_lines}"
    )
