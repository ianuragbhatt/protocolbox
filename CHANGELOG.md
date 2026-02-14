# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-14

### Added
- **MCP Server**: FastMCP-based server implementation.
- **Tools**:
  - `scrape(url)`: Fetch web pages and return clean Markdown.
  - `heal_json(broken_json)`: Repair malformed JSON output from LLMs.
  - `generate_invoice(data)`: Create PDF invoices from structured data.
- **CLI**: `protocolbox init` and `protocolbox start` commands.
- **Documentation**:
  - `README.md` with badges and quick start.
  - `docs/llms.txt` for AI agent consumption.
  - `docs/index.html` landing page.
  - `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- **Testing**: Comprehensive test suite with 110+ tests.
