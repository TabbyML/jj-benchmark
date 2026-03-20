import os
import subprocess
import pytest

REPO = "/home/user/widget-engine"


def run(cmd, cwd=None):
    result = subprocess.run(["jj", "--no-pager"] + list(cmd), capture_output=True, text=True, cwd=cwd)
    return result


def test_no_mixed_commit_in_history():
    """The 'add API endpoint and fix login bug' commit must not exist."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint and fix login bug")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    assert "add API endpoint and fix login bug" not in result.stdout


def test_no_wip_bump_version_in_history():
    """The 'wip: bump version' commit must not exist."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"wip: bump version")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    assert "wip: bump version" not in result.stdout


def test_no_fixup_commit_in_history():
    """The fixup commit must not exist."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"fixup: missing newline in release notes")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    assert "fixup: missing newline in release notes" not in result.stdout


def test_fix_login_bug_commit_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"fix login bug")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    assert "fix login bug" in result.stdout


def test_add_api_endpoint_commit_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    # Must match exactly "add API endpoint" — not "add API endpoint and fix login bug"
    lines = result.stdout.strip().splitlines()
    descs = [l.strip() for l in lines if l.strip()]
    assert any(d.rstrip() == "add API endpoint" for d in descs), \
        f"Expected 'add API endpoint' commit, got: {descs}"


def test_bump_version_description_correct():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"bump version to 2.3.0")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    assert "bump version to 2.3.0" in result.stdout


def test_fix_login_bug_contains_only_auth_py():
    result = run(
        ["show", "--name-only",
         "-r", 'description(substring:"fix login bug")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj show failed: {result.stderr}"
    assert "src/auth.py" in result.stdout
    assert "src/api.py" not in result.stdout


def test_add_api_endpoint_contains_only_api_py():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint")'],
        cwd=REPO,
    )
    assert result.returncode == 0
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    # Find the exact "add API endpoint" commit
    exact_commits = [l for l in lines if l.rstrip() == "add API endpoint"]
    assert len(exact_commits) == 1, f"Expected exactly 1 'add API endpoint' commit, got: {lines}"

    result2 = run(
        ["show", "--name-only",
         "-r", 'description(exact:"add API endpoint\n")'],
        cwd=REPO,
    )
    if result2.returncode != 0:
        # Try substring match — but must not contain auth.py
        result2 = run(
            ["show", "--name-only",
             "-r", 'description(substring:"add API endpoint") ~ description(substring:"fix login bug")'],
            cwd=REPO,
        )
    assert result2.returncode == 0, f"jj show failed: {result2.stderr}"
    assert "src/api.py" in result2.stdout
    assert "src/auth.py" not in result2.stdout


def test_add_release_notes_contains_release_notes_md():
    result = run(
        ["show", "--name-only",
         "-r", 'description(substring:"add release notes")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj show failed: {result.stderr}"
    assert "RELEASE_NOTES.md" in result.stdout


def test_bump_version_commit_contains_version_txt():
    result = run(
        ["show", "--name-only",
         "-r", 'description(substring:"bump version to 2.3.0")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj show failed: {result.stderr}"
    assert "version.txt" in result.stdout


def test_fix_login_bug_is_ancestor_of_add_api_endpoint():
    """fix login bug should be the parent of add API endpoint."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint") & description(substring:"fix login bug")+'],
        cwd=REPO,
    )
    # If fix login bug is parent of add API endpoint, this intersection should be non-empty
    # Actually let's verify differently: add API endpoint's parent should be fix login bug
    result2 = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint")-'],
        cwd=REPO,
    )
    assert result2.returncode == 0
    assert "fix login bug" in result2.stdout, \
        f"Parent of 'add API endpoint' should be 'fix login bug', got: {result2.stdout}"


def test_bookmark_release_v23_points_to_bump_version():
    """release/v2.3 bookmark must point to the 'bump version to 2.3.0' commit."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", "release/v2.3"],
        cwd=REPO,
    )
    assert result.returncode == 0, f"Failed to resolve bookmark: {result.stderr}"
    assert "bump version to 2.3.0" in result.stdout, \
        f"release/v2.3 bookmark does not point to 'bump version to 2.3.0', got: {result.stdout}"


def test_linear_chain_has_five_meaningful_commits():
    """History should have exactly 5 non-empty commits from root to the bump version commit."""
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", "root()..release/v2.3"],
        cwd=REPO,
    )
    assert result.returncode == 0
    descriptions = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(descriptions) == 5, \
        f"Expected 5 commits from root to release/v2.3, got {len(descriptions)}: {descriptions}"
