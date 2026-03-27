import os
import subprocess
import pytest

REPO = "/home/user/repo"


def jj(*args, **kwargs):
    env = os.environ.copy()
    env["HOME"] = "/home/user"
    return subprocess.run(
        ["jj"] + list(args),
        cwd=REPO,
        capture_output=True,
        text=True,
        env=env,
        **kwargs
    )


def test_commit_1_has_strip_parser():
    result = jj("file", "show", "parser.py", "-r", "commit-1")
    assert result.returncode == 0
    assert "strip()" in result.stdout, \
        "commit-1 parser.py should have the strip() fixup absorbed"


def test_commit_3_has_improved_formatter():
    result = jj("file", "show", "formatter.py", "-r", "commit-3")
    assert result.returncode == 0
    assert "if i" in result.stdout, \
        "commit-3 formatter.py should have the 'if i' fixup absorbed"


def test_commit_5_has_none_check_runner():
    result = jj("file", "show", "runner.py", "-r", "commit-5")
    assert result.returncode == 0
    assert "None" in result.stdout, \
        "commit-5 runner.py should have the None check fixup absorbed"


def test_working_copy_is_clean():
    result = jj("diff", "-r", "@")
    assert result.returncode == 0
    assert result.stdout.strip() == "", \
        "Working copy should be empty after absorb"


def test_commit_2_unchanged():
    result = jj("file", "show", "validator.py", "-r", "commit-2")
    assert result.returncode == 0
    # validator.py should be unchanged (no fixup for it)
    assert "def validate" in result.stdout


def test_commit_4_unchanged():
    result = jj("file", "show", "exporter.py", "-r", "commit-4")
    assert result.returncode == 0
    assert "def export" in result.stdout


def test_absorb_report_exists():
    report_path = "/home/user/absorb_report.md"
    assert os.path.isfile(report_path), \
        "Absorb report should exist at /home/user/absorb_report.md"
    with open(report_path) as f:
        content = f.read()
    assert len(content) > 50, "Absorb report should have meaningful content"
