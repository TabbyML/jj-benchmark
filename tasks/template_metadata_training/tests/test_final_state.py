import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(args, cwd=REPO_DIR):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def test_author_name_is_trainer():
    result = run_jj(["log", "-r", "@", "-T", "author.name()", "--no-graph"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "Trainer", (
        f"Expected author name 'Trainer', got: {result.stdout.strip()}"
    )


def test_author_email_is_trainer():
    result = run_jj(["log", "-r", "@", "-T", "author.email()", "--no-graph"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "trainer@example.com", (
        f"Expected author email 'trainer@example.com', got: {result.stdout.strip()}"
    )


def test_template_alias_training_log_exists():
    result = run_jj(["config", "get", "template-aliases.training_log"])
    assert result.returncode == 0, (
        f"Template alias 'training_log' not found in jj config: {result.stderr}"
    )
    config = result.stdout.strip()
    assert "commit_id.short()" in config, (
        f"Template alias must include commit_id.short(), got: {config}"
    )
    assert "author.email()" in config, (
        f"Template alias must include author.email(), got: {config}"
    )
    assert "description.first_line()" in config, (
        f"Template alias must include description.first_line(), got: {config}"
    )


def test_formatted_log_file_exists():
    log_file = os.path.join(REPO_DIR, "formatted_log.txt")
    assert os.path.exists(log_file), (
        f"formatted_log.txt must exist at {log_file}"
    )


def test_formatted_log_has_two_lines():
    log_file = os.path.join(REPO_DIR, "formatted_log.txt")
    with open(log_file) as f:
        lines = [l for l in f.read().strip().splitlines() if l.strip()]
    assert len(lines) == 2, (
        f"formatted_log.txt should have 2 lines, got {len(lines)}: {lines}"
    )


def test_formatted_log_contains_trainer_wip():
    log_file = os.path.join(REPO_DIR, "formatted_log.txt")
    with open(log_file) as f:
        content = f.read()
    assert "trainer@example.com" in content and "WIP commit" in content, (
        f"First entry should contain trainer@example.com and 'WIP commit', got: {content}"
    )


def test_formatted_log_contains_default_base():
    log_file = os.path.join(REPO_DIR, "formatted_log.txt")
    with open(log_file) as f:
        content = f.read()
    assert "default@example.com" in content and "Base commit" in content, (
        f"Second entry should contain default@example.com and 'Base commit', got: {content}"
    )
