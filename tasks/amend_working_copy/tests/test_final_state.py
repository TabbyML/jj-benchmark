import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_working_copy_description_amended():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement hello function" in result.stdout, (
        f"Expected 'feat: implement hello function', got: {result.stdout.strip()}"
    )


def test_wip_description_gone():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: add feature" not in result.stdout, "'wip: add feature' still present — amend was not applied."


def test_feature_py_unchanged():
    path = os.path.join(REPO_DIR, "feature.py")
    content = open(path).read()
    assert "def hello():" in content, "feature.py content changed unexpectedly."
    assert "pass" in content, "feature.py content changed unexpectedly."


def test_desc_log_exists_and_correct():
    log_path = os.path.join(REPO_DIR, "desc.log")
    assert os.path.isfile(log_path), f"desc.log not found at {log_path}."
    content = open(log_path).read()
    assert "feat: implement hello function" in content, (
        f"desc.log should contain 'feat: implement hello function', got: {content.strip()}"
    )


def test_exactly_two_commits_above_root():
    result = run_jj(["log", "--no-graph", "-r", "root()..@", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descriptions = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descriptions) == 2, f"Expected exactly 2 commits above root, found {len(descriptions)}: {descriptions}"
