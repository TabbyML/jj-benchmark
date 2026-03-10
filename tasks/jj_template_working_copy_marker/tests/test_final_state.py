import os
import subprocess
import pytest

REPO_DIR = "/home/user/wc-marker-repo"
REPORT_FILE = "/home/user/wc-marker-repo/wc_marker_report.txt"


def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), f"wc_marker_report.txt not found at {REPORT_FILE}."


def test_report_file_is_non_empty():
    assert os.path.getsize(REPORT_FILE) > 0, "wc_marker_report.txt is empty."


def test_report_has_wc_line():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    non_empty = [l for l in lines if l.strip()]
    wc_lines = [l for l in non_empty if l.startswith("[WC]")]
    assert len(wc_lines) >= 1, f"No lines starting with [WC] found. Lines: {non_empty}"


def test_report_has_regular_lines():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    non_empty = [l for l in lines if l.strip()]
    regular_lines = [l for l in non_empty if l.startswith("[  ]")]
    assert len(regular_lines) >= 1, f"No lines starting with '[  ]' found. Lines: {non_empty}"


def test_all_lines_have_valid_prefix():
    with open(REPORT_FILE) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    non_empty = [l for l in lines if l.strip()]
    for line in non_empty:
        assert line.startswith("[WC]") or line.startswith("[  ]"), (
            f"Line has invalid prefix: {repr(line)}"
        )


def test_jj_log_current_working_copy_template_runs():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "all()", "-T",
         'if(current_working_copy, "[WC] ", "[  ] ") ++ description.first_line() ++ "\\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
