import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_working_copy_description():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add helper" in result.stdout, (
        f"Expected '@' to be 'feat: add helper', got: {result.stdout.strip()}"
    )


def test_parent_is_project_setup():
    result = run_jj(["log", "--no-graph", "-r", "@-", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: project setup" in result.stdout, (
        f"Parent of @ should be 'chore: project setup', got: {result.stdout.strip()}"
    )


def test_two_commits_above_root():
    result = run_jj(["log", "--no-graph", "-r", "root()..@", "-T", 'description ++ "\\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descs) == 2, (
        f"Expected 2 commits above root after rebase, found {len(descs)}: {descs}"
    )


def test_both_files_exist():
    assert os.path.isfile(os.path.join(REPO_DIR, "main.py")), "main.py not found after rebase."
    assert os.path.isfile(os.path.join(REPO_DIR, "helper.py")), "helper.py not found after rebase."


def test_rebase_log_exists():
    log_path = os.path.join(REPO_DIR, "rebase.log")
    assert os.path.isfile(log_path), f"rebase.log not found at {log_path}."
    content = open(log_path).read()
    assert "chore: project setup" in content, "rebase.log missing 'chore: project setup'."
    assert "feat: add helper" in content, "rebase.log missing 'feat: add helper'."
