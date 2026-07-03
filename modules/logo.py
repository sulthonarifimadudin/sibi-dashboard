"""
SIBI Dashboard — Logo
~~~~~~~~~~~~~~~~~~~~~~

ASCII art header and branding panel.
Renders the brain logo on the left and the large block-text
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
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_HIGHLIGHT, TEXT_PRIMARY
from modules.helpers import get_terminal_height


# ═══════════════════════════════════════════════════════════════════
#  Internal Builders
# ═══════════════════════════════════════════════════════════════════


def _render_logo() -> Text:
    """Build a Rich :class:`Text` from the brain ASCII logo."""
    return Text(ASCII_LOGO, style=f"bold {ACCENT_CYAN}", no_wrap=True)


def _render_subtitle() -> Text:
    """Build the right-side big block-text subtitle."""
    return Text(LOGO_SUBTITLE, style=f"bold {ACCENT_PURPLE}", no_wrap=True)


# ═══════════════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════════════


def build_header_panel() -> Panel:
    """Construct the full header panel with brain logo + big subtitle.

    The brain logo sits on the left and the large ASCII block-text
    *LLM SERVER FOR SIBI* sits on the right. Table.grid is used
    to ensure they stay strictly side-by-side without wrapping.
    """
    logo = _render_logo()
    subtitle = _render_subtitle()

    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)
    grid.add_row(
        Align.center(logo, vertical="middle"),
        Align.center(subtitle, vertical="middle"),
    )

    return Panel(
        Align.center(grid),
        title=f"[bold {ACCENT_CYAN}]⟨ {DASHBOARD_TITLE} ⟩[/]",
        subtitle=f"[{ACCENT_PURPLE}]Enterprise AI Server Monitor[/]",
        border_style=BORDER_HIGHLIGHT,
        padding=(0, 2),
        expand=True,
    )
