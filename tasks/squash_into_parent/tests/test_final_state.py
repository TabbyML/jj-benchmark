import os
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_exactly_two_commits_above_root():
    result = run_jj(["log", "--no-graph", "-r", "root()..@", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descs) == 2, f"Expected 2 commits above root, found {len(descs)}: {descs}"


def test_combined_commit_description():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "build: add lint target with error-only flag" in result.stdout, (
        f"Expected 'build: add lint target with error-only flag', got: {result.stdout.strip()}"
    )


def test_fixup_commit_gone():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: fixup lint flag" not in result.stdout, "'wip: fixup lint flag' still present — squash not done."


def test_makefile_has_errors_only():
    path = os.path.join(REPO_DIR, "Makefile")
    content = open(path).read()
    assert "pylint --errors-only src/" in content, "Makefile missing 'pylint --errors-only src/' after squash."


def test_log_file_exists():
    log_path = os.path.join(REPO_DIR, "log.txt")
    assert os.path.isfile(log_path), f"log.txt not found at {log_path}."
    assert len(open(log_path).read().strip()) > 0, "log.txt is empty."


def test_base_commit_still_present():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "build: add base Makefile" in result.stdout, "'build: add base Makefile' missing from log."
