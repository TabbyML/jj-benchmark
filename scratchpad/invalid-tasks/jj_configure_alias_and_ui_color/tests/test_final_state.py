import os
import subprocess


CONFIG_FILE = "/home/user/.config/jj/config.toml"
REPO_DIR = "/home/user/myrepo"


def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), (
        f"Config file {CONFIG_FILE} does not exist"
    )


def test_ui_color_set_to_always():
    result = subprocess.run(
        ["jj", "config", "get", "--user", "ui.color"],
        capture_output=True,
        env={**os.environ, "HOME": "/home/user"},
    )
    assert result.returncode == 0, (
        f"jj config get --user ui.color failed: {result.stderr.decode()}"
    )
    output = result.stdout.decode().strip()
    assert output == "always", (
        f"Expected ui.color = 'always', got '{output}'"
    )


def test_ui_color_in_toml_file():
    with open(CONFIG_FILE, "r") as f:
        contents = f.read()
    assert 'color = "always"' in contents or "color = 'always'" in contents, (
        f"ui.color = \"always\" not found in {CONFIG_FILE}. Contents:\n{contents}"
    )


def test_alias_ll_in_toml_file():
    with open(CONFIG_FILE, "r") as f:
        contents = f.read()
    assert "ll" in contents, (
        f"Alias 'll' not found in {CONFIG_FILE}. Contents:\n{contents}"
    )
    assert '"log"' in contents or "'log'" in contents, (
        f"Expected 'log' command in alias definition. Contents:\n{contents}"
    )
    assert '"--limit"' in contents or "'--limit'" in contents, (
        f"Expected '--limit' in alias definition. Contents:\n{contents}"
    )
    assert '"10"' in contents or "'10'" in contents or "10" in contents, (
        f"Expected '10' in alias definition. Contents:\n{contents}"
    )


def test_alias_ll_config_get():
    result = subprocess.run(
        ["jj", "config", "list", "--user", "aliases.ll"],
        capture_output=True,
        env={**os.environ, "HOME": "/home/user"},
    )
    assert result.returncode == 0, (
        f"jj config list --user aliases.ll failed: {result.stderr.decode()}"
    )
    output = result.stdout.decode().strip()
    assert "ll" in output, (
        f"aliases.ll not found in config list output: '{output}'"
    )
    assert "log" in output, (
        f"Expected 'log' in aliases.ll config list output: '{output}'"
    )
    assert "--limit" in output, (
        f"Expected '--limit' in aliases.ll config list output: '{output}'"
    )


def test_alias_ll_runs_successfully():
    result = subprocess.run(
        ["jj", "ll"],
        capture_output=True,
        cwd=REPO_DIR,
        env={**os.environ, "HOME": "/home/user"},
    )
    assert result.returncode == 0, (
        f"jj ll failed with exit code {result.returncode}: {result.stderr.decode()}"
    )
