import os
import subprocess
import pytest

REPO_DIR = "/home/user/release-repo"
CHANGELOG_PATH = "/home/user/CHANGELOG.md"
STATS_PATH = "/home/user/contributor_stats.txt"

EXPECTED_CHANGELOG = """## Features
- add CSV export (Alice)
- add dark mode (Charlie)
- new dashboard UI (Alice)

## Bug Fixes
- correct login redirect (Bob)
- prevent XSS in user input (Charlie)

## Maintenance
- update dependencies (Bob)"""


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_changelog_file_exists():
    assert os.path.isfile(CHANGELOG_PATH), f"CHANGELOG.md not found at {CHANGELOG_PATH}."


def test_changelog_content():
    with open(CHANGELOG_PATH) as f:
        content = f.read().strip()
    assert content == EXPECTED_CHANGELOG.strip(), \
        f"CHANGELOG.md content does not match expected.\nExpected:\n{EXPECTED_CHANGELOG}\n\nGot:\n{content}"


def test_contributor_stats_file_exists():
    assert os.path.isfile(STATS_PATH), f"contributor_stats.txt not found at {STATS_PATH}."


def test_contributor_stats_content():
    with open(STATS_PATH) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    non_empty = [l for l in lines if l.strip()]
    assert len(non_empty) == 3, f"contributor_stats.txt should have 3 lines, found {len(non_empty)}: {non_empty}"
    assert "Alice: 2" in non_empty, f"'Alice: 2' not found in stats: {non_empty}"
    assert "Bob: 2" in non_empty, f"'Bob: 2' not found in stats: {non_empty}"
    assert "Charlie: 2" in non_empty, f"'Charlie: 2' not found in stats: {non_empty}"


def test_release_commit_exists():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "release: v1.1 changelog" in result.stdout, \
        "'release: v1.1 changelog' commit not found in the repository log."


def test_v1_1_bookmark_points_to_release_commit():
    result = run_jj(["log", "--no-graph", "-r", "v1.1", "-T", 'description'])
    assert result.returncode == 0, f"v1.1 bookmark not found: {result.stderr}"
    assert "release: v1.1 changelog" in result.stdout, \
        f"v1.1 bookmark should point to 'release: v1.1 changelog', got: {result.stdout.strip()}"


def test_changelog_in_repo_at_release_commit():
    result = run_jj(["file", "show", "CHANGELOG.md", "-r", 'description("release: v1.1 changelog")'])
    assert result.returncode == 0, f"CHANGELOG.md not found in repo at release commit: {result.stderr}"
    assert "## Features" in result.stdout, "CHANGELOG.md in repo does not contain '## Features' section."
    assert "## Bug Fixes" in result.stdout, "CHANGELOG.md in repo does not contain '## Bug Fixes' section."


def test_changelog_has_correct_sections():
    with open(CHANGELOG_PATH) as f:
        content = f.read()
    assert "## Features" in content, "'## Features' section missing from CHANGELOG.md."
    assert "## Bug Fixes" in content, "'## Bug Fixes' section missing from CHANGELOG.md."
    assert "## Maintenance" in content, "'## Maintenance' section missing from CHANGELOG.md."
