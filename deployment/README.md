DEVOPS DEPLOYMENT GUIDE
=======================

This folder contains scripts to build and deploy the Reflex application to an offline Windows Server 2019 environment.

## 1. Build Artifact (Online Machine)

Run `deployment/build_artifact.ps1` in PowerShell.
- Requirements: Internet access, PowerShell, Python 3 installed.
- Output: `dist/deployment_package.zip`
- Contents: Source code, `uv.exe`, `reflex_service.exe` (WinSW), `node` (Node.js binary), Python wheels (dependencies), configuration files.

## 2. Initial Deployment (Offline Server)

1. Transfer `deployment_package.zip` to the server.
2. Unzip to a temporary location or directly to target (e.g., `C:\Inetpub\wwwroot\ReflexPMT`).
3. Open PowerShell as Administrator.
4. Navigate to the `scripts` folder inside the package.
5. Run `.\deploy_initial.ps1`.
   - Bootstraps `uv`.
   - Creates virtualenv and installs dependencies offline.
   - Registers Windows Service.
   - Configures IIS Application `/pmt`.

## 3. Updates (Offline Server)

1. Transfer new `deployment_package.zip`.
2. Unzip and overwrite files in `C:\Inetpub\wwwroot\ReflexPMT` (preserve `app.db` if needed, script handles backup).
3. Run `scripts\deploy_update.ps1`.
   - Stops service.
   - Backups DB.
   - Updates code and dependencies.
   - Runs migrations.
   - Restarts service.

## Configuration Notes

### `rxconfig.py` Configuration for `/pmt`

To support the `/pmt` subpath, `rxconfig.py` must use the `api_url` setting.
The deployment scripts set `CI=1` which puts Reflex in production mode.

We recommend modifying `rxconfig.py` to read from environment variables or explicitly set:

```python
import reflex as rx
import os

# Ensure API URL handles the subpath
# When hosted at https://hcma.ds.susq.com/pmt, the API URL should be reachable.
# If IIS proxies /pmt to localhost:8000, and Reflex is serving everything,
# we need to ensure the frontend knows where to connect.

api_url = os.getenv("API_URL", "https://hcma.ds.susq.com/pmt")

config = rx.Config(
    app_name="app",
    api_url=api_url,
    deploy_url=api_url, # Ensure frontend assets are linked correctly if needed
    # ... other config ...
)
```

**Important:** The IIS `web.config` handles the reverse proxy. Ensure `WinSW` service is running on port 8000.

### Environment Variables

The `reflex_service.xml` sets:
- `CI=1` (Required for prod)
- `PMT_INTEGRATION_MODE=real` (Default for prod, change to `mock` if needed)
