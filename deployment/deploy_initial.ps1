<#
.SYNOPSIS
    Performs the INITIAL deployment on the offline Windows Server 2019.

.DESCRIPTION
    1. Verifies prerequisites (IIS modules, features).
    2. Sets up the directory structure.
    3. Bootstraps 'uv'.
    4. Creates a Virtual Environment (.venv) and installs deps (Offline).
    5. Deploys Static Frontend to IIS.
    6. Sets up WinSW Service for Backend (FastAPI).
    7. Configures IIS (Reverse Proxy + Static Files).

.NOTES
    Run as Administrator.
    Ensure C:\Apps\Software contains: uv.exe, WinSW*.exe, node.exe
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$PackageRoot = "$ScriptDir\.."

# --- Configuration ---
$AppName = "ReflexPMT"
$AppRoot = "C:\Inetpub\wwwroot\$AppName"
$LogDir = "$AppRoot\logs"
$IISSiteName = "ReflexPMT" # We will create a new site or app?
# User wants https://hcma.ds.susq.com/pmt
# We will create an Application "/pmt" under "Default Web Site" (or appropriate site).
$BaseSiteName = "Default Web Site"
$AppPath = "/pmt"
$LocalSoftwareCache = "C:\Apps\Software"

Write-Host "Starting Initial Deployment for $AppName..." -ForegroundColor Cyan

# --- 0. Verify Prerequisites ---
Write-Host "Verifying Prerequisites..." -ForegroundColor Cyan
Import-Module WebAdministration -ErrorAction Stop

# Check URL Rewrite Module
$urlRewriteInstalled = Test-Path "C:\Windows\System32\inetsrv\rewrite.dll"
if (-not $urlRewriteInstalled) {
    Write-Error "IIS URL Rewrite Module is not installed. Please install it first.`nDownload from: https://www.iis.net/downloads/microsoft/url-rewrite`nOr copy the installer from $LocalSoftwareCache if available."
}
Write-Host "[OK] URL Rewrite Module found" -ForegroundColor Green

# Check Application Request Routing (ARR)
$arrInstalled = Test-Path "C:\Program Files\IIS\Application Request Routing\requestRouter.dll"
if (-not $arrInstalled) {
    Write-Error "IIS Application Request Routing (ARR) is not installed. Please install it first.`nDownload from: https://www.iis.net/downloads/microsoft/application-request-routing`nOr copy the installer from $LocalSoftwareCache if available."
}
Write-Host "[OK] Application Request Routing (ARR) found" -ForegroundColor Green

# Check WebSocket Protocol
$webSocketFeature = Get-WindowsFeature -Name Web-WebSockets -ErrorAction SilentlyContinue
if ($webSocketFeature -and -not $webSocketFeature.Installed) {
    Write-Warning "Web-WebSockets feature not installed. Installing..."
    Install-WindowsFeature -Name Web-WebSockets
}
Write-Host "[OK] WebSocket Protocol feature verified" -ForegroundColor Green

# Enable ARR Proxy (required for URL Rewrite reverse proxy to work)
Write-Host "Enabling ARR Proxy..." -ForegroundColor Cyan
try {
    Set-WebConfigurationProperty -Filter "system.webServer/proxy" -Name "enabled" -Value "true" -PSPath "IIS:\" -ErrorAction Stop
    Write-Host "[OK] ARR Proxy enabled" -ForegroundColor Green
}
catch {
    Write-Warning "Could not enable ARR proxy automatically. You may need to enable it manually in IIS Manager -> Server -> Application Request Routing Cache -> Server Proxy Settings -> Enable proxy."
}

# --- 1. Directory Setup ---
Write-Host "Setting up directories..." -ForegroundColor Cyan
if (-not (Test-Path $AppRoot)) {
    New-Item -ItemType Directory -Force -Path $AppRoot | Out-Null
}
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host "Copying files..."
Copy-Item "$PackageRoot\*" "$AppRoot" -Recurse -Force -Exclude "scripts"
Copy-Item "$PackageRoot\scripts" "$AppRoot" -Recurse -Force

Set-Location $AppRoot

# --- 2. Bootstrap uv & Install Deps (Backend) ---
Write-Host "Bootstrapping uv & Installing Backend Dependencies..." -ForegroundColor Cyan
$uvSrc = "$AppRoot\uv.exe"

