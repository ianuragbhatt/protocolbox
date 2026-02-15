# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-02-15

### Added
- **Web Search** (`web_search`): Privacy-focused web search using DuckDuckGo with Markdown-formatted results.
- **Safe Math** (`safe_math`): Secure mathematical expression evaluator using `ast.parse` (no `eval()`). Supports arithmetic and `math` functions.
- **Get Time** (`get_time`): Real-world time retrieval for any timezone using `pytz`, returns ISO 8601 format.
- **Get Transcript** (`get_transcript`): YouTube video transcript fetcher via `youtube-transcript-api`.
- **Memory** (`remember` / `recall`): Persistent local key-value store using `~/.protocolbox/memory.json`.
- **Tests**: 184 new edge-case tests (283 total) covering all new tools — security, error handling, unicode, and boundary conditions.

### Fixed
- **YouTube Tool**: Migrated to `youtube-transcript-api` v1.x instance-based API (`api.fetch()` instead of removed `get_transcript()` class method).

### Dependencies
- Added `duckduckgo-search`, `youtube-transcript-api`, and `pytz`.

## [0.1.3] - 2026-02-15

### Removed
- **Invoice Tool**: Removed `generate_invoice()` tool and all related code, tests, and documentation.
- **Dependency**: Removed `reportlab` from project dependencies (was only used by the invoice tool).

## [0.1.2] - 2026-02-14

### Fixed
- **CLI**: Silenced "🚀 Starting ProtocolBox..." startup message to stderr to prevent JSON-RPC corruption in MCP clients.

## [0.1.1] - 2026-02-14
- *Skipped due to missing version bump.*

## [0.1.0] - 2026-02-14

**Initial Public Release** 🚀

ProtocolBox v0.1.0 establishes the "Standard Library for the Agentic Web," providing high-reliability MCP tools for AI agents. This release focuses on stability, token efficiency, and developer experience.

### ✨ Features

- **MCP Server Implementation**
  - Fast, async-native server built on the Model Context Protocol.
  - Robust error handling and type validation for all tools.
  - Zero-config deployment for local usage.

- **Core Tools**
  - `scrape(url)`: 
    - Fetches web pages and returns clean, token-optimized Markdown.
    - Automatically strips scripts, styles, ads, and footers.
    - Handles redirects, timeouts, and encoding issues gracefully.
  - `heal_json(broken_json)`: 
    - deterministic recovery of malformed JSON from LLM outputs.
    - Fixes trailing commas, missing quotes, unclosed brackets, and truncated strings.

- **Developer Experience**
  - **CLI**: `protocolbox init` for environment setup and `protocolbox start` for running the server.
  - **Type Hints**: 100% type coverage for better Agentic reasoning.
  - **Testing**: Comprehensive test suite (112 tests) ensuring reliability across edge cases.

### 📚 Documentation

- **Landing Page**: [protocolbox.in](https://protocolbox.in) — Modern, dark-themed documentation site.
- **Agent Manual**: `docs/llms.txt` optimized for machine reading.
- **Governance**: Added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`.

### ⚙️ Infrastructure

- **CI/CD**:
  - Automated testing on Python 3.11/3.12 via GitHub Actions.
  - Strict linting (`Ruff`) and formatting enforcement.
  - Automatic deployment of documentation to GitHub Pages.
  - Automated PyPI publishing workflow on Release.

### 🛡️ Security

- All dependencies pinned via `uv.lock`.
- No external API key requirements for core tools.
