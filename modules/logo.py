"""
SIBI Dashboard -- Logo
~~~~~~~~~~~~~~~~~~~~~~

ASCII art header and branding panel.
Renders the robot logo on the left and the large block-text
*LLM SERVER FOR SIBI* subtitle on the right.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from config import ASCII_LOGO, DASHBOARD_TITLE, LOGO_SUBTITLE
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_HIGHLIGHT


# -------------------------------------------------------------------
#  Public API
# -------------------------------------------------------------------


def build_header_panel() -> Panel:
    """Construct the full header panel with robot logo + big subtitle.

    The robot art sits on the left and the large ASCII block-text
    *LLM SERVER FOR SIBI* sits on the right. Table.grid is used
    to ensure they stay side-by-side without wrapping.
    """
    # Gemini-inspired colors
    logo = Text(ASCII_LOGO, style="bold #8ab4f8", no_wrap=True)
    subtitle = Text(LOGO_SUBTITLE, style="bold #c58af9", no_wrap=True)

    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=2)
    grid.add_row(
        Align.center(logo, vertical="middle"),
        Align.center(subtitle, vertical="middle"),
    )

    return Panel(
        Align.center(grid),
        title=f"[bold {ACCENT_CYAN}]( {DASHBOARD_TITLE} )[/]",
        subtitle=f"[{ACCENT_PURPLE}]Enterprise AI Server Monitor[/]",
        border_style=BORDER_HIGHLIGHT,
        padding=(0, 2),
        expand=True,
    )
