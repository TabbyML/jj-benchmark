import os
import subprocess
import pytest


REPO_DIR = "/home/user/release-project"


def test_auth_v1_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "auth-v1.0" in result.stdout, "Bookmark 'auth-v1.0' not found in bookmark list"


def test_auth_v1_bookmark_points_to_auth_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "auth-v1.0",
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for auth-v1.0 failed: {result.stderr}"
    assert "add authentication module" in result.stdout, (
        f"auth-v1.0 bookmark does not point to 'add authentication module' commit, got: {result.stdout!r}"
    )


def test_payments_v1_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "payments-v1.0" in result.stdout, "Bookmark 'payments-v1.0' not found in bookmark list"


def test_payments_v1_bookmark_points_to_payment_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "payments-v1.0",
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for payments-v1.0 failed: {result.stderr}"
    assert "add payment gateway" in result.stdout, (
        f"payments-v1.0 bookmark does not point to 'add payment gateway' commit, got: {result.stdout!r}"
    )


def test_main_bookmark_points_to_reporting_dashboard():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "main",
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for main failed: {result.stderr}"
    assert "add reporting dashboard" in result.stdout, (
        f"main bookmark does not point to 'add reporting dashboard' commit, got: {result.stdout!r}"
    )


def test_main_bookmark_is_not_on_auth_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "main",
         "--template", "description", "--color", "never"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for main failed: {result.stderr}"
    assert "add authentication module" not in result.stdout, (
        "main bookmark still points to 'add authentication module' and has not been moved"
    )
