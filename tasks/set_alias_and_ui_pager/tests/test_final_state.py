import os
import subprocess
import pytest

HOME = "/home/user"
REPO_PATH = os.path.join(HOME, "myrepo")
CONFIG_PATH = os.path.join(HOME, ".config", "jj", "config.toml")


def _parse_toml_simple(path):
    """Parse a simple TOML file into a nested dict (no external deps)."""
    import re
    result = {}
    current_section = result
    current_keys = []

    with open(path, "r") as f:
        for line in f:
            line = line.rstrip()
            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue
            # Section header
            m = re.match(r'^\[([^\]]+)\]$', line)
            if m:
                section_name = m.group(1)
                parts = section_name.split(".")
                current_keys = parts
                d = result
                for part in parts:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                current_section = d
                continue
            # Key = value
            m = re.match(r'^([a-zA-Z0-9_.-]+)\s*=\s*(.+)$', line)
            if m:
                key = m.group(1)
                val_str = m.group(2).strip()
                # Parse array
                if val_str.startswith("["):
                    inner = val_str.strip("[]")
                    items = [x.strip().strip('"') for x in inner.split(",") if x.strip()]
                    current_section[key] = items
                # Parse quoted string
                elif val_str.startswith('"') and val_str.endswith('"'):
                    current_section[key] = val_str[1:-1]
                elif val_str.startswith("'") and val_str.endswith("'"):
                    current_section[key] = val_str[1:-1]
                else:
                    current_section[key] = val_str
    return result


def test_config_file_has_aliases_st():
    config = _parse_toml_simple(CONFIG_PATH)
    assert "aliases" in config, "No [aliases] section found in config.toml"
    aliases = config["aliases"]
    assert "st" in aliases, "aliases.st not found in config.toml"
    assert aliases["st"] == ["status"], (
        f"aliases.st should equal ['status'], got {aliases['st']!r}"
    )


def test_config_file_has_ui_paginate_never():
    config = _parse_toml_simple(CONFIG_PATH)
    assert "ui" in config, "No [ui] section found in config.toml"
    ui = config["ui"]
    assert "paginate" in ui, "ui.paginate not found in config.toml"
    assert ui["paginate"] == "never", (
        f"ui.paginate should be 'never', got {ui['paginate']!r}"
    )


def test_alias_st_runs_as_status():
    result = subprocess.run(
        ["jj", "--no-pager", "st"],
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME, "JJ_CONFIG": CONFIG_PATH},
    )
    assert result.returncode == 0, (
        f"jj st failed with exit code {result.returncode}. stderr: {result.stderr}"
    )
    # jj status output should not contain "error" or "unrecognized"
    assert "unrecognized" not in result.stderr.lower(), (
        f"jj st output contained 'unrecognized': {result.stderr}"
    )


def test_jj_config_list_shows_paginate_never():
    result = subprocess.run(
        ["jj", "--no-pager", "config", "list", "--user"],
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME, "JJ_CONFIG": CONFIG_PATH},
    )
    assert result.returncode == 0, f"jj config list failed: {result.stderr}"
    assert "ui.paginate" in result.stdout, (
        f"ui.paginate not found in jj config list output: {result.stdout}"
    )
    assert "never" in result.stdout, (
        f"'never' not found in jj config list output: {result.stdout}"
    )


def test_user_identity_preserved():
    """Verify that user.name and user.email were not removed."""
    config = _parse_toml_simple(CONFIG_PATH)
    assert "user" in config, "No [user] section in config.toml"
    user = config["user"]
    assert user.get("name") == "Dev User", f"user.name changed: {user.get('name')!r}"
    assert user.get("email") == "dev@example.com", f"user.email changed: {user.get('email')!r}"
