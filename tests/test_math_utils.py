"""Tests for the pb_safe_math tool — comprehensive security and edge-case coverage."""

import math

from protocolbox.tools.math_utils import safe_math


class TestSafeMathBasicArithmetic:
    """Basic arithmetic operations."""

    def test_addition(self) -> None:
        assert safe_math("2 + 3") == "5"

    def test_subtraction(self) -> None:
        assert safe_math("10 - 4") == "6"

    def test_multiplication(self) -> None:
        assert safe_math("6 * 7") == "42"

    def test_division(self) -> None:
        assert safe_math("10 / 4") == "2.5"

    def test_power(self) -> None:
        assert safe_math("2 ** 10") == "1024"

    def test_modulo(self) -> None:
        assert safe_math("17 % 5") == "2"

    def test_integer_result(self) -> None:
        assert safe_math("3 + 4") == "7"

    def test_float_result(self) -> None:
        assert safe_math("1 / 3") == str(1 / 3)

    def test_negative_numbers(self) -> None:
        assert safe_math("-5 + 3") == "-2"

    def test_unary_positive(self) -> None:
        assert safe_math("+5") == "5"

    def test_unary_negative(self) -> None:
        assert safe_math("-42") == "-42"


class TestSafeMathComplexExpressions:
    """Complex and compound expressions."""

    def test_order_of_operations(self) -> None:
        assert safe_math("2 + 3 * 4") == "14"

    def test_parenthesized_expression(self) -> None:
        assert safe_math("(2 + 3) * 4") == "20"

    def test_nested_parentheses(self) -> None:
        assert safe_math("((1 + 2) * (3 + 4))") == "21"

    def test_mixed_operators(self) -> None:
        assert safe_math("10 + 5 * 2 - 3 / 1") == "17.0"

    def test_chained_powers(self) -> None:
        # 2 ** 3 ** 2 = 2 ** 9 = 512 (right-associative)
        assert safe_math("2 ** 3 ** 2") == "512"

    def test_float_literal(self) -> None:
        assert safe_math("3.14 * 2") == str(3.14 * 2)

    def test_large_numbers(self) -> None:
        result = safe_math("999999999 * 999999999")
        assert result == str(999999999 * 999999999)

    def test_very_small_float(self) -> None:
        result = safe_math("0.0001 * 0.0001")
        assert float(result) == 0.0001 * 0.0001


class TestSafeMathFunctions:
    """Math module function tests."""

    def test_sqrt(self) -> None:
        assert safe_math("sqrt(16)") == "4.0"

    def test_sqrt_non_perfect(self) -> None:
        assert safe_math("sqrt(2)") == str(math.sqrt(2))

    def test_floor(self) -> None:
        assert safe_math("floor(3.7)") == "3"

    def test_floor_negative(self) -> None:
        assert safe_math("floor(-3.2)") == "-4"

    def test_ceil(self) -> None:
        assert safe_math("ceil(3.1)") == "4"

    def test_ceil_negative(self) -> None:
        assert safe_math("ceil(-3.7)") == "-3"

    def test_abs_positive(self) -> None:
        assert safe_math("abs(5)") == "5"

    def test_abs_negative(self) -> None:
        assert safe_math("abs(-5)") == "5"

    def test_sin_zero(self) -> None:
        assert safe_math("sin(0)") == "0.0"

    def test_cos_zero(self) -> None:
        assert safe_math("cos(0)") == "1.0"

    def test_tan_zero(self) -> None:
        assert safe_math("tan(0)") == "0.0"

    def test_log_natural(self) -> None:
        assert safe_math("log(1)") == "0.0"

    def test_log_e(self) -> None:
        result = float(safe_math("log(2.718281828)"))
        assert abs(result - 1.0) < 0.0001

    def test_function_with_expression_arg(self) -> None:
        assert safe_math("sqrt(4 + 12)") == "4.0"

    def test_function_in_expression(self) -> None:
        assert safe_math("sqrt(16) + 2 ** 3") == "12.0"

    def test_nested_function_calls(self) -> None:
        assert safe_math("abs(floor(-3.7))") == "4"


