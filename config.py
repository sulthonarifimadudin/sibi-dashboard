"""
SIBI Dashboard — Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Central configuration for the SIBI Dashboard.
All tuneable parameters, feature flags, and static assets
are defined here.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from typing import Final


# ── Meta ─────────────────────────────────────────────────────────

DASHBOARD_TITLE: Final[str] = "SIBI Dashboard"
DASHBOARD_VERSION: Final[str] = "1.0.0"
DASHBOARD_AUTHOR: Final[str] = "Sulthon"
USER_NAME: Final[str] = "SIBI"

# ── Refresh ──────────────────────────────────────────────────────

REFRESH_INTERVAL: Final[float] = 2.0  # seconds

# ── ASCII Logo (Slant) ───────────────────────────────────────────

ASCII_LOGO: Final[str] = (
    "   _____ ________  ____\n"
    "  / ___//  _/ __ )/  _/\n"
    "  \__ \ / // __  |/ /  \n"
    " ___/ // // /_/ // /   \n"
    "/____/___/_____/___/   "
)

# ── ASCII Subtitle (small text) ──────────────────────────────────

LOGO_SUBTITLE: Final[str] = (
    " _    _    __  __   ___ ___ _____   _____ ___ \n"
    "| |  | |  |  \/  | / __| __| _ \ \ / / __| _ \\\n"
    "| |__| |__| |\/| | \__ \ _||   /\ V /| _||   /\n"
    "|____|____|_|  |_| |___/___|_|_\ \_/ |___|_|_\\\n"
    "                                              \n"
    " ___ ___  ___   ___ ___ ___ ___ \n"
    "| __/ _ \| _ \ / __|_ _| _ )_ _|\n"
    "| _| (_) |   / \__ \| || _ \| | \n"
    "|_| \___/|_|_\ |___/___|___/___|"
)

# ── Services ─────────────────────────────────────────────────────
# Each service maps to a detection strategy:
#   port     — TCP port to probe on localhost
#   process  — process name to search in the process table
#   icon     — Unicode icon for the services panel

SERVICES: Final[dict[str, dict[str, object]]] = {
    "Docker": {
        "port": None,
        "process": "dockerd",
        "icon": "🐳",
    },
    "Portainer": {
        "port": 9443,
        "process": None,
        "icon": "📦",
    },
    "Ollama": {
        "port": 11434,
        "process": "ollama",
        "icon": "🦙",
    },
    "Open WebUI": {
        "port": 3000,
        "process": None,
        "icon": "🌐",
    },
    "PostgreSQL": {
        "port": 5432,
        "process": "postgres",
        "icon": "🐘",
    },
    "Redis": {
        "port": 6379,
        "process": "redis-server",
        "icon": "🔴",
    },
    "Nginx Proxy": {
        "port": 81,
        "process": None,
        "icon": "🔀",
    },
    "ComfyUI": {
        "port": 8188,
        "process": None,
        "icon": "🎨",
    },
    "MLflow": {
        "port": 5000,
        "process": None,
        "icon": "📊",
    },
    "Jupyter": {
        "port": 8888,
        "process": None,
        "icon": "📓",
    },
    "SSH": {
        "port": 22,
        "process": "sshd",
        "icon": "🔑",
    },
    "Tailscale": {
        "port": None,
        "process": "tailscaled",
        "icon": "🔗",
    },
}

# ── Ollama API ───────────────────────────────────────────────────

OLLAMA_API_URL: Final[str] = "http://localhost:11434"

# ── Public IP ────────────────────────────────────────────────────

PUBLIC_IP_URL: Final[str] = "https://api.ipify.org"
PUBLIC_IP_TIMEOUT: Final[float] = 3.0

# ── Panel Feature Flags ─────────────────────────────────────────
# Set any panel to False to hide it from the dashboard.

ENABLED_PANELS: Final[dict[str, bool]] = {
    "header": True,
    "system": True,
    "resources": True,
    "network": True,
    "services": True,
    "docker": True,
    "gpu": True,
    "ollama": True,
    "footer": True,
}

# ── Layout ───────────────────────────────────────────────────────

WIDE_LAYOUT_MIN_COLS: Final[int] = 120
HEADER_HEIGHT: Final[int] = 13
FOOTER_HEIGHT: Final[int] = 3
