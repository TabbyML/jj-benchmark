import subprocess
import pytest

REPO_DIR = "/home/user/project"


def _jj(*args):
    """Run a jj command in REPO_DIR and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["jj"] + list(args),
        capture_output=True,
        cwd=REPO_DIR,
    )
    return result.returncode, result.stdout.decode(), result.stderr.decode()


def test_implement_core_feature_commit_restored():
    """The commit with description 'implement core feature' must be visible."""
    rc, out, err = _jj("log", "--no-pager", "-r", "description(substring:'implement core feature')")
    assert rc == 0, f"jj log failed: {err}"
    assert "implement core feature" in out, (
        f"'implement core feature' not found in log output: {out}"
    )


def test_bad_description_not_present():
    """The bad description 'WIP: bad description do not merge' must NOT be visible in jj log."""
    rc, out, err = _jj("log", "--no-pager", "-r", "description(substring:'WIP: bad description do not merge')")
    # Command should succeed but return no revisions (empty output)
    assert rc == 0, f"jj log command failed unexpectedly: {err}"
    assert "WIP: bad description do not merge" not in out, (
        f"Bad description commit still present after recovery. Output: {out}"
    )


def test_add_tests_commit_restored():
    """The commit with description 'add tests for core feature' must be visible."""
    rc, out, err = _jj("log", "--no-pager", "-r", "description(substring:'add tests for core feature')")
    assert rc == 0, f"jj log failed: {err}"
    assert "add tests for core feature" in out, (
        f"'add tests for core feature' not found in log output: {out}"
    )


def test_all_three_commits_in_history():
    """All three original commits must appear in the full jj log."""
    rc, out, err = _jj("log", "--no-pager")
    assert rc == 0, f"jj log failed: {err}"
    assert "add initial readme" in out, (
        f"'add initial readme' not found in full log: {out}"
    )
    assert "implement core feature" in out, (
        f"'implement core feature' not found in full log: {out}"
    )
    assert "add tests for core feature" in out, (
        f"'add tests for core feature' not found in full log: {out}"
    )


def test_undo_operations_in_oplog():
    """At least one undo operation must appear in jj op log (shown as 'undo:')."""
    rc, out, err = _jj("op", "log", "--no-pager")
    assert rc == 0, f"jj op log failed: {err}"
    # jj op log shows undo entries with "undo: restore to operation ..."
    assert "undo:" in out, (
        f"No undo operation found in op log. Output: {out}"
    )


def test_tests_py_file_accessible():
    """tests.py must be accessible in the 'add tests for core feature' commit."""
    rc, out, err = _jj(
        "file", "list", "--no-pager",
        "-r", "description(substring:'add tests for core feature')"
    )
    assert rc == 0, f"jj file list failed: {err}"
    assert "tests.py" in out, (
        f"tests.py not found in 'add tests for core feature' commit. Output: {out}"
    )


def test_core_py_file_accessible():
    """core.py must be accessible in the 'implement core feature' commit."""
    rc, out, err = _jj(
        "file", "list", "--no-pager",
        "-r", "description(substring:'implement core feature')"
    )
    assert rc == 0, f"jj file list failed: {err}"
    assert "core.py" in out, (
        f"core.py not found in 'implement core feature' commit. Output: {out}"
    )
