"""Custom pytest plugin for clean, organized test output."""

import os
from collections import defaultdict

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Module-level storage for results
_results: dict = defaultdict(lambda: {"passed": 0, "failed": 0, "errors": []})
_use_color: bool = hasattr(os, "isatty") and os.isatty(1)


def pytest_runtest_logreport(report):
    """Collect results per file during test execution."""
    if report.when != "call":
        return

    file_key = report.nodeid.split("::")[0]

    if report.passed:
        _results[file_key]["passed"] += 1
    elif report.failed:
        _results[file_key]["failed"] += 1
        test_name = report.nodeid.split("::")[-1]
        short_reason = str(report.longrepr).strip().split("\n")[-1]
        _results[file_key]["errors"].append((test_name, short_reason))


def pytest_terminal_summary(terminalreporter):
    """Print a clean, organized summary at the end."""
    if not _results:
        return

    def c(text, color):
        return f"{color}{text}{RESET}" if _use_color else text

    total_passed = 0
    total_failed = 0
    max_name_len = max(
        len(os.path.basename(f).replace("test_", "").replace(".py", ""))
        for f in _results
    )

    terminalreporter.write_line("")
    terminalreporter.write_line(c("  Test Results", BOLD))
    terminalreporter.write_line(c("  " + "─" * 50, DIM))

    for filepath in sorted(_results):
        data = _results[filepath]
        passed = data["passed"]
        failed = data["failed"]
        total = passed + failed
        total_passed += passed
        total_failed += failed

        name = os.path.basename(filepath).replace("test_", "").replace(".py", "")
        name_display = name.ljust(max_name_len)

        if failed == 0:
            status = c("✓ PASS", GREEN)
            count = c(f"{passed}/{total}", GREEN)
        else:
            status = c("✗ FAIL", RED)
            count = c(f"{passed}/{total}", RED)

        terminalreporter.write_line(f"  {status}  {name_display}  {count}")

        for test_name, reason in data["errors"]:
            terminalreporter.write_line(
                f"         {c('└─', DIM)} {c(test_name, YELLOW)}"
            )
            terminalreporter.write_line(f"            {c(reason, RED)}")

    grand_total = total_passed + total_failed
    terminalreporter.write_line(c("  " + "─" * 50, DIM))

    if total_failed == 0:
        terminalreporter.write_line(
            f"  {c('✓', GREEN)} {c(f'{total_passed}/{grand_total} passed', BOLD)}"
        )
    else:
        terminalreporter.write_line(
            f"  {c(f'{total_passed} passed', GREEN)}"
            f" · {c(f'{total_failed} failed', RED)}"
            f" {c(f'({grand_total} total)', DIM)}"
        )
    terminalreporter.write_line("")

    # Clear for next run
    _results.clear()
