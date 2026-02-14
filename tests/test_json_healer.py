"""Tests for the pb_heal_json tool — comprehensive edge-case coverage."""

from protocolbox.tools.json_healer import heal_json


class TestHealJsonBasic:
    """Basic repair and passthrough tests."""

    def test_valid_json_passthrough(self) -> None:
        """Valid JSON should pass through unchanged."""
        result = heal_json('{"name": "Alice", "age": 30}')
        assert result == {"name": "Alice", "age": 30}

    def test_valid_nested_json(self) -> None:
        """Deeply nested valid JSON should pass through."""
        inp = '{"a": {"b": {"c": {"d": 1}}}}'
        result = heal_json(inp)
        assert result["a"]["b"]["c"]["d"] == 1

    def test_valid_json_with_array(self) -> None:
        """Valid JSON containing arrays should pass through."""
        inp = '{"items": [1, 2, 3], "count": 3}'
        result = heal_json(inp)
        assert result["items"] == [1, 2, 3]
        assert result["count"] == 3


class TestHealJsonCommonFixes:
    """Common LLM output issues that json_repair should fix."""

    def test_fix_trailing_comma(self) -> None:
        result = heal_json('{"name": "Alice", "age": 30,}')
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_fix_single_quotes(self) -> None:
        result = heal_json("{'name': 'Bob'}")
        assert result["name"] == "Bob"

    def test_fix_unquoted_keys(self) -> None:
        result = heal_json("{name: 'Charlie'}")
        assert "name" in result or "Charlie" in str(result)

    def test_fix_missing_closing_brace(self) -> None:
        """Truncated JSON missing closing brace."""
        result = heal_json('{"name": "Alice"')
        assert isinstance(result, dict)
        assert "name" in result

    def test_fix_missing_closing_bracket(self) -> None:
        """Truncated JSON array missing closing bracket."""
        result = heal_json('{"data": [1, 2, 3')
        assert isinstance(result, dict)

    def test_fix_double_commas(self) -> None:
        """Double commas between values."""
        result = heal_json('{"a": 1,, "b": 2}')
        assert isinstance(result, dict)

    def test_fix_mixed_quotes(self) -> None:
        """Mixed single and double quotes."""
        result = heal_json("""{'name': "Alice", 'age': 30}""")
        assert isinstance(result, dict)

    def test_fix_nested_broken_json(self) -> None:
        """Nested broken JSON should be repaired."""
        broken = "{'users': [{'name': 'Alice',}, {'name': 'Bob'}]}"
        result = heal_json(broken)
        assert "users" in result
        assert len(result["users"]) == 2


class TestHealJsonWrapping:
    """Non-dict results should be wrapped in a dict."""

    def test_list_wrapped_in_dict(self) -> None:
        result = heal_json("[1, 2, 3]")
        assert isinstance(result, dict)
        assert "data" in result
        assert result["data"] == [1, 2, 3]

    def test_nested_list_wrapped(self) -> None:
        """A list of objects should be wrapped."""
        result = heal_json('[{"a": 1}, {"b": 2}]')
        assert isinstance(result, dict)
        assert "data" in result
        assert len(result["data"]) == 2

    def test_scalar_string_wrapped(self) -> None:
        result = heal_json('"just a string"')
        assert isinstance(result, dict)

    def test_scalar_number_wrapped(self) -> None:
        result = heal_json("42")
        assert isinstance(result, dict)

    def test_scalar_boolean_wrapped(self) -> None:
        result = heal_json("true")
        assert isinstance(result, dict)

    def test_null_wrapped(self) -> None:
        result = heal_json("null")
        assert isinstance(result, dict)


class TestHealJsonEdgeCases:
    """Unusual and extreme inputs."""

    def test_empty_string(self) -> None:
        """Empty input should return a dict (not crash)."""
        result = heal_json("")
        assert isinstance(result, dict)

    def test_whitespace_only(self) -> None:
        """Whitespace-only input should return a dict."""
        result = heal_json("   \n\t  ")
        assert isinstance(result, dict)

    def test_garbage_input(self) -> None:
        """Random garbage should return a dict."""
        result = heal_json("not json at all {{{[[[")
        assert isinstance(result, dict)

    def test_unicode_content(self) -> None:
        """Unicode values should be preserved."""
        result = heal_json('{"city": "東京", "emoji": "🎉"}')
        assert result["city"] == "東京"
        assert result["emoji"] == "🎉"

    def test_special_characters_in_values(self) -> None:
        """Special chars like newlines and tabs in values."""
        inp = '{"msg": "line1\\nline2\\ttab"}'
        result = heal_json(inp)
        assert isinstance(result, dict)
        assert "msg" in result

    def test_very_long_input(self) -> None:
        """Very long JSON string should not crash."""
        items = ", ".join(f'"k{i}": {i}' for i in range(200))
        big_json = "{" + items + "}"
        result = heal_json(big_json)
        assert isinstance(result, dict)
        assert result["k0"] == 0
        assert result["k199"] == 199

    def test_deeply_nested_structure(self) -> None:
        """Deeply nested JSON should not crash."""
        # 50 levels of nesting
        nested = '{"a": ' * 50 + "1" + "}" * 50
        result = heal_json(nested)
        assert isinstance(result, dict)

    def test_json_with_comments(self) -> None:
        """JSON with C-style comments (common LLM mistake)."""
        inp = """{
            // This is a comment
            "name": "Alice",
            /* block comment */
            "age": 30
        }"""
        result = heal_json(inp)
        assert isinstance(result, dict)

    def test_json_with_markdown_fences(self) -> None:
        """LLMs often wrap JSON in markdown code fences."""
        inp = '```json\n{"name": "Alice"}\n```'
        result = heal_json(inp)
        assert isinstance(result, dict)

    def test_return_type_always_dict(self) -> None:
        """No matter the input, return type is always dict."""
        inputs = [
            "{}",
            "[]",
            '""',
            "123",
            "true",
            "null",
            "",
            "garbage",
            '{"a": 1}',
        ]
        for inp in inputs:
            assert isinstance(heal_json(inp), dict), f"Failed for input: {inp!r}"

    def test_boolean_values_preserved(self) -> None:
        """Boolean values should be Python bool, not strings."""
        result = heal_json('{"active": true, "deleted": false}')
        assert result["active"] is True
        assert result["deleted"] is False

    def test_null_values_preserved(self) -> None:
        """Null values should be Python None."""
        result = heal_json('{"value": null}')
        assert result["value"] is None

    def test_numeric_types_preserved(self) -> None:
        """Integers and floats should retain their types."""
        result = heal_json('{"int": 42, "float": 3.14}')
        assert result["int"] == 42
        assert result["float"] == 3.14
