import os
import subprocess
import pytest


REPO_DIR = "/home/user/mylib"


def test_no_wip_revisions_remain():
    """After abandoning, the revset for WIP commits should return no results."""
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'change_id ++ "\\n"',
            "-r", 'mutable() & description("") & ~::bookmarks()',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj log revset query failed with rc={result.returncode}:\n{result.stderr}"
    )
    # Strip ANSI escape sequences and check there are no change IDs in the output
    import re
    clean = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
    lines = [line.strip() for line in clean.strip().splitlines() if line.strip()]
    assert len(lines) == 0, (
        f"Expected 0 WIP revisions after abandoning, but found {len(lines)}:\n{result.stdout}"
    )


def test_bookmark_main_still_exists():
    """The 'main' bookmark must still exist after the cleanup."""
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, (
        f"bookmark 'main' not found after cleanup:\n{result.stdout}"
    )


def test_bookmark_feature_core_still_exists():
    """The 'feature/core' bookmark must still exist after the cleanup."""
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/core" in result.stdout, (
        f"bookmark 'feature/core' not found after cleanup:\n{result.stdout}"
    )


def test_readme_still_accessible():
    """README.md must still be accessible via the feature/core revision."""
    result = subprocess.run(
        ["jj", "file", "show", "-r", "feature/core", "README.md"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj file show README.md at feature/core failed: {result.stderr}"
    )
    assert "mylib" in result.stdout, (
        f"README.md content not as expected:\n{result.stdout}"
    )


def test_lib_rs_still_accessible():
    """src/lib.rs must still be accessible via the feature/core revision."""
    result = subprocess.run(
        ["jj", "file", "show", "-r", "feature/core", "src/lib.rs"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj file show src/lib.rs at feature/core failed: {result.stderr}"
    )
    assert "core library" in result.stdout, (
        f"src/lib.rs content not as expected:\n{result.stdout}"
    )


def test_feature_core_commit_still_has_correct_description():
    """The feature/core commit must still have its original description."""
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", "description",
            "-r", "feature/core",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"jj log for feature/core failed: {result.stderr}"
    )
    import re
    clean = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
    assert "Add core library module" in clean, (
        f"feature/core description not as expected:\n{result.stdout}"
    )
