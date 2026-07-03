"""
SIBI Dashboard — Widgets
~~~~~~~~~~~~~~~~~~~~~~~~~

Reusable UI widgets and composite panels:

* **Resource Panel** — CPU, memory, disk, swap, temperature, load,
  network I/O, and battery progress bars.
* **GPU Panel** — NVIDIA GPU stats via ``nvidia-smi``.
* **Ollama Panel** — installed and running LLM models.
* **Footer** — greeting, date/time, timezone, version.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

import psutil

from config import DASHBOARD_VERSION, OLLAMA_API_URL, USER_NAME
from modules.helpers import clamp, format_bytes, safe_command
from theme import (
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    BORDER_HIGHLIGHT,
    BORDER_NORMAL,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    progress_color,
)

from rich.align import Align
from rich.bar import Bar
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ═══════════════════════════════════════════════════════════════════
#  Progress Bar Factory
# ═══════════════════════════════════════════════════════════════════


def _colored_bar(
    label: str,
    value: float,
    total: float = 100.0,
    suffix: str = "",
    bar_width: int = 20,
) -> Table:
    """Create a single row with a coloured progress bar.

    The bar colour adapts based on the percentage:
    green (<50%), yellow (50–80%), red (>80%).
    """
    pct = clamp((value / total) * 100.0 if total > 0 else 0.0)
    color = progress_color(pct)

    bar = Bar(
        size=total,
        begin=0,
        end=value,
        color=color,
        bgcolor="#30363d",
        width=bar_width,
    )

    display = suffix if suffix else f"{pct:.0f}%"

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1),
        show_edge=False,
        expand=True,
    )
    table.add_column("Label", style=f"bold {TEXT_SECONDARY}", width=12)
    table.add_column("Bar", ratio=3)
    table.add_column(
        "Value", style=f"bold {color}", width=12, justify="right"
    )
    table.add_row(f"  {label}", bar, display)
    return table


# ═══════════════════════════════════════════════════════════════════
#  Resource Collectors
# ═══════════════════════════════════════════════════════════════════


def _get_cpu_percent() -> float:
    """Return current CPU usage percentage."""
    return psutil.cpu_percent(interval=0.1)


def _get_memory_percent() -> float:
    """Return current memory usage percentage."""
    return psutil.virtual_memory().percent


def _get_disk_percent() -> float:
    """Return current root disk usage percentage."""
    return psutil.disk_usage("/").percent


def _get_swap_percent() -> float:
    """Return current swap usage percentage (0 if no swap)."""
    swap = psutil.swap_memory()
    return swap.percent if swap.total > 0 else 0.0


def _get_temperature() -> Optional[float]:
    """Return the highest CPU temperature if available."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        # Prefer well-known sensor names
        preferred = ("coretemp", "cpu_thermal", "k10temp", "zenpower")
        for name in preferred:
            if name in temps and temps[name]:
                return max(r.current for r in temps[name])
        # Fallback: first available sensor
        for readings in temps.values():
            if readings:
                return max(r.current for r in readings)
    except (AttributeError, OSError):
        pass
    return None


def _get_load_average() -> Optional[tuple[float, float, float]]:
    """Return the 1/5/15-min load averages or ``None``."""
    try:
        load = psutil.getloadavg()
        return load  # type: ignore[return-value]
    except (AttributeError, OSError):
        return None


def _get_network_io() -> tuple[str, str]:
    """Return formatted total upload / download since boot."""
    counters = psutil.net_io_counters()
    return (
        format_bytes(counters.bytes_sent),
        format_bytes(counters.bytes_recv),
    )


def _get_battery() -> Optional[tuple[float, bool]]:
    """Return ``(percent, is_charging)`` or ``None``."""
    try:
        batt = psutil.sensors_battery()
        if batt is not None:
            return batt.percent, bool(batt.power_plugged)
    except (AttributeError, OSError):
        pass
    return None


# ═══════════════════════════════════════════════════════════════════
#  Resource Panel
# ═══════════════════════════════════════════════════════════════════


