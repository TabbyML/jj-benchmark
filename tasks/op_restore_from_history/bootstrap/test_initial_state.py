import os
import subprocess
import pytest


REPO_DIR = "/home/user/project"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["jj", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj not found in PATH: {result.stderr}"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory does not exist: {REPO_DIR}"


def test_jj_repo_dot_jj_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in repo: {jj_dir}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_add_base_module_commit_visible():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add base module" in result.stdout, (
        f"'add base module' not found in visible log: {result.stdout}"
    )


def test_squash_target_commit_not_visible():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "refactor: squash target" not in result.stdout, (
        "The 'refactor: squash target' commit should NOT be visible before recovery: "
        f"{result.stdout}"
    )


def test_base_py_exists():
    base_path = os.path.join(REPO_DIR, "base.py")
    assert os.path.isfile(base_path), (
        f"base.py should exist in the repo: {base_path}"
    )


def test_refactor_py_exists_in_merged_commit():
    # After squash, refactor.py should still exist on disk (its content was merged in)
    refactor_path = os.path.join(REPO_DIR, "refactor.py")
    assert os.path.isfile(refactor_path), (
        f"refactor.py should exist on disk (squashed into parent): {refactor_path}"
    )


def test_operation_log_has_squash_operation():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description ++ '\\n'"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "squash" in result.stdout.lower(), (
        f"Expected a 'squash' operation in op log, got: {result.stdout}"
    )


def test_only_one_non_root_non_wc_commit_visible():
    # Before recovery, only "add base module" should appear (squash target was merged in)
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
    descriptions = [d for d in result.stdout.strip().splitlines() if d.strip()]
    # Should have the merged commit and the empty working copy (empty desc)
    named = [d for d in descriptions if d.strip()]
    # "add base module" should be present; "refactor: squash target" should not be separate
    assert "refactor: squash target" not in result.stdout, (
        f"'refactor: squash target' should not be a separate commit yet: {result.stdout}"
    )
