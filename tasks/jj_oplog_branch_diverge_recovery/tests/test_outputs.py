"""
Tests for jj_oplog_branch_diverge_recovery.
Verify the divergence report and analysis log are correctly written.
"""

import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
REPORT_FILE = "/home/user/divergence-report.md"
LOG_FILE = "/home/user/divergence_analysis_log.txt"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_divergence_report_exists():
    assert os.path.isfile(REPORT_FILE), f"Divergence report {REPORT_FILE} does not exist."


def test_analysis_log_exists():
    assert os.path.isfile(LOG_FILE), f"Analysis log {LOG_FILE} does not exist."


def test_analysis_log_content():
    with open(LOG_FILE) as f:
        content = f.read()
    assert "methodology:" in content, "log missing 'methodology:'"
    assert "common_ancestor_found: true" in content, "log missing 'common_ancestor_found: true'"
    assert "divergence_op_identified: true" in content, "log missing 'divergence_op_identified: true'"
    assert "report_written: /home/user/divergence-report.md" in content, \
        "log missing report_written path"


def test_report_has_section_headings():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "# Branch Divergence Report" in content, "report missing main heading"
    assert "## Common Ancestor" in content, "report missing '## Common Ancestor' section"
    assert "## Divergence Operation" in content, "report missing '## Divergence Operation' section"
    assert "## First Unique Commits After Split" in content, \
        "report missing unique commits section"


def test_report_has_commit_description():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "commit_description:" in content, "report missing 'commit_description:'"
    # The actual value should be "feat: shared-utils" (the divergence point)
    assert "feat: shared-utils" in content, \
        "report should identify 'feat: shared-utils' as common ancestor"


def test_report_has_change_id():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "change_id_short:" in content, "report missing 'change_id_short:'"
    for line in content.splitlines():
        if "change_id_short:" in line:
            val = line.split(":", 1)[1].strip()
            assert len(val) > 0, "change_id_short is empty"
            break


def test_report_has_divergence_op_id():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "divergence_op_id:" in content, "report missing 'divergence_op_id:'"
    for line in content.splitlines():
        if "divergence_op_id:" in line:
            val = line.split(":", 1)[1].strip()
            assert len(val) > 0, "divergence_op_id is empty"
            break


def test_report_has_first_develop_commit():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "first_develop_only_commit:" in content, "report missing first_develop_only_commit"
    assert "feat: feature-x-start" in content, \
        "report should identify 'feat: feature-x-start' as first develop-only commit"


def test_report_has_first_main_commit():
    with open(REPORT_FILE) as f:
        content = f.read()
    assert "first_main_only_commit:" in content, "report missing first_main_only_commit"
    assert "release: v1.1" in content, \
        "report should identify 'release: v1.1' as first main-only commit"


def test_common_ancestor_is_correct():
    # Verify the actual LCA using jj
    result = run_jj(["log", "--no-graph", "-r", "heads(::develop & ::main)", "-T", 'description'])
    assert result.returncode == 0, f"LCA revset failed: {result.stderr}"
    assert "feat: shared-utils" in result.stdout, \
        f"LCA should be 'feat: shared-utils', got: {result.stdout.strip()}"
