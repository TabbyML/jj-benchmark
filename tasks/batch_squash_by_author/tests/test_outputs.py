import os
import subprocess
import pytest

REPO = "/home/user/repo"
SQUASH_LOG = "/home/user/squash_log.txt"


def run_jj(args, cwd=REPO):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def test_squash_log_exists():
    assert os.path.exists(SQUASH_LOG), f"squash_log.txt must exist at {SQUASH_LOG}"


def test_fewer_bot_commits():
    result = run_jj(["log", "--no-graph", "-r", 'author("bot@company.com")',
                     "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    # Originally 8 bot commits in 3 consecutive groups; after squashing should be fewer
    assert len(lines) < 8, f"After squashing, should have fewer than 8 bot commits, got {len(lines)}"


def test_human_commits_preserved():
    result = run_jj(["log", "--no-graph", "-r",
                     '~root() & ~author("bot@company.com")',
                     "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip() and "(no description" not in l]
    assert len(lines) >= 4, f"Human commits must be preserved, got {len(lines)}"


def test_squashed_bot_commits_have_correct_format():
    result = run_jj(["log", "--no-graph", "-r", 'author("bot@company.com")',
                     "-T", "description.first_line() ++ '\n'"])
    assert result.returncode == 0
    for line in result.stdout.splitlines():
        if line.strip():
            # Squashed bot commits should follow a specific format
            assert "bot" in line.lower() or "chore" in line.lower() or "automated" in line.lower(), \
                f"Squashed bot commit description doesn't follow expected format: {line}"


def test_squash_log_mentions_merged_commits():
    with open(SQUASH_LOG) as f:
        content = f.read()
    assert len(content.strip()) > 0, "squash_log.txt must not be empty"
    # Should mention something about squashing or merging
    assert any(word in content.lower() for word in ["squash", "merge", "combined", "consolidated"]), \
        "squash_log.txt must describe what was squashed"


def test_main_bookmark_still_valid():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0
    assert "main" in result.stdout, "main bookmark must still exist"


def test_data_and_main_py_intact():
    result_data = run_jj(["file", "show", "data.txt", "-r", "main"])
    result_main = run_jj(["file", "show", "main.py", "-r", "main"])
    assert result_data.returncode == 0, "data.txt must still exist in main"
    assert result_main.returncode == 0, "main.py must still exist in main"
