import os
import subprocess
import pytest

REPO_DIR = "/home/user/incident-repo"


def test_jj_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_jj_dir_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status", "--no-pager"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_src_metrics_py_exists():
    path = os.path.join(REPO_DIR, "src", "metrics.py")
    assert os.path.isfile(path), f"src/metrics.py not found at {path}"


def test_config_settings_toml_exists():
    path = os.path.join(REPO_DIR, "config", "settings.toml")
    assert os.path.isfile(path), f"config/settings.toml not found at {path}"


def test_src_metrics_py_is_corrupted():
    """The working copy metrics.py must contain the corruption marker."""
    path = os.path.join(REPO_DIR, "src", "metrics.py")
    with open(path) as fh:
        content = fh.read()
    assert "DEBUG_GARBAGE" in content, (
        f"Expected corruption marker 'DEBUG_GARBAGE' in src/metrics.py but not found.\n"
        f"Content:\n{content}"
    )


def test_config_settings_toml_is_corrupted():
    """The working copy settings.toml must contain the corruption marker."""
    path = os.path.join(REPO_DIR, "config", "settings.toml")
    with open(path) as fh:
        content = fh.read()
    assert "CORRUPTED" in content, (
        f"Expected corruption marker 'CORRUPTED' in config/settings.toml but not found.\n"
        f"Content:\n{content}"
    )


def test_commit_description_wip_present():
    """The 'wip: integrate metrics module' commit must exist in the log."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: integrate metrics module" in result.stdout, (
        f"Expected commit 'wip: integrate metrics module' not found in log.\n"
        f"Output:\n{result.stdout}"
    )


def test_commit_description_feat_add_config_present():
    """The 'feat: add config module' commit must exist in the log."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add config module" in result.stdout, (
        f"Expected commit 'feat: add config module' not found in log.\n"
        f"Output:\n{result.stdout}"
    )


def test_commit_description_init_present():
    """The 'init: project scaffold' commit must exist in the log."""
    result = subprocess.run(
        ["jj", "log", "--no-pager", "--no-graph", "-T", "description ++ '\\n'", "-r", "::@"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "init: project scaffold" in result.stdout, (
        f"Expected commit 'init: project scaffold' not found in log.\n"
        f"Output:\n{result.stdout}"
    )


def test_working_copy_has_changes():
    """Working copy must have changes (corrupted files) before the task."""
    result = subprocess.run(
        ["jj", "diff", "--no-pager", "--summary"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() != "", (
        "Expected working copy to have changes (corrupted files) but diff is empty."
    )


def test_user_config_set():
    """User identity must be configured."""
    result = subprocess.run(
        ["jj", "config", "get", "user.name"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj config get user.name failed: {result.stderr}"
    assert result.stdout.strip() != "", "user.name is not configured"