class TestSafeMathSecurity:
    """Security tests — ensure no code injection is possible."""

    def test_rejects_import(self) -> None:
        result = safe_math("__import__('os')")
        assert "Error" in result

    def test_rejects_eval(self) -> None:
        result = safe_math("eval('1+1')")
        assert "Error" in result

    def test_rejects_exec(self) -> None:
        result = safe_math("exec('print(1)')")
        assert "Error" in result

    def test_rejects_open(self) -> None:
        result = safe_math("open('/etc/passwd')")
        assert "Error" in result

    def test_rejects_os_system(self) -> None:
        result = safe_math("os.system('ls')")
        assert "Error" in result

    def test_rejects_attribute_access(self) -> None:
        result = safe_math("(1).__class__")
        assert "Error" in result

    def test_rejects_lambda(self) -> None:
        result = safe_math("(lambda: 1)()")
        assert "Error" in result

    def test_rejects_list_comprehension(self) -> None:
        result = safe_math("[x for x in range(10)]")
        assert "Error" in result

    def test_rejects_string_literals(self) -> None:
        result = safe_math("'hello'")
        assert "Error" in result

    def test_rejects_unknown_function(self) -> None:
        result = safe_math("print(42)")
        assert "Error" in result
        assert "Unknown function" in result

    def test_rejects_dunder_methods(self) -> None:
        result = safe_math("__builtins__")
        assert "Error" in result

    def test_no_eval_used_in_implementation(self) -> None:
        """Verify the source code does not use Python's builtin eval()."""
        from pathlib import Path

        import protocolbox.tools.math_utils as mod

        source = Path(mod.__file__).read_text(encoding="utf-8")
        # Remove all _safe_eval references and docstrings to avoid false positives.
        cleaned = source.replace("_safe_eval", "")
        # Remove docstrings (triple-quoted strings).
        import re

        cleaned = re.sub(r'""".*?"""', "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"'''.*?'''", "", cleaned, flags=re.DOTALL)
        assert "eval(" not in cleaned


class TestSafeMathErrors:
    """Error conditions and invalid inputs."""

    def test_division_by_zero(self) -> None:
        result = safe_math("1 / 0")
        assert "Error" in result

    def test_modulo_by_zero(self) -> None:
        result = safe_math("10 % 0")
        assert "Error" in result

    def test_sqrt_negative(self) -> None:
        result = safe_math("sqrt(-1)")
        assert "Error" in result

    def test_log_zero(self) -> None:
        result = safe_math("log(0)")
        assert "Error" in result

    def test_log_negative(self) -> None:
        result = safe_math("log(-1)")
        assert "Error" in result

    def test_empty_string(self) -> None:
        result = safe_math("")
        assert "Error" in result

    def test_whitespace_only(self) -> None:
        result = safe_math("   ")
        assert "Error" in result

    def test_invalid_syntax(self) -> None:
        result = safe_math("2 +* 3")
        assert "Error" in result

    def test_unmatched_parentheses(self) -> None:
        result = safe_math("(2 + 3")
        assert "Error" in result

    def test_garbage_input(self) -> None:
        result = safe_math("not a math expression")
        assert "Error" in result

    def test_return_type_always_string(self) -> None:
        """Return type should always be str, even on errors."""
        inputs = ["2 + 3", "1/0", "garbage", "", "sqrt(4)"]
        for inp in inputs:
            assert isinstance(safe_math(inp), str), f"Failed for: {inp!r}"


class TestSafeMathEdgeCases:
    """Edge cases and unusual inputs."""

    def test_whitespace_around_expression(self) -> None:
        assert safe_math("  2 + 3  ") == "5"

    def test_zero(self) -> None:
        assert safe_math("0") == "0"

    def test_negative_zero(self) -> None:
        result = float(safe_math("-0"))
        assert result == 0.0

    def test_very_large_power(self) -> None:
        """Large exponentials should still evaluate (Python handles big ints)."""
        result = safe_math("2 ** 100")
        assert result == str(2**100)

    def test_float_precision(self) -> None:
        """Standard float arithmetic precision."""
        result = safe_math("0.1 + 0.2")
        assert float(result) == 0.1 + 0.2

    def test_integer_division_gives_float(self) -> None:
        """Python true division should return float."""
        assert safe_math("7 / 2") == "3.5"
