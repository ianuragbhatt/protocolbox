"""Tests for the pb_invoice tool."""

import os

from protocolbox.tools.invoice import generate_invoice


class TestGenerateInvoice:
    """Test the generate_invoice tool."""

    def test_basic_invoice(self) -> None:
        """A valid invoice should generate a PDF and return its path."""
        result = generate_invoice({
            "client_name": "Acme Corp",
            "total": 1500.00,
        })
        assert result.startswith("/tmp/invoice_")
        assert result.endswith(".pdf")
        assert os.path.exists(result)

        # Cleanup
        os.remove(result)

    def test_invoice_with_items(self) -> None:
        """An invoice with line items should generate a PDF."""
        result = generate_invoice({
            "client_name": "Widgets Inc",
            "total": 300.00,
            "items": [
                {"description": "Widget A", "qty": 2, "price": 100.00},
                {"description": "Widget B", "qty": 1, "price": 100.00},
            ],
        })
        assert os.path.exists(result)
        os.remove(result)

    def test_invoice_with_all_fields(self) -> None:
        """An invoice with all optional fields should generate a PDF."""
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
        os.remove(result)

    def test_missing_client_name(self) -> None:
        """Missing client_name should return an error."""
        result = generate_invoice({"total": 100})
        assert "Error" in result
        assert "client_name" in result

    def test_missing_total(self) -> None:
        """Missing total should return an error."""
        result = generate_invoice({"client_name": "Test"})
        assert "Error" in result
        assert "total" in result

    def test_invalid_total(self) -> None:
        """Non-numeric total should return an error."""
        result = generate_invoice({
            "client_name": "Test",
            "total": "not_a_number",
        })
        assert "Error" in result

    def test_empty_data(self) -> None:
        """Empty dict should return an error."""
        result = generate_invoice({})
        assert "Error" in result

    def test_pdf_file_is_not_empty(self) -> None:
        """The generated PDF should have content (non-zero size)."""
        result = generate_invoice({
            "client_name": "Size Test",
            "total": 42.00,
        })
        assert os.path.getsize(result) > 0
        os.remove(result)
