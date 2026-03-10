import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_settings_ini_has_conflict():
    path = os.path.join(REPO_DIR, "settings.ini")
    assert os.path.isfile(path), "settings.ini not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "settings.ini should have conflict markers."


def test_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "settings.ini" in result.stdout


def test_report_files_not_created_yet():
    for f in ["pre_resolve.txt", "post_resolve.txt", "final_status.txt", "final_log.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