def build_resource_panel() -> Panel:
    """Build the Resource Usage panel with coloured progress bars."""
    parts: list[object] = []

    parts.append(_colored_bar("CPU", _get_cpu_percent()))
    parts.append(_colored_bar("Memory", _get_memory_percent()))
    parts.append(_colored_bar("Disk", _get_disk_percent()))
    parts.append(_colored_bar("Swap", _get_swap_percent()))

    # Temperature
    temp = _get_temperature()
    if temp is not None:
        parts.append(
            _colored_bar("Temp", clamp(temp, 0, 110), 110.0, f"{temp:.0f}C")
        )
    else:
        parts.append(_colored_bar("Temp", 0, suffix="N/A"))

    # Load Average
    load = _get_load_average()
    if load is not None:
        cores = psutil.cpu_count(logical=True) or 1
        load_pct = clamp((load[0] / cores) * 100.0)
        parts.append(_colored_bar("Load", load_pct, suffix=f"{load[0]:.2f}"))
    else:
        parts.append(_colored_bar("Load", 0, suffix="N/A"))

    # Network I/O
    net_up, net_down = _get_network_io()
    parts.append(_colored_bar("Net Up", 0, suffix=net_up))
    parts.append(_colored_bar("Net Down", 0, suffix=net_down))

    # Battery (optional)
    battery = _get_battery()
    if battery is not None:
        pct, charging = battery
        icon = "[+]" if charging else "[-]"
        parts.append(
            _colored_bar("Battery", pct, suffix=f"{pct:.0f}%")
        )

    return Panel(
        Group(*parts),
        title=f"[bold {ACCENT_CYAN}]Resources[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )


# ═══════════════════════════════════════════════════════════════════
#  GPU Panel  (NVIDIA only)
# ═══════════════════════════════════════════════════════════════════


def _parse_nvidia_smi() -> Optional[dict[str, str]]:
    """Parse ``nvidia-smi`` output for GPU information."""
    raw = safe_command(
        [
            "nvidia-smi",
            "--query-gpu=driver_version,name,temperature.gpu,"
            "memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        timeout=5.0,
        default="",
    )
    if not raw or raw == "N/A":
        return None

    parts = [p.strip() for p in raw.split(",")]
    if len(parts) < 6:
        return None

    cuda = _detect_cuda_version()

    return {
        "driver": parts[0],
        "cuda": cuda,
        "name": parts[1],
        "temp": parts[2],
        "vram_used": parts[3],
        "vram_total": parts[4],
        "gpu_util": parts[5],
    }


def _detect_cuda_version() -> str:
    """Detect CUDA version via nvidia-smi or nvcc."""
    # Try nvidia-smi first
    cuda = safe_command(
        [
            "nvidia-smi",
            "--query-gpu=cuda_version",
            "--format=csv,noheader",
        ],
        timeout=3.0,
        default="",
    ).strip()
    if cuda:
        return cuda

    # Fallback: nvcc --version
    nvcc = safe_command(["nvcc", "--version"], default="")
    if "release" in nvcc.lower():
        for line in nvcc.splitlines():
            if "release" in line.lower():
                return (
                    line.split("release")[-1]
                    .strip()
                    .split(",")[0]
                    .strip()
                )
    return "N/A"


def _gpu_info_table(gpu: dict[str, str]) -> Table:
    """Build a key-value table of GPU properties."""
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1),
        show_edge=False,
        expand=True,
    )
    table.add_column(
        "Label", style=f"bold {ACCENT_PURPLE}", min_width=14, ratio=1
    )
    table.add_column("Value", style=TEXT_PRIMARY, ratio=2)

    rows = [
        ("  Driver", gpu["driver"]),
        ("  CUDA", gpu["cuda"]),
        ("  GPU Name", gpu["name"]),
        ("  Temp", f"{gpu['temp']}C"),
        ("  VRAM", f"{gpu['vram_used']} / {gpu['vram_total']} MiB"),
        ("  GPU Load", f"{gpu['gpu_util']}%"),
    ]
    for label, value in rows:
        table.add_row(f"  {label}", value)

    return table


