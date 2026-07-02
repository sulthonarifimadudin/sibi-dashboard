"""
SIBI Dashboard — Theme
~~~~~~~~~~~~~~~~~~~~~~~

Centralized color palette and Rich Theme definition.
All visual styles are defined here so that every module
draws from a single source of truth.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from typing import Final

from rich.style import Style
from rich.theme import Theme


# ═══════════════════════════════════════════════════════════════════
#  Color Palette  —  GitHub-Dark inspired
# ═══════════════════════════════════════════════════════════════════

# ── Backgrounds ──────────────────────────────────────────────────

BG_PRIMARY: Final[str] = "#0d1117"
BG_SECONDARY: Final[str] = "#161b22"
BG_TERTIARY: Final[str] = "#1c2333"

# ── Text ─────────────────────────────────────────────────────────

TEXT_PRIMARY: Final[str] = "#e6edf3"
TEXT_SECONDARY: Final[str] = "#8b949e"
TEXT_MUTED: Final[str] = "#484f58"

# ── Accents ──────────────────────────────────────────────────────

ACCENT_CYAN: Final[str] = "#58a6ff"
ACCENT_PURPLE: Final[str] = "#bc8cff"
ACCENT_BLUE: Final[str] = "#388bfd"
ACCENT_GREEN: Final[str] = "#3fb950"
ACCENT_YELLOW: Final[str] = "#d29922"
ACCENT_ORANGE: Final[str] = "#db6d28"
ACCENT_RED: Final[str] = "#f85149"
ACCENT_PINK: Final[str] = "#f778ba"

# ── Status ───────────────────────────────────────────────────────

STATUS_RUNNING: Final[str] = "#3fb950"
STATUS_STOPPED: Final[str] = "#f85149"
STATUS_UNKNOWN: Final[str] = "#8b949e"

# ── Progress bar thresholds ──────────────────────────────────────

PROGRESS_LOW: Final[str] = "#3fb950"      # green   < 50 %
PROGRESS_MEDIUM: Final[str] = "#d29922"   # yellow  50–80 %
PROGRESS_HIGH: Final[str] = "#f85149"     # red     > 80 %

# ── Panel borders ───────────────────────────────────────────────

BORDER_NORMAL: Final[str] = "#30363d"
BORDER_HIGHLIGHT: Final[str] = "#58a6ff"


# ═══════════════════════════════════════════════════════════════════
#  Rich Theme
# ═══════════════════════════════════════════════════════════════════

SIBI_THEME: Final[Theme] = Theme(
    {
        # general
        "info": f"bold {ACCENT_CYAN}",
        "info.label": f"bold {ACCENT_PURPLE}",
        "success": f"bold {ACCENT_GREEN}",
        "warning": f"bold {ACCENT_YELLOW}",
        "danger": f"bold {ACCENT_RED}",
        "muted": TEXT_MUTED,
        # header
        "header.title": f"bold {ACCENT_CYAN}",
        "header.subtitle": f"bold {TEXT_SECONDARY}",
        # panels
        "panel.border": BORDER_NORMAL,
        "panel.title": f"bold {ACCENT_CYAN}",
        # tables
        "table.header": f"bold {ACCENT_PURPLE}",
        # progress bars
        "progress.bar.low": PROGRESS_LOW,
        "progress.bar.medium": PROGRESS_MEDIUM,
        "progress.bar.high": PROGRESS_HIGH,
        # status
        "status.running": f"bold {STATUS_RUNNING}",
        "status.stopped": f"bold {STATUS_STOPPED}",
        "status.unknown": f"italic {STATUS_UNKNOWN}",
        # footer
        "footer.text": TEXT_SECONDARY,
        "footer.accent": f"bold {ACCENT_CYAN}",
        # misc
        "logo": f"bold {ACCENT_CYAN}",
        "logo.subtitle": f"bold {ACCENT_PURPLE}",
        "label": f"bold {TEXT_SECONDARY}",
        "value": TEXT_PRIMARY,
    }
)


# ═══════════════════════════════════════════════════════════════════
#  Helper Functions
# ═══════════════════════════════════════════════════════════════════


def progress_color(percentage: float) -> str:
    """Return the appropriate color hex for a given percentage value.

    * Green  — below 50 %
    * Yellow — between 50 % and 80 %
    * Red    — above 80 %
    """
    if percentage < 50.0:
        return PROGRESS_LOW
    if percentage <= 80.0:
        return PROGRESS_MEDIUM
    return PROGRESS_HIGH


def status_style(running: bool | None) -> Style:
    """Return a Rich :class:`Style` for the given service status.

    * ``True``  → green / bold
    * ``False`` → red / bold
    * ``None``  → grey / italic
    """
    if running is True:
        return Style(color=STATUS_RUNNING, bold=True)
    if running is False:
        return Style(color=STATUS_STOPPED, bold=True)
    return Style(color=STATUS_UNKNOWN, italic=True)
