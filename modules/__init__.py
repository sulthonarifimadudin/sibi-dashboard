"""
SIBI Dashboard -- Modules
~~~~~~~~~~~~~~~~~~~~~~~~~

Core modules for system monitoring, service detection,
and UI rendering.

Re-exports the public panel-builder API so that ``dashboard.py``
can do a single grouped import::

    from modules import build_header_panel, build_system_panel, ...

:copyright: (c) 2026 Sulthon
:license: MIT
"""

from modules.logo import build_header_panel
from modules.system import build_system_panel
from modules.docker import build_docker_panel
from modules.services import build_services_panel
from modules.network import build_network_panel
from modules.power import build_power_panel
from modules.widgets import (
    build_resource_panel,
    build_gpu_panel,
    build_ollama_panel,
    build_footer,
)

__all__: list[str] = [
    "build_header_panel",
    "build_system_panel",
    "build_docker_panel",
    "build_services_panel",
    "build_network_panel",
    "build_power_panel",
    "build_resource_panel",
    "build_gpu_panel",
    "build_ollama_panel",
    "build_footer",
]
