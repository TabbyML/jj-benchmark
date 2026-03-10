import os
import subprocess
import shutil
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_available():
    assert shutil.which("jj") is not None


def test_repo_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj"))


def test_build_sh_has_conflict():
    path = os.path.join(REPO_DIR, "build.sh")
    assert os.path.isfile(path), "build.sh not found."
    content = open(path).read()
    assert "<<<<<<<" in content, "build.sh should have conflict markers."


def test_feature_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: custom build" in result.stdout


def test_conflict_listed():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "build.sh" in result.stdout


def test_output_files_not_created():
    for f in ["before_abandon.txt", "after_abandon_log.txt", "final_conflicts.txt", "final_log.txt"]:
        assert not os.path.exists(os.path.join(REPO_DIR, f)), f"{f} should not exist yet."
