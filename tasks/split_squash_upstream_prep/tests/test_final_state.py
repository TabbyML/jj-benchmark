import os
import subprocess
import pytest

REPO_DIR = "/home/user/mylib"


def run_jj(args, cwd=REPO_DIR):
    """Helper: run a jj command and return CompletedProcess."""
    return subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_working_copy_is_empty():
    result = run_jj(["diff", "--summary"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy (@) should be empty but has changes: {result.stdout!r}"
    )


def test_commit_add_utility_fix_exists():
    result = run_jj(["log", "-r", 'description(substring:"add utility fix")',
                     "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add utility fix" in result.stdout, (
        f"Commit 'add utility fix' not found. stdout: {result.stdout!r}"
    )


def test_commit_add_config_parser_exists():
    result = run_jj(["log", "-r", 'description(substring:"add config parser")',
                     "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # Ensure we match "add config parser" but not "add config parser and update tests"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    exact_matches = [l for l in lines if l.strip() == "add config parser"]
    assert len(exact_matches) >= 1, (
        f"Commit with exact description 'add config parser' not found. stdout: {result.stdout!r}"
    )


def test_commit_add_config_tests_exists():
    result = run_jj(["log", "-r", 'description(substring:"add config tests")',
                     "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add config tests" in result.stdout, (
        f"Commit 'add config tests' not found. stdout: {result.stdout!r}"
    )


def test_mixed_commit_no_longer_exists():
    """The original mixed commit should no longer be in the visible history."""
    result = run_jj(["log", "-r", 'description(exact:"add config parser and update tests\n")',
                     "--no-graph", "-T", 'description ++ "\n"'])
    # It's okay if the command returns 0 with empty output, or returns non-zero
    # The important thing is that the description no longer appears in visible log
    assert "add config parser and update tests" not in result.stdout, (
        f"Mixed commit 'add config parser and update tests' still visible in history: {result.stdout!r}"
    )


def test_linear_history_order():
    """Verify linear ancestry: initial commit -> add utility fix -> add config parser -> add config tests -> @."""
    result = run_jj(["log", "-r", "::@", "--no-graph", "-T", 'description ++ "\\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    output = result.stdout
    assert "add utility fix" in output, f"'add utility fix' not in ancestry of @: {output!r}"
    assert "add config parser" in output, f"'add config parser' not in ancestry of @: {output!r}"
    assert "add config tests" in output, f"'add config tests' not in ancestry of @: {output!r}"
    assert "initial commit" in output, f"'initial commit' not in ancestry of @: {output!r}"

    # Verify the ordering: utility fix -> config parser -> config tests (newest to oldest in jj log)
    idx_tests = output.find("add config tests")
    idx_parser = output.find("add config parser")
    idx_util = output.find("add utility fix")
    idx_initial = output.find("initial commit")
    assert idx_tests < idx_parser, (
        f"'add config tests' should appear before 'add config parser' in jj log (newest first). "
        f"Got tests at {idx_tests}, parser at {idx_parser}"
    )
    assert idx_parser < idx_util, (
        f"'add config parser' should appear before 'add utility fix' in jj log (newest first). "
        f"Got parser at {idx_parser}, util at {idx_util}"
    )
    assert idx_util < idx_initial, (
        f"'add utility fix' should appear before 'initial commit' in jj log (newest first). "
        f"Got util at {idx_util}, initial at {idx_initial}"
    )


def test_add_utility_fix_modifies_only_utils_py():
    result = run_jj(["diff", "-r", 'description(substring:"add utility fix")', "--name-only"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    assert files == ["src/utils.py"], (
        f"'add utility fix' should modify only src/utils.py, but modifies: {files}"
    )


def test_add_config_parser_modifies_only_config_py():
    # Use exact description to avoid matching "add config parser and update tests" if it still exists
    result = run_jj(["log", "-r", 'description(substring:"add config parser")',
                     "--no-graph", "-T", "change_id.short()"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    change_ids = [c.strip() for c in result.stdout.splitlines() if c.strip()]
    # Filter to commits that have exactly "add config parser" (not "add config parser and update tests")
    target_change_id = None
    for cid in change_ids:
        desc_result = run_jj(["log", "-r", cid, "--no-graph", "-T", 'description ++ "\n"'])
        if desc_result.returncode == 0 and desc_result.stdout.strip() == "add config parser":
            target_change_id = cid
            break
    assert target_change_id is not None, (
        "Could not find commit with exact description 'add config parser'"
    )
    result = run_jj(["diff", "-r", target_change_id, "--name-only"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    assert files == ["src/config.py"], (
        f"'add config parser' should modify only src/config.py, but modifies: {files}"
    )


def test_add_config_tests_modifies_only_test_config_py():
    result = run_jj(["diff", "-r", 'description(substring:"add config tests")', "--name-only"])
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    assert files == ["tests/test_config.py"], (
        f"'add config tests' should modify only tests/test_config.py, but modifies: {files}"
    )


def test_utils_py_contains_greet_function():
    result = run_jj(["file", "show", "-r", 'description(substring:"add utility fix")',
                     "src/utils.py"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "def greet" in result.stdout, (
        f"src/utils.py in 'add utility fix' missing 'def greet'. Content: {result.stdout!r}"
    )
    assert "Hello" in result.stdout, (
        f"src/utils.py in 'add utility fix' missing greeting. Content: {result.stdout!r}"
    )


def test_config_py_contains_parse_config_function():
    result = run_jj(["file", "show", "-r", 'description(substring:"add config parser")',
                     "src/config.py"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "def parse_config" in result.stdout, (
        f"src/config.py in 'add config parser' missing 'def parse_config'. Content: {result.stdout!r}"
    )


def test_test_config_py_contains_test_function():
    result = run_jj(["file", "show", "-r", 'description(substring:"add config tests")',
                     "tests/test_config.py"])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "def test_parse_config" in result.stdout, (
        f"tests/test_config.py in 'add config tests' missing 'def test_parse_config'. Content: {result.stdout!r}"
    )


def test_bookmark_feature_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, (
        f"Bookmark 'feature' not found. Output: {result.stdout!r}"
    )


def test_bookmark_feature_points_to_add_config_tests():
    """Verify bookmark 'feature' points to the commit with description 'add config tests'."""
    # Get change_id of the commit that bookmark 'feature' points to
    result = run_jj(["log", "-r", "feature", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log on bookmark 'feature' failed: {result.stderr}"
    desc = result.stdout.strip()
    assert desc == "add config tests", (
        f"Bookmark 'feature' should point to commit with description 'add config tests', "
        f"but points to: {desc!r}"
    )


def test_exactly_three_non_root_non_working_copy_commits():
    """The history should have exactly 4 non-root commits: initial commit + 3 clean commits."""
    # Get all commits excluding root and working copy
    result = run_jj(["log", "-r", "root()..@-", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descriptions = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(descriptions) == 4, (
        f"Expected exactly 4 commits between root and working-copy parent "
        f"(initial commit + 3 clean commits), got {len(descriptions)}: {descriptions}"
    )
