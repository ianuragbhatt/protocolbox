"""pb_heal_json — Fix malformed JSON from LLM output."""

import json
from typing import Any

import json_repair

from protocolbox.server import mcp


@mcp.tool()
def heal_json(broken_json: str) -> dict[str, Any]:
    """Attempt to repair malformed JSON and return a valid Python dict.

    Handles common LLM output issues: trailing commas, unquoted keys,
    single quotes, truncated output, and more.

    Args:
        broken_json: A string containing malformed or broken JSON.

    Returns:
        A valid Python dictionary parsed from the repaired JSON,
        or an error dict if repair is impossible.
    """
    try:
        repaired = json_repair.repair_json(broken_json, return_objects=False)

        if not isinstance(repaired, str):
            repaired = str(repaired)

        result = json.loads(repaired)

        # Ensure we always return a dict.
        if isinstance(result, dict):
            return result
        elif isinstance(result, list):
            return {"data": result}
        else:
            return {"value": result}

    except (json.JSONDecodeError, TypeError, ValueError):
        snippet = broken_json[:100] + ("..." if len(broken_json) > 100 else "")
        return {"error": "Failed", "input_snippet": snippet}
