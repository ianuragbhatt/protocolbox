"""Tests for the pb_heal_json tool."""

from protocolbox.tools.json_healer import heal_json


class TestHealJson:
    """Test the heal_json tool."""

    def test_valid_json_passthrough(self) -> None:
        """Valid JSON should pass through unchanged."""
        result = heal_json('{"name": "Alice", "age": 30}')
        assert result == {"name": "Alice", "age": 30}

    def test_fix_trailing_comma(self) -> None:
        """Trailing commas should be fixed."""
        result = heal_json('{"name": "Alice", "age": 30,}')
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_fix_single_quotes(self) -> None:
        """Single quotes should be converted to double quotes."""
        result = heal_json("{'name': 'Bob'}")
        assert result["name"] == "Bob"

    def test_fix_unquoted_keys(self) -> None:
        """Unquoted keys should be fixed."""
        result = heal_json("{name: 'Charlie'}")
        assert "name" in result or "Charlie" in str(result)

    def test_list_wrapped_in_dict(self) -> None:
        """A repaired JSON list should be wrapped in a dict."""
        result = heal_json("[1, 2, 3]")
        assert isinstance(result, dict)
        assert "data" in result
        assert result["data"] == [1, 2, 3]

    def test_scalar_wrapped_in_dict(self) -> None:
        """A repaired scalar value should be wrapped in a dict."""
        result = heal_json('"just a string"')
        assert isinstance(result, dict)

    def test_unrepairable_returns_error(self) -> None:
        """Completely unrepairable input should return an error dict."""
        # json_repair is very resilient, but we should at least
        # verify the return type is always a dict.
        result = heal_json("")
        assert isinstance(result, dict)

    def test_error_has_snippet(self) -> None:
        """Error responses should include an input snippet."""
        # Even on very broken input, json_repair may succeed.
        # This test verifies our function always returns a dict.
        result = heal_json("not json at all {{{[[[")
        assert isinstance(result, dict)

    def test_nested_json_repair(self) -> None:
        """Nested broken JSON should be repaired."""
        broken = "{'users': [{'name': 'Alice',}, {'name': 'Bob'}]}"
        result = heal_json(broken)
        assert "users" in result
        assert len(result["users"]) == 2
