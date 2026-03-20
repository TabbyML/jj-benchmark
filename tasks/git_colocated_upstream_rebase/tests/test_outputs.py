import os
import subprocess
import pytest


REPO = "/home/user/local-repo"
REPORT = "/home/user/status_report.txt"


def run_jj(args, cwd=REPO):
    return subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )


def test_status_report_exists():
    assert os.path.isfile(REPORT), \
        "status_report.txt must exist at /home/user/status_report.txt"


def test_upstream_commits_fetched():
    """After fetch, local should have upstream-3 and upstream-4."""
    result = run_jj(["log", "--no-graph", "-r", "all()",
                     "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    assert "upstream-3" in result.stdout or "security config" in result.stdout, \
        "upstream-3 should be fetched"
    assert "upstream-4" in result.stdout or "cache" in result.stdout, \
        "upstream-4 should be fetched"


def test_local_commits_rebased_onto_new_upstream():
    """Local commits should be descendants of the new upstream HEAD."""
    result = run_jj(["log", "--no-graph",
                     "-r", "local-branch & descendants(main)",
                     "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    assert "local-3" in result.stdout or "order" in result.stdout, \
        "local-branch should be rebased onto new main (upstream-4)"


def test_all_local_commits_present():
    """All 3 local commits should still exist after rebasing."""
    result = run_jj(["log", "--no-graph", "-r", "all()",
                     "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    for i in range(1, 4):
        assert f"local-{i}" in result.stdout, \
            f"local-{i} should still exist after rebase"


def test_no_conflicts():
    """No commits should have conflicts after the rebase."""
    result = run_jj(["log", "--no-graph", "-r", "conflicts()",
                     "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    assert result.stdout.strip() == "", \
        "No conflicts should remain after rebase"


def test_main_on_new_upstream_head():
    """main bookmark should point to upstream-4 (the new upstream HEAD)."""
    result = run_jj(["file", "show", "features.txt", "-r", "main"])
    assert result.returncode == 0
    assert "security=strict" in result.stdout, \
        "main should now include the security config from upstream-3"


def test_status_report_content():
    """The status report should document the rebase operation."""
    with open(REPORT) as f:
        content = f.read()
    assert len(content) > 50, "status_report.txt must have content"
    assert any(word in content.lower() for word in
               ["fetch", "rebase", "upstream", "local", "main"]), \
        "Status report should mention fetch/rebase operations"
