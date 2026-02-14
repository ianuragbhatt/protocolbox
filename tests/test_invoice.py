"""Tests for the pb_invoice tool — comprehensive edge-case coverage."""

import os

from protocolbox.tools.invoice import generate_invoice


def _cleanup(path: str) -> None:
    """Remove a generated file if it exists."""
    if os.path.exists(path):
        os.remove(path)


class TestInvoiceBasic:
    """Core happy-path invoice generation tests."""

    def test_basic_invoice(self) -> None:
        """Minimal valid invoice generates a PDF."""
        result = generate_invoice({
            "client_name": "Acme Corp",
            "total": 1500.00,
        })
        assert result.startswith("/tmp/invoice_")
        assert result.endswith(".pdf")
        assert os.path.exists(result)
        _cleanup(result)

    def test_invoice_with_items(self) -> None:
        """Invoice with line items generates a PDF."""
        result = generate_invoice({
            "client_name": "Widgets Inc",
            "total": 300.00,
            "items": [
                {"description": "Widget A", "qty": 2, "price": 100},
                {"description": "Widget B", "qty": 1, "price": 100},
            ],
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_invoice_with_all_fields(self) -> None:
        """All optional fields should generate a PDF."""
        result = generate_invoice({
            "client_name": "Full Corp",
            "total": 999.99,
            "invoice_number": "INV-CUSTOM-001",
            "currency": "€",
            "items": [
                {"description": "Service", "qty": 1, "price": 999.99},
            ],
            "notes": "Payment due within 30 days.",
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_pdf_file_is_not_empty(self) -> None:
        """Generated PDF should have content (non-zero size)."""
        result = generate_invoice({
            "client_name": "Size Test",
            "total": 42.00,
        })
        assert os.path.getsize(result) > 0
        _cleanup(result)

    def test_each_call_produces_unique_file(self) -> None:
        """Two calls should produce different file paths."""
        r1 = generate_invoice({
            "client_name": "A", "total": 1
        })
        r2 = generate_invoice({
            "client_name": "B", "total": 2
        })
        assert r1 != r2
        assert os.path.exists(r1)
        assert os.path.exists(r2)
        _cleanup(r1)
        _cleanup(r2)


class TestInvoiceValidation:
    """Input validation and error handling."""

    def test_missing_client_name(self) -> None:
        result = generate_invoice({"total": 100})
        assert "Error" in result
        assert "client_name" in result

    def test_missing_total(self) -> None:
        result = generate_invoice({"client_name": "Test"})
        assert "Error" in result
        assert "total" in result

    def test_empty_data(self) -> None:
        result = generate_invoice({})
        assert "Error" in result

    def test_invalid_total_string(self) -> None:
        """Non-numeric total string should return error."""
        result = generate_invoice({
            "client_name": "Test",
            "total": "not_a_number",
        })
        assert "Error" in result

    def test_invalid_total_none(self) -> None:
        """None total should trigger missing-total error."""
        result = generate_invoice({
            "client_name": "Test",
            "total": None,
        })
        assert "Error" in result

    def test_empty_client_name(self) -> None:
        """Empty string client name should return error."""
        result = generate_invoice({
            "client_name": "",
            "total": 100,
        })
        assert "Error" in result

    def test_error_returns_string_not_path(self) -> None:
        """Errors should be plain strings, not file paths."""
        result = generate_invoice({})
        assert not result.startswith("/tmp/")


class TestInvoiceEdgeCases:
    """Unusual and boundary condition inputs."""

    def test_zero_total(self) -> None:
        """Zero total should generate a valid PDF."""
        result = generate_invoice({
            "client_name": "Zero Corp",
            "total": 0,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_negative_total(self) -> None:
        """Negative total (credit note) should generate a PDF."""
        result = generate_invoice({
            "client_name": "Credit Corp",
            "total": -150.00,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_very_large_total(self) -> None:
        """Very large total should not crash."""
        result = generate_invoice({
            "client_name": "Big Corp",
            "total": 999_999_999.99,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_integer_total(self) -> None:
        """Integer total should work (not just float)."""
        result = generate_invoice({
            "client_name": "Int Corp",
            "total": 500,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_string_numeric_total(self) -> None:
        """String that looks like a number should work."""
        result = generate_invoice({
            "client_name": "Str Corp",
            "total": "250.50",
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_unicode_client_name(self) -> None:
        """Unicode client name should not crash."""
        result = generate_invoice({
            "client_name": "株式会社テスト",
            "total": 100,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_special_chars_in_client_name(self) -> None:
        """Special characters in client name."""
        result = generate_invoice({
            "client_name": "O'Brien & Sons <LLC>",
            "total": 200,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_very_long_client_name(self) -> None:
        """Very long client name should not crash."""
        result = generate_invoice({
            "client_name": "A" * 500,
            "total": 100,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_many_line_items(self) -> None:
        """A large number of line items should not crash."""
        items = [
            {"description": f"Item {i}", "qty": 1, "price": 10.0}
            for i in range(100)
        ]
        result = generate_invoice({
            "client_name": "Bulk Corp",
            "total": 1000.0,
            "items": items,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_empty_items_list(self) -> None:
        """Empty items list should generate a valid PDF."""
        result = generate_invoice({
            "client_name": "Empty Items",
            "total": 50,
            "items": [],
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_items_with_missing_fields(self) -> None:
        """Items missing optional fields should use defaults."""
        result = generate_invoice({
            "client_name": "Sparse Corp",
            "total": 100,
            "items": [
                {"description": "Partial item"},
                {},
            ],
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_custom_currency_symbols(self) -> None:
        """Various currency symbols should work."""
        for symbol in ["$", "€", "£", "¥", "₹", "₿"]:
            result = generate_invoice({
                "client_name": "Currency Test",
                "total": 100,
                "currency": symbol,
            })
            assert os.path.exists(result)
            _cleanup(result)

    def test_long_notes(self) -> None:
        """Very long notes text should not crash."""
        result = generate_invoice({
            "client_name": "Notes Corp",
            "total": 100,
            "notes": "This is a note. " * 100,
        })
        assert os.path.exists(result)
        _cleanup(result)

    def test_extra_unknown_fields_ignored(self) -> None:
        """Unknown fields in data should be silently ignored."""
        result = generate_invoice({
            "client_name": "Extra Corp",
            "total": 100,
            "foo": "bar",
            "nested": {"deep": True},
        })
        assert os.path.exists(result)
        _cleanup(result)
