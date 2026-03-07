import os
import subprocess

import pytest

REPO_DIR = "/home/user/workspace"
EXPECTED_SERVER_PY = (
    '# Web service configuration\n'
    'HOST = "0.0.0.0"\n'
    'PORT = 9000\n'
    'LOG_LEVEL = "WARNING"\n'
    'DEBUG = False\n'
)
EXPECTED_ROUTES_PY = (
    '# HTTP route definitions\n'
    'routes = [\n'
    '    {"path": "/", "handler": "index", "description": "Home page (v2)"},\n'
    '    {"path": "/health", "handler": "health_check", "description": "Health endpoint"},\n'
    '    {"path": "/api/v2/users", "handler": "users_v2", "description": "Users API v2"},\n'
    ']\n'
)


def test_server_py_has_correct_content():
    server_path = os.path.join(REPO_DIR, "src", "server.py")
    assert os.path.isfile(server_path), f"src/server.py not found: {server_path}"
    with open(server_path) as fh:
        content = fh.read()
    assert content == EXPECTED_SERVER_PY, (
        f"src/server.py content mismatch.\n"
        f"Expected:\n{EXPECTED_SERVER_PY!r}\n"
        f"Got:\n{content!r}"
    )


def test_routes_py_has_correct_content():
    routes_path = os.path.join(REPO_DIR, "src", "routes.py")
    assert os.path.isfile(routes_path), f"src/routes.py not found: {routes_path}"
    with open(routes_path) as fh:
        content = fh.read()
    assert content == EXPECTED_ROUTES_PY, (
        f"src/routes.py content mismatch.\n"
        f"Expected:\n{EXPECTED_ROUTES_PY!r}\n"
        f"Got:\n{content!r}"
    )


def test_server_py_has_no_conflict_markers():
    server_path = os.path.join(REPO_DIR, "src", "server.py")
    with open(server_path) as fh:
        content = fh.read()
    assert "<<<<<<<" not in content, "src/server.py still contains conflict markers (<<<<<<<)"
    assert ">>>>>>>" not in content, "src/server.py still contains conflict markers (>>>>>>>)"
    assert "=======" not in content, "src/server.py still contains conflict markers (=======)"


def test_routes_py_has_no_conflict_markers():
    routes_path = os.path.join(REPO_DIR, "src", "routes.py")
    with open(routes_path) as fh:
        content = fh.read()
    assert "<<<<<<<" not in content, "src/routes.py still contains conflict markers (<<<<<<<)"
    assert ">>>>>>>" not in content, "src/routes.py still contains conflict markers (>>>>>>>)"
    assert "=======" not in content, "src/routes.py still contains conflict markers (=======)"


def test_working_copy_has_no_conflicts():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    # When there are no conflicts, jj resolve --list exits non-zero and prints nothing (or "No conflicts found")
    assert "server.py" not in result.stdout, (
        "src/server.py is still listed as conflicted after resolution"
    )
    assert "routes.py" not in result.stdout, (
        "src/routes.py is still listed as conflicted after resolution"
    )


def test_working_copy_conflict_flag_is_false():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "conflict"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "true" not in result.stdout.lower(), (
        f"Working copy commit still has conflict flag set.\nGot: {result.stdout!r}"
    )


def test_working_copy_description_contains_merge_message():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "merge: integrate feature-api and feature-logging" in result.stdout, (
        f"Working-copy description does not contain expected merge message.\n"
        f"Got: {result.stdout!r}"
    )


def test_working_copy_has_two_parents():
    result = subprocess.run(
        ["jj", "log", "-r", "@", "--no-graph", "-T", "parents.len()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "2" in result.stdout, (
        f"Working-copy commit does not have 2 parents (expected merge commit).\n"
        f"Got parents.len() = {result.stdout!r}"
    )


def test_bookmark_main_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Bookmark 'main' was removed but should still exist"


def test_bookmark_feature_api_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-api" in result.stdout, (
        "Bookmark 'feature-api' was removed but should still exist"
    )


def test_bookmark_feature_logging_still_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature-logging" in result.stdout, (
        "Bookmark 'feature-logging' was removed but should still exist"
    )
