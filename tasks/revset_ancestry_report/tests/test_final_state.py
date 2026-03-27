import os
import subprocess
import pytest

REPO = "/home/user/repo"
REPORT = "/home/user/ancestry_report.txt"


def run_jj(args, cwd=REPO):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def test_report_exists():
    assert os.path.exists(REPORT), f"ancestry_report.txt must exist at {REPORT}"


def test_report_has_feature_a_exclusive_section():
    with open(REPORT) as f:
        content = f.read()
    assert "feature-a" in content.lower() or "FEATURE-A" in content, \
        "Report must contain feature-a analysis"


def test_report_has_all_features_intersection():
    with open(REPORT) as f:
        content = f.read()
    # Should have a section about commits in all three features
    assert "all" in content.lower() or "intersection" in content.lower() or \
           ("feature-a" in content.lower() and "feature-b" in content.lower() and "feature-c" in content.lower()), \
        "Report must contain intersection analysis of all three features"


def test_report_has_merge_base_section():
    with open(REPORT) as f:
        content = f.read()
    assert "merge" in content.lower() or "common" in content.lower() or "base" in content.lower(), \
        "Report must contain merge base analysis"


def test_report_has_core_py_section():
    with open(REPORT) as f:
        content = f.read()
    assert "core.py" in content, "Report must mention core.py commits"


def test_report_is_non_trivial():
    with open(REPORT) as f:
        content = f.read()
    lines = [l for l in content.splitlines() if l.strip()]
    assert len(lines) >= 10, f"Report must have at least 10 non-empty lines, got {len(lines)}"


def test_feature_a_exclusive_commits_identified():
    # The report should include actual commit descriptions or IDs from feature-a
    with open(REPORT) as f:
        content = f.read()
    # feature-a exclusive commits should include "feature-a adds" descriptions
    assert "feature-a" in content.lower(), \
        "Report must identify feature-a exclusive commits"


def test_core_py_commits_in_report():
    # Get commits that modified core.py in features
    result = run_jj(["log", "--no-graph", "-r",
                     "(feature-a | feature-b | feature-c) & ~ancestors(main)",
                     "-T", "description.first_line() ++ '\n'"])
    if result.returncode == 0 and result.stdout.strip():
        with open(REPORT) as f:
            content = f.read()
        assert "core" in content.lower(), \
            "Report must reference core.py related commits"
