import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "main" in result.stdout, "main bookmark not found"


def test_commits_above_main_exist():
    result = run_jj(["log", "--no-graph", "-r", "main..", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descs) >= 3, f"Expected at least 3 commits above main, got {len(descs)}"


def test_build_pipeline_commit_exists():
    result = run_jj(["log", "--no-graph", "-r", "main..", "-T", 'description ++ "\n"'])
    assert "feat: add build pipeline" in result.stdout, \
        "'feat: add build pipeline' commit not found"


def test_ci_metadata_does_not_exist_yet():
    assert not os.path.isfile("/home/user/ci_metadata.json"), \
        "/home/user/ci_metadata.json should not exist yet."


def test_ci_diff_stats_does_not_exist_yet():
    assert not os.path.isfile("/home/user/ci_diff_stats.txt"), \
        "/home/user/ci_diff_stats.txt should not exist yet."


def test_bookmark_does_not_exist_yet():
    result = run_jj(["bookmark", "list"])
    assert "ci-metadata-exported" not in result.stdout, \
        "ci-metadata-exported bookmark should not exist yet."
