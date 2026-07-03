#!/usr/bin/env python3
"""
SIBI Dashboard — Main Entry Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enterprise AI server monitoring dashboard built with Rich.

Usage::

    python dashboard.py             # render once
    python dashboard.py --watch     # auto-refresh (default 2 s)
    python dashboard.py --interval 5  # custom interval

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from typing import NoReturn

# ── Ensure project root is on sys.path ───────────────────────────
# When the user runs `python dashboard.py` from *outside* the
# project directory we still need `config`, `theme`, and `modules`
# to be importable.

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from rich.console import Console, Group, RenderableType
from rich.table import Table
from rich.live import Live

from config import (
    DASHBOARD_TITLE,
    DASHBOARD_VERSION,
    ENABLED_PANELS,
    FOOTER_HEIGHT,
    HEADER_HEIGHT,
    REFRESH_INTERVAL,
    WIDE_LAYOUT_MIN_COLS,
)
from modules import (
    build_docker_panel,
    build_footer,
    build_gpu_panel,
    build_header_panel,
    build_network_panel,
    build_ollama_panel,
    build_resource_panel,
    build_services_panel,
    build_system_panel,
)
from modules.helpers import get_terminal_width, get_terminal_height
from theme import ACCENT_CYAN, SIBI_THEME


# ═══════════════════════════════════════════════════════════════════
#  Layout Construction
# ═══════════════════════════════════════════════════════════════════


def _build_wide_layout() -> RenderableType:
    """Build a two-column layout for terminals ≥ 120 cols."""
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    left_panels = []
    if ENABLED_PANELS.get("system", True): left_panels.append(build_system_panel())
    if ENABLED_PANELS.get("resources", True): left_panels.append(build_resource_panel())
    left = Group(*left_panels)

    svc_net_row = Table.grid(expand=True)
    svc_net_row.add_column(ratio=1)
    svc_net_row.add_column(ratio=1)
    svc_net_row.add_row(
        build_services_panel() if ENABLED_PANELS.get("services", True) else "",
        build_network_panel() if ENABLED_PANELS.get("network", True) else ""
    )

    gpu_ollama_row = Table.grid(expand=True)
    gpu_ollama_row.add_column(ratio=1)
    gpu_ollama_row.add_column(ratio=1)
    gpu_ollama_row.add_row(
        build_gpu_panel() if ENABLED_PANELS.get("gpu", True) else "",
        build_ollama_panel() if ENABLED_PANELS.get("ollama", True) else ""
    )

    right_panels = []
    right_panels.append(svc_net_row)
    if ENABLED_PANELS.get("docker", True): right_panels.append(build_docker_panel())
    right_panels.append(gpu_ollama_row)
    right = Group(*right_panels)

    grid.add_row(left, right)

    parts = []
    if ENABLED_PANELS.get("header", True):
        parts.append(build_header_panel())
    parts.append(grid)
    if ENABLED_PANELS.get("footer", True):
        parts.append(build_footer())

    return Group(*parts)


def _build_narrow_layout() -> RenderableType:
    """Build a single-column stacked layout for terminals < 120 cols."""
    parts = []
    
    panel_map = [
        ("header", build_header_panel),
        ("system", build_system_panel),
        ("resources", build_resource_panel),
        ("services", build_services_panel),
        ("network", build_network_panel),
        ("docker", build_docker_panel),
        ("gpu", build_gpu_panel),
        ("ollama", build_ollama_panel),
        ("footer", build_footer),
    ]

    for name, builder in panel_map:
        if ENABLED_PANELS.get(name, True):
            parts.append(builder())
            
    return Group(*parts)


def _build_layout() -> RenderableType:
    """Select the appropriate layout based on terminal width."""
    width = get_terminal_width()
    if width >= WIDE_LAYOUT_MIN_COLS:
        return _build_wide_layout()
    return _build_narrow_layout()


# ═══════════════════════════════════════════════════════════════════
#  Render Modes
# ═══════════════════════════════════════════════════════════════════


def render_once(console: Console) -> None:
    """Render the dashboard once and print to *console*."""
    layout = _build_layout()
    console.print(layout)


def watch(console: Console, interval: float) -> NoReturn:
    """Continuously refresh the dashboard using Rich Live.

    :param interval: seconds between refreshes.
    """
    with Live(
        console=console,
        refresh_per_second=1,
        screen=True,
    ) as live:
        while True:
            # Rebuild layout on every tick to support dynamic resizing
            layout = _build_layout()
            live.update(layout)
            time.sleep(interval)


# ═══════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="sibi-dashboard",
        description=(
            f"{DASHBOARD_TITLE} v{DASHBOARD_VERSION} "
            "— Enterprise AI Server Dashboard"
        ),
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help=f"Auto-refresh every {REFRESH_INTERVAL}s (default interval)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=REFRESH_INTERVAL,
        metavar="SEC",
        help=f"Refresh interval in seconds (default: {REFRESH_INTERVAL})",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {DASHBOARD_VERSION}",
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════
#  Entry Point
# ═══════════════════════════════════════════════════════════════════


def main() -> None:
    """Application entry point."""
    args = _parse_args()
    console = Console(theme=SIBI_THEME, force_terminal=True)

    try:
        if args.watch:
            watch(console, args.interval)
        else:
            render_once(console)
    except KeyboardInterrupt:
        console.print(
            f"\n[bold {ACCENT_CYAN}]"
            "👋 Dashboard stopped. Goodbye!"
            "[/]\n"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
