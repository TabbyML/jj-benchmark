import os
import subprocess
import pytest

REPO = "/home/user/repo"


def jj(*args, **kwargs):
    env = os.environ.copy()
    env["HOME"] = "/home/user"
    return subprocess.run(
        ["jj"] + list(args),
        cwd=REPO,
        capture_output=True,
        text=True,
        env=env,
        **kwargs
    )


def test_repo_exists():
    assert os.path.isdir(REPO)
    assert os.path.isdir(os.path.join(REPO, ".jj"))


def test_five_commits_in_stack():
    result = jj("log", "--no-graph", "-T", 'description ++ "\n"')
    assert result.returncode == 0
    assert "commit-1" in result.stdout
    assert "commit-2" in result.stdout
    assert "commit-3" in result.stdout
    assert "commit-4" in result.stdout
    assert "commit-5" in result.stdout


def test_working_copy_has_fixups():
    result = jj("diff", "-r", "@")
    assert result.returncode == 0
    # Should have changes to parser.py, formatter.py, and runner.py
    assert "parser.py" in result.stdout
    assert "formatter.py" in result.stdout
    assert "runner.py" in result.stdout


def test_parser_fixup_strips_whitespace():
    # Current WC should have the improved parser
    result = jj("file", "show", "parser.py")
    assert result.returncode == 0
    assert "strip()" in result.stdout


def test_formatter_fixup_handles_empty():
    result = jj("file", "show", "formatter.py")
    assert result.returncode == 0
    assert "if i" in result.stdout


def test_runner_fixup_handles_none():
    result = jj("file", "show", "runner.py")
    assert result.returncode == 0
    assert "None" in result.stdout


def test_bookmarks_exist():
    result = jj("bookmark", "list")
    assert result.returncode == 0
    for i in range(1, 6):
        assert f"commit-{i}" in result.stdout
