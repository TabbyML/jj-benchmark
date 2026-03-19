import os
import re
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
PATCHES_DIR = "/home/user/patches"


def test_patches_directory_exists():
    assert os.path.isdir(PATCHES_DIR), \
        f"{PATCHES_DIR} directory does not exist."


def test_cover_letter_exists():
    path = os.path.join(PATCHES_DIR, "0000-cover-letter.patch")
    assert os.path.isfile(path), \
        f"{path} does not exist. Write the cover letter."


def test_patch_0001_exists():
    assert os.path.isfile(os.path.join(PATCHES_DIR, "0001.patch")), \
        "0001.patch does not exist."


def test_patch_0002_exists():
    assert os.path.isfile(os.path.join(PATCHES_DIR, "0002.patch")), \
        "0002.patch does not exist."


def test_patch_0003_exists():
    assert os.path.isfile(os.path.join(PATCHES_DIR, "0003.patch")), \
        "0003.patch does not exist."


def test_patch_0004_exists():
    assert os.path.isfile(os.path.join(PATCHES_DIR, "0004.patch")), \
        "0004.patch does not exist."


def test_patch_0001_has_from_header():
    with open(os.path.join(PATCHES_DIR, "0001.patch")) as f:
        content = f.read()
    assert re.search(r"^From: .+ <.+>", content, re.MULTILINE), \
        "0001.patch missing 'From: Name <email>' header"


def test_patch_0001_has_date_header():
    with open(os.path.join(PATCHES_DIR, "0001.patch")) as f:
        content = f.read()
    assert re.search(r"^Date: ", content, re.MULTILINE), \
        "0001.patch missing 'Date:' header"


def test_patch_0001_subject_is_patch_1_of_4():
    with open(os.path.join(PATCHES_DIR, "0001.patch")) as f:
        content = f.read()
    assert re.search(r"^Subject: \[PATCH 1/4\]", content, re.MULTILINE), \
        "0001.patch must have 'Subject: [PATCH 1/4] ...' line"


def test_patch_0002_subject_is_patch_2_of_4():
    with open(os.path.join(PATCHES_DIR, "0002.patch")) as f:
        content = f.read()
    assert re.search(r"^Subject: \[PATCH 2/4\]", content, re.MULTILINE), \
        "0002.patch must have 'Subject: [PATCH 2/4] ...' line"


def test_patch_0003_subject_is_patch_3_of_4():
    with open(os.path.join(PATCHES_DIR, "0003.patch")) as f:
        content = f.read()
    assert re.search(r"^Subject: \[PATCH 3/4\]", content, re.MULTILINE), \
        "0003.patch must have 'Subject: [PATCH 3/4] ...' line"


def test_patch_0004_subject_is_patch_4_of_4():
    with open(os.path.join(PATCHES_DIR, "0004.patch")) as f:
        content = f.read()
    assert re.search(r"^Subject: \[PATCH 4/4\]", content, re.MULTILINE), \
        "0004.patch must have 'Subject: [PATCH 4/4] ...' line"


def test_patches_have_separator():
    for n in ["0001", "0002", "0003", "0004"]:
        with open(os.path.join(PATCHES_DIR, f"{n}.patch")) as f:
            content = f.read()
        assert "---" in content, f"{n}.patch missing '---' separator before diff"


def test_patch_0001_contains_config_parser():
    with open(os.path.join(PATCHES_DIR, "0001.patch")) as f:
        content = f.read()
    assert "config parser" in content.lower() or "implement config" in content.lower(), \
        "0001.patch should contain 'config parser' in subject (it's the oldest commit)"


def test_cover_letter_subject():
    with open(os.path.join(PATCHES_DIR, "0000-cover-letter.patch")) as f:
        content = f.read()
    assert re.search(r"^Subject: \[PATCH 0/4\]", content, re.MULTILINE), \
        "Cover letter must have 'Subject: [PATCH 0/4] ...' line"


def test_cover_letter_has_from_header():
    with open(os.path.join(PATCHES_DIR, "0000-cover-letter.patch")) as f:
        content = f.read()
    assert re.search(r"^From: ", content, re.MULTILINE), \
        "Cover letter missing 'From:' header"


def test_patch_bundle_log_exists():
    assert os.path.isfile("/home/user/patch_bundle_log.txt"), \
        "/home/user/patch_bundle_log.txt does not exist."


def test_patch_bundle_log_has_four_lines():
    with open("/home/user/patch_bundle_log.txt") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    assert len(lines) == 4, f"patch_bundle_log.txt must have 4 lines, got {len(lines)}: {lines}"


def test_patch_bundle_log_patch_subjects():
    with open("/home/user/patch_bundle_log.txt") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    for i, line in enumerate(lines, 1):
        assert f"[PATCH {i}/4]" in line, \
            f"Line {i} of patch_bundle_log.txt should contain '[PATCH {i}/4]', got: {line}"
