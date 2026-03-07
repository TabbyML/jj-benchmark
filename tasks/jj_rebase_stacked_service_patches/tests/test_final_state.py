import os
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def test_infra_base_bookmark_still_points_at_health_check_commit():
    """infra/base must still point at the 'feat: add health check module' commit."""
    result = subprocess.run(
        ["jj", "log", "-r", "infra/base", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add health check module" in result.stdout, (
        f"infra/base should still point at 'feat: add health check module', got: {result.stdout}"
    )


def test_auth_patch_tip_description_after_rebase():
    """services/auth-patch must point at commit with description 'fix: patch auth token validation'."""
    result = subprocess.run(
        ["jj", "log", "-r", "services/auth-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: patch auth token validation" in result.stdout, (
        f"Expected services/auth-patch tip 'fix: patch auth token validation', got: {result.stdout}"
    )


def test_cache_patch_tip_description_after_rebase():
    """services/cache-patch must point at commit with description 'fix: add cache TTL enforcement'."""
    result = subprocess.run(
        ["jj", "log", "-r", "services/cache-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: add cache TTL enforcement" in result.stdout, (
        f"Expected services/cache-patch tip 'fix: add cache TTL enforcement', got: {result.stdout}"
    )


def test_auth_patch_parent_is_infra_base():
    """The parent of services/auth-patch tip must be the commit pointed to by infra/base."""
    # Get commit_id of infra/base
    result_infra = subprocess.run(
        ["jj", "log", "-r", "infra/base", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_infra.returncode == 0, f"jj log infra/base failed: {result_infra.stderr}"
    infra_commit_id = result_infra.stdout.strip()

    # Get commit_id of parent of services/auth-patch
    result_parent = subprocess.run(
        ["jj", "log", "-r", "services/auth-patch-", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_parent.returncode == 0, f"jj log auth-patch parent failed: {result_parent.stderr}"
    parent_commit_id = result_parent.stdout.strip()

    assert infra_commit_id == parent_commit_id, (
        f"Parent of services/auth-patch ({parent_commit_id}) should equal infra/base ({infra_commit_id}). "
        "The auth-patch branch may not have been rebased onto infra/base."
    )


def test_cache_patch_parent_is_infra_base():
    """The parent of services/cache-patch tip must be the commit pointed to by infra/base."""
    # Get commit_id of infra/base
    result_infra = subprocess.run(
        ["jj", "log", "-r", "infra/base", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_infra.returncode == 0, f"jj log infra/base failed: {result_infra.stderr}"
    infra_commit_id = result_infra.stdout.strip()

    # Get commit_id of parent of services/cache-patch
    result_parent = subprocess.run(
        ["jj", "log", "-r", "services/cache-patch-", "--no-graph", "-T", 'commit_id ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_parent.returncode == 0, f"jj log cache-patch parent failed: {result_parent.stderr}"
    parent_commit_id = result_parent.stdout.strip()

    assert infra_commit_id == parent_commit_id, (
        f"Parent of services/cache-patch ({parent_commit_id}) should equal infra/base ({infra_commit_id}). "
        "The cache-patch branch may not have been rebased onto infra/base."
    )


def test_auth_patch_parent_description_is_health_check():
    """The parent of services/auth-patch tip must have description 'feat: add health check module'."""
    result = subprocess.run(
        ["jj", "log", "-r", "services/auth-patch-", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add health check module" in result.stdout, (
        f"Expected parent of auth-patch to be 'feat: add health check module', got: {result.stdout}"
    )


def test_cache_patch_parent_description_is_health_check():
    """The parent of services/cache-patch tip must have description 'feat: add health check module'."""
    result = subprocess.run(
        ["jj", "log", "-r", "services/cache-patch-", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add health check module" in result.stdout, (
        f"Expected parent of cache-patch to be 'feat: add health check module', got: {result.stdout}"
    )


def test_lib_config_py_in_auth_patch():
    """lib/config.py must be visible in services/auth-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/auth-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/config.py" in result.stdout, (
        f"lib/config.py should be in services/auth-patch after rebase. Got: {result.stdout}"
    )


def test_lib_health_py_in_auth_patch():
    """lib/health.py must be visible in services/auth-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/auth-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/health.py" in result.stdout, (
        f"lib/health.py should be in services/auth-patch after rebase. Got: {result.stdout}"
    )


def test_lib_config_py_in_cache_patch():
    """lib/config.py must be visible in services/cache-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/cache-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/config.py" in result.stdout, (
        f"lib/config.py should be in services/cache-patch after rebase. Got: {result.stdout}"
    )


def test_lib_health_py_in_cache_patch():
    """lib/health.py must be visible in services/cache-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/cache-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/health.py" in result.stdout, (
        f"lib/health.py should be in services/cache-patch after rebase. Got: {result.stdout}"
    )


def test_services_auth_py_in_auth_patch():
    """services/auth.py must still be present in services/auth-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/auth-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "services/auth.py" in result.stdout, (
        f"services/auth.py should be in services/auth-patch. Got: {result.stdout}"
    )


def test_services_cache_py_in_cache_patch():
    """services/cache.py must still be present in services/cache-patch after rebase."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/cache-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "services/cache.py" in result.stdout, (
        f"services/cache.py should be in services/cache-patch. Got: {result.stdout}"
    )


def test_auth_patch_range_from_infra_base():
    """jj log -r 'infra/base::services/auth-patch' should show health check then auth-patch commits."""
    result = subprocess.run(
        ["jj", "log", "-r", "infra/base::services/auth-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log range failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert "feat: add health check module" in lines, (
        f"'feat: add health check module' not in range output: {lines}"
    )
    assert "fix: patch auth token validation" in lines, (
        f"'fix: patch auth token validation' not in range output: {lines}"
    )


def test_cache_patch_range_from_infra_base():
    """jj log -r 'infra/base::services/cache-patch' should show health check then cache-patch commits."""
    result = subprocess.run(
        ["jj", "log", "-r", "infra/base::services/cache-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log range failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert "feat: add health check module" in lines, (
        f"'feat: add health check module' not in range output: {lines}"
    )
    assert "fix: add cache TTL enforcement" in lines, (
        f"'fix: add cache TTL enforcement' not in range output: {lines}"
    )
