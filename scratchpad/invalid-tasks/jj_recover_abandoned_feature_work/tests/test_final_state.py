import os
import shutil
import subprocess
import pytest


REPO_DIR = "/home/user/project"


def test_recovered_commit_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add login page skeleton" in result.stdout, \
        "Expected 'add login page skeleton' commit to be visible in jj log after recovery"


def test_working_copy_parent_is_recovered_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "@-"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log @- failed: {result.stderr}"
    assert "add login page skeleton" in result.stdout, \
        "Expected working copy parent (@-) to have description 'add login page skeleton'"


def test_login_py_file_exists():
    login_file = os.path.join(REPO_DIR, "login.py")
    assert os.path.isfile(login_file), \
        f"Expected file login.py to exist at {login_file}"


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


def test_recovered_commit_not_abandoned():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ ' abandoned=' ++ if(description.contains('add login page skeleton'), 'found', 'not-found')", "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    # Check via a targeted query: the commit with that description must exist and not be abandoned
    result2 = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r", "description('add login page skeleton')"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result2.returncode == 0, \
        f"Could not find 'add login page skeleton' commit via revset: {result2.stderr}"
    assert "add login page skeleton" in result2.stdout, \
        "The 'add login page skeleton' commit is not accessible (still abandoned or missing)"
