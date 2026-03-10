import os
import shutil
import subprocess
import pytest


REPO_DIR = "/home/user/support-repo"


def test_recovered_commit_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "ticket-1042" in result.stdout, \
        "Expected 'ticket-1042' commit to be visible in jj log after recovery"


def test_working_copy_parent_is_recovered_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "@-"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log @- failed: {result.stderr}"
    assert "ticket-1042" in result.stdout, \
        "Expected working-copy parent (@-) description to contain 'ticket-1042'"


def test_auth_fix_py_file_exists():
    auth_fix = os.path.join(REPO_DIR, "auth_fix.py")
    assert os.path.isfile(auth_fix), \
        f"Expected file auth_fix.py to exist at {auth_fix}"


def test_main_bookmark_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, \
        "Expected 'main' bookmark to still exist after recovery"


def test_recovered_commit_accessible_via_revset():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", "description('ticket-1042')"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, \
        f"Could not find ticket-1042 commit via revset description(): {result.stderr}"
    assert "ticket-1042" in result.stdout, \
        "The ticket-1042 commit is not accessible (still abandoned or missing)"
