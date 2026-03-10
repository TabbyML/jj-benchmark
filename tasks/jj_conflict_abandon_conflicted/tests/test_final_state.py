import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_build_sh_no_conflicts():
    path = os.path.join(REPO_DIR, "build.sh")
    content = open(path).read()
    assert "<<<<<<<" not in content, "build.sh still has conflict markers."


def test_build_sh_has_correct_content():
    path = os.path.join(REPO_DIR, "build.sh")
    content = open(path).read()
    assert "BUILD=10" in content, f"Expected BUILD=10. Got: {content}"
    assert "OPT=fast" in content, f"Expected OPT=fast. Got: {content}"
    assert "CUSTOM=true" in content, f"Expected CUSTOM=true. Got: {content}"


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_clean_commit_created():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: custom build (clean)" in result.stdout


def test_before_abandon_txt_exists():
    path = os.path.join(REPO_DIR, "before_abandon.txt")
    assert os.path.isfile(path), "before_abandon.txt missing."
    assert "build.sh" in open(path).read()


def test_final_conflicts_empty():
    path = os.path.join(REPO_DIR, "final_conflicts.txt")
    assert os.path.isfile(path), "final_conflicts.txt missing."
    assert open(path).read().strip() == ""


def test_final_log_exists():
    path = os.path.join(REPO_DIR, "final_log.txt")
    assert os.path.isfile(path), "final_log.txt missing."
    content = open(path).read()
    assert "feat: custom build (clean)" in content
