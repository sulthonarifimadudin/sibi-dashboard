"""
SIBI Dashboard -- Network
~~~~~~~~~~~~~~~~~~~~~~~~~

Network information: LAN/Tailnet/public IPs, gateway, DNS,
and internet connectivity checks.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import socket
from typing import Optional

import psutil

from config import PUBLIC_IP_TIMEOUT, PUBLIC_IP_URL
from modules.helpers import safe_command
from theme import (
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    ACCENT_RED,
    BORDER_NORMAL,
    TEXT_PRIMARY,
)

from rich.panel import Panel
from rich.table import Table


# -------------------------------------------------------------------
#  Data Collectors
# -------------------------------------------------------------------


def get_lan_ip() -> str:
    """Return the primary LAN IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except (OSError, socket.error):
        return _fallback_lan_ip()


def _fallback_lan_ip() -> str:
    """Iterate psutil interfaces to find a non-loopback IPv4."""
    for _name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if (
                addr.family == socket.AF_INET
                and not addr.address.startswith("127.")
            ):
                return addr.address
    return "N/A"


def get_tailnet_ip() -> str:
    """Return the Tailscale (tailnet) IP if available."""
    for name, addrs in psutil.net_if_addrs().items():
        if "tailscale" in name.lower() or name.startswith("ts"):
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address

    return safe_command(
        ["tailscale", "ip", "-4"],
        timeout=3.0,
        default="N/A",
    )


def get_public_ip() -> str:
    """Return the public IP address via an external API."""
    try:
        import requests

        resp = requests.get(PUBLIC_IP_URL, timeout=PUBLIC_IP_TIMEOUT)
        resp.raise_for_status()
        return resp.text.strip()
    except Exception:
        return "N/A"


def get_gateway() -> str:
    """Return the default network gateway address."""
    gw = safe_command(
        [
            "sh", "-c",
            "ip route | grep default | awk '{print $3}' | head -1",
        ],
        default="",
    )
    if gw and gw != "N/A":
        return gw

    return safe_command(
        [
            "sh", "-c",
            "route -n get default 2>/dev/null "
            "| grep gateway | awk '{print $2}'",
        ],
        default="N/A",
    )


def get_dns_servers() -> str:
    """Return a comma-separated list of configured DNS servers."""
    raw = safe_command(
        [
            "sh", "-c",
            "grep nameserver /etc/resolv.conf "
            "| awk '{print $2}' | head -3",
        ],
        default="",
    )
    if raw and raw != "N/A":
        return ", ".join(raw.splitlines())
    return "N/A"


def check_internet() -> tuple[bool, str]:
    """Check internet connectivity."""
    try:
        socket.setdefaulttimeout(3)
        socket.create_connection(("8.8.8.8", 53))
        return True, "Online"
    except OSError:
        return False, "Offline"


# -------------------------------------------------------------------
#  Panel Builder
# -------------------------------------------------------------------


def _network_rows() -> list[tuple[str, str, Optional[str]]]:
    """Collect network info rows."""
    online, status_label = check_internet()
    status_color = ACCENT_GREEN if online else ACCENT_RED
    indicator = "\u2714" if online else "\u2716"  # check / cross marks

    return [
        ("\U0001f3e0  LAN IP", get_lan_ip(), None),
        ("\U0001f517  Tailnet", get_tailnet_ip(), None),
        ("\U0001f310  Public IP", get_public_ip(), None),
        ("\U0001f6aa  Gateway", get_gateway(), None),
        ("\U0001f50d  DNS", get_dns_servers(), None),
        ("\U0001f4e1  Internet", f"{indicator} {status_label}", status_color),
    ]


def build_network_panel() -> Panel:
    """Build the Network Information panel."""
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

    for label, value, style_override in _network_rows():
        styled = (
            f"[{style_override}]{value}[/]" if style_override else value
        )
        table.add_row(f"  {label}", styled)

    return Panel(
        table,
        title=f"[bold {ACCENT_CYAN}]\U0001f310  Network[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )
