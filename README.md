# ProtocolBox 📦

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

ProtocolBox currently exports 8 tools optimized for agent workflows:

| Tool | Signature | Description |
| :--- | :--- | :--- |
| **Scrape** | `scrape(url: str) -> str` | Fetches a webpage and converts it to clean, token-saving Markdown. Removes ads, scripts, and clutter automatically. |
| **Heal JSON** | `heal_json(json_str: str) -> dict` | Repairs malformed JSON strings often produced by LLMs (trailing commas, missing quotes, etc.) into valid Python dictionaries. |
| **Web Search** | `web_search(query: str, max_results: int) -> str` | Privacy-focused web search using DuckDuckGo. Returns formatted Markdown results. |
| **Safe Math** | `safe_math(expression: str) -> str` | Securely evaluates mathematical expressions without `eval()`. Supports arithmetic and common math functions. |
| **Get Time** | `get_time(timezone: str) -> str` | Returns the current real-world time in any timezone (ISO 8601 format). |
| **Get Transcript** | `get_transcript(video_url: str) -> str` | Fetches the English transcript of a YouTube video as clean text. |
| **Remember** | `remember(key: str, value: str) -> str` | Stores a key-value pair in persistent local memory. |
| **Recall** | `recall(key: str) -> str` | Retrieves a value from persistent local memory by key. |

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
│       ├── scraper.py    # scrape()
│       ├── json_healer.py# heal_json()
│       ├── search.py     # web_search()
│       ├── math_utils.py # safe_math()
│       ├── time_utils.py # get_time()
│       ├── youtube.py    # get_transcript()
│       └── memory.py     # remember() + recall()
├── tests/                # 280+ edge-case tests
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
