import os
import subprocess
import pytest

REPO_DIR = "/home/user/monorepo"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory not found: {REPO_DIR}"


def test_jj_subdirectory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_scaffold_py_exists():
    path = os.path.join(REPO_DIR, "scaffold.py")
    assert os.path.isfile(path), f"scaffold.py not found at {path}"


def test_lib_config_py_exists():
    path = os.path.join(REPO_DIR, "lib", "config.py")
    assert os.path.isfile(path), f"lib/config.py not found at {path}"


def test_lib_health_py_exists():
    path = os.path.join(REPO_DIR, "lib", "health.py")
    assert os.path.isfile(path), f"lib/health.py not found at {path}"


def test_services_auth_py_in_auth_patch_branch():
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/auth-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "services/auth.py" in result.stdout, "services/auth.py not found in services/auth-patch"


def test_services_cache_py_in_cache_patch_branch():
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/cache-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "services/cache.py" in result.stdout, "services/cache.py not found in services/cache-patch"


def test_infra_base_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "infra/base" in result.stdout, "bookmark 'infra/base' not found"


def test_services_auth_patch_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "services/auth-patch" in result.stdout, "bookmark 'services/auth-patch' not found"


def test_services_cache_patch_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "services/cache-patch" in result.stdout, "bookmark 'services/cache-patch' not found"


def test_infra_base_tip_description():
    result = subprocess.run(
        ["jj", "log", "-r", "infra/base", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add health check module" in result.stdout, (
        f"Expected infra/base to point to 'feat: add health check module', got: {result.stdout}"
    )


def test_auth_patch_description():
    result = subprocess.run(
        ["jj", "log", "-r", "services/auth-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: patch auth token validation" in result.stdout, (
        f"Expected services/auth-patch description 'fix: patch auth token validation', got: {result.stdout}"
    )


def test_cache_patch_description():
    result = subprocess.run(
        ["jj", "log", "-r", "services/cache-patch", "--no-graph", "-T", 'description ++ "\\n"'],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: add cache TTL enforcement" in result.stdout, (
        f"Expected services/cache-patch description 'fix: add cache TTL enforcement', got: {result.stdout}"
    )


def test_auth_patch_not_yet_on_infra_base():
    """Before rebasing, auth-patch should NOT have lib/health.py (it's on old infra/base)."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/auth-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/health.py" not in result.stdout, (
        "lib/health.py should NOT be in services/auth-patch before rebase (branch is on old infra/base)"
    )


def test_cache_patch_not_yet_on_infra_base():
    """Before rebasing, cache-patch should NOT have lib/health.py (it's on old infra/base)."""
    result = subprocess.run(
        ["jj", "file", "list", "-r", "services/cache-patch"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "lib/health.py" not in result.stdout, (
        "lib/health.py should NOT be in services/cache-patch before rebase (branch is on old infra/base)"
    )
