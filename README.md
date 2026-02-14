# ProtocolBox 📦

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Ruff](https://img.shields.io/badge/linting-ruff-orange.svg)](https://docs.astral.sh/ruff/)
[![MCP](https://img.shields.io/badge/protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)

> **The Standard Library for the Agentic Web.**

ProtocolBox is an open-source collection of high-reliability [MCP](https://modelcontextprotocol.io/) tools that any AI Agent — Claude, Gemini, Antigravity — can install and use immediately.

## Quick Start

```bash
pip install protocolbox
protocolbox init
protocolbox start
```

## Available Tools

| Tool | Category | Description |
|------|----------|-------------|
| `scrape(url)` | Token Saver | Fetch any web page and return clean Markdown. Strips scripts, styles, and footers. |
| `heal_json(broken_json)` | Reliability | Fix malformed JSON output from LLMs. Handles trailing commas, unquoted keys, truncated output. |
| `generate_invoice(data)` | Business Output | Generate a professional PDF invoice from structured data. |

## How It Works

```
Agent  →  MCP Protocol  →  ProtocolBox Server  →  Tool (scrape / heal / invoice)
```

ProtocolBox exposes an MCP server that AI agents connect to. Each tool is a verified, type-checked function with robust error handling.

## Development

### Prerequisites

- **Python 3.11+**
- [**uv**](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone the repo
git clone https://github.com/ianuragbhatt/protocolbox.git
cd protocolbox

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# All tests (115 tests with edge-case coverage)
pytest tests/ -v

# Specific tool
pytest tests/test_scraper.py -v
```

### Linting

```bash
ruff check .          # Check
ruff check . --fix    # Auto-fix
```

## Contributing

We welcome contributions! See our **[Contributing Guide](CONTRIBUTING.md)** for:

- Development setup instructions
- How to add a new tool (step-by-step)
- Code standards and testing requirements
- Pull request process

Please also read our **[Code of Conduct](CODE_OF_CONDUCT.md)**.

### Quick contribution checklist

1. Fork → Clone → Branch
2. Make your changes
3. `pytest tests/ -v` — all tests pass
4. `ruff check .` — no lint errors
5. Open a PR

## Project Structure

```
protocolbox/
├── src/protocolbox/
│   ├── server.py           # FastMCP server engine
│   ├── cli.py              # CLI (init + start)
│   └── tools/
│       ├── scraper.py      # scrape() tool
│       ├── json_healer.py  # heal_json() tool
│       └── invoice.py      # generate_invoice() tool
├── tests/                  # 115 tests with edge-case coverage
├── docs/                   # Landing page + llms.txt
├── .github/                # Issue & PR templates
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── pyproject.toml
```

## Documentation

- **[llms.txt](docs/llms.txt)** — Agent-readable tool manual
- **[Landing Page](docs/index.html)** — Human-readable project page

## Maintainer

**Anurag Bhatt** — [@anuragbhatt](https://github.com/anuragbhatt)

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built for the Agentic Web 🚀*
