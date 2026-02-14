# ProtocolBox 📦

> **The Standard Library for the Agentic Web.**

ProtocolBox is an open-source collection of high-reliability [MCP](https://modelcontextprotocol.io/) tools that any AI Agent — Claude, Gemini, Antigravity — can install and use immediately.

## Quick Start

```bash
pip install protocolbox
protocolbox init
```

## Available Tools

| Tool | Description |
|------|-------------|
| `scrape(url)` | Fetch any web page and return clean Markdown. Token-efficient web reading. |
| `heal_json(broken_json)` | Fix malformed JSON output from LLMs. Never lose a response again. |
| `generate_invoice(data)` | Generate a professional PDF invoice from structured data. |

## Development

```bash
# Clone and install in dev mode
git clone https://github.com/your-org/protocolbox.git
cd protocolbox
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
```

## How It Works

ProtocolBox exposes an MCP server that AI agents connect to. Each tool is a verified, type-checked function with robust error handling.

```
Agent  →  MCP Protocol  →  ProtocolBox Server  →  Tool (scrape / heal / invoice)
```

## License

MIT — see [LICENSE](LICENSE).