# Verify uv.exe exists
if (-not (Test-Path $uvSrc)) {
    # Try to copy from local software cache
    $localUv = Join-Path $LocalSoftwareCache "uv.exe"
    if (Test-Path $localUv) {
        Copy-Item $localUv $uvSrc
        Write-Host "Copied uv.exe from $LocalSoftwareCache"
    }
    else {
        Write-Error "uv.exe not found in package or $LocalSoftwareCache"
    }
}

& $uvSrc venv .venv
& $uvSrc pip install --python "$AppRoot\.venv\Scripts\python.exe" --no-index --find-links "$AppRoot\wheels" -r requirements.txt

# --- 3. Database Setup ---
Write-Host "Initializing Database..." -ForegroundColor Cyan
$env:PATH = "$AppRoot\.venv\Scripts;$env:PATH"
$env:PMT_INTEGRATION_MODE = "mock"
reflex db init
reflex db migrate

# --- 4. Setup Static Frontend ---
Write-Host "Deploying Static Frontend..." -ForegroundColor Cyan
# Check for frontend_static folder
if (Test-Path "$AppRoot\frontend_static") {
    # We need to serve these files.
    # We can put them in $AppRoot\public
    New-Item -ItemType Directory -Force -Path "$AppRoot\public" | Out-Null
    Copy-Item "$AppRoot\frontend_static\*" "$AppRoot\public\" -Recurse -Force
    Write-Host "Frontend assets deployed to $AppRoot\public"
}
else {
    Write-Warning "frontend_static not found! Frontend might not load."
}

# --- 5. WinSW Service (Backend Only) ---
Write-Host "Setting up Backend Service (WinSW)..." -ForegroundColor Cyan
Copy-Item "$AppRoot\config\reflex_service.xml" "$AppRoot\reflex_service.xml"

$reflexServiceExe = "$AppRoot\reflex_service.exe"
if (-not (Test-Path $reflexServiceExe)) {
    # Try to copy from local software cache
    $LocalWinSW = Get-ChildItem "$LocalSoftwareCache\WinSW*.exe" | Select-Object -First 1
    if ($LocalWinSW) {
        Copy-Item $LocalWinSW.FullName $reflexServiceExe
        Write-Host "Copied WinSW from $LocalSoftwareCache"
    }
    else {
        Write-Error "reflex_service.exe (WinSW) not found in package or $LocalSoftwareCache"
    }
}

# Uninstall existing service if present (for reinstall scenarios)
$existingService = Get-Service "reflex_service" -ErrorAction SilentlyContinue
if ($existingService) {
    Write-Host "Removing existing service..."
    & $reflexServiceExe uninstall
    Start-Sleep -Seconds 2
}

& $reflexServiceExe install
Write-Host "Service Installed." -ForegroundColor Green

# --- 6. IIS Setup ---
Write-Host "Configuring IIS..." -ForegroundColor Cyan

# Check/Create Application
$existingApp = Get-WebApplication -Site $BaseSiteName -Name "pmt" -ErrorAction SilentlyContinue
if (-not $existingApp) {
    # Point the application to the PUBLIC folder (Static files)
    New-WebApplication -Name "pmt" -Site $BaseSiteName -PhysicalPath "$AppRoot\public"
    Write-Host "Created IIS Application '/pmt' pointing to static assets."
}
else {
    # Ensure physical path is correct
    Set-ItemProperty "IIS:\Sites\$BaseSiteName\pmt" -Name physicalPath -Value "$AppRoot\public"
    Write-Host "Updated IIS Application '/pmt' physical path."
}

# Apply Web.Config to the PUBLIC folder (where IIS serves from)
Copy-Item "$AppRoot\config\web.config" "$AppRoot\public\web.config"

# --- 7. Start Service and Verify ---
Write-Host "Starting Backend Service..." -ForegroundColor Cyan
Start-Service reflex_service

# Wait and verify service started successfully
Start-Sleep -Seconds 5
$svc = Get-Service "reflex_service"
if ($svc.Status -eq 'Running') {
    Write-Host "[OK] Service 'reflex_service' is running" -ForegroundColor Green
}
else {
    Write-Warning "Service 'reflex_service' status: $($svc.Status). Check logs at $LogDir"
}

# --- Finish ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Initial Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Application URL: https://hcma.ds.susq.com/pmt"
Write-Host "Backend Service: reflex_service (port 8000)"
Write-Host "Logs Directory: $LogDir"
Write-Host ""
Write-Host "To check service status: Get-Service reflex_service"
Write-Host "To view logs: Get-Content $LogDir\reflex_service.*.log -Tail 50"
