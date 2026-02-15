"""pb_get_time — Real-world time with timezone support."""

from datetime import datetime

import pytz

from protocolbox.server import mcp

# Common timezones shown in error messages.
_COMMON_TIMEZONES = [
    "UTC",
    "US/Eastern",
    "US/Central",
    "US/Pacific",
    "Europe/London",
    "Europe/Berlin",
    "Asia/Kolkata",
    "Asia/Tokyo",
    "Australia/Sydney",
]


@mcp.tool()
def get_time(timezone: str = "UTC") -> str:
    """Get the current real-world time in a specified timezone.

    Returns the time in ISO 8601 format (YYYY-MM-DD HH:MM:SS TZ).

    Args:
        timezone: A valid timezone string (default "UTC").
                  Examples: "US/Eastern", "Asia/Kolkata", "Europe/London".

    Returns:
        The current time as a formatted string, or an error message
        with a list of common timezones if the input is invalid.
    """
    try:
        tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        tz_list = ", ".join(_COMMON_TIMEZONES)
        return (
            f"Error: Unknown timezone '{timezone}'. "
            f"Common timezones: {tz_list}."
        )

    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")
