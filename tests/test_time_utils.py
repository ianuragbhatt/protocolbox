"""Tests for the pb_get_time tool — comprehensive timezone edge-case coverage."""

import re
from unittest.mock import patch

from protocolbox.tools.time_utils import get_time


class TestGetTimeBasic:
    """Basic happy-path time tests."""

    def test_default_timezone_is_utc(self) -> None:
        """Default call should return UTC time."""
        result = get_time()
        assert "UTC" in result

    def test_utc_format_matches_iso8601(self) -> None:
        """Output should match YYYY-MM-DD HH:MM:SS TZ pattern."""
        result = get_time("UTC")
        pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w+"
        assert re.match(pattern, result), f"Format mismatch: {result}"

    def test_return_type_is_string(self) -> None:
        assert isinstance(get_time(), str)

    def test_return_is_not_empty(self) -> None:
        assert len(get_time()) > 10


class TestGetTimeValidTimezones:
    """Test various valid timezone strings."""

    def test_us_eastern(self) -> None:
        result = get_time("US/Eastern")
        assert "E" in result  # EST or EDT

    def test_us_pacific(self) -> None:
        result = get_time("US/Pacific")
        assert "P" in result  # PST or PDT

    def test_us_central(self) -> None:
        result = get_time("US/Central")
        assert "C" in result  # CST or CDT

    def test_europe_london(self) -> None:
        result = get_time("Europe/London")
        assert isinstance(result, str)
        assert len(result) > 10

    def test_europe_berlin(self) -> None:
        result = get_time("Europe/Berlin")
        assert isinstance(result, str)

    def test_asia_kolkata(self) -> None:
        result = get_time("Asia/Kolkata")
        assert "IST" in result

    def test_asia_tokyo(self) -> None:
        result = get_time("Asia/Tokyo")
        assert "JST" in result

    def test_australia_sydney(self) -> None:
        result = get_time("Australia/Sydney")
        assert isinstance(result, str)

    def test_utc_explicit(self) -> None:
        result = get_time("UTC")
        assert "UTC" in result


class TestGetTimeInvalidTimezones:
    """Invalid timezone handling."""

    def test_invalid_timezone_returns_error(self) -> None:
        result = get_time("Invalid/Timezone")
        assert "Error" in result
        assert "Unknown timezone" in result

    def test_invalid_timezone_includes_input(self) -> None:
        result = get_time("Mars/Olympus")
        assert "Mars/Olympus" in result

    def test_invalid_timezone_lists_common_timezones(self) -> None:
        """Error should include common timezone suggestions."""
        result = get_time("Nowhere/Place")
        assert "UTC" in result
        assert "US/Eastern" in result
        assert "Asia/Kolkata" in result

    def test_empty_string_timezone(self) -> None:
        """Empty timezone string should return an error."""
        result = get_time("")
        assert "Error" in result

    def test_numeric_timezone(self) -> None:
        """A purely numeric string should return an error."""
        result = get_time("12345")
        assert "Error" in result

    def test_special_characters_timezone(self) -> None:
        """Special characters should return an error."""
        result = get_time("!@#$%")
        assert "Error" in result

    def test_partial_timezone(self) -> None:
        """A partial timezone like 'US' alone should return an error."""
        result = get_time("US")
        assert "Error" in result


class TestGetTimeEdgeCases:
    """Edge cases and unusual inputs."""

    def test_case_sensitivity(self) -> None:
        """A misspelled timezone should fail."""
        result = get_time("Americaa/New_Yorrk")
        assert "Error" in result

    def test_timezone_with_spaces(self) -> None:
        """Timezone with spaces should fail."""
        result = get_time("US / Eastern")
        assert "Error" in result

    def test_gmt_timezone(self) -> None:
        """GMT should be a valid timezone."""
        result = get_time("GMT")
        assert "Error" not in result
        assert "GMT" in result

    @patch("protocolbox.tools.time_utils.datetime")
    def test_midnight_time(self, mock_datetime) -> None:
        """Midnight should format correctly."""
        from datetime import datetime

        import pytz

        utc = pytz.UTC
        fixed_time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=utc)
        mock_datetime.now.return_value = fixed_time
        result = get_time("UTC")
        assert "2026-01-01 00:00:00" in result

    @patch("protocolbox.tools.time_utils.datetime")
    def test_end_of_day_time(self, mock_datetime) -> None:
        """23:59:59 should format correctly."""
        from datetime import datetime

        import pytz

        utc = pytz.UTC
        fixed_time = datetime(2026, 12, 31, 23, 59, 59, tzinfo=utc)
        mock_datetime.now.return_value = fixed_time
        result = get_time("UTC")
        assert "2026-12-31 23:59:59" in result

    def test_all_common_timezones_are_valid(self) -> None:
        """Every timezone listed in the error message should be valid."""
        from protocolbox.tools.time_utils import _COMMON_TIMEZONES

        for tz in _COMMON_TIMEZONES:
            result = get_time(tz)
            assert "Error" not in result, f"Common timezone '{tz}' failed"

    def test_error_return_type_is_string(self) -> None:
        """Even on error, return type should be str."""
        result = get_time("Fake/Zone")
        assert isinstance(result, str)
