<div align="center">

```
 █████╗ ██╗
██╔══██╗██║
███████║██║
██╔══██║██║
██║  ██║██║
╚═╝  ╚═╝╚═╝
```

# SIBI Dashboard

**Enterprise AI Server Monitoring Dashboard**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Rich](https://img.shields.io/badge/Rich-Terminal_UI-58A6FF?style=for-the-badge)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-3FB950?style=for-the-badge)](LICENSE)

A premium, terminal-based server dashboard inspired by **btop**, **htop**, **fastfetch**, **neofetch**, and **lazydocker**.
Built with [Rich](https://github.com/Textualize/rich) for beautiful, dark-terminal-optimized output.

</div>

---

## ✨ Features

| Category | Details |
|----------|---------|
| **System Info** | Hostname, OS, kernel, architecture, CPU model/cores/threads, memory, disk, uptime, boot time, shell, Python version |
| **Resource Bars** | CPU %, memory %, disk %, swap %, temperature, load average, network I/O, battery — all with adaptive colour coding (green / yellow / red) |
| **Network** | LAN IP, Tailscale IP, public IP, hostname, gateway, DNS, internet status |
| **Services** | Auto-detect 12 services: Docker, Portainer, Ollama, Open WebUI, PostgreSQL, Redis, Nginx Proxy Manager, ComfyUI, MLflow, Jupyter, SSH, Tailscale |
| **Docker** | Running/stopped containers, images, volumes, networks + running container table |
| **GPU** | NVIDIA driver, CUDA, GPU name, temperature, VRAM usage, GPU utilisation |
| **Ollama** | Installed models, running models, model sizes |
| **Adaptive Layout** | Two-column layout on wide terminals (≥120 cols), single-column stacked layout on narrower terminals |
| **Watch Mode** | `--watch` flag for continuous 2-second refresh via Rich Live |

---

## 📸 Screenshots

> **TODO**: Add terminal screenshots here.
>
> ```
> python dashboard.py
> ```

---

## 📦 Installation

### Prerequisites

- **Python 3.12+**
- **pip** (Python package manager)

### Quick Install (Linux / macOS)

```bash
# Clone the repository
git clone https://github.com/your-username/sibi-dashboard.git
cd sibi-dashboard

# Run the installer
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
# Clone
git clone https://github.com/your-username/sibi-dashboard.git
cd sibi-dashboard

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
git clone https://github.com/your-username/sibi-dashboard.git
cd sibi-dashboard

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## 🚀 Usage

### One-shot Render

```bash
python dashboard.py
```

### Watch Mode (auto-refresh)

```bash
python dashboard.py --watch
```

### Custom Refresh Interval

```bash
python dashboard.py --watch --interval 5
```

### Version

```bash
python dashboard.py --version
```

---

## ⚙️ Configuration

All configuration lives in [`config.py`](config.py):

| Setting | Description | Default |
|---------|-------------|---------|
| `DASHBOARD_TITLE` | Title shown in header | `"SIBI Dashboard"` |
| `DASHBOARD_VERSION` | Semantic version | `"1.0.0"` |
| `USER_NAME` | Greeting name in footer | `"Sulthon"` |
| `REFRESH_INTERVAL` | Watch mode interval (sec) | `2.0` |
| `SERVICES` | Services to detect (port + process) | 12 services |
| `OLLAMA_API_URL` | Ollama API base URL | `http://localhost:11434` |
| `ENABLED_PANELS` | Toggle panels on/off | All `True` |
| `WIDE_LAYOUT_MIN_COLS` | Min terminal width for 2-col layout | `120` |

### Theme

All colours are centralised in [`theme.py`](theme.py).
The palette uses a **GitHub Dark**-inspired scheme with:

- Cyan accents (`#58a6ff`)
- Purple labels (`#bc8cff`)
- Green / yellow / red progress bar thresholds
- Muted borders (`#30363d`)

---

## 📁 Project Structure

```
sibi-dashboard/
├── dashboard.py          # Main entry point
├── config.py             # Central configuration
├── theme.py              # Colour palette & Rich Theme
├── install.sh            # Automated installer (bash)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── modules/
│   ├── __init__.py       # Package re-exports
│   ├── helpers.py        # Utility functions
│   ├── logo.py           # ASCII art header panel
│   ├── system.py         # System info collection (psutil)
│   ├── network.py        # Network info (IPs, gateway, DNS)
│   ├── services.py       # Service auto-detection
│   ├── docker.py         # Docker monitoring (SDK)
│   └── widgets.py        # Resource bars, GPU, Ollama, footer
├── assets/               # Static assets
└── themes/               # Additional colour themes (future)
```

---

## 🗺️ Roadmap

- [ ] **Theme switcher** — load themes from `themes/` directory
- [ ] **Per-core CPU bars** — individual progress bars per CPU core
- [ ] **Network traffic rate** — real-time upload/download speed (not totals)
- [ ] **Disk I/O** — read/write throughput
- [ ] **Process list** — top processes by CPU/memory
- [ ] **Log viewer** — tail system logs in a panel
- [ ] **Remote mode** — connect to remote servers via SSH
- [ ] **Export** — save snapshot as HTML/PNG
- [ ] **Plugin system** — user-defined custom panels
- [ ] **Configuration file** — TOML/YAML config support

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by Sulthon**

*Powered by [Rich](https://github.com/Textualize/rich) • [psutil](https://github.com/giampaolo/psutil) • [Docker SDK](https://docker-py.readthedocs.io/)*

</div>
