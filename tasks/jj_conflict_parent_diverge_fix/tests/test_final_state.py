import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_params_env_resolved():
    path = os.path.join(REPO_DIR, "params.env")
    content = open(path).read()
    assert "<<<<<<<" not in content, "params.env still has conflict markers."
    assert "DB_HOST=db.prod.internal" in content
    assert "DB_PORT=5433" in content


def test_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_diverge_conflicts_txt_exists():
    path = os.path.join(REPO_DIR, "diverge_conflicts.txt")
    assert os.path.isfile(path), "diverge_conflicts.txt missing."
    assert "params.env" in open(path).read()


def test_final_params_txt_exists():
    path = os.path.join(REPO_DIR, "final_params.txt")
    assert os.path.isfile(path), "final_params.txt missing."
    content = open(path).read()
    assert "DB_HOST=db.prod.internal" in content
    assert "DB_PORT=5433" in content


def test_verify_txt_empty():
    path = os.path.join(REPO_DIR, "verify.txt")
    assert os.path.isfile(path), "verify.txt missing."
    assert open(path).read().strip() == ""


def test_commit_description():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "ops: merge DB params" in result.stdout
