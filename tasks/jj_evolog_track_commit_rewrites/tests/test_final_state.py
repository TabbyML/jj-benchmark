import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"
REPORT_FILE = "/home/user/project/evolog_report.txt"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."


def test_report_has_exactly_three_lines():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    assert len(lines) == 3, f"Expected exactly 3 lines in report, found {len(lines)}: {lines}"


def test_report_change_id_line():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    assert lines[0].startswith("change_id: "), (
        f"Line 1 must start with 'change_id: ', got: {repr(lines[0])}"
    )
    reported_id = lines[0][len("change_id: "):].strip()
    assert len(reported_id) == 8, (
        f"Change ID must be 8 characters, got {len(reported_id)}: {repr(reported_id)}"
    )
    # Verify the reported change ID matches the actual working-copy change ID
    result = run_jj(["log", "--no-graph", "-r", "@", "-T", "change_id.short(8)"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    actual_id = result.stdout.strip()
    assert reported_id == actual_id, (
        f"Reported change_id '{reported_id}' does not match actual working-copy change ID '{actual_id}'."
    )


def test_report_predecessor_count_line():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    assert lines[1] == "predecessor_count: 2", (
        f"Line 2 must be 'predecessor_count: 2', got: {repr(lines[1])}"
    )


def test_report_total_evolog_entries_line():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    assert lines[2] == "total_evolog_entries: 3", (
        f"Line 3 must be 'total_evolog_entries: 3', got: {repr(lines[2])}"
    )


def test_evolog_actually_has_three_entries():
    result = run_jj(["evolog", "-r", "@", "--no-graph", "-T", 'change_id ++ "\n"'])
    assert result.returncode == 0, f"jj evolog failed: {result.stderr}"
    entries = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert len(entries) == 3, (
        f"Expected 3 evolog entries for @, found {len(entries)}: {entries}"
    )
