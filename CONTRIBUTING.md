# Contributing to ProtocolBox

Thank you for your interest in contributing to ProtocolBox! We welcome contributions from everyone.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding a New Tool](#adding-a-new-tool)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/ianuragbhatt/protocolbox.git
   cd protocolbox
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

ProtocolBox requires **Python 3.11+**. We recommend using [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or with uv
uv pip install -e ".[dev]"
```

Verify your setup:

```bash
pytest tests/ -v      # All tests should pass
ruff check .          # No lint errors
```

## Project Structure

```
protocolbox/
├── src/protocolbox/
│   ├── __init__.py          # Package version
│   ├── server.py            # FastMCP server engine
│   ├── cli.py               # CLI (init + start commands)
│   └── tools/
│       ├── __init__.py      # Tool exports
│       ├── utils.py         # Shared utilities (HTTP client)
│       ├── scraper.py       # scrape() tool
│       ├── json_healer.py   # heal_json() tool
│       └── invoice.py       # generate_invoice() tool
├── tests/                   # Test suite (mirrors tool structure)
├── docs/                    # Documentation & landing page
├── pyproject.toml           # Project config
├── CONTRIBUTING.md          # ← You are here
└── CODE_OF_CONDUCT.md
```

## Adding a New Tool

ProtocolBox is designed to make adding new tools straightforward:

### 1. Create the tool file

Create `src/protocolbox/tools/your_tool.py`:

```python
"""Description of your tool."""

from protocolbox.server import mcp


@mcp.tool()
def your_tool_name(param: str) -> str:
    """Clear docstring describing what the tool does.

    Args:
        param: Description of the parameter.

    Returns:
        Description of the return value.
    """
    # Your implementation here
    return result
```

### 2. Register the tool

Add the import to `src/protocolbox/server.py`:

```python
import protocolbox.tools.your_tool  # noqa: F401, E402
```

And export it from `src/protocolbox/tools/__init__.py`.

### 3. Write tests

Create `tests/test_your_tool.py` with:
- Happy-path tests
- Edge cases (empty input, unicode, very large input)
- Error handling tests

### 4. Update documentation

- Add the tool to `docs/llms.txt`
- Add a card to `docs/index.html`
- Update the `README.md` tool table

## Code Standards

We enforce consistent code quality with **Ruff**:

| Rule | Setting |
|------|---------|
| Line length | 88 characters |
| Target version | Python 3.11 |
| Lint rules | `E` (pycodestyle), `F` (pyflakes), `I` (isort) |
| Type hints | **Mandatory** on all public functions |

### Before submitting

```bash
# Fix auto-fixable issues
ruff check . --fix

# Verify clean
ruff check .
```

### Style guidelines

- **Type hints are mandatory** on all function signatures.
- **Docstrings** are required on all public functions (Google style).
- **Error handling**: Tools should return error strings/dicts, not raise exceptions.
- **No print statements**: Use `typer.echo()` in CLI code only.

## Testing

We use **pytest** for testing. Our test suite aims for comprehensive edge-case coverage.

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_scraper.py -v

# Run with coverage (install pytest-cov first)
pytest tests/ --cov=protocolbox --cov-report=term-missing
```

### Test expectations

- **Every tool must have tests** covering:
  - Normal/happy path
  - Edge cases (empty, unicode, very large, special characters)
  - Error handling (invalid input, network errors)
- **Mock external calls** (HTTP, filesystem) — never make real network requests in tests.
- **Clean up** generated files (e.g., PDFs in `/tmp/`).

## Pull Request Process

1. **Ensure all tests pass** and **ruff is clean**.
2. **Write clear commit messages** following conventional commits:
   - `feat: add new_tool for X`
   - `fix: handle edge case in scraper`
   - `docs: update README with new tool`
   - `test: add edge cases for json_healer`
3. **Open a PR** against `main` with:
   - A description of what changed and why.
   - Link to any related issue.
4. **Address review feedback** promptly.

### PR checklist

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Lint is clean (`ruff check .`)
- [ ] New tools have comprehensive tests
- [ ] Documentation is updated (README, llms.txt)
- [ ] Commit messages follow conventional format

## Reporting Issues

Use the [GitHub issue templates](.github/ISSUE_TEMPLATE/) to report:

- **Bugs**: Include reproduction steps, expected vs actual behavior, and your environment.
- **Feature requests**: Describe the tool or improvement and the use case.

## Questions?

Open a [discussion](https://github.com/ianuragbhatt/protocolbox/discussions) or reach out to the maintainers.

---

Thank you for helping build the Standard Library for the Agentic Web! 🚀
