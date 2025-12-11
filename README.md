# Kage - Agentic AI Extension for LivingArchive-clean

**Kage** is an **agentic AI extension** for LivingArchive-clean that performs autonomous, AI-driven port scanning.

## Overview

**Kage (Shadow)** is an autonomous port scanning daemon with **agentic AI decision-making** powered by LivingArchive-clean's LLM Gateway.

This version includes:
- ⚡ **Kage Port Scanner**: Fast socket-based and Nmap port scanning
- 🤖 **Agentic AI Extension**: Autonomous decision-making via LivingArchive-clean
- 🥚 **EggRecords Management**: Target management and tracking
- 🎯 **Intelligent Scanning**: AI-generated strategies and prioritization
- 🌐 **Flask Web Interface**: Simple dashboard for viewing scan results
- 💾 **SQLite Database**: Lightweight, no external database required

**Deprecated/Removed:**
- Kumo (HTTP Spider) - functionality removed
- Ryu (Threat Assessment) - functionality removed
- Kaze (High-speed Scanner) - functionality removed
- Suzu (Subdomain Discovery) - functionality removed
- Network learning and heuristics
- Advanced technique effectiveness tracking
- Multiple agent coordination

The Kage daemon runs as an independent process that communicates with a Django API server via HTTP.

## Features

- 🚀 **Standalone Daemons**: Independent processes with their own PIDs
- 🐳 **Docker Ready**: Full containerization support with health checks
- ⏸️ **Pause/Resume**: Control daemons without full restart
- 🔄 **Auto-Recovery**: Exponential backoff retry logic
- 🛑 **Graceful Shutdown**: Proper signal handling for clean stops
- 📊 **Health Checks**: Built-in health monitoring endpoints
- 🔌 **API-Based**: Clean separation via HTTP API

## Quick Start

### Prerequisites

- Python 3.13+
- Nmap installed (`apt-get install nmap` or `brew install nmap`)
- Django server running (for API communication)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd LivingArchive-Kage

# Install Flask dependencies
pip install -r requirements_flask.txt

# Start LivingArchive-clean gateway (required for agentic AI)
cd ../LivingArchive-clean
./quick_start.sh
# Gateway runs on http://localhost:8082

# Configure environment
export LLM_GATEWAY_URL="http://localhost:8082"
export KAGE_API_BASE="http://127.0.0.1:5000"
```

### Running Kage Daemon

```bash
# Start Kage daemon
python3 daemons/manage_daemons.py start kage

# Check status
python3 daemons/manage_daemons.py status

# Pause/Resume
python3 daemons/manage_daemons.py pause kage
python3 daemons/manage_daemons.py resume kage

# Stop
python3 daemons/manage_daemons.py stop kage
```

### Docker Deployment

```bash
cd docker

# Build and start all daemons
docker-compose up -d

# View logs
docker-compose logs -f kage-daemon

# Stop
docker-compose down
```

## Architecture

```
LivingArchive-Kage/
├── app.py             # Flask application (main entry point)
├── daemons/           # Daemon scripts (Kage only)
│   ├── kage_daemon.py
│   └── manage_daemons.py
├── kage/              # Kage (Port Scanner) source
│   ├── nmap_scanner.py
│   └── ...
├── templates/         # Flask/Jinja2 templates
│   └── reconnaissance/
│       ├── kage_dashboard.html
│       ├── dashboard.html
│       └── ...
├── static/            # Static files (CSS, JS)
├── kage.db            # SQLite database (created on first run)
├── docker/            # Docker configuration (optional)
│   ├── Dockerfile
│   └── docker-compose.yml (Kage only)
├── fallback_storage.py # Fallback storage system
└── requirements_flask.txt
```

![flow graph agent](https://github.com/CharlesMcGowen/LivingArchive-Kage/blob/master/images/agent_flow_graph.jpg)

**Deprecated/Removed:**
- `kumo/`, `suzu/`, `ryu/`, `kaze/` directories (moved to @trash/)
- Learning/heuristics functionality
- Network visualizer
- Monitoring dashboard
- Multi-agent coordination

## Running the Flask App

### Development
```bash
python app.py
```

The app will run on `http://localhost:5000`

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

Kage communicates with Flask via these endpoints:

- `GET /reconnaissance/api/daemon/kage/eggrecords/` - Get targets to process
- `POST /reconnaissance/api/daemon/kage/scan/` - Submit scan results
- `GET /reconnaissance/api/daemon/kage/health/` - Health check
- `GET /api/kage/status/` - Get Kage status
- `POST /api/kage/<action>/` - Control Kage (start/pause/kill)

**Note:** All endpoints are compatible with the Kage daemon. No daemon changes needed.

## Configuration

Environment variables:

```bash
# LivingArchive-clean LLM Gateway (required for agentic AI)
export LLM_GATEWAY_URL="http://localhost:8082"
export EGOLLAMA_API_KEY="your-api-key"  # Optional

# Kage configuration
export KAGE_SCAN_INTERVAL=30      # Seconds between scan cycles
export KAGE_MAX_SCANS=5            # Max scans per cycle
export KAGE_API_BASE="http://127.0.0.1:5000"  # Flask API base URL
```

## Agentic AI Features

Kage is an **extension for LivingArchive-clean** that enables autonomous AI decision-making:

- 🤖 **AI Target Prioritization** - Intelligently ranks targets by value/risk
- 🎯 **AI Strategy Generation** - Generates optimal Nmap arguments per target
- 📊 **AI Result Analysis** - Analyzes scan results for security insights
- 🔄 **Autonomous Decision-Making** - Decides next actions without human input

See `LIVINGARCHIVE_EXTENSION.md` and `EXTENSION_SETUP.md` for details.

## Signal Handling

- **SIGTERM/SIGINT**: Graceful shutdown (finishes current work)
- **SIGUSR1**: Pause daemon
- **SIGUSR2**: Resume daemon

## Docker Commands

```bash
# Start all
docker-compose up -d

# Pause daemon
docker kill --signal=SIGUSR1 recon-kage

# Resume daemon
docker kill --signal=SIGUSR2 recon-kage

# Stop gracefully
docker stop recon-kage

# View logs
docker logs -f recon-kage
```

## Agentic AI Extension

Kage extends **LivingArchive-clean** (LLM Gateway) to provide:
- Autonomous reconnaissance decision-making
- Intelligent target prioritization
- Context-aware scan strategy generation
- Result-driven adaptive behavior

**Prerequisites:**
- LivingArchive-clean gateway running on port 8082
- LLM model loaded in gateway

**See:**
- `LIVINGARCHIVE_EXTENSION.md` - Extension architecture and features
- `EXTENSION_SETUP.md` - Setup and configuration guide
- `AGENTIC_AI_INTEGRATION.md` - Technical integration details

## Development

This is an isolated version extracted from the main EgoWebs1 project. Kage works as a standalone Flask app with optional agentic AI extension via LivingArchive-clean.

## License

[Add your license here]

## Author

EGO Revolution