def build_gpu_panel() -> Panel:
    """Build the GPU Information panel.

    Falls back to *"No NVIDIA GPU detected"* when ``nvidia-smi``
    is not available.
    """
    gpu = _parse_nvidia_smi()

    if gpu is None:
        return Panel(
            Text(
                "  No NVIDIA GPU detected.",
                style=f"italic {TEXT_MUTED}",
            ),
            title=f"[bold {ACCENT_CYAN}]GPU[/]",
            border_style=BORDER_NORMAL,
            padding=(1, 1),
            expand=True,
        )

    parts: list[object] = [_gpu_info_table(gpu)]

    # VRAM progress bar
    try:
        used = float(gpu["vram_used"])
        total = float(gpu["vram_total"])
        pct = (used / total) * 100.0
        parts.append(Text(""))
        parts.append(
            _colored_bar("VRAM", used, total, suffix=f"{pct:.0f}%")
        )
    except (ValueError, ZeroDivisionError):
        pass

    # GPU utilization bar
    try:
        util = float(gpu["gpu_util"])
        parts.append(_colored_bar("GPU Load", util))
    except ValueError:
        pass

    return Panel(
        Group(*parts),
        title=f"[bold {ACCENT_CYAN}]GPU[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )


# ═══════════════════════════════════════════════════════════════════
#  Ollama Panel
# ═══════════════════════════════════════════════════════════════════


def _fetch_ollama_models() -> Optional[list[dict]]:
    """Fetch installed models from the Ollama API."""
    try:
        import requests

        resp = requests.get(
            f"{OLLAMA_API_URL}/api/tags", timeout=3
        )
        resp.raise_for_status()
        return resp.json().get("models", [])
    except Exception:
        return None


def _fetch_ollama_running() -> list[dict]:
    """Fetch currently loaded/running models from Ollama."""
    try:
        import requests

        resp = requests.get(
            f"{OLLAMA_API_URL}/api/ps", timeout=3
        )
        resp.raise_for_status()
        return resp.json().get("models", [])
    except Exception:
        return []


def _models_table(
    models: list[dict],
    running_names: set[str],
) -> Table:
    """Build a table listing Ollama models."""
    table = Table(
        show_header=True,
        expand=True,
        box=None,
        padding=(0, 1),
        show_edge=False,
        header_style=f"bold {ACCENT_PURPLE}",
    )
    table.add_column("Model", style=TEXT_PRIMARY, ratio=3)
    table.add_column("Size", style=TEXT_SECONDARY, ratio=1, justify="right")
    table.add_column("Status", ratio=1, justify="center")

    for model in models[:15]:
        name = model.get("name", "unknown")
        size_raw = model.get("size", 0)
        size_str = (
            format_bytes(size_raw)
            if isinstance(size_raw, (int, float))
            else str(size_raw)
        )
        is_loaded = name in running_names
        status = (
            Text("[+] Loaded", style=f"bold {ACCENT_GREEN}")
            if is_loaded
            else Text("[-] Idle", style=TEXT_MUTED)
        )
        table.add_row(f"  {name}", size_str, status)

    return table


def build_ollama_panel() -> Panel:
    """Build the Ollama Models panel.

    Shows installed models, their sizes, and which ones are
    currently loaded in memory.
    """
    models = _fetch_ollama_models()

    if models is None:
        return Panel(
            Text(
                "  Ollama is not available.",
                style=f"italic {TEXT_MUTED}",
            ),
            title=f"[bold {ACCENT_CYAN}]Ollama[/]",
            border_style=BORDER_NORMAL,
            padding=(1, 1),
            expand=True,
        )

    running = _fetch_ollama_running()
    running_names = {m.get("name", "") for m in running}

    table = _models_table(models, running_names)
    summary = Text(
        f"\n  {len(models)} model(s) installed  |  "
        f"{len(running)} running",
        style=f"bold {TEXT_SECONDARY}",
    )

    return Panel(
        Group(table, summary),
        title=f"[bold {ACCENT_CYAN}]Ollama[/]",
        border_style=BORDER_NORMAL,
        padding=(1, 1),
        expand=True,
    )


# ═══════════════════════════════════════════════════════════════════
#  Footer
# ═══════════════════════════════════════════════════════════════════


def build_footer() -> Panel:
    """Build the dashboard footer with greeting, clock, and version."""
    now = datetime.now()
    tz_name = time.strftime("%Z") or "UTC"

    segments: list[str] = [
        f"[bold {ACCENT_CYAN}]Welcome back, {USER_NAME}[/]",
        f"[{TEXT_SECONDARY}]{now.strftime('%A, %d %B %Y')}[/]",
        f"[{TEXT_SECONDARY}]{now.strftime('%H:%M:%S')} {tz_name}[/]",
        f"[{TEXT_MUTED}]v{DASHBOARD_VERSION}[/]",
    ]

    footer_text = Text.from_markup("  |  ".join(segments))

    return Panel(
        Align.center(footer_text),
        border_style=BORDER_HIGHLIGHT,
        padding=(0, 1),
        expand=True,
    )
