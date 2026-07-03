"""
SIBI Dashboard — Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~

Utility functions shared across all modules.
Each function is intentionally small, pure, and well-typed
so it can be reused without side effects.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta
from rich.console import Console

_console = Console()


# ═══════════════════════════════════════════════════════════════════
#  Formatting
# ═══════════════════════════════════════════════════════════════════


def format_bytes(num_bytes: float, precision: int = 1) -> str:
    """Convert *num_bytes* to a human-readable string.

    Examples::

        >>> format_bytes(3_221_225_472)
        '3.0 GiB'
    """
    units: list[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    for unit in units:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.{precision}f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.{precision}f} EiB"


def format_uptime(seconds: float) -> str:
    """Format *seconds* into a human-readable uptime string.

    Examples::

        >>> format_uptime(90061)
        '1d 1h 1m'
    """
    delta = timedelta(seconds=int(seconds))
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    parts: list[str] = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def format_timestamp(
    timestamp: float,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """Format a UNIX *timestamp* into a human-readable date/time string."""
    return datetime.fromtimestamp(timestamp).strftime(fmt)


# ═══════════════════════════════════════════════════════════════════
#  Shell Helpers
# ═══════════════════════════════════════════════════════════════════


def safe_command(
    cmd: list[str],
    timeout: float = 5.0,
    default: str = "N/A",
) -> str:
    """Run a shell command safely and return its stripped stdout.

    Returns *default* on any error (timeout, missing binary, etc.).
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        return output if output else default
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return default


# ═══════════════════════════════════════════════════════════════════
#  Terminal
# ═══════════════════════════════════════════════════════════════════


def get_terminal_width() -> int:
    """Return the current terminal width in columns."""
    return _console.size.width


def get_terminal_height() -> int:
    """Return the current terminal height in rows."""
    return _console.size.height


# ═══════════════════════════════════════════════════════════════════
#  String Utilities
# ═══════════════════════════════════════════════════════════════════


def truncate(text: str, max_length: int = 40) -> str:
    """Truncate *text* to *max_length* characters, adding ``...`` if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


# ═══════════════════════════════════════════════════════════════════
#  Math
# ═══════════════════════════════════════════════════════════════════


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Clamp *value* between *lo* and *hi*."""
    return max(lo, min(hi, value))


# ═══════════════════════════════════════════════════════════════════
#  Environment
# ═══════════════════════════════════════════════════════════════════


def is_wsl() -> bool:
    """Detect if running inside Windows Subsystem for Linux."""
    try:
        with open("/proc/version", "r", encoding="utf-8") as fh:
            return "microsoft" in fh.read().lower()
    except FileNotFoundError:
        return False


def env_or(key: str, default: str = "N/A") -> str:
    """Return the value of environment variable *key*, or *default*."""
    return os.environ.get(key, default)
