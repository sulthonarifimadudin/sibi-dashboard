"""
SIBI Dashboard — Docker
~~~~~~~~~~~~~~~~~~~~~~~~

Docker container and resource monitoring via the Docker SDK.

.. note::

   This file is named ``docker.py`` inside the ``modules`` package.
   Because Python 3 uses absolute imports by default, ``import docker``
   within this file resolves to the **pip-installed** ``docker`` package,
   not to ``modules.docker`` (i.e. itself).

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from typing import Any, Optional

from modules.helpers import format_bytes, truncate
from theme import (
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    ACCENT_RED,
    ACCENT_YELLOW,
    BORDER_NORMAL,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ═══════════════════════════════════════════════════════════════════
#  Docker Client
# ═══════════════════════════════════════════════════════════════════


def _get_docker_client() -> Any:
    """Attempt to create a Docker client; return ``None`` on failure."""
    try:
        import docker as docker_lib  # pip package, not this file

        client = docker_lib.from_env(timeout=5)
        client.ping()
        return client
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════
#  Data Collectors
# ═══════════════════════════════════════════════════════════════════


def get_docker_summary(client: Any) -> dict[str, int]:
    """Return counts of containers, images, volumes, and networks."""
    try:
        containers = client.containers.list(all=True)
        running = sum(1 for c in containers if c.status == "running")
        stopped = len(containers) - running
        images = len(client.images.list())
        volumes = len(client.volumes.list())
        networks = len(client.networks.list())
        return {
            "running": running,
            "stopped": stopped,
            "images": images,
            "volumes": volumes,
            "networks": networks,
        }
    except Exception:
        return {}


def get_running_containers(client: Any) -> list[dict[str, str]]:
    """Return details of all running Docker containers."""
    containers: list[dict[str, str]] = []
    try:
        for ctr in client.containers.list():
            name = ctr.name or "unnamed"
            image = (
                str(ctr.image.tags[0])
                if ctr.image.tags
                else str(ctr.short_id)
            )
            status = ctr.status
            ports = _format_ports(ctr.ports or {})
            containers.append(
                {
                    "name": truncate(name, 20),
                    "image": truncate(image, 28),
                    "status": status,
                    "ports": ports,
                }
            )
    except Exception:
        pass
    return containers


# ═══════════════════════════════════════════════════════════════════
#  Formatters
# ═══════════════════════════════════════════════════════════════════


def _format_ports(ports: dict[str, Any]) -> str:
    """Format Docker port mappings into a concise string.

    Example output: ``8080→80/tcp, 443→443/tcp``
    """
    parts: list[str] = []
    for container_port, host_bindings in ports.items():
        if host_bindings:
            for binding in host_bindings:
                host_port = binding.get("HostPort", "?")
                parts.append(f"{host_port}→{container_port}")
        else:
            parts.append(str(container_port))
    if not parts:
        return "—"
    display = ", ".join(parts[:3])
    if len(parts) > 3:
        display += "…"
    return display


# ═══════════════════════════════════════════════════════════════════
#  Sub-tables
# ═══════════════════════════════════════════════════════════════════


def _summary_table(summary: dict[str, int]) -> Table:
    """Build a compact summary stats table."""
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1),
        show_edge=False,
        expand=True,
    )
    table.add_column(
        "Label", style=f"bold {ACCENT_PURPLE}", ratio=1
    )
    table.add_column("Value", style=TEXT_PRIMARY, ratio=1)

    rows: list[tuple[str, str, str]] = [
        ("🟢 Running", str(summary.get("running", 0)), ACCENT_GREEN),
        ("🔴 Stopped", str(summary.get("stopped", 0)), ACCENT_RED),
        ("📦 Images", str(summary.get("images", 0)), TEXT_PRIMARY),
        ("💾 Volumes", str(summary.get("volumes", 0)), TEXT_PRIMARY),
        ("🌐 Networks", str(summary.get("networks", 0)), TEXT_PRIMARY),
    ]

    for label, value, color in rows:
        table.add_row(f"  {label}", f"[bold {color}]{value}[/]")

    return table


def _containers_table(containers: list[dict[str, str]]) -> Table:
    """Build a table listing running containers."""
    table = Table(
        show_header=True,
        expand=True,
        box=None,
        padding=(0, 1),
        show_edge=False,
        header_style=f"bold {ACCENT_PURPLE}",
    )
    table.add_column("Container", style=TEXT_PRIMARY, ratio=2)
    table.add_column("Image", style=TEXT_SECONDARY, ratio=2)
    table.add_column("Status", style=f"bold {ACCENT_GREEN}", ratio=1)
    table.add_column("Ports", style=TEXT_MUTED, ratio=2)

    for ctr in containers[:10]:
        table.add_row(
            ctr["name"], ctr["image"], ctr["status"], ctr["ports"]
        )

    return table


# ═══════════════════════════════════════════════════════════════════
#  Panel Builder
# ═══════════════════════════════════════════════════════════════════


def build_docker_panel() -> Panel:
    """Build the Docker monitoring panel.

    If Docker is unreachable the panel shows a friendly
    "Docker is not available" message.
    """
    client = _get_docker_client()

    if client is None:
        return Panel(
            Text(
                "  Docker is not available or not running.",
                style=f"italic {TEXT_MUTED}",
            ),
            title=f"[bold {ACCENT_CYAN}]🐳  Docker[/]",
            border_style=BORDER_NORMAL,
            padding=(1, 1),
            expand=True,
        )

    summary = get_docker_summary(client)
    containers = get_running_containers(client)

    parts: list[object] = [_summary_table(summary)]

    if containers:
        parts.append(Text(""))
        parts.append(
            Text(
                "  Running Containers",
                style=f"bold {ACCENT_YELLOW}",
            )
        )
        parts.append(Text(""))
        parts.append(_containers_table(containers))

    return Panel(
        Group(*parts),
        title=f"[bold {ACCENT_CYAN}]🐳  Docker[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )
