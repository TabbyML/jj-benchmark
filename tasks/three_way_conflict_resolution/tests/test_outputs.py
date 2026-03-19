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


def test_no_conflicts_remain():
    result = jj("resolve", "--list", "-r", "merge-ab")
    assert result.returncode != 0 or result.stdout.strip() == "", \
        "No conflicts should remain in merge-ab"


def test_config_has_production_host():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert "db.production.example.com" in result.stdout, \
        "Resolved config should have production database host from branch-a"


def test_config_has_production_port():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert "5433" in result.stdout, \
        "Resolved config should have port 5433 from branch-a"


def test_config_has_prod_db_name():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert "mydb_prod" in result.stdout, \
        "Resolved config should have mydb_prod from branch-a"


def test_config_has_debug_log_level():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert 'LOG_LEVEL = "DEBUG"' in result.stdout, \
        "Resolved config should have DEBUG log level from branch-b"


def test_config_has_max_connections_50():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert "MAX_CONNECTIONS = 50" in result.stdout, \
        "Resolved config should have MAX_CONNECTIONS = 50 from branch-a"


def test_config_has_timeout_60():
    result = jj("file", "show", "src/config.py", "-r", "merge-ab")
    assert result.returncode == 0
    assert "TIMEOUT = 60" in result.stdout, \
        "Resolved config should have TIMEOUT = 60 from branch-b"


def test_resolution_summary_exists():
    summary_path = "/home/user/resolution_summary.md"
    assert os.path.isfile(summary_path), \
        "Resolution summary file should exist at /home/user/resolution_summary.md"
    with open(summary_path) as f:
        content = f.read()
    assert len(content) > 50, "Resolution summary should have meaningful content"


def test_working_copy_clean():
    result = jj("resolve", "--list")
    assert result.returncode != 0 or result.stdout.strip() == "", \
        "Working copy should have no conflicts"
