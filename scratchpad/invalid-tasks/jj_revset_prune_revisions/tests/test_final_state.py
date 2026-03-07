import os
import subprocess
import pytest

REPO_DIR = "/home/user/audit-repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_no_wip_revisions_in_visible_history():
    result = run_jj(["log", "--no-graph", "-r", 'description(glob:"wip:*")', "-T", 'description ++ "\\n"'])
    assert result.returncode == 0, f"jj log with wip revset failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Expected no wip revisions, but found:\n{result.stdout}"
    )


def test_meaningful_commits_present():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "chore: add pipeline config" in log, (
        "'chore: add pipeline config' commit is missing from visible history."
    )
    assert "feat: add transform script" in log, (
        "'feat: add transform script' commit is missing from visible history."
    )
    assert "feat: add validation logic" in log, (
        "'feat: add validation logic' commit is missing from visible history."
    )


def test_wip_commits_not_in_history():
    result = run_jj(["log", "--no-graph", "-T", 'description ++ "\\n"'])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "wip: debug temp" not in log, (
        "'wip: debug temp' still appears in visible history — it was not abandoned."
    )
    assert "wip: scratch notes" not in log, (
        "'wip: scratch notes' still appears in visible history — it was not abandoned."
    )


def test_working_copy_parent_is_validation_logic():
    result = run_jj(["log", "--no-graph", "-r", "@-", "-T", "description"])
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add validation logic" in result.stdout, (
        f"Working copy parent should be 'feat: add validation logic', got: {result.stdout.strip()}"
    )


def test_audit_log_file_exists():
    audit_log = os.path.join(REPO_DIR, "audit_log.txt")
    assert os.path.isfile(audit_log), (
        f"audit_log.txt not found at {audit_log}. "
        "Run 'jj log --no-graph > audit_log.txt' to create it."
    )


def test_audit_log_file_not_empty():
    audit_log = os.path.join(REPO_DIR, "audit_log.txt")
    assert os.path.isfile(audit_log), f"audit_log.txt not found at {audit_log}."
    content = open(audit_log).read().strip()
    assert len(content) > 0, "audit_log.txt exists but is empty."


def test_pipeline_config_toml_still_present():
    path = os.path.join(REPO_DIR, "pipeline_config.toml")
    assert os.path.isfile(path), (
        f"pipeline_config.toml missing at {path} — it should not have been removed."
    )


def test_transform_py_still_present():
    path = os.path.join(REPO_DIR, "transform.py")
    assert os.path.isfile(path), (
        f"transform.py missing at {path} — it should not have been removed."
    )


def test_validation_py_still_present():
    path = os.path.join(REPO_DIR, "validation.py")
    assert os.path.isfile(path), (
        f"validation.py missing at {path} — it should not have been removed."
    )


def test_no_conflicts_in_repo():
    result = run_jj(["status"])
    assert result.returncode == 0, f"jj status failed: {result.stderr}"
    assert "conflict" not in result.stdout.lower(), (
        f"jj status reports conflicts in the repository:\n{result.stdout}"
    )
