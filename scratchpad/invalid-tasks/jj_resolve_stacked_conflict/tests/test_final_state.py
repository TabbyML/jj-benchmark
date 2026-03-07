import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"

EXPECTED_SETTINGS_CONTENT = """\
[server]
host = "0.0.0.0"
port = 8081

[database]
url = "postgres://localhost/mydb"
pool_size = 10
"""

CONFLICT_MARKER_PREFIXES = [
    "<<<<<<<",
    ">>>>>>>",
    "%%%%%%%",
    "+++++++",
    "-------",
    "\\\\\\\\\\\\\\",
]


def test_settings_toml_no_conflict_markers():
    settings_file = os.path.join(REPO_DIR, "config", "settings.toml")
    assert os.path.isfile(settings_file), (
        f"config/settings.toml must exist: {settings_file}"
    )
    with open(settings_file, "r") as f:
        content = f.read()
    for marker in CONFLICT_MARKER_PREFIXES:
        assert marker not in content, (
            f"config/settings.toml must not contain conflict marker '{marker}'. "
            f"File content:\n{content}"
        )


def test_settings_toml_correct_content():
    settings_file = os.path.join(REPO_DIR, "config", "settings.toml")
    assert os.path.isfile(settings_file), (
        f"config/settings.toml must exist: {settings_file}"
    )
    with open(settings_file, "r") as f:
        content = f.read()
    assert content == EXPECTED_SETTINGS_CONTENT, (
        f"config/settings.toml content must exactly match expected resolved content.\n"
        f"Expected:\n{EXPECTED_SETTINGS_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )


def test_no_conflicts_in_status():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj status must succeed (exit code 0). stderr: {result.stderr}"
    )
    assert "conflict" not in result.stdout.lower(), (
        f"jj status must not report any conflicts after resolution. "
        f"Output:\n{result.stdout}"
    )


def test_working_copy_description():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log -r @ must succeed. stderr: {result.stderr}"
    )
    description = result.stdout.strip()
    assert description == "resolve: merge server and db config updates", (
        f"Working copy commit description must be 'resolve: merge server and db config updates'. "
        f"Got: {description!r}"
    )


def test_bookmark_main_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "main"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "main" in result.stdout, (
        "Bookmark 'main' must still exist after resolution"
    )


def test_bookmark_feature_server_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "feature-server"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "feature-server" in result.stdout, (
        "Bookmark 'feature-server' must still exist after resolution"
    )


def test_bookmark_feature_db_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "feature-db"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "feature-db" in result.stdout, (
        "Bookmark 'feature-db' must still exist after resolution"
    )


def test_working_copy_commit_shows_resolved_content():
    result = subprocess.run(
        ["jj", "file", "show", "-r", "@", "config/settings.toml"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj file show must succeed on config/settings.toml at @. stderr: {result.stderr}"
    )
    content = result.stdout
    assert 'host = "0.0.0.0"' in content, (
        f"Resolved settings.toml must contain 'host = \"0.0.0.0\"'. Got:\n{content}"
    )
    assert "port = 8081" in content, (
        f"Resolved settings.toml must contain 'port = 8081'. Got:\n{content}"
    )
    assert "pool_size = 10" in content, (
        f"Resolved settings.toml must contain 'pool_size = 10'. Got:\n{content}"
    )
