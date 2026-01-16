<#
.SYNOPSIS
    Performs the INITIAL deployment on the offline Windows Server 2019.

.DESCRIPTION
    1. Sets up the directory structure.
    2. Bootstraps 'uv'.
    3. Creates a Virtual Environment (.venv) and installs deps (Offline).
    4. Deploys Static Frontend to IIS.
    5. Sets up WinSW Service for Backend (FastAPI).
    6. Configures IIS (Reverse Proxy + Static Files).

.NOTES
    Run as Administrator.
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

Write-Host "Starting Initial Deployment for $AppName..." -ForegroundColor Cyan

# --- 1. Directory Setup ---
if (-not (Test-Path $AppRoot)) {
    New-Item -ItemType Directory -Force -Path $AppRoot | Out-Null
}
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host "Copying files..."
Copy-Item "$PackageRoot\*" "$AppRoot" -Recurse -Force -Exclude "scripts"
Copy-Item "$PackageRoot\scripts" "$AppRoot" -Recurse -Force

Set-Location $AppRoot

# --- 2. Bootstrap uv & Install Deps (Backend) ---
Write-Host "Bootstrapping uv & Installing Backend Dependencies..."
$uvSrc = "$AppRoot\uv.exe"
& $uvSrc venv .venv
& $uvSrc pip install --no-index --find-links "$AppRoot\wheels" -r requirements.txt

# --- 3. Database Setup ---
Write-Host "Initializing Database..."
$env:PATH = "$AppRoot\.venv\Scripts;$env:PATH"
$env:PMT_INTEGRATION_MODE = "mock"
reflex db init
reflex db migrate

# --- 4. Setup Static Frontend ---
Write-Host "Deploying Static Frontend..."
# Check for frontend_static folder
if (Test-Path "$AppRoot\frontend_static") {
    # We need to serve these files.
    # We can put them in $AppRoot\public
    New-Item -ItemType Directory -Force -Path "$AppRoot\public" | Out-Null
    Copy-Item "$AppRoot\frontend_static\*" "$AppRoot\public\" -Recurse -Force
    Write-Host "Frontend assets deployed to $AppRoot\public"
} else {
    Write-Warning "frontend_static not found! Frontend might not load."
}

# --- 5. WinSW Service (Backend Only) ---
Write-Host "Setting up Backend Service (WinSW)..."
Copy-Item "$AppRoot\config\reflex_service.xml" "$AppRoot\reflex_service.xml"

if (Test-Path "$AppRoot\reflex_service.exe") {
    & "$AppRoot\reflex_service.exe" install
    Write-Host "Service Installed."
} else {
    Write-Warning "reflex_service.exe not found."
}

# --- 6. IIS Setup ---
Write-Host "Configuring IIS..."
Import-Module WebAdministration

# Check/Create Application
if (-not (Get-WebApplication -Site $BaseSiteName -Name $AppPath)) {
    # Point the application to the PUBLIC folder (Static files)
    New-WebApplication -Name "pmt" -Site $BaseSiteName -PhysicalPath "$AppRoot\public"
    Write-Host "Created IIS Application '/pmt' pointing to static assets."
} else {
    # Ensure physical path is correct
    Set-ItemProperty "IIS:\Sites\$BaseSiteName\pmt" -Name physicalPath -Value "$AppRoot\public"
}

# Apply Web.Config to the PUBLIC folder (where IIS serves from)
Copy-Item "$AppRoot\config\web.config" "$AppRoot\public\web.config"

# --- Finish ---
Write-Host "Initial Deployment Complete!" -ForegroundColor Green
Write-Host "Please start the backend service: Start-Service reflex_service"
