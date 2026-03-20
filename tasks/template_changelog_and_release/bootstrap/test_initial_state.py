import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/release-repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"


def test_v1_0_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "v1.0", "-T", 'description'])
    assert result.returncode == 0, f"v1.0 bookmark not found: {result.stderr}"
    assert "release: v1.0 baseline" in result.stdout, f"v1.0 bookmark should point to 'release: v1.0 baseline', got: {result.stdout.strip()}"


def test_main_bookmark_exists():
    result = run_jj(["log", "--no-graph", "-r", "main", "-T", 'description'])
    assert result.returncode == 0, f"main bookmark not found: {result.stderr}"
    assert "feat: add dark mode" in result.stdout, f"main bookmark should point to 'feat: add dark mode', got: {result.stdout.strip()}"


def test_all_six_commits_present():
    result = run_jj(["log", "--no-graph", "-r", "v1.0..main", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "feat: new dashboard UI" in log, "Expected 'feat: new dashboard UI' not found."
    assert "fix: correct login redirect" in log, "Expected 'fix: correct login redirect' not found."
    assert "feat: add CSV export" in log, "Expected 'feat: add CSV export' not found."
    assert "fix: prevent XSS in user input" in log, "Expected 'fix: prevent XSS in user input' not found."
    assert "chore: update dependencies" in log, "Expected 'chore: update dependencies' not found."
    assert "feat: add dark mode" in log, "Expected 'feat: add dark mode' not found."


def test_author_metadata_alice():
    result = run_jj(["log", "--no-graph", "-r", 'author("alice@company.com") & (v1.0..main)', "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log for Alice failed: {result.stderr}"
    assert "feat: new dashboard UI" in result.stdout, "Alice's 'feat: new dashboard UI' not found."
    assert "feat: add CSV export" in result.stdout, "Alice's 'feat: add CSV export' not found."


def test_author_metadata_bob():
    result = run_jj(["log", "--no-graph", "-r", 'author("bob@company.com") & (v1.0..main)', "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log for Bob failed: {result.stderr}"
    assert "fix: correct login redirect" in result.stdout, "Bob's 'fix: correct login redirect' not found."
    assert "chore: update dependencies" in result.stdout, "Bob's 'chore: update dependencies' not found."


def test_author_metadata_charlie():
    result = run_jj(["log", "--no-graph", "-r", 'author("charlie@company.com") & (v1.0..main)', "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log for Charlie failed: {result.stderr}"
    assert "fix: prevent XSS in user input" in result.stdout, "Charlie's 'fix: prevent XSS in user input' not found."
    assert "feat: add dark mode" in result.stdout, "Charlie's 'feat: add dark mode' not found."
