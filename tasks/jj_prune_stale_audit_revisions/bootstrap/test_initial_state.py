import os
import subprocess
import pytest

REPO_DIR = "/home/user/audit-repo"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "--no-pager", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists_in_repo():
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list",
         "-r", 'description(substring:"init: scaffold audit repo")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "README.md" in result.stdout


def test_ingest_pipeline_file_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list",
         "-r", 'description(substring:"feat: add ingestion pipeline")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/ingest.py" in result.stdout


def test_transform_pipeline_file_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list",
         "-r", 'description(substring:"feat: add transformation step")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/transform.py" in result.stdout


def test_draft_validate_wip_revision_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "log",
         "-r", 'description(substring:"draft: WIP validation logic")',
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "draft: WIP validation logic (do not merge)" in result.stdout


def test_draft_dedup_revision_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "log",
         "-r", 'description(substring:"draft: experimental dedup pass")',
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "draft: experimental dedup pass" in result.stdout


def test_reporting_module_revision_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "log",
         "-r", 'description(substring:"feat: add reporting module")',
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add reporting module" in result.stdout


def test_validate_wip_file_present_in_draft_revision():
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list",
         "-r", 'description(substring:"draft: WIP validation logic")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/validate_wip.py" in result.stdout


def test_dedup_exp_file_present_in_draft_revision():
    result = subprocess.run(
        ["jj", "--no-pager", "file", "list",
         "-r", 'description(substring:"draft: experimental dedup pass")'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "pipelines/dedup_exp.py" in result.stdout


def test_audit_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "--no-pager", "bookmark", "list", "audit-main"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "audit-main" in result.stdout


def test_audit_main_points_to_reporting_revision():
    result = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "audit-main",
         "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add reporting module" in result.stdout


def test_six_non_root_revisions_exist():
    result = subprocess.run(
        ["jj", "--no-pager", "log", "-r", "all()",
         "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descriptions = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    non_root = [d for d in descriptions if d != "(no description set)"]
    # Expect: 6 named revisions (descriptions are non-empty)
    assert len(non_root) >= 6, f"Expected at least 6 named revisions, got: {non_root}"
