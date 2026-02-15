"""Tests for the pb_memory tool — comprehensive persistence and edge-case coverage."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from protocolbox.tools.memory import _load_memory, _save_memory, recall, remember


@pytest.fixture()
def tmp_memory(tmp_path: Path):
    """Redirect memory storage to a temp directory for test isolation."""
    memory_dir = tmp_path / ".protocolbox"
    memory_file = memory_dir / "memory.json"
    with (
        patch("protocolbox.tools.memory._MEMORY_DIR", memory_dir),
        patch("protocolbox.tools.memory._MEMORY_FILE", memory_file),
    ):
        yield memory_file


class TestRememberBasic:
    """Basic happy-path tests for remember()."""

    def test_remember_returns_confirmation(self, tmp_memory: Path) -> None:
        result = remember("name", "Alice")
        assert "Remembered" in result
        assert "name" in result

    def test_remember_creates_file(self, tmp_memory: Path) -> None:
        remember("key", "value")
        assert tmp_memory.exists()

    def test_remember_stores_correct_value(self, tmp_memory: Path) -> None:
        remember("color", "blue")
        data = json.loads(tmp_memory.read_text())
        assert data["color"] == "blue"

    def test_remember_multiple_keys(self, tmp_memory: Path) -> None:
        remember("a", "1")
        remember("b", "2")
        remember("c", "3")
        data = json.loads(tmp_memory.read_text())
        assert data == {"a": "1", "b": "2", "c": "3"}

    def test_remember_overwrites_existing_key(self, tmp_memory: Path) -> None:
        remember("key", "old")
        remember("key", "new")
        data = json.loads(tmp_memory.read_text())
        assert data["key"] == "new"

    def test_remember_return_type_is_string(self, tmp_memory: Path) -> None:
        assert isinstance(remember("k", "v"), str)


class TestRecallBasic:
    """Basic happy-path tests for recall()."""

    def test_recall_existing_key(self, tmp_memory: Path) -> None:
        remember("name", "Bob")
        result = recall("name")
        assert result == "Bob"

    def test_recall_returns_correct_value(self, tmp_memory: Path) -> None:
        remember("score", "100")
        assert recall("score") == "100"

    def test_recall_missing_key(self, tmp_memory: Path) -> None:
        result = recall("nonexistent")
        assert "not found" in result.lower() or "Memory not found" in result

    def test_recall_missing_key_includes_key_name(self, tmp_memory: Path) -> None:
        result = recall("my_special_key")
        assert "my_special_key" in result

    def test_recall_return_type_is_string(self, tmp_memory: Path) -> None:
        assert isinstance(recall("anything"), str)


class TestMemoryPersistence:
    """Test that memory persists correctly between operations."""

    def test_round_trip(self, tmp_memory: Path) -> None:
        remember("round_trip", "data")
        assert recall("round_trip") == "data"

    def test_multiple_round_trips(self, tmp_memory: Path) -> None:
        for i in range(10):
            remember(f"key_{i}", f"value_{i}")
        for i in range(10):
            assert recall(f"key_{i}") == f"value_{i}"

    def test_overwrite_and_recall(self, tmp_memory: Path) -> None:
        remember("version", "1")
        remember("version", "2")
        assert recall("version") == "2"

    def test_recall_after_multiple_writes(self, tmp_memory: Path) -> None:
        """Writing different keys should not affect earlier keys."""
        remember("first", "A")
        remember("second", "B")
        remember("third", "C")
        assert recall("first") == "A"

    def test_json_file_is_valid_json(self, tmp_memory: Path) -> None:
        remember("test", "data")
        data = json.loads(tmp_memory.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_json_file_is_pretty_printed(self, tmp_memory: Path) -> None:
        """The JSON file should be human-readable (indented)."""
        remember("test", "data")
        content = tmp_memory.read_text(encoding="utf-8")
        assert "\n" in content  # Indented JSON has newlines


class TestMemoryEdgeCases:
    """Edge cases and unusual inputs."""

    def test_empty_key(self, tmp_memory: Path) -> None:
        """An empty string key should still work."""
        remember("", "empty_key_value")
        assert recall("") == "empty_key_value"

    def test_empty_value(self, tmp_memory: Path) -> None:
        """An empty string value should be stored."""
        remember("empty_val", "")
        assert recall("empty_val") == ""

    def test_unicode_key(self, tmp_memory: Path) -> None:
        remember("名前", "太郎")
        assert recall("名前") == "太郎"

    def test_unicode_value(self, tmp_memory: Path) -> None:
        remember("emoji", "🚀🎉")
        assert recall("emoji") == "🚀🎉"

    def test_very_long_key(self, tmp_memory: Path) -> None:
        long_key = "k" * 1000
        remember(long_key, "long")
        assert recall(long_key) == "long"

    def test_very_long_value(self, tmp_memory: Path) -> None:
        long_value = "v" * 10000
        remember("long_val", long_value)
        assert recall("long_val") == long_value

    def test_special_chars_in_key(self, tmp_memory: Path) -> None:
        remember("key/with.special!chars@#$", "special")
        assert recall("key/with.special!chars@#$") == "special"

    def test_special_chars_in_value(self, tmp_memory: Path) -> None:
        remember("special_val", "quotes \"and\" 'single' & <tags>")
        assert recall("special_val") == "quotes \"and\" 'single' & <tags>"

    def test_multiline_value(self, tmp_memory: Path) -> None:
        """Multiline strings should be preserved."""
        value = "line1\nline2\nline3"
        remember("multi", value)
        assert recall("multi") == value

    def test_json_like_value(self, tmp_memory: Path) -> None:
        """A JSON string as a value should be stored as-is."""
        value = '{"nested": "json"}'
        remember("json_val", value)
        assert recall("json_val") == value

    def test_whitespace_key(self, tmp_memory: Path) -> None:
        """Keys with whitespace should work."""
        remember("  spaced key  ", "value")
        assert recall("  spaced key  ") == "value"


class TestMemoryCorruptedFile:
    """Tests for corrupted or missing memory file."""

    def test_recall_when_no_file_exists(self, tmp_memory: Path) -> None:
        """Recall should return not-found when no file exists."""
        result = recall("anything")
        assert "not found" in result.lower() or "Memory not found" in result

    def test_remember_creates_directory(self, tmp_memory: Path) -> None:
        """The .protocolbox directory should be created on first write."""
        remember("first", "write")
        assert tmp_memory.parent.is_dir()

    def test_corrupted_json_file_recover(self, tmp_memory: Path) -> None:
        """A corrupted memory file should not crash recall."""
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        tmp_memory.write_text("not valid json {{{", encoding="utf-8")
        result = recall("key")
        assert "not found" in result.lower() or "Memory not found" in result

    def test_corrupted_json_file_remember_recovers(self, tmp_memory: Path) -> None:
        """Remember should overwrite a corrupted memory file."""
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        tmp_memory.write_text("broken!!!", encoding="utf-8")
        result = remember("key", "value")
        assert "Remembered" in result
        assert recall("key") == "value"

    def test_empty_json_file(self, tmp_memory: Path) -> None:
        """An empty file should not crash."""
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        tmp_memory.write_text("", encoding="utf-8")
        result = recall("key")
        assert "not found" in result.lower() or "Memory not found" in result


class TestLoadSaveMemoryHelpers:
    """Direct tests for _load_memory and _save_memory."""

    def test_load_empty(self, tmp_memory: Path) -> None:
        assert _load_memory() == {}

    def test_save_then_load(self, tmp_memory: Path) -> None:
        _save_memory({"a": "1", "b": "2"})
        assert _load_memory() == {"a": "1", "b": "2"}

    def test_save_creates_dir(self, tmp_memory: Path) -> None:
        _save_memory({"test": "data"})
        assert tmp_memory.parent.is_dir()

    def test_load_corrupted_returns_empty(self, tmp_memory: Path) -> None:
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        tmp_memory.write_text("corrupted", encoding="utf-8")
        assert _load_memory() == {}

    def test_save_overwrites_completely(self, tmp_memory: Path) -> None:
        _save_memory({"first": "1"})
        _save_memory({"second": "2"})
        result = _load_memory()
        assert "first" not in result
        assert result == {"second": "2"}
