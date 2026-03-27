"""
Tests to verify symmetric merge divergence reconciliation task.
All tests should FAIL before the task is completed.
"""
import os
import subprocess

REPO_DIR = "/home/user/repo"
LOG_FILE = "/home/user/divergence_log.txt"


def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} does not exist"


def test_log_file_has_required_keys():
    content = open(LOG_FILE).read()
    assert "approach:" in content, "Missing approach key"
    assert "patch_v1_change_id:" in content, "Missing patch_v1_change_id key"
    assert "patch_v2_change_id:" in content, "Missing patch_v2_change_id key"
    assert "canonical_change_id:" in content, "Missing canonical_change_id key"
    assert "resolution:" in content, "Missing resolution key"


def test_log_change_ids_nonempty():
    content = open(LOG_FILE).read()
    for line in content.strip().splitlines():
        if "change_id" in line and ":" in line:
            val = line.split(":", 1)[1].strip()
            assert val, f"Empty change_id value in: {line}"


def test_patch_bookmark_exists():
    r = run_jj(["bookmark", "list"])
    assert "patch" in r.stdout, "patch bookmark not found"


def test_patch_has_no_conflicts():
    r = run_jj(["resolve", "--list", "-r", "patch"])
    assert r.stdout.strip() == "", f"patch commit has conflicts: {r.stdout}"


def test_patch_py_has_apply_patch_v1():
    r = run_jj(["file", "show", "-r", "patch", "src/patch.py"])
    assert "def apply_patch_v1(" in r.stdout, \
        "apply_patch_v1() missing from src/patch.py at patch bookmark"


def test_patch_py_has_apply_patch_v2():
    r = run_jj(["file", "show", "-r", "patch", "src/patch.py"])
    assert "def apply_patch_v2(" in r.stdout, \
        "apply_patch_v2() missing from src/patch.py at patch bookmark"


def test_patch_py_no_conflict_markers():
    r = run_jj(["file", "show", "-r", "patch", "src/patch.py"])
    assert "<<<<<<<" not in r.stdout, "Conflict markers in src/patch.py"


def test_canonical_commit_description_is_fix_patch():
    r = run_jj(["log", "--no-graph", "-T", "description", "-r", "patch"])
    assert "fix: patch" in r.stdout, \
        "patch bookmark does not point to a 'fix: patch' commit"
