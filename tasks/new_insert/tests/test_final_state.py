import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_feature_file_exists():
    feature_path = os.path.join(PROJECT_DIR, "feature.txt")
    assert os.path.isfile(feature_path), "feature.txt does not exist in the working directory."
    with open(feature_path, "r") as f:
        content = f.read()
    assert content == "new feature\n", f"Expected 'new feature\\n', got {repr(content)}"

def test_commit_stack_order():
    # We want to verify the lineage: A -> new commit -> B -> C
    # The working copy (@) should be C or a child of C. Let's just check the ancestors of the commit with description "commit C".
    # Since C might have been rebased, its change ID is preserved but commit ID changed.
    # We can query jj log to get the sequence of descriptions.
    
    # Get change IDs for A, B, C
    id_a = subprocess.run(["jj", "log", "-r", "description(\"commit A\\n\")", "-T", "change_id", "--no-graph"], cwd=PROJECT_DIR, capture_output=True, text=True).stdout.strip()
    id_b = subprocess.run(["jj", "log", "-r", "description(\"commit B\\n\")", "-T", "change_id", "--no-graph"], cwd=PROJECT_DIR, capture_output=True, text=True).stdout.strip()
    id_c = subprocess.run(["jj", "log", "-r", "description(\"commit C\\n\")", "-T", "change_id", "--no-graph"], cwd=PROJECT_DIR, capture_output=True, text=True).stdout.strip()

    # Let's get the log from the root to the commit C
    result = subprocess.run(
        ["jj", "log", "-r", f"::{id_c}", "-T", "change_id ++ \"\\n\"", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"

    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]

    try:
        idx_a = lines.index(id_a)
        idx_b = lines.index(id_b)
        idx_c = lines.index(id_c)
    except ValueError as e:
        pytest.fail(f"Missing expected commit in history: {e}. Output was: {lines}")
    
    assert idx_c < idx_b, "'commit C' should be a descendant of 'commit B'"
    assert idx_b < idx_a, "'commit B' should be a descendant of 'commit A'"
    
    # There should be exactly one commit between A and B
    assert idx_a - idx_b == 2, f"Expected exactly one commit between 'commit A' and 'commit B', but found {idx_a - idx_b - 1}."

def test_new_commit_adds_feature_txt():
    # Find the commit between A and B
    id_a = subprocess.run(["jj", "log", "-r", "description(\"commit A\\n\")", "-T", "change_id", "--no-graph"], cwd=PROJECT_DIR, capture_output=True, text=True).stdout.strip()
    id_b = subprocess.run(["jj", "log", "-r", "description(\"commit B\\n\")", "-T", "change_id", "--no-graph"], cwd=PROJECT_DIR, capture_output=True, text=True).stdout.strip()

    result = subprocess.run(
        ["jj", "log", "-r", f"{id_a}..{id_b}", "-T", "change_id ++ \"\\n\"", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    
    # The range A..B includes B, and the intermediate commit(s).
    # Since we asserted idx_b - idx_a == 2, there should be exactly 2 commits here: the new commit, and B.
    assert len(lines) == 2, f"Expected 2 commits in range A..B, got {len(lines)}: {lines}"
    
    new_commit_change_id = lines[1]
    
    # Verify that this new commit introduced feature.txt
    show_result = subprocess.run(
        ["jj", "show", new_commit_change_id],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "feature.txt" in show_result.stdout, f"New commit does not seem to modify feature.txt. Output: {show_result.stdout}"
