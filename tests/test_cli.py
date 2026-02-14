"""Tests for the ProtocolBox CLI."""

import os
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from protocolbox.cli import _detect_antigravity, _write_skill_file, app

runner = CliRunner()


class TestCliInit:
    """Test the `protocolbox init` command."""

    def test_init_runs_without_error(self) -> None:
        """init command should exit successfully."""
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0

    def test_init_prints_ready_message(self) -> None:
        """init should print a 'Ready' message."""
        result = runner.invoke(app, ["init"])
        assert "Ready" in result.output

    def test_init_prints_start_instructions(self) -> None:
        """init should tell user how to start the server."""
        result = runner.invoke(app, ["init"])
        assert "protocolbox start" in result.output

    def test_init_antigravity_detected(self, tmp_path: Path) -> None:
        """When Antigravity is detected, init should say so."""
        with patch(
            "protocolbox.cli._detect_antigravity",
            return_value=tmp_path,
        ):
            result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Antigravity" in result.output

    def test_init_no_antigravity_fallback(self) -> None:
        """Without Antigravity, init should use fallback."""
        with patch(
            "protocolbox.cli._detect_antigravity",
            return_value=None,
        ):
            result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "No Antigravity" in result.output

    def test_init_overwrites_on_repeat(self) -> None:
        """Running init twice should not crash."""
        result1 = runner.invoke(app, ["init"])
        result2 = runner.invoke(app, ["init"])
        assert result1.exit_code == 0
        assert result2.exit_code == 0


class TestWriteSkillFile:
    """Test the _write_skill_file helper directly."""

    def test_creates_skill_md(self, tmp_path: Path) -> None:
        """Should create SKILL.md in the target directory."""
        skill_path = _write_skill_file(tmp_path)
        assert skill_path.exists()
        assert skill_path.name == "SKILL.md"

    def test_skill_content(self, tmp_path: Path) -> None:
        """SKILL.md should contain tool descriptions."""
        skill_path = _write_skill_file(tmp_path)
        content = skill_path.read_text()
        assert "protocolbox" in content
        assert "scrape" in content
        assert "heal_json" in content

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Should create parent directories if needed."""
        deep_path = tmp_path / "a" / "b" / "c"
        skill_path = _write_skill_file(deep_path)
        assert skill_path.exists()

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        """Should overwrite an existing SKILL.md."""
        _write_skill_file(tmp_path)
        skill_path = _write_skill_file(tmp_path)
        assert skill_path.exists()
        content = skill_path.read_text()
        assert "protocolbox" in content


class TestDetectAntigravity:
    """Test Antigravity environment detection."""

    def test_detects_env_var(self) -> None:
        """Should detect ANTIGRAVITY_HOME env var."""
        with patch.dict(
            os.environ,
            {"ANTIGRAVITY_HOME": "/fake/path"},
        ):
            result = _detect_antigravity()
        assert result == Path("/fake/path")

    def test_detects_home_dir(self, tmp_path: Path) -> None:
        """Should detect ~/.antigravity directory."""
        ag_dir = tmp_path / ".antigravity"
        ag_dir.mkdir()
        with patch("protocolbox.cli.Path.home", return_value=tmp_path):
            with patch.dict(os.environ, {}, clear=False):
                # Remove env var if present
                os.environ.pop("ANTIGRAVITY_HOME", None)
                result = _detect_antigravity()
        assert result == ag_dir

    def test_returns_none_when_not_found(self, tmp_path: Path) -> None:
        """Should return None when no Antigravity env found."""
        with patch("protocolbox.cli.Path.home", return_value=tmp_path):
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("ANTIGRAVITY_HOME", None)
                result = _detect_antigravity()
        assert result is None

    def test_env_var_takes_priority(self, tmp_path: Path) -> None:
        """Env var should take priority over directory."""
        ag_dir = tmp_path / ".antigravity"
        ag_dir.mkdir()
        with patch.dict(
            os.environ,
            {"ANTIGRAVITY_HOME": "/env/path"},
        ):
            result = _detect_antigravity()
        assert result == Path("/env/path")


class TestCliHelp:
    """Test CLI help output."""

    def test_no_args_exits_with_usage(self) -> None:
        """Running without args should show help (exit 0)."""
        result = runner.invoke(app, [])
        # no_args_is_help=True causes Typer to show help
        assert "protocolbox" in result.output.lower() or (result.exit_code in (0, 2))

    def test_help_flag(self) -> None:
        """--help should display usage info."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "start" in result.output

    def test_init_help(self) -> None:
        """init --help should describe the command."""
        result = runner.invoke(app, ["init", "--help"])
        assert result.exit_code == 0

    def test_start_help(self) -> None:
        """start --help should describe the command."""
        result = runner.invoke(app, ["start", "--help"])
        assert result.exit_code == 0
