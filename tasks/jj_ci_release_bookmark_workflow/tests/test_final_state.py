import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"

RELEASE_DESC = "release: v1.0 \u2014 bundle auth, payment, and notification"


def run(cmd, cwd=REPO_DIR):
    env = dict(os.environ)
    env["JJ_NO_PAGER"] = "1"
    env["PAGER"] = "cat"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env
    )
    return result


def test_squashed_commit_exists_with_correct_description():
    """Exactly one squashed release commit exists with the required description."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"release: v1.0\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Expected exactly 1 release commit, got {len(lines)}: {result.stdout!r}"
    )
    assert lines[0].startswith("release: v1.0"), (
        f"Release commit description wrong. Got: {lines[0]!r}"
    )
    assert "bundle auth, payment, and notification" in lines[0], (
        f"Description missing bundle text. Got: {lines[0]!r}"
    )


def test_squashed_commit_contains_all_three_files():
    """The squashed release commit contains src/auth.py, src/payment.py, src/notify.py."""
    result = run(
        "jj file list -r 'description(substring:\"release: v1.0\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/auth.py" in result.stdout, (
        f"src/auth.py missing from release commit. Files: {result.stdout}"
    )
    assert "src/payment.py" in result.stdout, (
        f"src/payment.py missing from release commit. Files: {result.stdout}"
    )
    assert "src/notify.py" in result.stdout, (
        f"src/notify.py missing from release commit. Files: {result.stdout}"
    )


def test_only_one_mutable_non_root_non_wc_commit():
    """There is exactly one mutable non-root non-working-copy commit (the squashed release)."""
    result = run(
        "jj log --no-graph -r 'mutable() & ~@ & ~root()' -T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Expected exactly 1 mutable non-root non-wc commit after squash, got {len(lines)}: "
        f"{result.stdout!r}"
    )


def test_original_feature_commits_gone():
    """The three original feature commits no longer exist as separate commits."""
    for desc in [
        "feat: add authentication module",
        "feat: add payment processing",
        "feat: add notification service",
    ]:
        result = run(
            f"jj log --no-graph -r 'description(substring:\"{desc}\")' "
            "-T 'change_id ++ \"\\n\"'"
        )
        assert result.returncode == 0, f"jj log failed: {result.stderr}"
        lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
        assert len(lines) == 0, (
            f"Original commit '{desc}' still exists but should have been squashed away. "
            f"Got: {result.stdout!r}"
        )


def test_bookmark_release_v1_0_exists():
    """A bookmark named 'release/v1.0' exists."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "release/v1.0" in result.stdout, (
        f"Bookmark 'release/v1.0' not found. Got: {result.stdout!r}"
    )


def test_bookmark_release_v1_0_points_to_release_commit():
    """The bookmark 'release/v1.0' points to the squashed release commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"release/v1.0\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "release: v1.0" in result.stdout, (
        f"Bookmark 'release/v1.0' does not point to release commit. Got: {result.stdout!r}"
    )
    assert "bundle auth, payment, and notification" in result.stdout, (
        f"Bookmark points to wrong commit. Got: {result.stdout!r}"
    )


def test_tag_v1_0_exists():
    """A tag named 'v1.0' exists."""
    result = run("jj tag list")
    assert result.returncode == 0, f"jj tag list failed: {result.stderr}"
    assert "v1.0" in result.stdout, (
        f"Tag 'v1.0' not found. Got: {result.stdout!r}"
    )


def test_tag_v1_0_points_to_release_commit():
    """The tag 'v1.0' points to the squashed release commit."""
    result = run(
        "jj log --no-graph -r 'tags(\"v1.0\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "release: v1.0" in result.stdout, (
        f"Tag 'v1.0' does not point to release commit. Got: {result.stdout!r}"
    )
    assert "bundle auth, payment, and notification" in result.stdout, (
        f"Tag points to wrong commit. Got: {result.stdout!r}"
    )


def test_working_copy_is_empty_child_of_release_commit():
    """The working copy is an empty commit whose parent is the squashed release commit."""
    wc_result = run("jj log --no-graph -r '@' -T 'description ++ \"\\n\"'")
    assert wc_result.returncode == 0, f"jj log @ failed: {wc_result.stderr}"
    wc_desc = wc_result.stdout.strip()
    assert wc_desc == "", (
        f"Working copy should have empty description, got: {wc_desc!r}"
    )

    parent_result = run(
        "jj log --no-graph -r '@-' -T 'description ++ \"\\n\"'"
    )
    assert parent_result.returncode == 0, f"jj log @- failed: {parent_result.stderr}"
    assert "release: v1.0" in parent_result.stdout, (
        f"Parent of working copy is not the release commit. Got: {parent_result.stdout!r}"
    )


def test_bookmark_and_tag_point_to_same_commit_as_wc_parent():
    """The bookmark 'release/v1.0' and tag 'v1.0' both point to @-."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"release/v1.0\") & @-' -T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Bookmark 'release/v1.0' is not pointing at @- (parent of working copy). "
        f"Got: {result.stdout!r}"
    )

    result2 = run(
        "jj log --no-graph -r 'tags(\"v1.0\") & @-' -T 'change_id ++ \"\\n\"'"
    )
    assert result2.returncode == 0, f"jj log failed: {result2.stderr}"
    lines2 = [l.strip() for l in result2.stdout.strip().splitlines() if l.strip()]
    assert len(lines2) == 1, (
        f"Tag 'v1.0' is not pointing at @- (parent of working copy). "
        f"Got: {result2.stdout!r}"
    )
