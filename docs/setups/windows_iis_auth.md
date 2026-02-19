# Windows Authentication for PMT (Reflex App) — Implementation Plan

> **Status**: Approved approach — ready for implementation  
> **Date**: 2026-02-12  
> **Target**: Windows Server 2019, IIS 10.0  
> **Approach**: HttpPlatformHandler + `forwardWindowsAuthToken`  
> **Goal**: Transparent SSO → identify Windows user → control page visibility and user actions per role  
> **Alternatives**: See [alternative_auth_approaches.md](./alternative_auth_approaches.md)

---

## Table of Contents

1. [Architecture](#1-architecture)
2. [IIS Setup (Step-by-Step)](#2-iis-setup-step-by-step)
3. [Local Development Mode](#3-local-development-mode)
4. [Python Token Decoding](#4-python-token-decoding)
5. [Reflex Integration](#5-reflex-integration)
6. [User Page Visibility Control](#6-user-page-visibility-control)
7. [User Action Control](#7-user-action-control)
8. [WebSocket Session Strategy](#8-websocket-session-strategy)
9. [Security Considerations](#9-security-considerations)
10. [File Changes Summary](#10-file-changes-summary)
11. [Next Steps Checklist](#11-next-steps-checklist)

---

## 1. Architecture

### Production (IIS + HttpPlatformHandler)

```
┌────────────────────────────────────────────────────────┐
│                 Browser (Intranet)                      │
│  Domain user auto-authenticates (Negotiate/NTLM/Kerb.) │
└─────────────────────┬──────────────────────────────────┘
                      │  HTTP + WebSocket
                      ▼
┌────────────────────────────────────────────────────────┐
│              IIS 10.0 (Server 2019)                     │
│                                                         │
│  1. Windows Authentication enabled (Anonymous OFF)      │
│  2. HttpPlatformHandler manages the Python process      │
│  3. forwardWindowsAuthToken="true"                      │
│  4. Passes MS-ASPNETCORE-WINAUTHTOKEN header            │
│  5. WebSocket Protocol feature enabled                  │
└─────────────────────┬──────────────────────────────────┘
                      │  localhost:%HTTP_PLATFORM_PORT%
                      ▼
┌────────────────────────────────────────────────────────┐
│              Reflex App (Python)                        │
│                                                         │
│  FastAPI middleware:                                     │
│    → Decodes token via pywin32 → gets DOMAIN\username   │
│    → Sets signed session cookie                         │
│                                                         │
│  AuthState / Permissions pipeline (shared with dev)     │
└────────────────────────────────────────────────────────┘
```

### Local Development (No IIS)

```
┌────────────────────────────────────────────────────────┐
│                 Browser (localhost)                      │
│  No auth challenge — dev mode auto-assigns identity     │
└─────────────────────┬──────────────────────────────────┘
                      │  HTTP + WebSocket
                      ▼
┌────────────────────────────────────────────────────────┐
│              Reflex App (uv run reflex run)             │
│                                                         │
│  PMT_AUTH_MODE=dev                                      │
│  PMT_DEV_USER=DOMAIN\jsmith  (configurable)             │
│  PMT_DEV_ROLE=admin          (configurable)             │
│                                                         │
│  FastAPI middleware:                                     │
│    → Skips token decoding                               │
│    → Uses dev user from env vars                        │
│    → Same cookie + AuthState pipeline as production     │
└────────────────────────────────────────────────────────┘
```

> [!TIP]
> **Dev mode and prod mode share the same AuthState, permissions, page guards, and action controls.** Only the identity source differs. This means you can develop and test RBAC features locally without IIS.

### Why HttpPlatformHandler?

| Benefit | Detail |
|:---|:---|
| **Fully built-in** | Ships with IIS on Server 2019 (v1.2) |
| **No third-party** | Only pip dependency is `pywin32` |
| **Transparent SSO** | Zero login prompts for domain users |
| **No header spoofing** | Token is a kernel handle, not a string |
| **Simpler deployment** | IIS manages the Python process lifecycle |
| **No C# code** | Unlike the reverse proxy + HTTP module approach |

---

## 2. IIS Setup (Step-by-Step)

### 2.1. Prerequisites

| Component | How to verify / install |
|:---|:---|
| IIS 10.0 | Server Manager → Add Roles → Web Server (IIS) |
| Windows Authentication | Server Manager → Web Server → Security → Windows Authentication |
| WebSocket Protocol | Server Manager → Web Server → Application Development → WebSocket Protocol |
| HttpPlatformHandler v1.2 | Check `%windir%\System32\inetsrv\config\schema\httpplatform_schema.xml` exists. If missing, download from [IIS.net](https://www.iis.net/downloads/microsoft/httpplatformhandler) or use the [HTTP Bridge Module](https://github.com/nickcimino/http-bridge-module) as a drop-in replacement |
| Python 3.9+ | Must be installed on the server. Note the full path (e.g., `C:\Python312\python.exe`) |
| `pywin32` | `pip install pywin32` in the deployment environment |

### 2.2. Create IIS Website

```
1. Open IIS Manager
2. Right-click "Sites" → "Add Website..."
3. Site name: PMT
4. Physical path: D:\Apps\PMT (or wherever the Reflex app lives)
5. Binding: http, port 80 (or your desired port)
6. Host name: pmt.yourdomain.com (optional)
```

### 2.3. Configure Application Pool

```
1. In IIS Manager → Application Pools → select "PMT" pool
2. Set ".NET CLR Version" → "No Managed Code"
3. Advanced Settings:
   - Enable 32-Bit Applications: False (assuming 64-bit Python)
   - Identity: NetworkService or a domain service account
4. Ensure the pool identity has read/execute permissions on the app directory
```

### 2.4. Configure Authentication

```
1. Select the PMT site → double-click "Authentication"
2. Disable: Anonymous Authentication
3. Enable: Windows Authentication
4. Click "Providers..." → ensure order is: Negotiate, NTLM
   (Negotiate first = prefer Kerberos, fall back to NTLM)
```

### 2.5. Create web.config

Place this in the root of your Reflex app directory:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>

    <!-- Authentication -->
    <security>
      <authentication>
        <anonymousAuthentication enabled="false" />
        <windowsAuthentication enabled="true" />
      </authentication>
    </security>

    <!-- HttpPlatformHandler -->
    <handlers>
      <add name="httpPlatformHandler"
           path="*" verb="*"
           modules="httpPlatformHandler"
           resourceType="Unspecified" />
    </handlers>

    <httpPlatform processPath="C:\Python312\python.exe"
                  arguments="-m uvicorn app.app:app --host 127.0.0.1 --port %HTTP_PLATFORM_PORT%"
                  stdoutLogEnabled="true"
                  stdoutLogFile=".\logs\stdout"
                  startupTimeLimit="120"
                  requestTimeout="00:05:00"
                  forwardWindowsAuthToken="true">
      <environmentVariables>
        <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
        <environmentVariable name="PYTHONPATH" value="D:\Apps\PMT" />
      </environmentVariables>
    </httpPlatform>

    <!-- Enable WebSockets -->
    <webSocket enabled="true" />

  </system.webServer>
</configuration>
```

> [!IMPORTANT]
> The `processPath` and `arguments` must match your actual Python installation and Reflex startup command. The `%HTTP_PLATFORM_PORT%` is dynamically assigned by IIS — your app must listen on this port.

### 2.6. Reflex Port Configuration

Reflex needs to listen on the port IIS assigns. In `rxconfig.py`:

```python
import os

config = rx.Config(
    app_name="app",
    # Use the IIS-assigned port, or default to 8000 for local dev
    backend_port=int(os.environ.get("PORT", "8000")),
)
```

---

## 3. Local Development Mode

When running `uv run reflex run` locally (no IIS), the auth system must still work so you can develop pages, test RBAC, and iterate on the UI.

### 3.1. Environment Variables

Set these in your `.env` file, shell, or IDE run configuration:

```bash
# .env (local development — DO NOT commit to git)
PMT_AUTH_MODE=dev
PMT_DEV_USER=YOURPC\yourusername
PMT_DEV_ROLE=admin
```

| Variable | Values | Default | Purpose |
|:---|:---|:---|:---|
| `PMT_AUTH_MODE` | `dev` / `iis` | `iis` | Toggle between dev mock and IIS token decoding |
| `PMT_DEV_USER` | Any string | `DEV\developer` | Mock username used in dev mode |
| `PMT_DEV_ROLE` | `admin`, `trader`, `risk`, `ops`, `readonly` | `admin` | Mock role — lets you test any permission level |

> [!TIP]
> Set `PMT_DEV_ROLE=readonly` to quickly test what a restricted user sees. Switch to `trader`, `ops`, etc. to verify page guards and action controls for each role.

### 3.2. How Dev Mode Works

The middleware detects `PMT_AUTH_MODE=dev` and skips all IIS/Windows token logic:

```python
# Simplified flow in dev mode
if AUTH_MODE == "dev":
    username = os.environ.get("PMT_DEV_USER", "DEV\\developer")
    # Skip token decoding entirely
    # Set the same signed cookie as production
    # AuthState loads from cookie identically
```

Everything downstream — AuthState, page guards, `rx.cond`, action permissions — works **identically** in both modes. You're only swapping the identity source.

### 3.3. Dev Mode Safety

> [!CAUTION]
> Dev mode **must never** be active in production. The middleware logs a loud warning at startup and refuses to activate if `PMT_AUTH_MODE=dev` is set alongside IIS-specific env vars (like `HTTP_PLATFORM_PORT`).

```python
# Safety check in middleware
if AUTH_MODE == "dev" and os.environ.get("HTTP_PLATFORM_PORT"):
    raise RuntimeError(
        "FATAL: PMT_AUTH_MODE=dev detected in IIS environment! "
        "Remove PMT_AUTH_MODE or set it to 'iis'."
    )

if AUTH_MODE == "dev":
    logger.warning(
        "⚠️  AUTH DEV MODE ACTIVE — using mock user '%s' with role '%s'. "
        "DO NOT use in production!",
        DEV_USER, DEV_ROLE,
    )
```

### 3.4. Quick Start (Local Dev)

```bash
# 1. Set env vars (PowerShell)
$env:PMT_AUTH_MODE = "dev"
$env:PMT_DEV_USER = "MYPC\myname"
$env:PMT_DEV_ROLE = "admin"       # or: trader, risk, ops, readonly

# 2. Run Reflex normally
uv run reflex run

# 3. Open http://localhost:3000 — you're "logged in" as the mock user
#    Page guards, nav filtering, and action controls all work
```

Alternatively, add a `.env` file at the repo root and load it with `python-dotenv`:

```python
# In app/middleware/auth_middleware.py (top of file)
try:
    from dotenv import load_dotenv
    load_dotenv()  # reads .env from repo root
except ImportError:
    pass  # dotenv not installed — fine for prod
```

### 3.5. `.env` File (Git-Ignored)

Add to `.gitignore`:

```gitignore
# Auth dev mode
.env
```

Provide a `.env.example` for onboarding:

```bash
# .env.example — copy to .env and customize
PMT_AUTH_MODE=dev
PMT_DEV_USER=DEV\developer
PMT_DEV_ROLE=admin
AUTH_SECRET=change-me-in-production
```

### 3.6. Testing Different Roles Locally

To test what each role sees, just change the env var and reload:

```bash
# Test as trader (sees PnL, Positions, Orders, etc.)
$env:PMT_DEV_ROLE = "trader"
# Restart Reflex or refresh browser

# Test as ops (sees Recon, Operations, Compliance, etc.)
$env:PMT_DEV_ROLE = "ops"

# Test as readonly (sees only PnL, Market Data)
$env:PMT_DEV_ROLE = "readonly"
```

> [!NOTE]
> If your role-to-user mapping lives in `USER_ROLES` dict, dev mode bypasses it and uses `PMT_DEV_ROLE` directly. This lets you test any role without needing matching usernames.

---

## 4. Python Token Decoding

### 4.1. How the Token Arrives

> [!NOTE]
> This section only applies in **production** (`PMT_AUTH_MODE=iis`). In dev mode, token decoding is skipped entirely.

When `forwardWindowsAuthToken="true"`, IIS sends the header:

```
MS-ASPNETCORE-WINAUTHTOKEN: <hex-encoded token handle>
```

This is a **Windows kernel token handle** (integer) — not a username string. The Python process must decode it using Win32 APIs.

### 4.2. Token Decoder Utility (Conceptual)

```python
# app/utils/windows_auth.py
import ctypes
import win32security
import logging

logger = logging.getLogger(__name__)

def decode_windows_token(token_hex: str) -> str | None:
    """
    Decode MS-ASPNETCORE-WINAUTHTOKEN header to DOMAIN\\username.

    Args:
        token_hex: Hex string from the MS-ASPNETCORE-WINAUTHTOKEN header

    Returns:
        "DOMAIN\\username" or None if decoding fails
    """
    try:
        # Convert hex string to integer handle
        handle_int = int(token_hex, 16)

        # Get token user information (returns (SID, attributes) tuple)
        token_user = win32security.GetTokenInformation(
            handle_int, win32security.TokenUser
        )
        sid = token_user[0]

        # Look up the account name from the SID
        username, domain, _ = win32security.LookupAccountSid(None, sid)

        return f"{domain}\\{username}"

    except Exception as e:
        logger.error(f"Failed to decode Windows auth token: {e}")
        return None

    finally:
        # CRITICAL: Close the handle to prevent resource leaks
        try:
            ctypes.windll.kernel32.CloseHandle(handle_int)
        except Exception:
            pass
```

> [!CAUTION]
> You **must** call `CloseHandle` on the token handle after use. Failing to do so will leak kernel handles and eventually crash the process.

### 4.3. Dependencies

```
pip install pywin32
```

- `pywin32` is well-maintained and widely used for Windows API access
- Only works on Windows (which is fine — this is a Server 2019 deployment)
- **Not needed for local development** — dev mode doesn't call any Win32 APIs

> [!TIP]
> You can make `pywin32` a conditional dependency so it doesn't break installs on non-Windows dev machines:
> ```toml
> # pyproject.toml
> [project.optional-dependencies]
> iis = ["pywin32"]
> ```
> Install in prod: `pip install .[iis]`  
> Install in dev: `pip install .` (no pywin32 needed)

---

## 5. Reflex Integration

### 5.1. FastAPI Middleware via `api_transformer`

This middleware runs on every HTTP request and sets a signed cookie with the authenticated username. **It supports both production (IIS) and local development modes.**

```python
# app/middleware/auth_middleware.py  (conceptual)
from fastapi import FastAPI, Request, Response
from itsdangerous import URLSafeTimedSerializer
import os
import logging

# Optional: load .env for local dev
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# --- Configuration ---
AUTH_MODE = os.environ.get("PMT_AUTH_MODE", "iis")  # "dev" or "iis"
AUTH_SECRET = os.environ.get("AUTH_SECRET", "change-me-in-production")
COOKIE_NAME = "pmt_session"
COOKIE_MAX_AGE = 28800  # 8 hours (trading day)

# Dev mode settings
DEV_USER = os.environ.get("PMT_DEV_USER", "DEV\\developer")
DEV_ROLE = os.environ.get("PMT_DEV_ROLE", "admin")

serializer = URLSafeTimedSerializer(AUTH_SECRET)

# --- Safety check ---
if AUTH_MODE == "dev" and os.environ.get("HTTP_PLATFORM_PORT"):
    raise RuntimeError(
        "FATAL: PMT_AUTH_MODE=dev detected in IIS environment! "
        "Remove PMT_AUTH_MODE or set it to 'iis'."
    )
if AUTH_MODE == "dev":
    logger.warning(
        "⚠️  AUTH DEV MODE — mock user '%s' role '%s'. DO NOT use in production!",
        DEV_USER, DEV_ROLE,
    )

# --- Token decoder (only imported in production) ---
if AUTH_MODE == "iis":
    from app.utils.windows_auth import decode_windows_token

auth_api = FastAPI()


def _resolve_username(request: Request) -> str | None:
    """Resolve username from token (prod) or env var (dev)."""
    if AUTH_MODE == "dev":
        return DEV_USER

    # Production: decode IIS Windows auth token
    token_header = request.headers.get("MS-ASPNETCORE-WINAUTHTOKEN")
    if token_header:
        return decode_windows_token(token_header)
    return None


@auth_api.middleware("http")
async def windows_auth_middleware(request: Request, call_next):
    # Check if user already has a valid session cookie
    session_cookie = request.cookies.get(COOKIE_NAME)
    username = None

    if session_cookie:
        try:
            username = serializer.loads(session_cookie, max_age=COOKIE_MAX_AGE)
        except Exception:
            username = None  # expired or tampered

    # If no valid cookie, resolve the username
    if not username:
        username = _resolve_username(request)

    response = await call_next(request)

    # Set/refresh the session cookie if we have a username
    if username and not session_cookie:
        signed_value = serializer.dumps(username)
        response.set_cookie(
            key=COOKIE_NAME,
            value=signed_value,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="strict",
            # secure=True,  # Enable when using HTTPS
        )

    return response
```

### 5.2. Wire Up in app.py

```python
# In app/app.py — add these lines
from app.middleware.auth_middleware import auth_api

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
    stylesheets=[...],
    api_transformer=auth_api,  # ← inject the middleware (works in both dev and prod)
)
```

### 5.3. AuthState

```python
# app/states/auth/auth_state.py  (conceptual)
import reflex as rx
from itsdangerous import URLSafeTimedSerializer
import os

AUTH_SECRET = os.environ.get("AUTH_SECRET", "change-me-in-production")
AUTH_MODE = os.environ.get("PMT_AUTH_MODE", "iis")
COOKIE_NAME = "pmt_session"
COOKIE_MAX_AGE = 28800

serializer = URLSafeTimedSerializer(AUTH_SECRET)

ALL_MODULES = [
    "PnL", "Positions", "Market Data", "Orders", "Instruments",
    "Risk", "Recon", "Operations", "Compliance", "Events", "Portfolio Tools",
]

# Role → permitted modules mapping
ROLE_PERMISSIONS: dict[str, list[str]] = {
    "trader":   ["PnL", "Positions", "Market Data", "Orders", "Instruments"],
    "risk":     ["PnL", "Positions", "Risk", "Market Data", "Instruments"],
    "ops":      ["Recon", "Operations", "Compliance", "Events", "Portfolio Tools"],
    "admin":    ["*"],  # all modules
    "readonly": ["PnL", "Market Data"],  # view-only access
}

# Username → role mapping (could be config file, DB, or AD group lookup)
USER_ROLES: dict[str, str] = {
    "DOMAIN\\jsmith":   "trader",
    "DOMAIN\\riskteam": "risk",
    "DOMAIN\\opsteam":  "ops",
    "DOMAIN\\admin":    "admin",
}


def _resolve_role(username: str) -> str:
    """Resolve role for a given username. Dev mode uses env var override."""
    if AUTH_MODE == "dev":
        # In dev mode, PMT_DEV_ROLE overrides any lookup
        return os.environ.get("PMT_DEV_ROLE", "admin")
    return USER_ROLES.get(username, "readonly")


class AuthState(rx.State):
    """Manages authenticated user identity and permissions.

    Works identically in both dev and prod modes — only the identity
    source differs (env var vs. IIS token → cookie).
    """

    current_user: str = ""          # "DOMAIN\\username" — visible to frontend
    user_role: str = ""             # "trader", "risk", etc.
    allowed_modules: list[str] = []
    is_authenticated: bool = False
    auth_mode: str = AUTH_MODE      # exposed so UI can show dev banner

    _session_token: str = ""        # backend-only — never sent to browser

    @rx.event
    def load_user_from_cookie(self):
        """Called on_load for every page. Reads the session cookie."""
        cookie_value = self.router.headers.get("cookie", "")
        username = _extract_username_from_cookie(cookie_value)

        if username:
            self.current_user = username
            self.is_authenticated = True
            self.user_role = _resolve_role(username)
            perms = ROLE_PERMISSIONS.get(self.user_role, [])
            self.allowed_modules = perms if perms != ["*"] else list(ALL_MODULES)
        else:
            self.is_authenticated = False
            self.current_user = ""
            self.user_role = ""
            self.allowed_modules = []
        self.auth_mode = AUTH_MODE

    @rx.event
    def check_module_access(self, module_name: str):
        """Page guard — redirect if user lacks access to this module."""
        if not self.is_authenticated:
            return rx.redirect("/unauthorized")
        if "*" not in self.allowed_modules and module_name not in self.allowed_modules:
            return rx.redirect("/unauthorized")

    @rx.var
    def can_access_module(self) -> bool:
        """Computed var for UI conditional rendering."""
        return self.is_authenticated

    @rx.var
    def display_name(self) -> str:
        """Short display name (without domain prefix)."""
        if "\\" in self.current_user:
            return self.current_user.split("\\")[1]
        return self.current_user or "Unknown"

    @rx.var
    def is_dev_mode(self) -> bool:
        """True when running in dev mode (for UI dev banner)."""
        return self.auth_mode == "dev"
```

### 5.4. Dev Mode UI Banner (Optional)

Show a visible indicator when dev mode is active to avoid confusion:

```python
def dev_mode_banner():
    return rx.cond(
        AuthState.is_dev_mode,
        rx.box(
            rx.text(
                f"🔧 DEV MODE — {AuthState.display_name} ({AuthState.user_role})",
                size="1",
                color="white",
            ),
            background="orange",
            padding="4px 12px",
            text_align="center",
            width="100%",
        ),
    )
```

---

## 6. User Page Visibility Control

### 6.1. Strategy Overview

Page visibility is controlled at **three levels**:

```
Level 1: on_load guard   → Redirect unauthorized users before page renders
Level 2: rx.cond         → Hide/show UI components based on role
Level 3: Navigation      → Only show menu items the user can access
```

> [!IMPORTANT]
> **Level 1 is mandatory.** `rx.cond` (Level 2) only hides HTML visually — the content is still in the page source. True protection requires the `on_load` redirect and backend data validation.

### 6.2. Level 1: `on_load` Page Guards

Add `AuthState.check_module_access` to every route's `on_load` list:

```python
# In app/app.py — modify existing routes
app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    on_load=[
        AuthState.load_user_from_cookie,           # ← NEW: load identity
        AuthState.check_module_access("PnL"),       # ← NEW: check permission
        PnLState.load_pnl_change_data,
        lambda: PnLState.set_pnl_subtab("PnL Change"),
        lambda: UIState.set_module("PnL"),
    ],
)

app.add_page(
    risk_measures_page,
    route="/risk/risk-measures",
    on_load=[
        AuthState.load_user_from_cookie,           # ← NEW
        AuthState.check_module_access("Risk"),      # ← NEW
        RiskState.load_risk_data,
        lambda: UIState.set_module("Risk"),
        lambda: UIState.set_subtab("Risk Measures"),
    ],
)
```

### 6.3. Level 2: `rx.cond` Conditional Rendering

For pages that should show different content based on roles:

```python
def risk_page():
    return rx.cond(
        AuthState.is_authenticated,
        # Authenticated content
        rx.vstack(
            rx.heading("Risk Dashboard"),
            rx.text(f"Welcome, {AuthState.display_name}"),
            # ... page content
        ),
        # Fallback (should rarely display due to on_load guard)
        rx.text("Redirecting..."),
    )
```

### 6.4. Level 3: Navigation Filtering

Only show sidebar links the user has access to:

```python
def sidebar_nav():
    return rx.vstack(
        # Always visible
        rx.link("Market Data", href="/market-data"),

        # Conditionally visible based on role
        rx.cond(
            AuthState.allowed_modules.contains("PnL"),
            rx.link("PnL", href="/pnl"),
        ),
        rx.cond(
            AuthState.allowed_modules.contains("Risk"),
            rx.link("Risk", href="/risk"),
        ),
        rx.cond(
            AuthState.allowed_modules.contains("Orders"),
            rx.link("Orders", href="/orders"),
        ),
        # ... etc.
    )
```

### 6.5. Module → Route Mapping

| Module | Routes | Typical Roles |
|:---|:---|:---|
| PnL | `/pnl/*` | trader, risk, admin |
| Positions | `/positions/*` | trader, risk, admin |
| Market Data | `/market-data/*` | all |
| Risk | `/risk/*` | risk, admin |
| Recon | `/recon/*` | ops, admin |
| Compliance | `/compliance/*` | ops, admin |
| Portfolio Tools | `/portfolio-tools/*` | ops, trader, admin |
| Instruments | `/instruments/*` | trader, risk, admin |
| Events | `/events/*` | trader, ops, admin |
| Operations | `/operations/*` | ops, admin |
| Orders | `/orders/*` | trader, admin |

---

## 7. User Action Control

Beyond page visibility, specific **actions** (buttons, data modifications) should be controlled per role.

### 7.1. Strategy

```
Level 1: UI — disable/hide buttons based on role
Level 2: Backend — validate permissions in event handlers before executing
```

> [!IMPORTANT]
> **Level 2 is mandatory.** Disabling a button in the UI is cosmetic — a skilled user could still trigger the event via browser dev tools. The event handler must validate.

### 7.2. Action Permissions Config

```python
# app/states/auth/permissions.py  (conceptual)

# Actions that require specific roles
ACTION_PERMISSIONS: dict[str, list[str]] = {
    "rerun_operation":     ["ops", "admin"],
    "kill_operation":      ["ops", "admin"],
    "submit_order":        ["trader", "admin"],
    "modify_restricted":   ["compliance", "admin"],
    "approve_trade":       ["risk", "admin"],
    "edit_instrument":     ["ops", "admin"],
    "export_data":         ["trader", "risk", "ops", "admin"],
    "view_only":           ["readonly", "trader", "risk", "ops", "admin"],
}
```

### 7.3. Backend Validation (Event Handlers)

```python
# Example: in operations state
class OperationsState(rx.State):

    @rx.event
    def rerun_operation(self, operation_id: str):
        # ← MUST validate before executing
        auth = self.get_state(AuthState)
        if auth.user_role not in ACTION_PERMISSIONS.get("rerun_operation", []):
            return rx.toast.error("Permission denied: you cannot rerun operations")

        # Proceed with the operation
        self._do_rerun(operation_id)
        return rx.toast.success(f"Operation {operation_id} rerun started")
```

### 7.4. UI Action Control (Buttons)

```python
# Example: conditionally enable/disable action buttons
def operation_actions(operation_id: str):
    return rx.hstack(
        # Rerun button — only visible to ops/admin
        rx.cond(
            AuthState.user_role.is_in(["ops", "admin"]),
            rx.button(
                "Rerun",
                on_click=OperationsState.rerun_operation(operation_id),
                color_scheme="blue",
            ),
        ),

        # Kill button — only visible to ops/admin
        rx.cond(
            AuthState.user_role.is_in(["ops", "admin"]),
            rx.button(
                "Kill",
                on_click=OperationsState.kill_operation(operation_id),
                color_scheme="red",
            ),
        ),

        # Export — available to most roles
        rx.button(
            "Export",
            on_click=OperationsState.export_data(),
        ),
    )
```

### 7.5. AG Grid Context Menu Integration

Since the project already has AG Grid context menus (from a previous task), action control should extend there:

```python
# Conceptual: filter context menu items based on role
def get_context_menu_items(role: str) -> list:
    items = [
        {"name": "View Details", "action": "viewDetails"},
        {"name": "Export Row", "action": "exportRow"},
    ]
    if role in ["ops", "admin"]:
        items.extend([
            {"name": "Rerun", "action": "rerun"},
            {"name": "Kill", "action": "kill"},
        ])
    if role in ["trader", "admin"]:
        items.append({"name": "Submit Order", "action": "submitOrder"})
    return items
```

---

## 8. WebSocket Session Strategy

### The Problem

Reflex uses WebSockets for all state updates. The Windows auth token is only available during HTTP requests — not reliably on WebSocket connections.

### The Solution: Cookie-Based Session

```
Step 1: Browser loads page → IIS authenticates (Windows Auth)
Step 2: FastAPI middleware decodes token → sets signed session cookie
Step 3: All subsequent requests (including WS upgrade) carry the cookie
Step 4: AuthState.load_user_from_cookie reads identity on page load
Step 5: Identity persists for the entire WS session
```

This works because:
- **Cookies are sent on WebSocket upgrade** requests (unlike custom headers)
- The cookie is **signed** with `itsdangerous` — can't be tampered with
- 8-hour expiration aligns with a trading day

### Sequence Diagram

```
Browser          IIS                 FastAPI Middleware      AuthState
  │                │                        │                    │
  │──GET /pnl────→│                        │                    │
  │                │──Win Auth (401→200)──→│                    │
  │                │  + WINAUTHTOKEN header │                    │
  │                │                        │──decode token──→  │
  │                │                        │  set cookie        │
  │←──HTML + cookie─────────────────────────│                    │
  │                │                        │                    │
  │──WS upgrade──→│                        │                    │
  │  (cookie sent) │────────────────────→  │                    │
  │                │                        │──read cookie──→   │
  │                │                        │                    │──load_user
  │                │                        │                    │  set role
  │←──WS connected──────────────────────────────────────────────│
  │                │                        │                    │
  │  (all state updates flow over WS, identity persists)        │
```

---

## 9. Security Considerations

### Token Handle Safety
- `MS-ASPNETCORE-WINAUTHTOKEN` is a kernel handle — not spoofable
- **Must call `CloseHandle`** after use to prevent resource leaks
- Token is process-local — only valid within the Python process IIS manages

### Cookie Security
| Property | Value | Why |
|:---|:---|:---|
| `HttpOnly` | `true` | Prevent JavaScript access (XSS protection) |
| `Secure` | `true` (when HTTPS) | Only sent over encrypted connections |
| `SameSite` | `Strict` | Prevent CSRF attacks |
| `max_age` | `28800` (8 hours) | Trading day alignment |
| **Signed** | `itsdangerous` | Prevent tampering |

### Backend-Only Variables
```python
class AuthState(rx.State):
    _session_token: str = ""   # ← prefixed with _ = backend-only
    current_user: str = ""     # ← visible to frontend (for display)
```

### Data-Level Protection
- Every event handler that returns sensitive data **must** check `AuthState.user_role`
- Every computed var that exposes data **must** validate permissions
- `rx.cond` is UI-only — it does not protect the data itself

---

## 10. File Changes Summary

| File | Change | Type |
|:---|:---|:---|
| `web.config` | HttpPlatformHandler + Windows Auth config (prod only) | NEW |
| `.env.example` | Template for dev mode env vars | NEW |
| `.gitignore` | Add `.env` to ignored files | MODIFY |
| `rxconfig.py` | Read `PORT` env var for IIS integration | MODIFY |
| `app/utils/windows_auth.py` | Token decoder utility (prod only) | NEW |
| `app/middleware/auth_middleware.py` | FastAPI middleware — dev/prod dual mode | NEW |
| `app/states/auth/auth_state.py` | AuthState with user identity and RBAC | NEW |
| `app/states/auth/permissions.py` | Role → module and action permission maps | NEW |
| `app/app.py` | Add `api_transformer`, add `on_load` guards to all routes | MODIFY |
| Navigation component(s) | Filter menu items by `AuthState.allowed_modules` | MODIFY |
| Event handlers (various states) | Add permission checks before actions | MODIFY |
| `pyproject.toml` | Add `itsdangerous`, `python-dotenv`; optional `pywin32` | MODIFY |

---

## 11. Next Steps Checklist

### Local Dev Setup (do first)
- [ ] Create `.env.example` with dev mode template
- [ ] Add `.env` to `.gitignore`
- [ ] Add `itsdangerous` and `python-dotenv` to `pyproject.toml`
- [ ] Create `app/middleware/auth_middleware.py` — dual-mode middleware
- [ ] Create `app/states/auth/auth_state.py` — AuthState
- [ ] Create `app/states/auth/permissions.py` — permission maps
- [ ] Modify `app/app.py` — add `api_transformer` + `on_load` guards
- [ ] Test dev mode: `PMT_AUTH_MODE=dev` + `uv run reflex run`
- [ ] Test role switching: change `PMT_DEV_ROLE` and verify page/action changes

### Production Infrastructure
- [ ] Verify HttpPlatformHandler is installed on target Server 2019
- [ ] Enable WebSocket Protocol in IIS features
- [ ] Enable Windows Authentication role service
- [ ] Install `pywin32` in deployment Python env (`pip install .[iis]`)

### Production Implementation
- [ ] Create `web.config` with HttpPlatformHandler config
- [ ] Update `rxconfig.py` to read `PORT` env var
- [ ] Create `app/utils/windows_auth.py` — token decoder
- [ ] Update navigation component — filter by `allowed_modules`
- [ ] Add permission checks to event handlers (operations, orders, etc.)

### Testing
- [ ] Test dev mode: page guards, action controls, role switching
- [ ] Test on local IIS (dev machine) with Windows Auth
- [ ] Test WebSocket session persistence (cookie-based)
- [ ] Test page guards — unauthorized user redirected
- [ ] Test action control — unauthorized action shows error toast
- [ ] Test cookie expiration and re-authentication
- [ ] Deploy to target Server 2019 and test with domain users

---

## References

- [HttpPlatformHandler Configuration (Microsoft)](https://learn.microsoft.com/en-us/iis/extensions/httpplatformhandler/httpplatformhandler-configuration-reference)
- [IIS Windows Authentication (Microsoft)](https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/authentication/windowsAuthentication/)
- [Configuring Python on IIS (Microsoft)](https://learn.microsoft.com/en-us/visualstudio/python/configure-web-apps-for-iis-windows)
- [pywin32 on PyPI](https://pypi.org/project/pywin32/)
- [itsdangerous (Pallets)](https://itsdangerous.palletsprojects.com/)
- [Reflex API Transformer](https://reflex.dev/docs/api-routes/api-transformer/)
- [Reflex Authentication](https://reflex.dev/docs/authentication/)
- [HTTP Bridge Module (HttpPlatformHandler alternative)](https://github.com/nickcimino/http-bridge-module)
