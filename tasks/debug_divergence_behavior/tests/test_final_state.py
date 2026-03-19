import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
RESOLVED_CHANGE_ID_FILE = "/home/user/resolved_change_id.txt"
MAIN_CONTENT_FILE = "/home/user/main_content.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_no_divergent_commits():
    # If a commit is divergent, jj log -r 'bookmarks(exact:feature)' will show multiple commits,
    # or the bookmark itself will be conflicted and error out when referenced as `feature`.
    # We can check if 'feature' resolves to exactly one commit.
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", "commit_id ++ \"\\n\""])
    assert result.returncode == 0, f"jj log failed, 'feature' bookmark might still be conflicted: {result.stderr}"
    lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    assert len(lines) == 1, f"Expected exactly 1 commit for 'feature' bookmark, found {len(lines)}. Divergence not resolved."

def test_resolved_change_id_file():
    assert os.path.isfile(RESOLVED_CHANGE_ID_FILE), f"{RESOLVED_CHANGE_ID_FILE} does not exist."
    with open(RESOLVED_CHANGE_ID_FILE, "r") as f:
        written_id = f.read().strip()
    
    # Get the actual change ID of the feature bookmark
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", "change_id"])
    assert result.returncode == 0, f"Failed to get change ID for 'feature': {result.stderr}"
    actual_id = result.stdout.strip()
    
    assert written_id == actual_id, f"Expected change ID '{actual_id}', but found '{written_id}' in {RESOLVED_CHANGE_ID_FILE}."

def test_main_content_file():
    assert os.path.isfile(MAIN_CONTENT_FILE), f"{MAIN_CONTENT_FILE} does not exist."
    with open(MAIN_CONTENT_FILE, "r") as f:
        content = f.read()
    
    # The combined content should have both the local feature print and the remote bugfix print.
    assert "local feature" in content, "The resolved main.py content is missing the 'local feature' changes."
    assert "remote bugfix" in content, "The resolved main.py content is missing the 'remote bugfix' changes."
    assert "<<<<<<<" not in content, "The resolved main.py content still contains conflict markers."
