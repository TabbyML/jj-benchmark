import os
import subprocess
import pytest


HOME_DIR = "/home/user"
REPO_DIR = os.path.join(HOME_DIR, "support-repo")
RECOVERED_DESCRIPTION = "fix: patch null pointer dereference in request handler"


def test_recovered_commit_visible_in_log():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-T", "description", "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert RECOVERED_DESCRIPTION in result.stdout, (
        f"Expected commit description '{RECOVERED_DESCRIPTION}' not found in jj log.\n"
        f"Output was:\n{result.stdout}"
    )


def test_recovered_commit_visible_in_default_log():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert RECOVERED_DESCRIPTION in result.stdout, (
        f"Recovered commit not in default jj log (should be reachable from working copy).\n"
        f"Output was:\n{result.stdout}"
    )


def test_recovered_commit_has_handler_file():
    # Find the commit by description
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-T", "change_id", "-r",
         f"description('{RECOVERED_DESCRIPTION}')"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Could not find commit with description '{RECOVERED_DESCRIPTION}': {result.stderr}"
    )
    change_id = result.stdout.strip().split()[0]
    assert change_id, "Could not extract change ID for recovered commit"

    file_result = subprocess.run(
        ["jj", "file", "show", "-r", change_id, "src/handler.py"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert file_result.returncode == 0, (
        f"src/handler.py not found in recovered commit (change_id={change_id}): "
        f"{file_result.stderr}"
    )


def test_handler_file_content():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-T", "change_id", "-r",
         f"description('{RECOVERED_DESCRIPTION}')"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    change_id = result.stdout.strip().split()[0]

    file_result = subprocess.run(
        ["jj", "file", "show", "-r", change_id, "src/handler.py"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert file_result.returncode == 0, f"Could not read src/handler.py: {file_result.stderr}"
    content = file_result.stdout
    assert "def handle_request(req):" in content, (
        f"Expected 'def handle_request(req):' in src/handler.py. Got:\n{content}"
    )
    assert "if req is None: return" in content, (
        f"Expected 'if req is None: return' in src/handler.py. Got:\n{content}"
    )


def test_op_log_has_multiple_operations():
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager", "--no-graph", "-T", "id"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    op_ids = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(op_ids) >= 2, (
        f"Expected at least 2 operations in op log (including the undo). "
        f"Found {len(op_ids)}: {op_ids}"
    )


def test_op_log_has_undo_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-pager", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "undo" in result.stdout.lower(), (
        f"Expected an 'undo' operation in op log. Got:\n{result.stdout}"
    )
