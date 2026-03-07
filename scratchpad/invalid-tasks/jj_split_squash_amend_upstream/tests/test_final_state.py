import os
import subprocess
import pytest

REPO_DIR = "/home/user/myproject"


def _jj_log_descriptions(cwd):
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", "mutable()",
        ],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    return result.stdout


def test_exactly_three_mutable_commits():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'change_id ++ "\n"',
            "-r", "mutable()",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) == 3, (
        f"Expected exactly 3 mutable commits after all tasks, got {len(lines)}: {result.stdout}"
    )


def test_no_fix_commit_in_mutable_history():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'mutable() & description(substring:"fix")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Found a 'fix' commit still in mutable history: {result.stdout}"
    )


def test_init_scaffold_commit_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"init: scaffold project structure")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "init: scaffold project structure" in result.stdout, (
        "Expected commit 'init: scaffold project structure' not found"
    )


def test_add_parser_commit_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"add parser")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add parser" in result.stdout, (
        "Expected commit 'add parser' not found"
    )


def test_feat_http_commit_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"feat(http): add http client and remove debug print")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat(http): add http client and remove debug print" in result.stdout, (
        "Expected commit 'feat(http): add http client and remove debug print' not found"
    )


def test_add_parser_commit_modifies_only_parser_rs():
    # Get the commit that has 'add parser' description
    result = subprocess.run(
        [
            "jj", "diff", "--summary",
            "-r", 'description(substring:"add parser") ~ description(substring:"add parser and")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    changed_files = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    # Each line has format like "A src/parser.rs" or "M src/parser.rs"
    file_paths = [line.split()[-1] for line in changed_files if line]
    assert file_paths == ["src/parser.rs"] or set(file_paths) == {"src/parser.rs"}, (
        f"'add parser' commit should only modify src/parser.rs, but modifies: {file_paths}"
    )


def test_feat_http_commit_modifies_http_rs_and_lib_rs():
    result = subprocess.run(
        [
            "jj", "diff", "--summary",
            "-r", 'description(substring:"feat(http):")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    changed_files = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    file_paths = set(line.split()[-1] for line in changed_files if line)
    assert "src/http.rs" in file_paths, (
        f"'feat(http)' commit should modify src/http.rs, but modifies: {file_paths}"
    )
    assert "src/lib.rs" in file_paths, (
        f"'feat(http)' commit should modify src/lib.rs, but modifies: {file_paths}"
    )


def test_working_copy_is_empty():
    result = subprocess.run(
        ["jj", "diff", "--summary"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should be empty but has changes: {result.stdout}"
    )


def test_add_parser_is_ancestor_of_feat_http():
    # 'add parser' should be a parent/ancestor of 'feat(http)' commit
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", (
                'ancestors(description(substring:"feat(http):"))'
                ' & description(substring:"add parser")'
                ' ~ description(substring:"add parser and")'
            ),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add parser" in result.stdout, (
        "'add parser' should be an ancestor of 'feat(http)' commit"
    )
