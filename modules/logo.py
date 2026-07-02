"""
SIBI Dashboard — Logo
~~~~~~~~~~~~~~~~~~~~~~

ASCII art header and branding panel.
Renders the AI logo on the left and the server subtitle
on the right inside a highlighted Rich Panel.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text

from config import ASCII_LOGO, DASHBOARD_TITLE, LOGO_SUBTITLE_LINES
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_HIGHLIGHT, TEXT_PRIMARY


# ═══════════════════════════════════════════════════════════════════
#  Internal Builders
# ═══════════════════════════════════════════════════════════════════


def _render_logo() -> Text:
    """Build a Rich :class:`Text` from the ASCII logo constant."""
    return Text(ASCII_LOGO, style=f"bold {ACCENT_CYAN}", no_wrap=True)


def _render_subtitle() -> Text:
    """Build the right-side subtitle block (vertically centred)."""
    block = Text(justify="center")
    for idx, line in enumerate(LOGO_SUBTITLE_LINES):
        if idx == 0:
            style = f"bold {ACCENT_PURPLE}"
        else:
            style = f"bold {TEXT_PRIMARY}"
        block.append(line, style=style)
        if idx < len(LOGO_SUBTITLE_LINES) - 1:
            block.append("\n")
    return block


# ═══════════════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════════════


def build_header_panel() -> Panel:
    """Construct the full header panel with logo + subtitle.

    The logo sits on the left and the *LLM / SERVER / FOR SIBI*
    tagline sits on the right, both centred within a highlighted
    border panel.
    """
    logo = _render_logo()
    subtitle = Align.center(
        _render_subtitle(),
        vertical="middle",
    )

    content = Columns(
        [
            Align.center(logo),
            Align.center(subtitle, vertical="middle"),
        ],
        equal=True,
        expand=True,
    )

    return Panel(
        Align.center(content),
        title=f"[bold {ACCENT_CYAN}]⟨ {DASHBOARD_TITLE} ⟩[/]",
        subtitle=f"[{ACCENT_PURPLE}]Enterprise AI Server Monitor[/]",
        border_style=BORDER_HIGHLIGHT,
        padding=(1, 2),
        expand=True,
    )
