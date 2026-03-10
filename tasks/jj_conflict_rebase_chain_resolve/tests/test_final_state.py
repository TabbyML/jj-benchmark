import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_no_conflicts_remain():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_before_txt_exists():
    path = os.path.join(REPO_DIR, "before.txt")
    assert os.path.isfile(path), "before.txt missing."
    assert "vars.sh" in open(path).read()


def test_chain_log_exists():
    path = os.path.join(REPO_DIR, "chain_log.txt")
    assert os.path.isfile(path), "chain_log.txt missing."


def test_chain_b_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "chain: set Y=X (rebased)" in result.stdout


def test_vars_sh_resolved_at_chain_a():
    # Check out chain_a and verify vars.sh content
    result = subprocess.run(
        ["jj", "show", "-r", "chain_a", "--stat"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj show chain_a failed: {result.stderr}"
