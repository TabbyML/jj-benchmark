import os
import subprocess
import pytest

REPO = "/home/user/repo"


def run_jj(args, cwd=REPO):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def test_repo_exists():
    assert os.path.isdir(REPO)


def test_jj_initialized():
    result = run_jj(["status"])
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0
    assert "main" in result.stdout


def test_has_12_commits():
    result = run_jj(["log", "--no-graph", "-r", "~root()", "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    # Count non-empty descriptions (excluding working copy if empty)
    lines = [l for l in result.stdout.splitlines() if l.strip() and "(no description" not in l]
    assert len(lines) >= 12, f"Expected at least 12 commits, got {len(lines)}: {result.stdout}"


def test_bot_commits_exist():
    result = run_jj(["log", "--no-graph", "-r", 'author("bot@company.com")', "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) >= 8, f"Expected at least 8 bot commits, got {len(lines)}"


def test_human_commits_exist():
    result = run_jj(["log", "--no-graph", "-r",
                     '~root() & ~author("bot@company.com")',
                     "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip() and "(no description" not in l]
    assert len(lines) >= 4, f"Expected at least 4 human commits, got {len(lines)}"


def test_bot_commits_have_chore_prefix():
    result = run_jj(["log", "--no-graph", "-r", 'author("bot@company.com")',
                     "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    for line in result.stdout.splitlines():
        if line.strip():
            assert line.startswith("chore:"), f"Bot commit should start with 'chore:': {line}"


def test_squash_log_not_yet_created():
    assert not os.path.exists("/home/user/squash_log.txt"), \
        "squash_log.txt should not exist yet"


def test_data_txt_exists():
    result = run_jj(["file", "show", "data.txt", "-r", "main"])
    assert result.returncode == 0, "data.txt must exist in main"


def test_main_py_exists():
    result = run_jj(["file", "show", "main.py", "-r", "main"])
    assert result.returncode == 0, "main.py must exist in main"
