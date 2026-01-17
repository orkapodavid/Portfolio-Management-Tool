# DevOps Deployment Guide

This folder contains scripts to build and deploy the Reflex application to an offline Windows Server 2019 environment with IIS.

## Prerequisites

Before deployment, ensure the target server has:

### Required Windows Features
```powershell
Install-WindowsFeature -Name Web-Server, Web-WebSockets, Web-Asp-Net45, Web-Mgmt-Console
```

### Required IIS Modules
- **URL Rewrite Module** - [Download](https://www.iis.net/downloads/microsoft/url-rewrite)
- **Application Request Routing (ARR)** - [Download](https://www.iis.net/downloads/microsoft/application-request-routing)

### Software Cache (`C:\Apps\Software`)
Place these files in `C:\Apps\Software` on both build and target machines:
- `uv.exe` - [Download](https://github.com/astral-sh/uv/releases)
- `WinSW-x64.exe` - [Download](https://github.com/winsw/winsw/releases)
- `node.exe` - [Download](https://nodejs.org/dist/) (win-x64)
- URL Rewrite installer (for offline servers)
- ARR installer (for offline servers)

## Deployment Scripts

| Script | Purpose |
|--------|---------|
| `build_artifact.ps1` | Creates offline deployment package (run on ONLINE machine) |
| `verify_prereqs.ps1` | Verifies all prerequisites before deployment |
| `deploy_initial.ps1` | First-time deployment to target server |
| `deploy_update.ps1` | Updates existing deployment |
| `deploy_rollback.ps1` | Rolls back to a previous version |

---

## 1. Build Artifact (Online Machine)

Run on a machine with internet access:

```powershell
cd deployment
.\build_artifact.ps1
```

**Requirements:**
- Internet access
- PowerShell 5.1+
- Python 3.11+ installed
- Node.js installed (for frontend export)
- Reflex installed (`pip install reflex`)

**Output:** `dist/deployment_package.zip`

**Contents:**
- `app/` - Application source code
- `wheels/` - Python dependencies (pre-downloaded)
- `frontend_static/` - Pre-built frontend assets
- `uv.exe` - Python package manager
- `reflex_service.exe` - WinSW service wrapper
- `config/` - IIS and service configuration files
- `scripts/` - Deployment scripts

---

## 2. Verify Prerequisites (Target Server)

Before initial deployment, verify the server is ready:

```powershell
.\verify_prereqs.ps1
```

This checks:
- Windows features installed
- IIS modules (URL Rewrite, ARR)
- Software cache contents
- Python availability
- Port availability (80, 8000)
- IIS Default Web Site status

---

## 3. Initial Deployment (Offline Server)

1. Transfer `deployment_package.zip` to the server
2. Extract to temporary location
3. Open PowerShell **as Administrator**
4. Navigate to the extracted `scripts` folder
5. Run:

```powershell
.\deploy_initial.ps1
```

**What it does:**
1. Verifies IIS prerequisites (URL Rewrite, ARR)
2. Enables ARR proxy
3. Creates application directory
4. Creates Python virtual environment
5. Installs dependencies offline
6. Initializes database
7. Deploys static frontend
8. Registers Windows Service (WinSW)
9. Configures IIS application `/pmt`
10. Starts service and verifies

---

## 4. Updates (Offline Server)

1. Transfer new `deployment_package.zip`
2. Extract to the existing `C:\Inetpub\wwwroot\ReflexPMT` folder
3. Run:

```powershell
.\scripts\deploy_update.ps1
```

**What it does:**
1. Stops the backend service
2. Backs up database (timestamped)
3. Creates version backup (for rollback)
4. Updates application files
5. Updates Python dependencies
6. Runs database migrations
7. Updates frontend static files
8. Restarts service
9. Performs health check

---

## 5. Rollback

If an update causes issues:

```powershell
.\scripts\deploy_rollback.ps1
```

This interactive script:
1. Lists available backups with timestamps
2. Lets you select which version to restore
3. Stops service, restores files, restarts service

---

## Configuration Files

### `rxconfig.py`

To support the `/pmt` subpath, configure:

```python
import reflex as rx
import os

api_url = os.getenv("API_URL", "https://hcma.ds.susq.com/pmt")

config = rx.Config(
    app_name="app",
    api_url=api_url,
    deploy_url=api_url,
)
```

### `reflex_service.xml` (WinSW)

Configures the Windows Service:
- Runs backend on port 8000
- Logs to `%BASE%\logs\` with rotation
- Auto-restarts on failure
- Delayed auto-start after boot

### `web.config` (IIS)

Configures IIS:
- WebSocket proxy for `_event` endpoint
- HTTP proxy for `_upload`, `ping`, `_image`
- SPA fallback to `index.html`
- MIME types for JSON and fonts
- Security headers

---

## Environment Variables

The `reflex_service.xml` sets:

| Variable | Value | Description |
|----------|-------|-------------|
| `CI` | `1` | Production mode |
| `API_URL` | `https://hcma.ds.susq.com/pmt` | Frontend API endpoint |
| `PMT_INTEGRATION_MODE` | `real` | Integration mode (use `mock` for testing) |

---

## Troubleshooting

### Service won't start
```powershell
# Check service status
Get-Service reflex_service

# View logs
Get-Content C:\Inetpub\wwwroot\ReflexPMT\logs\reflex_service.*.log -Tail 100

# Manually run to see errors
cd C:\Inetpub\wwwroot\ReflexPMT
.\.venv\Scripts\python.exe -m reflex run --backend-only --backend-port 8000
```

### WebSocket connection fails
1. Ensure ARR is installed and proxy is enabled
2. Check IIS has WebSocket Protocol feature
3. Verify `web.config` is in the `public` folder

### 502 Bad Gateway
1. Verify backend service is running on port 8000
2. Check if firewall blocks localhost:8000
3. Ensure ARR proxy is enabled:
```powershell
Set-WebConfigurationProperty -Filter "system.webServer/proxy" -Name "enabled" -Value "true" -PSPath "IIS:\"
```

### Frontend loads but no data
1. Check browser DevTools Network tab for WebSocket errors
2. Verify `_event` requests reach the backend
3. Check backend logs for exceptions

---

## Directory Structure (Post-Deployment)

```
C:\Inetpub\wwwroot\ReflexPMT\
├── app/                    # Python application code
├── assets/                 # Application assets
├── backups/                # Version backups for rollback
│   └── 20260116153000/     # Timestamped backup
├── config/                 # Configuration files
│   ├── reflex_service.xml
│   └── web.config
├── frontend_static/        # Original frontend build
├── logs/                   # Service logs
├── public/                 # IIS serves from here
│   ├── index.html
│   ├── _next/
│   └── web.config
├── scripts/                # Deployment scripts
├── wheels/                 # Python packages
├── .venv/                  # Python virtual environment
├── reflex_service.exe      # WinSW executable
├── reflex_service.xml      # Service config (copy)
├── requirements.txt        # Python dependencies
├── rxconfig.py             # Reflex config
├── pyproject.toml          # Project metadata
└── uv.exe                  # Python package manager
```
