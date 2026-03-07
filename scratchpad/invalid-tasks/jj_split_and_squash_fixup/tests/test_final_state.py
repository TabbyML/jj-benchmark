import os
import subprocess
import pytest

REPO_DIR = "/home/user/myproject"


def _jj(args, **kwargs):
    return subprocess.run(
        ["jj"] + args,
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        **kwargs,
    )


def test_exactly_two_non_root_non_wc_commits():
    """Visible history must have exactly 2 non-root, non-working-copy commits."""
    result = _jj([
        "log", "--no-graph", "-T", "change_id ++ '\n'",
        "-r", "mutable() ~ @",
    ])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) == 2, (
        f"Expected exactly 2 mutable non-wc commits, found {len(lines)}: {result.stdout}"
    )


def test_readme_commit_exists():
    """A commit with description 'add README.md' must exist."""
    result = _jj([
        "log", "--no-graph", "-T", "description",
        "-r", "description(substring:\"add README.md\")",
    ])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add README.md" in result.stdout, (
        f"Commit 'add README.md' not found. Got: {result.stdout}"
    )


def test_config_commit_exists():
    """A commit with description 'add config.toml' must exist."""
    result = _jj([
        "log", "--no-graph", "-T", "description",
        "-r", "description(substring:\"add config.toml\")",
    ])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add config.toml" in result.stdout, (
        f"Commit 'add config.toml' not found. Got: {result.stdout}"
    )


def test_fixup_commit_absent():
    """The fixup commit must not appear in visible history."""
    result = _jj([
        "log", "--no-graph", "-T", "description",
        "-r", "description(substring:\"fixup\")",
    ])
    # returncode 0 with empty output means no match (jj returns 0 for empty revset in log)
    # returncode non-0 if revset error – we only care that stdout is empty
    assert "fixup" not in result.stdout, (
        f"Fixup commit should not be visible but found: {result.stdout}"
    )


def test_readme_commit_contains_only_readme():
    """The 'add README.md' commit must contain only README.md."""
    result = _jj([
        "file", "list",
        "-r", "description(substring:\"add README.md\")",
    ])
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    files = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert files == ["README.md"], (
        f"Expected only README.md in 'add README.md' commit, got: {files}"
    )


def test_config_commit_contains_only_config():
    """The 'add config.toml' commit must contain only config.toml."""
    result = _jj([
        "file", "list",
        "-r", "description(substring:\"add config.toml\")",
    ])
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    files = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert files == ["config.toml"], (
        f"Expected only config.toml in 'add config.toml' commit, got: {files}"
    )


def test_readme_content_is_corrected():
    """README.md in the 'add README.md' commit must contain the corrected text."""
    result = _jj([
        "file", "show",
        "-r", "description(substring:\"add README.md\")",
        "README.md",
    ])
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    assert "Welcome to myproject" in result.stdout, (
        f"README.md does not contain corrected text. Got: {result.stdout}"
    )
    assert "Wellcome to myproject" not in result.stdout, (
        "README.md still contains the typo 'Wellcome'. Fixup was not squashed."
    )


def test_readme_is_ancestor_of_config():
    """'add README.md' must be an ancestor of 'add config.toml'."""
    result = _jj([
        "log", "--no-graph", "-T", "change_id ++ '\n'",
        "-r", (
            "description(substring:\"add README.md\") & "
            "::description(substring:\"add config.toml\")"
        ),
    ])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) == 1, (
        "'add README.md' is not an ancestor of 'add config.toml'. "
        "The linear order README -> config is required."
    )
