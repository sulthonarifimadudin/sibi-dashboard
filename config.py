"""
SIBI Dashboard -- Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Central configuration for the SIBI Dashboard.
All tuneable parameters, feature flags, and static assets
are defined here.

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from __future__ import annotations

from typing import Final


# -- Meta ---------------------------------------------------------

DASHBOARD_TITLE: Final[str] = "SIBI Dashboard"
DASHBOARD_VERSION: Final[str] = "1.0.0"
DASHBOARD_AUTHOR: Final[str] = "Sulthon"
USER_NAME: Final[str] = "SIBI"

# -- Refresh ------------------------------------------------------

REFRESH_INTERVAL: Final[float] = 2.0  # seconds

# -- ASCII Logo (Gemini Star) --------------------------------------------

ASCII_LOGO: Final[str] = (
    "        ✧        \n"
    "      ✧ ✦ ✧      \n"
    "    ✧   ✦   ✧    \n"
    "  ✧     ✦     ✧  \n"
    "✧ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✧\n"
    "  ✧     ✦     ✧  \n"
    "    ✧   ✦   ✧    \n"
    "      ✧ ✦ ✧      \n"
    "        ✧        "
)

LOGO_SUBTITLE: Final[str] = (
    " ___  ___    _   _    ___  ___  _  _  \n"
    "/ __|| __|  /_\\ | |  |_ _|/ _ \\| \\| | \n"
    "\\__ \\| _|  / _ \\| |__ | || (_) | .  | \n"
    "|___/|___|/_/ \\_\\____|___|\\___/|_|\\_| "
)

# -- Services ------------------------------------------------------

SERVICES: Final[dict[str, dict[str, object]]] = {
    "Docker": {
        "port": None,
        "process": "dockerd",
        "icon": "\U0001f433",
    },
    "Portainer": {
        "port": 9443,
        "process": None,
        "icon": "\U0001f4e6",
    },
    "Ollama": {
        "port": 11434,
        "process": "ollama",
        "icon": "\U0001f999",
    },
    "Open WebUI": {
        "port": 3000,
        "process": None,
        "icon": "\U0001f310",
    },
    "PostgreSQL": {
        "port": 5432,
        "process": "postgres",
        "icon": "\U0001f418",
    },
    "Redis": {
        "port": 6379,
        "process": "redis-server",
        "icon": "\U0001f534",
    },
    "Nginx Proxy": {
        "port": 81,
        "process": None,
        "icon": "\U0001f500",
    },
    "ComfyUI": {
        "port": 8188,
        "process": None,
        "icon": "\U0001f3a8",
    },
    "MLflow": {
        "port": 5000,
        "process": None,
        "icon": "\U0001f4ca",
    },
    "Jupyter": {
        "port": 8888,
        "process": None,
        "icon": "\U0001f4d3",
    },
    "SSH": {
        "port": 22,
        "process": "sshd",
        "icon": "\U0001f511",
    },
    "Tailscale": {
        "port": None,
        "process": "tailscaled",
        "icon": "\U0001f517",
    },
}

# -- Ollama API ----------------------------------------------------

OLLAMA_API_URL: Final[str] = "http://localhost:11434"

# -- Public IP -----------------------------------------------------

PUBLIC_IP_URL: Final[str] = "https://api.ipify.org"
PUBLIC_IP_TIMEOUT: Final[float] = 3.0

# -- Power Estimation ---------------------------------------------

POWER_RATE_PER_KWH: Final[float] = 1444.70  # Rp/kWh
IDLE_POWER_WATTS: Final[float] = 80.0        # estimated idle draw

# -- Panel Feature Flags ------------------------------------------

ENABLED_PANELS: Final[dict[str, bool]] = {
    "header": True,
    "system": True,
    "resources": True,
    "network": True,
    "services": True,
    "docker": True,
    "power": True,
    "gpu": False,
    "ollama": False,
    "footer": True,
}

# -- Layout --------------------------------------------------------

WIDE_LAYOUT_MIN_COLS: Final[int] = 80
HEADER_HEIGHT: Final[int] = 11
FOOTER_HEIGHT: Final[int] = 3
