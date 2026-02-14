"""ProtocolBox CLI — auto-setup for AI Agent environments."""

import os
from pathlib import Path

import typer

app = typer.Typer(
    name="protocolbox",
    help="ProtocolBox — The Standard Library for the Agentic Web.",
    no_args_is_help=True,
)

SKILL_TEMPLATE = """---
name: protocolbox
description: >
  Standard Library of verified tools for AI Agents.
  Tools: scrape(url), heal_json(str), generate_invoice(dict).
---

# ProtocolBox

## Installation

```bash
pip install protocolbox
```

## Usage

Start the MCP server:

```bash
protocolbox start
```

Or with uv:

```bash
uv run protocolbox start
```

## Available Tools

- **scrape(url: str) -> str** — Fetch a web page and return clean Markdown.
- **heal_json(broken_json: str) -> dict** — Fix malformed JSON from LLM output.
- **generate_invoice(data: dict) -> str** — Generate a PDF invoice.
  Requires `client_name` and `total` in data.
"""


def _detect_antigravity() -> Path | None:
    """Detect if running in an Antigravity environment.

    Returns the config directory path if detected, None otherwise.
    """
    # Check environment variable first
    antigravity_home = os.environ.get("ANTIGRAVITY_HOME")
    if antigravity_home:
        return Path(antigravity_home)

    # Check for ~/.antigravity directory
    antigravity_dir = Path.home() / ".antigravity"
    if antigravity_dir.exists():
        return antigravity_dir

    return None


def _write_skill_file(target_dir: Path) -> Path:
    """Write the SKILL.md file to the target directory.

    Returns the path to the created file.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    skill_path = target_dir / "SKILL.md"
    skill_path.write_text(SKILL_TEMPLATE.strip() + "\n")
    return skill_path


@app.command()
def init() -> None:
    """Initialize ProtocolBox for your AI Agent environment."""
    typer.echo("🔧 ProtocolBox Init")
    typer.echo("=" * 40)

    antigravity_dir = _detect_antigravity()

    if antigravity_dir:
        typer.echo(f"✅ Antigravity environment detected: {antigravity_dir}")
        skill_path = _write_skill_file(antigravity_dir / "skills" / "protocolbox")
        typer.echo(f"📄 SKILL.md written to: {skill_path}")
    else:
        typer.echo("ℹ️  No Antigravity environment detected.")
        # Write to current directory as fallback
        skill_path = _write_skill_file(Path.cwd() / ".protocolbox")
        typer.echo(f"📄 SKILL.md written to: {skill_path}")

    typer.echo()
    typer.echo("🚀 Ready! Start the server with:")
    typer.echo("   protocolbox start")


@app.command()
def start() -> None:
    """Start the ProtocolBox MCP server."""
    typer.echo("🚀 Starting ProtocolBox MCP Server...", err=True)
    from protocolbox.server import main

    main()


if __name__ == "__main__":
    app()
