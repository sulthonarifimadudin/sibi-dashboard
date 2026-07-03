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

# -- ASCII Logo (NeoFetch-style brain) -----------------------------

ASCII_LOGO: Final[str] = (
    "         .,;;;;;;,.\n"
    "      .;;;;;;;;;;;;;;\n"
    "    .;;;' .,,.  `;;;;\n"
    "   ;;;;  /:  :\\  ;;;;\n"
    "   ;;;;  \\:  :/  ;;;;    SIBI\n"
    "   `;;;.  `--'  .;;;'    LLM Server\n"
    "    `;;;;,    ,;;;;'\n"
    "      `;;;;;;;;;;'\n"
    "         `''''`"
)

# -- Services ------------------------------------------------------

SERVICES: Final[dict[str, dict[str, object]]] = {
    "Docker": {
        "port": None,
        "process": "dockerd",
        "icon": ">>",
    },
    "Portainer": {
        "port": 9443,
        "process": None,
        "icon": ">>",
    },
    "Ollama": {
        "port": 11434,
        "process": "ollama",
        "icon": ">>",
    },
    "Open WebUI": {
        "port": 3000,
        "process": None,
        "icon": ">>",
    },
    "PostgreSQL": {
        "port": 5432,
        "process": "postgres",
        "icon": ">>",
    },
    "Redis": {
        "port": 6379,
        "process": "redis-server",
        "icon": ">>",
    },
    "Nginx Proxy": {
        "port": 81,
        "process": None,
        "icon": ">>",
    },
    "ComfyUI": {
        "port": 8188,
        "process": None,
        "icon": ">>",
    },
    "MLflow": {
        "port": 5000,
        "process": None,
        "icon": ">>",
    },
    "Jupyter": {
        "port": 8888,
        "process": None,
        "icon": ">>",
    },
    "SSH": {
        "port": 22,
        "process": "sshd",
        "icon": ">>",
    },
    "Tailscale": {
        "port": None,
        "process": "tailscaled",
        "icon": ">>",
    },
}

# -- Ollama API ----------------------------------------------------

OLLAMA_API_URL: Final[str] = "http://localhost:11434"

# -- Public IP -----------------------------------------------------

PUBLIC_IP_URL: Final[str] = "https://api.ipify.org"
PUBLIC_IP_TIMEOUT: Final[float] = 3.0

# -- Power Estimation ---------------------------------------------
# Electricity rate in IDR per kWh (PLN tariff R-1/1300 VA)

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

