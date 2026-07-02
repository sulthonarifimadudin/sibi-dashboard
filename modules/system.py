"""
SIBI Dashboard — System
~~~~~~~~~~~~~~~~~~~~~~~~

System information collection using :mod:`psutil` and :mod:`platform`.
Gathers hostname, OS, kernel, CPU, memory, disk, uptime, and more.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import os
import platform
import sys
import time

import psutil

from modules.helpers import (
    format_bytes,
    format_timestamp,
    format_uptime,
    safe_command,
)
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_NORMAL, TEXT_PRIMARY

from rich.panel import Panel
from rich.table import Table


# ═══════════════════════════════════════════════════════════════════
#  Data Collectors
# ═══════════════════════════════════════════════════════════════════


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
    """Return the CPU architecture (e.g. ``x86_64``, ``aarch64``)."""
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


def get_cpu_threads() -> int:
    """Return the number of logical CPU threads."""
    return psutil.cpu_count(logical=True) or 0


def get_memory_total() -> str:
    """Return total physical memory as a formatted string."""
    return format_bytes(psutil.virtual_memory().total)


def get_memory_used() -> str:
    """Return used physical memory as a formatted string."""
    mem = psutil.virtual_memory()
    return f"{format_bytes(mem.used)} ({mem.percent}%)"


def get_disk_total() -> str:
    """Return total root disk space as a formatted string."""
    return format_bytes(psutil.disk_usage("/").total)


def get_disk_used() -> str:
    """Return used root disk space as a formatted string."""
    usage = psutil.disk_usage("/")
    return f"{format_bytes(usage.used)} ({usage.percent}%)"


def get_uptime() -> str:
    """Return the system uptime as a formatted string."""
    return format_uptime(time.time() - psutil.boot_time())


def get_boot_time() -> str:
    """Return the system boot time as a formatted timestamp."""
    return format_timestamp(psutil.boot_time())


def get_shell() -> str:
    """Return the current user's shell and version."""
    shell_path = os.environ.get("SHELL", "")
    if not shell_path:
        return "N/A"

    name = os.path.basename(shell_path)
    version_output = safe_command([shell_path, "--version"], default="")

    if version_output and version_output != "N/A":
        first_line = version_output.splitlines()[0]
        return first_line[:60]
    return name


def get_python_version() -> str:
    """Return the running Python version string."""
    v = sys.version_info
    return f"{v.major}.{v.minor}.{v.micro}"


# ═══════════════════════════════════════════════════════════════════
#  Panel Builder
# ═══════════════════════════════════════════════════════════════════


def _info_rows() -> list[tuple[str, str]]:
    """Collect all system info key-value pairs."""
    return [
        ("🖥  Hostname", get_hostname()),
        ("💿  OS", get_os_info()),
        ("🔧  Kernel", get_kernel()),
        ("📐  Architecture", get_architecture()),
        ("⚡  CPU Model", get_cpu_model()),
        ("🧮  CPU Cores", str(get_cpu_cores())),
        ("🧵  CPU Threads", str(get_cpu_threads())),
        ("🧠  Mem Total", get_memory_total()),
        ("📊  Mem Used", get_memory_used()),
        ("💾  Disk Total", get_disk_total()),
        ("📀  Disk Used", get_disk_used()),
        ("⏱  Uptime", get_uptime()),
        ("📅  Boot Time", get_boot_time()),
        ("🐚  Shell", get_shell()),
        ("🐍  Python", get_python_version()),
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
        min_width=16,
        ratio=1,
    )
    table.add_column("Value", style=TEXT_PRIMARY, ratio=2)

    for label, value in _info_rows():
        table.add_row(f"  {label}", value)

    return Panel(
        table,
        title=f"[bold {ACCENT_CYAN}]⚙  System Info[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )
