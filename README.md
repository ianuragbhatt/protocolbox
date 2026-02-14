# ProtocolBox 📦

[![PyPI Version](https://img.shields.io/pypi/v/protocolbox?style=for-the-badge&color=blue)](https://pypi.org/project/protocolbox/)
[![Python Version](https://img.shields.io/pypi/pyversions/protocolbox?style=for-the-badge&color=blue)](https://pypi.org/project/protocolbox/)
[![Downloads](https://img.shields.io/pypi/dm/protocolbox?style=for-the-badge&color=blue)](https://pypi.org/project/protocolbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[![Build Status](https://img.shields.io/github/actions/workflow/status/ianuragbhatt/protocolbox/ci.yml?branch=master&style=for-the-badge)](https://github.com/ianuragbhatt/protocolbox/actions)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![MCP Compliant](https://img.shields.io/badge/MCP-Compliant-orange?style=for-the-badge)](https://modelcontextprotocol.io/)
[![Built for Antigravity](https://img.shields.io/badge/Built%20for-Antigravity-purple?style=for-the-badge)](https://protocolbox.in)

> **The Standard Library for the Agentic Web.**  
> https://protocolbox.in

ProtocolBox is a collection of high-reliability **[MCP (Model Context Protocol)](https://modelcontextprotocol.io/)** tools designed for AI Agents. It provides verified, token-efficient utilities that work out-of-the-box with Claude, Gemini, and other MCP-compliant agents.

## 🚀 Installation

```bash
pip install protocolbox
```

Initialize the configuration for your agent:

```bash
protocolbox init
```

## 🛠️ Tools

ProtocolBox currently exports 3 core tools optimized for agent workflows:

| Tool | Signature | Description |
| :--- | :--- | :--- |
| **Scrape** | `scrape(url: str) -> str` | Fetches a webpage and converts it to clean, token-saving Markdown. Removes ads, scripts, and clutter automatically. |
| **Heal JSON** | `heal_json(json_str: str) -> dict` | repairs malformed JSON strings often produced by LLMs (trailing commas, missing quotes, etc.) into valid Python dictionaries. |
| **Invoice** | `generate_invoice(data: dict) -> str` | Generates a professional PDF invoice from structured data in milliseconds. |

## ⚡ Usage

Start the MCP server to expose these tools to your agent:

```bash
protocolbox start
```

Or using `uv`:

```bash
uv run protocolbox start
```

## 📦 Project Structure

```text
protocolbox/
├── src/protocolbox/      # Core package
│   ├── server.py         # FastMCP server
│   ├── cli.py            # CLI entry point
│   └── tools/            # Tool implementations
├── tests/                # 115+ edge-case tests
├── docs/                 # Documentation site
└── pyproject.toml        # Project config
```

## 👨‍💻 Development

We recommend [uv](https://docs.astral.sh/uv/) for a fast, reliable dev environment.

```bash
# Clone and setup
git clone https://github.com/ianuragbhatt/protocolbox.git
cd protocolbox
uv pip install -e ".[dev]"

# Run tests (100% pass rate required)
pytest tests/ -v

# Linting
ruff check .
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to add new tools.

**Maintainer:** [Anurag Bhatt (@ianuragbhatt)](https://github.com/ianuragbhatt)

## License

MIT © 2026 ProtocolBox.
