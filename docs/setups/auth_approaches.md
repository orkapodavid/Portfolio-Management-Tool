# Alternative Authentication Approaches (Reference)

> **Status**: Reference only — these are **not recommended** as the primary approach for this project.  
> **Primary plan**: See [windows_iis_auth.md](./windows_iis_auth.md) for the recommended HttpPlatformHandler approach.

---

## 1. IIS Reverse Proxy + Custom C# HTTP Module

Use this if you prefer to run Reflex independently (not managed by IIS) and use IIS purely as a reverse proxy.

### How It Works

1. Reflex runs independently (e.g., `uv run reflex run` on port 8000)
2. IIS uses **ARR + URL Rewrite** to reverse-proxy to `localhost:8000`
3. A small **C# HTTP Module** (~30 lines) hooks `PostAuthenticateRequest` and injects `X-Remote-User: DOMAIN\username` as a header
4. Reflex/FastAPI middleware reads the header

### Why Not Just URL Rewrite Alone?

> [!WARNING]
> Microsoft's URL Rewrite `serverVariables` execute **before** Windows Authentication in the IIS pipeline. The `{LOGON_USER}` variable is **empty** at that point. This is a well-known limitation.

### Conceptual C# Module

```csharp
// WindowsAuthHeaderModule.cs
using System;
using System.Web;

public class WindowsAuthHeaderModule : IHttpModule
{
    public void Init(HttpApplication app)
    {
        app.PostAuthenticateRequest += OnPostAuth;
    }

    private void OnPostAuth(object sender, EventArgs e)
    {
        var app = (HttpApplication)sender;
        var user = app.Context.User?.Identity?.Name;
        if (!string.IsNullOrEmpty(user))
        {
            app.Context.Request.Headers.Set("X-Remote-User", user);
        }
    }

    public void Dispose() { }
}
```

### IIS Setup

```
Prerequisites:
  ✅ ARR 3.0 (free download)
  ✅ URL Rewrite 2.1 (free download)
  ✅ .NET Framework (already on Server 2019)

Steps:
  1. Compile: csc /target:library WindowsAuthHeaderModule.cs
  2. Place DLL in IIS site's bin/ folder
  3. Register module in web.config
  4. Set up ARR reverse proxy rule to localhost:8000
  5. Disable Anonymous Auth, enable Windows Auth
```

### Pros / Cons

| Pros | Cons |
|:---|:---|
| Reflex runs independently | Need C# DLL to compile and maintain |
| Familiar reverse proxy pattern | Header spoofing risk (must strip headers) |
| Plain-text username | Two processes to manage (IIS + Reflex) |
| | WebSocket header forwarding may be unreliable |

---

## 2. Helicon ISAPI_Rewrite 3 Lite

- **What**: Third-party ISAPI filter (free Lite version) that runs after auth in the IIS pipeline
- **Why not primary**: Third-party dependency, may not be approved in enterprise environments
- **When useful**: Quick prototyping without writing C# code

---

## 3. pyspnego (Native NTLM/Kerberos in Python)

- **What**: Python handles NTLM/Kerberos negotiation directly using `pyspnego` library, skipping IIS auth
- **PyPI**: `pyspnego` (requires `cryptography`, `sspilib` on Windows)
- **Why not primary**: No pre-built ASGI middleware exists. Complex multi-round-trip NTLM handshake. Must implement from scratch.
- **When useful**: If deploying without IIS entirely (e.g., Linux)

---

## 4. Azure AD / Entra ID OAuth

- **What**: Use `reflex-azure-auth` package for Microsoft OAuth login
- **Existing skill**: `.agents/skills/reflex-dev/references/reflex-azure-auth.mdc`
- **Why not primary**: Not transparent SSO (users must click login), requires Azure AD tenant + internet
- **When useful**: Cloud/hybrid deployments, MFA requirements, off-domain users

### Key Patterns (from existing skill)

```python
# Protected page pattern
from reflex_azure_auth import AzureAuthState, azure_login_button

def protected_page():
    return rx.cond(
        AzureAuthState.userinfo,
        rx.text(f"Welcome, {AzureAuthState.userinfo['name']}!"),
        azure_login_button(rx.button("Login with Microsoft")),
    )
```

---

## 5. URL Rewrite `serverVariables` (Direct)

- **What**: Use IIS URL Rewrite to set `{LOGON_USER}` into a header
- **Why not usable**: **Does not work** for Windows Auth — URL Rewrite fires before authentication, header arrives empty
- **Known issue**: Confirmed by Microsoft docs and StackOverflow

---

## Comparison Matrix

| Criteria | C# HTTP Module | Helicon ISAPI | pyspnego | Azure AD |
|:---|:---|:---|:---|:---|
| **Transparent SSO** | ✅ | ✅ | ✅ | ⚠️ One-click |
| **Third-party free** | ✅ | ❌ | ✅ | ✅ |
| **Setup complexity** | Medium | Medium | High | Medium |
| **Spoofing risk** | ⚠️ Header | ⚠️ Header | ✅ None | ✅ JWT |
| **WebSocket compat** | ⚠️ Cookie workaround | ⚠️ Cookie workaround | ⚠️ Custom | ✅ Native |
| **Works off-domain** | ❌ | ❌ | ❌ | ✅ |
