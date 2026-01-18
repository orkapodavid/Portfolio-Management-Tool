<#
.SYNOPSIS
    Performs the INITIAL deployment on the offline Windows Server 2019.

.DESCRIPTION
    1. Verifies prerequisites.
    2. Sets up directory structure from Config.
    3. Bootstraps 'uv' & installs dependencies.
    4. Deploys Static Frontend to IIS.
    5. Sets up WinSW Service for Backend.
    6. Configures IIS (Reverse Proxy).
    7. Schedules Nightly Restart.

.NOTES
    Run as Administrator.
#>

$ScriptDir = $PSScriptRoot
Import-Module "$ScriptDir\deploy_utils.psm1" -Force

$ErrorActionPreference = "Stop"
$PackageRoot = "$ScriptDir\.."

# --- Load Configuration ---
try {
    $Config = Get-DeployConfig
    Write-Host "Starting Initial Deployment for $($Config.AppName)..." -ForegroundColor Cyan
}
catch {
    Write-Error "Failed to load configuration: $_"
    exit 1
}

# --- 0. Verify Prerequisites ---
Write-Log "Verifying Prerequisites..." "Cyan"

# Minimal check - users should run verify_prereqs.ps1 for full details
if (-not (Test-Path "$($Config.SoftwareCache)\uv.exe")) {
    Write-WarningLog "uv.exe not found in cache. Deployment may fail if not bundled."
}

# Enable ARR Proxy
Write-Log "Enabling ARR Proxy..." "Cyan"
try {
    Set-WebConfigurationProperty -Filter "system.webServer/proxy" -Name "enabled" -Value "true" -PSPath "IIS:\" -ErrorAction Stop
    Write-Success "ARR Proxy enabled"
}
catch {
    Write-WarningLog "Could not enable ARR proxy automatically. Check IIS settings."
}

# --- 1. Directory Setup ---
Write-Log "Setting up directories..." "Cyan"
if (-not (Test-Path $Config.AppRoot)) {
    New-Item -ItemType Directory -Force -Path $Config.AppRoot | Out-Null
    Write-Log "Created AppRoot: $($Config.AppRoot)"
}
New-Item -ItemType Directory -Force -Path $Config.LogDir | Out-Null

Write-Log "Copying files..."
Copy-Item "$PackageRoot\*" "$Config.AppRoot" -Recurse -Force -Exclude "scripts"
Copy-Item "$PackageRoot\scripts" "$Config.AppRoot" -Recurse -Force

Set-Location $Config.AppRoot

# --- 2. Bootstrap uv & Install Deps ---
Write-Log "Bootstrapping uv & Installing Backend Dependencies..." "Cyan"
$uvSrc = "$($Config.AppRoot)\uv.exe"

if (-not (Test-Path $uvSrc)) {
    $localUv = Join-Path $Config.SoftwareCache "uv.exe"
    if (Test-Path $localUv) {
        Copy-Item $localUv $uvSrc
        Write-Log "Copied uv.exe from cache."
    }
    else {
        Write-ErrorLog "uv.exe not found in package or cache."
        exit 1
    }
}

& $uvSrc venv .venv
& $uvSrc pip install --python "$($Config.AppRoot)\.venv\Scripts\python.exe" --no-index --find-links "$($Config.AppRoot)\wheels" -r requirements.txt

# --- 3. Database Setup ---
Write-Log "Initializing Database..." "Cyan"
$env:PATH = "$($Config.AppRoot)\.venv\Scripts;$env:PATH"
$env:PMT_INTEGRATION_MODE = "mock" # Initial setup default
reflex db init
reflex db migrate

# --- 4. Setup Static Frontend ---
Write-Log "Deploying Static Frontend..." "Cyan"
if (Test-Path "$($Config.AppRoot)\frontend_static") {
    New-Item -ItemType Directory -Force -Path "$($Config.AppRoot)\public" | Out-Null
    Copy-Item "$($Config.AppRoot)\frontend_static\*" "$($Config.AppRoot)\public\" -Recurse -Force
    Write-Success "Frontend assets deployed to public/"
}
else {
    Write-WarningLog "frontend_static not found!"
}

# --- 5. WinSW Service ---
Write-Log "Setting up Backend Service (WinSW)..." "Cyan"
Copy-Item "$($Config.AppRoot)\config\reflex_service.xml" "$($Config.AppRoot)\reflex_service.xml"

$reflexServiceExe = "$($Config.AppRoot)\reflex_service.exe"
if (-not (Test-Path $reflexServiceExe)) {
    $LocalWinSW = Get-ChildItem "$($Config.SoftwareCache)\WinSW*.exe" | Select-Object -First 1
    if ($LocalWinSW) {
        Copy-Item $LocalWinSW.FullName $reflexServiceExe
        Write-Log "Copied WinSW from cache."
    }
    else {
        Write-ErrorLog "WinSW not found."
    }
}

# Install Service
Install-WinSWService -ExePath $reflexServiceExe -UninstallExisting $true

# --- 6. IIS Setup ---
Write-Log "Configuring IIS..." "Cyan"
Ensure-IISApp -SiteName $Config.IISSiteName -AppPath $Config.IISAppPath -PhysicalPath "$($Config.AppRoot)\public"

# Apply Web.Config
Copy-Item "$($Config.AppRoot)\config\web.config" "$($Config.AppRoot)\public\web.config"

# --- 7. Start Service & Verify ---
Ensure-ServiceStarted -ServiceName $Config.ServiceName

# --- 8. Scheduled Restart (New) ---
Ensure-ScheduledRestart -TaskName $Config.TaskName -ServiceName $Config.ServiceName -Time $Config.TaskTime

# --- Finish ---
Write-Host ""
Write-Success "Initial Deployment Complete!"
Write-Log "Application URL: https://hcma.ds.susq.com$($Config.IISAppPath)"
Write-Log "Logs Directory: $($Config.LogDir)"
Write-Host ""

