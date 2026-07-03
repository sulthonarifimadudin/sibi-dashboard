"""
SIBI Dashboard -- Power
~~~~~~~~~~~~~~~~~~~~~~~~

Estimated power consumption panel.
Uses CPU load as a proxy to estimate current wattage,
accumulates daily kWh, and calculates estimated cost in IDR.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import time

import psutil

from config import IDLE_POWER_WATTS, POWER_RATE_PER_KWH
from theme import ACCENT_CYAN, ACCENT_PURPLE, BORDER_NORMAL, TEXT_PRIMARY

from rich.panel import Panel
from rich.table import Table


# -------------------------------------------------------------------
#  Power Estimation
# -------------------------------------------------------------------

# Maximum estimated wattage at 100% CPU load
_MAX_POWER_WATTS: float = 250.0

# Track boot time for daily estimation
_boot_time: float = psutil.boot_time()


def _estimate_current_watts() -> float:
    """Estimate current power draw based on CPU usage.

    Uses a linear model: idle_watts + (max - idle) * cpu_percent/100
    """
    cpu_pct = psutil.cpu_percent(interval=0.1)
    return IDLE_POWER_WATTS + (_MAX_POWER_WATTS - IDLE_POWER_WATTS) * (cpu_pct / 100.0)


def _estimate_today_kwh() -> float:
    """Estimate today's power consumption in kWh.

    Uses average of idle and current power draw over uptime hours.
    """
    uptime_hours = (time.time() - _boot_time) / 3600.0
    current_watts = _estimate_current_watts()
    avg_watts = (IDLE_POWER_WATTS + current_watts) / 2.0
    return (avg_watts * uptime_hours) / 1000.0


def _estimate_cost_idr(kwh: float) -> float:
    """Convert kWh to estimated cost in IDR."""
    return kwh * POWER_RATE_PER_KWH


def _format_rupiah(amount: float) -> str:
    """Format a number as Indonesian Rupiah."""
    if amount >= 1000:
        return f"Rp {amount:,.0f}"
    return f"Rp {amount:,.2f}"


# -------------------------------------------------------------------
#  Panel Builder
# -------------------------------------------------------------------


def build_power_panel() -> Panel:
    """Build the Power Estimation panel."""
    current_w = _estimate_current_watts()
    today_kwh = _estimate_today_kwh()
    cost = _estimate_cost_idr(today_kwh)

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
        no_wrap=True,
    )
    table.add_column("Value", style=TEXT_PRIMARY)

    table.add_row("  \u26a1 Current", f"{current_w:.0f} W")
    table.add_row("  \U0001f4c8 Today", f"{today_kwh:.2f} kWh")
    table.add_row("  \U0001f4b5 Estimated", _format_rupiah(cost))

    return Panel(
        table,
        title=f"[bold {ACCENT_CYAN}]\u26a1  Power[/]",
        border_style=BORDER_NORMAL,
        padding=(0, 1),
        expand=True,
    )
