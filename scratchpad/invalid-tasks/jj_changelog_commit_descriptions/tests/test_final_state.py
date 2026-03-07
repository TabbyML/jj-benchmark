import os
import subprocess
import pytest

REPO_DIR = "/home/user/myrepo"


def _jj(*args, cwd=REPO_DIR):
    result = subprocess.run(
        ["jj"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def test_docs_readme_description_corrected():
    """The docs(readme) commit must have the corrected spelling 'contribution' (not 'contributing')."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'docs(readme): add contribution guide')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "docs(readme): add contribution guide" in result.stdout, \
        "Corrected description 'docs(readme): add contribution guide' must exist"


def test_docs_readme_old_description_gone():
    """The old mis-spelled 'contributing guide' description must no longer exist."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(exact:'docs(readme): add contributing guide\n')",
        "--template", "description",
    )
    # Should either fail (no match) or return empty — not find the old spelling
    assert "contributing guide" not in result.stdout or result.returncode != 0, \
        "Old description 'docs(readme): add contributing guide' must be gone"


def test_docs_readme_change_id_trailer():
    """The docs(readme) commit must contain the Change-Id trailer."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'docs(readme): add contribution guide')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Idocs000000000000000000000000000000000000" in result.stdout, \
        "docs(readme) commit must contain Change-Id: Idocs000000000000000000000000000000000000"


def test_feat_changelog_commit_exists():
    """The feat(changelog) commit must exist with correct first line."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'feat(changelog): add CHANGELOG file')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat(changelog): add CHANGELOG file" in result.stdout, \
        "Commit 'feat(changelog): add CHANGELOG file' must exist"


def test_feat_changelog_change_id_trailer():
    """The feat(changelog) commit must contain the correct Change-Id trailer."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'feat(changelog): add CHANGELOG file')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "I0000000000000000000000000000000000000001" in result.stdout, \
        "feat(changelog) commit must contain Change-Id: I0000000000000000000000000000000000000001"


def test_feat_changelog_body_present():
    """The feat(changelog) commit description must include the body paragraph."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'feat(changelog): add CHANGELOG file')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "Adds the initial CHANGELOG.md" in result.stdout, \
        "feat(changelog) commit description must include the body paragraph"


def test_fix_parser_commit_exists():
    """The fix(parser) commit must exist with correct first line."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'fix(parser): correct off-by-one error in line counter')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix(parser): correct off-by-one error in line counter" in result.stdout, \
        "Commit 'fix(parser): correct off-by-one error in line counter' must exist"


def test_fix_parser_change_id_trailer():
    """The fix(parser) commit must contain the correct Change-Id trailer."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'fix(parser): correct off-by-one error in line counter')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "I0000000000000000000000000000000000000002" in result.stdout, \
        "fix(parser) commit must contain Change-Id: I0000000000000000000000000000000000000002"


def test_fix_parser_body_present():
    """The fix(parser) commit description must include the body paragraph."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'fix(parser): correct off-by-one error in line counter')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "off-by-one" in result.stdout, \
        "fix(parser) commit description must include the body paragraph mentioning 'off-by-one'"


def test_changelog_md_exists_in_feat_commit():
    """CHANGELOG.md must exist in the feat(changelog) commit's tree."""
    result = _jj(
        "file", "list", "--no-pager",
        "-r", "description(substring:'feat(changelog): add CHANGELOG file')",
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "CHANGELOG.md" in result.stdout, \
        "CHANGELOG.md must be present in the feat(changelog) commit"


def test_working_copy_parent_is_fix_parser():
    """The working-copy parent (@-) must be the fix(parser) commit."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "@-",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log @- failed: {result.stderr}"
    assert "fix(parser): correct off-by-one error in line counter" in result.stdout, \
        "Parent of working copy must be the fix(parser) commit"


def test_chore_init_commit_unchanged():
    """The original chore(init) commit must still exist unchanged."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "description(substring:'chore(init): initialise project skeleton')",
        "--template", "description",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore(init): initialise project skeleton" in result.stdout, \
        "Original chore(init) commit must still exist"


def test_commit_order_is_correct():
    """The four non-empty commits must appear in the correct topological order."""
    result = _jj(
        "log", "--no-pager", "--no-graph",
        "-r", "::@ ~ root()",
        "--template", "description.first_line() ++ '\\n'",
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    assert lines.index("chore(init): initialise project skeleton") < \
           lines.index("docs(readme): add contribution guide"), \
        "chore(init) must come before docs(readme)"
    assert lines.index("docs(readme): add contribution guide") < \
           lines.index("feat(changelog): add CHANGELOG file"), \
        "docs(readme) must come before feat(changelog)"
    assert lines.index("feat(changelog): add CHANGELOG file") < \
           lines.index("fix(parser): correct off-by-one error in line counter"), \
        "feat(changelog) must come before fix(parser)"
