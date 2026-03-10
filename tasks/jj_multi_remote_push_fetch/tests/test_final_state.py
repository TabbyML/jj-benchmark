import os
import subprocess
import pytest


REPO_DIR = "/home/user/myrepo"


def test_both_remotes_listed():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj git remote list failed:\n{result.stderr}"
    )
    assert "origin" in result.stdout, (
        f"Remote 'origin' not found in remote list:\n{result.stdout}"
    )
    assert "upstream" in result.stdout, (
        f"Remote 'upstream' not found in remote list:\n{result.stdout}"
    )


def test_release_1_0_bookmark_exists_locally():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj bookmark list failed:\n{result.stderr}"
    )
    assert "release/1.0" in result.stdout, (
        f"Local bookmark 'release/1.0' not found:\n{result.stdout}"
    )


def test_release_1_0_pushed_to_origin():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj bookmark list --all-remotes failed:\n{result.stderr}"
    )
    assert "release/1.0@origin" in result.stdout, (
        f"Remote tracking bookmark 'release/1.0@origin' not found. "
        f"Did you push to origin?\n{result.stdout}"
    )


def test_release_1_0_points_to_correct_commit():
    result = subprocess.run(
        ["jj", "log", "-r", 'release/1.0', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log for release/1.0 failed:\n{result.stderr}"
    )
    assert "feat: add release notes" in result.stdout, (
        f"bookmark 'release/1.0' does not point to the 'feat: add release notes' commit.\n"
        f"Got: {result.stdout}"
    )


def test_integration_commit_present_locally():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"ci: add integration pipeline")',
         "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log for integration pipeline commit failed:\n{result.stderr}"
    )
    assert "ci: add integration pipeline" in result.stdout, (
        f"Commit 'ci: add integration pipeline' not found locally. "
        f"Did you fetch from upstream?\n{result.stdout}"
    )


def test_integration_bookmark_exists_locally():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj bookmark list failed:\n{result.stderr}"
    )
    assert "integration" in result.stdout, (
        f"Local bookmark 'integration' not found. "
        f"Did you track integration@upstream?\n{result.stdout}"
    )


def test_integration_bookmark_tracks_upstream():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj bookmark list --all-remotes failed:\n{result.stderr}"
    )
    assert "integration@upstream" in result.stdout, (
        f"Remote tracking bookmark 'integration@upstream' not found. "
        f"Did you fetch from upstream?\n{result.stdout}"
    )


def test_integration_bookmark_points_to_correct_commit():
    result = subprocess.run(
        ["jj", "log", "-r", "integration",
         "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log for 'integration' bookmark failed:\n{result.stderr}"
    )
    assert "ci: add integration pipeline" in result.stdout, (
        f"Local 'integration' bookmark does not point to 'ci: add integration pipeline'.\n"
        f"Got: {result.stdout}"
    )
