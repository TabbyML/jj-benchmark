"""
Tests to verify the criss-cross merge resolution task outputs.
All tests should FAIL before the task is completed.
"""
import os
import subprocess


REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/criss_cross_log.txt"


def run_jj(args, cwd=REPO_DIR):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist"


def test_log_file_format():
    assert os.path.isfile(LOG_FILE), "Log file missing"
    content = open(LOG_FILE).read()
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    keys = [l.split(":")[0].strip() for l in lines if ":" in l]
    assert "branch_a_tip" in keys, "Missing branch_a_tip in log"
    assert "branch_b_tip" in keys, "Missing branch_b_tip in log"
    assert "integration_commit" in keys, "Missing integration_commit in log"


def test_log_file_change_ids_nonempty():
    assert os.path.isfile(LOG_FILE), "Log file missing"
    content = open(LOG_FILE).read()
    for line in content.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            assert val.strip(), f"Empty value for key: {key.strip()}"


def test_integration_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "integration" in result.stdout, "integration bookmark not found"


def test_integration_has_no_conflicts():
    result = run_jj(["resolve", "--list", "-r", "integration"])
    # If returncode != 0 or stdout is empty, there are no conflicts
    assert result.stdout.strip() == "", \
        f"integration bookmark has unresolved conflicts: {result.stdout}"


def test_core_py_has_initialize():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/core.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "def initialize(" in r.stdout, "initialize() function missing from src/core.py"


def test_core_py_has_shutdown():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/core.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "def shutdown(" in r.stdout, "shutdown() function missing from src/core.py"


def test_utils_py_has_format_output():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/utils.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "def format_output(" in r.stdout, "format_output() function missing from src/utils.py"


def test_utils_py_has_parse_input():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/utils.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "def parse_input(" in r.stdout, "parse_input() function missing from src/utils.py"


def test_feature_a_exists_in_integration():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/feature_a.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert r.returncode == 0 and len(r.stdout.strip()) > 0, \
        "src/feature_a.py missing from integration commit"


def test_feature_b_exists_in_integration():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/feature_b.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert r.returncode == 0 and len(r.stdout.strip()) > 0, \
        "src/feature_b.py missing from integration commit"


def test_no_conflict_markers_in_core_py():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/core.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "<<<<<<<" not in r.stdout, "Conflict markers found in src/core.py"
    assert ">>>>>>>" not in r.stdout, "Conflict markers found in src/core.py"


def test_no_conflict_markers_in_utils_py():
    r = subprocess.run(
        ["jj", "file", "show", "-r", "integration", "src/utils.py"],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    assert "<<<<<<<" not in r.stdout, "Conflict markers found in src/utils.py"
    assert ">>>>>>>" not in r.stdout, "Conflict markers found in src/utils.py"
