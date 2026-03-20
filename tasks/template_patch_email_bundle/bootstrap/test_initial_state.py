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


def test_feature_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "feature" in result.stdout, "feature bookmark not found"


def test_four_commits_above_main():
    result = run_jj(["log", "--no-graph", "-r", "main..feature", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descs) == 4, f"Expected 4 commits above main on feature, got {len(descs)}: {descs}"


def test_config_parser_commit_exists():
    result = run_jj(["log", "--no-graph", "-r", "main..feature", "-T", 'description ++ "\n"'])
    assert "feat: implement config parser" in result.stdout, "config parser commit not found"


def test_validation_commit_exists():
    result = run_jj(["log", "--no-graph", "-r", "main..feature", "-T", 'description ++ "\n"'])
    assert "feat: add validation layer" in result.stdout, "validation layer commit not found"


def test_cli_commit_exists():
    result = run_jj(["log", "--no-graph", "-r", "main..feature", "-T", 'description ++ "\n"'])
    assert "feat: implement CLI interface" in result.stdout, "CLI interface commit not found"


def test_error_reporting_commit_exists():
    result = run_jj(["log", "--no-graph", "-r", "main..feature", "-T", 'description ++ "\n"'])
    assert "feat: add error reporting" in result.stdout, "error reporting commit not found"


def test_patches_dir_does_not_exist_yet():
    assert not os.path.isdir("/home/user/patches"), \
        "/home/user/patches/ should not exist yet before the task is completed."


def test_patch_bundle_log_does_not_exist_yet():
    assert not os.path.isfile("/home/user/patch_bundle_log.txt"), \
        "/home/user/patch_bundle_log.txt should not exist yet."
