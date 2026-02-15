"""pb_memory — Persistent key-value memory store for Agents."""

import json
from pathlib import Path
from typing import Any

from protocolbox.server import mcp

# Memory file location: ~/.protocolbox/memory.json
_MEMORY_DIR = Path.home() / ".protocolbox"
_MEMORY_FILE = _MEMORY_DIR / "memory.json"


def _load_memory() -> dict[str, Any]:
    """Load the memory store from disk.

    Returns:
        The memory dictionary, or an empty dict if the file doesn't exist.
    """
    if not _MEMORY_FILE.exists():
        return {}
    try:
        return json.loads(_MEMORY_FILE.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except (json.JSONDecodeError, OSError):
        return {}


def _save_memory(data: dict[str, Any]) -> None:
    """Save the memory store to disk.

    Creates the parent directory if it doesn't exist.

    Args:
        data: The memory dictionary to persist.
    """
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    _MEMORY_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


@mcp.tool()
def remember(key: str, value: str) -> str:
    """Store a key-value pair in persistent memory.

    Data is saved to ~/.protocolbox/memory.json and persists across
    sessions.

    Args:
        key: The identifier for the stored value.
        value: The data to store.

    Returns:
        A confirmation message.
    """
    try:
        data = _load_memory()
        data[key] = value
        _save_memory(data)
        return f"Remembered: '{key}' has been saved."
    except OSError as e:
        return f"Error: Could not save memory. {type(e).__name__}: {e}"


@mcp.tool()
def recall(key: str) -> str:
    """Retrieve a value from persistent memory by key.

    Args:
        key: The identifier to look up.

    Returns:
        The stored value, or a "not found" message.
    """
    try:
        data = _load_memory()
        if key in data:
            return str(data[key])
        return f"Memory not found: No value stored for key '{key}'."
    except OSError as e:
        return f"Error: Could not read memory. {type(e).__name__}: {e}"
