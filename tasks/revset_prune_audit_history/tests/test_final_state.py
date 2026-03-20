import os
import subprocess
import pytest

REPO_DIR = "/home/user/audit-repo"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_wip_commits_abandoned():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "WIP: data ingest part 1" not in result.stdout, "Commit 'WIP: data ingest part 1' still exists in visible history."
    assert "WIP: data ingest part 2" not in result.stdout, "Commit 'WIP: data ingest part 2' still exists in visible history."

def test_main_bookmark_position():
    result = run_jj(["log", "--no-graph", "-r", "main", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Audit log entry 3" in result.stdout, f"Expected bookmark 'main' to point to 'Audit log entry 3', got: {result.stdout.strip()}"

def test_working_copy_commit_description():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Audit log entry 4" in result.stdout, f"Expected working copy description 'Audit log entry 4', got: {result.stdout.strip()}"

def test_working_copy_parent():
    result = run_jj(["log", "--no-graph", "-r", "@-", "-T", 'description'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Audit log entry 3" in result.stdout, f"Expected working copy parent to be 'Audit log entry 3', got: {result.stdout.strip()}"

def test_entry4_file_exists():
    file_path = os.path.join(REPO_DIR, "entry4.txt")
    assert os.path.isfile(file_path), "File 'entry4.txt' does not exist in the working copy."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "data", f"Expected 'entry4.txt' to contain 'data', got: '{content}'"
