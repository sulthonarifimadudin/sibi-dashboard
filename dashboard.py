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

from rich.console import Console
from rich.layout import Layout
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


def _build_wide_layout() -> Layout:
    """Build a two-column layout for terminals ≥ 120 cols."""
    header_size = HEADER_HEIGHT if get_terminal_height() >= 28 else 3
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=header_size),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=FOOTER_HEIGHT),
    )

    # Body → left / right columns
    layout["body"].split_row(
        Layout(name="left_col", ratio=1),
        Layout(name="right_col", ratio=1),
    )

    # Left: system info + resource bars
    layout["left_col"].split_column(
        Layout(name="system", ratio=1),
        Layout(name="resources", ratio=1),
    )

    # Right: top row (services + network), docker, bottom row (gpu + ollama)
    layout["right_col"].split_column(
        Layout(name="svc_net_row", ratio=1),
        Layout(name="docker", ratio=1),
        Layout(name="gpu_ollama_row", ratio=1),
    )

    layout["svc_net_row"].split_row(
        Layout(name="services", ratio=1),
        Layout(name="network", ratio=1),
    )

    layout["gpu_ollama_row"].split_row(
        Layout(name="gpu", ratio=1),
        Layout(name="ollama", ratio=1),
    )

    return layout


def _build_narrow_layout() -> Layout:
    """Build a single-column stacked layout for terminals < 120 cols."""
    header_size = HEADER_HEIGHT if get_terminal_height() >= 28 else 3
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=header_size),
        Layout(name="system", ratio=1),
        Layout(name="resources", ratio=1),
        Layout(name="services", ratio=1),
        Layout(name="network", ratio=1),
        Layout(name="docker", ratio=1),
        Layout(name="gpu", ratio=1),
        Layout(name="ollama", ratio=1),
        Layout(name="footer", size=FOOTER_HEIGHT),
    )

    return layout


def _build_layout() -> Layout:
    """Select the appropriate layout based on terminal width."""
    width = get_terminal_width()
    if width >= WIDE_LAYOUT_MIN_COLS:
        return _build_wide_layout()
    return _build_narrow_layout()


# ═══════════════════════════════════════════════════════════════════
#  Layout Population
# ═══════════════════════════════════════════════════════════════════


def _populate_layout(layout: Layout) -> Layout:
    """Fill every layout slot with live panel content.

    Respects ``ENABLED_PANELS`` in :mod:`config` — disabled
    panels are silently skipped.
    """
    _panel_map: dict[str, object] = {
        "header": build_header_panel,
        "system": build_system_panel,
        "resources": build_resource_panel,
        "services": build_services_panel,
        "network": build_network_panel,
        "docker": build_docker_panel,
        "gpu": build_gpu_panel,
        "ollama": build_ollama_panel,
        "footer": build_footer,
    }

    for name, builder in _panel_map.items():
        if ENABLED_PANELS.get(name, True):
            try:
                layout[name].update(builder())  # type: ignore[operator]
            except KeyError:
                pass  # slot doesn't exist in this layout variant

    return layout


# ═══════════════════════════════════════════════════════════════════
#  Render Modes
# ═══════════════════════════════════════════════════════════════════


def render_once(console: Console) -> None:
    """Render the dashboard once and print to *console*."""
    layout = _build_layout()
    _populate_layout(layout)
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
            _populate_layout(layout)
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
