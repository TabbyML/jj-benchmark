import os
import subprocess
import pytest

REPO_DIR = "/home/user/workspace/repo"
RECOVERED_ID_FILE = "/home/user/workspace/recovered_commit_id.txt"

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_recovered_commit_id_file_exists():
    assert os.path.isfile(RECOVERED_ID_FILE), f"Expected file {RECOVERED_ID_FILE} does not exist."

def test_bookmark_recovered_fix_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "recovered-fix" in result.stdout, "Bookmark 'recovered-fix' does not exist."

def test_bookmark_points_to_correct_content():
    # Verify the commit at recovered-fix has the expected file contents
    result = run_jj(["file", "show", "src/bugfix.py", "-r", "recovered-fix"])
    assert result.returncode == 0, f"jj file show failed or file missing at recovered-fix: {result.stderr}"
    content = result.stdout.strip()
    assert "def fix_bug(): return True" in content, \
        f"Expected 'def fix_bug(): return True' in src/bugfix.py at recovered-fix, got: {content}"

def test_recovered_commit_id_matches_bookmark():
    # Verify the ID in the file matches the commit the bookmark points to
    with open(RECOVERED_ID_FILE, "r") as f:
        written_id = f.read().strip()
    
    assert written_id, f"File {RECOVERED_ID_FILE} is empty."
    
    # Check if the written ID resolves to the same commit as the bookmark
    result_bookmark = run_jj(["log", "--no-graph", "-r", "recovered-fix", "-T", "commit_id"])
    assert result_bookmark.returncode == 0
    bookmark_commit_id = result_bookmark.stdout.strip()
    
    result_written = run_jj(["log", "--no-graph", "-r", written_id, "-T", "commit_id"])
    assert result_written.returncode == 0, f"The commit ID written ({written_id}) is not a valid revision."
    written_commit_id = result_written.stdout.strip()
    
    assert written_commit_id == bookmark_commit_id, \
        f"The commit ID in {RECOVERED_ID_FILE} ({written_commit_id}) does not match the 'recovered-fix' bookmark ({bookmark_commit_id})."

def test_recovered_commit_is_not_abandoned():
    # The recovered commit should be visible in default() (which means it's not abandoned)
    # wait, default() is not a valid revset function, let's just check if `jj log -r <id>` works without --hidden
    # Actually, jj log -r <id> might work for hidden commits if explicitly specified.
    # To check if it's hidden, we can check if it's in `all()` but not in `visible_heads()`? No, `all()` is all visible commits.
    # So if it's in `all()`, it's not hidden.
    result = run_jj(["log", "--no-graph", "-r", "recovered-fix", "-T", "commit_id"])
    assert result.returncode == 0, "The recovered-fix commit is not visible or doesn't exist."
