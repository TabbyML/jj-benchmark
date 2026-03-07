import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/audit-repo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"


def test_pipeline_config_toml_exists():
    path = os.path.join(REPO_DIR, "pipeline_config.toml")
    assert os.path.isfile(path), f"pipeline_config.toml not found at {path}."


def test_pipeline_config_toml_content():
    path = os.path.join(REPO_DIR, "pipeline_config.toml")
    content = open(path).read()
    assert "[pipeline]" in content, "pipeline_config.toml missing '[pipeline]' section."
    assert "version = 1" in content, "pipeline_config.toml missing 'version = 1'."


def test_transform_py_exists():
    path = os.path.join(REPO_DIR, "transform.py")
    assert os.path.isfile(path), f"transform.py not found at {path}."


def test_transform_py_content():
    path = os.path.join(REPO_DIR, "transform.py")
    content = open(path).read()
    assert "def transform" in content, "transform.py missing 'def transform' function."


def test_validation_py_exists():
    path = os.path.join(REPO_DIR, "validation.py")
    assert os.path.isfile(path), f"validation.py not found at {path}."


def test_validation_py_content():
    path = os.path.join(REPO_DIR, "validation.py")
    content = open(path).read()
    assert "def validate" in content, "validation.py missing 'def validate' function."


def test_debug_log_exists():
    path = os.path.join(REPO_DIR, "debug.log")
    assert os.path.isfile(path), f"debug.log not found at {path}."


def test_notes_txt_exists():
    path = os.path.join(REPO_DIR, "notes.txt")
    assert os.path.isfile(path), f"notes.txt not found at {path}."


def test_initial_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "chore: add pipeline config" in log, "Expected commit 'chore: add pipeline config' not found in log."
    assert "feat: add transform script" in log, "Expected commit 'feat: add transform script' not found in log."
    assert "wip: debug temp" in log, "Expected commit 'wip: debug temp' not found in log."
    assert "feat: add validation logic" in log, "Expected commit 'feat: add validation logic' not found in log."
    assert "wip: scratch notes" in log, "Expected commit 'wip: scratch notes' not found in log."


def test_wip_revisions_present_before_prune():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", 'description(glob:"wip:*")', "-T", 'description ++ "\\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log with revset failed: {result.stderr}"
    log = result.stdout
    assert "wip: debug temp" in log, "Expected 'wip: debug temp' to be present before pruning."
    assert "wip: scratch notes" in log, "Expected 'wip: scratch notes' to be present before pruning."


def test_working_copy_is_empty_on_top_of_wip():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@-", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: scratch notes" in result.stdout, (
        f"Working copy parent should be 'wip: scratch notes', got: {result.stdout.strip()}"
    )
