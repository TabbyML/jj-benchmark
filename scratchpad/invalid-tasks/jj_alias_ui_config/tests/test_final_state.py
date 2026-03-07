import os
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myrepo"
CONFIG_PATH = "/home/user/.config/jj/config.toml"
CONFIG_VERIFICATION_FILE = "/home/user/config_verification.txt"
ALIAS_ST_OUTPUT = "/home/user/alias_st_output.txt"
ALIAS_L_OUTPUT = "/home/user/alias_l_output.txt"
JJ_BIN = "jj"


def test_user_config_file_exists():
    assert os.path.isfile(CONFIG_PATH), (
        f"User config file {CONFIG_PATH} does not exist"
    )


def test_user_config_is_nonempty():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert content.strip(), "User config file is empty"


def test_user_name_configured():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "user.name"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get user.name: {result.stderr}"
    assert result.stdout.strip() == "Alex Dev", (
        f"Expected user.name='Alex Dev', got '{result.stdout.strip()}'"
    )


def test_user_email_configured():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "user.email"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get user.email: {result.stderr}"
    assert result.stdout.strip() == "alex.dev@example.com", (
        f"Expected user.email='alex.dev@example.com', got '{result.stdout.strip()}'"
    )


def test_alias_st_configured():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "aliases.st"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get aliases.st: {result.stderr}"
    value = result.stdout.strip()
    assert "status" in value, (
        f"aliases.st should contain 'status', got '{value}'"
    )


def test_alias_l_configured():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "aliases.l"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get aliases.l: {result.stderr}"
    value = result.stdout.strip()
    assert "log" in value, (
        f"aliases.l should contain 'log', got '{value}'"
    )
    assert "--limit" in value or "10" in value, (
        f"aliases.l should reference '--limit 10', got '{value}'"
    )


def test_ui_graph_style_square():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "ui.graph.style"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get ui.graph.style: {result.stderr}"
    assert result.stdout.strip() == "square", (
        f"Expected ui.graph.style='square', got '{result.stdout.strip()}'"
    )


def test_ui_color_never():
    result = subprocess.run(
        [JJ_BIN, "config", "get", "ui.color"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"Could not get ui.color: {result.stderr}"
    assert result.stdout.strip() == "never", (
        f"Expected ui.color='never', got '{result.stdout.strip()}'"
    )


def test_config_verification_file_exists():
    assert os.path.isfile(CONFIG_VERIFICATION_FILE), (
        f"Config verification file {CONFIG_VERIFICATION_FILE} does not exist"
    )


def test_config_verification_file_contains_all_keys():
    with open(CONFIG_VERIFICATION_FILE, "r") as f:
        content = f.read()
    required_keys = [
        "user.name",
        "user.email",
        "aliases.st",
        "aliases.l",
        "ui.graph.style",
        "ui.color",
    ]
    for key in required_keys:
        assert key in content, (
            f"config_verification.txt is missing key '{key}'. Content:\n{content}"
        )


def test_alias_st_output_file_exists():
    assert os.path.isfile(ALIAS_ST_OUTPUT), (
        f"Alias st output file {ALIAS_ST_OUTPUT} does not exist"
    )


def test_alias_st_output_is_nonempty():
    with open(ALIAS_ST_OUTPUT, "r") as f:
        content = f.read()
    assert content.strip(), "alias_st_output.txt is empty"


def test_alias_l_output_file_exists():
    assert os.path.isfile(ALIAS_L_OUTPUT), (
        f"Alias l output file {ALIAS_L_OUTPUT} does not exist"
    )


def test_alias_l_output_is_nonempty():
    with open(ALIAS_L_OUTPUT, "r") as f:
        content = f.read()
    assert content.strip(), "alias_l_output.txt is empty"


def test_alias_st_works_via_jj():
    result = subprocess.run(
        [JJ_BIN, "st"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"'jj st' alias failed with return code {result.returncode}: {result.stderr}"
    )


def test_alias_l_works_via_jj():
    result = subprocess.run(
        [JJ_BIN, "l"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, (
        f"'jj l' alias failed with return code {result.returncode}: {result.stderr}"
    )
    assert result.stdout.strip(), "'jj l' produced no output"
