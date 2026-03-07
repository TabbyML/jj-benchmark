import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_jj_in_path():
    assert shutil.which("jj") is not None, "jj binary must be in PATH"


def test_repo_dir_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory must exist: {REPO_DIR}"


def test_jj_dir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory must exist inside repo: {jj_dir}"


def test_repo_is_valid_jj_repo():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj status must succeed in repo directory. stderr: {result.stderr}"
    )


def test_config_dir_exists():
    config_dir = os.path.join(REPO_DIR, "config")
    assert os.path.isdir(config_dir), (
        f"config/ directory must exist inside repo: {config_dir}"
    )


def test_settings_toml_exists():
    settings_file = os.path.join(REPO_DIR, "config", "settings.toml")
    assert os.path.isfile(settings_file), (
        f"config/settings.toml must exist in the repo: {settings_file}"
    )


def test_settings_toml_has_conflict_markers():
    settings_file = os.path.join(REPO_DIR, "config", "settings.toml")
    with open(settings_file, "r") as f:
        content = f.read()
    conflict_indicators = ["<<<<<<<", "+++++++", "%%%%%%%"]
    found = any(marker in content for marker in conflict_indicators)
    assert found, (
        "config/settings.toml must contain conflict markers before task starts"
    )


def test_bookmark_main_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "main"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "main" in result.stdout, (
        "Bookmark 'main' must exist in the repository"
    )


def test_bookmark_feature_server_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "feature-server"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "feature-server" in result.stdout, (
        "Bookmark 'feature-server' must exist in the repository"
    )


def test_bookmark_feature_db_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "feature-db"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "feature-db" in result.stdout, (
        "Bookmark 'feature-db' must exist in the repository"
    )


def test_working_copy_has_conflict():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj status must succeed. stderr: {result.stderr}"
    )
    assert "conflict" in result.stdout.lower(), (
        "Working copy must have a conflict before task starts. jj status output: "
        + result.stdout
    )


def test_init_config_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"init-config")', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "init-config" in result.stdout, (
        "A commit with description containing 'init-config' must exist. Got: " + result.stdout
    )


def test_update_server_config_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"update-server-config")', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "update-server-config" in result.stdout, (
        "A commit with description containing 'update-server-config' must exist. Got: " + result.stdout
    )


def test_update_db_config_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"update-db-config")', "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0 and "update-db-config" in result.stdout, (
        "A commit with description containing 'update-db-config' must exist. Got: " + result.stdout
    )
