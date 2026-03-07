import os
import subprocess

REPO_DIR = "/home/user/upstream-project"

EXPECTED_FILE_CONTENT = (
    "def load_data(path):\n"
    "    with open(path) as f:\n"
    "        return f.read()\n"
    "\n"
    "def process_data(raw):\n"
    "    return raw.strip()\n"
)


def test_no_conflicted_commits():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "conflicts()"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # conflicts() should return empty — no lines with commit info
    output = result.stdout.strip()
    assert output == "", (
        f"Expected no conflicted commits, but got:\n{output}"
    )


def test_resolve_list_is_empty():
    result = subprocess.run(
        ["jj", "resolve", "--list", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj resolve --list failed: {result.stderr}"
    output = result.stdout.strip()
    assert output == "", (
        f"Expected no unresolved conflicts, but jj resolve --list output:\n{output}"
    )


def test_feature_bookmark_exists_and_not_conflicted():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "feature", "--no-graph", "-T", "description"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log for feature bookmark failed: {result.stderr}"
    assert result.stdout.strip() != "", "feature bookmark should point to a commit"


def test_main_bookmark_points_to_v2():
    # Verify main bookmark has been updated to main-v2
    # Both should resolve to the same commit
    result_main = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "main", "--no-graph", "-T", "commit_id"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    result_v2 = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "main-v2", "--no-graph", "-T", "commit_id"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result_main.returncode == 0, f"jj log for main failed: {result_main.stderr}"
    assert result_v2.returncode == 0, f"jj log for main-v2 failed: {result_v2.stderr}"
    assert result_main.stdout.strip() == result_v2.stdout.strip(), (
        "main bookmark does not point to the same commit as main-v2.\n"
        f"  main -> {result_main.stdout.strip()}\n"
        f"  main-v2 -> {result_v2.stdout.strip()}"
    )


def test_resolved_file_content_in_feature_stack():
    # Check the content of src/data.py at the commit just before feature (feature-patch-1)
    # by looking at all commits in the feature stack that are not the empty WC commit
    result = subprocess.run(
        ["jj", "file", "show", "-r", "feature-", "src/data.py", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    # feature- is the parent of feature bookmark (feature-patch-1 after rebase)
    if result.returncode != 0:
        # fallback: try checking at feature bookmark itself
        result = subprocess.run(
            ["jj", "file", "show", "-r", "feature", "src/data.py", "--no-pager"],
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
        )
    assert result.returncode == 0, f"Could not read src/data.py from jj: {result.stderr}"
    actual = result.stdout
    # The file at feature-patch-1 (parent of feature-patch-2) should contain the resolved content
    # feature-patch-2 (the feature bookmark) adds logging, so let's check feature-patch-1's
    # resolved version specifically
    # We check that the resolved load_data with context manager is present
    assert "with open(path) as f:" in actual, (
        f"Resolved 'with open' form not found in src/data.py at feature- :\n{actual}"
    )
    assert "def process_data(raw):" in actual, (
        f"process_data function not found in src/data.py at feature- :\n{actual}"
    )


def test_resolved_file_at_feature_minus():
    result = subprocess.run(
        ["jj", "file", "show", "-r", "feature-", "src/data.py", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj file show failed: {result.stderr}"
    actual = result.stdout
    assert actual == EXPECTED_FILE_CONTENT, (
        f"src/data.py at feature- does not match expected content.\n"
        f"Expected:\n{EXPECTED_FILE_CONTENT!r}\n"
        f"Got:\n{actual!r}"
    )


def test_no_conflict_markers_in_working_copy():
    data_py = os.path.join(REPO_DIR, "src", "data.py")
    if os.path.isfile(data_py):
        with open(data_py) as f:
            content = f.read()
        assert "<<<<<<<" not in content, "Conflict markers found in working copy src/data.py"
        assert ">>>>>>>" not in content, "Conflict markers found in working copy src/data.py"
