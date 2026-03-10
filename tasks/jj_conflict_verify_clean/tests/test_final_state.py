import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_pre_resolve_txt_has_settings_ini():
    path = os.path.join(REPO_DIR, "pre_resolve.txt")
    assert os.path.isfile(path), "pre_resolve.txt missing."
    assert "settings.ini" in open(path).read()


def test_settings_ini_resolved():
    path = os.path.join(REPO_DIR, "settings.ini")
    content = open(path).read()
    assert "<<<<<<<" not in content, "settings.ini still has conflict markers."
    assert "mode=production" in content, f"Expected mode=production. Got: {content}"
    assert "log_level=info" in content, f"Expected log_level=info. Got: {content}"


def test_post_resolve_txt_is_empty():
    path = os.path.join(REPO_DIR, "post_resolve.txt")
    assert os.path.isfile(path), "post_resolve.txt missing."
    assert open(path).read().strip() == "", "post_resolve.txt should be empty after resolution."


def test_final_status_txt_exists():
    path = os.path.join(REPO_DIR, "final_status.txt")
    assert os.path.isfile(path), "final_status.txt missing."


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: set debug mode (resolved)" in result.stdout


def test_final_log_txt_exists():
    path = os.path.join(REPO_DIR, "final_log.txt")
    assert os.path.isfile(path), "final_log.txt missing."
    content = open(path).read()
    assert "feat: set debug mode (resolved)" in content or "main: set production mode" in content
