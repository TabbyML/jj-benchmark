import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(*args, check=True):
    result = subprocess.run(
        ["jj", "--no-pager"] + list(args),
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"jj command failed: jj {' '.join(args)}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


def test_jj_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_dir_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_repo_is_valid_jj_repo():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), (
        f"No .jj directory found in {REPO_DIR} — not a valid jj repository"
    )


def test_jj_status_succeeds():
    run_jj("status")


def test_commit_initial_scaffold_visible():
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'description(substring:"initial payments service scaffold")'
    )
    assert "feat: initial payments service scaffold" in result.stdout, (
        "Commit 'feat: initial payments service scaffold' not visible in jj log"
    )


def test_commit_invoice_generation_visible():
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'description(substring:"add invoice generation")'
    )
    assert "feat: add invoice generation" in result.stdout, (
        "Commit 'feat: add invoice generation' not visible in jj log"
    )


def test_bookmark_main_exists():
    result = run_jj("bookmark", "list")
    assert "main" in result.stdout, (
        "Bookmark 'main' does not exist in the repository"
    )


def test_bookmark_main_points_to_scaffold():
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", "main"
    )
    assert "initial payments service scaffold" in result.stdout, (
        "Bookmark 'main' does not point to 'feat: initial payments service scaffold'"
    )


def test_fix_commit_is_abandoned():
    result = run_jj(
        "log", "--no-graph",
        "-T", "description",
        "-r", 'all()'
    )
    assert "billing amount rounding error" not in result.stdout, (
        "The commit 'fix: billing amount rounding error' should be abandoned (not visible in jj log) initially"
    )


def test_op_log_contains_abandon_operation():
    result = run_jj("op", "log", "--no-graph", "-T", "description")
    assert "abandon" in result.stdout.lower(), (
        "Operation log does not contain an abandon operation — expected an 'abandon commit' entry"
    )


def test_working_copy_is_empty_change():
    result = run_jj("status")
    # The working copy should not show any tracked changes (it's an empty change)
    # An empty working copy typically says "The working copy is clean" or shows no M/A/D lines
    # We check that there are no Modified/Added/Deleted lines for tracked files
    lines = result.stdout.splitlines()
    file_change_lines = [
        l for l in lines
        if l.startswith("M ") or l.startswith("A ") or l.startswith("D ")
    ]
    assert len(file_change_lines) == 0, (
        f"Working copy should be empty (no file changes), but got: {file_change_lines}"
    )


def test_no_recovered_fix_bookmark_yet():
    result = run_jj("bookmark", "list")
    assert "recovered-fix" not in result.stdout, (
        "Bookmark 'recovered-fix' should not exist before the task is completed"
    )
