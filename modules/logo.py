"""
SIBI Dashboard -- Logo
~~~~~~~~~~~~~~~~~~~~~~

ASCII art header and branding panel.
Renders the NeoFetch-style brain logo with inline
SIBI / LLM Server branding.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from config import ASCII_LOGO, DASHBOARD_TITLE
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_HIGHLIGHT


# -------------------------------------------------------------------
#  Public API
# -------------------------------------------------------------------


def build_header_panel() -> Panel:
    """Construct the header panel with the brain ASCII logo.

    The brain art includes inline text for SIBI and LLM Server,
    centered in a highlighted panel.
    """
    logo = Text(ASCII_LOGO, style=f"bold {ACCENT_CYAN}", no_wrap=True)

    return Panel(
        Align.center(logo, vertical="middle"),
        title=f"[bold {ACCENT_CYAN}]( {DASHBOARD_TITLE} )[/]",
        subtitle=f"[{ACCENT_PURPLE}]Enterprise AI Server Monitor[/]",
        border_style=BORDER_HIGHLIGHT,
        padding=(0, 2),
        expand=True,
    )
