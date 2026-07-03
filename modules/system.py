"""
SIBI Dashboard -- System
~~~~~~~~~~~~~~~~~~~~~~~~

System information collection using :mod:`psutil` and :mod:`platform`.
Gathers hostname, OS, kernel, CPU, memory, disk, uptime, and more.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import platform
import time

import psutil

from modules.helpers import (
    format_bytes,
    format_uptime,
    safe_command,
)
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_NORMAL, TEXT_PRIMARY

from rich.panel import Panel
from rich.table import Table


# -------------------------------------------------------------------
#  Data Collectors
# -------------------------------------------------------------------


def get_hostname() -> str:
    """Return the system hostname."""
    return platform.node()


def get_os_info() -> str:
    """Return a human-readable OS description."""
    if platform.system() == "Linux":
        try:
            import distro  # type: ignore[import-untyped]
            return distro.name(pretty=True)
        except ImportError:
            return safe_command(
                ["lsb_release", "-ds"],
                default=f"Linux {platform.release()}",
            ).strip('"')
    return f"{platform.system()} {platform.release()}"


def get_kernel() -> str:
    """Return the kernel version string."""
    return platform.release()


def get_architecture() -> str:
    """Return the CPU architecture."""
    return platform.machine()


def get_cpu_model() -> str:
    """Return the CPU model name."""
    if platform.system() == "Linux":
        model = safe_command(
            [
                "sh", "-c",
                "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2",
            ],
        )
        stripped = model.strip()
        if stripped and stripped != "N/A":
            return stripped
    proc = platform.processor()
    return proc if proc else "Unknown"


def get_cpu_cores() -> int:
    """Return the number of physical CPU cores."""
    return psutil.cpu_count(logical=False) or 0


def get_memory_info() -> str:
    """Return RAM used / total as a formatted string."""
    mem = psutil.virtual_memory()
    return f"{format_bytes(mem.used)} / {format_bytes(mem.total)} ({mem.percent}%)"


def get_disk_info() -> str:
    """Return disk used / total as a formatted string."""
    usage = psutil.disk_usage("/")
    return f"{format_bytes(usage.used)} / {format_bytes(usage.total)} ({usage.percent}%)"


def get_uptime() -> str:
    """Return the system uptime as a formatted string."""
    return format_uptime(time.time() - psutil.boot_time())


# -------------------------------------------------------------------
#  Panel Builder
# -------------------------------------------------------------------


def _info_rows() -> list[tuple[str, str]]:
    """Collect all system info key-value pairs."""
    return [
        ("\U0001f5a5  Hostname", get_hostname()),
        ("\U0001f4bf  OS", get_os_info()),
        ("\U0001f527  Kernel", get_kernel()),
        ("\U0001f4d0  Arch", get_architecture()),
        ("\u26a1  CPU", get_cpu_model()),
        ("\U0001f9ee  Cores", str(get_cpu_cores())),
        ("\U0001f9e0  RAM", get_memory_info()),
        ("\U0001f4be  Storage", get_disk_info()),
        ("\u23f1  Uptime", get_uptime()),
    ]


def build_system_panel() -> Panel:
    """Build the System Information panel.

    Displays a two-column table of system properties in a
    rounded Rich Panel.
    """
    table = Table(
        show_header=False,
        expand=True,
        box=None,
        padding=(0, 1),
        show_edge=False,
    )
    table.add_column(
        "Label",
        style=f"bold {ACCENT_PURPLE}",
        min_width=14,
        ratio=1,
    )
    table.add_column("Value", style=TEXT_PRIMARY, ratio=2)

    for label, value in _info_rows():
        table.add_row(f"  {label}", value)

    return Panel(
        table,
        title=f"[bold {ACCENT_CYAN}]\u2699  System Info[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )
