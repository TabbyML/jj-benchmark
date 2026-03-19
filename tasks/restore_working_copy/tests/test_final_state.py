import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_parser_py_restored_to_strip():
    parser_path = os.path.join(REPO_DIR, "parser.py")
    assert os.path.isfile(parser_path), f"parser.py not found at {parser_path}."
    content = open(parser_path).read()
    assert "return text.strip()" in content, (
        f"parser.py should contain 'return text.strip()' after restore, got:\n{content}"
    )
    assert "return text.upper()" not in content, (
        "parser.py still contains 'return text.upper()' — restore was not applied correctly."
    )


def test_config_toml_unchanged():
    config_path = os.path.join(REPO_DIR, "config.toml")
    assert os.path.isfile(config_path), f"config.toml not found at {config_path}."
    content = open(config_path).read()
    assert "[settings]" in content, "config.toml missing '[settings]' section — file may have been corrupted."
    assert "version = 1" in content, "config.toml missing 'version = 1' — file may have been corrupted."


def test_status_log_exists():
    log_path = os.path.join(REPO_DIR, "status.log")
    assert os.path.isfile(log_path), f"status.log not found at {log_path}."
    content = open(log_path).read().strip()
    assert len(content) > 0, "status.log exists but is empty — jj status output was not saved."


def test_working_copy_description_unchanged():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: partial refactor" in result.stdout, (
        f"Working copy description should still be 'wip: partial refactor', got: {result.stdout.strip()}"
    )


def test_all_three_commits_still_present():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "chore: add config" in log, "'chore: add config' commit is missing — it should not have been abandoned."
    assert "feat: add parser" in log, "'feat: add parser' commit is missing — it should not have been abandoned."
    assert "wip: partial refactor" in log, "'wip: partial refactor' commit is missing — it should not have been abandoned."


def test_working_copy_not_abandoned():
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", 'change_id ++ "\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip(), "Working copy change_id is empty — the revision may have been abandoned."
