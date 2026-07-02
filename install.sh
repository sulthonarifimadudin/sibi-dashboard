#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#  SIBI Dashboard — Installer
# ═══════════════════════════════════════════════════════════════════
#
#  Usage:
#      chmod +x install.sh
#      ./install.sh
#
#  This script will:
#    1. Check for Python 3.12+
#    2. Create a virtual environment
#    3. Install dependencies
#    4. Verify the installation
#
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Colors ───────────────────────────────────────────────────────

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'  # No Color

# ── Functions ────────────────────────────────────────────────────

info()    { echo -e "${CYAN}[INFO]${NC}  $1"; }
success() { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()    { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }

header() {
    echo ""
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  SIBI Dashboard — Installer${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════${NC}"
    echo ""
}

# ── Pre-flight Checks ───────────────────────────────────────────

check_python() {
    info "Checking Python version…"

    if ! command -v python3 &> /dev/null; then
        fail "Python 3 is not installed. Please install Python 3.12+."
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 12 ]; }; then
        fail "Python 3.12+ is required (found $PYTHON_VERSION)."
    fi

    success "Python $PYTHON_VERSION detected."
}

# ── Virtual Environment ─────────────────────────────────────────

setup_venv() {
    local VENV_DIR=".venv"

    if [ -d "$VENV_DIR" ]; then
        warn "Virtual environment already exists at ./$VENV_DIR"
        info "Re-using existing environment."
    else
        info "Creating virtual environment…"
        python3 -m venv "$VENV_DIR"
        success "Virtual environment created at ./$VENV_DIR"
    fi

    info "Activating virtual environment…"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    success "Virtual environment activated."
}

# ── Install Dependencies ────────────────────────────────────────

install_deps() {
    info "Upgrading pip…"
    pip install --upgrade pip --quiet

    info "Installing dependencies from requirements.txt…"
    pip install -r requirements.txt --quiet
    success "All dependencies installed."
}

# ── Verify ───────────────────────────────────────────────────────

verify_install() {
    info "Verifying installation…"

    python3 -c "
import rich, psutil, requests
print(f'  rich     {rich.__version__}')
print(f'  psutil   {psutil.__version__}')
print(f'  requests {requests.__version__}')
"
    # docker is optional (requires Docker daemon)
    python3 -c "import docker; print(f'  docker   {docker.__version__}')" 2>/dev/null \
        || warn "docker SDK installed but Docker daemon may not be running."

    success "Installation verified."
}

# ── Post-install ─────────────────────────────────────────────────

post_install() {
    echo ""
    echo -e "${BOLD}${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${GREEN}  ✔ Installation Complete!${NC}"
    echo -e "${BOLD}${GREEN}═══════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${BOLD}Quick Start:${NC}"
    echo ""
    echo -e "    ${CYAN}source .venv/bin/activate${NC}"
    echo -e "    ${CYAN}python dashboard.py${NC}"
    echo ""
    echo -e "  ${BOLD}Watch Mode (auto-refresh):${NC}"
    echo ""
    echo -e "    ${CYAN}python dashboard.py --watch${NC}"
    echo ""
}

# ── Main ─────────────────────────────────────────────────────────

main() {
    header
    check_python
    setup_venv
    install_deps
    verify_install
    post_install
}

main "$@"
