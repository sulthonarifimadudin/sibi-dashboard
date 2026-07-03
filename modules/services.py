"""
SIBI Dashboard — Services
~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatic detection of running services by probing TCP ports
and scanning the process table.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import socket
from typing import Optional

import psutil

from config import SERVICES
from theme import (
    ACCENT_CYAN,
    BORDER_NORMAL,
    STATUS_RUNNING,
    STATUS_STOPPED,
    STATUS_UNKNOWN,
    TEXT_PRIMARY,
)

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ═══════════════════════════════════════════════════════════════════
#  Detection Helpers
# ═══════════════════════════════════════════════════════════════════


def _check_port(
    port: int,
    host: str = "127.0.0.1",
    timeout: float = 0.5,
) -> bool:
    """Return ``True`` if a TCP port is open on *host*."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except OSError:
        return False


def _check_process(name: str) -> bool:
    """Return ``True`` if a process whose name contains *name* exists."""
    name_lower = name.lower()
    for proc in psutil.process_iter(["name", "cmdline"]):
        try:
            proc_name = (proc.info["name"] or "").lower()
            if name_lower in proc_name:
                return True
            cmdline = proc.info.get("cmdline") or []
            if any(name_lower in arg.lower() for arg in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


# ═══════════════════════════════════════════════════════════════════
#  Service Detection
# ═══════════════════════════════════════════════════════════════════


def detect_service(service_cfg: dict[str, object]) -> Optional[bool]:
    """Detect whether a single service is running.

    Returns:
        * ``True``  — service confirmed running
        * ``False`` — service confirmed stopped
        * ``None``  — detection not possible (no port/process configured)
    """
    port = service_cfg.get("port")
    process = service_cfg.get("process")

    if port is not None and _check_port(int(port)):
        return True
    if process is not None and _check_process(str(process)):
        return True
    if port is not None or process is not None:
        return False
    return None


def detect_all_services() -> list[tuple[str, str, Optional[bool]]]:
    """Detect all configured services.

    Returns a list of ``(service_name, icon, is_running)`` tuples.
    """
    results: list[tuple[str, str, Optional[bool]]] = []
    for name, cfg in SERVICES.items():
        status = detect_service(cfg)
        icon = str(cfg.get("icon", ">>"))
        results.append((name, icon, status))
    return results


# ═══════════════════════════════════════════════════════════════════
#  UI Helpers
# ═══════════════════════════════════════════════════════════════════


def _status_indicator(running: Optional[bool]) -> Text:
    """Return a styled ``✔ Running`` / ``✖ Stopped`` / ``? Unknown`` text."""
    if running is True:
        return Text("[+] Running", style=f"bold {STATUS_RUNNING}")
    if running is False:
        return Text("[x] Stopped", style=f"bold {STATUS_STOPPED}")
    return Text("[?] Unknown", style=f"italic {STATUS_UNKNOWN}")


# ═══════════════════════════════════════════════════════════════════
#  Panel Builder
# ═══════════════════════════════════════════════════════════════════


def build_services_panel() -> Panel:
    """Build the Services Detection panel.

    Lists every service defined in :data:`config.SERVICES`
    with its live status.
    """
    services = detect_all_services()

    table = Table(
        show_header=False,
        expand=True,
        box=None,
        padding=(0, 1),
        show_edge=False,
    )
    table.add_column("Icon", width=3, justify="center")
    table.add_column("Service", style=TEXT_PRIMARY, min_width=14, ratio=1)
    table.add_column("Status", ratio=1)

    for name, icon, running in services:
        table.add_row(icon, name, _status_indicator(running))

    return Panel(
        table,
        title=f"[bold {ACCENT_CYAN}]Services[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )
