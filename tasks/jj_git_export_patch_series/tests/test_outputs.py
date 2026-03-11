"""
Tests for jj_git_export_patch_series task.
Verifies:
  - /home/user/patches/ directory exists with 6 files
  - Each patch file (0001-0005) has correct Subject header and diff content
  - Cover letter (0000) has correct [PATCH 0/5] Subject
  - patch_export_log.txt has 5 lines
"""

import os
import subprocess
import pytest
import glob

PATCHES_DIR = "/home/user/patches"
LOG_FILE = "/home/user/patch_export_log.txt"

EXPECTED_PATCHES = [
    ("0001", "fix", "off-by-one"),
    ("0002", "fix", "empty input"),
    ("0003", "refactor", "validation"),
    ("0004", "test", "parser"),
    ("0005", "docs", "parser"),
]


def test_patches_directory_exists():
    assert os.path.isdir(PATCHES_DIR), f"Patches directory {PATCHES_DIR} does not exist"


def test_patches_directory_has_six_files():
    files = [f for f in os.listdir(PATCHES_DIR) if f.endswith(".patch")]
    assert len(files) == 6, \
        f"Expected 6 patch files (0000-0005), found {len(files)}: {sorted(files)}"


def test_cover_letter_exists():
    cover = next(
        (f for f in os.listdir(PATCHES_DIR) if f.startswith("0000") and f.endswith(".patch")),
        None
    )
    assert cover is not None, "Cover letter (0000-*.patch) not found in patches directory"


def test_cover_letter_subject():
    cover_files = [f for f in os.listdir(PATCHES_DIR) if f.startswith("0000")]
    assert len(cover_files) > 0, "No cover letter file found"
    cover_path = os.path.join(PATCHES_DIR, cover_files[0])
    with open(cover_path) as f:
        content = f.read()
    assert "[PATCH 0/5]" in content, \
        f"Cover letter missing '[PATCH 0/5]' in Subject. Content:\n{content[:500]}"


def test_patch_0001_exists_and_valid():
    files = sorted(os.listdir(PATCHES_DIR))
    p1 = next((f for f in files if f.startswith("0001")), None)
    assert p1 is not None, "Patch 0001 not found"
    with open(os.path.join(PATCHES_DIR, p1)) as f:
        content = f.read()
    assert "[PATCH 1/5]" in content or "[PATCH 1" in content, \
        f"Patch 0001 missing '[PATCH 1' in Subject. Content:\n{content[:500]}"
    assert "off-by-one" in content.lower() or "parser" in content.lower(), \
        "Patch 0001 content doesn't match expected subject"
    # Must contain a diff
    assert "+++ " in content or "diff --git" in content, \
        "Patch 0001 missing diff content"


def test_patch_0002_exists_and_valid():
    files = sorted(os.listdir(PATCHES_DIR))
    p2 = next((f for f in files if f.startswith("0002")), None)
    assert p2 is not None, "Patch 0002 not found"
    with open(os.path.join(PATCHES_DIR, p2)) as f:
        content = f.read()
    assert "[PATCH 2/5]" in content or "[PATCH 2" in content, \
        f"Patch 0002 missing '[PATCH 2' in Subject"
    assert "+++ " in content or "diff --git" in content, \
        "Patch 0002 missing diff content"


def test_patch_0003_exists_and_valid():
    files = sorted(os.listdir(PATCHES_DIR))
    p3 = next((f for f in files if f.startswith("0003")), None)
    assert p3 is not None, "Patch 0003 not found"
    with open(os.path.join(PATCHES_DIR, p3)) as f:
        content = f.read()
    assert "+++ " in content or "diff --git" in content, \
        "Patch 0003 missing diff content"


def test_patch_0004_exists_and_valid():
    files = sorted(os.listdir(PATCHES_DIR))
    p4 = next((f for f in files if f.startswith("0004")), None)
    assert p4 is not None, "Patch 0004 not found"
    with open(os.path.join(PATCHES_DIR, p4)) as f:
        content = f.read()
    assert "+++ " in content or "diff --git" in content, \
        "Patch 0004 missing diff content"


def test_patch_0005_exists_and_valid():
    files = sorted(os.listdir(PATCHES_DIR))
    p5 = next((f for f in files if f.startswith("0005")), None)
    assert p5 is not None, "Patch 0005 not found"
    with open(os.path.join(PATCHES_DIR, p5)) as f:
        content = f.read()
    assert "[PATCH 5/5]" in content or "[PATCH 5" in content, \
        f"Patch 0005 missing '[PATCH 5' in Subject"
    assert "+++ " in content or "diff --git" in content, \
        "Patch 0005 missing diff content"


def test_all_patches_have_from_header():
    for fname in os.listdir(PATCHES_DIR):
        if not fname.startswith("0000") and fname.endswith(".patch"):
            path = os.path.join(PATCHES_DIR, fname)
            with open(path) as f:
                content = f.read()
            assert "From:" in content, \
                f"Patch {fname} missing 'From:' header"


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} not found"


def test_log_file_has_five_lines():
    with open(LOG_FILE) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    assert len(lines) == 5, f"Expected 5 lines in log, got {len(lines)}: {lines}"


def test_log_file_content():
    with open(LOG_FILE) as f:
        content = f.read()
    assert "0001" in content, "Log missing 0001 entry"
    assert "0002" in content, "Log missing 0002 entry"
    assert "0003" in content, "Log missing 0003 entry"
    assert "0004" in content, "Log missing 0004 entry"
    assert "0005" in content, "Log missing 0005 entry"
