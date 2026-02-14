# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
  - `generate_invoice(data)`: 
    - Generates professional PDF invoices from structured Python dictionaries.
    - Supports line items, tax calculations, and custom notes.

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
- Sandboxed PDF generation.
