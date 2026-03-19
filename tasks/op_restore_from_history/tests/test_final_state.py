import os
import subprocess
import pytest


REPO_DIR = "/home/user/project"


def test_refactor_py_exists():
    refactor_path = os.path.join(REPO_DIR, "refactor.py")
    assert os.path.isfile(refactor_path), (
        f"refactor.py should exist after recovery: {refactor_path}"
    )


def test_refactor_py_content():
    refactor_path = os.path.join(REPO_DIR, "refactor.py")
    with open(refactor_path, "r") as fh:
        content = fh.read()
    assert "# refactor module" in content, (
        f"refactor.py should contain '# refactor module', got: {content!r}"
    )


def test_base_py_exists():
    base_path = os.path.join(REPO_DIR, "base.py")
    assert os.path.isfile(base_path), (
        f"base.py should still exist after recovery: {base_path}"
    )


def test_base_py_content():
    base_path = os.path.join(REPO_DIR, "base.py")
    with open(base_path, "r") as fh:
        content = fh.read()
    assert "# base module" in content, (
        f"base.py should contain '# base module', got: {content!r}"
    )


def test_add_base_module_commit_visible():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add base module" in result.stdout, (
        f"'add base module' commit should be visible after recovery: {result.stdout}"
    )


def test_refactor_squash_target_commit_visible():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "refactor: squash target" in result.stdout, (
        f"'refactor: squash target' commit should be visible as a separate commit after recovery: "
        f"{result.stdout}"
    )


def test_both_commits_are_separate():
    # Verify that "add base module" and "refactor: squash target" are separate commits
    # by checking their descriptions appear in separate revisions
    result = subprocess.run(
        [
            "jj", "log", "--no-graph", "-T", "description ++ '\\n'",
            "-r", "::@ ~ root()",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # Count commits with the known descriptions
    lines = result.stdout.splitlines()
    descriptions = [ln.strip() for ln in lines if ln.strip()]
    has_base = any("add base module" in d and "refactor" not in d for d in descriptions)
    has_refactor = any("refactor: squash target" in d for d in descriptions)
    assert has_base and has_refactor, (
        f"Both 'add base module' and 'refactor: squash target' should be separate commits. "
        f"Got descriptions: {descriptions}"
    )


def test_op_log_has_restore_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\\n'"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "restore" in result.stdout.lower(), (
        f"Expected a 'restore' operation in op log, got: {result.stdout}"
    )


def test_op_log_most_recent_is_restore():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\\n'", "-n", "1"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "restore" in result.stdout.lower(), (
        f"Most recent operation should be a 'restore', got: {result.stdout}"
    )


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
