import os
import subprocess
import pytest

REPO = "/home/user/repo"


def run_jj(args, cwd=REPO):
    result = subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def test_repo_exists():
    assert os.path.isdir(REPO), "Repo directory must exist"


def test_jj_initialized():
    result = run_jj(["status"])
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_main_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0
    assert "main" in result.stdout, "main bookmark must exist"


def test_feature_a_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "feature-a" in result.stdout, "feature-a bookmark must exist"


def test_feature_b_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "feature-b" in result.stdout, "feature-b bookmark must exist"


def test_feature_c_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert "feature-c" in result.stdout, "feature-c bookmark must exist"


def test_feature_a_not_in_main():
    # feature-a should have commits not reachable from main
    result = run_jj(["log", "--no-graph", "-r", "feature-a & ~ancestors(main)", "-T", "description\n"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0, "feature-a must have commits not in main"


def test_feature_b_not_in_main():
    result = run_jj(["log", "--no-graph", "-r", "feature-b & ~ancestors(main)", "-T", "description\n"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0, "feature-b must have commits not in main"


def test_feature_c_not_in_main():
    result = run_jj(["log", "--no-graph", "-r", "feature-c & ~ancestors(main)", "-T", "description\n"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0, "feature-c must have commits not in main"


def test_src_core_py_exists():
    core_path = os.path.join(REPO, "src", "core.py")
    # Check it exists in feature-a
    result = run_jj(["file", "show", "src/core.py", "-r", "feature-a"])
    assert result.returncode == 0, "src/core.py must exist in feature-a"


def test_commits_modify_core_py():
    # There should be commits modifying src/core.py in feature branches
    result = run_jj(["log", "--no-graph", "-r",
                     "feature-a | feature-b | feature-c",
                     "-T", "description\n"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0


def test_ancestry_report_not_yet_created():
    report_path = "/home/user/ancestry_report.txt"
    assert not os.path.exists(report_path), "ancestry_report.txt should not exist yet"


def test_feature_c_is_descendant_of_feature_a():
    # feature-c branches from feature-a so feature-a should be ancestor of feature-c
    result = run_jj(["log", "--no-graph", "-r", "ancestors(feature-c) & feature-a", "-T", "description\n"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0, "feature-a should be an ancestor of feature-c"
