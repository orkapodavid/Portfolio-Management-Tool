# Windows Authentication for PMT (Reflex App) Behind IIS

> **Status**: Research / Brainstorming — no code changes proposed yet  
> **Date**: 2026-02-12  
> **Goal**: Identify the authenticated Windows user so the Reflex app can control page visibility and feature access per user/role.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Approach A – IIS Handles Auth, Forwards Username via Header](#2-approach-a--iis-handles-auth-forwards-username-via-header)
3. [Approach B – HttpPlatformHandler with `forwardWindowsAuthToken`](#3-approach-b--httpplatformhandler-with-forwardwindowsauthtoken)
4. [Approach C – Native NTLM/Kerberos in Python (`pyspnego`)](#4-approach-c--native-ntlmkerberos-in-python-pyspnego)
5. [Approach D – Azure AD / Entra ID OAuth (Existing Skill)](#5-approach-d--azure-ad--entra-id-oauth-existing-skill)
6. [How to Use the Identity in Reflex](#6-how-to-use-the-identity-in-reflex)
7. [WebSocket Caveats (Critical)](#7-websocket-caveats-critical)
8. [Security Considerations](#8-security-considerations)
9. [Comparison Matrix](#9-comparison-matrix)
10. [Recommendation](#10-recommendation)

---

## 1. Architecture Overview

```
┌────────────────────────────────────┐
│         Browser (Intranet)         │
│  (Windows user auto-authenticates) │
└──────────────┬─────────────────────┘
               │  HTTP + WebSocket
               ▼
┌────────────────────────────────────┐
│      IIS (Windows Server)          │
│  • Windows Authentication enabled  │
│  • ARR / URL Rewrite / HttpPlat.   │
│  • Forwards identity to backend    │
└──────────────┬─────────────────────┘
               │  Reverse proxy
               ▼
┌────────────────────────────────────┐
│      Reflex App                    │
│  • FastAPI backend (Python)        │
│  • React/Next.js frontend (SSR)    │
│  • WebSocket for state updates     │
└────────────────────────────────────┘
```

Reflex compiles to:
- **Frontend**: Next.js (served as static or SSR)
- **Backend**: FastAPI (Python), communicates with the frontend via **WebSockets**

The key challenge is that IIS must authenticate the user **and** relay the identity to the Reflex backend, including over WebSocket connections.

---

## 2. Approach A – IIS Handles Auth, Forwards Username via Header

### How It Works

1. **IIS performs Windows Authentication** (Negotiate/NTLM/Kerberos). Anonymous auth is disabled.
2. After authentication, IIS knows the user as the `LOGON_USER` / `REMOTE_USER` server variable (e.g., `DOMAIN\username`).
3. **IIS URL Rewrite** or an **ISAPI filter** injects a custom HTTP header (e.g., `X-Remote-User`) into the proxied request.
4. The Reflex/FastAPI backend reads that header.

### IIS Configuration (High Level)

```
Modules needed:
  ✅ Application Request Routing (ARR)
  ✅ URL Rewrite
  ✅ Windows Authentication (role service)

Steps:
  1. Disable Anonymous Authentication on the IIS site
  2. Enable Windows Authentication
  3. Set up a URL Rewrite inbound rule to reverse-proxy to http://localhost:8000 (Reflex)
  4. Add a server variable to inject the authenticated user into a header
```

### The REMOTE_USER Timing Problem

> [!WARNING]
> **Known issue**: IIS URL Rewrite `serverVariables` execute **before** authentication completes in the pipeline. This means `REMOTE_USER` / `LOGON_USER` may be **empty** when URL Rewrite processes the request.

#### Workarounds

| Workaround | Description | Complexity |
|:---|:---|:---|
| **Helicon ISAPI_Rewrite 3 Lite** | Third-party ISAPI filter that runs *after* auth. Can inject `X-Remote-User` header. Free Lite version available. | Medium |
| **Custom IIS HTTP Module** (C#) | Write a small managed module (`IHttpModule`) that runs in `PostAuthenticateRequest` and sets a header. | Medium-High |
| **Two-hop setup** | First IIS site authenticates, second forwards. Complex and fragile. | High |

### Pros
- Transparent SSO — users never see a login prompt
- IIS does all the heavy lifting
- Works with existing AD infrastructure

### Cons
- The REMOTE_USER timing problem requires a workaround
- Header-based identity is vulnerable to spoofing if not properly secured
- **WebSocket connections may not receive the header** (see Section 7)

---

## 3. Approach B – HttpPlatformHandler with `forwardWindowsAuthToken`

### How It Works

Instead of ARR reverse proxy, IIS uses **HttpPlatformHandler** to launch the Python process directly and forward a Windows auth token.

1. IIS receives the request and performs Windows Authentication.
2. `HttpPlatformHandler` starts the Python process (e.g., `uv run reflex run`) and passes a **Windows auth token handle** via the `MS-ASPNETCORE-WINAUTHTOKEN` request header.
3. The Python backend can decode this token using Win32 APIs.

### web.config Example (Concept)

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="httpPlatformHandler"
           path="*" verb="*"
           modules="httpPlatformHandler"
           resourceType="Unspecified" />
    </handlers>
    <httpPlatform processPath="C:\path\to\python.exe"
                  arguments="-m uvicorn app:app --port %HTTP_PLATFORM_PORT%"
                  stdoutLogEnabled="true"
                  forwardWindowsAuthToken="true">
      <environmentVariables>
        <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>
```

### Token Handling in Python

The `MS-ASPNETCORE-WINAUTHTOKEN` header contains a **Windows token handle** (an integer). You'd use `pywin32` (specifically `win32security`) to:

1. Open the token handle
2. Call `GetTokenInformation` to extract the user SID
3. Call `LookupAccountSid` to get `DOMAIN\username`

### Pros
- Most "native" Windows integration — you get a real Windows token
- No header spoofing risk (it's a kernel handle, not a string)
- No ISAPI filter or custom module needed

### Cons
- Requires `pywin32` dependency
- Token handle is **process-local** — it only works for the same server process
- More complex to integrate with Reflex's process model
- `HttpPlatformHandler` vs `ASP.NET Core Module` confusion in docs
- **WebSocket token forwarding is unconfirmed** for this approach

---

## 4. Approach C – Native NTLM/Kerberos in Python (`pyspnego`)

### How It Works

Skip IIS authentication entirely. The Python app itself handles NTLM/Kerberos negotiation using the `pyspnego` library.

1. Browser sends `Authorization: Negotiate <token>` header.
2. FastAPI/Starlette middleware uses `pyspnego` to accept the token.
3. `pyspnego` returns the authenticated username.
4. Middleware stores the username in the request state.

### Key Library: `pyspnego`

- **PyPI**: `pyspnego`
- **Purpose**: Abstracts NTLM/Kerberos on both Windows (SSPI) and Linux (GSSAPI)
- **Requirements**: Python 3.9+, `cryptography`, `sspilib` (Windows)

### Pros
- Full control in Python, no IIS auth dependency
- Works with any ASGI server (uvicorn, hypercorn)
- Could potentially handle WebSocket auth at connection time

### Cons
- Must implement SPNEGO challenge/response middleware from scratch
- Multi-round-trip NTLM handshake is complex
- Kerberos requires SPN and keytab configuration
- Browsers may not send `Negotiate` header unless site is in the Intranet zone
- No pre-built Reflex or FastAPI middleware exists — custom development required

---

## 5. Approach D – Azure AD / Entra ID OAuth (Existing Skill)

### How It Works

Use `reflex-azure-auth` (already documented in the project skill at `.agents/skills/reflex-dev/references/reflex-azure-auth.mdc`) to authenticate via Azure AD / Microsoft Entra ID.

1. User visits the app → redirected to Microsoft login.
2. After OAuth flow, the app gets an ID token with user claims (name, email, etc.).
3. `AzureAuthState` provides `is_authenticated`, `userinfo`, and role checking.

### Pros
- Already has a Reflex integration (`reflex-azure-auth` package)
- Well-documented patterns for protected pages, RBAC, and conditional nav
- Works regardless of deployment (IIS, Docker, cloud)
- No WebSocket concerns — auth is token-based via cookies
- Supports MFA, conditional access policies

### Cons
- **Not transparent SSO** — users must click "Login with Microsoft" (though can be auto-triggered)
- Requires Azure AD App Registration setup
- Requires internet connectivity to validate tokens
- Users not in Azure AD cannot authenticate

### Hybrid Possibility

Use IIS Windows Auth to get the username, then look up that user in Azure AD to get roles/groups. This gives transparent SSO + rich role data.

---

## 6. How to Use the Identity in Reflex

Regardless of which approach provides the username, here's how the Reflex app can use it:

### 6.1 Auth State

```python
# Conceptual — not actual implementation
class AuthState(rx.State):
    """Stores the authenticated user and their permissions."""
    current_user: str = ""          # e.g., "DOMAIN\\jsmith"
    user_role: str = ""             # e.g., "trader", "risk", "ops", "admin"
    allowed_modules: list[str] = [] # e.g., ["PnL", "Positions", "Risk"]
```

### 6.2 Loading the User (via `api_transformer` Middleware)

Reflex supports `api_transformer` to add custom FastAPI middleware:

```python
# Conceptual
from fastapi import FastAPI

api = FastAPI()

@api.middleware("http")
async def extract_windows_user(request, call_next):
    username = request.headers.get("X-Remote-User", "")
    # Store in a way accessible to Reflex State
    response = await call_next(request)
    return response

app = rx.App(api_transformer=api)
```

### 6.3 Page Visibility with `rx.cond`

```python
# Conceptual — show/hide content based on role
def risk_page():
    return rx.cond(
        AuthState.user_role.contains("risk"),
        rx.vstack(rx.heading("Risk Dashboard"), ...),
        rx.text("Access Denied — you do not have permission to view this page."),
    )
```

### 6.4 `on_load` Page Guards

```python
# Conceptual — redirect unauthorized users on page load
class AuthState(rx.State):
    def check_access(self, required_module: str):
        if required_module not in self.allowed_modules:
            return rx.redirect("/unauthorized")

app.add_page(
    risk_page,
    route="/risk",
    on_load=[AuthState.check_access("Risk")],
)
```

### 6.5 Role → Module Permission Mapping

```python
# Conceptual — a config or DB lookup
ROLE_PERMISSIONS = {
    "trader":   ["PnL", "Positions", "Market Data", "Orders"],
    "risk":     ["PnL", "Positions", "Risk", "Market Data"],
    "ops":      ["Recon", "Operations", "Compliance"],
    "admin":    ["*"],  # all modules
}
```

> [!IMPORTANT]
> **Reflex security note**: Client-side `rx.cond` only hides UI. Statically rendered content is still accessible in the HTML source. True protection must come from **backend validation** — ensure event handlers and data loaders check permissions before returning data.

---

## 7. WebSocket Caveats (Critical)

> [!CAUTION]
> This is the biggest technical risk for Approaches A, B, and C.

Reflex uses **WebSockets** for all state updates between the browser and the FastAPI backend. This creates a fundamental challenge:

### The Problem

| Step | HTTP Request | WebSocket |
|:---|:---|:---|
| Windows Auth challenge | ✅ Works (401 → Negotiate → 200) | ❌ No standard mechanism |
| Custom headers from IIS | ✅ Injected per-request | ⚠️ Only available during **WS upgrade** (initial handshake) |
| NTLM multi-round-trip | ✅ Works over HTTP | ❌ Not supported over WS |

**Key issues:**
1. **WebSocket connections do not repeat authentication**. The auth header is only present during the initial HTTP upgrade request.
2. **IIS may not forward custom headers** (like `X-Remote-User`) during the WebSocket upgrade.
3. **NTLM is connection-based** — each new connection requires re-authentication. WebSockets are long-lived, which may cause issues with NTLM timeouts.
4. **Windows Authentication is not supported with HTTP/2** — IIS falls back to HTTP/1.1.

### Mitigation Strategies

| Strategy | Description |
|:---|:---|
| **Cookie-based identity** | After initial HTTP auth, set a signed cookie with the username. Reflex/FastAPI reads the cookie on every request including WS upgrade. |
| **Token exchange** | IIS authenticates the user, then the app issues a JWT or session token. The frontend includes this token in the WS connection. |
| **Initial HTTP pre-flight** | Add a Reflex `on_load` event that calls a regular API endpoint (not WS) to fetch the username, then stores it in state. |
| **Approach D (Azure AD)** | Avoids the problem entirely — tokens are stored in cookies, which are sent on WS connections. |

---

## 8. Security Considerations

### Header Spoofing Prevention

If relying on `X-Remote-User` header from IIS:

- **Strip the header** from incoming client requests before IIS injects it. Use an IIS URL Rewrite outbound rule or request filtering to ensure clients cannot set `X-Remote-User` themselves.
- Only trust the header if the request comes from the **known IIS server IP** (loopback `127.0.0.1` if same machine).
- In FastAPI middleware, validate the header source.

### Cookie Security

If using a session cookie after the initial auth:
- Use `HttpOnly`, `Secure`, and `SameSite=Strict` flags
- Sign the cookie with a server-side secret (use `itsdangerous` or similar)
- Set a reasonable expiration (e.g., 8 hours for a trading day)

### Backend-Only Variables

Store sensitive user information in Reflex **backend-only vars** (`_variable`). These are never sent to the frontend:

```python
class AuthState(rx.State):
    _user_token: str = ""      # ← backend only, not visible to browser
    current_user: str = ""     # ← visible to frontend for display
```

---

## 9. Comparison Matrix

| Criteria | A: IIS + Header | B: HttpPlatformHandler | C: pyspnego | D: Azure AD |
|:---|:---|:---|:---|:---|
| **SSO Experience** | ✅ Transparent | ✅ Transparent | ✅ Transparent | ⚠️ One-click login |
| **Setup Complexity** | Medium | Medium-High | High | Medium |
| **WebSocket Compat** | ⚠️ Needs workaround | ⚠️ Unconfirmed | ⚠️ Needs workaround | ✅ Works natively |
| **Spoofing Risk** | ⚠️ Header spoofing | ✅ Kernel token | ✅ Direct auth | ✅ JWT/OAuth |
| **External Dependency** | ISAPI filter or C# module | `pywin32` | `pyspnego` | Azure AD tenant |
| **Reflex Integration** | Custom middleware | Custom middleware | Custom middleware | `reflex-azure-auth` pkg |
| **Works Off-Domain** | ❌ | ❌ | ❌ | ✅ |
| **Role/Group Support** | ❌ (needs LDAP/AD lookup) | ⚠️ (token has groups) | ⚠️ (needs LDAP) | ✅ (Azure AD groups) |
| **Maintenance** | Low | Medium | High | Low |

---

## 10. Recommendation

### Suggested Path: Approach D (Azure AD) with Optional IIS Pre-Auth

**For the quickest and most robust solution**, use **Approach D (Azure AD / Entra ID)**:

1. It already has a Reflex package (`reflex-azure-auth`) with documented patterns.
2. It avoids the WebSocket authentication problem entirely.
3. It supports role-based access from Azure AD groups.
4. The existing project skill already documents this flow.

**If transparent SSO is a hard requirement** (users must never see a login prompt):

1. Start with **Approach A (IIS + Header)** using the **Helicon ISAPI_Rewrite** workaround or a **custom IIS HTTP module**.
2. Use a **cookie-based identity** strategy to solve the WebSocket problem — after the initial HTTP request authenticates the user, set a signed session cookie that Reflex reads on WS connections.
3. Implement an LDAP/AD lookup to get group memberships for role-based access.

### Suggested Next Steps

- [ ] Decide: Is transparent SSO (no login click) a hard requirement?
- [ ] If Azure AD: Set up the App Registration and test `reflex-azure-auth`
- [ ] If IIS Windows Auth: Prototype the ISAPI filter or custom HTTP module approach
- [ ] Design the role ↔ module permission mapping (config file vs. AD groups vs. database)
- [ ] Implement `AuthState` with `on_load` guards and `rx.cond` visibility
- [ ] Test WebSocket behavior behind IIS with the chosen approach

---

## References

- [IIS Windows Authentication Overview (Microsoft)](https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/authentication/windowsAuthentication/)
- [HttpPlatformHandler Configuration (Microsoft)](https://learn.microsoft.com/en-us/iis/extensions/httpplatformhandler/httpplatformhandler-configuration-reference)
- [pyspnego on GitHub](https://github.com/jborean93/pyspnego)
- [Reflex Authentication Docs](https://reflex.dev/docs/authentication/)
- [Reflex API Transformer / Custom Middleware](https://reflex.dev/docs/api-routes/api-transformer/)
- [reflex-azure-auth Skill Reference](../../../.agents/skills/reflex-dev/references/reflex-azure-auth.mdc)
