import os
import subprocess
import pytest

REPO_DIR = "/home/user/audit-repo"


def test_no_draft_revisions_remain():
    """After the task, no revision should have a description starting with 'draft:'."""
    result = subprocess.run(
        ["jj", "--no-pager", "log",
         "-r", 'description(glob:"draft:*")',
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Draft revisions still exist: {result.stdout.strip()}"
    )


def test_exactly_four_named_revisions():
    """After pruning, exactly 4 non-empty, non-working-copy revisions should exist."""
    result = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "all()",
         "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # descriptions that are non-empty (skip empty working copy change)
    descriptions = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    named = [d for d in descriptions if d != "(no description set)"]
    assert len(named) == 4, (
        f"Expected exactly 4 named revisions, got {len(named)}: {named}"
    )


def test_revision_descriptions_in_order():
    """The 4 revisions must have specific descriptions, forming the cleaned audit trail."""
    result = subprocess.run(
        ["jj", "--no-pager", "log",
         "-r", "roots(all())::audit-main",
         "--no-graph", "--reversed", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected = [
        "init: scaffold audit repo",
        "feat: add ingestion pipeline",
        "feat: add transformation step",
        "feat: add reporting module",
    ]
    assert lines == expected, (
        f"Revision descriptions don't match.\nExpected: {expected}\nGot: {lines}"
    )


def test_audit_main_points_to_reporting_module():
    """The audit-main bookmark must point to 'feat: add reporting module'."""
    result = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "audit-main",
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add reporting module" in result.stdout, (
        f"audit-main does not point to 'feat: add reporting module': {result.stdout}"
    )


def test_files_at_audit_main_are_correct():
    """The audit-main tip should contain exactly the four expected files."""
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list", "-r", "audit-main"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    files = set(result.stdout.strip().splitlines())
    expected_files = {
        "README.md",
        "pipelines/ingest.py",
        "pipelines/transform.py",
        "reports/summary.py",
    }
    assert expected_files.issubset(files), (
        f"Expected files {expected_files} not all present. Got: {files}"
    )


def test_validate_wip_absent_at_audit_main():
    """pipelines/validate_wip.py must NOT be present at the audit-main tip."""
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list", "-r", "audit-main"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/validate_wip.py" not in result.stdout, (
        "pipelines/validate_wip.py should not be present at audit-main"
    )


def test_dedup_exp_absent_at_audit_main():
    """pipelines/dedup_exp.py must NOT be present at the audit-main tip."""
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list", "-r", "audit-main"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/dedup_exp.py" not in result.stdout, (
        "pipelines/dedup_exp.py should not be present at audit-main"
    )


def test_working_copy_parent_is_reporting_module():
    """The working-copy's parent (@-) must be 'feat: add reporting module'."""
    result = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "@-",
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add reporting module" in result.stdout, (
        f"Working copy parent is not 'feat: add reporting module': {result.stdout}"
    )


def test_audit_main_is_parent_of_working_copy():
    """audit-main bookmark should point to the same revision as @-."""
    # Get the commit id of audit-main
    r1 = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "audit-main",
         "--no-graph", "-T", "commit_id"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert r1.returncode == 0, f"jj log audit-main failed: {r1.stderr}"
    bookmark_commit = r1.stdout.strip()

    # Get the commit id of @-
    r2 = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "@-",
         "--no-graph", "-T", "commit_id"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert r2.returncode == 0, f"jj log @- failed: {r2.stderr}"
    parent_commit = r2.stdout.strip()

    assert bookmark_commit == parent_commit, (
        f"audit-main ({bookmark_commit}) does not match @- ({parent_commit})"
    )
