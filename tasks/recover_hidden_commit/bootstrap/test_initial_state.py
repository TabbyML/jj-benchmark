import os
import subprocess
import pytest

REPO_DIR = "/home/user/kernel-patch"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_directory_exists():
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


def test_makefile_exists_in_visible_history():
    result = subprocess.run(
        ["jj", "file", "list", "-r", 'description(substring:"init: add initial Makefile")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "Makefile" in result.stdout, "Makefile not found in 'init: add initial Makefile' commit"


def test_irq_file_exists_in_visible_history():
    result = subprocess.run(
        ["jj", "file", "list", "-r", 'description(substring:"refactor: clean up interrupt handler")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "irq.c" in result.stdout, "irq.c not found in 'refactor: clean up interrupt handler' commit"


def test_hidden_commit_discoverable_via_at_operation():
    result = subprocess.run(
        ["jj", "log", "-r", "at_operation(@-, all())", "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log at_operation(@-, all()) failed: {result.stderr}"
    assert "feat: add watchdog timer support" in result.stdout, (
        "Hidden commit 'feat: add watchdog timer support' not found via at_operation(@-, all())"
    )


def test_watchdog_change_id_retrievable_via_at_operation():
    result = subprocess.run(
        [
            "jj", "log",
            "-r", 'at_operation(@-, all()) & description(substring:"watchdog")',
            "--no-graph",
            "-T", "change_id",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for hidden commit change_id failed: {result.stderr}"
    change_id = result.stdout.strip()
    assert change_id, "Could not get change_id for hidden watchdog commit"


def test_watchdog_not_in_default_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add watchdog timer support" not in result.stdout, (
        "Watchdog commit should be hidden (not in default visible log)"
    )
